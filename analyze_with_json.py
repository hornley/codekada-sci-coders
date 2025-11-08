#!/usr/bin/env python3
"""
Quick demo showing JSON output feature.
"""

import sys
import os
from datetime import datetime
from src import IngredientIntelligenceAnalyzer
from src.utils import pretty_print_results, save_results_to_json

def analyze_and_save_json(image_path: str):
    """Analyze product and save results as JSON."""
    
    print("\n" + "="*70)
    print("🧪 AI Ingredient Intelligence Analyzer - JSON Output Demo")
    print("="*70)
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found: {image_path}")
        return
    
    # Initialize analyzer with Vision API
    print("\n📸 Analyzing product image...")
    analyzer = IngredientIntelligenceAnalyzer(ocr_method='vision')
    
    # Analyze
    result = analyzer.analyze_product_image(image_path)
    
    # Display results
    print("\n" + "="*70)
    print("📊 ANALYSIS RESULTS")
    print("="*70)
    pretty_print_results(result.model_dump())
    
    # Save to JSON
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"{base_name}_{timestamp}.json"
    json_path = os.path.join(output_dir, json_filename)
    
    save_results_to_json(result.model_dump(), json_path)
    
    print("\n" + "="*70)
    print("💾 JSON OUTPUT SAVED")
    print("="*70)
    print(f"📁 Location: {json_path}")
    print(f"📊 Size: {os.path.getsize(json_path)} bytes")
    print(f"\n💡 Use this JSON file for:")
    print(f"   - Integration with other systems")
    print(f"   - Database storage")
    print(f"   - API responses")
    print(f"   - Data analysis")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python3 analyze_with_json.py <image_path>")
        print("Example: python3 analyze_with_json.py images/product.jpg\n")
        sys.exit(1)
    
    image_path = sys.argv[1]
    analyze_and_save_json(image_path)
