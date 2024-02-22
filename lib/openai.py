from pathlib import Path
from openai import OpenAI
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def tts(text, file_name):
    # Ensure the highlights/commentary directory exists
    base_path = Path(__file__).parent.parent / "highlights/commentary"
    base_path.mkdir(parents=True, exist_ok=True)

    # Set the path for the AAC file
    speech_file_path = base_path / f"{file_name}.mp3"

    # Generate the speech
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",  # Change to "oxyn" voice
        input=text
    )

    # Stream and save the audio in AAC format
    response.stream_to_file(speech_file_path)
