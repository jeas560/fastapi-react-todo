from pydantic import BaseModel
from datetime import time
from typing import Union, Optional


# Criando a classe ToDoRequest, herdeira da classe BaseModel (Pydantic)
class ToDo(BaseModel):
    task: str
    suggested_time: Union[time, None] = None


class ToDoWithId(BaseModel):
    id: int
    task: str
    suggested_time: Union[time, None] = None

    class Config:
        from_attributes = True
