import sys
import csv
import os
import base64
import time
import datetime
from asterisk.agi import AGI
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def check_ivr_response(ivr_response, allowed_responses):
    client = OpenAI()

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
    # This step assumes you have the assistant ID available. Replace 'your_assistant_id' with the actual ID.
    assistant_id = "your_assistant_id"

    # Run the thread with the assistant
    try:
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # Assuming the assistant responds with only "OK" or "NOK"
        response = run.messages[-1]['content']  # Get the last message, which should be the response
        return response.strip()

    except Exception as e:
        # Handle exceptions
        print(f"Error: {e}")
        return None


def read_allowed_responses(filename):
    """
    Reads allowed responses from a CSV file and returns them as a list.
    """
    allowed_responses = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            allowed_responses.append(row[0].strip())
    return allowed_responses

def check_response(response, allowed_responses):
    """
    Checks if the given response is in the list of allowed responses.
    """
    return response in allowed_responses

def record_and_transcribe(agi, language, sample_rate, credentials_path, wait_time, wav_file):
    # Wait for specified seconds before starting the recording
    time.sleep(wait_time)

    # Play the WAV file if specified
    if wav_file:
        agi.stream_file(wav_file)

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


def log_results(filename, transcribed_text, is_allowed):
    """
    Logs the results of the speech recognition and check to a CSV file.
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), transcribed_text, "OK" if is_allowed else "Not OK"])

def main():
    agi = AGI()

    # Configuration Variables
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = '/path/to/your/credentials.json'
    LANGUAGE = 'en-US'
    SAMPLE_RATE = 8000  # Adjust as needed

    # Read arguments
    if len(sys.argv) != 5:
        agi.verbose("Usage: script.py <NumberToDial> <WaitTime> <WavFileName> <AllowedResponsesFileName>")
        agi.hangup()
        return

    number_to_dial, wait_time, wav_file, allowed_responses_file = sys.argv[1:5]
    wait_time = int(wait_time)  # Convert wait time to integer

    try:
        # Record the audio and transcribe
        transcribed_text = record_and_transcribe(agi, LANGUAGE, SAMPLE_RATE, GOOGLE_CLOUD_SPEECH_CREDENTIALS, wait_time, wav_file)
        agi.verbose("Transcribed Text: " + transcribed_text)

        # Check if the response is allowed
        allowed_responses = read_allowed_responses(allowed_responses_file)
        ivr_check_result = check_ivr_response(transcribed_text, allowed_responses)

        # Interpret the result from your IVR assistant
        is_allowed = ivr_check_result == "OK"

        if is_allowed:
            agi.verbose("Response matches intent.")
        else:
            agi.verbose("Response does not match intent.")

        # Log results to a CSV file
        log_results('results_log.csv', transcribed_text, is_allowed)

        # Hang up the call
        agi.hangup()

    except Exception as e:
        agi.verbose("Error: " + str(e))
        agi.hangup()

if __name__ == "__main__":
    main()
