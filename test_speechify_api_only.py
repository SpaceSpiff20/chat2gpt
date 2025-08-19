#!/usr/bin/env python3
"""
Simplified test script for Speechify API functionality only
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_speechify_sdk():
    """Test if we can import and use the Speechify SDK directly"""
    print("🔍 Testing Speechify SDK...")
    
    try:
        from speechify import Speechify
        from speechify.tts import GetSpeechOptionsRequest
        print("✅ Successfully imported Speechify SDK")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_speechify_client():
    """Test creating a Speechify client"""
    print("\n🔍 Testing Speechify client creation...")
    
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if not api_key:
        print("⚠️  SPEECHIFY_API_KEY not set")
        return False
    
    try:
        from speechify import Speechify
        client = Speechify(token=api_key)
        print("✅ Successfully created Speechify client")
        return True
    except Exception as e:
        print(f"❌ Error creating client: {e}")
        return False

def test_voices_api():
    """Test the voices API"""
    print("\n🔍 Testing Speechify voices API...")
    
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if not api_key:
        print("⚠️  SPEECHIFY_API_KEY not set")
        return False
    
    try:
        from speechify import Speechify
        client = Speechify(token=api_key)
        
        # Get voices
        voices_response = client.tts.voices.list()
        
        if voices_response:
            print(f"✅ Successfully fetched {len(voices_response)} voices")
            print("   Sample voices:")
            for i, voice in enumerate(voices_response[:5]):
                # Try different possible attribute names
                voice_name = getattr(voice, 'name', getattr(voice, 'display_name', str(voice)))
                voice_id = getattr(voice, 'id', getattr(voice, 'voice_id', 'unknown'))
                print(f"   - {voice_name}: {voice_id}")
            if len(voices_response) > 5:
                print(f"   ... and {len(voices_response) - 5} more voices")
            return True
        else:
            print("❌ No voices returned")
            return False
            
    except Exception as e:
        print(f"❌ Error testing voices API: {e}")
        return False

def test_tts_api():
    """Test the TTS API"""
    print("\n🔍 Testing Speechify TTS API...")
    
    api_key = os.getenv("SPEECHIFY_API_KEY")
    if not api_key:
        print("⚠️  SPEECHIFY_API_KEY not set")
        return False
    
    try:
        from speechify import Speechify
        from speechify.tts import GetSpeechOptionsRequest
        client = Speechify(token=api_key)
        
        # First get a voice
        voices_response = client.tts.voices.list()
        if not voices_response:
            print("❌ No voices available for TTS test")
            return False
        
        # Use the first voice
        test_voice = voices_response[0]
        test_text = "Hello, this is a test of the Speechify text-to-speech API!"
        
        # Get voice name safely
        voice_name = getattr(test_voice, 'name', getattr(test_voice, 'display_name', str(test_voice)))
        voice_id = getattr(test_voice, 'id', getattr(test_voice, 'voice_id', 'unknown'))
        
        print(f"   Testing with voice: {voice_name}")
        print(f"   Test text: {test_text}")
        
        # Call TTS API
        response = client.tts.audio.speech(
            audio_format="mp3",
            input=test_text,
            language="en-US",
            model="simba-english",
            options=GetSpeechOptionsRequest(
                loudness_normalization=False,
                text_normalization=True
            ),
            voice_id=voice_id
        )
        
        if hasattr(response, 'audio_data') and response.audio_data:
            print(f"✅ Successfully generated audio data ({len(response.audio_data)} characters)")
            print(f"   Audio format: {response.audio_format}")
            print(f"   Billable characters: {response.billable_characters_count}")
            return True
        else:
            print("❌ No audio data received")
            return False
            
    except Exception as e:
        print(f"❌ Error testing TTS API: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Speechify API Only...\n")
    
    tests = [
        test_speechify_sdk,
        test_speechify_client,
        test_voices_api,
        test_tts_api
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All Speechify API tests passed!")
        print("   The Speechify integration is working correctly.")
        print("   Note: Google Cloud Storage integration needs to be tested separately.")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        print("\n🔧 Troubleshooting:")
        print("1. Check your SPEECHIFY_API_KEY is set correctly")
        print("2. Verify your API key is valid")
        print("3. Check your internet connection")

if __name__ == "__main__":
    main() 