"""
Database Initialization and Seeding
Seed the database with common allergens, preferences, comorbidities, and ingredients
"""

from src.db import db
from src.db_models import Allergen, Preference, Comorbidity, Ingredient
from datetime import datetime


def seed_allergens():
    """Seed common allergens."""
    allergens_data = [
        # Food Allergens - Biological (Animal)
        {"name": "Milk", "category": "food_biological", "severity": "moderate"},
        {"name": "Eggs", "category": "food_biological", "severity": "moderate"},
        {"name": "Fish", "category": "food_biological", "severity": "severe"},
        {"name": "Shellfish", "category": "food_biological", "severity": "severe"},
        
        # Food Allergens - Biological (Plant)
        {"name": "Peanuts", "category": "food_biological", "severity": "severe"},
        {"name": "Tree Nuts", "category": "food_biological", "severity": "severe"},
        {"name": "Soybeans", "category": "food_biological", "severity": "moderate"},
        {"name": "Wheat", "category": "food_biological", "severity": "moderate"},
        {"name": "Sesame", "category": "food_biological", "severity": "moderate"},
        {"name": "Mustard", "category": "food_biological", "severity": "moderate"},
        {"name": "Celery", "category": "food_biological", "severity": "mild"},
        {"name": "Lupin", "category": "food_biological", "severity": "moderate"},
        
        # Chemical Irritants
        {"name": "MSG (Monosodium Glutamate)", "category": "food_chemical", "severity": "mild"},
        {"name": "Preservatives", "category": "food_chemical", "severity": "mild"},
        {"name": "Artificial Colors", "category": "food_chemical", "severity": "mild"},
        {"name": "Artificial Sweeteners", "category": "food_chemical", "severity": "mild"},
        {"name": "Acids", "category": "food_chemical", "severity": "mild"},
        {"name": "Emulsifiers", "category": "food_chemical", "severity": "mild"},
        {"name": "Flavoring Agents", "category": "food_chemical", "severity": "mild"},
        {"name": "Sulfites", "category": "food_chemical", "severity": "moderate"},
        
        # Beauty - Fragrance
        {"name": "Fragrance", "category": "beauty_fragrance", "severity": "moderate"},
        {"name": "Limonene", "category": "beauty_fragrance", "severity": "mild"},
        {"name": "Linalool", "category": "beauty_fragrance", "severity": "mild"},
        {"name": "Citronellol", "category": "beauty_fragrance", "severity": "mild"},
        {"name": "Geraniol", "category": "beauty_fragrance", "severity": "mild"},
        {"name": "Eugenol", "category": "beauty_fragrance", "severity": "mild"},
        {"name": "Cinnamal", "category": "beauty_fragrance", "severity": "moderate"},
        {"name": "Balsam of Peru", "category": "beauty_fragrance", "severity": "moderate"},
        
        # Beauty - Preservatives
        {"name": "Parabens", "category": "beauty_preservative", "severity": "moderate"},
        {"name": "Formaldehyde", "category": "beauty_preservative", "severity": "severe"},
        {"name": "Isothiazolinones", "category": "beauty_preservative", "severity": "moderate"},
        {"name": "Phenoxyethanol", "category": "beauty_preservative", "severity": "mild"},
        {"name": "Sodium Benzoate", "category": "beauty_preservative", "severity": "mild"},
        {"name": "Potassium Sorbate", "category": "beauty_preservative", "severity": "mild"},
        {"name": "Benzyl Alcohol", "category": "beauty_preservative", "severity": "mild"},
        
        # Beauty - Botanical
        {"name": "Essential Oils", "category": "beauty_botanical", "severity": "moderate"},
        {"name": "Aloe Vera", "category": "beauty_botanical", "severity": "mild"},
        {"name": "Chamomile", "category": "beauty_botanical", "severity": "mild"},
        {"name": "Calendula", "category": "beauty_botanical", "severity": "mild"},
        {"name": "Coconut Oil", "category": "beauty_botanical", "severity": "mild"},
        {"name": "Shea Butter", "category": "beauty_botanical", "severity": "mild"},
        {"name": "Almond Oil", "category": "beauty_botanical", "severity": "moderate"},
        {"name": "Eucalyptus", "category": "beauty_botanical", "severity": "mild"},
    ]
    
    for allergen_data in allergens_data:
        if not Allergen.query.filter_by(name=allergen_data['name']).first():
            allergen = Allergen(**allergen_data)
            db.session.add(allergen)
    
    db.session.commit()
    print(f"✓ Seeded {len(allergens_data)} allergens")


