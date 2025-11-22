#!/usr/bin/env python3
"""
Test script to verify if the OpenAI API key is working correctly.
"""
import os
import sys

def test_openai_key():
    """Test the OpenAI API key by making a simple API call."""
    
    # Get the API key from environment or use the one from config
    api_key = os.environ.get('OPENAI_API_KEY', 'scale-iq')
    
    print("=" * 60)
    print("Testing OpenAI API Key")
    print("=" * 60)
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    print(f"API Key length: {len(api_key)} characters")
    print()
    
    # Check if it looks like a placeholder
    if api_key == 'scale-iq' or len(api_key) < 20:
        print("⚠️  WARNING: The API key appears to be a placeholder!")
        print("   Expected format: sk-... (starts with 'sk-' and is ~50+ characters)")
        print()
    
    # Set the environment variable
    os.environ['OPENAI_API_KEY'] = api_key
    
    try:
        # Try importing required libraries
        print("1. Checking dependencies...")
        from litellm import completion
        from google.adk.models.lite_llm import LiteLlm
        print("   ✓ Dependencies imported successfully")
        print()
        
        # Test 1: Direct LiteLLM call
        print("2. Testing direct LiteLLM API call...")
        try:
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": "Say 'API key is working!' if you can read this."}
                ],
                api_key=api_key,
                timeout=10
            )
            
            if response and response.choices:
                result = response.choices[0].message.content
                print(f"   ✓ API call successful!")
                print(f"   Response: {result}")
                print()
                return True
            else:
                print("   ✗ API call returned empty response")
                return False
                
        except Exception as e:
            error_msg = str(e)
            print(f"   ✗ API call failed: {error_msg}")
            print()
            
            # Provide helpful error messages
            if "Invalid API key" in error_msg or "401" in error_msg or "Unauthorized" in error_msg or "Incorrect API key" in error_msg:
                print("   → The API key is invalid or expired")
                print("   → 'scale-iq' is a placeholder, not a real API key")
            elif "Rate limit" in error_msg or "429" in error_msg:
                print("   → Rate limit exceeded (but key might be valid)")
            elif "Insufficient quota" in error_msg or "quota" in error_msg.lower():
                print("   → API key has insufficient quota/credits")
            else:
                print("   → Check your internet connection and API key format")
            
            return False
        
        # Test 2: Test with ADK LiteLlm model (same as agents use)
        print("3. Testing with ADK LiteLlm model (same as agents)...")
        try:
            model = LiteLlm("openai/gpt-4o")
            # This is a basic test - ADK models need more setup for full testing
            print("   ✓ LiteLlm model initialized successfully")
            print("   (Full ADK agent testing requires running the agents)")
            print()
            return True
        except Exception as e:
            print(f"   ✗ LiteLlm initialization failed: {e}")
            return False
            
    except ImportError as e:
        print(f"   ✗ Missing dependency: {e}")
        print("   Please install requirements: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

if __name__ == '__main__':
    success = test_openai_key()
    print("=" * 60)
    if success:
        print("✓ API Key Test: PASSED")
    else:
        print("✗ API Key Test: FAILED")
        print("\nTo fix:")
        print("1. Get a valid OpenAI API key from https://platform.openai.com/api-keys")
        print("2. Set it as: export OPENAI_API_KEY='your-actual-key'")
        print("3. Or update the key in start_services.py, start_all.sh, and start_app.sh")
    print("=" * 60)
    sys.exit(0 if success else 1)

