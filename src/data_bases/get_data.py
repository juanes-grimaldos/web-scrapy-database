from sqlalchemy import create_engine
import os
import pandas as pd

if __name__ == '__main__':
  password = os.getenv('POSTGRES_PASSWORD')
  port = os.getenv('POSTGRES_PORT')
  db = os.getenv('POSTGRES_DB')
  base_path = 'postgresql+psycopg2://postgres' # postgres is the default user
  server = os.getenv('POSTGRES_SERVER')
  engine = create_engine(f'{base_path}:{password}@localhost:{port}/{db}')

  df = pd.read_sql(
      "SELECT * FROM public.fridges WHERE seller = 'Alkosto'",
      engine
  )

  print(df.head())

