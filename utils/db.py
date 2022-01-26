import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "database": os.getenv("database"),
    "user": os.getenv("user"),
    "password": os.getenv("password"),
    "port": os.getenv("port")
}
con = psycopg2.connect(**db_config)
cur = con.cursor()

def try_to_create_db() -> None:
    try:
        cur.execute("CREATE TABLE auth (user_id INTEGER, token TEXT)")
    except Exception as e:
        print(e)
    con.commit()

def reset_db() -> None:
    cur.execute("DELETE FROM auth")
    con.commit()

def init() -> None:
    try_to_create_db()
    reset_db()

def save_auth_token(user_id: int, token: str) -> None:
    cur.execute("INSERT INTO auth VALUES (%s, %s)", (user_id, token))
    con.commit()

init()