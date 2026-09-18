# Vocal-X Multilingual Speech Dataset Configuration

DATASET_NAME = "ai4bharat/IndicVoices"

LANGUAGES = {
    "hi": "hindi",
    "bn": "bengali",
    "gu": "gujarati",
    "mr": "marathi",
    "ta": "tamil",
    "te": "telugu",
    "kn": "kannada",
    "ml": "malayalam",
}

DATASET_SPLIT = "train"

RAW_DATA_DIR = "data_pipeline/raw"
PROCESSED_DATA_DIR = "data_pipeline/processed"
METADATA_DIR = "data_pipeline/metadata"
REPORTS_DIR = "data_pipeline/reports"

TARGET_SAMPLE_RATE = 16000
TARGET_CHANNELS = 1

MIN_DURATION_SECONDS = 1.0
MAX_DURATION_SECONDS = 30.0