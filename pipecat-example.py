import requests
import wave
import pyaudio
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
API_KEY = os.getenv('CARTESIA_API_KEY')

# Correct Cartesia TTS API URL
CARTESIA_TTS_API_URL = "https://api.cartesia.ai/tts/bytes"

# Hardcoded text for testing
HARD_CODED_TEXT = "Hey, muppet, what kind music are we listening to?!"

# Function to send text to Cartesia's TTS API and get synthesized audio
def text_to_speech(text):
    headers = {
        'X-API-Key': API_KEY,  # Updated header with X-API-Key
        'Content-Type': 'application/json',
        'Cartesia-Version': '2024-06-10'
    }
    data = {
        'transcript': text,
        'model_id': 'sonic-english',  # Updated model ID
        'voice': {
            'mode': 'id',
            'id': '1df86052-512c-4d8e-b933-f955b27f7f42'  # Updated voice ID
        },
        'output_format': {
            'container': 'wav',
            'encoding': 'pcm_s16le',  # Simpler format
            'sample_rate': 44100
        }
    }
    
    response = requests.post(CARTESIA_TTS_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        # Save the audio file from the TTS response
        with open("response.wav", 'wb') as f:
            f.write(response.content)
        print("Response speech saved to response.wav")
        play_audio("response.wav")
    else:
        print(f"Error in text-to-speech: {response.status_code} - {response.text}")

# Function to play the audio file
def play_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    audio = pyaudio.PyAudio()

    # Open stream to play the audio
    stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

    # Read and play the audio
    data = wf.readframes(chunk)
    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    # Close the stream
    stream.close()
    audio.terminate()

# Main function to handle the hardcoded text-to-audio flow
def generate_and_send_to_robot():
    # Hardcoded Text: "Welcome to Cartesia Sonic, you absolyute!"
    print("Hardcoded Text:", HARD_CODED_TEXT)
    
    # Convert hardcoded text to speech using Cartesia
    text_to_speech(HARD_CODED_TEXT)
    
# Example test call
if __name__ == "__main__":
    generate_and_send_to_robot()
