"""
User Profile Database Models
Comprehensive user health profile with allergens, diet preferences, and comorbidities
"""

from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field, EmailStr, validator
import sqlite3
import json


class UserProfile(BaseModel):
    """Complete user profile with health information."""
    
    # Basic Information
    user_id: str = Field(..., description="Unique user identifier")
    full_name: str = Field(..., description="User's full name")
    age: int = Field(..., ge=0, le=150, description="User's age")
    birth_date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    email: Optional[EmailStr] = None
    
    # Food Allergens & Irritants
    # Biological Allergens - Animal-derived
    allergen_milk: bool = False
    allergen_eggs: bool = False
    allergen_fish: bool = False
    allergen_shellfish: bool = False
    
    # Biological Allergens - Plant-derived
    allergen_peanuts: bool = False
    allergen_tree_nuts: bool = False
    allergen_soybeans: bool = False
    allergen_wheat: bool = False
    allergen_sesame: bool = False
    
    # Chemical Irritants
    irritant_msg: bool = False
    irritant_preservatives: bool = False
    irritant_artificial_colors: bool = False
    irritant_artificial_sweeteners: bool = False
    irritant_acids: bool = False
    irritant_emulsifiers: bool = False
    irritant_flavoring_agents: bool = False
    
    # Beauty Product Allergens
    # Fragrance-Related
    beauty_fragrance: bool = False
    beauty_limonene: bool = False
    beauty_linalool: bool = False
    beauty_citronellol: bool = False
    beauty_geraniol: bool = False
    beauty_eugenol: bool = False
    beauty_cinnamal: bool = False
    beauty_balsam_peru: bool = False
    
    # Beauty Preservatives
    beauty_parabens: bool = False
    beauty_formaldehyde: bool = False
    beauty_isothiazolinones: bool = False
    beauty_phenoxyethanol: bool = False
    beauty_sodium_benzoate: bool = False
    beauty_potassium_sorbate: bool = False
    beauty_benzyl_alcohol: bool = False
    
    # Beauty Botanical & Natural Extracts
    beauty_essential_oils: bool = False
    beauty_aloe_vera: bool = False
    beauty_chamomile: bool = False
    beauty_calendula: bool = False
    beauty_coconut_oil: bool = False
    beauty_shea_butter: bool = False
    beauty_almond_oil: bool = False
    beauty_eucalyptus: bool = False
    
    # Diet Preferences - Plant-Based
    diet_vegan: bool = False
    diet_vegetarian: bool = False
    diet_pescatarian: bool = False
    diet_flexitarian: bool = False
    
    # Diet Preferences - Animal-Based / Low-Carb
    diet_keto: bool = False
    diet_paleo: bool = False
    diet_carnivore: bool = False
    diet_atkins: bool = False
    
    # Diet Preferences - Religion/Culture-Based
    diet_halal: bool = False
    diet_kosher: bool = False
    diet_hindu: bool = False
    diet_buddhist: bool = False
    diet_rastafarian: bool = False
    
    # Health Preferences
    health_gluten_free: bool = False
    health_lactose_free: bool = False
    health_low_sodium: bool = False
    health_low_fat: bool = False
    health_low_carb: bool = False
    health_diabetic: bool = False
    health_allergen_free: bool = False
    
    # Comorbidities - Cardiovascular
    comorbid_hypertension: bool = False
    comorbid_hyperlipidemia: bool = False
    comorbid_cad: bool = False
    comorbid_heart_failure: bool = False
    comorbid_atrial_fib: bool = False
    comorbid_pad: bool = False
    
    # Comorbidities - Metabolic & Endocrine
    comorbid_diabetes: bool = False
    comorbid_obesity: bool = False
    comorbid_hypothyroid: bool = False
    comorbid_hyperthyroid: bool = False
    comorbid_pcos: bool = False
    comorbid_gout: bool = False
    
    # Comorbidities - Respiratory
    comorbid_asthma: bool = False
    comorbid_copd: bool = False
    comorbid_bronchitis: bool = False
    comorbid_sleep_apnea: bool = False
    comorbid_pulmonary_hypertension: bool = False
    
    # Metadata
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        """Validate birth date format."""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('birth_date must be in YYYY-MM-DD format')
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user123",
                "full_name": "John Doe",
                "age": 30,
                "birth_date": "1994-05-15",
                "email": "john@example.com",
                "allergen_peanuts": True,
                "allergen_shellfish": True,
                "diet_vegan": True,
                "health_gluten_free": True,
                "comorbid_diabetes": True
            }
        }


