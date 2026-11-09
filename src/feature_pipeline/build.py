import json
import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from src.utils.paths import RAW_DIR, PROCESSED_DIR, MODELS_DIR, PROJECT_ROOT
from src.feature_pipeline.preprocess import clean, prepare, to_features, transform_features, cat_cols, ID_COL, TARGET
from src.feature_pipeline.validate import validate_data


FEATURE_DIR = MODELS_DIR / "week5_features"
REPORT_DIR = PROJECT_ROOT / "reports" / "week5"


def run():
    train = pd.read_csv(RAW_DIR / "train.csv")
    evaluation = pd.read_csv(RAW_DIR / "eval.csv")
    # holdout = pd.read_csv(RAW_DIR / "holdout.csv")
    validate_data(train, REPORT_DIR / "train_incoming.json")
    validate_data(evaluation, REPORT_DIR / "eval_incoming.json")
    #validate_data(....)

    train, evaluation = clean(train), clean(evaluation)
    validate_data(train, REPORT_DIR / "train_cleaned.json", cleaned=True)
    validate_data(evaluation, REPORT_DIR / "eval_cleaned.json", cleaned=True)
    if not set(train.customerID).isdisjoint(evaluation.customerID):
        raise ValueError("The same customer appears in training and evaluation.")
    ready = prepare(train)
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoder.fit(ready[cat_cols])  # learn from TRAIN only
    columns = [c for c in to_features(ready, encoder).columns if c not in (ID_COL, TARGET)]
    train_features = transform_features(train, encoder, columns)
    eval_features = transform_features(evaluation, encoder, columns)
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(encoder, FEATURE_DIR / "encoder.joblib")
    (FEATURE_DIR / "feature_columns.json").write_text(json.dumps(columns, indent=2))
    for name, source, features in [("train", train, train_features), ("eval", evaluation, eval_features)]:
        features = features.assign(customerID=source["customerID"], Churn=source["Churn"])
        features.to_csv(PROCESSED_DIR / f"week5_features_{name}.csv", index=False)
    print(f"Validation passed. Saved {len(columns)} features for train and evaluation.")

if __name__ == "__main__":
    run()
