import sqlite3
from datetime import datetime, timezone

def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path):
    conn = get_connection(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            sender TEXT NOT NULL,
            subject TEXT NOT NULL,
            body TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            verdict TEXT NOT NULL,
            indicators TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_analysis(db_path, result):
    conn = get_connection(db_path)
    cur = conn.execute("""
        INSERT INTO analyses
        (created_at, sender, subject, body, risk_score, risk_level, verdict, indicators)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        result["sender"], result["subject"], result["body"],
        result["risk_score"], result["risk_level"], result["verdict"],
        " | ".join(result["indicators"])
    ))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id

def list_analyses(db_path, limit=100):
    conn = get_connection(db_path)
    rows = conn.execute(
        "SELECT * FROM analyses ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows
