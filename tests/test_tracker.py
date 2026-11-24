"""Unit tests for Personal Expense Tracker."""

import pandas as pd
from src.models import init_db
from src.ingest import clean_and_standardize, upsert_transactions
from src.categorize import classify_description, categorize_transactions
from src.analyze import fetch_transactions, compute_kpis
from src.budget import set_budget, check_budget


def test_clean_and_categorize(tmp_path):
    db_file = str(tmp_path / "test.db")
    init_db(db_file)

    raw = pd.DataFrame(
        [
            {"Date": "2026-10-01", "Description": "  Monthly Salary  ", "Amount": 40000, "Payment_Method": "Net Banking", "Account": "HDFC", "Note": "Income"},
            {"Date": "2026-10-02", "Description": "Swiggy Order", "Amount": -450, "Payment_Method": "UPI", "Account": "HDFC", "Note": "Lunch"},
            {"Date": "bad-date", "Description": "Invalid", "Amount": -100, "Payment_Method": "Cash", "Account": "Cash", "Note": ""},
        ]
    )
    cleaned, stats = clean_and_standardize(raw)
    assert stats["clean_rows"] == 2
    assert stats["dropped_invalid"] == 1

    inserted = upsert_transactions(cleaned, db_file)
    assert inserted == 2
    assert categorize_transactions(db_file) == 2

    df = fetch_transactions(db_file)
    kpis = compute_kpis(df)
    assert kpis["total_income"] == 40000.0
    assert kpis["total_spend"] == 450.0
    assert kpis["highest_spending_category"] == "Food & Dining"

    set_budget("2026-10", "Food & Dining", 400.0, db_file)
    b = check_budget("2026-10", db_file)
    assert b.iloc[0]["status"] == "OVER BUDGET"


def test_classify_rules():
    assert classify_description("D-Mart Supermarket", -500) == "Groceries"
    assert classify_description("Uber Ride", -250) == "Transport"
    assert classify_description("Monthly Stipend", 35000) == "Income"
