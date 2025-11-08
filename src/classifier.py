"""
Product Type Classifier
Classifies products as food, drink, or beauty based on OCR text and keywords.
"""

from typing import Dict, List, Optional
import re


class ProductClassifier:
    """Classifies product type from extracted text."""
    
    # Keyword categories for classification
    FOOD_KEYWORDS = [
        'flour', 'sugar', 'salt', 'bread', 'cookie', 'biscuit', 'cake',
        'pasta', 'rice', 'cereal', 'cheese', 'meat', 'chicken', 'beef',
        'pork', 'fish', 'sauce', 'snack', 'chips', 'chocolate', 'candy',
        'protein', 'calories', 'serving size', 'nutrition facts',
        'allergen', 'wheat', 'soy', 'milk', 'nuts', 'eggs'
    ]
    
    DRINK_KEYWORDS = [
        'juice', 'soda', 'water', 'beverage', 'drink', 'cola', 'tea',
        'coffee', 'energy drink', 'sports drink', 'milk', 'smoothie',
        'carbonated', 'ml', 'liter', 'litre', 'fl oz', 'ounce',
        'concentrate', 'caffeine', 'vitamin water'
    ]
    
    BEAUTY_KEYWORDS = [
        'lotion', 'cream', 'serum', 'shampoo', 'conditioner', 'soap',
        'cleanser', 'moisturizer', 'sunscreen', 'spf', 'makeup',
        'foundation', 'lipstick', 'mascara', 'perfume', 'fragrance',
        'deodorant', 'antiperspirant', 'body wash', 'face wash',
        'toner', 'essence', 'mask', 'scrub', 'exfoliant', 'oil-free',
        'hypoallergenic', 'dermatologist', 'cosmetic', 'beauty',
        'skin care', 'hair care', 'paraben', 'sulfate'
    ]
    
    def __init__(self):
        """Initialize the classifier."""
        pass
    
    def _count_keywords(self, text: str, keywords: List[str]) -> int:
        """
        Count how many keywords from a list appear in the text.
        
        Args:
            text: Text to search
            keywords: List of keywords to count
            
        Returns:
            Number of keyword matches
        """
        text_lower = text.lower()
        count = 0
        
        for keyword in keywords:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, text_lower):
                count += 1
        
        return count
    
    def classify_by_keywords(self, text: str) -> Dict:
        """
        Classify product type based on keyword matching.
        
        Args:
            text: OCR extracted text
            
        Returns:
            Dictionary with product_type and confidence scores
        """
        # Count matches for each category
        food_score = self._count_keywords(text, self.FOOD_KEYWORDS)
        drink_score = self._count_keywords(text, self.DRINK_KEYWORDS)
        beauty_score = self._count_keywords(text, self.BEAUTY_KEYWORDS)
        
        # Determine product type
        scores = {
            'food': food_score,
            'drink': drink_score,
            'beauty': beauty_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return {
                'product_type': 'unknown',
                'confidence': 0.0,
                'scores': scores
            }
        
        # Get type with highest score
        product_type = max(scores, key=scores.get)
        
        # Calculate confidence (normalized)
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0
        
        return {
            'product_type': product_type,
            'confidence': round(confidence, 2),
            'scores': scores
        }
    
    def classify_by_ingredients(self, ingredients_text: Optional[str]) -> Optional[str]:
        """
        Classify based on ingredients list characteristics.
        
        Args:
            ingredients_text: Extracted ingredients string
            
        Returns:
            Product type or None
        """
        if not ingredients_text:
            return None
        
        ingredients_lower = ingredients_text.lower()
        
        # Beauty products often have specific chemical ingredients
        beauty_indicators = [
            'paraben', 'sulfate', 'glycerin', 'dimethicone', 'tocopherol',
            'retinol', 'hyaluronic', 'salicylic', 'benzoyl', 'cetyl',
            'stearyl', 'phenoxyethanol'
        ]
        
        # Food/drink indicators
        food_indicators = [
            'sugar', 'salt', 'flour', 'starch', 'glucose', 'fructose',
            'dextrose', 'lactose', 'maltose'
        ]
        
        drink_indicators = [
            'carbonated water', 'concentrate', 'citric acid', 'ascorbic acid',
            'natural flavor', 'artificial flavor'
        ]
        
        beauty_count = sum(1 for ind in beauty_indicators if ind in ingredients_lower)
        food_count = sum(1 for ind in food_indicators if ind in ingredients_lower)
        drink_count = sum(1 for ind in drink_indicators if ind in ingredients_lower)
        
        if beauty_count >= 2:
            return 'beauty'
        elif drink_count >= 2:
            return 'drink'
        elif food_count >= 2:
            return 'food'
        
        return None
    
    def classify(
        self,
        full_text: str,
        ingredients_text: Optional[str] = None,
        product_name: Optional[str] = None
    ) -> Dict:
        """
        Main classification method combining multiple strategies.
        
        Args:
            full_text: Full OCR extracted text
            ingredients_text: Extracted ingredients (if available)
            product_name: Extracted product name (if available)
            
        Returns:
            Classification result with product type and confidence
        """
        # Primary: keyword-based classification
        keyword_result = self.classify_by_keywords(full_text)
        
        # Secondary: ingredient-based classification
        ingredient_type = None
        if ingredients_text:
            ingredient_type = self.classify_by_ingredients(ingredients_text)
        
        # If both methods agree, increase confidence
        if ingredient_type and ingredient_type == keyword_result['product_type']:
            keyword_result['confidence'] = min(1.0, keyword_result['confidence'] + 0.2)
        
        # Override if ingredient analysis is strong and disagrees
        elif ingredient_type and keyword_result['confidence'] < 0.5:
            keyword_result['product_type'] = ingredient_type
            keyword_result['confidence'] = 0.7
        
        return {
            'product_type': keyword_result['product_type'],
            'confidence': round(keyword_result['confidence'], 2),
            'scores': keyword_result['scores'],
            'method': 'keyword_matching'
        }


if __name__ == "__main__":
    # Test the classifier
    classifier = ProductClassifier()
    
    test_text = "Ingredients: Water, Sugar, Citric Acid, Natural Flavor, Preservatives"
    result = classifier.classify(test_text, ingredients_text=test_text)
    print(result)
