#!/usr/bin/env python3
"""
Simple Ingredient Analyzer CLI
Analyzes product image and outputs JSON + Markdown report

Usage:
    python3 simple_analyzer.py <image_path>
    python3 simple_analyzer.py <image_path> --user-id <user_id>
    python3 simple_analyzer.py <image_path> --output-dir <output_dir>

Example:
    python3 simple_analyzer.py product.jpg
    python3 simple_analyzer.py product.jpg --user-id abc123
    python3 simple_analyzer.py product.jpg --output-dir results/
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import IngredientAnalysisService


def create_markdown_report(analysis_result: dict, output_path: str):
    """
    Create a markdown report from analysis result.
    
    Args:
        analysis_result: Analysis result dictionary
        output_path: Path to save markdown file
    """
    md_content = []
    
    # Header
    md_content.append("# 🔍 Ingredient Analysis Report\n")
    md_content.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_content.append("---\n")
    
    if not analysis_result.get('success'):
        md_content.append(f"\n❌ **Error:** {analysis_result.get('error', 'Unknown error')}\n")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        return
    
    # Product Information
    md_content.append("\n## 📦 Product Information\n")
    md_content.append(f"**Name:** {analysis_result.get('product_name', 'Unknown Product')}\n")
    md_content.append(f"**Type:** {analysis_result.get('product_type', 'Unknown')}\n")
    
    # Overall Safety Score
    analysis = analysis_result.get('analysis', {})
    safety_score = analysis.get('overall_safety_score', 0)
    
    md_content.append("\n## ⭐ Overall Safety Score\n")
    md_content.append(f"**Score:** {safety_score}/5.0\n")
    
    # Visual rating
    stars = '★' * int(safety_score) + '☆' * (5 - int(safety_score))
    md_content.append(f"**Rating:** {stars}\n")
    
    # Score interpretation
    if safety_score >= 4.5:
        interpretation = "✅ Excellent - Very safe for consumption"
    elif safety_score >= 3.5:
        interpretation = "👍 Good - Generally safe with minor concerns"
    elif safety_score >= 2.5:
        interpretation = "⚠️ Moderate - Some concerns, use with caution"
    elif safety_score >= 1.5:
        interpretation = "⚡ Poor - Multiple concerns, avoid if possible"
    else:
        interpretation = "❌ Very Poor - High risk, not recommended"
    
    md_content.append(f"**Interpretation:** {interpretation}\n")
    
    # Personalized Warnings
    warnings = analysis.get('personalized_warnings', [])
    if warnings:
        md_content.append("\n## ⚠️ Personalized Warnings\n")
        for warning in warnings:
            md_content.append(f"- {warning}\n")
    
    # Ingredients List
    ingredients = analysis_result.get('ingredients', [])
    if ingredients:
        md_content.append("\n## 📋 Ingredients List\n")
        md_content.append(f"**Total Ingredients:** {len(ingredients)}\n\n")
        for i, ingredient in enumerate(ingredients, 1):
            md_content.append(f"{i}. {ingredient}\n")
    
    # Detailed Ingredient Breakdown
    ingredient_breakdown = analysis.get('ingredient_breakdown', [])
    if ingredient_breakdown:
        md_content.append("\n## 🔬 Detailed Ingredient Analysis\n")
        md_content.append("| Ingredient | Category | Safety Score | Concerns |\n")
        md_content.append("|------------|----------|--------------|----------|\n")
        
        for item in ingredient_breakdown:
            name = item.get('name', 'Unknown')
            category = item.get('category', 'Unknown')
            score = item.get('safety_score', 'N/A')
            concerns = item.get('concerns', [])
            concerns_str = ', '.join(concerns) if concerns else 'None'
            
            md_content.append(f"| {name} | {category} | {score} | {concerns_str} |\n")
    
    # Health Recommendations
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        md_content.append("\n## 💡 Health Recommendations\n")
        for rec in recommendations:
            md_content.append(f"- {rec}\n")
    
    # Additional Information
    if analysis_result.get('expiration_date'):
        md_content.append("\n## 📅 Additional Information\n")
        md_content.append(f"**Expiration Date:** {analysis_result.get('expiration_date')}\n")
    
    # Summary
    md_content.append("\n## 📊 Summary\n")
    if safety_score >= 3.5:
        md_content.append("This product appears to be **safe for consumption** with no major concerns.\n")
    elif warnings:
        md_content.append("This product has **some concerns** based on your profile. Review the warnings above.\n")
    else:
        md_content.append("This product has **moderate concerns**. Consider alternatives if available.\n")
    
    # Footer
    md_content.append("\n---\n")
    md_content.append("*Generated by Ingredient Intelligence Analyzer*\n")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Analyze product ingredients from image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 simple_analyzer.py product.jpg
  python3 simple_analyzer.py product.jpg --user-id abc123
  python3 simple_analyzer.py product.jpg --output-dir analysis_results/
  python3 simple_analyzer.py product.jpg --no-markdown
        """
    )
    
    parser.add_argument('image_path', help='Path to product image')
    parser.add_argument('--user-id', help='User ID for personalized analysis')
    parser.add_argument('--output-dir', default='output', help='Output directory for results (default: output/)')
    parser.add_argument('--no-json', action='store_true', help='Skip JSON output')
    parser.add_argument('--no-markdown', action='store_true', help='Skip Markdown report')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress console output')
    
    args = parser.parse_args()
    
    # Validate image path
    if not os.path.exists(args.image_path):
        print(f"❌ Error: Image file not found: {args.image_path}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize service
    if not args.quiet:
        print("\n" + "="*70)
        print("🔍 Ingredient Intelligence Analyzer")
        print("="*70)
        print(f"\n📸 Analyzing image: {args.image_path}")
    
    service = IngredientAnalysisService()
    
    # Load user profile if provided
    user_profile = None
    if args.user_id:
        if not args.quiet:
            print(f"👤 Loading user profile: {args.user_id}")
        
        # Try to load from database
        try:
            from src.user_profile_manager import UserProfileManager
            user = UserProfileManager.get_user(user_id=args.user_id)
            if user:
                user_profile = UserProfileManager.get_user_profile_dict(user)
                if not args.quiet:
                    print(f"   ✓ Profile loaded with {len(user_profile.get('allergens', []))} allergens")
            else:
                if not args.quiet:
                    print(f"   ⚠️  User not found, continuing without profile")
        except Exception as e:
            if not args.quiet:
                print(f"   ⚠️  Could not load user profile: {e}")
    
    # Analyze image
    if not args.quiet:
        print("\n⏳ Analyzing product...")
    
    try:
        result = service.analyze_image(args.image_path, user_profile)
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        sys.exit(1)
    
    if not result.get('success'):
        print(f"\n❌ Analysis failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)
    
    # Generate output filename base
    image_name = Path(args.image_path).stem
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_base = f"{image_name}_{timestamp}"
    
    # Save JSON
    json_path = None
    if not args.no_json:
        json_path = output_dir / f"{output_base}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        if not args.quiet:
            print(f"✅ JSON saved: {json_path}")
    
    # Save Markdown
    md_path = None
    if not args.no_markdown:
        md_path = output_dir / f"{output_base}.md"
        create_markdown_report(result, str(md_path))
        
        if not args.quiet:
            print(f"✅ Markdown report saved: {md_path}")
    
    # Print summary
    if not args.quiet:
        print("\n" + "="*70)
        print("📊 ANALYSIS SUMMARY")
        print("="*70)
        print(f"\n📦 Product: {result.get('product_name', 'Unknown')}")
        print(f"⭐ Safety Score: {result.get('analysis', {}).get('overall_safety_score', 'N/A')}/5.0")
        
        warnings = result.get('analysis', {}).get('personalized_warnings', [])
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings[:3]:  # Show first 3
                print(f"   - {warning}")
            if len(warnings) > 3:
                print(f"   ... and {len(warnings) - 3} more (see full report)")
        else:
            print("\n✅ No warnings for your profile")
        
        ingredients = result.get('ingredients', [])
        print(f"\n📋 Ingredients: {len(ingredients)} found")
        
        print("\n" + "="*70)
        if json_path:
            print(f"📄 JSON: {json_path}")
        if md_path:
            print(f"📝 Report: {md_path}")
        print("="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
