import os
import tempfile

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.speech_service import transcribe_audio

router = APIRouter(prefix="/api/voice", tags=["Voice Translation"])


LANGUAGE_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu"
}


@router.post("/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: str = Form(...)
):
    if language not in LANGUAGE_CODES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported language"
        )

    suffix = os.path.splitext(audio.filename or "")[1] or ".webm"
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:
            temp_path = temp_file.name
            content = await audio.read()
            temp_file.write(content)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Empty audio file"
            )

        text = transcribe_audio(
            temp_path,
            language=LANGUAGE_CODES[language]
        )

        return {
            "recognized_text": text,
            "language": language
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Speech recognition failed: {str(error)}"
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)