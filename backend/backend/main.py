from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas


# Criando a base de dados
Base.metadata.create_all(engine)

# Inicializa o app
app = FastAPI()


@app.get("/")
def root():
    return "App -- lista de tarefas"


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDo):
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Criando uma instancia do modelo de banco de dados ToDo
    tododb = models.ToDo(task=todo.task, suggested_time=todo.suggested_time)

    # Adicionando a instância e comitando
    session.add(tododb)
    session.commit()

    # Pegando a id dada ao objeto pela base de dados
    id = tododb.id

    # Encerrando a sessão
    session.close()

    return f"criado um item na lista com a id {id}"


@app.get("/todo/{id}")
def read_todo(id: int):
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Pegando o item pelo id da base de dados
    todo = session.query(models.ToDo).get(id)

    # Encerrando a sessão
    session.close()

    # Verificando se o item existe ao ser procurado pelo id
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if not todo:
        raise HTTPException(status_code=404, detail=f"item com o {id} não encontrado")

    return todo


@app.put("/todo/{id}")
def update_todo(id: int, todo_mod: schemas.ToDo):
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Pegando um item pelo id na base de dados
    todo = session.query(ToDo).get(id)

    # Atualizar um item com as novas informações (caso for encontrado)
    if todo:
        todo.task = todo_mod.task
        todo.suggested_time = todo_mod.suggested_time
        session.commit()

    # Encerrando a sessão
    session.close()

    # Verificando se o item existe ao ser procurado pelo id
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if not todo:
        raise HTTPException(status_code=404, detail=f"item com o {id} não encontrado")

    return todo


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Pegando um item pelo id na base de dados
    todo = session.query(models.ToDo).get(id)

    # Caso o item for encontrado ele será excluído do banco de dados
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"item com o {id} não encontrado")

    return None


@app.get("/todo")
def read_todo_list():
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Pegando todos os itens do banco
    todo_list = session.query(models.ToDo).all()

    # Encerrando a sessão
    session.close()

    return todo_list
