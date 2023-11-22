from pydantic import BaseModel
from datetime import time
from typing import Union

# Criando a classe ToDoRequest, herdeira da classe BaseModel (Pydantic)
class ToDo(BaseModel):
    task: str
    suggested_time: Union[time, None] = None