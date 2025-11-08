"""
User Profile Manager using Database
Replaces boolean-based profile with database relationships
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date
import uuid

from src.db import db
from src.db_models import User, Allergen, Preference, Comorbidity


class UserProfileManager:
    """
    Manage user profiles with database-backed allergens, preferences, and comorbidities.
    Replaces the old boolean-based UserProfile class.
    """
    
    @staticmethod
    def create_user(
        username: str,
        full_name: str,
        age: int = None,
        birth_date: date = None,
        email: str = None,
        password_hash: str = None,
        password_salt: str = None
    ) -> User:
        """
        Create a new user.
        
        Args:
            username: Unique username
            full_name: User's full name
            age: User's age
            birth_date: User's birth date
            email: User's email
            password_hash: Hashed password
            password_salt: Password salt
            
        Returns:
            User object
        """
        # Generate unique user_id
        user_id = str(uuid.uuid4())
        
        # Split name
        name_parts = full_name.split(maxsplit=1)
        first_name = name_parts[0] if name_parts else full_name
        last_name = name_parts[1] if len(name_parts) > 1 else None
        
        user = User(
            user_id=user_id,
            username=username,
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            age=age,
            birth_date=birth_date,
            email=email,
            password_hash=password_hash,
            password_salt=password_salt
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_user(user_id: str = None, username: str = None, email: str = None) -> Optional[User]:
        """
        Get user by ID, username, or email.
        
        Args:
            user_id: User ID (UUID)
            username: Username
            email: Email address
            
        Returns:
            User object or None
        """
        if user_id:
            return User.query.filter_by(user_id=user_id).first()
        elif username:
            return User.query.filter_by(username=username).first()
        elif email:
            return User.query.filter_by(email=email).first()
        return None
    
    @staticmethod
    def update_user(user: User, **kwargs) -> User:
        """
        Update user fields.
        
        Args:
            user: User object
            **kwargs: Fields to update
            
        Returns:
            Updated user object
        """
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return user
    
    @staticmethod
    def delete_user(user: User) -> bool:
        """
        Delete user.
        
        Args:
            user: User object
            
        Returns:
            True if deleted
        """
        db.session.delete(user)
        db.session.commit()
        return True
    
    # ==================== ALLERGENS ====================
    
    @staticmethod
    def add_allergen(user: User, allergen_name: str) -> bool:
        """
        Add allergen to user profile.
        
        Args:
            user: User object
            allergen_name: Allergen name
            
        Returns:
            True if added, False if already exists or allergen not found
        """
        allergen = Allergen.query.filter_by(name=allergen_name).first()
        if not allergen:
            return False
        
        if allergen not in user.allergens:
            user.allergens.append(allergen)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def remove_allergen(user: User, allergen_name: str) -> bool:
        """
        Remove allergen from user profile.
        
        Args:
            user: User object
            allergen_name: Allergen name
            
        Returns:
            True if removed
        """
        allergen = Allergen.query.filter_by(name=allergen_name).first()
        if allergen and allergen in user.allergens:
            user.allergens.remove(allergen)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def set_allergens(user: User, allergen_names: List[str]) -> int:
        """
        Set user's allergens (replaces existing).
        
        Args:
            user: User object
            allergen_names: List of allergen names
            
        Returns:
            Number of allergens set
        """
        allergens = Allergen.query.filter(Allergen.name.in_(allergen_names)).all()
        user.allergens = allergens
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return len(allergens)
    
    @staticmethod
    def get_allergens(user: User) -> List[Dict[str, Any]]:
        """Get user's allergens."""
        return [a.to_dict() for a in user.allergens]
    
    # ==================== PREFERENCES ====================
    
    @staticmethod
    def add_preference(user: User, preference_name: str) -> bool:
        """
        Add preference to user profile.
        
        Args:
            user: User object
            preference_name: Preference name
            
        Returns:
            True if added
        """
        pref = Preference.query.filter_by(name=preference_name).first()
        if not pref:
            return False
        
        if pref not in user.preferences:
            user.preferences.append(pref)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def remove_preference(user: User, preference_name: str) -> bool:
        """Remove preference from user profile."""
        pref = Preference.query.filter_by(name=preference_name).first()
        if pref and pref in user.preferences:
            user.preferences.remove(pref)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def set_preferences(user: User, preference_names: List[str]) -> int:
        """
        Set user's preferences (replaces existing).
        
        Args:
            user: User object
            preference_names: List of preference names
            
        Returns:
            Number of preferences set
        """
        prefs = Preference.query.filter(Preference.name.in_(preference_names)).all()
        user.preferences = prefs
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return len(prefs)
    
    @staticmethod
    def get_preferences(user: User) -> List[Dict[str, Any]]:
        """Get user's preferences."""
        return [p.to_dict() for p in user.preferences]
    
    # ==================== COMORBIDITIES ====================
    
    @staticmethod
    def add_comorbidity(user: User, comorbidity_name: str) -> bool:
        """
        Add comorbidity to user profile.
        
        Args:
            user: User object
            comorbidity_name: Comorbidity name
            
        Returns:
            True if added
        """
        comorb = Comorbidity.query.filter_by(name=comorbidity_name).first()
        if not comorb:
            return False
        
        if comorb not in user.comorbidities:
            user.comorbidities.append(comorb)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def remove_comorbidity(user: User, comorbidity_name: str) -> bool:
        """Remove comorbidity from user profile."""
        comorb = Comorbidity.query.filter_by(name=comorbidity_name).first()
        if comorb and comorb in user.comorbidities:
            user.comorbidities.remove(comorb)
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    @staticmethod
    def set_comorbidities(user: User, comorbidity_names: List[str]) -> int:
        """
        Set user's comorbidities (replaces existing).
        
        Args:
            user: User object
            comorbidity_names: List of comorbidity names
            
        Returns:
            Number of comorbidities set
        """
        comorbs = Comorbidity.query.filter(Comorbidity.name.in_(comorbidity_names)).all()
        user.comorbidities = comorbs
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return len(comorbs)
    
    @staticmethod
    def get_comorbidities(user: User) -> List[Dict[str, Any]]:
        """Get user's comorbidities."""
        return [c.to_dict() for c in user.comorbidities]
    
    # ==================== BULK OPERATIONS ====================
    
    @staticmethod
    def create_user_from_dict(data: Dict[str, Any]) -> User:
        """
        Create user from dictionary (for API requests).
        
        Args:
            data: User data dict with personal_info, allergens, preferences, comorbidities
            
        Returns:
            Created user object
        """
        # Extract personal info
        personal_info = data.get('personal_info', {})
        
        # Get values from either personal_info or top level (for flexibility)
        full_name = personal_info.get('full_name') or data.get('full_name', '')
        age = personal_info.get('age') or data.get('age')
        
        # Parse birth date
        birth_date = None
        birth_str = personal_info.get('birth_date') or personal_info.get('birthday') or data.get('birthday')
        if birth_str:
            try:
                birth_date = datetime.strptime(birth_str, '%Y-%m-%d').date()
            except:
                pass
        
        # Create user
        user = UserProfileManager.create_user(
            username=data.get('username') or data.get('email') or f"user_{uuid.uuid4().hex[:8]}",
            full_name=full_name,
            age=age,
            birth_date=birth_date,
            email=data.get('email') or personal_info.get('email')
        )
        
        # Add allergens (from various formats)
        allergen_names = []
        
        # Handle food_allergens dict
        if 'food_allergens' in data:
            food_allergens = data['food_allergens']
            if isinstance(food_allergens, dict):
                for category, items in food_allergens.items():
                    if isinstance(items, dict):
                        allergen_names.extend([k.replace('_', ' ').title() for k, v in items.items() if v])
        
        # Handle beauty_allergens dict
        if 'beauty_allergens' in data:
            beauty_allergens = data['beauty_allergens']
            if isinstance(beauty_allergens, dict):
                for category, items in beauty_allergens.items():
                    if isinstance(items, dict):
                        allergen_names.extend([k.replace('_', ' ').title() for k, v in items.items() if v])
        
        # Handle simple allergens list
        if 'allergens' in data and isinstance(data['allergens'], list):
            allergen_names.extend(data['allergens'])
        
        if allergen_names:
            UserProfileManager.set_allergens(user, allergen_names)
        
        # Add preferences
        pref_names = []
        
        # Handle diet_preferences dict
        if 'diet_preferences' in data:
            diet_prefs = data['diet_preferences']
            if isinstance(diet_prefs, dict):
                for category, items in diet_prefs.items():
                    if isinstance(items, dict):
                        pref_names.extend([k.replace('_', ' ').title() for k, v in items.items() if v])
        
        # Handle health_preferences dict
        if 'health_preferences' in data:
            health_prefs = data['health_preferences']
            if isinstance(health_prefs, dict):
                pref_names.extend([k.replace('_', ' ').title() for k, v in health_prefs.items() if v])
        
        # Handle simple preferences list
        if 'preferences' in data and isinstance(data['preferences'], list):
            pref_names.extend(data['preferences'])
        
        if pref_names:
            UserProfileManager.set_preferences(user, pref_names)
        
        # Add comorbidities
        comorb_names = []
        
        # Handle comorbidities dict
        if 'comorbidities' in data:
            comorbs = data['comorbidities']
            if isinstance(comorbs, dict):
                for category, items in comorbs.items():
                    if isinstance(items, dict):
                        comorb_names.extend([k.replace('_', ' ').title() for k, v in items.items() if v])
            elif isinstance(comorbs, list):
                comorb_names.extend(comorbs)
        
        if comorb_names:
            UserProfileManager.set_comorbidities(user, comorb_names)
        
        return user
    
    @staticmethod
    def get_user_profile_dict(user: User) -> Dict[str, Any]:
        """
        Get user profile as dictionary (for API responses).
        Compatible with old UserProfile format.
        
        Args:
            user: User object
            
        Returns:
            Profile dictionary
        """
        profile = {
            'user_id': user.user_id,
            'username': user.username,
            'full_name': user.full_name,
            'email': user.email,
            'age': user.age,
            'birth_date': user.birth_date.isoformat() if user.birth_date else None,
            'allergens': user.get_allergen_names(),
            'preferences': user.get_preference_names(),
            'comorbidities': user.get_comorbidity_names(),
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
        }
        
        return profile


