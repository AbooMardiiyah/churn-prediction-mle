
# Churn Prediction (end to end)

Predict which telecom customers are likely to cancel, and turn that into something a retention team can use.

The project is built in public, week by week: notebooks first, then production-style Python modules, tests, an API,
a UI, and finally deployment. The structure follows the "production-ready ML" approach from The Neural Maze.

## Where we are

| Week | Topic | Status |
|---|---|---|
| 1 | Project setup, data download, split, EDA | ✅ `notebooks/00_data_split.ipynb`, `notebooks/01_EDA_cleaning.ipynb` |
| 2 | Validation (Great Expectations), cleaning, feature engineering | ⏳ |
| 3 | Baselines and imbalance | ⏳ |
| 4 | XGBoost, tuning (Optuna), tracking (MLflow) | ⏳ |
| 5 | Inference pipeline and FastAPI | ⏳ |
| 6 | UI and first deployment | ⏳ |
| 7 | Docker, AWS | ⏳ |
| 8 | CI/CD, monitoring | ⏳ |

## Quick start

You need [uv](https://docs.astral.sh/uv/) and Git. No other setup.

```bash
git clone <this-repo-url>
cd churn-prediction-mle

uv sync                                   # creates .venv and installs everything from uv.lock
uv run python -m ipykernel install --user --name churn-mle --display-name "Python (churn-mle)"

uv run python -m src.feature_pipeline.load   # downloads the dataset from Kaggle into data/raw/
uv run pytest                                # run the tests
```

Then open the notebooks in VS Code or Jupyter and select the **Python (churn-mle)** kernel.
Run `00_data_split.ipynb` first, then `01_EDA_cleaning.ipynb`.

If the Kaggle download is blocked on your network, download the CSV by hand from
<https://www.kaggle.com/datasets/blastchar/telco-customer-churn> and save it as `data/raw/telco_churn.csv`.

## Project layout

```
churn-prediction-mle/
├── configs/                 # YAML configs (validation rules, app settings)   [Week 2+]
├── data/                    # NOT in git. raw/ and processed/ are created by the code
├── models/                  # trained models and fitted encoders              [Week 3+]
├── notebooks/               # exploration, one notebook per step
├── src/
│   ├── utils/paths.py       # project root and data paths (works on any machine)
│   ├── feature_pipeline/    # load -> preprocess -> feature engineering
│   ├── training_pipeline/   # train, tune, evaluate                           [Week 3+]
│   ├── inference_pipeline/  # predict with saved artefacts                    [Week 5+]
│   └── api/                 # FastAPI service                                 [Week 5+]
├── tests/
└── pyproject.toml           # dependencies (managed with uv)
```

## Conventions

- **No hard-coded paths.** Everything comes from `src/utils/paths.py`, which finds the project root by locating `pyproject.toml`.
- **Data never goes to Git.** It is downloaded by code. See `.gitignore`.
- **Split first, explore after.** EDA only looks at the training split. The holdout set is used once, at the end.
- **Notebooks explore, `src/` ships.** Logic proven in a notebook moves into a tested module.
