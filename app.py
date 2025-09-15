import streamlit as st   # main UIlibrary , built widget,page and chart
import pandas as pd  # ye read aur  transform tabular data
from db import init_db,add_expense,load_expenses
from auth import create_user,authenticate_user,init_user_table,set_login_cookie,logout_user,get_logged_in_user
from utils import expenses_dashboard
from datetime import date

import os

st.set_page_config(page_title="Student Khata",layout="wide")
# SESSION_FILE = "current_user.txt"

conn=init_db()
init_user_table()


# user_id = get_logged_in_user()

def restore_session():
    """Restore user login from cookie into session_state."""
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = get_logged_in_user()
    if "username_input" not in st.session_state:
        st.session_state["username_input"] = ""

restore_session()  # call at the very top



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
                
                
                set_login_cookie(user_id)  # <-- Persist login
                st.success(f"🎉 Welcome {username}!")
                st.experimental_rerun()
            else:
                st.error("Invalid Credentials")



elif menu == "Logout":
    if st.session_state["user_id"]:
        logout_user()
        st.success("✅ Logged out successfully!")
    else:
        st.info("You are not logged in.")


elif menu == "Daily Expense":
    if st.session_state["user_id"] is None:
        st.warning("please login first")
    else:
        st.subheader(f"Welcome , {st.session_state.get("username_input","")}! This Is your Khata_Book")

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

            # category = st.selectbox("optional", ["Category is not define here !"])
            notes = st.text_input("Notes (optional)")
            submitted = st.form_submit_button("Add more..")
            if submitted:
                total=quantity*price
                add_expense(conn, st.session_state["user_id"], expense_date.strftime("%Y-%m-%d"),item,quantity,price,total, notes=notes)
                st.success(f"Added  {quantity} x {item}   =  ₹ {price}  each")


        st.subheader("Dashboard")
        df = load_expenses(conn, st.session_state["user_id"])
        if not df.empty:
            # st.dataframe(df[['date', 'item', 'quantity', 'price', 'total', 'category', 'notes']])
            # categories = ["All"] + sorted(df["category"].unique().tolist())
            # selected_category = st.selectbox("Filter by category", categories)
            # filtered_df = df if selected_category == "All" else df[df["category"] == selected_category]
            
            edited_df = st.data_editor(
                df[['id', 'date', 'item', 'quantity', 'price', 'total', 'notes']],
                num_rows="dynamic",  # allows adding/removing rows
                key="editor"
                )

            # Detect changes (edited rows)
            if not edited_df.equals(df):
                for i in range(len(edited_df)):
                    row = edited_df.iloc[i]
                    cur = conn.cursor()
                    cur.execute(
                        "UPDATE expenses SET date=?, item=?, quantity=?, price=?, total=?, notes=? WHERE id=?",
                        (row["date"], row["item"], row["quantity"], row["price"], row["total"], row["notes"], row["id"])
                    )
                conn.commit()
                st.success("Changes saved to database!")


            # st.metric("Total Spent", f"₹ {df['total'].sum():.2f}")

            expenses_dashboard(df)

            
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