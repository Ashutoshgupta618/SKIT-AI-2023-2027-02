from datasets import load_dataset, Audio


DATASET_NAME = "ai4bharat/IndicVoices"
LANGUAGE = "hindi"

MAX_SPEAKERS = 10
RECORDINGS_PER_SPEAKER = 5


print(f"Loading {LANGUAGE} dataset in streaming mode...")

dataset = load_dataset(
    DATASET_NAME,
    LANGUAGE,
    split="train",
    streaming=True
)

# IMPORTANT:
# We only need audio metadata right now.
# Do not decode the actual audio.
dataset = dataset.cast_column(
    "audio_filepath",
    Audio(decode=False)
)

print("Dataset loaded.")
print("\nSelecting speakers...\n")


speakers = {}
total_selected = 0


for sample in dataset:

    speaker_id = sample["speaker_id"]

    if speaker_id not in speakers:

        if len(speakers) >= MAX_SPEAKERS:
            continue

        speakers[speaker_id] = []

    if len(speakers[speaker_id]) >= RECORDINGS_PER_SPEAKER:
        continue

    speakers[speaker_id].append(sample)

    total_selected += 1

    print(
        f"Speaker: {speaker_id} | "
        f"Recording: {len(speakers[speaker_id])}/"
        f"{RECORDINGS_PER_SPEAKER}"
    )

    if (
        len(speakers) == MAX_SPEAKERS
        and
        all(
            len(records) == RECORDINGS_PER_SPEAKER
            for records in speakers.values()
        )
    ):
        break


print("\n-----------------------------")
print("Selection completed")
print("-----------------------------")

print("Speakers selected:", len(speakers))
print("Total recordings:", total_selected)

for speaker_id, records in speakers.items():
    print(
        f"{speaker_id}: {len(records)} recordings"
    )