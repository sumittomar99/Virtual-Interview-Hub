import pyaudio
import wave
from pydub import AudioSegment

# Constants
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = -50  # Silence threshold in dBFS
MIN_SILENCE_LEN = 3000  # Minimum length of silence in milliseconds

def record_audio(filename, duration=None):
    """
    Record audio from the microphone and save it to a file.

    Args:
        filename (str): The filename for the recorded audio.
        duration (int, optional): The duration of the recording in seconds. If None, will stop based on silence detection.
    """
    print("Recording...")
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    if duration:
        for _ in range(0, int(RATE / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
    else:
        silent_chunks = 0
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            # Convert chunk data to audio segment
            audio_chunk = AudioSegment(data, sample_width=p.get_sample_size(AUDIO_FORMAT), frame_rate=RATE, channels=CHANNELS)
            # Check if the chunk is silent
            if audio_chunk.dBFS < SILENCE_THRESHOLD:
                silent_chunks += 1
            else:
                silent_chunks = 0
            if silent_chunks > int((MIN_SILENCE_LEN / 1000) * (RATE / CHUNK)):
                break

    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(AUDIO_FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename, whisper_model):
    """
    Transcribe the given audio file using Whisper.

    Args:
        filename (str): The path to the audio file.
        whisper_model: The Whisper model instance.

    Returns:
        str: The transcribed text.
    """
    print("Transcribing audio...")
    result = whisper_model.transcribe(filename)
    transcription = result['text']
    print(f"\nTranscription: {transcription}")
    return transcription
