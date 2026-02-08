from db import get_db

def create_users_table():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT
        )
    """)
    db.commit()
    
def create_daily_logs_table():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            period INTEGER,
            mood INTEGER,
            energy INTEGER,
            cravings INTEGER,
            symptoms TEXT
        )
    """)
    db.commit()

