"""
Utility functions for the Ingredient Intelligence Analyzer
"""

import json
from typing import Dict, Any
from datetime import datetime


def format_date(date_str: str) -> str:
    """
    Format date string to YYYY-MM-DD.
    
    Args:
        date_str: Date string in various formats
        
    Returns:
        Formatted date string
    """
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str


def pretty_print_results(result: Dict[str, Any]) -> None:
    """
    Pretty print analysis results to console.
    
    Args:
        result: Analysis result dictionary
    """
    print("\n" + "="*80)
    print("INGREDIENT INTELLIGENCE ANALYSIS REPORT")
    print("="*80)
    
    if not result.get('success'):
        print(f"\n❌ Analysis Failed: {result.get('error', 'Unknown error')}")
        return
    
    # Product Information
    print("\n📦 PRODUCT INFORMATION")
    print("-" * 80)
    print(f"Product Name: {result.get('product_name', 'Unknown')}")
    print(f"Product Type: {result.get('product_type', 'Unknown').upper()}")
    print(f"Classification Confidence: {result.get('classification_confidence', 0):.0%}")
    
    if result.get('expiration_date'):
        status = "✅ Valid" if result.get('expiration_valid') else "⚠️ EXPIRED"
        print(f"Expiration Date: {result.get('expiration_date')} {status}")
    
    # Ingredients
    print("\n🧪 INGREDIENTS")
    print("-" * 80)
    if result.get('ingredients_text'):
        print(f"{result['ingredients_text']}")
    else:
        print("No ingredients detected")
    
    # Health Rating
    print("\n💚 HEALTH ASSESSMENT")
    print("-" * 80)
    rating = result.get('healthiness_rating', 0)
    stars = "⭐" * rating + "☆" * (10 - rating)
    print(f"Healthiness Rating: {rating}/10 {stars}")
    print(f"FDA Approval Status: {result.get('fda_approval', 'Unverified')}")
    
    # Warnings and Alerts
    harmful = result.get('harmful_ingredients', [])
    allergens = result.get('allergens', [])
    
    if harmful or allergens:
        print("\n⚠️  WARNINGS & ALERTS")
        print("-" * 80)
        
        if harmful:
            print(f"❌ Harmful Ingredients ({len(harmful)}):")
            for item in harmful:
                print(f"   • {item}")
        
        if allergens:
            print(f"\n🔴 Allergens ({len(allergens)}):")
            for item in allergens:
                print(f"   • {item}")
    
    # Detailed Breakdown
    print("\n📋 DETAILED BREAKDOWN")
    print("-" * 80)
    
    additives = result.get('additives', [])
    preservatives = result.get('preservatives', [])
    chemicals = result.get('chemicals', [])
    irritants = result.get('irritants', [])
    
    if additives:
        print(f"Additives ({len(additives)}): {', '.join(additives)}")
    
    if preservatives:
        print(f"Preservatives ({len(preservatives)}): {', '.join(preservatives)}")
    
    if chemicals:
        print(f"Chemicals ({len(chemicals)}): {', '.join(chemicals)}")
    
    if irritants:
        print(f"Irritants ({len(irritants)}): {', '.join(irritants)}")
    
    # Certifications
    certifications = result.get('certifications', [])
    if certifications:
        print("\n✨ CERTIFICATIONS")
        print("-" * 80)
        for cert in certifications:
            print(f"✓ {cert}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("-" * 80)
    
    if result.get('recommendation'):
        print(f"Expert Opinion: {result['recommendation']}")
    
    if result.get('health_suggestion'):
        print(f"Health Tip: {result['health_suggestion']}")
    
    # Personalized Analysis (Phase 2)
    if result.get('personalized_recommendation'):
        print("\n🏥 PERSONALIZED ANALYSIS")
        print("-" * 80)
        print(f"For Your Profile: {result['personalized_recommendation']}")
        
        if result.get('safety_score_for_user') is not None:
            user_rating = result['safety_score_for_user']
            user_stars = "⭐" * user_rating + "☆" * (10 - user_rating)
            print(f"Your Safety Score: {user_rating}/10 {user_stars}")
        
        if result.get('warnings_for_user'):
            print(f"\n⚠️  Warnings for You:")
            for warning in result['warnings_for_user']:
                print(f"   • {warning}")
        
        if result.get('matches_preferences') is not None:
            match_status = "✅ YES" if result['matches_preferences'] else "❌ NO"
            print(f"\nMatches Your Preferences: {match_status}")
    
    # Processing info
    if result.get('processing_time'):
        print(f"\n⏱️  Processing Time: {result['processing_time']:.2f} seconds")
    
    print("\n" + "="*80 + "\n")


def save_results_to_json(result: Dict[str, Any], output_path: str) -> bool:
    """
    Save analysis results to JSON file.
    
    Args:
        result: Analysis result dictionary
        output_path: Path to save JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False


def validate_image_path(image_path: str) -> bool:
    """
    Validate that image path exists and is a valid image file.
    
    Args:
        image_path: Path to image file
        
    Returns:
        True if valid, False otherwise
    """
    import os
    
    if not os.path.exists(image_path):
        return False
    
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    ext = os.path.splitext(image_path)[1].lower()
    
    return ext in valid_extensions


def get_health_rating_description(rating: int) -> str:
    """
    Get textual description for health rating.
    
    Args:
        rating: Health rating (1-10)
        
    Returns:
        Description string
    """
    if rating >= 8:
        return "Excellent - Very healthy choice"
    elif rating >= 6:
        return "Good - Generally healthy"
    elif rating >= 4:
        return "Fair - Consume in moderation"
    elif rating >= 2:
        return "Poor - Consider alternatives"
    else:
        return "Very Poor - Avoid if possible"