def seed_preferences():
    """Seed diet and health preferences."""
    preferences_data = [
        # Plant-Based Diets
        {"name": "Vegan", "type": "diet", "category": "plant_based"},
        {"name": "Vegetarian", "type": "diet", "category": "plant_based"},
        {"name": "Pescatarian", "type": "diet", "category": "plant_based"},
        {"name": "Flexitarian", "type": "diet", "category": "plant_based"},
        
        # Low-Carb / Animal-Based
        {"name": "Keto", "type": "diet", "category": "low_carb"},
        {"name": "Paleo", "type": "diet", "category": "low_carb"},
        {"name": "Carnivore", "type": "diet", "category": "low_carb"},
        {"name": "Atkins", "type": "diet", "category": "low_carb"},
        
        # Religious / Cultural
        {"name": "Halal", "type": "diet", "category": "religious"},
        {"name": "Kosher", "type": "diet", "category": "religious"},
        {"name": "Hindu Vegetarian", "type": "diet", "category": "religious"},
        {"name": "Buddhist", "type": "diet", "category": "religious"},
        {"name": "Rastafarian", "type": "diet", "category": "religious"},
        
        # Health Preferences
        {"name": "Gluten-Free", "type": "health", "category": "allergen_free"},
        {"name": "Lactose-Free", "type": "health", "category": "allergen_free"},
        {"name": "Low Sodium", "type": "health", "category": "medical"},
        {"name": "Low Fat", "type": "health", "category": "medical"},
        {"name": "Low Carb", "type": "health", "category": "medical"},
        {"name": "Low Sugar", "type": "health", "category": "medical"},
        {"name": "Diabetic Friendly", "type": "health", "category": "medical"},
        {"name": "Heart Healthy", "type": "health", "category": "medical"},
        {"name": "Allergen-Free", "type": "health", "category": "allergen_free"},
    ]
    
    for pref_data in preferences_data:
        if not Preference.query.filter_by(name=pref_data['name']).first():
            pref = Preference(**pref_data)
            db.session.add(pref)
    
    db.session.commit()
    print(f"✓ Seeded {len(preferences_data)} preferences")


def seed_comorbidities():
    """Seed medical comorbidities as preferences with type='comorbidity'."""
    comorbidities_data = [
        # Cardiovascular
        {"name": "Hypertension", "type": "comorbidity", "category": "cardiovascular", "description": "High blood pressure"},
        {"name": "Hyperlipidemia", "type": "comorbidity", "category": "cardiovascular", "description": "High cholesterol"},
        {"name": "Coronary Artery Disease", "type": "comorbidity", "category": "cardiovascular", "description": "CAD"},
        {"name": "Heart Failure", "type": "comorbidity", "category": "cardiovascular", "description": "Congestive heart failure"},
        {"name": "Atrial Fibrillation", "type": "comorbidity", "category": "cardiovascular", "description": "AFib"},
        {"name": "Peripheral Artery Disease", "type": "comorbidity", "category": "cardiovascular", "description": "PAD"},
        
        # Metabolic & Endocrine
        {"name": "Diabetes Type 1", "type": "comorbidity", "category": "metabolic", "description": "Type 1 diabetes mellitus"},
        {"name": "Diabetes Type 2", "type": "comorbidity", "category": "metabolic", "description": "Type 2 diabetes mellitus"},
        {"name": "Prediabetes", "type": "comorbidity", "category": "metabolic", "description": "Impaired glucose tolerance"},
        {"name": "Obesity", "type": "comorbidity", "category": "metabolic", "description": "BMI > 30"},
        {"name": "Hypothyroidism", "type": "comorbidity", "category": "endocrine", "description": "Underactive thyroid"},
        {"name": "Hyperthyroidism", "type": "comorbidity", "category": "endocrine", "description": "Overactive thyroid"},
        {"name": "PCOS", "type": "comorbidity", "category": "endocrine", "description": "Polycystic ovary syndrome"},
        {"name": "Gout", "type": "comorbidity", "category": "metabolic", "description": "Elevated uric acid"},
        
        # Respiratory
        {"name": "Asthma", "type": "comorbidity", "category": "respiratory", "description": "Chronic airway inflammation"},
        {"name": "COPD", "type": "comorbidity", "category": "respiratory", "description": "Chronic obstructive pulmonary disease"},
        {"name": "Chronic Bronchitis", "type": "comorbidity", "category": "respiratory", "description": "Long-term bronchitis"},
        {"name": "Sleep Apnea", "type": "comorbidity", "category": "respiratory", "description": "Obstructive sleep apnea"},
        {"name": "Pulmonary Hypertension", "type": "comorbidity", "category": "respiratory", "description": "High blood pressure in lungs"},
        
        # Gastrointestinal
        {"name": "IBS", "type": "comorbidity", "category": "gastrointestinal", "description": "Irritable bowel syndrome"},
        {"name": "Crohn's Disease", "type": "comorbidity", "category": "gastrointestinal", "description": "Inflammatory bowel disease"},
        {"name": "Ulcerative Colitis", "type": "comorbidity", "category": "gastrointestinal", "description": "IBD affecting colon"},
        {"name": "Celiac Disease", "type": "comorbidity", "category": "gastrointestinal", "description": "Gluten intolerance"},
        {"name": "GERD", "type": "comorbidity", "category": "gastrointestinal", "description": "Gastroesophageal reflux disease"},
    ]
    
    for comorb_data in comorbidities_data:
        if not Preference.query.filter_by(name=comorb_data['name']).first():
            comorb = Preference(**comorb_data)
            db.session.add(comorb)
    
    db.session.commit()
    print(f"✓ Seeded {len(comorbidities_data)} comorbidities")


