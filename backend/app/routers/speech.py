from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS
from io import BytesIO

router = APIRouter(
    prefix="/api/speech",
    tags=["Text to Speech"]
)

LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu"
}


class SpeechRequest(BaseModel):
    text: str
    language: str


@router.post("/generate")
def generate_speech(data: SpeechRequest):

    if not data.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

    if data.language not in LANGUAGE_CODES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported language"
        )

    try:
        audio_buffer = BytesIO()

        tts = gTTS(
            text=data.text,
            lang=LANGUAGE_CODES[data.language],
            slow=False
        )

        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return StreamingResponse(
            audio_buffer,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=translated_audio.mp3"
            }
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Audio generation failed: {str(error)}"
        )