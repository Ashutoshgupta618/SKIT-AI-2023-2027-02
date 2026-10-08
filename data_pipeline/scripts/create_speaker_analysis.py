from pathlib import Path

import pandas as pd

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference


# ==========================================
# Paths
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_DIR = (
    PROJECT_ROOT
    / "data_pipeline"
    / "metadata"
)

OUTPUT_FILE = (
    METADATA_DIR
    / "speaker_analysis.xlsx"
)


# ==========================================
# Input files
# ==========================================

ACOUSTIC_FILE = (
    METADATA_DIR
    / "acoustic_features.csv"
)

PROFILE_FILE = (
    METADATA_DIR
    / "speaker_profiles.csv"
)

SIMILARITY_FILE = (
    METADATA_DIR
    / "speaker_similarity.csv"
)


# ==========================================
# Load data
# ==========================================

acoustic_features = pd.read_csv(
    ACOUSTIC_FILE
)

speaker_profiles = pd.read_csv(
    PROFILE_FILE
)

similarity = pd.read_csv(
    SIMILARITY_FILE
)


# ==========================================
# Basic statistics
# ==========================================

total_recordings = len(acoustic_features)

total_speakers = (
    acoustic_features["speaker_id"]
    .nunique()
)

total_languages = (
    acoustic_features["language"]
    .nunique()
)

total_features = (
    len(acoustic_features.columns)
)

total_pairs = len(similarity)

same_speaker = similarity[
    similarity["pair_type"] == "same_speaker"
]

different_speaker = similarity[
    similarity["pair_type"] == "different_speaker"
]


same_mean = (
    same_speaker["cosine_similarity"]
    .mean()
)

same_std = (
    same_speaker["cosine_similarity"]
    .std()
)

different_mean = (
    different_speaker["cosine_similarity"]
    .mean()
)

different_std = (
    different_speaker["cosine_similarity"]
    .std()
)

separation = (
    same_mean - different_mean
)


# ==========================================
# Overview table
# ==========================================

overview = pd.DataFrame({

    "Metric": [
        "Languages",
        "Speakers",
        "Recordings",
        "Acoustic features per recording",
        "Total recording pairs",
        "Same-speaker pairs",
        "Different-speaker pairs",
        "Mean same-speaker similarity",
        "Std same-speaker similarity",
        "Mean different-speaker similarity",
        "Std different-speaker similarity",
        "Mean similarity separation"
    ],

    "Value": [
        total_languages,
        total_speakers,
        total_recordings,
        total_features,
        total_pairs,
        len(same_speaker),
        len(different_speaker),
        same_mean,
        same_std,
        different_mean,
        different_std,
        separation
    ]
})


# ==========================================
# Similarity summary
# ==========================================

similarity_summary = pd.DataFrame({

    "Comparison": [
        "Same Speaker",
        "Different Speaker"
    ],

    "Number of Pairs": [
        len(same_speaker),
        len(different_speaker)
    ],

    "Mean Similarity": [
        same_mean,
        different_mean
    ],

    "Standard Deviation": [
        same_std,
        different_std
    ],

    "Interpretation": [
        "Higher similarity indicates within-speaker consistency.",
        "Lower similarity indicates separation between speakers."
    ]
})


# ==========================================
# Same-speaker pairs
# ==========================================

same_speaker_pairs = same_speaker[
    [
        "speaker_1",
        "recording_1",
        "language_1",
        "speaker_2",
        "recording_2",
        "language_2",
        "cosine_similarity"
    ]
].copy()


# ==========================================
# Different-speaker pairs
# ==========================================

different_speaker_pairs = different_speaker[
    [
        "speaker_1",
        "recording_1",
        "language_1",
        "speaker_2",
        "recording_2",
        "language_2",
        "cosine_similarity"
    ]
].copy()


# ==========================================
# Create workbook
# ==========================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    overview.to_excel(
        writer,
        sheet_name="Overview",
        index=False
    )

    speaker_profiles.to_excel(
        writer,
        sheet_name="Speaker Profiles",
        index=False
    )

    similarity_summary.to_excel(
        writer,
        sheet_name="Similarity Summary",
        index=False
    )

    same_speaker_pairs.to_excel(
        writer,
        sheet_name="Same Speaker Pairs",
        index=False
    )

    different_speaker_pairs.to_excel(
        writer,
        sheet_name="Different Speaker Pairs",
        index=False
    )

    acoustic_features.to_excel(
        writer,
        sheet_name="Acoustic Features",
        index=False
    )


# ==========================================
# Load workbook for formatting
# ==========================================

workbook = load_workbook(
    OUTPUT_FILE
)


# ==========================================
# Common styles
# ==========================================

header_fill = PatternFill(
    "solid",
    fgColor="1F4E78"
)

header_font = Font(
    bold=True,
    color="FFFFFF"
)

title_font = Font(
    bold=True,
    size=16
)

subheader_font = Font(
    bold=True,
    size=12
)


