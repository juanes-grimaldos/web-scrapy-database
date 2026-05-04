import psycopg2
import os


password = os.getenv("POSTGRES_PASSWORD")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB")
server = os.getenv("POSTGRES_SERVER", "localhost")
user = os.getenv("POSTGRES_USER", "postgres")

if server == 'localhost':
    conn = psycopg2.connect(
        host=server,
        database=db,
        user=user,
        password=password,
        port=port
    )
else:
    conn = psycopg2.connect(
        host=server,
        database=db,
        user=user,
        password=password,
        port=port,
        sslmode="require"
    )

cur = conn.cursor()

create_view_sql = """
CREATE OR REPLACE VIEW fridges_clean AS
SELECT 
    f.link,
    f.product,
    f.price,
    f.seller,
    s.storage,
    s.size,
    s.energy,
    s.color,
    s.date,

    CASE
        WHEN LOWER(f.product) LIKE '%samsung%' THEN 'Samsung'
        WHEN LOWER(f.product) LIKE '%lg%' THEN 'LG'
        WHEN LOWER(f.product) LIKE '%mabe%' THEN 'Mabe'
        WHEN LOWER(f.product) LIKE '%haceb%' THEN 'Haceb'
        WHEN LOWER(f.product) LIKE '%electrolux%' THEN 'Electrolux'
        WHEN LOWER(f.product) LIKE '%challenger%' THEN 'Challenger'
        WHEN LOWER(f.product) LIKE '%whirlpool%' THEN 'Whirlpool'
        WHEN LOWER(f.product) LIKE '%indurama%' THEN 'Indurama'
        WHEN LOWER(f.product) LIKE '%coldex%' THEN 'Coldex'
        ELSE 'Otra'
    END AS brand,

    CAST(NULLIF(regexp_replace(s.storage, '\\D', '', 'g'), '') AS INT) AS storage_lt,

    CASE
        WHEN f.price < 1500000 THEN 'Económico'
        WHEN f.price < 3000000 THEN 'Mid-range'
        ELSE 'Premium'
    END AS segment,

    ROUND(
        f.price / NULLIF(
            CAST(NULLIF(regexp_replace(s.storage, '\\D', '', 'g'), '') AS INT),
            0
        )
    ) AS price_per_liter

FROM fridges f
LEFT JOIN specs s ON f.link = s.fridge_link;
"""

cur.execute(create_view_sql)
conn.commit()

cur.close()
conn.close()

print("✅ View fridges_clean creada/actualizada")