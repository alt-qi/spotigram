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

def create_table() -> None:
    try:
        cur.execute("CREATE TABLE auth (user_id INTEGER, code TEXT)")
    except:
        ...
    con.commit()

def reset_table() -> None:
    cur.execute("DELETE FROM auth")
    con.commit()

def init() -> None:
    create_table()
    reset_table()

def user_exists(user_id: int) -> bool:
    cur.execute("SELECT EXISTS (SELECT * FROM auth WHERE user_id = %s)", (user_id,))
    return cur.fetchall()[0][0]

def save_auth_code(user_id: int, code: str) -> None:
    if not user_exists(user_id):
        cur.execute("INSERT INTO auth VALUES (%s, %s)", (user_id, code))
    else:
        cur.execute("UPDATE auth SET code = %s WHERE user_id = %s", (code, user_id))
    con.commit()