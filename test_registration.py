#!/usr/bin/env python3
"""
Test script to verify user registration works
"""

import requests
import json

# Test registration
url = "http://localhost:5000/api/user/register"

test_user = {
    "username": "test_user_123",
    "email": "test@example.com",
    "personal_info": {
        "full_name": "Test User",
        "age": 25,
        "birthday": "2000-01-15"
    },
    "allergens": ["Peanuts", "Milk"],
    "preferences": ["Vegan", "Low Sodium"],
    "comorbidities": ["Diabetes Type 2"]
}

print("🧪 Testing User Registration API")
print("=" * 60)
print(f"URL: {url}")
print(f"Payload: {json.dumps(test_user, indent=2)}")
print("=" * 60)

try:
    response = requests.post(url, json=test_user)
    print(f"\n✅ Status Code: {response.status_code}")
    print(f"📦 Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        data = response.json()
        if data.get('success'):
            print(f"\n🎉 SUCCESS! User created with ID: {data.get('user_id')}")
        else:
            print(f"\n❌ FAILED: {data.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP Error {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: Cannot connect to server")
    print("Make sure Flask server is running: python3 app.py")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
