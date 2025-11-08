#!/usr/bin/env python3
"""
Example usage of the Ingredient Intelligence Analyzer
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.main import IngredientIntelligenceAnalyzer
from src.utils import pretty_print_results, save_results_to_json


def example_analyze_from_image():
    """Example: Analyze product from image."""
    print("="*80)
    print("EXAMPLE 1: Analyze Product from Image")
    print("="*80)
    
    # Initialize analyzer
    analyzer = IngredientIntelligenceAnalyzer()
    
    # Analyze image
    image_path = "examples/sample_product.jpg"  # Replace with your image
    
    if not os.path.exists(image_path):
        print(f"\n⚠️  Image not found: {image_path}")
        print("Please provide a valid product image path")
        return
    
    result = analyzer.analyze_product_image(image_path)
    
    # Display results
    pretty_print_results(result.model_dump())
    
    # Save to JSON
    save_results_to_json(result.model_dump(), "output/analysis_result.json")
    print("✅ Results saved to: output/analysis_result.json")


def example_analyze_from_text():
    """Example: Analyze ingredients from text directly."""
    print("="*80)
    print("EXAMPLE 2: Analyze Ingredients from Text")
    print("="*80)
    
    # Sample ingredients
    ingredients = """
    Water, Sugar, High Fructose Corn Syrup, Citric Acid, 
    Sodium Benzoate (preservative), Natural and Artificial Flavors, 
    Yellow 5, Red 40, Ascorbic Acid (Vitamin C)
    """
    
    # Initialize analyzer
    analyzer = IngredientIntelligenceAnalyzer()
    
    # Analyze
    result = analyzer.analyze_from_text(
        ingredients_text=ingredients.strip(),
        product_type="drink",
        expiration_date="2026-12-31"
    )
    
    # Display results
    pretty_print_results(result.model_dump())


def example_beauty_product():
    """Example: Analyze beauty product."""
    print("="*80)
    print("EXAMPLE 3: Analyze Beauty Product")
    print("="*80)
    
    # Sample beauty product ingredients
    ingredients = """
    Water, Glycerin, Dimethicone, Cetyl Alcohol, Stearyl Alcohol,
    Methylparaben, Propylparaben, Fragrance, Tocopheryl Acetate,
    Retinyl Palmitate, Phenoxyethanol, DMDM Hydantoin
    """
    
    # Initialize analyzer
    analyzer = IngredientIntelligenceAnalyzer()
    
    # Analyze
    result = analyzer.analyze_from_text(
        ingredients_text=ingredients.strip(),
        product_type="beauty"
    )
    
    # Display results
    pretty_print_results(result.model_dump())


def example_command_line():
    """Example: Command-line usage."""
    print("="*80)
    print("EXAMPLE 4: Command-Line Usage")
    print("="*80)
    
    if len(sys.argv) < 2:
        print("\nUsage Examples:")
        print("-" * 80)
        print("\n1. Analyze from image:")
        print("   python example.py path/to/product_image.jpg")
        print("\n2. Analyze from text:")
        print("   python example.py --text 'Water, Sugar, Salt'")
        print("\n3. Analyze with product type:")
        print("   python example.py --text 'Water, Sugar' --type drink")
        print("\n")
        return
    
    # Parse arguments
    if "--text" in sys.argv:
        text_idx = sys.argv.index("--text") + 1
        ingredients_text = sys.argv[text_idx]
        
        product_type = None
        if "--type" in sys.argv:
            type_idx = sys.argv.index("--type") + 1
            product_type = sys.argv[type_idx]
        
        analyzer = IngredientIntelligenceAnalyzer()
        result = analyzer.analyze_from_text(
            ingredients_text=ingredients_text,
            product_type=product_type
        )
        pretty_print_results(result.model_dump())
    
    else:
        # Assume it's an image path
        image_path = sys.argv[1]
        
        if not os.path.exists(image_path):
            print(f"❌ Error: Image not found: {image_path}")
            return
        
        # Use Vision API by default (recommended)
        analyzer = IngredientIntelligenceAnalyzer(ocr_method='vision')
        
        # Or use PaddleOCR (uncomment below):
        # analyzer = IngredientIntelligenceAnalyzer(ocr_method='paddleocr', max_image_dimension=1920)
        
        result = analyzer.analyze_product_image(image_path)
        
        # Display results
        pretty_print_results(result.model_dump())
        
        # Save to JSON file
        import os
        from datetime import datetime
        
        # Create output directory
        output_dir = "results"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_filename = f"{base_name}_{timestamp}.json"
        json_path = os.path.join(output_dir, json_filename)
        
        # Save to JSON
        save_results_to_json(result.model_dump(), json_path)
        print(f"\n💾 Results saved to: {json_path}\n")


def example_batch_processing():
    """Example: Process multiple products."""
    print("="*80)
    print("EXAMPLE 5: Batch Processing")
    print("="*80)
    
    # Sample products
    products = [
        {
            "name": "Soda",
            "ingredients": "Carbonated water, Sugar, Citric acid, Natural flavors, Caffeine",
            "type": "drink"
        },
        {
            "name": "Face Cream",
            "ingredients": "Water, Glycerin, Dimethicone, Methylparaben, Fragrance",
            "type": "beauty"
        },
        {
            "name": "Cookies",
            "ingredients": "Wheat flour, Sugar, Palm oil, Chocolate chips, Baking soda, Salt",
            "type": "food"
        }
    ]
    
    analyzer = IngredientIntelligenceAnalyzer()
    results = []
    
    for product in products:
        print(f"\n{'='*80}")
        print(f"Analyzing: {product['name']}")
        print(f"{'='*80}")
        
        result = analyzer.analyze_from_text(
            ingredients_text=product['ingredients'],
            product_type=product['type']
        )
        
        results.append({
            'name': product['name'],
            'result': result.model_dump()
        })
        
        # Quick summary
        print(f"\n✅ {product['name']}: Rating {result.healthiness_rating}/10")
        print(f"   Harmful: {len(result.harmful_ingredients)}, "
              f"Allergens: {len(result.allergens)}")
    
    print(f"\n\n{'='*80}")
    print(f"Batch processing complete: {len(results)} products analyzed")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("examples", exist_ok=True)
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║          INGREDIENT INTELLIGENCE ANALYZER - USAGE EXAMPLES                   ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Run examples
    try:
        # Check if running with command-line arguments
        if len(sys.argv) > 1:
            example_command_line()
        else:
            # Run demo examples
            print("Running demo examples...\n")
            
            # Example 2: Text-based analysis (no image needed)
            example_analyze_from_text()
            input("\nPress Enter to continue to next example...")
            
            # Example 3: Beauty product
            example_beauty_product()
            input("\nPress Enter to continue to next example...")
            
            # Example 5: Batch processing
            example_batch_processing()
            
            print("\n✅ All examples completed!")
            print("\nTo analyze your own products:")
            print("  • From image: python example.py path/to/image.jpg")
            print("  • From text:  python example.py --text 'your ingredients' --type food")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
