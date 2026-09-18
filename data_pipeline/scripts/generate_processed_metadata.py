from pathlib import Path
import csv
import wave

from dataset_config import (
    PROCESSED_DATA_DIR,
    METADATA_DIR,
)


OUTPUT_FILE = Path(METADATA_DIR) / "processed_metadata.csv"


def extract_metadata(file_path, processed_root):
    with wave.open(str(file_path), "rb") as audio:
        sample_rate = audio.getframerate()
        channels = audio.getnchannels()
        frames = audio.getnframes()

    duration = frames / sample_rate if sample_rate else 0.0

    relative_path = file_path.relative_to(processed_root)
    parts = relative_path.parts

    # Expected structure: language/audio_file.wav
    language = parts[0] if len(parts) > 1 else "unknown"

    return {
        "audio_id": file_path.stem,
        "language": language,
        "file_path": str(relative_path),
        "duration_seconds": round(duration, 3),
        "sample_rate": sample_rate,
        "channels": channels,
        "processing_status": "processed",
    }


def generate_metadata():
    processed_root = Path(PROCESSED_DATA_DIR)

    audio_files = [
        path
        for path in processed_root.rglob("*.wav")
        if path.is_file()
    ]

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fieldnames = [
        "audio_id",
        "language",
        "file_path",
        "duration_seconds",
        "sample_rate",
        "channels",
        "processing_status",
    ]

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        for audio_file in audio_files:
            try:
                metadata = extract_metadata(
                    audio_file,
                    processed_root
                )

                writer.writerow(metadata)

            except (wave.Error, OSError) as error:
                print(f"Skipped: {audio_file}")
                print(f"  Reason: {error}")

    print("\nProcessed Metadata Summary")
    print("=" * 34)
    print(f"Processed audio files : {len(audio_files)}")
    print(f"Metadata file         : {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_metadata()