from datasets import load_dataset, Audio


DATASET_NAME = "ai4bharat/IndicVoices"
LANGUAGE = "hindi"


print(f"Loading {LANGUAGE} dataset...")

dataset = load_dataset(
    DATASET_NAME,
    LANGUAGE,
    split="train",
    streaming=True
)

dataset = dataset.cast_column(
    "audio_filepath",
    Audio(decode=False)
)

print("Getting first sample...\n")

sample = next(iter(dataset))

print("Speaker ID:")
print(sample["speaker_id"])

print("\nLanguage:")
print(sample["lang"])

print("\nDuration:")
print(sample["duration"])

print("\nAudio reference:")
print(sample["audio_filepath"])
