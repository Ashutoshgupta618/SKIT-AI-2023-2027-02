from pathlib import Path
import wave
import numpy as np

from dataset_config import RAW_DATA_DIR, PROCESSED_DATA_DIR


SILENCE_THRESHOLD = 500


def trim_silence(input_path, output_path):
    try:
        with wave.open(str(input_path), "rb") as audio:
            params = audio.getparams()
            frames = audio.readframes(audio.getnframes())

        sample_width = params.sampwidth

        if sample_width != 2:
            return False, "Only 16-bit PCM WAV files are supported"

        samples = np.frombuffer(frames, dtype=np.int16)

        if len(samples) == 0:
            return False, "Empty audio file"

        # Calculate short-time RMS energy.
        frame_size = 1024
        rms_values = []

        for start in range(0, len(samples), frame_size):
            frame = samples[start:start + frame_size]

            if len(frame) == 0:
                continue

            rms = np.sqrt(np.mean(frame.astype(np.float32) ** 2))
            rms_values.append(rms)

        if not rms_values:
            return False, "Unable to calculate audio energy"

        # Locate audio above the silence threshold.
        active_frames = [
            index
            for index, rms in enumerate(rms_values)
            if rms > SILENCE_THRESHOLD
        ]

        if not active_frames:
            return False, "Audio contains only silence"

        start_sample = active_frames[0] * frame_size
        end_sample = min(
            (active_frames[-1] + 1) * frame_size,
            len(samples)
        )

        trimmed_samples = samples[start_sample:end_sample]

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with wave.open(str(output_path), "wb") as output:
            output.setparams(params)
            output.writeframes(trimmed_samples.tobytes())

        return True, "Silence trimmed successfully"

    except (wave.Error, OSError, ValueError) as error:
        return False, f"Processing failed: {error}"

def trim_audio_dataset():
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

        success, message = trim_silence(
            input_file,
            output_file
        )

        if success:
            processed_count += 1
        else:
            skipped_count += 1
            print(f"Skipped: {input_file}")
            print(f"  Reason: {message}")

    print("\nSilence Trimming Summary")
    print("=" * 30)
    print(f"Files found     : {len(audio_files)}")
    print(f"Processed files : {processed_count}")
    print(f"Skipped files   : {skipped_count}")


if __name__ == "__main__":
    trim_audio_dataset()