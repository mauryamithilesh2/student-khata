import streamlit as st
import pandas as pd
import plotly.express as px


def expenses_dashboard(df):
    """Show expenses dashboard without categories"""
    if df.empty:
        st.info("No expenses yet.")
        return

    # Work on a copy; coerce types safely
    df_plot = df.copy()
    df_plot["total"] = pd.to_numeric(df_plot["total"], errors="coerce").fillna(0)
    df_plot["date"] = pd.to_datetime(df_plot["date"], errors="coerce")
    df_plot = df_plot.dropna(subset=["date"])  # drop invalid dates

    if df_plot.empty:
        st.info("No plottable data yet (invalid dates).")
        return

    # --- KPIs ---
    total_spent = df_plot["total"].sum()
    avg_spent = df_plot["total"].mean()
    max_spent = df_plot["total"].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₹ {total_spent:.2f}")
    col2.metric("Average Spend", f"₹ {avg_spent:.2f}")
    col3.metric("Max Expense", f"₹ {max_spent:.2f}")

    # --- Line Chart: Spending over time ---
    daily = df_plot.groupby(df_plot["date"].dt.date)["total"].sum().reset_index()
    daily = daily.rename(columns={"date": "Date", "total": "Total Spent"})

    if not daily.empty:
        fig_line = px.line(
            daily, x="Date", y="Total Spent",
            markers=True, title="Daily Spending Trend"
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No daily data to plot yet.")

    # --- Bar Chart: Top Items ---
    items = (
        df_plot.groupby("item")["total"]
        .sum()
        .reset_index()
        .sort_values(by="total", ascending=False)
        .head(10)
    )
    if not items.empty:
        fig_bar = px.bar(
            items, x="item", y="total",
            title="Top Items by Spending", text="total"
        )
        fig_bar.update_traces(
            texttemplate="₹%{text:.2f}", textposition="outside"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No item data to plot yet.")
