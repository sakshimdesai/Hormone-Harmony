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


def create_myths_table():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS myths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            myth TEXT,
            fact TEXT,
            category TEXT,
            severity TEXT
        )
    """)
    db.commit()


def create_awareness_table():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS awareness (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            category TEXT,
            importance TEXT
        )
    """)
    db.commit()


def create_meals_table():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT,
            category TEXT,
            description TEXT,
            benefit TEXT,
            best_time TEXT,
            avoid_if TEXT
        )
    """)
def create_selfcare_table():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS selfcare (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            why_it_helps TEXT,
            category TEXT,
            difficulty TEXT
        )
    """)

    
    db.commit()