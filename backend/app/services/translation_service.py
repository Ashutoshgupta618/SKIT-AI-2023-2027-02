import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/nllb-200-distilled-600M"

# All planned VOCAL-X languages
LANGUAGE_CODES = {
    "English": "eng_Latn",
    "Hindi": "hin_Deva",
    "Bengali": "ben_Beng",
    "Gujarati": "guj_Gujr",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva",
    "Odia": "ory_Orya",
    "Punjabi": "pan_Guru",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu"
}

print("Loading NLLB translation model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = "mps" if torch.backends.mps.is_available() else "cpu"
model = model.to(device)

print(f"NLLB model loaded successfully on {device}!")


def translate_text(text: str, source_language: str, target_language: str) -> str:

    if source_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported source language")

    if target_language not in LANGUAGE_CODES:
        raise ValueError("Unsupported target language")

    if not text.strip():
        return ""

    tokenizer.src_lang = LANGUAGE_CODES[source_language]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True
    ).to(device)

    target_code = tokenizer.convert_tokens_to_ids(
        LANGUAGE_CODES[target_language]
    )

    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=target_code,
            max_length=256
        )

    return tokenizer.batch_decode(
        generated_tokens,
        skip_special_tokens=True
    )[0]