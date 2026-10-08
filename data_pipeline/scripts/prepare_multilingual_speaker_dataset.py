from datasets import load_dataset, Audio
from collections import defaultdict
from pathlib import Path
import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

LANGUAGES = {
    "bengali": "bn",
    "tamil": "ta"
}

SPEAKERS_NEEDED = 5
RECORDINGS_PER_SPEAKER = 3

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "raw"
METADATA_DIR = BASE_DIR / "metadata"

METADATA_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Process each language
# --------------------------------------------------

all_metadata = []


for language, lang_code in LANGUAGES.items():

    print("\n" + "=" * 60)
    print(f"Processing language: {language}")
    print("=" * 60)

    output_dir = RAW_DIR / lang_code
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading dataset...")

    dataset = load_dataset(
        "ai4bharat/IndicVoices",
        language,
        split="valid",
        streaming=True
    )

    # Avoid TorchCodec decoding
    dataset = dataset.cast_column(
        "audio_filepath",
        Audio(decode=False)
    )

    # speaker_id -> list of samples
    speaker_samples = defaultdict(list)

    selected_speakers = set()

    print("Searching for 5 speakers with 3 recordings each...")

    for sample in dataset:

        speaker_id = sample["speaker_id"]

        # Ignore speakers already selected
        if speaker_id in selected_speakers:
            continue

        # Collect recordings for this speaker
        speaker_samples[speaker_id].append(sample)

        # Once speaker has 3 recordings, select them
        if len(speaker_samples[speaker_id]) == RECORDINGS_PER_SPEAKER:

            selected_speakers.add(speaker_id)

            print(
                f"Selected speaker {len(selected_speakers)}/{SPEAKERS_NEEDED}: "
                f"{speaker_id}"
            )

            if len(selected_speakers) == SPEAKERS_NEEDED:
                break

    # --------------------------------------------------
    # Save selected recordings
    # --------------------------------------------------

    recording_number = 1

    for speaker_id in selected_speakers:

        samples = speaker_samples[speaker_id]

        for sample in samples:

            audio = sample["audio_filepath"]

            audio_bytes = audio["bytes"]

            filename = (
                f"{lang_code}_"
                f"{recording_number:03d}_"
                f"{speaker_id}.flac"
            )

            output_path = output_dir / filename

            with open(output_path, "wb") as f:
                f.write(audio_bytes)

            all_metadata.append({
                "audio_filepath": str(output_path),
                "speaker_id": speaker_id,
                "language": language,
                "duration": sample.get("duration"),
                "text": sample.get("text")
            })

            recording_number += 1

    print(f"\n{language} completed.")
    print(f"Speakers selected: {len(selected_speakers)}")
    print(f"Recordings saved: {recording_number - 1}")


# --------------------------------------------------
# Save metadata
# --------------------------------------------------

metadata_path = (
    METADATA_DIR /
    "multilingual_speaker_dataset.csv"
)

df = pd.DataFrame(all_metadata)

df.to_csv(
    metadata_path,
    index=False
)

print("\n" + "=" * 60)
print("MULTILINGUAL DATASET PREPARATION COMPLETED")
print("=" * 60)

print(f"\nTotal recordings added: {len(df)}")
print(f"Metadata saved to:")
print(metadata_path)

print("\nRecordings per language:")
print(df["language"].value_counts())

print("\nSpeakers per language:")
print(
    df.groupby("language")["speaker_id"]
    .nunique()
)

print("\nRecordings per speaker:")
print(
    df.groupby(["language", "speaker_id"])
    .size()
)