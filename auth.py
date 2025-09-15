# it handle signup login , and password hashing

import streamlit as st
import sqlite3
import bcrypt
from db import get_connection
import extra_streamlit_components as stx

_cookie_manager_instance = None

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

def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    try:
        cur.execute(
            "INSERT INTO users (username,password_hash) VALUES(?,?)",
            (username, password_hash)
        )
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
        return None

    user_id, stored_hash = row
    if stored_hash and bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return user_id
    return None


def set_login_cookie(user_id):
    # cookie_manager = get_cookie_manager()
    # cookie_manager.set("user_id", str(user_id), key="login_cookie")
    pass

# def get_username_from_id(user_id: int):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
#     row = cur.fetchone()
#     conn.close()
#     return row[0] if row else None

def get_logged_in_user():
    # cookie_manager = get_cookie_manager()
    # user_id = cookie_manager.get("user_id")
    # if user_id:
    #     return int(user_id), get_username_from_id(int(user_id))
    return None, None

def logout_user():
    # cookie_manager = get_cookie_manager()
    # cookie_manager.delete("user_id", key="login_cookie")
    st.session_state.clear()
    st.session_state["refresh_after_logout"] = True
    st.stop()
