# 03_figures.py

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
python 03_figures.py
```

## Outputs

All outputs go to `outputs/figures/`, which the script creates if it is missing.

| File | Figure | Panels |
|---|---|---|
| `Fig2_ai_use.png` / `.pdf` | Fig. 2. Use of AI in the included studies | **a** AI function, split by when the AI was applied: prospective and changed trial conduct, prospective without changing trial conduct, or retrospective post hoc analysis. **b** Included studies by publication year. **c** Trial programs contributing more than one study (HARBOR, FILLY, OAKS/DERBY, HAWK/HARRIER). |
| `Fig3_reporting_by_study_type.png` / `.pdf` | Fig. 3. Reporting completeness by study type | **a** AI measurement studies (n = 22): share reporting each item, grouped into reproducibility, measurement validity, transportability and output, with the CONSORT-AI items adapted. **b** Prediction and diagnostic model studies (n = 12): TRIPOD+AI ratings by manuscript section, with the median adherence in the title. **c** Randomized trials of AI interventions (n = 2, ACCESS and RAIDERS): adherence to the CONSORT 2010 items and to the CONSORT-AI extension items. |
| `FigS1_tripod_items.png` / `.pdf` | Supplementary Fig. 1 (optional) | Heatmap of the TRIPOD+AI rating for each item in each of the 12 prediction model studies. |

The script also prints the panel c adherence values and the median TRIPOD+AI adherence, so they can be checked against the text.

## How ratings are scored

- **Bar colours:** dark blue means reported, light blue means partially reported and grey means not reported.
- **Adherence:** Yes = 1, Partial = 0.5 and No = 0. Items rated not applicable are left out of the denominator.
- **Fig. 3a, "Accuracy or agreement on trial images":** this row comes from the coded measurement validation, not from a checklist item.
  - Reported: accuracy or agreement was assessed.
  - Partially reported: outputs were corrected by graders.

## Changing the figures

- **Colours:** the `YES`, `PAR`, `NO` and `TIM` variables near the top of the script.
- **Panel titles:** the `panel(...)` calls.
- **Fig. 3a items:** the `dims` list.
- **Fig. 2c programs:** the `prog` dictionary, which uses study row numbers from the JSON.
- **Figure size:** the `figsize` arguments, in inches. 7.2 inches is about the full page width.
