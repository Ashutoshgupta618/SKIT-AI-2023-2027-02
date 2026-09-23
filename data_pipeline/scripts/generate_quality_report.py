from pathlib import Path
import csv
import wave
from collections import Counter

from dataset_config import (
    PROCESSED_DATA_DIR,
    REPORTS_DIR,
)


OUTPUT_FILE = Path(REPORTS_DIR) / "audio_quality_report.txt"


def inspect_audio(file_path):
    with wave.open(str(file_path), "rb") as audio:
        sample_rate = audio.getframerate()
        channels = audio.getnchannels()
        frames = audio.getnframes()

    duration = frames / sample_rate if sample_rate else 0.0

    return sample_rate, channels, duration


def generate_quality_report():
    processed_root = Path(PROCESSED_DATA_DIR)

    audio_files = [
        path
        for path in processed_root.rglob("*.wav")
        if path.is_file()
    ]

    language_counts = Counter()
    sample_rates = Counter()
    channel_counts = Counter()

    durations = []
    invalid_files = []

    for audio_file in audio_files:
        try:
            sample_rate, channels, duration = inspect_audio(audio_file)

            relative_path = audio_file.relative_to(processed_root)
            language = (
                relative_path.parts[0]
                if len(relative_path.parts) > 1
                else "unknown"
            )

            language_counts[language] += 1
            sample_rates[sample_rate] += 1
            channel_counts[channels] += 1
            durations.append(duration)

        except (wave.Error, OSError) as error:
            invalid_files.append(
                f"{audio_file}: {error}"
            )

    total_files = len(audio_files)

    if durations:
        min_duration = min(durations)
        max_duration = max(durations)
        average_duration = sum(durations) / len(durations)
        total_duration = sum(durations)
    else:
        min_duration = 0.0
        max_duration = 0.0
        average_duration = 0.0
        total_duration = 0.0

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as report:

        report.write("Vocal-X Audio Quality Report\n")
        report.write("=" * 32 + "\n\n")

        report.write("Dataset Summary\n")
        report.write("-" * 20 + "\n")
        report.write(f"Total audio files: {total_files}\n")
        report.write(
            f"Total duration: {total_duration / 3600:.2f} hours\n"
        )
        report.write(
            f"Average duration: {average_duration:.2f} seconds\n"
        )
        report.write(
            f"Minimum duration: {min_duration:.2f} seconds\n"
        )
        report.write(
            f"Maximum duration: {max_duration:.2f} seconds\n\n"
        )

        report.write("Language Distribution\n")
        report.write("-" * 24 + "\n")

        if language_counts:
            for language, count in sorted(language_counts.items()):
                report.write(f"{language}: {count}\n")
        else:
            report.write("No processed audio files found.\n")

        report.write("\nSample Rate Distribution\n")
        report.write("-" * 26 + "\n")

        if sample_rates:
            for rate, count in sorted(sample_rates.items()):
                report.write(f"{rate} Hz: {count}\n")
        else:
            report.write("No sample-rate data available.\n")

        report.write("\nChannel Distribution\n")
        report.write("-" * 22 + "\n")

        if channel_counts:
            for channels, count in sorted(channel_counts.items()):
                report.write(f"{channels} channel(s): {count}\n")
        else:
            report.write("No channel data available.\n")

        report.write("\nValidation Issues\n")
        report.write("-" * 20 + "\n")

        if invalid_files:
            for issue in invalid_files:
                report.write(f"{issue}\n")
        else:
            report.write("No invalid audio files detected.\n")

    print("\nAudio Quality Report")
    print("=" * 30)
    print(f"Files analyzed : {total_files}")
    print(f"Invalid files  : {len(invalid_files)}")
    print(f"Report saved   : {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_quality_report()