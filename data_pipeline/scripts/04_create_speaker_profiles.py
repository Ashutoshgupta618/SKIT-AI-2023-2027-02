from pathlib import Path
import pandas as pd


# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_DIR = PROJECT_ROOT / "data_pipeline" / "metadata"

INPUT_FILE = METADATA_DIR / "acoustic_features.csv"

OUTPUT_FILE = METADATA_DIR / "speaker_profiles.csv"


# ==========================================
# Load acoustic features
# ==========================================

features = pd.read_csv(INPUT_FILE)


# ==========================================
# Features to aggregate
# ==========================================

PROFILE_FEATURES = [
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
    "spectral_centroid_std_hz"
]


# ==========================================
# Create speaker profiles
# ==========================================

speaker_profiles = (
    features
    .groupby(
        ["speaker_id", "language"],
        as_index=False
    )[PROFILE_FEATURES]
    .mean()
)


# ==========================================
# Add recording count
# ==========================================

recording_counts = (
    features
    .groupby(
        ["speaker_id", "language"]
    )
    .size()
    .reset_index(name="recordings_used")
)


speaker_profiles = speaker_profiles.merge(
    recording_counts,
    on=["speaker_id", "language"],
    how="left"
)


# ==========================================
# Save
# ==========================================

speaker_profiles.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# Summary
# ==========================================

print("======================================")
print("Speaker Profile Creation Completed")
print("======================================")

print(
    f"\nTotal speakers: "
    f"{speaker_profiles['speaker_id'].nunique()}"
)

print("\nSpeakers per language:")

print(
    speaker_profiles["language"].value_counts()
)

print("\nRecordings used per speaker:")

print(
    speaker_profiles[
        [
            "speaker_id",
            "language",
            "recordings_used"
        ]
    ].to_string(index=False)
)

print("\nSaved to:")
print(OUTPUT_FILE)