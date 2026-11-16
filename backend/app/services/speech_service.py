import whisper
import os

# Load Whisper model once when the backend starts
MODEL_NAME = "base"

model = whisper.load_model(MODEL_NAME)


def transcribe_audio(audio_path: str, language: str = None) -> str:
    """
    Convert recorded audio into text using Whisper.
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError("Audio file not found")

    options = {}

    if language:
        options["language"] = language

    result = model.transcribe(
        audio_path,
        **options
    )

    return result["text"].strip()