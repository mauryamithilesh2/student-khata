# it handle signup login , and password hashing

# import streamlit as st
import sqlite3
import bcrypt
from db import get_connection
# DB_FILE = "expenses.db"

# # ----------------- Connection -----------------
# def get_connection():
#     return sqlite3.connect(DB_FILE, check_same_thread=False)

# ----------------- Initialize Users Table -----------------
def init_user_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_user(username,password):
    conn=get_connection()
    cur=conn.cursor()
    password_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cur.execute("INSERT INTO users (username,password_hash) VALUES(?,?)",(username,password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None  # username not found

    user_id, stored_hash = row
    if stored_hash is None:
        return None  # no password hash stored (should not happen)
    
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return user_id

    return None

