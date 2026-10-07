
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

TRANSLATION_MODEL = (
    "facebook/nllb-200-distilled-600M"
)

tokenizer = AutoTokenizer.from_pretrained(
    TRANSLATION_MODEL
)

translation_model = AutoModelForSeq2SeqLM.from_pretrained(
    TRANSLATION_MODEL
)

print(
    "Translation model loaded successfully."
)

LANGUAGE_CODES = {

    "Hindi": "hin_Deva",

    "Bengali": "ben_Beng",

    "Gujarati": "guj_Gujr",

    "Kannada": "kan_Knda",

    "Malayalam": "mal_Mlym",

    "Marathi": "mar_Deva",

    "Punjabi": "pan_Guru",

    "Tamil": "tam_Taml",

    "Telugu": "tel_Telu",

    "Urdu": "urd_Arab",

    "English": "eng_Latn"
}

TARGET_LANGUAGE = "eng_Latn"

print(
    "Target language:",
    TARGET_LANGUAGE
)

# initial use eng . as target after finish aadd more

def translate_to_english(
    text,
    source_language
):

    if not text:
        return ""

    if source_language not in LANGUAGE_CODES:
        return ""

    source_code = LANGUAGE_CODES[
        source_language
    ]

    try:

        tokenizer.src_lang = source_code

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        translated_tokens = (
            translation_model.generate(
                **inputs,
                forced_bos_token_id=
                tokenizer.convert_tokens_to_ids(
                    TARGET_LANGUAGE
                ),
                max_length=512
            )
        )

        translated_text = (
            tokenizer.batch_decode(
                translated_tokens,
                skip_special_tokens=True
            )[0]
        )

        return translated_text

    except Exception as e:

        print(
            "Translation error:",
            e
        )

        return ""

translation_results = []

for _, row in tqdm(
    asr_df.iterrows(),
    total=len(asr_df),
    desc="Translating"
):

    transcription = row["transcription"]

    source_language = (
        row["original_language"]
    )

    translated_text = translate_to_english(
        transcription,
        source_language
    )

    translation_results.append({

        "id": row["id"],

        "audio_file":
            row["audio_file"],

        "source_language":
            source_language,

        "detected_language":
            row["detected_language"],

        "original_text":
            transcription,

        "translated_text":
            translated_text,

        "asr_status":
            row["status"]
    })


translation_df = pd.DataFrame(
    translation_results
)

display(
    translation_df.head(20)
)

translation_output = (
    METADATA_DIR /
    "translation_results.csv"
)

translation_df.to_csv(
    translation_output,
    index=False
)

print(
    "Translation results saved to:",
    translation_output
)

print("=" * 60)
print("SPEECH-TO-TEXT & TRANSLATION PIPELINE SUMMARY")
print("=" * 60)

print(
    "\nTotal processed audio:",
    len(processed_df)
)

print(
    "Audio tested for ASR:",
    len(asr_df)
)

print(
    "Successful ASR:",
    (asr_df["status"] == "success").sum()
)

print(
    "Failed ASR:",
    (asr_df["status"] != "success").sum()
)

print(
    "Translation records:",
    len(translation_df)
)

print("\nFiles generated:")

print(
    "- asr_results.csv"
)

print(
    "- translation_results.csv"
)
