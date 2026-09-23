from pathlib import Path
import wave
import csv


RAW_DATA_DIR = Path("data_pipeline/raw")
OUTPUT_FILE = Path("data_pipeline/metadata/audio_metadata.csv")

SUPPORTED_EXTENSIONS = {".wav"}


def extract_wav_metadata(file_path):
    with wave.open(str(file_path), "rb") as audio:

        channels = audio.getnchannels()
        sample_rate = audio.getframerate()
        frames = audio.getnframes()
        duration = frames / sample_rate if sample_rate else 0

    return {
        "file_name": file_path.name,
        "file_path": str(file_path),
        "format": file_path.suffix.lower(),
        "duration_seconds": round(duration, 3),
        "sample_rate": sample_rate,
        "channels": channels,
    }


def collect_audio_metadata():
    records = []

    audio_files = [
        path
        for path in RAW_DATA_DIR.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    for audio_file in audio_files:
        try:
            records.append(extract_wav_metadata(audio_file))
        except Exception as error:
            print(f"Could not process {audio_file}: {error}")

    return records


def save_metadata(records):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file_name",
        "file_path",
        "format",
        "duration_seconds",
        "sample_rate",
        "channels",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


if __name__ == "__main__":
    metadata = collect_audio_metadata()
    save_metadata(metadata)

    print(f"Audio files scanned : {len(metadata)}")
    print(f"Metadata saved to   : {OUTPUT_FILE}")