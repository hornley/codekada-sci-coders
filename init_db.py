from db import db
from models import Allergen, Preferences

def seed_data():
    # Only seed if tables are empty
    if Allergen.query.first() or Preferences.query.first():
        print("Tables already have data. Skipping seeding.")
        return

    # Expanded allergens list
    allergens = [
        "Peanuts", "Tree Nuts", "Dairy", "Eggs", "Fish", "Shellfish",
        "Soy", "Wheat/Gluten", "Sesame", "Mustard", "Lupin", "Celery",
        "Sulfites", "Corn", "Rice", "Oats", "Fruits", "Vegetables",
        "Chocolate/Cocoa", "Yeast", "Spices"
    ]

    # Sample preferences
    preferences = [
        {"name": "Vegetarian", "type": "diet"},
        {"name": "Vegan", "type": "diet"},
        {"name": "Keto", "type": "diet"},
        {"name": "Low Carb", "type": "diet"},
        {"name": "Diabetic Friendly", "type": "health"},
        {"name": "Low Sodium", "type": "health"},
        {"name": "Heart Healthy", "type": "health"}
    ]

    # Insert allergens
    for name in allergens:
        db.session.add(Allergen(name=name))

    # Insert preferences
    for pref in preferences:
        db.session.add(Preferences(name=pref["name"], type=pref["type"]))

    db.session.commit()
    print("Seed data inserted.")

if __name__ == "__main__":
    seed_data()
