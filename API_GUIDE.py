"""
API Usage Guide - Ingredient Intelligence Analyzer
Complete reference for developers
"""

# ========================================
# QUICK REFERENCE
# ========================================

# 1. Basic Image Analysis
from src import IngredientIntelligenceAnalyzer

analyzer = IngredientIntelligenceAnalyzer()
result = analyzer.analyze_product_image("product.jpg")

# 2. Text Analysis
result = analyzer.analyze_from_text(
    ingredients_text="Water, Sugar, Preservatives",
    product_type="food",
    expiration_date="2026-12-31"
)

# 3. Access Results
print(f"Product: {result.product_type}")
print(f"Health Rating: {result.healthiness_rating}/10")
print(f"Harmful: {result.harmful_ingredients}")
print(f"Allergens: {result.allergens}")

# ========================================
# DETAILED API REFERENCE
# ========================================

# ----------------------------------------
# 1. IngredientIntelligenceAnalyzer
# ----------------------------------------
"""
Main class for complete analysis pipeline

Constructor:
    IngredientIntelligenceAnalyzer(
        openai_api_key: str = None,  # Defaults to env var
        ocr_lang: str = 'en',
        use_gpu: bool = False
    )

Methods:
    analyze_product_image(image_path: str) -> ProductAnalysisResponse
        - Full pipeline: OCR -> Classification -> Analysis
        
    analyze_from_text(
        ingredients_text: str,
        product_type: str = None,
        expiration_date: str = None
    ) -> ProductAnalysisResponse
        - Skip OCR, analyze ingredients directly
"""

# Example: Custom initialization
analyzer = IngredientIntelligenceAnalyzer(
    openai_api_key="sk-...",
    ocr_lang="es",  # Spanish
    use_gpu=True
)


# ----------------------------------------
# 2. OCRDetector
# ----------------------------------------
"""
PaddleOCR text extraction

Constructor:
    OCRDetector(lang: str = 'en', use_gpu: bool = False)

Methods:
    detect(image_path: str) -> Dict
        Returns: {
            'success': bool,
            'product_name': str,
            'ingredients_text': str,
            'expiration_date': str,  # YYYY-MM-DD
            'manufacture_date': str,
            'full_text': str
        }
"""

from src.ocr_detector import OCRDetector

ocr = OCRDetector(lang='en')
result = ocr.detect("product.jpg")

if result['success']:
    print(f"Ingredients: {result['ingredients_text']}")


# ----------------------------------------
# 3. ProductClassifier
# ----------------------------------------
"""
Product type classification

Methods:
    classify(
        full_text: str,
        ingredients_text: str = None,
        product_name: str = None
    ) -> Dict
        Returns: {
            'product_type': str,  # food/drink/beauty/unknown
            'confidence': float,  # 0.0 to 1.0
            'scores': dict
        }
"""

from src.classifier import ProductClassifier

classifier = ProductClassifier()
result = classifier.classify("Water, Sugar, Flavoring")

print(f"Type: {result['product_type']}")
print(f"Confidence: {result['confidence']}")


# ----------------------------------------
# 4. IngredientAnalyzer
# ----------------------------------------
"""
AI-powered ingredient analysis

Constructor:
    IngredientAnalyzer(api_key: str = None, model: str = "gpt-4o-mini")

Methods:
    analyze(
        product_type: str,
        ingredients_text: str,
        expiration_date: str = None,
        manufacture_date: str = None
    ) -> Dict
        Returns comprehensive analysis with:
        - harmful_ingredients
        - additives, preservatives
        - allergens, chemicals
        - certifications
        - healthiness_rating (1-10)
        - recommendations
"""

from src.ingredient_analyzer import IngredientAnalyzer

analyzer = IngredientAnalyzer(model="gpt-4o-mini")
result = analyzer.analyze(
    product_type="drink",
    ingredients_text="Water, Sugar, Citric Acid"
)

print(f"Rating: {result['healthiness_rating']}/10")


# ========================================
# RESPONSE MODEL STRUCTURE
# ========================================

"""
ProductAnalysisResponse (Pydantic Model)

Fields:
    # Status
    success: bool
    error: Optional[str]
    
    # Product Info
    product_type: str
    product_name: Optional[str]
    classification_confidence: float
    
    # OCR Data
    ingredients_text: Optional[str]
    expiration_date: Optional[str]  # YYYY-MM-DD
    manufacture_date: Optional[str]
    
    # Analysis Results
    harmful_ingredients: List[str]
    additives: List[str]
    preservatives: List[str]
    irritants: List[str]
    allergens: List[str]
    chemicals: List[str]
    certifications: List[str]
    
    # Health Metrics
    fda_approval: str  # "Likely" / "Unverified" / "Not Found"
    healthiness_rating: int  # 1-10
    expiration_valid: bool
    
    # Recommendations
    recommendation: str
    health_suggestion: str
    
    # Metadata
    processing_time: Optional[float]
"""

# Access fields
result = analyzer.analyze_product_image("product.jpg")

print(f"Success: {result.success}")
print(f"Product: {result.product_name}")
print(f"Type: {result.product_type}")
print(f"Rating: {result.healthiness_rating}/10")
print(f"Expired: {not result.expiration_valid}")

# Convert to dict/JSON
data = result.model_dump()  # Dict
json_str = result.model_dump_json(indent=2)  # JSON string


# ========================================
# UTILITY FUNCTIONS
# ========================================

from src.utils import (
    pretty_print_results,
    save_results_to_json,
    validate_image_path,
    get_health_rating_description
)

