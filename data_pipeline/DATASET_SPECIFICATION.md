# Vocal-X Multilingual Speech Dataset Specification

## Objective

Vocal-X requires multilingual speech data for developing and evaluating its
speech processing and translation pipeline.

The initial development phase focuses on eight Indian languages.

## Initial Languages

| Language | Code | Script |
|----------|------|--------|
| Hindi | hi | Devanagari |
| Bengali | bn | Bengali |
| Gujarati | gu | Gujarati |
| Marathi | mr | Devanagari |
| Tamil | ta | Tamil |
| Telugu | te | Telugu |
| Kannada | kn | Kannada |
| Malayalam | ml | Malayalam |

## Primary Dataset

AI4Bharat IndicVoices will be used as the primary source of multilingual
Indian speech data.

## Supplementary Dataset

Mozilla Common Voice may be used as a supplementary source when additional
speech data is required for the selected languages.

## Data Preprocessing

The collected speech data will undergo the following preprocessing stages:

1. Audio format validation
2. Sample-rate standardization
3. Channel standardization
4. Audio quality checks
5. Silence trimming
6. Audio normalization
7. Speech segmentation
8. Duration filtering
9. Metadata generation
10. Dataset quality analysis

## Data Organization

Original downloaded audio will be stored under `raw/`.

Processed audio will be stored under `processed/`.

Dataset metadata will be maintained under `metadata/`.

Preprocessing scripts will be maintained under `scripts/`.

Quality reports will be maintained under `reports/`.

## Raw Data Policy

Original source files will not be modified during preprocessing.
All transformations will produce separate processed files.

## Metadata

The dataset metadata will contain information such as:

- Audio ID
- Language
- Speaker ID, where available
- Dataset source
- File path
- Duration
- Sampling rate
- Number of channels
- Transcription, where available
- Processing status

## Initial Scope

The first phase will focus only on the eight selected Indian languages.

Additional languages and datasets may be added after the initial
preprocessing pipeline has been validated.