"""
Ingredient Intelligence Analyzer Package
"""

from src.main import IngredientIntelligenceAnalyzer
from src.vision_ocr_detector import VisionOCRDetector
from src.classifier import ProductClassifier
from src.ingredient_analyzer import IngredientAnalyzer
from src.models import ProductAnalysisResponse, UserHealthPreferences
from src.utils import pretty_print_results, save_results_to_json
from src.intake_tracker import IntakeTracker

# OCRDetector is optional (only if PaddleOCR is installed)
try:
    from src.ocr_detector import OCRDetector
    __all__ = [
        "IngredientIntelligenceAnalyzer",
        "OCRDetector",
        "VisionOCRDetector",
        "ProductClassifier",
        "IngredientAnalyzer",
        "ProductAnalysisResponse",
        "UserHealthPreferences",
        "IntakeTracker",
        "pretty_print_results",
        "save_results_to_json"
    ]
except ImportError:
    __all__ = [
        "IngredientIntelligenceAnalyzer",
        "VisionOCRDetector",
        "ProductClassifier",
        "IngredientAnalyzer",
        "ProductAnalysisResponse",
        "UserHealthPreferences",
        "IntakeTracker",
        "pretty_print_results",
        "save_results_to_json"
    ]

__version__ = "3.0.0"  # Updated to 3.0.0 with Phase 2 & 3 (Personalization + Intake Tracking)