# ==================== HELPER FUNCTIONS ====================

def get_all_allergens() -> List[Dict[str, Any]]:
    """Get all available allergens."""
    allergens = Allergen.query.all()
    return [a.to_dict() for a in allergens]


def get_all_preferences() -> List[Dict[str, Any]]:
    """Get all available preferences."""
    prefs = Preference.query.all()
    return [p.to_dict() for p in prefs]


def get_all_comorbidities() -> List[Dict[str, Any]]:
    """Get all available comorbidities."""
    comorbs = Comorbidity.query.all()
    return [c.to_dict() for c in comorbs]


def search_allergens(query: str) -> List[Dict[str, Any]]:
    """Search allergens by name."""
    allergens = Allergen.query.filter(Allergen.name.ilike(f'%{query}%')).all()
    return [a.to_dict() for a in allergens]


def search_preferences(query: str, pref_type: str = None) -> List[Dict[str, Any]]:
    """Search preferences by name and optionally type."""
    q = Preference.query.filter(Preference.name.ilike(f'%{query}%'))
    if pref_type:
        q = q.filter_by(type=pref_type)
    prefs = q.all()
    return [p.to_dict() for p in prefs]


def search_comorbidities(query: str) -> List[Dict[str, Any]]:
    """Search comorbidities by name."""
    comorbs = Comorbidity.query.filter(Comorbidity.name.ilike(f'%{query}%')).all()
    return [c.to_dict() for c in comorbs]
