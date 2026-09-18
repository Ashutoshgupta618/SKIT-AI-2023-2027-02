from pathlib import Path
import subprocess
import sys


SCRIPT_DIR = Path(__file__).resolve().parent

PIPELINE_STEPS = [
    ("Audio quality validation", "validate_audio.py"),
    ("Audio format standardization", "standardize_audio.py"),
    ("Silence trimming", "trim_silence.py"),
    ("Audio normalization", "normalize_audio.py"),
    ("Speech segmentation", "segment_speech.py"),
    ("Duration filtering", "filter_duration.py"),
    ("Processed metadata generation", "generate_processed_metadata.py"),
    ("Audio quality reporting", "generate_quality_report.py"),
]


def run_step(name, script_name):
    script_path = SCRIPT_DIR / script_name

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=SCRIPT_DIR.parent.parent,
    )

    if result.returncode != 0:
        print(f"\nPipeline stopped: {name}")
        return False

    return True


def run_pipeline():
    print("Vocal-X Multilingual Speech Preprocessing Pipeline")
    print("=" * 60)

    for name, script_name in PIPELINE_STEPS:
        if not run_step(name, script_name):
            return

    print("\n" + "=" * 60)
    print("Preprocessing pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()