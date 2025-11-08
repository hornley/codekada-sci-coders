# 🧪 Ingredient Intelligence Analyzer

**AI-Powered Product Safety & Health Analysis System**

An intelligent system that detects and analyzes ingredients from consumer product images (food, drinks, and beauty products) to identify harmful ingredients, additives, allergens, certifications, and overall health impact using OCR and OpenAI.

---

## 🌟 Features

### 1️⃣ **OCR Detection** (PaddleOCR)
- Extract text from product images
- Detect ingredients lists automatically
- Extract expiration and manufacture dates
- Identify product names and brands

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
OCR_LANG=en
OCR_GPU=false
```

---

## 💻 Usage

### Quick Start

```python
from src import IngredientIntelligenceAnalyzer

# Initialize analyzer
analyzer = IngredientIntelligenceAnalyzer()

# For faster processing with large images (e.g., 4032x3028)
# analyzer = IngredientIntelligenceAnalyzer(max_image_dimension=1280)

# Analyze product image
result = analyzer.analyze_product_image("product.jpg")

print(f"Health Rating: {result.healthiness_rating}/10")
print(f"Harmful: {result.harmful_ingredients}")
print(f"Allergens: {result.allergens}")
```

### Command Line

```bash
# From image
python example.py path/to/product.jpg

# From text
python example.py --text "Water, Sugar, Salt" --type food

# Run demo examples
python example.py
```

---

## 📁 Project Structure

```
codekada/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main orchestration pipeline
│   ├── ocr_detector.py          # PaddleOCR text extraction
│   ├── classifier.py            # Product type classification
│   ├── ingredient_analyzer.py   # OpenAI-powered analysis
│   ├── models.py                # Pydantic data models
│   └── utils.py                 # Utility functions
├── example.py                   # Usage examples
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
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

### Batch Processing
```python
for product in products:
    result = analyzer.analyze_from_text(product['ingredients'])
    print(f"Rating: {result.healthiness_rating}/10")
```

---

## 🎯 System Workflow

```
Product Image → OCR Detection → Classification → AI Analysis → JSON Output
```

1. **OCR**: Extract text, ingredients, dates using PaddleOCR
2. **Classification**: Identify product type (food/drink/beauty)
3. **AI Analysis**: OpenAI analyzes ingredients for health impact
4. **Output**: Structured JSON with complete analysis

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

- **PaddleOCR** - OCR text extraction
- **OpenAI** - AI-powered ingredient analysis
- **Pydantic** - Data validation
- **OpenCV** - Image processing
- **python-dotenv** - Environment management
- **python-dateutil** - Date parsing

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Built with [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- Powered by [OpenAI GPT](https://openai.com)
- Created for SCI Coders by hornley

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

---

**Made with ❤️ for healthier consumer choices**