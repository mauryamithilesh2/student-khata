# auth.py
import streamlit as st
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
        cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    user_id, stored_hash = row
    if bcrypt.checkpw(password.encode(), stored_hash.encode()):
        return user_id
    return None

def get_cookie_manager():
    global _cookie_manager_instance
    if _cookie_manager_instance is None:
        _cookie_manager_instance = stx.CookieManager(key="unique_cookie_manager")
    return _cookie_manager_instance

def set_login_cookie(user_id):
    cm = get_cookie_manager()
    cm.set("user_id", str(user_id), key="login_cookie")

def get_logged_in_user():
    cm = get_cookie_manager()
    val = cm.get("user_id")
    if val:
        return int(val)
    return None

def logout_user():
    cm = get_cookie_manager()
    cm.delete("user_id", key="login_cookie")
    st.session_state.clear()
    st.session_state["refresh_after_logout"] = True
    st.stop()
