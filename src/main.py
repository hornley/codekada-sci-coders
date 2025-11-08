"""
Main Orchestration Pipeline
Coordinates OCR detection, classification, and AI analysis.
"""

import os
import time
from typing import Dict, Optional
from dotenv import load_dotenv

from src.vision_ocr_detector import VisionOCRDetector
from src.classifier import ProductClassifier
from src.ingredient_analyzer import IngredientAnalyzer
from src.models import ProductAnalysisResponse, UserHealthPreferences

# Load environment variables
load_dotenv()


class IngredientIntelligenceAnalyzer:
    """Main class that orchestrates the complete analysis pipeline."""
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        ocr_method: str = 'vision',
        ocr_lang: str = 'en',
        use_gpu: bool = False,
        max_image_dimension: int = 1920
    ):
        """
        Initialize the analyzer pipeline.
        
        Args:
            openai_api_key: OpenAI API key
            ocr_method: OCR method to use - 'vision' (OpenAI Vision API - default) or 'paddleocr' (local OCR)
            ocr_lang: Language for OCR (only used with paddleocr)
            use_gpu: Whether to use GPU for OCR (only used with paddleocr)
            max_image_dimension: Max image size for OCR processing (only used with paddleocr)
        """
        # Initialize OCR detector based on method
        self.ocr_method = ocr_method.lower()
        
        if self.ocr_method == 'vision':
            print("   ℹ️  Using OpenAI Vision API for OCR (recommended)")
            self.ocr_detector = VisionOCRDetector(api_key=openai_api_key)
        elif self.ocr_method == 'paddleocr':
            print("   ℹ️  Using PaddleOCR for local OCR")
            try:
                from src.ocr_detector import OCRDetector
                self.ocr_detector = OCRDetector(
                    lang=ocr_lang, 
                    use_gpu=use_gpu,
                    max_image_dimension=max_image_dimension
                )
            except ImportError:
                raise ImportError(
                    "PaddleOCR dependencies not installed. "
                    "Install with: pip install paddleocr paddlepaddle opencv-python\n"
                    "Or use Vision API: ocr_method='vision'"
                )
        else:
            raise ValueError(f"Invalid ocr_method: {ocr_method}. Use 'vision' or 'paddleocr'")
        
        self.classifier = ProductClassifier()
        self.analyzer = IngredientAnalyzer(api_key=openai_api_key)
    
    def analyze_product_image(
        self, 
        image_path: str, 
        user_preferences: Optional[UserHealthPreferences] = None
    ) -> ProductAnalysisResponse:
        """
        Complete analysis pipeline: OCR → Classification → AI Analysis.
        
        Args:
            image_path: Path to product image
            user_preferences: Optional user health preferences for personalized analysis
            
        Returns:
            Complete analysis response
        """
        start_time = time.time()
        
        try:
            # Step 1: OCR Detection
            print("🔍 Step 1: Extracting text from image...")
            ocr_result = self.ocr_detector.detect(image_path)
            
            if not ocr_result['success']:
                return ProductAnalysisResponse(
                    success=False,
                    product_type='unknown',
                    error=f"OCR failed: {ocr_result.get('error', 'Unknown error')}",
                    processing_time=time.time() - start_time
                )
            
            print(f"   ✓ Extracted product name: {ocr_result.get('product_name', 'Unknown')}")
            print(f"   ✓ Found ingredients: {'Yes' if ocr_result.get('ingredients_text') else 'No'}")
            
            # Step 2: Product Classification
            print("\n📊 Step 2: Classifying product type...")
            classification = self.classifier.classify(
                full_text=ocr_result['full_text'],
                ingredients_text=ocr_result.get('ingredients_text'),
                product_name=ocr_result.get('product_name')
            )
            
            print(f"   ✓ Product type: {classification['product_type']} "
                  f"(confidence: {classification['confidence']})")
            
            # Step 3: AI Analysis
            if not ocr_result.get('ingredients_text'):
                print("\n⚠️  Warning: No ingredients found, skipping AI analysis")
                return ProductAnalysisResponse(
                    success=True,
                    product_type=classification['product_type'],
                    product_name=ocr_result.get('product_name'),
                    classification_confidence=classification['confidence'],
                    expiration_date=ocr_result.get('expiration_date'),
                    manufacture_date=ocr_result.get('manufacture_date'),
                    error="No ingredients found for detailed analysis",
                    processing_time=time.time() - start_time
                )
            
            print("\n🧠 Step 3: Analyzing ingredients with AI...")
            analysis = self.analyzer.analyze(
                product_type=classification['product_type'],
                ingredients_text=ocr_result['ingredients_text'],
                expiration_date=ocr_result.get('expiration_date'),
                manufacture_date=ocr_result.get('manufacture_date'),
                user_preferences=user_preferences
            )
            
            if not analysis['success']:
                return ProductAnalysisResponse(
                    success=False,
                    product_type=classification['product_type'],
                    product_name=ocr_result.get('product_name'),
                    classification_confidence=classification['confidence'],
                    ingredients_text=ocr_result.get('ingredients_text'),
                    expiration_date=ocr_result.get('expiration_date'),
                    error=f"Analysis failed: {analysis.get('error', 'Unknown error')}",
                    processing_time=time.time() - start_time
                )
            
            print(f"   ✓ Healthiness rating: {analysis.get('healthiness_rating', 'N/A')}/10")
            print(f"   ✓ Harmful ingredients: {len(analysis.get('harmful_ingredients', []))}")
            print(f"   ✓ Allergens: {len(analysis.get('allergens', []))}")
            
            # Step 4: Combine results
            processing_time = time.time() - start_time
            print(f"\n✅ Analysis complete in {processing_time:.2f} seconds\n")
            
            response = ProductAnalysisResponse(
                success=True,
                product_type=classification['product_type'],
                product_name=ocr_result.get('product_name'),
                classification_confidence=classification['confidence'],
                ingredients_text=ocr_result.get('ingredients_text'),
                expiration_date=ocr_result.get('expiration_date'),
                manufacture_date=ocr_result.get('manufacture_date'),
                harmful_ingredients=analysis.get('harmful_ingredients', []),
                additives=analysis.get('additives', []),
                preservatives=analysis.get('preservatives', []),
                irritants=analysis.get('irritants', []),
                allergens=analysis.get('allergens', []),
                chemicals=analysis.get('chemicals', []),
                certifications=analysis.get('certifications', []),
                fda_approval=analysis.get('fda_approval', 'Unverified'),
                healthiness_rating=analysis.get('healthiness_rating', 5),
                expiration_valid=analysis.get('expiration_valid', True),
                recommendation=analysis.get('recommendation', ''),
                health_suggestion=analysis.get('health_suggestion', ''),
                processing_time=processing_time
            )
            
            # Add personalization if user preferences provided
            if user_preferences:
                response.personalized_recommendation = analysis.get('personalized_recommendation')
                response.safety_score_for_user = analysis.get('safety_score_for_user')
                response.warnings_for_user = analysis.get('warnings_for_user', [])
                response.matches_preferences = analysis.get('matches_preferences')
            
            return response
        
        except Exception as e:
            return ProductAnalysisResponse(
                success=False,
                product_type='unknown',
                error=f"Pipeline error: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def analyze_from_text(
        self,
        ingredients_text: str,
        product_type: Optional[str] = None,
        expiration_date: Optional[str] = None,
        user_preferences: Optional[UserHealthPreferences] = None
    ) -> ProductAnalysisResponse:
        """
        Analyze ingredients from text directly (skip OCR).
        
        Args:
            ingredients_text: Ingredients list as text
            product_type: Optional product type (will classify if not provided)
            expiration_date: Optional expiration date
            user_preferences: Optional user health preferences for personalized analysis
            
        Returns:
            Analysis response
        """
        start_time = time.time()
        
        try:
            # Classify if not provided
            if not product_type:
                print("📊 Classifying product type...")
                classification = self.classifier.classify(
                    full_text=ingredients_text,
                    ingredients_text=ingredients_text
                )
                product_type = classification['product_type']
                confidence = classification['confidence']
                print(f"   ✓ Product type: {product_type} (confidence: {confidence})")
            else:
                confidence = 1.0
            
            # Analyze ingredients
            print("🧠 Analyzing ingredients with AI...")
            analysis = self.analyzer.analyze(
                product_type=product_type,
                ingredients_text=ingredients_text,
                expiration_date=expiration_date,
                user_preferences=user_preferences
            )
            
            if not analysis['success']:
                return ProductAnalysisResponse(
                    success=False,
                    product_type=product_type,
                    classification_confidence=confidence,
                    ingredients_text=ingredients_text,
                    error=analysis.get('error', 'Analysis failed'),
                    processing_time=time.time() - start_time
                )
            
            processing_time = time.time() - start_time
            print(f"✅ Analysis complete in {processing_time:.2f} seconds\n")
            
            response = ProductAnalysisResponse(
                success=True,
                product_type=product_type,
                classification_confidence=confidence,
                ingredients_text=ingredients_text,
                expiration_date=expiration_date,
                harmful_ingredients=analysis.get('harmful_ingredients', []),
                additives=analysis.get('additives', []),
                preservatives=analysis.get('preservatives', []),
                irritants=analysis.get('irritants', []),
                allergens=analysis.get('allergens', []),
                chemicals=analysis.get('chemicals', []),
                certifications=analysis.get('certifications', []),
                fda_approval=analysis.get('fda_approval', 'Unverified'),
                healthiness_rating=analysis.get('healthiness_rating', 5),
                expiration_valid=analysis.get('expiration_valid', True),
                recommendation=analysis.get('recommendation', ''),
                health_suggestion=analysis.get('health_suggestion', ''),
                processing_time=processing_time
            )
            
            # Add personalization if user preferences provided
            if user_preferences:
                response.personalized_recommendation = analysis.get('personalized_recommendation')
                response.safety_score_for_user = analysis.get('safety_score_for_user')
                response.warnings_for_user = analysis.get('warnings_for_user', [])
                response.matches_preferences = analysis.get('matches_preferences')
            
            return response
        
        except Exception as e:
            return ProductAnalysisResponse(
                success=False,
                product_type=product_type or 'unknown',
                classification_confidence=0.0,
                ingredients_text=ingredients_text,
                error=f"Analysis error: {str(e)}",
                processing_time=time.time() - start_time
            )


if __name__ == "__main__":
    import sys
    
    # Example usage
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # Initialize analyzer
    analyzer = IngredientIntelligenceAnalyzer()
    
    # Run analysis
    result = analyzer.analyze_product_image(image_path)
    
    # Print results
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)
    print(result.model_dump_json(indent=2))
