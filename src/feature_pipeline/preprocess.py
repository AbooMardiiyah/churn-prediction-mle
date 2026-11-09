import numpy as np
import pandas as pd


ID_COL, TARGET = ("customerID", "Churn")
DROP_COLS = ["gender", "TotalCharges"]
addon_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
yes_no_cols = ["Partner", "Dependents", "PhoneService", "MultipleLines", "PaperlessBilling"] + addon_cols
cat_cols = ["Contract", "InternetService", "PaymentMethod"]


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # strip stray whitespace in text columns
    text_cols = df.select_dtypes(exclude="number").columns
    df[text_cols] = df[text_cols].apply(lambda s: s.str.strip())

    # TotalCharges: text -> number; blank means a brand-new customer (tenure 0) -> 0
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    new_customer = df["tenure"] == 0
    df.loc[new_customer, "TotalCharges"] = df.loc[new_customer, "TotalCharges"].fillna(0.0)

    # same customer twice -> keep one
    df = df.drop_duplicates(subset="customerID")

    # target to 0/1
    if "Churn" in df and not pd.api.types.is_numeric_dtype(df["Churn"]):
        df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})

    return df


def simplify_services(df):
    df = df.copy()
    service_cols = addon_cols + ["MultipleLines"]
    df[service_cols] = df[service_cols].replace({"No internet service": "No", "No phone service": "No"})
    return df


def add_features(df):
    df = df.copy()
    df["is_first_year"] = (df["tenure"] <= 12).astype(int)
    df["has_internet"] = (df["InternetService"] != "No").astype(int)
    df["addon_count"] = df[addon_cols].eq("Yes").sum(axis=1)
    df["autopay"] = df["PaymentMethod"].str.contains("automatic").astype(int)

    n_services = (df["PhoneService"] == "Yes").astype(int) + df["has_internet"] + df["addon_count"]
    df["spend_per_service"] = df["MonthlyCharges"] / n_services.clip(lower=1)
    return df


def prepare(df):
    df = add_features(simplify_services(df))
    df[yes_no_cols] = df[yes_no_cols].apply(lambda s: s.map({"Yes": 1, "No": 0}))
    return df.drop(columns=DROP_COLS)


def to_features(df, encoder):
    encoded = pd.DataFrame(encoder.transform(df[cat_cols]),
                           columns=encoder.get_feature_names_out(cat_cols), index=df.index)
    return pd.concat([df.drop(columns=cat_cols), encoded], axis=1)


def transform_features(df, encoder, feature_columns):
    """Apply our notebook steps, then select only the saved model inputs."""
    features = to_features(prepare(df), encoder)
    features = features.drop(columns=[ID_COL, TARGET], errors="ignore")
    if set(features.columns) != set(feature_columns):
        raise ValueError("Feature schema does not match the saved encoder and model.")
    features = features[feature_columns]
    if not np.isfinite(features.to_numpy(dtype=float)).all():
        raise ValueError("Prepared features contain missing or non-finite values.")
    return features


# Data-contract definitions for Week 5 validation, not new feature rules.
DOMAINS = {"gender": ["Male", "Female"], "SeniorCitizen": [0, 1],
           "InternetService": ["DSL", "Fiber optic", "No"],
           "Contract": ["Month-to-month", "One year", "Two year"],
           "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]}
DOMAINS.update({c: ["Yes", "No"] for c in yes_no_cols})
DOMAINS.update({c: ["Yes", "No", "No internet service"] for c in addon_cols})
DOMAINS["MultipleLines"] = ["Yes", "No", "No phone service"]

CUSTOMER_COLUMNS = ["customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService"] + addon_cols + ["Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges"]
