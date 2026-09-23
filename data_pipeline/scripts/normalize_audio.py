from pathlib import Path
import wave
import numpy as np

from dataset_config import RAW_DATA_DIR, PROCESSED_DATA_DIR


TARGET_PEAK = 0.95


def normalize_wav_file(input_path, output_path):
    try:
        with wave.open(str(input_path), "rb") as audio:
            params = audio.getparams()
            frames = audio.readframes(audio.getnframes())

        if params.sampwidth != 2:
            return False, "Only 16-bit PCM WAV files are supported"

        samples = np.frombuffer(
            frames,
            dtype=np.int16
        ).astype(np.float32)

        if len(samples) == 0:
            return False, "Empty audio file"

        peak = np.max(np.abs(samples))

        if peak == 0:
            return False, "Silent audio file"

        # Scale the waveform to a consistent peak level.
        normalized = samples * (TARGET_PEAK * 32767 / peak)

        normalized = np.clip(
            normalized,
            -32768,
            32767
        ).astype(np.int16)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with wave.open(str(output_path), "wb") as output:
            output.setparams(params)
            output.writeframes(normalized.tobytes())

        return True, "Audio normalized successfully"

    except (wave.Error, OSError, ValueError) as error:
        return False, f"Processing failed: {error}"


def normalize_audio_dataset():
    raw_path = Path(RAW_DATA_DIR)
    processed_path = Path(PROCESSED_DATA_DIR)

    audio_files = [
        path
        for path in raw_path.rglob("*.wav")
        if path.is_file()
    ]

    normalized_count = 0
    skipped_count = 0

    for input_file in audio_files:
        relative_path = input_file.relative_to(raw_path)
        output_file = processed_path / relative_path

        success, message = normalize_wav_file(
            input_file,
            output_file
        )

        if success:
            normalized_count += 1
        else:
            skipped_count += 1
            print(f"Skipped: {input_file}")
            print(f"  Reason: {message}")

    print("\nAudio Normalization Summary")
    print("=" * 32)
    print(f"Files found       : {len(audio_files)}")
    print(f"Normalized files  : {normalized_count}")
    print(f"Skipped files     : {skipped_count}")


if __name__ == "__main__":
    normalize_audio_dataset()