from db import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    password_salt = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    bdate = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=db.func.now())

    allergens = db.relationship(
        'Allergen',
        secondary='user_allergens',
        backref=db.backref('users', lazy=True)
    )
    
    preferences = db.relationship(
        'Preferences',
        secondary='user_preferences',
        backref=db.backref('users', lazy=True)
    )

class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Preferences(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Enum('diet', 'health', name='preferences_enum'), nullable=False)

# Association tables (composite entities)
user_allergens = db.Table(
    'user_allergens',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('allergen_id', db.Integer, db.ForeignKey('allergen.id'), primary_key=True)
)

user_preferences = db.Table(
    'user_preferences',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('preference_id', db.Integer, db.ForeignKey('preferences.id'), primary_key=True)
)
