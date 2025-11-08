"""
Database Models using SQLAlchemy
Unified database schema for users, allergens, preferences, ingredients, and intake tracking
"""

from src.db import db
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import json


# ==================== ASSOCIATION TABLES ====================

user_allergens = db.Table(
    'user_allergens',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('allergen_id', db.Integer, db.ForeignKey('allergens.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

user_preferences = db.Table(
    'user_preferences',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('preference_id', db.Integer, db.ForeignKey('preferences.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

user_comorbidities = db.Table(
    'user_comorbidities',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('comorbidity_id', db.Integer, db.ForeignKey('comorbidities.id'), primary_key=True),
    db.Column('diagnosed_date', db.Date, nullable=True),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

product_ingredients = db.Table(
    'product_ingredients',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.id'), primary_key=True),
    db.Column('position', db.Integer),  # Order in ingredient list
    db.Column('percentage', db.Float, nullable=True)  # Optional percentage
)


# ==================== CORE MODELS ====================

class User(db.Model):
    """User profile with comprehensive health information."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), unique=True, nullable=False, index=True)  # External UUID
    
    # Authentication (optional for now)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=True)
    password_salt = db.Column(db.String(128), nullable=True)
    
    # Personal Information
    full_name = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=True)
    age = db.Column(db.Integer)
    birth_date = db.Column(db.Date)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    allergens = db.relationship(
        'Allergen',
        secondary=user_allergens,
        backref=db.backref('users', lazy='dynamic')
    )
    
    preferences = db.relationship(
        'Preference',
        secondary=user_preferences,
        backref=db.backref('users', lazy='dynamic')
    )
    
    comorbidities = db.relationship(
        'Comorbidity',
        secondary=user_comorbidities,
        backref=db.backref('users', lazy='dynamic')
    )
    
    intake_logs = db.relationship('IntakeLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'age': self.age,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'allergens': [a.to_dict() for a in self.allergens],
            'preferences': [p.to_dict() for p in self.preferences],
            'comorbidities': [c.to_dict() for c in self.comorbidities],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def get_allergen_names(self) -> List[str]:
        """Get list of allergen names."""
        return [a.name for a in self.allergens]
    
    def get_preference_names(self) -> List[str]:
        """Get list of preference names."""
        return [p.name for p in self.preferences]
    
    def get_comorbidity_names(self) -> List[str]:
        """Get list of comorbidity names."""
        return [c.name for c in self.comorbidities]


class Allergen(db.Model):
    """Allergens and irritants database."""
    __tablename__ = 'allergens'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50))  # food_biological, food_chemical, beauty_fragrance, etc.
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))  # mild, moderate, severe
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Allergen {self.name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'severity': self.severity
        }


class Preference(db.Model):
    """Diet and health preferences."""
    __tablename__ = 'preferences'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False)  # diet, health, religious, comorbidity
    category = db.Column(db.String(50))  # plant_based, low_carb, religious, etc.
    description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Preference {self.name} ({self.type})>'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'category': self.category,
            'description': self.description
        }


class Comorbidity(db.Model):
    """Medical comorbidities."""
    __tablename__ = 'comorbidities'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50))  # cardiovascular, metabolic, respiratory, etc.
    icd10_code = db.Column(db.String(20))  # Optional ICD-10 code
    description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Comorbidity {self.name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'icd10_code': self.icd10_code,
            'description': self.description
        }


class Ingredient(db.Model):
    """Ingredients database - reusable across products."""
    __tablename__ = 'ingredients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)
    normalized_name = db.Column(db.String(200), index=True)  # Lowercase, no special chars
    category = db.Column(db.String(50))  # preservative, sweetener, flavor, color, etc.
    safety_score = db.Column(db.Float)  # 1-5 safety rating
    description = db.Column(db.Text)
    
    # Risk flags
    is_allergen = db.Column(db.Boolean, default=False)
    is_irritant = db.Column(db.Boolean, default=False)
    is_artificial = db.Column(db.Boolean, default=False)
    is_natural = db.Column(db.Boolean, default=False)
    
    # Metadata
    times_seen = db.Column(db.Integer, default=1)  # How many products contain this
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ingredient {self.name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'normalized_name': self.normalized_name,
            'category': self.category,
            'safety_score': self.safety_score,
            'description': self.description,
            'is_allergen': self.is_allergen,
            'is_irritant': self.is_irritant,
            'is_artificial': self.is_artificial,
            'is_natural': self.is_natural,
            'times_seen': self.times_seen
        }
    
    @staticmethod
    def normalize_name(name: str) -> str:
        """Normalize ingredient name for matching."""
        import re
        # Lowercase, remove special chars, strip whitespace
        normalized = re.sub(r'[^a-z0-9\s]', '', name.lower())
        normalized = ' '.join(normalized.split())  # Normalize whitespace
        return normalized
    
    @classmethod
    def get_or_create(cls, name: str, category: str = None) -> 'Ingredient':
        """
        Get existing ingredient or create new one.
        
        Args:
            name: Ingredient name
            category: Optional category
            
        Returns:
            Ingredient object
        """
        normalized = cls.normalize_name(name)
        
        # Try to find existing
        ingredient = cls.query.filter_by(normalized_name=normalized).first()
        
        if ingredient:
            # Update times_seen and last_seen
            ingredient.times_seen += 1
            ingredient.last_seen = datetime.utcnow()
            db.session.commit()
            return ingredient
        
        # Create new
        ingredient = cls(
            name=name.strip(),
            normalized_name=normalized,
            category=category,
            times_seen=1,
            first_seen=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        
        db.session.add(ingredient)
        db.session.commit()
        
        return ingredient


class Product(db.Model):
    """Analyzed products."""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    barcode = db.Column(db.String(50), index=True)
    product_type = db.Column(db.String(50))  # food, beverage, beauty, etc.
    brand = db.Column(db.String(100))
    
    # Analysis results (JSON)
    analysis_json = db.Column(db.Text)  # Full analysis result
    overall_safety_score = db.Column(db.Float)
    
    # Metadata
    times_analyzed = db.Column(db.Integer, default=1)
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ingredients = db.relationship(
        'Ingredient',
        secondary=product_ingredients,
        backref=db.backref('products', lazy='dynamic')
    )
    
    intake_logs = db.relationship('IntakeLog', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'barcode': self.barcode,
            'product_type': self.product_type,
            'brand': self.brand,
            'overall_safety_score': self.overall_safety_score,
            'ingredients': [i.to_dict() for i in self.ingredients],
            'times_analyzed': self.times_analyzed
        }


class IntakeLog(db.Model):
    """User intake tracking."""
    __tablename__ = 'intake_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    
    # Product info (if not in products table)
    product_name = db.Column(db.String(200))
    product_type = db.Column(db.String(50))
    
    # Consumption details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    quantity = db.Column(db.Float)
    unit = db.Column(db.String(20))  # ml, g, serving, etc.
    
    # Analysis snapshot
    analysis_json = db.Column(db.Text)  # Full analysis at time of consumption
    safety_score = db.Column(db.Float)
    warnings_count = db.Column(db.Integer, default=0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<IntakeLog {self.product_name} by User {self.user_id}>'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_name': self.product_name,
            'product_type': self.product_type,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'quantity': self.quantity,
            'unit': self.unit,
            'safety_score': self.safety_score,
            'warnings_count': self.warnings_count,
            'analysis': json.loads(self.analysis_json) if self.analysis_json else None
        }
