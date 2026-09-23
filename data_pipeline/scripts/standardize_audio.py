from pathlib import Path
import wave

from dataset_config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    TARGET_SAMPLE_RATE,
    TARGET_CHANNELS,
)


def standardize_wav_file(input_path, output_path):
    """
    Convert a WAV file to the project's standard audio format.

    Target format:
    - Sample rate: 16 kHz
    - Channels: Mono
    - Sample width: 16-bit PCM
    """

    try:
        with wave.open(str(input_path), "rb") as source:
            sample_width = source.getsampwidth()
            sample_rate = source.getframerate()
            channels = source.getnchannels()
            frames = source.readframes(source.getnframes())

        # This module currently handles PCM WAV files.
        if sample_width != 2:
            return False, "Unsupported sample width"

        if sample_rate == TARGET_SAMPLE_RATE and channels == TARGET_CHANNELS:
            converted_frames = frames

        else:
            return False, (
                f"Conversion required: {sample_rate} Hz, "
                f"{channels} channel(s)"
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with wave.open(str(output_path), "wb") as output:
            output.setnchannels(TARGET_CHANNELS)
            output.setsampwidth(2)
            output.setframerate(TARGET_SAMPLE_RATE)
            output.writeframes(converted_frames)

        return True, "Standardized successfully"

    except (wave.Error, OSError) as error:
        return False, f"Processing failed: {error}"


def standardize_audio_dataset():
    raw_path = Path(RAW_DATA_DIR)
    processed_path = Path(PROCESSED_DATA_DIR)

    audio_files = [
        path
        for path in raw_path.rglob("*.wav")
        if path.is_file()
    ]

    processed_count = 0
    skipped_count = 0

    for input_file in audio_files:
        relative_path = input_file.relative_to(raw_path)
        output_file = processed_path / relative_path

        success, message = standardize_wav_file(
            input_file,
            output_file
        )

        if success:
            processed_count += 1
        else:
            skipped_count += 1
            print(f"Skipped: {input_file}")
            print(f"  Reason: {message}")

    print("\nAudio Standardization Summary")
    print("=" * 35)
    print(f"Files found      : {len(audio_files)}")
    print(f"Processed files  : {processed_count}")
    print(f"Skipped files    : {skipped_count}")


if __name__ == "__main__":
    standardize_audio_dataset()