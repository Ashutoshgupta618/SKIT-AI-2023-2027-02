!pip install -q openai-whisper transformers sentencepiece

# ============================================================
# IMPORT LIBRARIES
# ============================================================

import whisper
import pandas as pd
from pathlib import Path
from tqdm.auto import tqdm

print("Libraries imported successfully.")

# ============================================================
# LOAD PROCESSED AUDIO METADATA
# ============================================================

METADATA_DIR = Path(PROJECT_DIR) / "metadata"
PROCESSED_DIR = Path(PROJECT_DIR) / "processed"

processed_metadata_file = (
    METADATA_DIR / "processed_metadata.csv"
)

processed_df = pd.read_csv(
    processed_metadata_file
)

print(
    "Processed dataset shape:",
    processed_df.shape
)

display(processed_df.head())


# ============================================================
# LOAD ASR MODEL
# ============================================================

model = whisper.load_model("base")

print("Whisper ASR model loaded successfully.")

# ============================================================
# SPEECH TO TEXT
# ============================================================

asr_results = []

valid_records = processed_df[
    processed_df["status"] == "valid"
]

# Initial testing
test_records = valid_records.head(20)

for _, row in tqdm(
    test_records.iterrows(),
    total=len(test_records),
    desc="Transcribing audio"
):

    audio_file = Path(row["audio_path"])

    try:

        result = model.transcribe(
            str(audio_file)
        )

        asr_results.append({

            "id": row["id"],

            "audio_file":
                audio_file.name,

            "original_language":
                row.get("language", ""),

            "detected_language":
                result.get("language", ""),

            "transcription":
                result.get("text", "").strip(),

            "status":
                "success"
        })

    except Exception as e:

        asr_results.append({

            "id": row["id"],

            "audio_file":
                audio_file.name,

            "original_language":
                row.get("language", ""),

            "detected_language":
                "",

            "transcription":
                "",

            "status":
                f"error: {e}"
        })


asr_df = pd.DataFrame(asr_results)

print(
    "ASR processing completed."
)

display(asr_df.head())

# ============================================================
# CHECK ASR RESULTS
# ============================================================

print(
    "Total audio tested:",
    len(asr_df)
)

print(
    "\nSuccessful transcriptions:",
    (asr_df["status"] == "success").sum()
)

print(
    "\nFailed transcriptions:",
    (asr_df["status"] != "success").sum()
)

display(
    asr_df[
        [
            "audio_file",
            "detected_language",
            "transcription",
            "status"
        ]
    ].head(20)
)

# ============================================================
# SAVE ASR RESULTS
# ============================================================

asr_output_file = (
    METADATA_DIR / "asr_results.csv"
)

asr_df.to_csv(
    asr_output_file,
    index=False
)

print(
    "ASR results saved to:",
    asr_output_file
)
