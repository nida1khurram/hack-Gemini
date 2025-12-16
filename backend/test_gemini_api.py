#!/usr/bin/env python3
"""
Test script to verify Google Gemini API key directly
"""

import google.generativeai as genai
from src.database import settings

def test_gemini_api():
    print("Testing Google Gemini API key...")
    print(f"API Key: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-5:]}")  # Show partial key
    print(f"API Key Length: {len(settings.GEMINI_API_KEY)}")
    print(f"Model: {settings.GEMINI_CHAT_MODEL}")

    try:
        # Configure the API
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Try to list models to verify the API key works
        print("\nListing available models...")
        models = genai.list_models()
        for model in models:
            print(f"Model: {model.name}")

        # Try to create a model instance and generate content
        print(f"\nTesting model: {settings.GEMINI_CHAT_MODEL}")
        model = genai.GenerativeModel(settings.GEMINI_CHAT_MODEL)

        print("Generating content...")
        response = model.generate_content("Hello, how are you?")

        if response.text:
            print(f"[SUCCESS] Response: {response.text[:100]}...")
        else:
            print("[FAILED] Got empty response")

    except Exception as e:
        print(f"[ERROR] {e}")
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str or "exceeded" in error_str:
            print("[INFO] This is a quota/exceeding limits issue - your API key is valid but has exceeded usage limits")
        elif "api key" in error_str or "invalid" in error_str or "400" in error_str:
            print("[INFO] This is an invalid API key issue - your API key needs to be regenerated")
        else:
            print("[INFO] This is another type of error")

if __name__ == "__main__":
    test_gemini_api()