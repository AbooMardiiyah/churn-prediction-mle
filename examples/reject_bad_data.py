"""A deliberate failure demp. """

import pandas as pd
from src.utils.paths import RAW_DIR, PROJECT_ROOT
from src.feature_pipeline.validate import validate_data


bad_df = pd.read_csv(RAW_DIR / "train.csv").head(10).copy()

bad_df.loc[bad_df.index[0], "tenure"] = -5
validate_data(bad_df, PROJECT_ROOT / "reports/week5/deliberate_failure.json")
