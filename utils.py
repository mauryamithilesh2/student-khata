#it contains helper functions (chart formatting and validations )
import plotly.express as px
import streamlit as st
import pandas as pd

def category_pie_chart(df):
    if not df.empty:
        c_data=df.groupby("category")["total"].sum().reset_index()
        fig=px.pie(c_data,values="total",names="category",title="category-wise spending")
        st.plotly_chart(fig,use_container_width=True)

def daily_line_chart(df):
    if not df.empty:
        df["date"]=pd.to_datetime(df["date"])

        daily=df.groupby(df["date"].dt.day)["total"].sum().reset_index()
        daily = daily.rename(columns={"date": "Day", "total": "Total Spent"})
        
        
        fig=px.line(daily,x="Day",y="Total Spent",markers=True,title="daiily Spending trend")
        st.plotly_chart(fig,use_container_width=True)


