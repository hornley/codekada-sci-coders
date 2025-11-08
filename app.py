"""
Unified Main Application - Ingredient Intelligence Analyzer
Consolidated API for Flask backend integration

This module combines all CLI functionalities into a unified interface
suitable for backend server integration.
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

from src.main import IngredientIntelligenceAnalyzer
from src.models import UserHealthPreferences, ProductAnalysisResponse
from src.intake_tracker import IntakeTracker
from src.vision_ocr_detector import VisionOCRDetector
from src.user_profile import UserProfile


class IngredientAnalysisService:
    """
    Unified service for ingredient analysis and user management.
    Designed for Flask/FastAPI backend integration.
    """
    
    def __init__(self, ocr_method: str = 'vision'):
        """
        Initialize the analysis service.
        
        Args:
            ocr_method: OCR method ('vision' or 'paddleocr')
        """
        self.analyzer = IngredientIntelligenceAnalyzer(ocr_method=ocr_method)
    
    # ==================== ANALYSIS METHODS ====================
    
    def analyze_image(
        self,
        image_path: str,
        user_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Analyze product from image with optional user profile.
        
        Args:
            image_path: Path to product image
            user_profile: Optional user profile dict with health preferences
            
        Returns:
            Analysis result as dictionary
        """
        # Convert user profile dict to UserHealthPreferences if provided
        preferences = None
        if user_profile:
            preferences = self._dict_to_preferences(user_profile)
        
        # Analyze
        result = self.analyzer.analyze_product_image(
            image_path,
            user_preferences=preferences
        )
        
        return result.model_dump()
    
    def analyze_text(
        self,
        ingredients_text: str,
        product_type: Optional[str] = None,
        user_profile: Optional[Dict] = None,
        expiration_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze product from ingredients text.
        
        Args:
            ingredients_text: Ingredients text
            product_type: Optional product type (food/drink/beauty)
            user_profile: Optional user profile dict
            expiration_date: Optional expiration date
            
        Returns:
            Analysis result as dictionary
        """
        # Convert user profile
        preferences = None
        if user_profile:
            preferences = self._dict_to_preferences(user_profile)
        
        # Analyze
        result = self.analyzer.analyze_from_text(
            ingredients_text=ingredients_text,
            product_type=product_type,
            expiration_date=expiration_date,
            user_preferences=preferences
        )
        
        return result.model_dump()
    
    def extract_ingredients_only(self, image_path: str) -> Dict[str, Any]:
        """
        Extract ingredients text from image without full analysis.
        Useful for quick OCR extraction.
        
        Args:
            image_path: Path to product image
            
        Returns:
            OCR result with extracted text
        """
        detector = VisionOCRDetector()
        result = detector.detect(image_path)
        return result
    
    # ==================== USER PROFILE METHODS ====================
    
    def create_user_profile(self, profile_data: Dict) -> Dict[str, Any]:
        """
        Create a new user profile from registration data.
        
        Args:
            profile_data: Dictionary containing all user profile fields
            
        Returns:
            Created user profile with ID
        """
        # Create UserProfile instance
        user_profile = UserProfile(**profile_data)
        
        # Save to database
        user_id = user_profile.save_to_database()
        
        return {
            "success": True,
            "user_id": user_id,
            "message": "User profile created successfully"
        }
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            User profile dictionary or None
        """
        user_profile = UserProfile.load_from_database(user_id)
        if user_profile:
            return user_profile.to_dict()
        return None
    
    def update_user_profile(self, user_id: str, updates: Dict) -> Dict[str, Any]:
        """
        Update user profile.
        
        Args:
            user_id: User identifier
            updates: Dictionary of fields to update
            
        Returns:
            Success response
        """
        user_profile = UserProfile.load_from_database(user_id)
        if not user_profile:
            return {"success": False, "error": "User not found"}
        
        # Update fields
        for key, value in updates.items():
            if hasattr(user_profile, key):
                setattr(user_profile, key, value)
        
        # Save
        user_profile.save_to_database()
        
        return {
            "success": True,
            "message": "Profile updated successfully"
        }
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user health preferences for analysis.
        
        Args:
            user_id: User identifier
            
        Returns:
            Health preferences dictionary
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        preferences = tracker.load_user_preferences()
        
        if preferences:
            return {
                "allergies": preferences.allergies,
                "dietary_restrictions": preferences.dietary_restrictions,
                "avoid_ingredients": preferences.avoid_ingredients,
                "health_goals": preferences.health_goals
            }
        return None
    
    def save_user_preferences(
        self,
        user_id: str,
        preferences: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Save user health preferences.
        
        Args:
            user_id: User identifier
            preferences: Dictionary with health preferences
            
        Returns:
            Success response
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        
        prefs = UserHealthPreferences(
            allergies=preferences.get('allergies', []),
            dietary_restrictions=preferences.get('dietary_restrictions', []),
            avoid_ingredients=preferences.get('avoid_ingredients', []),
            health_goals=preferences.get('health_goals', [])
        )
        
        tracker.save_user_preferences(prefs)
        
        return {
            "success": True,
            "message": "Preferences saved successfully"
        }
    
    # ==================== INTAKE TRACKING METHODS ====================
    
    def log_intake(
        self,
        user_id: str,
        analysis_result: Dict,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log consumed product to user's intake history.
        
        Args:
            user_id: User identifier
            analysis_result: Product analysis result
            timestamp: Optional consumption timestamp (ISO format)
            
        Returns:
            Success response with entry ID
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        
        # Convert dict to ProductAnalysisResponse
        analysis = ProductAnalysisResponse(**analysis_result)
        
        # Parse timestamp if provided
        ts = None
        if timestamp:
            ts = datetime.fromisoformat(timestamp)
        
        # Log intake
        entry_id = tracker.log_intake(analysis, timestamp=ts)
        
        return {
            "success": True,
            "entry_id": entry_id,
            "message": "Product logged to intake history"
        }
    
    def get_daily_summary(
        self,
        user_id: str,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get daily intake summary for user.
        
        Args:
            user_id: User identifier
            date: Optional date (YYYY-MM-DD), defaults to today
            
        Returns:
            Daily summary with metrics
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        
        # Parse date if provided
        target_date = None
        if date:
            target_date = datetime.strptime(date, '%Y-%m-%d')
        
        return tracker.get_daily_summary(date=target_date)
    
    def get_weekly_report(
        self,
        user_id: str,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get weekly intake report for user.
        
        Args:
            user_id: User identifier
            end_date: Optional end date (YYYY-MM-DD), defaults to today
            
        Returns:
            Weekly report with insights
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        
        # Parse end date if provided
        target_date = None
        if end_date:
            target_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        return tracker.get_weekly_report(end_date=target_date)
    
    def get_intake_history(
        self,
        user_id: str,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Get intake history for user.
        
        Args:
            user_id: User identifier
            limit: Number of entries to return
            
        Returns:
            List of consumed products
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        history = tracker.get_all_history(limit=limit)
        
        return {
            "history": history,
            "count": len(history)
        }
    
    def check_product_history(
        self,
        user_id: str,
        product_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Check if user has consumed a product before.
        
        Args:
            user_id: User identifier
            product_name: Product name to check
            
        Returns:
            Previous consumption data or None
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        return tracker.check_product_against_history(product_name)
    
    def delete_intake_entry(
        self,
        user_id: str,
        entry_id: int
    ) -> Dict[str, Any]:
        """
        Delete an intake entry.
        
        Args:
            user_id: User identifier
            entry_id: Entry ID to delete
            
        Returns:
            Success response
        """
        tracker = IntakeTracker(db_path=f"intake_{user_id}.db")
        deleted = tracker.delete_entry(entry_id)
        
        if deleted:
            return {"success": True, "message": "Entry deleted"}
        else:
            return {"success": False, "error": "Entry not found"}
    
    # ==================== BATCH OPERATIONS ====================
    
    def analyze_batch(
        self,
        items: List[Dict[str, Any]],
        user_profile: Optional[Dict] = None
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple products in batch.
        
        Args:
            items: List of items to analyze (each with 'type' and 'data')
            user_profile: Optional user profile
            
        Returns:
            List of analysis results
        """
        results = []
        
        for item in items:
            if item['type'] == 'image':
                result = self.analyze_image(item['data'], user_profile)
            elif item['type'] == 'text':
                result = self.analyze_text(
                    item['data'],
                    item.get('product_type'),
                    user_profile
                )
            else:
                result = {"success": False, "error": "Invalid item type"}
            
            results.append(result)
        
        return results
    
    # ==================== HELPER METHODS ====================
    
    def _dict_to_preferences(self, profile: Dict) -> UserHealthPreferences:
        """Convert dictionary to UserHealthPreferences object."""
        return UserHealthPreferences(
            allergies=profile.get('allergies', profile.get('allergens', [])),
            dietary_restrictions=profile.get('dietary_restrictions', profile.get('diet_preferences', [])),
            avoid_ingredients=profile.get('avoid_ingredients', []),
            health_goals=profile.get('health_goals', profile.get('health_preferences', []))
        )
    
    def health_check(self) -> Dict[str, Any]:
        """
        Health check endpoint.
        
        Returns:
            Service status
        """
        return {
            "status": "healthy",
            "service": "Ingredient Intelligence Analyzer",
            "version": "3.0.0",
            "features": [
                "image_analysis",
                "text_analysis",
                "user_profiles",
                "intake_tracking",
                "personalized_recommendations"
            ]
        }


# ==================== CONVENIENCE FUNCTIONS ====================

def analyze_product_quick(
    image_path: str,
    user_allergies: Optional[List[str]] = None,
    user_restrictions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Quick analysis function for simple use cases.
    
    Args:
        image_path: Path to product image
        user_allergies: Optional list of allergies
        user_restrictions: Optional list of dietary restrictions
        
    Returns:
        Analysis result
    """
    service = IngredientAnalysisService()
    
    user_profile = None
    if user_allergies or user_restrictions:
        user_profile = {
            'allergies': user_allergies or [],
            'dietary_restrictions': user_restrictions or []
        }
    
    return service.analyze_image(image_path, user_profile)


def get_user_analysis(
    user_id: str,
    image_path: str
) -> Dict[str, Any]:
    """
    Analyze product with user's saved preferences.
    
    Args:
        user_id: User identifier
        image_path: Path to product image
        
    Returns:
        Personalized analysis result
    """
    service = IngredientAnalysisService()
    
    # Load user preferences
    user_profile = service.get_user_preferences(user_id)
    
    # Analyze
    return service.analyze_image(image_path, user_profile)


# ==================== MAIN (for testing) ====================

if __name__ == "__main__":
    import sys
    
    # Demo usage
    service = IngredientAnalysisService()
    
    print("\n" + "="*70)
    print("🧪 INGREDIENT ANALYSIS SERVICE - DEMO")
    print("="*70)
    
    # Health check
    health = service.health_check()
    print(f"\n✓ Service: {health['service']}")
    print(f"✓ Version: {health['version']}")
    print(f"✓ Status: {health['status']}")
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        print(f"\n📸 Analyzing: {image_path}")
        
        # Example with user preferences
        user_profile = {
            'allergies': ['peanuts', 'milk'],
            'dietary_restrictions': ['vegan'],
            'health_goals': ['weight loss']
        }
        
        result = service.analyze_image(image_path, user_profile)
        
        print(f"\n✓ Product: {result.get('product_name', 'Unknown')}")
        print(f"✓ Health Rating: {result['healthiness_rating']}/10")
        if result.get('safety_score_for_user'):
            print(f"✓ Your Safety Score: {result['safety_score_for_user']}/10")
        
        print("\n" + "="*70)
    else:
        print("\nUsage: python app.py <image_path>")
        print("\nThis service provides:")
        print("  • Product analysis from images and text")
        print("  • User profile management")
        print("  • Personalized health recommendations")
        print("  • Intake tracking and reports")
