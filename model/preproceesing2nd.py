

# (previously these were only detected and printed, never removed)
clean_df = df[
    df["duration"].notna()
    & (df["duration"] >= SHORT_LIMIT)
    & (df["duration"] <= LONG_LIMIT)
].reset_index(drop=True)

print(
    f"\nKept {len(clean_df)} / {len(df)} files after filtering "
    f"({len(df) - len(clean_df)} dropped)"
)

# 
import os

PROJECT_DIR = "/content/polyvoice_dataset"

directories = [
    "raw",
    "processed",
    "metadata",
    "splits",
    "reports"
]

for directory in directories:

    os.makedirs(
        os.path.join(PROJECT_DIR, directory),
        exist_ok=True
    )

print("Project directories created.")

# Process audio files

import soundfile as sf
import librosa
from pathlib import Path
from tqdm.auto import tqdm

PROCESSED_DIR = Path(PROJECT_DIR) / "processed"

TARGET_SR = 16000

processed_records = []

for idx, row in tqdm(
    clean_df.iterrows(),   # use the filtered dataframe, not the raw one
    total=len(clean_df)
):

    input_file = Path(row["audio_path"])

    try:

        audio, sr = librosa.load(
            input_file,
            sr=TARGET_SR,
            mono=True
        )

        output_file = (
            PROCESSED_DIR /
            f"{idx:06d}.wav"
        )

        sf.write(
            output_file,
            audio,
            TARGET_SR
        )

        duration = len(audio) / TARGET_SR

        processed_records.append({
            "id": idx,
            "original_path": str(input_file),
            "audio_path": str(output_file),
            "language": row.get("language", ""),  # carried through if present in the manifest
            "sample_rate": TARGET_SR,
            "duration": duration,
            "status": "valid"
        })

    except Exception as e:

        processed_records.append({
            "id": idx,
            "original_path": str(input_file),
            "audio_path": "",
            "sample_rate": None,
            "duration": None,
            "status": f"error: {e}"
        })

processed_df = pd.DataFrame(processed_records)

print(processed_df.head())

processed_df.to_csv(Path(PROJECT_DIR) / "metadata" / "processed_metadata.csv", index=False)
print("Processed metadata saved.")


### Normalize processed audio for consistent loudness.
# Peak normalization (not zero-mean/unit-variance) is used here: zero-mean/unit-variance
# treats audio like generic numeric features and distorts waveform shape/timbre, which
# matters if these clips are later used as voice-cloning reference audio.

TARGET_PEAK = 0.95

for record in tqdm(processed_records, desc="Normalizing"):
    if record["status"] != "valid":
        continue

    audio_path = Path(record["audio_path"])
    audio, sr = librosa.load(audio_path, sr=None, mono=True)

    peak = max(abs(audio.max()), abs(audio.min())) or 1.0
    normalized = audio / peak * TARGET_PEAK

    sf.write(audio_path, normalized, sr)

print("Normalization complete.")


#  Processed audio validation

import soundfile as sf

validation_results = []

for record in processed_records:

    if record["status"] != "valid":
        continue

    file_path = Path(record["audio_path"])

    try:
        info = sf.info(file_path)

        validation_results.append({
            "id": record["id"],
            "file": str(file_path),
            "sample_rate": info.samplerate,
            "channels": info.channels,
            "duration": info.duration,
            "valid": True
        })

    except Exception as e:

        validation_results.append({
            "id": record["id"],
            "file": str(file_path),
            "sample_rate": None,
            "channels": None,
            "duration": None,
            "valid": False
        })

validation_df = pd.DataFrame(validation_results)

print(
    "Valid processed files:",
    validation_df["valid"].sum()
)

print(
    "Invalid processed files:",
    (~validation_df["valid"]).sum()
)

##B. Check 16 kHz and Mono
print("Sample rate distribution:")
print(
    validation_df["sample_rate"].value_counts()
)

print("\nChannel distribution:")
print(
    validation_df["channels"].value_counts()
)

## C. Final validation report save karo
REPORT_DIR = Path(PROJECT_DIR) / "reports"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

validation_df.to_csv(
    REPORT_DIR / "validation_report.csv",
    index=False
)

print(
    "Validation report saved successfully."
)

