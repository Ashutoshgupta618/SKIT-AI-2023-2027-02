from datasets import load_dataset


DATASET_NAME = "ai4bharat/IndicVoices"
LANGUAGE = "hindi"


print(f"Loading {LANGUAGE} dataset in streaming mode...")

dataset = load_dataset(
    DATASET_NAME,
    LANGUAGE,
    split="train",
    streaming=True
)

print("\nDataset loaded successfully.")

print("\nDataset features:")

for name, feature in dataset.features.items():
    print(f"- {name}: {feature}")

print("\nDataset inspection completed.")