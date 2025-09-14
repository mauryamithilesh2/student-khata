# database functions for connect ,create and queries
#handle all database connections and queries
import sqlite3
import pandas as pd


#create db name

DB_PATH = "expenses.db"   # create db file
def get_connection():
    return sqlite3.connect(DB_PATH,check_same_thread=False)


def init_db():  # initialise db
    conn=get_connection()  # call
    cur = conn.cursor()      # or cur=(get_connection()).cursor()

    #user table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
                )
                """)

    # expenses table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                notes TEXT,

                item TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                total REAL NOT NULL,

                FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """)
    conn.commit()
    return conn



def add_expense(conn,user_id,date,item,quantity,price,total,category,notes=""):
    total = quantity * price  # calculate total
    cur=conn.cursor()
    cur.execute(
        "INSERT INTO expenses(user_id,date,item,quantity,price,total,category,notes) VALUES(?,?,?,?,?,?,?,?)",
        (user_id,date,item,quantity,float(price),float(total),category,notes)
    )
    conn.commit()

def load_expenses(conn,user_id):
    return pd.read_sql_query(
        "SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC",
        conn,
        params=(user_id,)
    )
