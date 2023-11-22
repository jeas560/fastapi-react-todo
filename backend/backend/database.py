from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Criando uma instancia de engine sqlite
engine = create_engine("sqlite:///todoo.db")

# Criando uma metaclasse Declarative
Base = declarative_base()
