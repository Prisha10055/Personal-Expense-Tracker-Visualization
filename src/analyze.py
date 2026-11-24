"""Analytics engine for category, monthly, daily, and payment method insights."""

import sqlite3
import pandas as pd


def fetch_transactions(db_path: str = "db/expenses.db") -> pd.DataFrame:
    """Load transactions joined with category names from SQLite."""
    con = sqlite3.connect(db_path)
    query = """
        SELECT
            t.id,
            t.tx_date,
            t.description,
            t.amount,
            t.payment_method,
            t.account,
            COALESCE(c.name, 'Uncategorized') AS category,
            t.tags
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        ORDER BY t.tx_date
    """
    df = pd.read_sql_query(query, con, parse_dates=["tx_date"])
    con.close()
    df["month"] = df["tx_date"].dt.to_period("M").astype(str)
    df["spend"] = df["amount"].apply(lambda x: -x if x < 0 else 0.0)
    df["income"] = df["amount"].apply(lambda x: x if x > 0 else 0.0)
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute core personal finance KPIs."""
    expenses = df[df["amount"] < 0]
    total_spend = float(expenses["spend"].sum())
    total_income = float(df["income"].sum())
    net_savings = total_income - total_spend
    savings_rate = (net_savings / total_income * 100.0) if total_income > 0 else 0.0

    cat_summary = category_analysis(df)
    top_category = cat_summary.iloc[0]["category"] if not cat_summary.empty else "N/A"
    top_category_spend = float(cat_summary.iloc[0]["total_spend"]) if not cat_summary.empty else 0.0

    num_days = max(int((df["tx_date"].max() - df["tx_date"].min()).days) + 1, 1) if not df.empty else 1
    avg_daily_spend = total_spend / num_days

    monthly = monthly_analysis(df)
    avg_monthly_spend = float(monthly["total_spend"].mean()) if not monthly.empty else 0.0

    return {
        "total_transactions": int(len(df)),
        "expense_transactions": int(len(expenses)),
        "total_income": round(total_income, 2),
        "total_spend": round(total_spend, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate_pct": round(savings_rate, 2),
        "highest_spending_category": top_category,
        "highest_category_spend": round(top_category_spend, 2),
        "avg_daily_spend": round(avg_daily_spend, 2),
        "avg_monthly_spend": round(avg_monthly_spend, 2),
    }


def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spending by category."""
    exp = df[df["amount"] < 0]
    if exp.empty:
        return pd.DataFrame(columns=["category", "total_spend", "tx_count", "avg_tx", "share_pct"])
    grouped = (
        exp.groupby("category", as_index=False)
        .agg(total_spend=("spend", "sum"), tx_count=("id", "count"), avg_tx=("spend", "mean"))
        .sort_values("total_spend", ascending=False)
        .reset_index(drop=True)
    )
    total = grouped["total_spend"].sum()
    grouped["share_pct"] = (grouped["total_spend"] / total * 100.0).round(2)
    grouped["total_spend"] = grouped["total_spend"].round(2)
    grouped["avg_tx"] = grouped["avg_tx"].round(2)
    return grouped


def monthly_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate income, spending, and savings by month."""
    if df.empty:
        return pd.DataFrame(columns=["month", "total_income", "total_spend", "net_savings"])
    grouped = (
        df.groupby("month", as_index=False)
        .agg(total_income=("income", "sum"), total_spend=("spend", "sum"))
        .sort_values("month")
        .reset_index(drop=True)
    )
    grouped["net_savings"] = (grouped["total_income"] - grouped["total_spend"]).round(2)
    grouped["total_income"] = grouped["total_income"].round(2)
    grouped["total_spend"] = grouped["total_spend"].round(2)
    return grouped


def payment_method_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spending by payment method."""
    exp = df[df["amount"] < 0]
    if exp.empty:
        return pd.DataFrame(columns=["payment_method", "total_spend", "tx_count", "share_pct"])
    grouped = (
        exp.groupby("payment_method", as_index=False)
        .agg(total_spend=("spend", "sum"), tx_count=("id", "count"))
        .sort_values("total_spend", ascending=False)
        .reset_index(drop=True)
    )
    total = grouped["total_spend"].sum()
    grouped["share_pct"] = (grouped["total_spend"] / total * 100.0).round(2)
    grouped["total_spend"] = grouped["total_spend"].round(2)
    return grouped


def daily_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spending by calendar day with 7-day rolling average."""
    exp = df[df["amount"] < 0]
    if exp.empty:
        return pd.DataFrame(columns=["tx_date", "daily_spend", "rolling_7d"])
    daily = (
        exp.groupby("tx_date", as_index=False)
        .agg(daily_spend=("spend", "sum"))
        .sort_values("tx_date")
        .reset_index(drop=True)
    )
    daily["rolling_7d"] = daily["daily_spend"].rolling(window=7, min_periods=1).mean().round(2)
    daily["daily_spend"] = daily["daily_spend"].round(2)
    return daily
