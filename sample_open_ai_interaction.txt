IVR System with OpenAI and Eleven Labs Integration

This Interactive Voice Response (IVR) system is designed to handle incoming calls, transcribe responses, analyze caller intent using OpenAI, and generate speech responses with Eleven Labs' Text-to-Speech API. It routes calls to different hunt groups based on the identified intent.
Features

    Voice Response Playback: Plays pre-recorded messages to callers.
    Speech-to-Text: Transcribes caller responses using Google Cloud Speech-to-Text.
    Intent Analysis: Analyzes caller intent with OpenAI's language model.
    Text-to-Speech: Converts text responses into speech using Eleven Labs' API.
    Dynamic Call Routing: Routes calls to designated hunt groups based on the identified intent.

Prerequisites

    Asterisk server with AGI (Asterisk Gateway Interface) enabled.
    Google Cloud account with Speech-to-Text API access.
    OpenAI API access with necessary permissions.
    Eleven Labs API access.
    Python environment with required libraries installed.

Installation

    Clone the Repository: Clone or download this repository to your Asterisk server.

    bash

git clone https://github.com/Brownster/asterisk-agi-scripts/

Install Dependencies: Install the required Python libraries.

    pip install requests google-cloud-speech openai

    API Keys and Credentials: Set up the necessary API keys and credentials for Google Cloud, OpenAI, and Eleven Labs.
        Google Cloud Speech-to-Text credentials JSON file.
        OpenAI API key.
        Eleven Labs API key.

    Store these credentials securely and update the script with the paths or variables as required.

    Configure Audio Files: Place your pre-recorded WAV files in the specified directory and update the script with the correct file paths.

Usage

    Run the Script: Execute the script on your Asterisk server.

    python ivr_script.py

    IVR Flow: The script will handle incoming calls, play the initial greeting, record responses, and transcribe them. It then analyzes the intent and routes the call accordingly.

    Monitoring and Logs: Monitor the system for performance and errors. Ensure logging is enabled for troubleshooting.

Configuration

    Update the GOOGLE_CLOUD_SPEECH_CREDENTIALS path with your Google Cloud credentials file path.
    Set the XI_API_KEY variable to your Eleven Labs API key.
    Configure the LANGUAGE and SAMPLE_RATE variables as per your requirements.
    Modify the WAV_FILE path to point to your pre-recorded greeting message.

Customization

    Modify the intent analysis and routing logic in the main() function to suit your specific IVR requirements.
    Update the list of intents and corresponding hunt group extensions as needed.

Troubleshooting

    Ensure all API keys and credentials are correctly set.
    Verify the paths to audio files and credentials.
    Check the Asterisk server and AGI configurations.
    Review logs for any error messages or anomalies.
