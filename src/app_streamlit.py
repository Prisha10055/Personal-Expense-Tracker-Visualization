"""Interactive Streamlit Dashboard for Personal Expense Tracker."""

import streamlit as st
import pandas as pd

from models import init_db
from ingest import clean_and_standardize, upsert_transactions
from categorize import categorize_transactions
from analyze import fetch_transactions, compute_kpis, category_analysis, monthly_analysis
from budget import check_budget, seed_default_budgets

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
st.title("Personal Expense Tracker with Data Visualization")

init_db("db/expenses.db")

with st.sidebar:
    st.header("Upload Transactions CSV")
    uploaded = st.file_uploader("Upload bank/expense CSV", type=["csv"])
    if uploaded is not None:
        raw_df = pd.read_csv(uploaded)
        cleaned, stats = clean_and_standardize(raw_df, raw_source=uploaded.name)
        inserted = upsert_transactions(cleaned, "db/expenses.db")
        categorize_transactions("db/expenses.db")
        st.success(f"Cleaned {stats['clean_rows']} rows | Inserted {inserted} new transactions")

df = fetch_transactions("db/expenses.db")
if df.empty:
    st.info("No transactions found. Run `python main.py` first or upload a CSV in the sidebar.")
    st.stop()

months = sorted(df["month"].unique())
selected_month = st.selectbox("Select Month", months[::-1])
accounts = sorted(df["account"].unique())
selected_accounts = st.multiselect("Filter Accounts", accounts, default=accounts)

dff = df[(df["month"] == selected_month) & (df["account"].isin(selected_accounts))]
k = compute_kpis(dff)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Spend", f"₹{k['total_spend']:,.0f}")
c2.metric("Total Income", f"₹{k['total_income']:,.0f}")
c3.metric("Net Savings", f"₹{k['net_savings']:,.0f}")
c4.metric("Savings Rate", f"{k['savings_rate_pct']:.1f}%")

col_left, col_right = st.columns(2)
with col_left:
    st.subheader(f"Category Spend ({selected_month})")
    cat_df = category_analysis(dff)
    if not cat_df.empty:
        st.bar_chart(cat_df.set_index("category")["total_spend"])

with col_right:
    st.subheader("Monthly Spending Trend")
    m_df = monthly_analysis(df)
    if not m_df.empty:
        st.line_chart(m_df.set_index("month")[["total_spend", "total_income"]])

st.subheader(f"Budget vs. Actual ({selected_month})")
seed_default_budgets(selected_month, "db/expenses.db")
st.dataframe(check_budget(selected_month, "db/expenses.db"), use_container_width=True)
