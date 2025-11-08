#!/usr/bin/env python3
"""
Simple test script to verify installation and basic functionality
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import cv2
        print("  ✓ OpenCV")
    except ImportError as e:
        print(f"  ✗ OpenCV: {e}")
        return False
    
    try:
        import paddleocr
        print("  ✓ PaddleOCR")
    except ImportError as e:
        print(f"  ✗ PaddleOCR: {e}")
        return False
    
    try:
        import openai
        print("  ✓ OpenAI")
    except ImportError as e:
        print(f"  ✗ OpenAI: {e}")
        return False
    
    try:
        from pydantic import BaseModel
        print("  ✓ Pydantic")
    except ImportError as e:
        print(f"  ✗ Pydantic: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
    except ImportError as e:
        print(f"  ✗ python-dotenv: {e}")
        return False
    
    return True


def test_project_structure():
    """Test if project structure is correct."""
    print("\nTesting project structure...")
    
    required_files = [
        'src/__init__.py',
        'src/main.py',
        'src/ocr_detector.py',
        'src/classifier.py',
        'src/ingredient_analyzer.py',
        'src/models.py',
        'src/utils.py',
        'requirements.txt',
        '.env.example',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (missing)")
            all_exist = False
    
    return all_exist


def test_env_file():
    """Test if .env file exists and has API key."""
    print("\nTesting environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ⚠️  .env file not found")
        print("     Run: cp .env.example .env")
        print("     Then add your OPENAI_API_KEY")
        return False
    
    print("  ✓ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("  ⚠️  OPENAI_API_KEY not set")
        print("     Edit .env and add your actual API key")
        return False
    
    print("  ✓ OPENAI_API_KEY is set")
    return True


def test_basic_functionality():
    """Test basic functionality of each module."""
    print("\nTesting basic functionality...")
    
    try:
        from src.classifier import ProductClassifier
        classifier = ProductClassifier()
        result = classifier.classify("Water, Sugar, Salt")
        print(f"  ✓ Classifier works (detected: {result['product_type']})")
    except Exception as e:
        print(f"  ✗ Classifier failed: {e}")
        return False
    
    try:
        from src.models import ProductAnalysisResponse
        response = ProductAnalysisResponse(
            success=True,
            product_type="food",
            healthiness_rating=5
        )
        print("  ✓ Models work")
    except Exception as e:
        print(f"  ✗ Models failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("="*60)
    print("INGREDIENT INTELLIGENCE ANALYZER - INSTALLATION TEST")
    print("="*60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Project Structure", test_project_structure),
        ("Environment", test_env_file),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test failed with error: {e}")
            results.append((name, False))
        print()
    
    # Summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 All tests passed! Your installation is ready.")
        print("\nNext steps:")
        print("  1. Run: python example.py")
        print("  2. Or analyze your own product:")
        print("     python example.py --text 'Water, Sugar' --type drink")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  • Missing packages: pip install -r requirements.txt")
        print("  • Missing .env: cp .env.example .env")
        print("  • Add API key: Edit .env and set OPENAI_API_KEY")
    
    print()
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
