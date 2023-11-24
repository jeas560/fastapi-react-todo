from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Criando uma instancia de engine sqlite
engine = create_engine("sqlite:///todoo.db")

# Criando uma metaclasse Declarative
Base = declarative_base()

# Criando uma classe SessionLocal de sessionmaker
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)