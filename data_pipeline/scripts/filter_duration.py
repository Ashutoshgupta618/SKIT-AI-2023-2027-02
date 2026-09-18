from pathlib import Path
import wave

from dataset_config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MIN_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
)


def get_audio_duration(file_path):
    with wave.open(str(file_path), "rb") as audio:
        sample_rate = audio.getframerate()
        frames = audio.getnframes()

        if sample_rate == 0:
            return 0.0

        return frames / sample_rate


def filter_audio_dataset():
    raw_path = Path(RAW_DATA_DIR)
    processed_path = Path(PROCESSED_DATA_DIR)

    audio_files = [
        path
        for path in raw_path.rglob("*.wav")
        if path.is_file()
    ]

    accepted_count = 0
    rejected_count = 0

    for input_file in audio_files:
        try:
            duration = get_audio_duration(input_file)

            if (
                MIN_DURATION_SECONDS
                <= duration
                <= MAX_DURATION_SECONDS
            ):
                relative_path = input_file.relative_to(raw_path)
                output_file = processed_path / relative_path

                output_file.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                output_file.write_bytes(
                    input_file.read_bytes()
                )

                accepted_count += 1

            else:
                rejected_count += 1
                print(
                    f"Rejected: {input_file} "
                    f"({duration:.2f}s)"
                )

        except (wave.Error, OSError) as error:
            rejected_count += 1
            print(f"Unable to process: {input_file}")
            print(f"  Reason: {error}")

    print("\nDuration Filtering Summary")
    print("=" * 32)
    print(f"Files found     : {len(audio_files)}")
    print(f"Accepted files  : {accepted_count}")
    print(f"Rejected files  : {rejected_count}")
    print(
        f"Allowed range   : "
        f"{MIN_DURATION_SECONDS}s - {MAX_DURATION_SECONDS}s"
    )


if __name__ == "__main__":
    filter_audio_dataset()