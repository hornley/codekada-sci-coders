#!/usr/bin/env python3
"""
Test OpenAI Vision API for ingredient extraction.
"""

import sys
from src.vision_ocr_detector import VisionOCRDetector

def test_vision_ocr(image_path: str):
    """Test Vision OCR on an image."""
    print("\n" + "="*70)
    print("🔍 Testing OpenAI Vision API for Ingredient Extraction")
    print("="*70)
    
    try:
        # Initialize Vision OCR
        detector = VisionOCRDetector(model="gpt-4o-mini")
        
        # Extract ingredients
        result = detector.extract_text_from_image(image_path)
        
        print(f"\n{'='*70}")
        print("📊 RESULTS")
        print("="*70)
        print(f"\n✅ Success: {result['success']}")
        
        if result['success']:
            print(f"\n📝 Extracted Ingredients:")
            print(f"{'-'*70}")
            print(result['full_text'])
            print(f"{'-'*70}")
            
            print(f"\n💡 This text will be sent to OpenAI for analysis:")
            print(f"   - Harmful ingredients")
            print(f"   - Allergens")
            print(f"   - Health rating")
            print(f"   - Recommendations")
        else:
            print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_vision.py <image_path>")
        print("Example: python3 test_vision.py images/combi2.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    test_vision_ocr(image_path)
    print()
