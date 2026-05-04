from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

password = os.getenv("POSTGRES_PASSWORD")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB")
server = os.getenv("POSTGRES_SERVER", "localhost")
user = os.getenv("POSTGRES_USER", "postgres")

engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}"
)

Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()