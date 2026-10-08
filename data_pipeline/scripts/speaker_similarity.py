import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
    / "acoustic_features.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
    / "speaker_similarity.csv"
)


# ==========================================
# Load acoustic features
# ==========================================

features_df = pd.read_csv(INPUT_FILE)

print("======================================")
print("Speaker Similarity Analysis")
print("======================================")

print(
    f"\nRecordings loaded: "
    f"{len(features_df)}"
)

print(
    f"Unique speakers: "
    f"{features_df['speaker_id'].nunique()}"
)


# ==========================================
# Select acoustic features
# ==========================================

FEATURE_COLUMNS = [
    "duration_sec",

    "pitch_mean_hz",
    "pitch_std_hz",
    "pitch_min_hz",
    "pitch_max_hz",

    "rms_mean",
    "rms_std",

    "zcr_mean",
    "zcr_std",

    "spectral_centroid_mean_hz",
    "spectral_centroid_std_hz",
]


# Add MFCC features
MFCC_COLUMNS = [
    f"mfcc_{i}"
    for i in range(1, 14)
]

FEATURE_COLUMNS.extend(MFCC_COLUMNS)


# ==========================================
# Prepare feature matrix
# ==========================================

X = features_df[FEATURE_COLUMNS].copy()


# Replace missing values with
# column median

X = X.fillna(
    X.median()
)


# ==========================================
# Standardize features
# ==========================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)


# ==========================================
# Calculate pairwise similarities
# ==========================================

similarity_matrix = cosine_similarity(
    X_scaled
)


# ==========================================
# Create pairwise results
# ==========================================

results = []

num_recordings = len(features_df)


for i in range(num_recordings):

    for j in range(i + 1, num_recordings):

        speaker_1 = features_df.iloc[i]["speaker_id"]
        speaker_2 = features_df.iloc[j]["speaker_id"]

        language_1 = features_df.iloc[i]["language"]
        language_2 = features_df.iloc[j]["language"]

        similarity = similarity_matrix[i, j]

        if speaker_1 == speaker_2:

            pair_type = "same_speaker"

        else:

            pair_type = "different_speaker"


        results.append({

            "speaker_1": speaker_1,

            "recording_1": features_df.iloc[i]["audio_filepath"],

            "language_1": language_1,

            "speaker_2": speaker_2,

            "recording_2": features_df.iloc[j]["audio_filepath"],

            "language_2": language_2,

            "pair_type": pair_type,

            "cosine_similarity": similarity
        })


# ==========================================
# Create DataFrame
# ==========================================

similarity_df = pd.DataFrame(results)


# ==========================================
# Save results
# ==========================================

similarity_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# Calculate summary statistics
# ==========================================

same_speaker = similarity_df[
    similarity_df["pair_type"] == "same_speaker"
]

different_speaker = similarity_df[
    similarity_df["pair_type"] == "different_speaker"
]


same_mean = same_speaker[
    "cosine_similarity"
].mean()

different_mean = different_speaker[
    "cosine_similarity"
].mean()


same_std = same_speaker[
    "cosine_similarity"
].std()

different_std = different_speaker[
    "cosine_similarity"
].std()


# ==========================================
# Final results
# ==========================================

print("\n======================================")
print("Similarity Analysis Completed")
print("======================================")

print(
    f"\nTotal recording pairs: "
    f"{len(similarity_df)}"
)

print(
    f"Same-speaker pairs: "
    f"{len(same_speaker)}"
)

print(
    f"Different-speaker pairs: "
    f"{len(different_speaker)}"
)


print("\nSimilarity Results:")

print(
    f"\nSame-speaker:"
    f"\n  Mean = {same_mean:.4f}"
    f"\n  Std  = {same_std:.4f}"
)

print(
    f"\nDifferent-speaker:"
    f"\n  Mean = {different_mean:.4f}"
    f"\n  Std  = {different_std:.4f}"
)


print("\nSaved to:")
print(OUTPUT_FILE)