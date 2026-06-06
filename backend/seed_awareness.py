import json
from db import get_db

def seed_awareness():
    db = get_db()

    with open("data/awareness.json", "r", encoding="utf-8") as file:
        awareness_items = json.load(file)

    for item in awareness_items:
        db.execute("""
            INSERT INTO awareness (title, content, category, importance)
            VALUES (?, ?, ?, ?)
        """, (
            item["title"],
            item["content"],
            item["category"],
            item["importance"]
        ))

    db.commit()

    print("Awareness data seeded successfully!")

seed_awareness()