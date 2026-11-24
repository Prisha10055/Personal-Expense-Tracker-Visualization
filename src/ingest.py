"""CSV ingestion, data cleaning, and SQLite upsert utilities."""

import sqlite3
import pandas as pd


STANDARD_COLS = ["tx_date", "description", "amount", "payment_method", "account", "raw_source", "tags"]


def clean_and_standardize(
    df: pd.DataFrame,
    raw_source: str = "manual_upload",
    date_col: str = "Date",
    desc_col: str = "Description",
    amt_col: str = "Amount",
    pm_col: str = "Payment_Method",
    acct_col: str = "Account",
    note_col: str = "Note",
) -> tuple[pd.DataFrame, dict]:
    """
    Clean raw expense DataFrame:
    - Parse and validate dates
    - Strip whitespace from descriptions
    - Coerce amounts to numeric
    - Drop invalid/null rows and exact duplicates
    Returns (cleaned_df, cleaning_stats).
    """
    initial_rows = len(df)
    work = df.copy()

    work["tx_date"] = pd.to_datetime(work[date_col], errors="coerce")
    work["description"] = work[desc_col].astype(str).str.strip()
    work["amount"] = pd.to_numeric(work[amt_col], errors="coerce")
    work["payment_method"] = work[pm_col].fillna("UPI").astype(str).str.strip() if pm_col in work.columns else "UPI"
    work["account"] = work[acct_col].fillna("Primary").astype(str).str.strip() if acct_col in work.columns else "Primary"
    work["tags"] = work[note_col].fillna("").astype(str).str.strip() if note_col in work.columns else ""
    work["raw_source"] = raw_source

    work = work.dropna(subset=["tx_date", "amount"])
    work = work[work["description"] != ""]
    work["tx_date"] = work["tx_date"].dt.strftime("%Y-%m-%d")

    before_dedup = len(work)
    work = work.drop_duplicates(subset=["tx_date", "description", "amount", "payment_method", "account"])

    stats = {
        "initial_rows": initial_rows,
        "dropped_invalid": initial_rows - before_dedup,
        "dropped_duplicates": before_dedup - len(work),
        "clean_rows": len(work),
    }
    return work[STANDARD_COLS], stats


def read_expense_csv(path: str, **kwargs) -> tuple[pd.DataFrame, dict]:
    """Read an expense CSV file and return cleaned DataFrame + cleaning stats."""
    raw_df = pd.read_csv(path)
    return clean_and_standardize(raw_df, raw_source=str(path), **kwargs)


def upsert_transactions(df: pd.DataFrame, db_path: str = "db/expenses.db") -> int:
    """Insert cleaned transactions into SQLite, ignoring duplicates."""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    before_count = cur.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    rows = list(df[STANDARD_COLS].itertuples(index=False, name=None))
    cur.executemany(
        """
        INSERT OR IGNORE INTO transactions
            (tx_date, description, amount, payment_method, account, raw_source, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )
    con.commit()
    after_count = cur.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    con.close()
    return after_count - before_count
