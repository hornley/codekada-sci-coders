"""
Data models for the Ingredient Intelligence Analyzer
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class UserHealthPreferences(BaseModel):
    """User's health preferences and restrictions."""
    allergies: List[str] = Field(default_factory=list, description="Personal allergies (e.g., peanuts, milk)")
    dietary_restrictions: List[str] = Field(default_factory=list, description="Dietary restrictions (e.g., vegan, gluten-free)")
    avoid_ingredients: List[str] = Field(default_factory=list, description="Ingredients to avoid (e.g., high-sugar, artificial-colors)")
    health_goals: List[str] = Field(default_factory=list, description="Health goals (e.g., weight-loss, muscle-gain)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "allergies": ["peanuts", "milk"],
                "dietary_restrictions": ["vegan", "gluten-free"],
                "avoid_ingredients": ["high-sugar", "artificial-colors"],
                "health_goals": ["weight-loss", "heart-health"]
            }
        }


class OCRResult(BaseModel):
    """Result from OCR detection."""
    success: bool
    product_name: Optional[str] = None
    ingredients_text: Optional[str] = None
    expiration_date: Optional[str] = None
    manufacture_date: Optional[str] = None
    full_text: str = ""
    error: Optional[str] = None


class ClassificationResult(BaseModel):
    """Result from product type classification."""
    product_type: str  # food, drink, beauty, or unknown
    confidence: float = Field(ge=0.0, le=1.0)
    scores: Optional[Dict[str, int]] = None


class AnalysisResult(BaseModel):
    """Result from ingredient analysis."""
    success: bool
    harmful_ingredients: List[str] = Field(default_factory=list)
    additives: List[str] = Field(default_factory=list)
    preservatives: List[str] = Field(default_factory=list)
    irritants: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    chemicals: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    fda_approval: str = "Unverified"
    healthiness_rating: int = Field(ge=1, le=10, default=5)
    expiration_valid: bool = True
    recommendation: str = ""
    health_suggestion: str = ""
    error: Optional[str] = None
    model_used: Optional[str] = None
    analysis_date: Optional[str] = None


class ProductAnalysisResponse(BaseModel):
    """Complete response from the analysis pipeline."""
    success: bool
    product_type: str
    product_name: Optional[str] = None
    classification_confidence: float = 0.0
    
    # OCR Data
    ingredients_text: Optional[str] = None
    expiration_date: Optional[str] = None
    manufacture_date: Optional[str] = None
    
    # Analysis Results
    harmful_ingredients: List[str] = Field(default_factory=list)
    additives: List[str] = Field(default_factory=list)
    preservatives: List[str] = Field(default_factory=list)
    irritants: List[str] = Field(default_factory=list)
    allergens: List[str] = Field(default_factory=list)
    chemicals: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    fda_approval: str = "Unverified"
    healthiness_rating: int = Field(ge=1, le=10, default=5)
    expiration_valid: bool = True
    days_until_expiration: Optional[int] = None
    recommendation: str = ""
    health_suggestion: str = ""
    
    # Phase 2: Personalization
    personalized_recommendation: Optional[str] = None
    safety_score_for_user: Optional[int] = Field(None, ge=1, le=10)
    warnings_for_user: List[str] = Field(default_factory=list)
    matches_preferences: Optional[bool] = None
    
    # Metadata
    processing_time: Optional[float] = None
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "product_type": "food",
                "product_name": "Chocolate Chip Cookies",
                "classification_confidence": 0.85,
                "ingredients_text": "Sugar, Palm oil, Sodium benzoate, Artificial flavor",
                "expiration_date": "2026-03-12",
                "harmful_ingredients": ["Sodium benzoate"],
                "additives": ["Artificial flavor"],
                "preservatives": ["Sodium benzoate"],
                "allergens": ["May contain milk"],
                "healthiness_rating": 4,
                "expiration_valid": True,
                "recommendation": "Consume in moderation due to high sugar content.",
                "health_suggestion": "Consider healthier snack alternatives with natural ingredients."
            }
        }
