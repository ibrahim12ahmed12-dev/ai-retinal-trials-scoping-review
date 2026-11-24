# 01_figures.py

This script draws the figures for "Uses and reporting quality of artificial intelligence in retinal disease clinical trials: a scoping review". Each figure is saved as a 300 dpi PNG and as a PDF.

## Requirements

- Python 3.13
- matplotlib 3.11.2
- numpy 2.5.3

Install them with:

```
pip install matplotlib==3.11.2 numpy==2.5.3
```

## Inputs

Both data files are included in the dataset. Keep them in these folders, relative to the script:

| File | Contents |
|---|---|
| `data/extraction_and_ratings.json` | The charted data and reporting ratings for the 36 included studies. `rows` holds the study details. `ratings` holds the item ratings (Yes, Partial, No or not applicable), with `full_items` for the CONSORT 2010 or TRIPOD+AI items and `ai_items` for the CONSORT-AI extension items. |
| `outputs/study_coding.json` | The coded variables for each study: AI function, timing, whether the AI changed trial conduct, appraisal group and measurement validation. |

## How to run

From the folder that holds the script:

```
python 01_figures.py
```

No other script needs to run first.

## Outputs

All outputs go to `outputs/figures/`, which the script creates if it is missing.

| File | Figure | Panels |
|---|---|---|
| `Fig1_PRISMA_ScR.png` / `.pdf` | Fig. 1. PRISMA-ScR flow diagram | Records identified, screened and excluded, full-text reports assessed with reasons for exclusion, and the 36 included studies. The counts are typed into the script. |
| `Fig2_ai_use.png` / `.pdf` | Fig. 2. Publication, trial sources and use of AI | **a** Included studies by publication year, with a bracket marking the 27 studies (75%) from 2022 onwards. **b** Trial programs contributing more than one study (HARBOR, FILLY, OAKS/DERBY, HAWK/HARRIER). **c** AI function, split by when the AI was applied: prospective and changed trial conduct, prospective without changing trial conduct, or retrospective (secondary or post hoc analysis). Segment counts and totals are printed on the bars. |
| `Fig3_reporting_by_study_type.png` / `.pdf` | Fig. 3. Reporting completeness by study type | **a** AI measurement studies (n = 22): share reporting each of ten adapted domains, grouped into reproducibility, measurement validity, transportability and output definition, with the numbers reporting and partially reporting each domain on the right. **b** Prediction and diagnostic model studies (n = 12): TRIPOD+AI ratings by manuscript section, with the median adherence in the title. **c** Randomized trials of AI interventions (n = 2, ACCESS and RAIDERS): adherence to the CONSORT 2010 items and to the CONSORT-AI extension items, with the number of applicable items. |
| `FigS1_tripod_items.png` / `.pdf` | Supplementary Fig. 1 (optional) | Heatmap of the TRIPOD+AI rating for each item in each of the 12 prediction model studies. |

The script also prints the panel c adherence values and the median TRIPOD+AI adherence, so they can be checked against the text.

## How ratings are scored

- **Bar colors:** dark blue means reported, light blue means partially reported and gray means not reported.
- **Adherence:** Yes = 1, Partial = 0.5 and No = 0. Items rated not applicable are left out of the denominator.
- **Fig. 3a, "Accuracy or agreement on trial images" (marked \*):** this row comes from the coded measurement validation, not from a checklist item.
  - Reported: accuracy against a human reference, or agreement with a clinical or alternative-modality reference, on trial images.
  - Partially reported: all outputs were corrected by analysts, without reported accuracy.

## Changing the figures

- **Colors:** `YES`, `PAR` and `NO` (reporting bars), `TIM` (Fig. 2c timing) and `C2010`, `CAI` (Fig. 3c), near the places they are used.
- **Panel titles:** the `panel(...)` calls.
- **Fig. 1 counts:** the box text in the Fig. 1 section.
- **Fig. 2b programs:** the `prog` dictionary of program names and study counts.
- **Fig. 3a domains:** the `dims` list.
- **Figure size:** the `figsize` arguments, in inches. 7.2 inches is about the full page width.
