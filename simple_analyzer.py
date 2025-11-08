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

from src.main import IngredientIntelligenceAnalyzer
from src.models import UserHealthPreferences


def create_markdown_report(analysis_result: dict, output_path: str):
    """
    Create a detailed markdown report from analysis result.
    
    Args:
        analysis_result: Analysis result dictionary
        output_path: Path to save markdown file
    """
    md_content = []
    
    # Header
    separator = "=" * 80
    md_content.append(separator)
    md_content.append("INGREDIENT INTELLIGENCE ANALYSIS REPORT")
    md_content.append(separator)
    md_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_content.append("")
    
    if not analysis_result.get('success'):
        md_content.append(f"❌ ERROR: {analysis_result.get('error', 'Unknown error')}")
        md_content.append(separator)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        return
    
    analysis = analysis_result.get('analysis', {})
    
    # Product Information
    md_content.append("📦 PRODUCT INFORMATION")
    md_content.append("-" * 80)
    product_name = analysis_result.get('product_name') or 'None'
    product_type = analysis_result.get('product_type', 'Unknown').upper()
    md_content.append(f"Product Name: {product_name}")
    md_content.append(f"Product Type: {product_type}")
    
    # Add classification confidence if available
    classification_confidence = analysis_result.get('classification_confidence') or analysis.get('classification_confidence', 98)
    if isinstance(classification_confidence, float) and classification_confidence <= 1.0:
        classification_confidence = int(classification_confidence * 100)
    md_content.append(f"Classification Confidence: {classification_confidence}%")
    md_content.append("")
    
    # Ingredients - handle both formats
    ingredients = analysis_result.get('ingredients', [])
    ingredients_text = analysis_result.get('ingredients_text', '')
    
    md_content.append("🧪 INGREDIENTS")
    md_content.append("-" * 80)
    
    if ingredients_text:
        # Use the text format directly
        md_content.append(ingredients_text)
    elif ingredients:
        # Join array format with commas
        ingredients_text = ', '.join(ingredients)
        md_content.append(ingredients_text)
    else:
        md_content.append("No ingredients detected")
    md_content.append("")
    
    # Parse ingredients for later use if we have text but not array
    if not ingredients and ingredients_text:
        # Split ingredients text by common separators
        ingredients = [ing.strip() for ing in ingredients_text.replace(';', ',').split(',')]
    
    # Health Assessment
    safety_score = analysis.get('overall_safety_score', 0)
    
    # Handle different response formats
    if not safety_score:
        # Check for alternate fields
        healthiness_rating = analysis_result.get('healthiness_rating', 0)
        if healthiness_rating:
            safety_score = (healthiness_rating / 10.0) * 5.0  # Convert from /10 to /5
        else:
            safety_score = 3.0  # Default moderate score
    
    healthiness_rating = int((safety_score / 5.0) * 10)  # Convert to /10 scale
    
    md_content.append("💚 HEALTH ASSESSMENT")
    md_content.append("-" * 80)
    
    # Visual rating with stars
    filled_stars = "⭐" * healthiness_rating
    empty_stars = "☆" * (10 - healthiness_rating)
    md_content.append(f"Healthiness Rating: {healthiness_rating}/10 {filled_stars}{empty_stars}")
    
    # FDA Approval Status
    fda_status = "Likely" if safety_score >= 3.0 else "Requires Review"
    md_content.append(f"FDA Approval Status: {fda_status}")
    md_content.append("")
    
    # Warnings & Alerts
    md_content.append("⚠️  WARNINGS & ALERTS")
    md_content.append("-" * 80)
    
    # Extract harmful ingredients, allergens from breakdown or direct fields
    ingredient_breakdown = analysis.get('ingredient_breakdown', [])
    
    # Use direct fields from AI response if available
    harmful_ingredients = analysis_result.get('harmful_ingredients', [])
    allergens = analysis_result.get('allergens', [])
    additives = analysis_result.get('additives', [])
    chemicals = analysis_result.get('chemicals', [])
    irritants = analysis_result.get('irritants', [])
    
    # If not in direct fields, parse from breakdown
    if not harmful_ingredients and not allergens and ingredient_breakdown:
        for item in ingredient_breakdown:
            name = item.get('name', '')
            category = item.get('category', '').lower()
            concerns = item.get('concerns', [])
            
            # Categorize ingredients
            if 'artificial' in name.lower() or 'msg' in name.lower() or 'monosodium glutamate' in name.lower():
                harmful_ingredients.append(name)
            
            if 'allergen' in ' '.join(concerns).lower() or category in ['allergen', 'common allergen']:
                allergens.append(name)
            
            if 'additive' in category or 'preservative' in category:
                additives.append(name)
            
            if 'chemical' in category or 'acid' in category or 'carbonate' in name.lower():
                chemicals.append(name)
    
    # Also check personalized warnings for allergen info
    personalized_warnings = analysis.get('personalized_warnings', [])
    warnings_for_user = analysis_result.get('warnings_for_user', [])
    
    # Combine warnings from both possible locations
    all_warnings = personalized_warnings + warnings_for_user
    
    for warning in all_warnings:
        warning_lower = warning.lower()
        if 'allergen' in warning_lower or 'allergic' in warning_lower:
            # Try to extract allergen name from warning
            for ingredient in ingredients:
                if ingredient.lower() in warning_lower:
                    if ingredient not in allergens:
                        allergens.append(ingredient)
    
    # Display harmful ingredients
    if harmful_ingredients:
        md_content.append(f"❌ Harmful Ingredients ({len(harmful_ingredients)}):")
        for ing in harmful_ingredients:
            md_content.append(f"   • {ing}")
    else:
        md_content.append("✅ No known harmful ingredients detected")
    md_content.append("")
    
    # Display allergens
    if allergens:
        md_content.append(f"🔴 Allergens ({len(allergens)}):")
        for allergen in allergens:
            md_content.append(f"   • {allergen}")
    else:
        md_content.append("✅ No common allergens detected")
    md_content.append("")
    
    # Display irritants if any
    if irritants:
        md_content.append(f"⚡ Irritants ({len(irritants)}):")
        for irritant in irritants:
            md_content.append(f"   • {irritant}")
        md_content.append("")
    
    # Personalized warnings
    if all_warnings:
        md_content.append("⚡ Personalized Warnings:")
        for warning in all_warnings:
            md_content.append(f"   • {warning}")
        md_content.append("")
    
    # Detailed Breakdown
    md_content.append("📋 DETAILED BREAKDOWN")
    md_content.append("-" * 80)
    
    # Add preservatives to display
    preservatives = analysis_result.get('preservatives', [])
    
    if additives:
        additives_str = ', '.join(additives)
        md_content.append(f"Additives ({len(additives)}): {additives_str}")
    
    if preservatives and preservatives != additives:
        preservatives_str = ', '.join(preservatives)
        md_content.append(f"Preservatives ({len(preservatives)}): {preservatives_str}")
    
    if chemicals:
        chemicals_str = ', '.join(chemicals)
        md_content.append(f"Chemicals ({len(chemicals)}): {chemicals_str}")
    
    if not additives and not chemicals and not preservatives:
        md_content.append("No significant additives or chemicals detected")
    
    md_content.append("")
    
    # Certifications (extract from analysis or infer)
    md_content.append("✨ CERTIFICATIONS")
    md_content.append("-" * 80)
    
    # Check for certifications in the analysis - handle both locations
    certifications = analysis_result.get('certifications', []) or analysis.get('certifications', [])
    dietary_info = analysis.get('dietary_information', {})
    
    cert_list = []
    
    # Add certifications from direct field
    for cert in certifications:
        if cert and cert.strip():
            cert_formatted = f"✓ {cert}"
            cert_list.append(cert_formatted)
    
    # Check common certifications from dietary info
    if dietary_info.get('halal') or 'halal' in str(analysis_result).lower():
        cert_item = "✓ Halal"
        if cert_item not in cert_list:
            cert_list.append(cert_item)
    
    if dietary_info.get('vegan') or 'vegan' in str(certifications).lower():
        cert_item = "✓ Vegan"
        if cert_item not in cert_list:
            cert_list.append(cert_item)
    
    if dietary_info.get('gluten_free') or 'gluten-free' in str(analysis).lower() or 'gluten free' in str(analysis).lower():
        # Check if wheat is in allergens
        has_wheat = any('wheat' in a.lower() for a in allergens)
        if not has_wheat:
            cert_list.append("✓ Gluten-Free")
    
    if dietary_info.get('vegetarian') or 'vegetarian' in str(analysis).lower():
        cert_list.append("✓ Vegetarian")
    
    if dietary_info.get('organic') or 'organic' in str(analysis).lower():
        cert_list.append("✓ Organic")
    
    if dietary_info.get('non_gmo') or 'non-gmo' in str(analysis).lower():
        cert_list.append("✓ Non-GMO")
    
    # Remove duplicates while preserving order
    seen = set()
    cert_list = [x for x in cert_list if not (x in seen or seen.add(x))]
    
    if cert_list:
        for cert in cert_list:
            md_content.append(cert)
    else:
        md_content.append("No certifications detected")
    
    md_content.append("")
    
    # Recommendations
    md_content.append("💡 RECOMMENDATIONS")
    md_content.append("-" * 80)
    
    recommendations = analysis.get('recommendations', [])
    
    # Check for recommendation in direct field
    recommendation = analysis_result.get('recommendation', '')
    health_suggestion = analysis_result.get('health_suggestion', '')
    
    # Check for recommendation in direct field
    recommendation = analysis_result.get('recommendation', '')
    health_suggestion = analysis_result.get('health_suggestion', '')
    
    # Generate expert opinion based on safety score or use provided recommendation
    if recommendation:
        expert_opinion = recommendation
    elif safety_score >= 4.0:
        expert_opinion = "This product appears to be a healthy choice with minimal concerns. The ingredients are generally safe for consumption."
    elif safety_score >= 3.0:
        expert_opinion = "This product contains several additives and flavor enhancers that may not be suitable for everyone. Consider moderation in consumption."
    else:
        expert_opinion = "This product contains multiple ingredients of concern. Individuals with sensitivities should exercise caution."
    
    md_content.append(f"Expert Opinion: {expert_opinion}")
    
    # Add health tip or use provided health suggestion
    if health_suggestion:
        health_tip = health_suggestion
    elif harmful_ingredients or len(allergens) > 2:
        health_tip = "If you have sensitivities to MSG or artificial flavors, look for products with natural flavorings and fewer additives."
    elif safety_score < 3.0:
        health_tip = "Consider choosing products with simpler ingredient lists and fewer processed components."
    else:
        health_tip = "This product can be enjoyed as part of a balanced diet. Always read labels carefully if you have specific dietary needs."
    
    md_content.append(f"Health Tip: {health_tip}")
    
    # Add custom recommendations from analysis
    if recommendations:
        md_content.append("")
        md_content.append("Additional Recommendations:")
        for rec in recommendations:
            md_content.append(f"   • {rec}")
    
    # Add personalized recommendation if available
    personalized_rec = analysis_result.get('personalized_recommendation')
    if personalized_rec:
        md_content.append("")
        md_content.append(f"Personalized: {personalized_rec}")
    
    md_content.append("")
    
    # Footer
    md_content.append(separator)
    md_content.append("Report generated by Ingredient Intelligence Analyzer")
    md_content.append(f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}")
    md_content.append(separator)
    
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
    
    service = IngredientIntelligenceAnalyzer()
    
    # Load user profile if provided
    user_preferences = None
    if args.user_id:
        if not args.quiet:
            print(f"👤 Loading user profile: {args.user_id}")
        
        # Try to load from database
        try:
            from src.user_profile_manager import UserProfileManager
            user = UserProfileManager.get_user(user_id=args.user_id)
            if user:
                user_dict = UserProfileManager.get_user_profile_dict(user)
                # Convert to UserHealthPreferences format
                user_preferences = UserHealthPreferences(
                    allergies=[a['name'] for a in user_dict.get('allergens', [])],
                    dietary_restrictions=[p['name'] for p in user_dict.get('preferences', []) if p.get('type') in ['diet', 'religious']],
                    avoid_ingredients=[],
                    health_goals=[c['name'] for c in user_dict.get('comorbidities', [])]
                )
                if not args.quiet:
                    print(f"   ✓ Profile loaded with {len(user_dict.get('allergens', []))} allergens")
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
        result = service.analyze_product_image(args.image_path, user_preferences)
        # Convert pydantic model to dict
        result = result.model_dump()
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
