# 🧪 Ingredient Intelligence Analyzer

**AI-Powered Product Safety & Health Analysis System**

An intelligent system that detects and analyzes ingredients from consumer product images (food, drinks, and beauty products) to identify harmful ingredients, additives, allergens, certifications, and overall health impact using OCR and OpenAI.

---

## 🌟 Features

### 1️⃣ **Intelligent OCR Detection**
**Two OCR Methods Available:**

**🌟 OpenAI Vision API (Recommended - Default)**
- Highly accurate ingredient text extraction
- Handles rotated, blurry, or low-quality images
- No preprocessing needed
- Works with multiple languages
- Fast and reliable

**🔧 PaddleOCR (Alternative - Local)**
- Extract text from cropped ingredient labels
- Automatic preprocessing (denoising, contrast enhancement)
- Runs locally (no internet required)
- Free but may struggle with some images

### 2️⃣ **Product Classification**
- Automatic classification (Food / Drink / Beauty)
- Keyword-based and ingredient-based analysis
- Confidence scoring

### 3️⃣ **AI-Powered Analysis** (OpenAI)
- Identify harmful ingredients and health risks
- Detect additives, preservatives, and chemicals
- Find allergens (FDA top 9, EU top 14)
- Identify irritants in beauty products
- Determine certifications (Halal, Vegan, Gluten-Free, etc.)
- FDA approval status verification
- Health rating (1-10 scale)
- Personalized health recommendations

### 4️⃣ **Personalized Health Analysis** (Phase 2) ⭐ NEW
- Define your health profile (allergies, dietary restrictions, health goals)
- Get personalized product safety scores
- Receive warnings specific to your health needs
- Check if products match your dietary preferences
- Tailored recommendations based on your health goals

### 5️⃣ **Intake Tracking & Reports** (Phase 3) ⭐ NEW
- Track consumed products over time with SQLite database
- Log products with automatic health metrics calculation
- View daily summaries and weekly health reports
- Check consumption history for specific products
- Monitor allergen exposures and preference violations
- Save and load user health preferences

---

## 📋 Output Example

```json
{
  "success": true,
  "product_type": "drink",
  "product_name": "Orange Soda",
  "classification_confidence": 0.92,
  "ingredients_text": "Carbonated water, Sugar, Citric acid, Natural flavors, Yellow 5",
  "expiration_date": "2026-03-12",
  "harmful_ingredients": ["Yellow 5"],
  "additives": ["Yellow 5", "Natural flavors"],
  "preservatives": ["Citric acid"],
  "allergens": [],
  "certifications": ["Vegetarian"],
  "fda_approval": "Likely",
  "healthiness_rating": 4,
  "expiration_valid": true,
  "recommendation": "High sugar content. Consume in moderation.",
  "health_suggestion": "Consider natural fruit juices as healthier alternatives."
}
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Step 1: Clone the Repository
```bash
git clone https://github.com/hornley/codekada-sci-coders.git
cd codekada
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

**Note:** PaddleOCR dependencies are now optional. The system uses OpenAI Vision API by default, which is faster and more accurate.

If you need offline OCR with PaddleOCR, install additional dependencies:
```bash
pip install paddleocr paddlepaddle opencv-python
```

---

## 💻 Usage

### Quick Start

```python
from src import IngredientIntelligenceAnalyzer

# Method 1: Using OpenAI Vision API (Recommended - Default)
analyzer = IngredientIntelligenceAnalyzer(ocr_method='vision')

# Method 2: Using PaddleOCR (Local, Free)
# analyzer = IngredientIntelligenceAnalyzer(ocr_method='paddleocr', max_image_dimension=1920)

# Analyze product image
result = analyzer.analyze_product_image("product_label.jpg")

print(f"Health Rating: {result.healthiness_rating}/10")
print(f"Harmful: {result.harmful_ingredients}")
print(f"Allergens: {result.allergens}")
```

### Personalized Health Analysis ⭐ NEW