def seed_common_ingredients():
    """Seed common ingredients for quick lookup."""
    ingredients_data = [
        {"name": "Water", "category": "base", "safety_score": 5.0, "is_natural": True},
        {"name": "Sugar", "category": "sweetener", "safety_score": 3.0, "is_natural": True},
        {"name": "Salt", "category": "seasoning", "safety_score": 3.5, "is_natural": True},
        {"name": "Citric Acid", "category": "preservative", "safety_score": 4.0, "is_natural": True},
        {"name": "Sodium Benzoate", "category": "preservative", "safety_score": 3.0, "is_artificial": True},
        {"name": "Potassium Sorbate", "category": "preservative", "safety_score": 3.5, "is_artificial": True},
        {"name": "High Fructose Corn Syrup", "category": "sweetener", "safety_score": 2.0, "is_artificial": True},
        {"name": "Aspartame", "category": "sweetener", "safety_score": 2.5, "is_artificial": True},
        {"name": "Red 40", "category": "color", "safety_score": 2.0, "is_artificial": True, "is_irritant": True},
        {"name": "Yellow 5", "category": "color", "safety_score": 2.0, "is_artificial": True, "is_irritant": True},
        {"name": "BHT", "category": "preservative", "safety_score": 2.5, "is_artificial": True},
        {"name": "BHA", "category": "preservative", "safety_score": 2.5, "is_artificial": True},
        {"name": "Natural Flavors", "category": "flavor", "safety_score": 3.5, "is_natural": True},
        {"name": "Artificial Flavors", "category": "flavor", "safety_score": 2.5, "is_artificial": True},
        {"name": "Vitamin C", "category": "vitamin", "safety_score": 5.0, "is_natural": True},
        {"name": "Vitamin E", "category": "vitamin", "safety_score": 5.0, "is_natural": True},
    ]
    
    for ing_data in ingredients_data:
        if not Ingredient.query.filter_by(normalized_name=Ingredient.normalize_name(ing_data['name'])).first():
            ing = Ingredient(**ing_data, normalized_name=Ingredient.normalize_name(ing_data['name']))
            db.session.add(ing)
    
    db.session.commit()
    print(f"✓ Seeded {len(ingredients_data)} common ingredients")


def init_database(app):
    """
    Initialize database with app context.
    
    Args:
        app: Flask app instance
    """
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Seed data
        seed_allergens()
        seed_preferences()
        seed_comorbidities()
        seed_common_ingredients()
        
        print("\n✅ Database initialization complete!")


def reset_database(app):
    """
    Drop all tables and reinitialize.
    WARNING: This will delete all data!
    
    Args:
        app: Flask app instance
    """
    with app.app_context():
        print("⚠️  Dropping all tables...")
        db.drop_all()
        print("✓ Tables dropped")
        
        init_database(app)


if __name__ == "__main__":
    # For standalone testing
    from flask import Flask
    from src.db import db
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    init_database(app)
