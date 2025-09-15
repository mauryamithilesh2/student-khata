import streamlit as st
import pandas as pd
import plotly.express as px


def expenses_dashboard(df):
    """Show expenses dashboard without categories"""
    if df.empty:
        st.info("No expenses yet.")
        return

    # --- KPIs ---
    total_spent = df["total"].sum()
    avg_spent = df["total"].mean()
    max_spent = df["total"].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₹ {total_spent:.2f}")
    col2.metric("Average Spend", f"₹ {avg_spent:.2f}")
    col3.metric("Max Expense", f"₹ {max_spent:.2f}")

    # --- Line Chart: Spending over time ---
    df["date"] = pd.to_datetime(df["date"])
    daily = df.groupby(df["date"].dt.date)["total"].sum().reset_index()
    daily = daily.rename(columns={"date": "Date", "total": "Total Spent"})

    fig_line = px.line(
        daily, x="Date", y="Total Spent",
        markers=True, title="Daily Spending Trend"
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # --- Bar Chart: Top Items ---
    items = (
        df.groupby("item")["total"]
        .sum()
        .reset_index()
        .sort_values(by="total", ascending=False)
        .head(10)
    )
    fig_bar = px.bar(
        items, x="item", y="total",
        title="Top Items by Spending", text="total"
    )
    fig_bar.update_traces(
        texttemplate="₹%{text:.2f}", textposition="outside"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
