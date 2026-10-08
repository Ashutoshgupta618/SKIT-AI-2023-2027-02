import librosa
import pandas as pd
import numpy as np
from pathlib import Path


# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
    / "acoustic_features.csv"
)


# ==========================================
# Audio settings
# ==========================================

TARGET_SR = 16000

N_MFCC = 13

N_FFT = 2048
HOP_LENGTH = 512


# ==========================================
# Load metadata
# ==========================================

METADATA_FILES = [
    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
    / "speaker_dataset.csv",

    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
    / "multilingual_speaker_dataset.csv",

    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
    / "telugu_marathi_speaker_dataset.csv"
]

metadata_list = []

for file in METADATA_FILES:

    print(f"Loading metadata: {file.name}")

    df = pd.read_csv(file)

    metadata_list.append(df)


# Combine all metadata files
metadata = pd.concat(
    metadata_list,
    ignore_index=True
)


# ==========================================
# Initial information
# ==========================================

print("\n======================================")
print("Speaker Acoustic Feature Extraction")
print("======================================")

print(f"\nAudio files to process: {len(metadata)}")

print("\nRecordings per language:")
print(
    metadata["language"].value_counts()
)

print("\nTotal speakers:")
print(
    metadata["speaker_id"].nunique()
)


results = []


# ==========================================
# Process every recording
# ==========================================

for index, row in metadata.iterrows():

    audio_path = PROJECT_ROOT / row["audio_filepath"]

    print(
        f"\n[{index + 1}/{len(metadata)}] "
        f"Processing: {audio_path.name}"
    )

    # --------------------------------------
    # Load audio
    # --------------------------------------

    y, sr = librosa.load(
        audio_path,
        sr=TARGET_SR,
        mono=True
    )

    # --------------------------------------
    # Duration
    # --------------------------------------

    duration = librosa.get_duration(
        y=y,
        sr=sr
    )

    # --------------------------------------
    # Pitch / Fundamental Frequency
    # --------------------------------------
    #
    # pYIN estimates F0 only for voiced frames.
    #

    f0, voiced_flag, voiced_prob = librosa.pyin(
        y,
        fmin=50,
        fmax=500,
        sr=sr,
        frame_length=N_FFT,
        hop_length=HOP_LENGTH
    )

    valid_f0 = f0[~np.isnan(f0)]

    if len(valid_f0) > 0:

        pitch_mean = float(np.mean(valid_f0))
        pitch_std = float(np.std(valid_f0))
        pitch_min = float(np.min(valid_f0))
        pitch_max = float(np.max(valid_f0))

    else:

        pitch_mean = np.nan
        pitch_std = np.nan
        pitch_min = np.nan
        pitch_max = np.nan


    # --------------------------------------
    # RMS Energy
    # --------------------------------------

    rms = librosa.feature.rms(
        y=y,
        frame_length=N_FFT,
        hop_length=HOP_LENGTH
    )

    rms_mean = float(np.mean(rms))
    rms_std = float(np.std(rms))


    # --------------------------------------
    # Zero Crossing Rate
    # --------------------------------------

    zcr = librosa.feature.zero_crossing_rate(
        y,
        frame_length=N_FFT,
        hop_length=HOP_LENGTH
    )

    zcr_mean = float(np.mean(zcr))
    zcr_std = float(np.std(zcr))


    # --------------------------------------
    # Spectral Centroid
    # --------------------------------------

    spectral_centroid = librosa.feature.spectral_centroid(
        y=y,
        sr=sr,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH
    )

    centroid_mean = float(
        np.mean(spectral_centroid)
    )

    centroid_std = float(
        np.std(spectral_centroid)
    )


    # --------------------------------------
    # MFCC
    # --------------------------------------

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=N_MFCC,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH
    )

    mfcc_mean = np.mean(
        mfcc,
        axis=1
    )


    # --------------------------------------
    # Create feature record
    # --------------------------------------

    feature_row = {

        "audio_filepath": row["audio_filepath"],

        "speaker_id": row["speaker_id"],

        "language": row["language"],

        "duration_sec": duration,

        "pitch_mean_hz": pitch_mean,

        "pitch_std_hz": pitch_std,

        "pitch_min_hz": pitch_min,

        "pitch_max_hz": pitch_max,

        "rms_mean": rms_mean,

        "rms_std": rms_std,

        "zcr_mean": zcr_mean,

        "zcr_std": zcr_std,

        "spectral_centroid_mean_hz":
            centroid_mean,

        "spectral_centroid_std_hz":
            centroid_std,
    }


    # --------------------------------------
    # Add 13 MFCC values
    # --------------------------------------

    for i in range(N_MFCC):

        feature_row[
            f"mfcc_{i + 1}"
        ] = float(
            mfcc_mean[i]
        )


    results.append(feature_row)


# ==========================================
# Create DataFrame
# ==========================================

features_df = pd.DataFrame(results)


# ==========================================
# Save results
# ==========================================

features_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==========================================
# Final summary
# ==========================================

print("\n======================================")
print("Feature extraction completed")
print("======================================")

print(
    f"Recordings processed : "
    f"{len(features_df)}"
)

print(
    f"Features per audio   : "
    f"{len(features_df.columns)}"
)

print("\nSaved to:")
print(OUTPUT_FILE)

print("\nTotal speakers:")
print(
    features_df["speaker_id"].nunique()
)

print("\nRecordings per language:")
print(
    features_df["language"].value_counts()
)

print("\nFeature preview:")

print(
    features_df[
        [
            "speaker_id",
            "language",
            "duration_sec",
            "pitch_mean_hz",
            "pitch_std_hz",
            "rms_mean",
            "zcr_mean",
            "spectral_centroid_mean_hz"
        ]
    ].to_string(index=False)
)