# Pretty print to console
pretty_print_results(result.model_dump())

# Save to JSON file
save_results_to_json(result.model_dump(), "output/result.json")

# Validate image
if validate_image_path("product.jpg"):
    print("Valid image")

# Get rating description
desc = get_health_rating_description(7)  # "Good - Generally healthy"


# ========================================
# ADVANCED USAGE EXAMPLES
# ========================================

# ----------------------------------------
# Example 1: Batch Processing
# ----------------------------------------
products = [
    {"path": "product1.jpg"},
    {"path": "product2.jpg"},
    {"path": "product3.jpg"}
]

analyzer = IngredientIntelligenceAnalyzer()
results = []

for product in products:
    result = analyzer.analyze_product_image(product["path"])
    results.append({
        'name': result.product_name,
        'rating': result.healthiness_rating,
        'harmful': len(result.harmful_ingredients)
    })

# Find unhealthy products
unhealthy = [r for r in results if r['rating'] < 5]


# ----------------------------------------
# Example 2: Custom Analysis Pipeline
# ----------------------------------------
from src.ocr_detector import OCRDetector
from src.classifier import ProductClassifier
from src.ingredient_analyzer import IngredientAnalyzer

# Step 1: OCR
ocr = OCRDetector()
ocr_result = ocr.detect("product.jpg")

# Step 2: Classification
classifier = ProductClassifier()
classification = classifier.classify(
    ocr_result['full_text'],
    ocr_result['ingredients_text']
)

# Step 3: Analysis (only if confidence > threshold)
if classification['confidence'] > 0.7:
    analyzer = IngredientAnalyzer()
    analysis = analyzer.analyze(
        product_type=classification['product_type'],
        ingredients_text=ocr_result['ingredients_text']
    )


# ----------------------------------------
# Example 3: Error Handling
# ----------------------------------------
try:
    result = analyzer.analyze_product_image("product.jpg")
    
    if not result.success:
        print(f"Analysis failed: {result.error}")
    elif result.healthiness_rating < 4:
        print("⚠️ Unhealthy product detected!")
        print(f"Harmful: {result.harmful_ingredients}")
    else:
        print("✓ Product seems safe")
        
except FileNotFoundError:
    print("Image not found")
except Exception as e:
    print(f"Error: {e}")


# ----------------------------------------
# Example 4: Filter by Allergens
# ----------------------------------------
result = analyzer.analyze_from_text(
    ingredients_text="Wheat, Milk, Eggs, Soy, Peanuts",
    product_type="food"
)

# Check for specific allergen
if "peanuts" in [a.lower() for a in result.allergens]:
    print("⚠️ Contains peanuts!")

# Get all allergens
all_allergens = result.allergens
print(f"Allergens: {', '.join(all_allergens)}")


# ----------------------------------------
# Example 5: Integration with Web API
# ----------------------------------------
from flask import Flask, request, jsonify
from src import IngredientIntelligenceAnalyzer

app = Flask(__name__)
analyzer = IngredientIntelligenceAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    result = analyzer.analyze_from_text(
        ingredients_text=data['ingredients'],
        product_type=data.get('type')
    )
    
    return jsonify(result.model_dump())

# Run: flask run


# ========================================
# CONFIGURATION
# ========================================

# Environment Variables (.env)
"""
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OCR_LANG=en
OCR_GPU=false
MIN_CONFIDENCE_SCORE=0.6
"""

# Runtime Configuration
import os
os.environ['OPENAI_MODEL'] = 'gpt-4o'  # Use better model

# Custom Model Selection
analyzer = IngredientIntelligenceAnalyzer()
analyzer.analyzer.model = 'gpt-4o'  # Override model


# ========================================
# PERFORMANCE TIPS
# ========================================

# Tip 1: Reuse analyzer instance (faster)
analyzer = IngredientIntelligenceAnalyzer()
for product in products:
    result = analyzer.analyze_from_text(product)

# Tip 2: Skip OCR when you have text
result = analyzer.analyze_from_text(ingredients)  # Faster

# Tip 3: Use gpt-4o-mini for cost efficiency
analyzer = IngredientIntelligenceAnalyzer()
analyzer.analyzer.model = 'gpt-4o-mini'  # Cheaper

# Tip 4: Process images in parallel
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(
        analyzer.analyze_product_image,
        image_paths
    ))


# ========================================
# ERROR CODES & TROUBLESHOOTING
# ========================================

"""
Common Errors:

1. "OCR failed: Could not read image"
   - Check image path exists
   - Verify image format (jpg, png)
   - Ensure image is readable

2. "Analysis failed: API key not found"
   - Set OPENAI_API_KEY in .env
   - Or pass api_key to constructor

3. "No ingredients found"
   - Image quality too low
   - Ingredients not visible in image
   - Try better lighting/resolution

4. Product type: "unknown"
   - Not enough context in text
   - Provide product_type manually
   - Check if ingredients were extracted

5. Low confidence score
   - Mixed product indicators
   - Unusual ingredient combinations
   - May need manual verification
"""

# ========================================
# TESTING
# ========================================

# Run installation test
# $ python test_installation.py

# Run examples
# $ python example.py

# Custom test
from src import IngredientIntelligenceAnalyzer

def test_basic():
    analyzer = IngredientIntelligenceAnalyzer()
    result = analyzer.analyze_from_text(
        ingredients_text="Water, Sugar",
        product_type="drink"
    )
    assert result.success
    assert result.product_type == "drink"
    assert result.healthiness_rating >= 1
    print("✓ Basic test passed")

test_basic()
