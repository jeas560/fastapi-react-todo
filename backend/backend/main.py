from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas
from typing import List


# Criando a base de dados
Base.metadata.create_all(engine)


# Função auxiliar para obter sessão de banco de dados
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# Inicializa o app
app = FastAPI()


@app.get("/")
def root():
    return "App -- lista de tarefas"


@app.post(
    "/todo", response_model=schemas.ToDoWithId, status_code=status.HTTP_201_CREATED
)
def create_todo(todo: schemas.ToDo, session: Session = Depends(get_session)):
    # Criando uma instancia do modelo de banco de dados ToDo
    tododb = models.ToDo(task=todo.task, suggested_time=todo.suggested_time)

    # Adicionando a instância e comitando
    session.add(tododb)
    session.commit()

    # Pegando a id dada ao objeto pela base de dados
    session.refresh(tododb)

    return tododb


@app.get("/todo/{id}", response_model=schemas.ToDoWithId)
def read_todo(id: int, session: Session = Depends(get_session)):
    # Pegando o item pelo id da base de dados
    todo = session.query(models.ToDo).get(id)

    # Verificando se o item existe ao ser procurado pelo id
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if not todo:
        raise HTTPException(
            status_code=404, detail=f"item com o id: {id}, não encontrado"
        )

    return todo


@app.put("/todo/{id}", response_model=schemas.ToDoWithId)
def update_todo(id: int, todo: schemas.ToDo, session: Session = Depends(get_session)):
    # Pegando um item pelo id na base de dados
    todo_mod = session.query(models.ToDo).get(id)

    # Atualizar um item com as novas informações (caso for encontrado)
    if todo_mod:
        todo_mod.task = todo.task
        todo_mod.suggested_time = todo.suggested_time
        session.commit()

    # Verificando se o item existe ao ser procurado pelo id
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if not todo_mod:
        raise HTTPException(
            status_code=404, detail=f"item com o id: {id}, não encontrado"
        )

    return todo_mod


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, session: Session = Depends(get_session)):
    # Pegando um item pelo id na base de dados
    todo = session.query(models.ToDo).get(id)

    # Caso o item for encontrado ele será excluído do banco de dados
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if todo:
        session.delete(todo)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"item com o id: {id}, não encontrado"
        )

    return None


@app.get("/todo", response_model=List[schemas.ToDoWithId])
def read_todo_list(session: Session = Depends(get_session)):
    # Pegando todos os itens do banco
    todo_list = session.query(models.ToDo).all()

    return todo_list
