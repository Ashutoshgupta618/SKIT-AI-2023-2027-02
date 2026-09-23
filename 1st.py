### Dataset was inspected and analyzed for file formats, languages, sample rates,
## missing/corrupted files, and abnormal audio durations.Short and excessively
## long audio files were identified for removal before preprocessing.


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
    print(bad_files.head(20).to_string())  # display() only works in Jupyter/Colab; print() works everywhere


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