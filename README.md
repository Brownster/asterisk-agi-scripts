Asterisk AGI Script for IVR Testing

This script is designed to test the functionality of Interactive Voice Response (IVR) systems by capturing audio from the call, transcribing it using Google Cloud Speech-to-Text, and checking if the transcribed response matches a list of allowed responses. The script also records the entire call using Asterisk's MixMonitor() application.

Prerequisites:

    Asterisk PBX
    Google Cloud Speech-to-Text credentials
    Python 3 with asterisk.agi installed

Installation:

    Copy the script files (main.py, record_and_transcribe.py, read_allowed_responses.py) to your Asterisk AGI directory (usually /var/lib/asterisk/agi-bin).

    Install the asterisk.agi Python module:

Bash

pip install asterisk.agi

Use code with caution. Learn more

    Create a CSV file named allowed_responses.csv and list the allowed responses in each row.

    Update the GOOGLE_CLOUD_SPEECH_CREDENTIALS variable in the main.py script with the path to your Google Cloud Speech-to-Text JSON credentials file.

    Update the LANGUAGE and SAMPLE_RATE variables in the main.py script with the desired language code and sample rate for speech recognition.

    Ensure that call recording is enabled in Asterisk.

Usage:
Example Dialplan:

[default]
exten => s,1,Answer()
 same => n,Wait(1)
 same => n,AGI(ivr_test_script.py,102,5,testprompt.wav,allowed_responses.csv)
 same => n,Hangup()

Breakdown:

    Context: [default]
        This is the context name. You might need to change this to match the context used in your Asterisk setup.

    Extension and Priority: exten => s,1,Answer()
        This line answers the call. The s extension is used for calls that don't have a specific dialed number. Adjust this according to your dialplan requirements.

    Wait: same => n,Wait(1)
        This line adds a 1-second pause after answering the call. This is often useful to ensure the call is fully established before proceeding.

    Invoke AGI Script: same => n,AGI(ivr_test_script.py,102,5,testprompt.wav,allowed_responses.csv)
        This line calls your AGI script with the required arguments: the number to dial (102), the time to wait before recording (5 seconds), the name of the WAV file (testprompt.wav), and the name of the CSV file containing allowed responses (allowed_responses.csv).

    Hangup: same => n,Hangup()
        This line hangs up the call after the AGI script has finished executing.

Important Notes:

    Script Permissions: Ensure that ivr_test_script.py is executable and accessible by the Asterisk process. You may need to set the appropriate permissions using chmod.

    Script Path: Verify that the path to your AGI script is correct. The default path for AGI scripts in Asterisk is usually /var/lib/asterisk/agi-bin/, but this can vary based on your Asterisk configuration.

    File Locations: Make sure that the WAV file (testprompt.wav) and the CSV file (allowed_responses.csv) are accessible by the script and are located in the correct directories.

    Testing: Test the dial plan thoroughly in a controlled environment to ensure that it works as expected and that the AGI script is invoked correctly.

    Context Name: The context name [default] is just an example. You will need to adjust this to fit into your existing dial plan structure.

This example provides a basic structure for your dial plan. Depending on the complexity of your Asterisk setup, you may need to make additional adjustments or add more logic to handle different scenarios.

    Restart Asterisk for the changes to take effect.

    Make a call to the extension number configured in your dialplan.

Testing:

    Verify that the script is capturing and transcribing audio correctly by reviewing the recorded audio files and corresponding transcript text.

    Ensure that the script is checking the transcribed responses against the allowed responses list and taking appropriate actions (e.g., playing a success prompt or routing to the next step).

    Validate that the entire call is being recorded using the MixMonitor() application.

Additional Notes:

    The script can be modified to handle DTMF input instead of voice input by replacing the agi.say() method with the agi.send_dtmf() method and modifying the record_and_transcribe() function accordingly.

    The call recording functionality can be integrated directly into the dialplan using the MixMonitor() application without the need for an external script.

    The script can be extended to handle more complex IVR scenarios by incorporating additional logic for branching, prompting, and routing based on user responses.
