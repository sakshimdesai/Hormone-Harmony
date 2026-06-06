import json
from db import get_db

def seed_meals():
    db = get_db()

    with open("data/meals.json", "r", encoding="utf-8") as file:
        meals = json.load(file)

    for meal in meals:
        db.execute("""
            INSERT INTO meals (
                meal_name,
                category,
                description,
                benefit,
                best_time,
                avoid_if
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            meal["meal_name"],
            meal["category"],
            meal["description"],
            meal["benefit"],
            meal["best_time"],
            meal["avoid_if"]
        ))

    db.commit()
    print("Meals seeded successfully!")

seed_meals()