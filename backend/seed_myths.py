import json
from db import get_db

def seed_myths():
    db = get_db()

    with open("data/myths.json", "r", encoding="utf-8") as file:
        myths = json.load(file)

    for myth in myths:
        db.execute("""
            INSERT INTO myths (myth, fact, category, severity)
            VALUES (?, ?, ?, ?)
        """, (
            myth["myth"],
            myth["fact"],
            myth["category"],
            myth["severity"]
        ))

    db.commit()

    print("Myths seeded successfully!")

seed_myths()