```python
from src import IngredientIntelligenceAnalyzer
from src.models import UserHealthPreferences

# Define your health profile
user_preferences = UserHealthPreferences(
    allergies=["peanuts", "shellfish", "soy"],
    dietary_restrictions=["vegan", "gluten-free"],
    avoid_ingredients=["artificial colors", "high fructose corn syrup"],
    health_goals=["weight loss", "reduce sugar intake"]
)

# Analyze with personalization
analyzer = IngredientIntelligenceAnalyzer()
result = analyzer.analyze_product_image(
    "product.jpg",
    user_preferences=user_preferences
)

# Get personalized results
print(f"Safety for you: {result.safety_score_for_user}/10")
print(f"Matches preferences: {result.matches_preferences}")
print(f"Personalized advice: {result.personalized_recommendation}")
print(f"Your warnings: {result.warnings_for_user}")
```

### OCR Method Comparison

| Feature | Vision API (Default) | PaddleOCR |
|---------|---------------------|-----------|
| **Accuracy** | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐ Good |
| **Speed** | ⚡ Fast (2-5 sec) | 🐌 Slow (30-120 sec) |
| **Cost** | 💰 ~$0.01-0.02/image | 🆓 Free |
| **Internet** | ☁️ Required | 📴 Offline |
| **Setup** | ✅ Easy | 🔧 Complex |
| **Handles blur/rotation** | ✅ Yes | ❌ Struggles |

**💡 Recommendation:** Use Vision API (default) unless you need offline processing.

### Command Line

```bash
# Standard analysis (uses Vision API by default)
python example.py path/to/product.jpg

# Personalized analysis with health preferences (Phase 2)
python example_with_preferences.py path/to/product.jpg

# Set your health preferences (Phase 3)
python set_preferences.py

# Track product intake and log to database (Phase 3)
python track_intake.py path/to/product.jpg

# View intake reports (Phase 3)
python view_intake.py today      # Today's summary
python view_intake.py week       # Weekly report
python view_intake.py history    # Full history

# Results are automatically saved to results/ folder as JSON

# From text
python example.py --text "Water, Sugar, Salt" --type food

# Run demo examples
python example.py
```

### Intake Tracking Workflow (Phase 3) ⭐ NEW

```bash
# 1. Set your health preferences (one-time setup)
python set_preferences.py

# 2. Track products you consume
python track_intake.py images/breakfast.jpg
python track_intake.py images/lunch.jpg
python track_intake.py images/snack.jpg

# 3. View your health reports
python view_intake.py today     # See what you ate today
python view_intake.py week      # Get weekly health insights
python view_intake.py history   # Review consumption history

# 4. Check consumption history for a product
# (automatically shown when tracking a previously consumed product)
```

### JSON Output

All analysis results are automatically saved as JSON files:

```bash
# Analyze and save JSON
python example.py images/product.jpg

# JSON saved to: results/product_20251108_143052.json
```

**JSON Structure:**
```json
{
  "success": true,
  "product_type": "food",
  "product_name": "Cookies",
  "ingredients_text": "Wheat Flour, Sugar, Palm Oil...",
  "harmful_ingredients": ["Palm Oil", "E129"],
  "allergens": ["wheat", "milk"],
  "healthiness_rating": 4,
  "recommendation": "Contains artificial colors...",
  "processing_time": 3.45
}
```

---

## 📁 Project Structure

```
codekada/
├── src/
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # Main orchestration pipeline
│   ├── vision_ocr_detector.py      # OpenAI Vision API (default)
│   ├── classifier.py               # Product type classification
│   ├── ingredient_analyzer.py      # OpenAI-powered analysis
│   ├── models.py                   # Pydantic data models
│   ├── utils.py                    # Utility functions
│   └── intake_tracker.py           # ⭐ NEW: SQLite intake tracking (Phase 3)
├── legacy_paddleocr/               # Optional PaddleOCR files
│   └── ocr_detector.py             # PaddleOCR implementation
├── results/                        # JSON output files (auto-created)
├── example.py                      # Basic usage examples
├── example_with_preferences.py     # ⭐ NEW: Personalized analysis (Phase 2)
├── track_intake.py                 # ⭐ NEW: Track product consumption (Phase 3)
├── view_intake.py                  # ⭐ NEW: View intake reports (Phase 3)
├── set_preferences.py              # ⭐ NEW: Set health preferences (Phase 3)
├── analyze_with_json.py            # JSON output demo
├── test_vision.py                  # Test Vision API
├── requirements.txt                # Core dependencies
├── .env.example                    # Environment template
├── intake_history.db               # ⭐ NEW: SQLite database (auto-created)
└── README.md                       # This file
```

