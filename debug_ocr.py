#!/usr/bin/env python3
"""Debug script to see raw OCR output"""

import sys
from src.ocr_detector import OCRDetector

if len(sys.argv) < 2:
    print("Usage: python3 debug_ocr.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

print(f"Analyzing: {image_path}\n")

# Create OCR detector
ocr = OCRDetector(max_image_dimension=1280)

# Extract text
result = ocr.extract_text_from_image(image_path)

print("="*80)
print("OCR RESULTS")
print("="*80)
print(f"Success: {result['success']}")
print(f"Number of text lines found: {len(result.get('lines', []))}")
print()

if result.get('lines'):
    print("Text detected:")
    print("-"*80)
    for i, line in enumerate(result['lines'], 1):
        print(f"{i}. {line['text']} (confidence: {line['confidence']:.2f})")
    print()
    print("Combined text:")
    print("-"*80)
    print(result.get('full_text', 'None'))
else:
    print("❌ No text detected!")
    print("\nPossible reasons:")
    print("  - Image quality too poor")
    print("  - Text too small after resizing")
    print("  - Wrong language (currently set to English)")
    print("  - Image orientation issue")
    
print()