class UserProfileDB:
    """Database manager for user profiles."""
    
    def __init__(self, db_path: str = "user_profiles.db"):
        """
        Initialize user profile database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self):
        """Create user profiles table if not exists."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL,
                birth_date TEXT NOT NULL,
                email TEXT,
                
                -- Food Allergens (Animal-derived)
                allergen_milk INTEGER DEFAULT 0,
                allergen_eggs INTEGER DEFAULT 0,
                allergen_fish INTEGER DEFAULT 0,
                allergen_shellfish INTEGER DEFAULT 0,
                
                -- Food Allergens (Plant-derived)
                allergen_peanuts INTEGER DEFAULT 0,
                allergen_tree_nuts INTEGER DEFAULT 0,
                allergen_soybeans INTEGER DEFAULT 0,
                allergen_wheat INTEGER DEFAULT 0,
                allergen_sesame INTEGER DEFAULT 0,
                
                -- Chemical Irritants
                irritant_msg INTEGER DEFAULT 0,
                irritant_preservatives INTEGER DEFAULT 0,
                irritant_artificial_colors INTEGER DEFAULT 0,
                irritant_artificial_sweeteners INTEGER DEFAULT 0,
                irritant_acids INTEGER DEFAULT 0,
                irritant_emulsifiers INTEGER DEFAULT 0,
                irritant_flavoring_agents INTEGER DEFAULT 0,
                
                -- Beauty Allergens (Fragrance)
                beauty_fragrance INTEGER DEFAULT 0,
                beauty_limonene INTEGER DEFAULT 0,
                beauty_linalool INTEGER DEFAULT 0,
                beauty_citronellol INTEGER DEFAULT 0,
                beauty_geraniol INTEGER DEFAULT 0,
                beauty_eugenol INTEGER DEFAULT 0,
                beauty_cinnamal INTEGER DEFAULT 0,
                beauty_balsam_peru INTEGER DEFAULT 0,
                
                -- Beauty Preservatives
                beauty_parabens INTEGER DEFAULT 0,
                beauty_formaldehyde INTEGER DEFAULT 0,
                beauty_isothiazolinones INTEGER DEFAULT 0,
                beauty_phenoxyethanol INTEGER DEFAULT 0,
                beauty_sodium_benzoate INTEGER DEFAULT 0,
                beauty_potassium_sorbate INTEGER DEFAULT 0,
                beauty_benzyl_alcohol INTEGER DEFAULT 0,
                
                -- Beauty Botanical
                beauty_essential_oils INTEGER DEFAULT 0,
                beauty_aloe_vera INTEGER DEFAULT 0,
                beauty_chamomile INTEGER DEFAULT 0,
                beauty_calendula INTEGER DEFAULT 0,
                beauty_coconut_oil INTEGER DEFAULT 0,
                beauty_shea_butter INTEGER DEFAULT 0,
                beauty_almond_oil INTEGER DEFAULT 0,
                beauty_eucalyptus INTEGER DEFAULT 0,
                
                -- Diet Preferences (Plant-based)
                diet_vegan INTEGER DEFAULT 0,
                diet_vegetarian INTEGER DEFAULT 0,
                diet_pescatarian INTEGER DEFAULT 0,
                diet_flexitarian INTEGER DEFAULT 0,
                
                -- Diet Preferences (Animal-based/Low-carb)
                diet_keto INTEGER DEFAULT 0,
                diet_paleo INTEGER DEFAULT 0,
                diet_carnivore INTEGER DEFAULT 0,
                diet_atkins INTEGER DEFAULT 0,
                
                -- Diet Preferences (Religion/Culture)
                diet_halal INTEGER DEFAULT 0,
                diet_kosher INTEGER DEFAULT 0,
                diet_hindu INTEGER DEFAULT 0,
                diet_buddhist INTEGER DEFAULT 0,
                diet_rastafarian INTEGER DEFAULT 0,
                
                -- Health Preferences
                health_gluten_free INTEGER DEFAULT 0,
                health_lactose_free INTEGER DEFAULT 0,
                health_low_sodium INTEGER DEFAULT 0,
                health_low_fat INTEGER DEFAULT 0,
                health_low_carb INTEGER DEFAULT 0,
                health_diabetic INTEGER DEFAULT 0,
                health_allergen_free INTEGER DEFAULT 0,
                
                -- Comorbidities (Cardiovascular)
                comorbid_hypertension INTEGER DEFAULT 0,
                comorbid_hyperlipidemia INTEGER DEFAULT 0,
                comorbid_cad INTEGER DEFAULT 0,
                comorbid_heart_failure INTEGER DEFAULT 0,
                comorbid_atrial_fib INTEGER DEFAULT 0,
                comorbid_pad INTEGER DEFAULT 0,
                
                -- Comorbidities (Metabolic & Endocrine)
                comorbid_diabetes INTEGER DEFAULT 0,
                comorbid_obesity INTEGER DEFAULT 0,
                comorbid_hypothyroid INTEGER DEFAULT 0,
                comorbid_hyperthyroid INTEGER DEFAULT 0,
                comorbid_pcos INTEGER DEFAULT 0,
                comorbid_gout INTEGER DEFAULT 0,
                
                -- Comorbidities (Respiratory)
                comorbid_asthma INTEGER DEFAULT 0,
                comorbid_copd INTEGER DEFAULT 0,
                comorbid_bronchitis INTEGER DEFAULT 0,
                comorbid_sleep_apnea INTEGER DEFAULT 0,
                comorbid_pulmonary_hypertension INTEGER DEFAULT 0,
                
                -- Metadata
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_profile(self, profile: UserProfile) -> bool:
        """
        Create a new user profile.
        
        Args:
            profile: UserProfile object
            
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        profile.created_at = now
        profile.updated_at = now
        
        try:
            # Convert boolean fields to integers for SQLite
            profile_dict = profile.model_dump()
            
            # Build column names and values
            columns = list(profile_dict.keys())
            values = [int(v) if isinstance(v, bool) else v for v in profile_dict.values()]
            
            placeholders = ','.join(['?' for _ in columns])
            column_names = ','.join(columns)
            
            cursor.execute(
                f"INSERT INTO user_profiles ({column_names}) VALUES ({placeholders})",
                values
            )
            
            conn.commit()
            return True
        
        except sqlite3.IntegrityError:
            # User already exists
            return False
        finally:
            conn.close()
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile by user_id.
        
        Args:
            user_id: User identifier
            
        Returns:
            UserProfile object or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Convert row to dict and booleans
            profile_dict = dict(row)
            
            # Convert integer fields back to booleans
            for key, value in profile_dict.items():
                if key.startswith(('allergen_', 'irritant_', 'beauty_', 'diet_', 'health_', 'comorbid_')):
                    profile_dict[key] = bool(value)
            
            return UserProfile(**profile_dict)
        
        return None
    
    def update_profile(self, profile: UserProfile) -> bool:
        """
        Update existing user profile.
        
        Args:
            profile: UserProfile object
            
        Returns:
            True if successful, False if user not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        profile.updated_at = datetime.now().isoformat()
        profile_dict = profile.model_dump()
        
        # Remove user_id and created_at from update
        profile_dict.pop('created_at', None)
        user_id = profile_dict.pop('user_id')
        
        # Convert booleans to integers
        values = [int(v) if isinstance(v, bool) else v for v in profile_dict.values()]
        
        # Build SET clause
        set_clause = ','.join([f"{k} = ?" for k in profile_dict.keys()])
        values.append(user_id)
        
        cursor.execute(
            f"UPDATE user_profiles SET {set_clause} WHERE user_id = ?",
            values
        )
        
        updated = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return updated
    
    def delete_profile(self, user_id: str) -> bool:
        """
        Delete user profile.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user_profiles WHERE user_id = ?", (user_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def list_profiles(self, limit: int = 100) -> List[UserProfile]:
        """
        List all user profiles.
        
        Args:
            limit: Maximum number of profiles to return
            
        Returns:
            List of UserProfile objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_profiles LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        profiles = []
        for row in rows:
            profile_dict = dict(row)
            
            # Convert integer fields back to booleans
            for key, value in profile_dict.items():
                if key.startswith(('allergen_', 'irritant_', 'beauty_', 'diet_', 'health_', 'comorbid_')):
                    profile_dict[key] = bool(value)
            
            profiles.append(UserProfile(**profile_dict))
        
        return profiles