---

## 🔧 API Reference

### `IngredientIntelligenceAnalyzer`

```python
analyzer = IngredientIntelligenceAnalyzer(
    openai_api_key: str = None,      # Defaults to env var
    ocr_lang: str = 'en',
    use_gpu: bool = False,
    max_image_dimension: int = 1920  # 1280=fast, 1920=balanced, 2560=accurate
)
```

**Methods:**

- `analyze_product_image(image_path: str)` - Complete analysis from image
- `analyze_from_text(ingredients_text: str, product_type: str = None)` - Analysis from text

**Response Fields:**
- `success`, `product_type`, `product_name`
- `harmful_ingredients`, `additives`, `preservatives`, `allergens`
- `healthiness_rating` (1-10), `expiration_valid`
- `recommendation`, `health_suggestion`

---

## 🧪 Examples

### Analyze Product Image
```python
from src import IngredientIntelligenceAnalyzer

analyzer = IngredientIntelligenceAnalyzer()
result = analyzer.analyze_product_image("product.jpg")
print(f"Rating: {result.healthiness_rating}/10")
```

### Analyze from Text
```python
result = analyzer.analyze_from_text(
    ingredients_text="Water, Glycerin, Methylparaben",
    product_type="beauty"
)
print(f"Irritants: {result.irritants}")
```

### Personalized Analysis (Phase 2)
```python
from src.models import UserHealthPreferences

preferences = UserHealthPreferences(
    allergies=["peanuts", "milk"],
    dietary_restrictions=["vegan"],
    health_goals=["weight loss"]
)

result = analyzer.analyze_product_image("product.jpg", user_preferences=preferences)
print(f"Safety for you: {result.safety_score_for_user}/10")
print(f"Warnings: {result.warnings_for_user}")
```

### Track Intake (Phase 3) ⭐ NEW
```python
from src.intake_tracker import IntakeTracker

tracker = IntakeTracker()

# Log a consumed product
result = analyzer.analyze_product_image("breakfast.jpg")
entry_id = tracker.log_intake(result)

# Get daily summary
summary = tracker.get_daily_summary()
print(f"Today: {summary['metrics']['total_products']} products")
print(f"Avg health rating: {summary['metrics']['avg_health_rating']}/10")

# Get weekly report
report = tracker.get_weekly_report()
print(f"Week: {report['total_products']} products")
print(f"Avg rating: {report['avg_health_rating']}/10")

# Check if product consumed before
history = tracker.check_product_against_history("Coca Cola")
if history:
    print(f"Last consumed: {history['last_consumed']}")
```

### Batch Processing
```python
for product in products:
    result = analyzer.analyze_from_text(product['ingredients'])
    print(f"Rating: {result.healthiness_rating}/10")
```

---

## 🎯 System Workflow

```
Cropped Ingredient Image → Preprocessing → OCR Detection → Classification → AI Analysis → JSON Output
```

1. **Preprocessing**: Grayscale conversion, denoising, adaptive thresholding for better contrast
2. **OCR**: Extract text and ingredients using PaddleOCR
3. **Classification**: Identify product type (food/drink/beauty)
4. **AI Analysis**: OpenAI analyzes ingredients for health impact
5. **Output**: Structured JSON with complete analysis

**📸 Image Requirements:**
- Crop to show only the ingredients label area
- Recommended size: 800-2000px wide
- Supported formats: JPG, PNG
- Clear, well-lit photos work best

---

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | (required) |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `OCR_LANG` | OCR language | `en` |
| `OCR_GPU` | Use GPU for OCR | `false` |

---

## 📦 Dependencies

**Core (Required):**
- **OpenAI** - Vision API for OCR + AI-powered analysis
- **Pydantic** - Data validation
- **Pillow** - Image handling
- **python-dotenv** - Environment management
- **python-dateutil** - Date parsing

**Optional (for offline OCR):**
- **PaddleOCR** - Local OCR text extraction
- **PaddlePaddle** - Deep learning framework
- **OpenCV** - Image processing

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Powered by [OpenAI Vision API](https://openai.com)
- Optional support for [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- Created for SCI Coders by hornley

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Made with ❤️ for healthier consumer choices**