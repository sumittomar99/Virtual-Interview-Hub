import os
import openai
from gtts import gTTS
from io import BytesIO
import pygame
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_hr_response(conversation):
    """
    Generate a response from the HR interviewer using GPT-4.

    Args:
        conversation (list): The conversation history with roles and content.

    Returns:
        str: The HR interviewer's response.
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # Use the appropriate model name
        messages=conversation,
        max_tokens=150,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].message.content

def speak_text_gtts(text):
    """
    Convert text to speech and play it immediately.

    Args:
        text (str): The text to convert to speech.
    """
    tts = gTTS(text)
    audio_fp = BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(audio_fp)
    pygame.mixer.music.play()

    # Wait until the audio is done playing
    while pygame.mixer.music.get_busy():
        continue


def speak_text(text):
    """
    Convert text to speech and play it immediately.

    Args:
        text (str): The text to convert to speech.
    """
    # Generate speech using OpenAI's API
    response = openai.audio.speech.create(
        model="tts-1",  # Replace with the actual TTS model name if different
        voice="shimmer",  # Replace with the actual voice if different
        input=text
    )

    # Read the audio data into a BytesIO object
    audio_fp = BytesIO(response.read())


    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load(audio_fp)
    pygame.mixer.music.play()

    # Wait until the audio is done playing
    while pygame.mixer.music.get_busy():
        continue