if __name__ == "__main__":
    # Test the user profile database
    print("Testing UserProfileDB...")
    
    db = UserProfileDB("test_profiles.db")
    
    # Create test profile
    test_profile = UserProfile(
        user_id="test_user_001",
        full_name="John Doe",
        age=30,
        birth_date="1994-05-15",
        email="john@example.com",
        allergen_peanuts=True,
        allergen_shellfish=True,
        diet_vegan=True,
        health_gluten_free=True,
        comorbid_diabetes=True,
        comorbid_hypertension=True
    )
    
    # Create profile
    created = db.create_profile(test_profile)
    print(f"✓ Profile created: {created}")
    
    # Get profile
    retrieved = db.get_profile("test_user_001")
    if retrieved:
        print(f"✓ Profile retrieved: {retrieved.full_name}")
        print(f"  Allergies: peanuts={retrieved.allergen_peanuts}, shellfish={retrieved.allergen_shellfish}")
        print(f"  Diet: vegan={retrieved.diet_vegan}")
        print(f"  Health: gluten-free={retrieved.health_gluten_free}")
        print(f"  Comorbidities: diabetes={retrieved.comorbid_diabetes}")
    
    # Update profile
    test_profile.age = 31
    test_profile.allergen_milk = True
    updated = db.update_profile(test_profile)
    print(f"✓ Profile updated: {updated}")
    
    # List profiles
    all_profiles = db.list_profiles()
    print(f"✓ Total profiles: {len(all_profiles)}")
    
    print("\n✅ UserProfileDB test complete!")
