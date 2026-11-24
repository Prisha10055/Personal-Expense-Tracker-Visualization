"""Database schema and SQLite initialization for Personal Expense Tracker."""

import sqlite3
from pathlib import Path


def init_db(db_path: str = "db/expenses.db") -> None:
    """Initialize SQLite database with normalized categories, transactions, and budgets tables."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            parent TEXT
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            payment_method TEXT DEFAULT 'UPI',
            account TEXT DEFAULT 'Primary',
            category_id INTEGER,
            raw_source TEXT,
            tags TEXT,
            UNIQUE(tx_date, description, amount, payment_method, account),
            FOREIGN KEY(category_id) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,
            category_name TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            UNIQUE(month, category_name)
        );
        """
    )
    con.commit()
    con.close()