# ==========================================
# Format every worksheet
# ==========================================

for worksheet in workbook.worksheets:

    # Freeze first row
    worksheet.freeze_panes = "A2"

    # Enable filters
    worksheet.auto_filter.ref = (
        worksheet.dimensions
    )

    # Header formatting
    for cell in worksheet[1]:

        cell.font = header_font

        cell.fill = header_fill

        cell.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    worksheet.row_dimensions[1].height = 25

    # Column widths
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
            45
        )


# ==========================================
# Format Overview sheet
# ==========================================

overview_sheet = workbook["Overview"]

overview_sheet["A1"].font = title_font

# Add explanatory section
overview_sheet["D1"] = "What This Means"
overview_sheet["D1"].font = title_font

overview_sheet["D3"] = (
    "Same-speaker similarity"
)

overview_sheet["E3"] = (
    "How similar the acoustic feature "
    "vectors are between recordings "
    "of the same person."
)

overview_sheet["D4"] = (
    "Different-speaker similarity"
)

overview_sheet["E4"] = (
    "How similar recordings from "
    "different people are."
)

overview_sheet["D5"] = (
    "Similarity separation"
)

overview_sheet["E5"] = (
    "Mean same-speaker similarity "
    "minus mean different-speaker similarity."
)

overview_sheet["D7"] = "Current Result"
overview_sheet["D7"].font = subheader_font

overview_sheet["D8"] = (
    f"Same speaker mean: {same_mean:.4f}"
)

overview_sheet["D9"] = (
    f"Different speaker mean: "
    f"{different_mean:.4f}"
)

overview_sheet["D10"] = (
    f"Separation: {separation:.4f}"
)

overview_sheet["D12"] = "Conclusion"
overview_sheet["D12"].font = subheader_font

overview_sheet["D13"] = (
    "The acoustic features show measurable "
    "speaker-related consistency because "
    "same-speaker recordings have a higher "
    "average similarity than different-speaker "
    "recordings."
)

overview_sheet["D13"].alignment = Alignment(
    wrap_text=True,
    vertical="top"
)

overview_sheet.column_dimensions["D"].width = 30
overview_sheet.column_dimensions["E"].width = 65

# Number formatting
for row in range(2, overview_sheet.max_row + 1):

    metric = overview_sheet.cell(
        row=row,
        column=1
    ).value

    if metric in [
        "Mean same-speaker similarity",
        "Std same-speaker similarity",
        "Mean different-speaker similarity",
        "Std different-speaker similarity",
        "Mean similarity separation"
    ]:

        overview_sheet.cell(
            row=row,
            column=2
        ).number_format = "0.0000"


# ==========================================
# Format Similarity Summary
# ==========================================

summary_sheet = workbook[
    "Similarity Summary"
]

for row in range(
    2,
    summary_sheet.max_row + 1
):

    summary_sheet.cell(
        row=row,
        column=3
    ).number_format = "0.0000"

    summary_sheet.cell(
        row=row,
        column=4
    ).number_format = "0.0000"


# ==========================================
# Format pair similarity values
# ==========================================

for sheet_name in [
    "Same Speaker Pairs",
    "Different Speaker Pairs"
]:

    sheet = workbook[sheet_name]

    # Cosine similarity is column G
    for row in range(
        2,
        sheet.max_row + 1
    ):

        sheet.cell(
            row=row,
            column=7
        ).number_format = "0.0000"


# ==========================================
# Add comparison chart
# ==========================================

chart_sheet = workbook[
    "Similarity Summary"
]

chart = BarChart()

chart.title = (
    "Average Speaker Similarity"
)

chart.y_axis.title = (
    "Cosine Similarity"
)

chart.x_axis.title = (
    "Comparison Type"
)

data = Reference(
    chart_sheet,
    min_col=3,
    min_row=1,
    max_row=3
)

categories = Reference(
    chart_sheet,
    min_col=1,
    min_row=2,
    max_row=3
)

chart.add_data(
    data,
    titles_from_data=True
)

chart.set_categories(
    categories
)

chart.height = 8
chart.width = 15

chart_sheet.add_chart(
    chart,
    "A6"
)


# ==========================================
# Save workbook
# ==========================================

workbook.save(
    OUTPUT_FILE
)


# ==========================================
# Final message
# ==========================================

print("======================================")
print("Speaker Analysis Workbook Created")
print("======================================")

print("\nSheets created:")

print("1. Overview")
print("2. Speaker Profiles")
print("3. Similarity Summary")
print("4. Same Speaker Pairs")
print("5. Different Speaker Pairs")
print("6. Acoustic Features")

print("\nKey results:")

print(
    f"Same-speaker mean      : "
    f"{same_mean:.4f}"
)

print(
    f"Different-speaker mean : "
    f"{different_mean:.4f}"
)

print(
    f"Similarity separation  : "
    f"{separation:.4f}"
)

print("\nSaved to:")
print(OUTPUT_FILE)