from sqlalchemy import create_engine, text
from data_bases.model.declarative_base import Base, engine
import os

password = os.getenv('POSTGRES_PASSWORD')
port = os.getenv('POSTGRES_PORT')

# 1. Conectarse a DB existente
engine = create_engine(
    f'postgresql+psycopg2://postgres:{password}@localhost:{port}/postgres'
)

# 2. Crear nueva DB
with engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(
        text("CREATE DATABASE mi_base_de_datos")
    )

