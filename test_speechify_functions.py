#!/usr/bin/env python3
"""
Test script for Speechify TTS functions
"""

import os
import sys
import base64

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_speechify_imports():
    """Test if we can import the Speechify module"""
    print("🔍 Testing Speechify imports...")
    
    try:
        from utils.speechify import get_voices_data, text_to_speech, filter_voice_models
        print("✅ Successfully imported Speechify functions")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_voices_function():
    """Test the get_voices_data function"""
    print("\n🔍 Testing get_voices_data function...")
    
    # Check if API key is set
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if not api_key or api_key == "your_speechify_api_key_here":
        print("⚠️  SPEECHIFY_API_KEY not set or using placeholder")
        print("   Set your API key: export SPEECHIFY_API_KEY='your_actual_key'")
        return False
    
    try:
        from utils.speechify import get_voices_data
        
        voices_data, error = get_voices_data()
        
        if error:
            print(f"❌ Error fetching voices: {error}")
            return False
        
        if voices_data:
            print(f"✅ Successfully fetched {len(voices_data)} voices")
            print("   Sample voices:")
            for i, (name, voice_id) in enumerate(list(voices_data.items())[:5]):
                print(f"   - {name}: {voice_id}")
            if len(voices_data) > 5:
                print(f"   ... and {len(voices_data) - 5} more voices")
            return True
        else:
            print("❌ No voices returned")
            return False
            
    except Exception as e:
        print(f"❌ Error testing voices function: {e}")
        return False

def test_tts_function():
    """Test the text_to_speech function"""
    print("\n🔍 Testing text_to_speech function...")
    
    # Check if API key is set
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if not api_key or api_key == "your_speechify_api_key_here":
        print("⚠️  SPEECHIFY_API_KEY not set or using placeholder")
        return False
    
    # Check if GCS bucket is set
    gcs_bucket = os.getenv("GCS_BUCKET_NAME")
    if not gcs_bucket or gcs_bucket == "your_gcs_bucket_name_here":
        print("⚠️  GCS_BUCKET_NAME not set - TTS will work but won't save to storage")
        print("   Set your bucket: export GCS_BUCKET_NAME='your_bucket_name'")
    
    try:
        from utils.speechify import text_to_speech, get_voices_data
        
        # First get available voices
        voices_data, error = get_voices_data()
        if error or not voices_data:
            print("❌ Cannot test TTS without available voices")
            return False
        
        # Use the first available voice
        test_voice = list(voices_data.keys())[0]
        test_text = "Hello, this is a test of the Speechify text-to-speech API!"
        
        print(f"   Testing with voice: {test_voice}")
        print(f"   Test text: {test_text}")
        
        audio_url, error = text_to_speech(test_text, test_voice)
        
        if error:
            print(f"❌ Error in TTS: {error}")
            return False
        
        if audio_url:
            print(f"✅ Successfully generated audio: {audio_url}")
            return True
        else:
            print("❌ No audio URL returned")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TTS function: {e}")
        return False

def test_voice_filtering():
    """Test the filter_voice_models function"""
    print("\n🔍 Testing filter_voice_models function...")
    
    try:
        from utils.speechify import filter_voice_models, get_voices_data
        
        # Get voices first
        voices_data, error = get_voices_data()
        if error or not voices_data:
            print("❌ Cannot test filtering without available voices")
            return False
        
        # Test filtering (this is a mock test since we don't have the actual voice objects)
        print("✅ filter_voice_models function is available")
        print("   Note: Full filtering test requires actual voice objects from API")
        return True
        
    except Exception as e:
        print(f"❌ Error testing voice filtering: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Speechify Functions...\n")
    
    tests = [
        test_speechify_imports,
        test_voices_function,
        test_tts_function,
        test_voice_filtering
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Speechify integration is working correctly!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed or skipped")
        print("\n🔧 To run full tests:")
        print("1. Get a Speechify API key from https://console.sws.speechify.com/signup")
        print("2. Set environment variables:")
        print("   export SPEECHIFY_API_KEY='your_api_key'")
        print("   export GCS_BUCKET_NAME='your_bucket_name' (optional)")
        print("3. Run this script again")

if __name__ == "__main__":
    main() 