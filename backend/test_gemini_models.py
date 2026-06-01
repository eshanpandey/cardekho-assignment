"""Test script to list available Gemini models."""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env")
    exit(1)

print(f"API Key found: {api_key[:10]}...")

genai.configure(api_key=api_key)

print("\nAvailable models:")
print("-" * 50)

try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display name: {model.display_name}")
            print(f"  Description: {model.description[:100]}...")
            print()
except Exception as e:
    print(f"ERROR: {e}")
    print("\nTrying alternative approach...")
    
    # Try with common model names
    test_models = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
    ]
    
    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say hello")
            print(f"✓ {model_name} - WORKS!")
            print(f"  Response: {response.text[:50]}...")
            break
        except Exception as e:
            print(f"✗ {model_name} - {str(e)[:80]}")
