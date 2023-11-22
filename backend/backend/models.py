from sqlalchemy import Column, Integer, String, Time
from database import Base


# Definindo a classe ToDo, herdeira da classe Base
class ToDo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    task = Column(String(256))
    suggested_time = Column(Time, default=None)
