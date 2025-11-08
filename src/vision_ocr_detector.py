"""
Vision OCR Detection Module
Uses OpenAI Vision API to extract and analyze ingredients from product images.
"""

import base64
import os
from typing import Dict, Optional
from openai import OpenAI


class VisionOCRDetector:
    """Detects and extracts text from product images using OpenAI Vision API."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize Vision OCR detector.
        
        Args:
            api_key: OpenAI API key (defaults to env var OPENAI_API_KEY)
            model: OpenAI model to use (gpt-4o-mini or gpt-4o)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
    
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64 string.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """
        Extract ingredients text from image using OpenAI Vision API.
        
        Args:
            image_path: Path to the product image
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            print(f"   🔍 Using OpenAI Vision API to read ingredients...")
            
            # Encode image
            base64_image = self._encode_image(image_path)
            
            # Create vision prompt
            prompt = """Analyze this product label image and extract the ingredients list.

Instructions:
1. Locate the ingredients section on the label
2. Extract ALL ingredients exactly as written
3. If you see multiple languages, extract the English version
4. Return just the ingredients text, nothing else
5. If no ingredients are visible, return "NO_INGREDIENTS_FOUND"

Example output format:
Water, Sugar, Citric Acid, Natural Flavors, Preservative (E202)"""

            # Call OpenAI Vision API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            # Extract response
            ingredients_text = response.choices[0].message.content.strip()
            
            if ingredients_text == "NO_INGREDIENTS_FOUND" or not ingredients_text:
                print(f"   ⚠️  No ingredients detected by Vision API")
                return {
                    'full_text': '',
                    'lines': [],
                    'success': False,
                    'error': 'No ingredients found in image'
                }
            
            print(f"   ✅ Extracted ingredients using Vision API")
            print(f"   📝 Preview: {ingredients_text[:100]}...")
            
            # Format response to match OCR detector interface
            return {
                'full_text': ingredients_text,
                'lines': [{'text': ingredients_text, 'confidence': 1.0}],
                'success': True
            }
            
        except FileNotFoundError:
            return {
                'full_text': '',
                'lines': [],
                'success': False,
                'error': f'Image file not found: {image_path}'
            }
        except Exception as e:
            error_msg = str(e)
            
            # Check for quota errors
            if 'insufficient_quota' in error_msg or '429' in error_msg:
                print(f"\n   ⚠️  OpenAI API quota exceeded!")
                print(f"   💡 Solutions:")
                print(f"      1. Add credits at: https://platform.openai.com/account/billing")
                print(f"      2. Use PaddleOCR instead: ocr_method='paddleocr'")
                print(f"      3. Use a different API key")
                return {
                    'full_text': '',
                    'lines': [],
                    'success': False,
                    'error': 'OpenAI API quota exceeded. Please add credits or use PaddleOCR.'
                }
            
            return {
                'full_text': '',
                'lines': [],
                'success': False,
                'error': f'Vision API error: {error_msg}'
            }
    
    def extract_ingredients(self, text: str) -> str:
        """
        Extract ingredients from text (compatibility method).
        Since Vision API already extracts just ingredients, return as-is.
        
        Args:
            text: Full text containing ingredients
            
        Returns:
            Ingredients text
        """
        return text
    
    def detect(self, image_path: str) -> Dict:
        """
        Main detection method - extracts ingredients from image.
        This method provides compatibility with OCRDetector interface.
        
        Args:
            image_path: Path to product image
            
        Returns:
            Dictionary with extracted information
        """
        # Extract text using Vision API
        ocr_result = self.extract_text_from_image(image_path)
        
        if not ocr_result['success']:
            return {
                'success': False,
                'error': ocr_result.get('error', 'Vision API failed')
            }
        
        ingredients_text = ocr_result['full_text']
        
        # Return in same format as OCRDetector
        return {
            'success': True,
            'product_name': None,  # Vision API focuses on ingredients only
            'ingredients_text': ingredients_text,
            'expiration_date': None,  # Not extracted by Vision API
            'manufacture_date': None,  # Not extracted by Vision API
            'full_text': ingredients_text,
            'raw_lines': ocr_result['lines']
        }
