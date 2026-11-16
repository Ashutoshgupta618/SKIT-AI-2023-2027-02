from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_DIR = PROJECT_ROOT / "data_pipeline" / "metadata"

OUTPUT_FILE = (
    METADATA_DIR /
    "25_speaker_voice_analysis.xlsx"
)


# ==========================================
# Read Dataset Metadata
# ==========================================

METADATA_FILES = [
    METADATA_DIR / "speaker_dataset.csv",
    METADATA_DIR / "multilingual_speaker_dataset.csv",
    METADATA_DIR / "telugu_marathi_speaker_dataset.csv"
]

metadata_list = []

for file in METADATA_FILES:

    df = pd.read_csv(file)

    metadata_list.append(df)


speaker_dataset = pd.concat(
    metadata_list,
    ignore_index=True
)


# ==========================================
# Read Acoustic Features
# ==========================================

acoustic_features = pd.read_csv(
    METADATA_DIR / "acoustic_features.csv"
)


# ==========================================
# Read Speaker Profiles
# ==========================================

speaker_profiles = pd.read_csv(
    METADATA_DIR / "speaker_profiles.csv"
)


# ==========================================
# Create Excel Workbook
# ==========================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    speaker_dataset.to_excel(
        writer,
        sheet_name="Dataset",
        index=False
    )

    acoustic_features.to_excel(
        writer,
        sheet_name="Acoustic Features",
        index=False
    )

    speaker_profiles.to_excel(
        writer,
        sheet_name="Speaker Profiles",
        index=False
    )


# ==========================================
# Format Workbook
# ==========================================

workbook = load_workbook(
    OUTPUT_FILE
)


for worksheet in workbook.worksheets:

    # --------------------------------------
    # Freeze header
    # --------------------------------------

    worksheet.freeze_panes = "A2"


    # --------------------------------------
    # Enable filters
    # --------------------------------------

    worksheet.auto_filter.ref = (
        worksheet.dimensions
    )


    # --------------------------------------
    # Format header
    # --------------------------------------

    for cell in worksheet[1]:

        cell.font = Font(
            bold=True,
            color="FFFFFF"
        )

        cell.fill = PatternFill(
            "solid",
            fgColor="1F4E78"
        )

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )


    # --------------------------------------
    # Adjust column widths
    # --------------------------------------

    for column_cells in worksheet.columns:

        max_length = 0

        column_letter = get_column_letter(
            column_cells[0].column
        )

        for cell in column_cells:

            if cell.value is not None:

                max_length = max(
                    max_length,
                    len(str(cell.value))
                )

        worksheet.column_dimensions[
            column_letter
        ].width = min(
            max_length + 2,
            40
        )


    # --------------------------------------
    # Header height
    # --------------------------------------

    worksheet.row_dimensions[1].height = 25


# ==========================================
# Save Workbook
# ==========================================

workbook.save(
    OUTPUT_FILE
)


# ==========================================
# Final Summary
# ==========================================

print("======================================")
print("Excel analysis workbook created")
print("======================================")

print("\nSheets created:")
print("1. Dataset")
print("2. Acoustic Features")
print("3. Speaker Profiles")

print("\nDataset recordings:")
print(len(speaker_dataset))

print("\nAcoustic feature records:")
print(len(acoustic_features))

print("\nSpeaker profiles:")
print(len(speaker_profiles))

print("\nSaved to:")
print(OUTPUT_FILE)