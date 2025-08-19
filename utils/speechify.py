import base64
import uuid
from env_loader import get_env
from utils.gcs import initialize_gcs_client
from speechify import Speechify
from speechify.tts import GetSpeechOptionsRequest

SPEECHIFY_API_KEY = get_env("SPEECHIFY_API_KEY")
GCS_BUCKET_NAME = get_env("GCS_BUCKET_NAME")

if GCS_BUCKET_NAME:
    storage_client = initialize_gcs_client(GCS_BUCKET_NAME)

# Initialize Speechify client
client = Speechify(token=SPEECHIFY_API_KEY)

def get_voices_data():
    """
    Fetch available voices from Speechify API and return them in a format
    compatible with the existing interface.
    """
    try:
        # Get all voices from Speechify
        voices_response = client.tts.voices.list()
        
        # Create a dictionary mapping voice names to voice IDs
        voices_data = {}
        for voice in voices_response:
            # Use the voice name as the key and voice ID as the value
            voices_data[voice.name.lower()] = voice.id
        
        return voices_data, None

    except Exception as e:
        print(f"Error fetching Speechify voices: {str(e)}")
        return None, "An internal error has occurred. Please try again later."


def get_voice_id(voice_name):
    """
    Get the voice ID for a given voice name.
    """
    voices_data, error = get_voices_data()
    if error:
        return None, error
    
    voice_id = voices_data.get(voice_name.lower())
    if not voice_id:
        return None, f"Voice {voice_name} not found."
    
    return voice_id, None


def text_to_speech(prompt, voice_name):
    """
    Convert text to speech using Speechify API.
    
    Args:
        prompt (str): The text to convert to speech
        voice_name (str): The name of the voice to use
    
    Returns:
        tuple: (audio_url, error) - audio_url is the public URL to the audio file, error is None if successful
    """
    try:
        # Get the voice ID for the given voice name
        voice_id, error = get_voice_id(voice_name)
        if error:
            return None, error

        # Call Speechify TTS API
        response = client.tts.audio.speech(
            audio_format="mp3",
            input=prompt,
            language="en-US",
            model="simba-english",
            options=GetSpeechOptionsRequest(
                loudness_normalization=False,
                text_normalization=True
            ),
            voice_id=voice_id
        )

        # The response contains base64 encoded audio data
        if hasattr(response, 'audio_data') and response.audio_data:
            # Decode the base64 audio data
            audio_data = base64.b64decode(response.audio_data)
            
            # Generate a unique filename for the audio
            file_name = f"tts_{uuid.uuid4()}.mp3"

            # Upload to Google Cloud Storage
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(file_name)
            blob.upload_from_string(audio_data, content_type="audio/mpeg")

            # Set the blob to be publicly readable
            blob.make_public()

            # Return the blob's public URL
            return blob.public_url, None
        else:
            return None, "No audio data received from Speechify API"

    except Exception as e:
        print(f"Error in Speechify TTS: {str(e)}")
        return None, f"Error generating audio: {str(e)}"


def filter_voice_models(voices, *, gender=None, locale=None, tags=None):
    """
    Filter Speechify voices by gender, locale, and/or tags,
    and return the list of model IDs for matching voices.

    Args:
        voices (list): List of GetVoice objects.
        gender (str, optional): e.g. 'male', 'female'.
        locale (str, optional): e.g. 'en-US'.
        tags (list, optional): list of tags, e.g. ['timbre:deep', 'use-case:advertisement'].

    Returns:
        list[str]: IDs of matching voice models.
    """
    results = []

    for voice in voices:
        # gender filter
        if gender and voice.gender.lower() != gender.lower():
            continue

        # locale filter (check across models and languages)
        if locale:
            if not any(
                any(lang.locale == locale for lang in model.languages)
                for model in voice.models
            ):
                continue

        # tags filter
        if tags:
            if not all(tag in voice.tags for tag in tags):
                continue

        # If we got here, the voice matches -> collect model ids
        results.append(voice.id)

    return results 