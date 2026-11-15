from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.translation_service import translate_text

router = APIRouter(
    prefix="/api/translation",
    tags=["Text Translation"]
)


class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


@router.post("/translate")
def translate(data: TranslationRequest):

    if data.source_language == data.target_language:
        return {
            "translated_text": data.text,
            "source_language": data.source_language,
            "target_language": data.target_language
        }

    try:
        translated_text = translate_text(
            data.text,
            data.source_language,
            data.target_language
        )

        return {
            "translated_text": translated_text,
            "source_language": data.source_language,
            "target_language": data.target_language
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))