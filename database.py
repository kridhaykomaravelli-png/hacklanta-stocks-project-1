import sqlite3
from datetime import datetime

DB_NAME = "stocks.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_type TEXT,
            ticker TEXT,
            score INTEGER,
            label TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_search(asset_type, ticker, score, label):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO searches (asset_type, ticker, score, label, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (asset_type, ticker, score, label, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_search_history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, asset_type, ticker, score, label, created_at
        FROM searches
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


def delete_all_history():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM searches")
    conn.commit()
    conn.close()


def delete_history_item(item_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM searches WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
