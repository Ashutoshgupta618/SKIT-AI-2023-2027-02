import pandas as pd

# take data from previous save 
df = pd.read_csv("audio_metadata.csv")
print("Checkpoint loaded! Dataset shape:", df.shape)

# remove corrupted files
bad_files = df[
    df["duration"].isna()
]

print("Corrupted/unreadable files:", len(bad_files))

if len(bad_files) > 0:
    display(bad_files.head(20))
    
    
# short files are not useful for training, and long files are too large to process efficiently
SHORT_LIMIT = 0.5

short_files = df[
    df["duration"] < SHORT_LIMIT
]

print(
    "Files shorter than",
    SHORT_LIMIT,
    "seconds:",
    len(short_files)
)

LONG_LIMIT = 30

long_files = df[
    df["duration"] > LONG_LIMIT
]

print(
    "Files longer than",
    LONG_LIMIT,
    "seconds:",
    len(long_files)
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
    df.iterrows(),
    total=len(df)
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


### normalizing the audio files to have zero mean and unit variance
