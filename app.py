import streamlit as st   # main UIlibrary , built widget,page and chart
import pandas as pd  # ye read aur  transform tabular data
from db import init_db,add_expense,load_expenses
from auth import create_user,authenticate_user,init_user_table,get_connection
from utils import category_pie_chart,daily_line_chart
from datetime import date

import os

st.set_page_config(page_title="Student Khata",layout="wide")
SESSION_FILE = "current_user.txt"

conn=init_db()
init_user_table()



if "user_id" not in st.session_state:
    st.session_state["user_id"]=None
if "username_input" not in st.session_state:
    st.session_state["username_input"] = ""

#Restore session from file 
if os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "r") as f:
        try:
            st.session_state["user_id"] = int(f.read())
        except:
            st.session_state["user_id"] = None


menu = st.sidebar.radio("Menu",["Login","Signup","Daily Expense","Logout"])

if menu =="Signup":
    st.subheader("Create Account")
    username=st.text_input("username")
    password=st.text_input("password",type="password")

    if st.button("Signup"):
        if create_user(username,password):
            st.success("Account Created! go to Login Page")
        else:
            st.error("Username already exist.")

elif menu == "Login":
    st.subheader("Login")
    #already login
    if st.session_state["user_id"]:
        st.info(f"Already logged in as {st.session_state['username_input']}")
    
    else:
        username = st.text_input("Username",value=st.session_state["username_input"])
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id=authenticate_user(username,password)
            if user_id:
                st.session_state["user_id"] = user_id
                st.session_state["username_input"] = username
                
                # Persist session across refresh
                with open(SESSION_FILE, "w") as f:
                    f.write(str(user_id))
                st.success(f"Wlcome {username}!")
            else:
                st.error("Invalid Credentials")



elif menu == "Logout":
    if st.session_state["user_id"]:
        st.session_state["user_id"] = None
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        st.success("Logged out successfully!")
    else:
        st.info("You are not logged in.")


elif menu == "Daily Expense":
    if st.session_state["user_id"] is None:
        st.warning("please login first")
    else:
        st.subheader(f"Welcome, {st.session_state.get("username_input","")}! 👋")

        st.subheader("Add Expense")
        with st.form("add_expense",clear_on_submit=True):
            col1,col2,col3,col4=st.columns(4)
            with col1:
                expense_date = st.date_input("Date", value=date.today())
            with col2:
                item = st.text_input("Items (i.e milk ,rice)")
            with col3:
                quantity = st.number_input("Quantity", min_value=1.0, step=1.0)
            with col4:
                price = st.number_input("Price per unit (₹)", min_value=0.0, step=1.0)

            category = st.selectbox("Category", ["Food", "Groceries", "Transport", "Bills", "Entertainment", "Other"])
            notes = st.text_input("Notes (optional)")
            submitted = st.form_submit_button("Add more..")
            if submitted:
                add_expense(conn, st.session_state["user_id"], expense_date.strftime("%Y-%m-%d"),item,quantity,price,category, notes)
                st.success(f"Added {quantity} x {item} @ ₹{price} each")


        st.subheader("Dashboard")
        df = load_expenses(conn, st.session_state["user_id"])
        if not df.empty:
            st.dataframe(df[['date', 'item', 'quantity', 'price', 'total', 'category', 'notes']])
            st.metric("Total Spent", f"₹ {df['total'].sum():.2f}")
            category_pie_chart(df)
            daily_line_chart(df)
            
        else:
            st.info("No expenses yet.")


 # Dashboard Dashboard

# elif menu == "Dashboard":
#     if st.session_state["user_id"] is None:
#         st.warning("Please login first")

#     else:
#         st.subheader("Dashboard")
#         df = load_expenses(conn, st.session_state["user_id"])
#         if not df.empty:
#             st.dataframe(df[['date', 'item', 'quantity', 'price', 'total', 'category', 'notes']])
#             st.metric("Total Spent", f"₹ {df['total'].sum():.2f}")
#             category_pie_chart(df)
#             daily_line_chart(df)
            
#         else:
#             st.info("No expenses yet.")