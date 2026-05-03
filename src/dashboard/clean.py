import psycopg2
import os

conn = psycopg2.connect(
    host=os.environ.get("POSTGRES_SERVER", "localhost"),
    database=os.environ.get("POSTGRES_DB", "tu_db"),
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("POSTGRES_PASSWORD", "tu_password")
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