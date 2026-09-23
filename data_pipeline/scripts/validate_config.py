from dataset_config import (
    DATASET_NAME,
    LANGUAGES,
    DATASET_SPLIT,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    METADATA_DIR,
    REPORTS_DIR,
    TARGET_SAMPLE_RATE,
    TARGET_CHANNELS,
    MIN_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
)


def validate_configuration():
    print("Vocal-X Dataset Configuration")
    print("=" * 40)

    print(f"Dataset          : {DATASET_NAME}")
    print(f"Split            : {DATASET_SPLIT}")

    print("\nSupported Languages:")
    for code, name in LANGUAGES.items():
        print(f"  {code} -> {name}")

    print("\nDirectories:")
    print(f"  Raw             : {RAW_DATA_DIR}")
    print(f"  Processed       : {PROCESSED_DATA_DIR}")
    print(f"  Metadata        : {METADATA_DIR}")
    print(f"  Reports         : {REPORTS_DIR}")

    print("\nAudio Standards:")
    print(f"  Sample Rate     : {TARGET_SAMPLE_RATE} Hz")
    print(f"  Channels        : {TARGET_CHANNELS}")
    print(f"  Duration Range  : {MIN_DURATION_SECONDS}s - "
          f"{MAX_DURATION_SECONDS}s")

    if len(LANGUAGES) != 8:
        raise ValueError("Expected exactly 8 supported languages.")

    if TARGET_SAMPLE_RATE <= 0:
        raise ValueError("Sample rate must be positive.")

    if TARGET_CHANNELS not in (1, 2):
        raise ValueError("Channels must be 1 or 2.")

    if MIN_DURATION_SECONDS >= MAX_DURATION_SECONDS:
        raise ValueError("Invalid duration range.")

    print("\nConfiguration validation successful.")


if __name__ == "__main__":
    validate_configuration()