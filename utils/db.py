import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "database": getenv("database"),
    "user": getenv("user"),
    "password": getenv("password"),
    "port": getenv("port")
}
con = psycopg2.connect(**db_config)
cur = con.cursor()

def try_to_create_db() -> None:
    try:
        cur.execute("CREATE TABLE auth (user_id INTEGER, token TEXT)")
    except:
        ...
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