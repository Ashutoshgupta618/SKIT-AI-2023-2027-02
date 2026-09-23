from pathlib import Path
import wave

from dataset_config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    MIN_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
)


SEGMENT_DURATION_SECONDS = 10.0


def segment_wav_file(input_path, output_directory):
    try:
        with wave.open(str(input_path), "rb") as audio:
            params = audio.getparams()
            frames = audio.readframes(audio.getnframes())

        sample_rate = params.framerate
        total_frames = len(frames) // params.sampwidth

        segment_frames = int(
            SEGMENT_DURATION_SECONDS * sample_rate
        )

        if segment_frames <= 0:
            return 0

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        segment_count = 0

        for start in range(0, total_frames, segment_frames):
            end = min(
                start + segment_frames,
                total_frames
            )

            duration = (end - start) / sample_rate

            # Ignore segments that are too short.
            if duration < MIN_DURATION_SECONDS:
                continue

            segment_data = frames[
                start * params.sampwidth:
                end * params.sampwidth
            ]

            output_file = (
                output_directory
                / f"{input_path.stem}_segment_{segment_count:04d}.wav"
            )

            with wave.open(str(output_file), "wb") as segment:
                segment.setparams(params)
                segment.writeframes(segment_data)

            segment_count += 1

        return segment_count

    except (wave.Error, OSError, ValueError) as error:
        print(f"Failed: {input_path}")
        print(f"  Reason: {error}")
        return 0


def segment_speech_dataset():
    raw_path = Path(RAW_DATA_DIR)
    processed_path = Path(PROCESSED_DATA_DIR)

    audio_files = [
        path
        for path in raw_path.rglob("*.wav")
        if path.is_file()
    ]

    total_segments = 0

    for input_file in audio_files:
        relative_parent = input_file.parent.relative_to(raw_path)

        output_directory = (
            processed_path
            / relative_parent
            / input_file.stem
        )

        segments = segment_wav_file(
            input_file,
            output_directory
        )

        total_segments += segments

    print("\nSpeech Segmentation Summary")
    print("=" * 32)
    print(f"Files found      : {len(audio_files)}")
    print(f"Segments created : {total_segments}")


if __name__ == "__main__":
    segment_speech_dataset()