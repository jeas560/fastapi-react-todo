from fastapi import FastAPI, status
from sqlalchemy import create_engine, Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

# Criando uma instancia de engine sqlite
engine = create_engine("sqlite:///todoo.db")

# Criando uma metaclasse Declarative
Base = declarative_base()


# Definindo a classe ToDo, herdeira da classe Base
class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
    suggested_time = Column(Time)


# Criando a base de dados
Base.metadata.create_all(engine)

# Inicializa o app
app = FastAPI()


@app.get("/")
def root():
    return "App -- lista de coisas a fazer"


@app.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo():
    return "criar um item na lista"


@app.get("/todo/{id}")
def read_todo(id: int):
    return f"ler item da lista com id {id}"


@app.put("/todo/{id}")
def update_todo(id: int):
    return f"atualizar item da lista com id {id}"


@app.delete("/todo/{id}")
def delete_todo(id: int):
    return f"apagar ler item da lista com id {id}"


@app.get("/todo")
def read_todo_list():
    return "ler a lista completa de itens"
