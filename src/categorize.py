"""Rule-based auto-categorization for expense transactions."""

import re
import sqlite3
import pandas as pd

RULES = {
    "Groceries": [r"d-mart|dmart|reliance fresh|bigbasket|big bazaar|kirana|supermart|grocery"],
    "Food & Dining": [r"swiggy|zomato|restaurant|cafe|coffee|canteen|lunch|dinner|pizza|burger"],
    "Transport": [r"uber|ola|metro|fuel|petrol|diesel|bus|auto|cab|train"],
    "Bills & Utilities": [r"electric|msedcl|water|wifi|jiofiber|broadband|mobile recharge|airtel|dth|gas"],
    "Shopping": [r"amazon|flipkart|myntra|ajio|mall|apparel|shoes"],
    "Entertainment": [r"netflix|amazon prime|spotify|cinema|bookmyshow|movie|game"],
    "Health & Fitness": [r"pharmacy|apollo|doctor|hospital|cult\.fit|gym|medical"],
    "Income": [r"salary|stipend|payout|refund|reimbursement|interest credit"],
}


def classify_description(description: str, amount: float) -> str:
    """Assign a category using amount sign and regex keyword rules."""
    if amount > 0:
        return "Income"
    text = str(description).lower()
    for category, patterns in RULES.items():
        if category == "Income":
            continue
        if any(re.search(pat, text) for pat in patterns):
            return category
    return "Uncategorized"


def categorize_transactions(db_path: str = "db/expenses.db") -> int:
    """Categorize all uncategorized transactions in SQLite and return count updated."""
    con = sqlite3.connect(db_path)
    existing = pd.read_sql_query("SELECT id, name FROM categories", con)
    name_to_id = dict(zip(existing["name"], existing["id"]))

    for name in set(RULES.keys()) | {"Uncategorized"}:
        if name not in name_to_id:
            con.execute("INSERT INTO categories(name) VALUES (?)", (name,))
    con.commit()

    existing = pd.read_sql_query("SELECT id, name FROM categories", con)
    name_to_id = dict(zip(existing["name"], existing["id"]))

    uncat = pd.read_sql_query(
        "SELECT id, description, amount FROM transactions WHERE category_id IS NULL",
        con,
    )
    for row in uncat.itertuples(index=False):
        cat_name = classify_description(row.description, row.amount)
        con.execute(
            "UPDATE transactions SET category_id = ? WHERE id = ?",
            (name_to_id[cat_name], row.id),
        )
    con.commit()
    con.close()
    return len(uncat)
