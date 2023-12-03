import sys
import csv
import os
import base64
import time
import datetime
import requests
from asterisk.agi import AGI
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from openai import OpenAI

def record_and_transcribe(agi, language, sample_rate, credentials_path, wav_file):
    # Play the WAV file if specified
    if wav_file:
        agi.stream_file(wav_file)

    # Start recording the caller's response
    agi.record_file("caller_response", "wav", escape_digits="", timeout=10000)  # 10 seconds timeout
    file_path = "/path/to/caller_response.wav"  # Update with actual path

    # Load the audio into memory
    with open(file_path, 'rb') as audio_file:
        audio_content = audio_file.read()

    # Transcribe the audio file
    client = speech.SpeechClient.from_service_account_json(credentials_path)
    audio = types.RecognitionAudio(content=audio_content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language,
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    return response.results[0].alternatives[0].transcript if response.results else ""

def check_ivr_response(ivr_response, allowed_responses):
    # Load API key from an environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    # Create the thread
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "system",
                "content": "You are an assistant named 'IVR assistant level one'. Your task is to validate IVR responses against a list of allowed phrases and determine if they match closely enough."
            },
            {
                "role": "user",
                "content": f"IVR response: '{ivr_response}'. Allowed responses are: {', '.join(allowed_responses)}."
            }
        ]
    )

    # Retrieve the assistant ID for 'IVR assistant level one'
    assistant_id = "your_assistant_id"  # Replace with actual assistant ID

    # Run the thread with the assistant
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Get the last message, which should be the response
        response = run.messages[-1]['content']
        return response.strip()

    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_speech_with_elevenlabs(text, xi_api_key, voice_id="default_voice_id"):
    url = "https://api.elevenlabs.io/v1/text-to-speech/{}".format(voice_id)
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": xi_api_key
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open('response_audio.mp3', 'wb') as f:
            f.write(response.content)
        return 'response_audio.mp3'
    return None

def main():
    agi = AGI()

    # Configuration Variables
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = '/path/to/your/credentials.json'
    XI_API_KEY = "your_elevenlabs_api_key"
    LANGUAGE = 'en-US'
    SAMPLE_RATE = 8000
    WAV_FILE = "welcome_message.wav"  # Update with actual WAV file path

    try:
        # Record the audio and transcribe
        transcribed_text = record_and_transcribe(agi, LANGUAGE, SAMPLE_RATE, GOOGLE_CLOUD_SPEECH_CREDENTIALS, WAV_FILE)
        agi.verbose("Transcribed Text: " + transcribed_text)

        # Analyze intent with OpenAI
        intent_or_question = check_ivr_response(transcribed_text, ["pass_to_agent", "book_an_engineer", "make_a_complaint", "cancel_appointment", "default_dropout"])

        if intent_or_question.startswith("!"):
            # Handle clarifying question
            clarifying_question = intent_or_question[1:]  # Remove '!' from the beginning
            speech_file = generate_speech_with_elevenlabs(clarifying_question, XI_API_KEY)  # Generate speech for the clarifying question
            if speech_file:
                agi.stream_file(speech_file.replace('.mp3', ''))  # Play the clarifying question

            # Record and analyze response to the clarifying question
            follow_up_text = record_and_transcribe(agi, LANGUAGE, SAMPLE_RATE, GOOGLE_CLOUD_SPEECH_CREDENTIALS, None)
            intent = check_ivr_response(follow_up_text, ["pass_to_agent", "book_an_engineer", "make_a_complaint", "cancel_appointment", "default_dropout"])
        else:
            intent = intent_or_question  # Directly use the intent if no clarifying question

        # Route call based on intent
        if intent in ["pass_to_agent", "book_an_engineer", "make_a_complaint", "cancel_appointment", "default_dropout"]:
            agi.set_extension("101")  # Route to extension 101

    except Exception as e:
        agi.verbose("Error: " + str(e))

    finally:
        agi.hangup()

if __name__ == "__main__":
    main()
