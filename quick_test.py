#!/usr/bin/env python3
"""
Quick performance test script
Compare different image sizes and processing times
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import IngredientIntelligenceAnalyzer


def test_image_with_different_sizes(image_path: str):
    """Test the same image with different max dimensions."""
    
    print("="*80)
    print(f"Testing: {image_path}")
    print("="*80)
    print()
    
    # Test configurations
    configs = [
        (1280, "Fast Mode")
    ]
    
    results = []
    
    for max_dim, description in configs:
        print(f"\n{'='*80}")
        print(f"{description} - Max Dimension: {max_dim}px")
        print('='*80)
        
        try:
            # Initialize with specific dimension
            analyzer = IngredientIntelligenceAnalyzer(max_image_dimension=max_dim)
            
            # Track time
            start_time = time.time()
            
            # Analyze
            result = analyzer.analyze_product_image(image_path)
            
            # Calculate time
            elapsed = time.time() - start_time
            
            # Store results
            results.append({
                'mode': description,
                'max_dim': max_dim,
                'time': elapsed,
                'success': result.success,
                'ingredients_found': bool(result.ingredients_text),
                'product_type': result.product_type
            })
            
            print(f"\n✅ OCR completed in {elapsed:.2f} seconds")
            
            if result.success:
                print(f"   ✓ Product Type: {result.product_type}")
                print(f"   ✓ Ingredients Found: {'Yes' if result.ingredients_text else 'No'}")
                if result.ingredients_text:
                    preview = result.ingredients_text[:100]
                    print(f"   ✓ Preview: {preview}...")
                if result.healthiness_rating:
                    print(f"   ✓ Health Rating: {result.healthiness_rating}/10")
            else:
                print(f"   ⚠️  Analysis failed: {result.error}")
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            results.append({
                'mode': description,
                'max_dim': max_dim,
                'time': 0,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n\n" + "="*80)
    print("PERFORMANCE SUMMARY")
    print("="*80)
    print()
    
    print(f"{'Mode':<30} {'Time (sec)':<15} {'Status':<15}")
    print("-"*60)
    
    for r in results:
        status = "✅ Success" if r['success'] else "❌ Failed"
        print(f"{r['mode']:<30} {r['time']:<15.2f} {status:<15}")
    
    print()
    
    # Speed comparison
    if len(results) > 1 and all(r['success'] for r in results):
        fastest = min(results, key=lambda x: x['time'])
        slowest = max(results, key=lambda x: x['time'])
        speedup = slowest['time'] / fastest['time']
        
        print(f"📊 Analysis:")
        print(f"   Fastest: {fastest['mode']} ({fastest['time']:.2f}s)")
        print(f"   Slowest: {slowest['mode']} ({slowest['time']:.2f}s)")
        print(f"   Speed difference: {speedup:.2f}x")
        print()
        print(f"💡 Recommendation: Use {fastest['mode']} for {speedup:.1f}x faster processing!")
    
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_test.py <image_path>")
        print("\nExample:")
        print("  python quick_test.py images/combi.JPG")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    print("\n🚀 Performance Testing Tool")
    print("Testing different image sizes to find optimal speed/accuracy balance\n")
    
    test_image_with_different_sizes(image_path)
    
    print("✅ Testing complete!")
    print("\nTo use the fastest setting in your code:")
    print("  analyzer = IngredientIntelligenceAnalyzer(max_image_dimension=1280)")
    print()
