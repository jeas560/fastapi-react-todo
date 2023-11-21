from fastapi import FastAPI, status, HTTPException 
from database import Base, engine, ToDo
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import time
from typing import Union


# Criando a classe ToDoRequest, herdeira da classe BaseModel
class ToDoRequest(BaseModel):
    task: str
    suggested_time: Union[time, None] = None


# Criando a base de dados
Base.metadata.create_all(engine)

# Inicializa o app
app = FastAPI()


@app.get("/")
def root():
    return "App -- lista de coisas a fazer"


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: ToDoRequest):
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Criando uma instancia do modelo de banco de dados ToDo
    tododb = ToDo(task=todo.task, suggested_time=todo.suggested_time)

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
    todo = session.query(ToDo).get(id)

    # Encerrando a sessão
    session.close()

    # Verificando se o item existe ao ser procurado pelo id.
    # Se não, levanta uma exceção e retorna 404: não encontrado
    if not todo:
        raise HTTPException(status_code=404, detail=f"item com o {id} não encontrado")
    
    return todo


@app.put("/todo/{id}")
def update_todo(id: int):
    return f"atualizar item da lista com id {id}"


@app.delete("/todo/{id}")
def delete_todo(id: int):
    return f"apagar ler item da lista com id {id}"


@app.get("/todo")
def read_todo_list():
    # Criando uma nova sessão da base de dados
    session = Session(bind=engine, expire_on_commit=False)

    # Pegando todos os itens do banco
    todo_list = session.query(ToDo).all()

    # Encerrando a sessão
    session.close()

    return todo_list
