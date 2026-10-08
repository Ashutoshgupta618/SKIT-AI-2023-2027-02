from datasets import load_dataset, Audio
from pathlib import Path
import csv


# =========================
# Configuration
# =========================

DATASET_NAME = "ai4bharat/IndicVoices"
LANGUAGE_CONFIG = "hindi"
LANGUAGE_CODE = "hi"

MAX_SPEAKERS = 5
RECORDINGS_PER_SPEAKER = 3


# =========================
# Project paths
# =========================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data_pipeline" / "raw" / LANGUAGE_CODE
METADATA_DIR = PROJECT_ROOT / "data_pipeline" / "metadata"

RAW_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_CSV = METADATA_DIR / "speaker_dataset.csv"


# =========================
# Load dataset
# =========================

print("Loading IndicVoices Hindi dataset...")

dataset = load_dataset(
    DATASET_NAME,
    LANGUAGE_CONFIG,
    split="train",
    streaming=True
)

# Do NOT decode audio using TorchCodec.
dataset = dataset.cast_column(
    "audio_filepath",
    Audio(decode=False)
)

print("Dataset loaded.")
print(f"Selecting {MAX_SPEAKERS} speakers × {RECORDINGS_PER_SPEAKER} recordings...\n")


# =========================
# Select speakers
# =========================

selected = {}

for sample in dataset:

    speaker_id = sample["speaker_id"]

    # Add a new speaker until we have 5 speakers
    if speaker_id not in selected:

        if len(selected) >= MAX_SPEAKERS:
            continue

        selected[speaker_id] = []

    # Already have enough recordings for this speaker
    if len(selected[speaker_id]) >= RECORDINGS_PER_SPEAKER:
        continue

    selected[speaker_id].append(sample)

    print(
        f"Speaker {speaker_id}: "
        f"{len(selected[speaker_id])}/{RECORDINGS_PER_SPEAKER}"
    )

    # Stop once 5 speakers have 3 recordings each
    if (
        len(selected) == MAX_SPEAKERS
        and all(
            len(records) == RECORDINGS_PER_SPEAKER
            for records in selected.values()
        )
    ):
        break


# =========================
# Save audio files
# =========================

print("\nSaving audio files...")

rows = []
counter = 1

for speaker_id, records in selected.items():

    for sample in records:

        audio = sample["audio_filepath"]
        audio_bytes = audio["bytes"]

        if audio_bytes is None:
            print(f"Skipping {speaker_id}: audio bytes unavailable.")
            continue

        filename = f"{LANGUAGE_CODE}_{counter:03d}_{speaker_id}.flac"

        output_path = RAW_DIR / filename

        output_path.write_bytes(audio_bytes)

        rows.append({
            "audio_filepath": str(
                Path("data_pipeline") / "raw" / LANGUAGE_CODE / filename
            ),
            "speaker_id": speaker_id,
            "language": LANGUAGE_CODE,
            "duration": sample.get("duration"),
            "text": sample.get("text")
        })

        print(f"Saved: {filename}")

        counter += 1


# =========================
# Save metadata CSV
# =========================

with open(
    OUTPUT_CSV,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "audio_filepath",
            "speaker_id",
            "language",
            "duration",
            "text"
        ]
    )

    writer.writeheader()
    writer.writerows(rows)


# =========================
# Final summary
# =========================

print("\n===================================")
print("Speaker dataset preparation complete")
print("===================================")

print(f"Speakers selected : {len(selected)}")
print(f"Audio files saved : {len(rows)}")
print(f"Audio directory   : {RAW_DIR}")
print(f"Metadata file     : {OUTPUT_CSV}")