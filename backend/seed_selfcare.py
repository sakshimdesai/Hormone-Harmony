import json
from db import get_db

def seed_selfcare():
    db = get_db()

    with open("data/selfcare.json", "r", encoding="utf-8") as file:
        entries = json.load(file)

    for item in entries:
        db.execute("""
            INSERT INTO selfcare (
                title,
                description,
                why_it_helps,
                category,
                difficulty
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            item["title"],
            item["description"],
            item["why_it_helps"],
            item["category"],
            item["difficulty"]
        ))

    db.commit()
    print("Self-care data seeded successfully!")

seed_selfcare()