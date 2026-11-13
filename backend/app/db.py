import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv("DATABASE_URL")
def get_conn():
    return psycopg.connect(
        DATABASE_URL, 
        autocommit=True, 
        row_factory=psycopg.rows.dict_row
        )



def create_schema(): 
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS applications (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            company VARCHAR NOT NULL,
            position VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT now()



            );
            """)
    except Exception as e:
                    print(f"Error while creating schema: {e}")
                    raise 
