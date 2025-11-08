"""
OCR Detection Module
Uses PaddleOCR to extract text from product images.
"""

import cv2
import numpy as np
from paddleocr import PaddleOCR
from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime
from dateutil import parser


class OCRDetector:
    """Detects and extracts text from product images using PaddleOCR."""
    
    def __init__(self, lang: str = 'en', use_gpu: bool = False, max_image_dimension: int = 1920):
        """
        Initialize OCR detector.
        
        Args:
            lang: Language code for OCR (default: 'en')
            use_gpu: Whether to use GPU acceleration
            max_image_dimension: Maximum dimension for image resize (default: 1920)
                                Set higher for better accuracy, lower for speed
                                Recommended: 1280 (fast), 1920 (balanced), 2560 (accurate)
        """
        self.max_image_dimension = max_image_dimension
        
        # Initialize PaddleOCR with compatible parameters
        # Note: Newer versions of PaddleOCR may not support all parameters
        try:
            self.ocr = PaddleOCR(
                use_angle_cls=True,
                lang=lang
            )
        except Exception as e:
            # Fallback to minimal configuration
            self.ocr = PaddleOCR(lang=lang)
    
    def _resize_image_if_needed(self, img: np.ndarray, max_dimension: int = None) -> np.ndarray:
        """
        Resize image if it's too large, maintaining aspect ratio.
        
        Args:
            img: Input image
            max_dimension: Maximum width or height (uses self.max_image_dimension if None)
            
        Returns:
            Resized image
        """
        if max_dimension is None:
            max_dimension = self.max_image_dimension
            
        height, width = img.shape[:2]
        
        # Only resize if image is larger than max_dimension
        if max(height, width) <= max_dimension:
            return img
        
        # Calculate scaling factor
        if width > height:
            scale = max_dimension / width
        else:
            scale = max_dimension / height
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize with high-quality interpolation
        resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized
    
    def extract_text_from_image(self, image_path: str) -> Dict:
        """
        Extract all text from an image.
        
        Args:
            image_path: Path to the product image
            
        Returns:
            Dictionary containing extracted text and metadata
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not read image: {image_path}")
            
            # Resize if needed for performance
            original_size = img.shape[:2]
            img = self._resize_image_if_needed(img)
            resized_size = img.shape[:2]
            
            if original_size != resized_size:
                print(f"   ℹ️  Resized image from {original_size[1]}x{original_size[0]} to {resized_size[1]}x{resized_size[0]} for faster processing")
            
            # Perform OCR (try with cls parameter, fallback without it for compatibility)
            try:
                result = self.ocr.ocr(img, cls=True)
            except TypeError:
                # Newer versions of PaddleOCR don't accept cls parameter
                result = self.ocr.ocr(img)
            
            # Extract text with confidence scores
            extracted_lines = []
            for line in result[0] if result and result[0] else []:
                box, (text, confidence) = line
                extracted_lines.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': box
                })
            
            # Combine all text
            full_text = ' '.join([line['text'] for line in extracted_lines])
            
            return {
                'full_text': full_text,
                'lines': extracted_lines,
                'success': True
            }
        
        except Exception as e:
            return {
                'full_text': '',
                'lines': [],
                'success': False,
                'error': str(e)
            }
    
    def extract_ingredients(self, text: str) -> Optional[str]:
        """
        Extract ingredients list from OCR text.
        
        Args:
            text: Full OCR extracted text
            
        Returns:
            Ingredients string or None
        """
        # Common ingredient list indicators
        patterns = [
            r'ingredients?\s*:?\s*([^.]+(?:\.[^.]*(?:oil|acid|extract|powder|flavor|color)[^.]*)*)',
            r'contains?\s*:?\s*([^.]+)',
            r'composition\s*:?\s*([^.]+)'
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if match:
                ingredients_text = match.group(1).strip()
                # Clean up
                ingredients_text = re.sub(r'\s+', ' ', ingredients_text)
                return ingredients_text
        
        # Fallback: look for comma-separated list with common ingredient terms
        if any(term in text_lower for term in ['sugar', 'water', 'oil', 'salt', 'flour', 'milk']):
            # Find sections with multiple commas (likely ingredient lists)
            sentences = text.split('.')
            for sentence in sentences:
                if sentence.count(',') >= 2:
                    return sentence.strip()
        
        return None
    
    def extract_dates(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract expiration and manufacture dates from text.
        
        Args:
            text: Full OCR extracted text
            
        Returns:
            Dictionary with expiration_date and manufacture_date
        """
        dates = {
            'expiration_date': None,
            'manufacture_date': None
        }
        
        # Patterns for date extraction
        exp_patterns = [
            r'exp(?:iry)?(?:\s+date)?[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
            r'best\s+before[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
            r'use\s+by[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
            r'bb[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})'
        ]
        
        mfg_patterns = [
            r'mfg(?:\s+date)?[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
            r'manuf(?:actured)?[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})',
            r'mfd[:\s]+([0-9]{1,2}[-/][0-9]{1,2}[-/][0-9]{2,4})'
        ]
        
        text_lower = text.lower()
        
        # Extract expiration date
        for pattern in exp_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    date_str = match.group(1)
                    parsed_date = parser.parse(date_str, fuzzy=True)
                    dates['expiration_date'] = parsed_date.strftime('%Y-%m-%d')
                    break
                except:
                    continue
        
        # Extract manufacture date
        for pattern in mfg_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    date_str = match.group(1)
                    parsed_date = parser.parse(date_str, fuzzy=True)
                    dates['manufacture_date'] = parsed_date.strftime('%Y-%m-%d')
                    break
                except:
                    continue
        
        return dates
    
    def extract_product_name(self, lines: List[Dict]) -> Optional[str]:
        """
        Extract product name (usually largest/most prominent text).
        
        Args:
            lines: List of extracted text lines with confidence
            
        Returns:
            Product name or None
        """
        if not lines:
            return None
        
        # Sort by confidence and length
        sorted_lines = sorted(
            lines,
            key=lambda x: (x['confidence'], len(x['text'])),
            reverse=True
        )
        
        # Return top confident line that's not too short
        for line in sorted_lines[:3]:
            if len(line['text']) > 3 and line['confidence'] > 0.7:
                return line['text']
        
        return None
    
    def detect(self, image_path: str) -> Dict:
        """
        Main detection method - extracts all relevant information from image.
        
        Args:
            image_path: Path to product image
            
        Returns:
            Dictionary with extracted information
        """
        # Extract all text
        ocr_result = self.extract_text_from_image(image_path)
        
        if not ocr_result['success']:
            return {
                'success': False,
                'error': ocr_result.get('error', 'OCR failed')
            }
        
        full_text = ocr_result['full_text']
        lines = ocr_result['lines']
        
        # Extract specific information
        ingredients_text = self.extract_ingredients(full_text)
        dates = self.extract_dates(full_text)
        product_name = self.extract_product_name(lines)
        
        return {
            'success': True,
            'product_name': product_name,
            'ingredients_text': ingredients_text,
            'expiration_date': dates['expiration_date'],
            'manufacture_date': dates['manufacture_date'],
            'full_text': full_text,
            'raw_lines': lines
        }


if __name__ == "__main__":
    # Test the detector
    detector = OCRDetector()
    result = detector.detect("test_image.jpg")
    print(result)
