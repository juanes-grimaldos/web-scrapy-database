from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

password = os.getenv('POSTGRES_PASSWORD')
port = os.getenv('POSTGRES_PORT')
db = os.getenv('POSTGRES_DB')
base_path = 'postgresql+psycopg2://postgres' # postgres is the default user
server = os.getenv('POSTGRES_SERVER')
engine = create_engine(f'{base_path}:{password}@localhost:{port}/{db}')
Session = sessionmaker(bind=engine)

Base = declarative_base()
session = Session()