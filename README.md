# Customer Churn Prediction

An in-progress machine learning project using the [Telco Customer Churn dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn). The current work downloads the data, creates reproducible train, evaluation, and holdout splits, and begins exploratory data analysis. Model training, an API, and a UI are planned but are not implemented yet.

## Setup

Python 3.10 or newer and [uv](https://docs.astral.sh/uv/) are required. From the project root, install the project and notebook dependencies:

```bash
uv sync --group dev
```

Open the notebooks in your preferred notebook editor and select the project's `.venv/bin/python` interpreter as the kernel. Run them in order:

1. `notebooks/00_data_split.ipynb` downloads the CSV and creates the splits.
2. `notebooks/01_EDA_cleaning.ipynb` loads the train and evaluation sets for initial exploration.

The first download needs internet access. The download helper reuses `data/raw/telco_churn.csv` on later runs. You can also run the helper from the project root:

```bash
uv run python -m src.feature_pipeline.load
```

## Data workflow

The source dataset contains 7,043 customers and 21 columns, including the `Churn` target. `00_data_split.ipynb` uses a stratified random split on `Churn` with seed `42`, preserving approximately the same churn rate in each set:

| Split | Share | Current rows | Purpose |
| --- | ---: | ---: | --- |
| Train | 70% | 4,930 | Exploration and fitting |
| Evaluation | 15% | 1,056 | Model selection and tuning |
| Holdout | 15% | 1,057 | Final assessment |

The notebook checks that the sets contain distinct `customerID` values and together cover all source rows. It writes `data/raw/train.csv`, `data/raw/eval.csv`, and `data/raw/holdout_df`. The holdout file currently has no `.csv` extension, although it contains CSV data. Keep the holdout set out of exploration and tuning.

The `data/` directory is ignored by Git, so downloaded data and generated splits stay local.

## Project layout

```text
configs/                  Configuration files (currently empty)
notebooks/
  00_data_split.ipynb     Download, inspect, and split the dataset
  01_EDA_cleaning.ipynb   Initial train/evaluation exploration
src/
  feature_pipeline/load.py  Kaggle download helper
  utils/paths.py            Project data and other directory paths
tests/                    Tests (currently empty)
```

The EDA notebook is still in progress. Data cleaning, feature engineering, model training, evaluation, and serving have not been added yet.
