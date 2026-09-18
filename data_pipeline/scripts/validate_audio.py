from pathlib import Path
import wave

from dataset_config import (
    RAW_DATA_DIR,
    MIN_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
    TARGET_SAMPLE_RATE,
    TARGET_CHANNELS,
)


SUPPORTED_EXTENSIONS = {".wav"}


def validate_wav_file(file_path):
    result = {
        "file": str(file_path),
        "valid": True,
        "issues": [],
    }

    try:
        with wave.open(str(file_path), "rb") as audio:
            sample_rate = audio.getframerate()
            channels = audio.getnchannels()
            frames = audio.getnframes()

            duration = frames / sample_rate if sample_rate else 0

            if sample_rate != TARGET_SAMPLE_RATE:
                result["valid"] = False
                result["issues"].append(
                    f"Invalid sample rate: {sample_rate} Hz"
                )

            if channels != TARGET_CHANNELS:
                result["valid"] = False
                result["issues"].append(
                    f"Invalid channels: {channels}"
                )

            if not (
                MIN_DURATION_SECONDS
                <= duration
                <= MAX_DURATION_SECONDS
            ):
                result["valid"] = False
                result["issues"].append(
                    f"Invalid duration: {duration:.2f}s"
                )

    except (wave.Error, OSError) as error:
        result["valid"] = False
        result["issues"].append(f"Unreadable audio: {error}")

    return result


def validate_audio_dataset():
    raw_data_path = Path(RAW_DATA_DIR)

    audio_files = [
        path
        for path in raw_data_path.rglob("*")
            if path.is_file()
            and path.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    valid_count = 0
    invalid_count = 0

    for audio_file in audio_files:
        result = validate_wav_file(audio_file)

        if result["valid"]:
            valid_count += 1
        else:
            invalid_count += 1
            print(f"\nInvalid: {audio_file}")

            for issue in result["issues"]:
                print(f"  - {issue}")

    print("\nAudio Validation Summary")
    print("=" * 30)
    print(f"Files scanned : {len(audio_files)}")
    print(f"Valid files   : {valid_count}")
    print(f"Invalid files : {invalid_count}")


if __name__ == "__main__":
    validate_audio_dataset()