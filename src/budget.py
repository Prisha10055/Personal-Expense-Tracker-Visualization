"""Monthly category budgeting and overspending detection."""

import sqlite3
import pandas as pd


DEFAULT_BUDGETS = {
    "Food & Dining": 7000.0,
    "Groceries": 7500.0,
    "Transport": 3500.0,
    "Bills & Utilities": 3500.0,
    "Shopping": 4500.0,
    "Entertainment": 1500.0,
    "Health & Fitness": 2000.0,
}


def set_budget(month: str, category: str, limit_amount: float, db_path: str = "db/expenses.db") -> None:
    """Insert or update a monthly budget limit for a category."""
    con = sqlite3.connect(db_path)
    con.execute(
        """
        INSERT INTO budgets(month, category_name, limit_amount)
        VALUES (?, ?, ?)
        ON CONFLICT(month, category_name) DO UPDATE SET limit_amount = excluded.limit_amount
        """,
        (month, category, float(limit_amount)),
    )
    con.commit()
    con.close()


def seed_default_budgets(month: str, db_path: str = "db/expenses.db") -> None:
    """Populate default monthly category budgets if none exist for that month."""
    for cat, lim in DEFAULT_BUDGETS.items():
        set_budget(month, cat, lim, db_path=db_path)


def check_budget(month: str, db_path: str = "db/expenses.db") -> pd.DataFrame:
    """Compare actual monthly category spend against budget limits."""
    con = sqlite3.connect(db_path)
    spend = pd.read_sql_query(
        """
        SELECT COALESCE(c.name, 'Uncategorized') AS category, -SUM(t.amount) AS actual_spend
        FROM transactions t
        LEFT JOIN categories c ON c.id = t.category_id
        WHERE t.amount < 0 AND strftime('%Y-%m', t.tx_date) = ?
        GROUP BY category
        """,
        con,
        params=[month],
    )
    budgets = pd.read_sql_query(
        "SELECT category_name AS category, limit_amount FROM budgets WHERE month = ?",
        con,
        params=[month],
    )
    con.close()

    if budgets.empty:
        return pd.DataFrame(columns=["category", "limit_amount", "actual_spend", "variance", "status"])

    merged = budgets.merge(spend, on="category", how="left").fillna({"actual_spend": 0.0})
    merged["actual_spend"] = merged["actual_spend"].round(2)
    merged["variance"] = (merged["limit_amount"] - merged["actual_spend"]).round(2)
    merged["status"] = merged["variance"].apply(lambda v: "OVER BUDGET" if v < 0 else "Within Budget")
    return merged.sort_values("variance").reset_index(drop=True)
