from sqlalchemy import create_engine
import os
import pandas as pd

if __name__ == '__main__':
    password = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB")
    server = os.getenv("POSTGRES_SERVER", "localhost")
    user = os.getenv("POSTGRES_USER", "postgres")

    print(password)
    print(port)
    print(db)
    print(server)
    print(user)

    is_prod = server != "localhost"

    ssl_part = "?sslmode=require" if is_prod else ""

    DATABASE_URL = (
        f"postgresql+psycopg2://{user}:{password}@{server}:{port}/{db}{ssl_part}"
    )
    print(DATABASE_URL)

    engine = create_engine(
        DATABASE_URL
    )

    df = pd.read_sql(
        "SELECT * FROM public.fridges WHERE seller = 'Alkosto'",
        engine
    )

    print(df.head())

