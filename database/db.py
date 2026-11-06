import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    try:
        if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
            return

        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        month = date.today().strftime("%Y-%m")
        expenses = [
            (user_id, 45.00, "Food", f"{month}-01", "Lunch at cafe"),
            (user_id, 120.00, "Transport", f"{month}-03", "Cab to office"),
            (user_id, 890.00, "Bills", f"{month}-05", "Electricity bill"),
            (user_id, 320.00, "Health", f"{month}-07", "Pharmacy"),
            (user_id, 250.00, "Entertainment", f"{month}-10", "Movie tickets"),
            (user_id, 650.00, "Shopping", f"{month}-12", "Clothes"),
            (user_id, 100.00, "Other", f"{month}-15", "Misc expense"),
            (user_id, 500.00, "Food", f"{month}-18", "Groceries"),
        ]
        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            expenses,
        )
        conn.commit()
    finally:
        conn.close()
