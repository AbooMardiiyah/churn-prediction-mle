from src.utils.paths import DATA_DIR, RAW_DIR
import kagglehub
import os
import shutil
from pathlib import Path

KAGGLE_DATASET = "blastchar/telco-customer-churn"
RAW_FILENAME= "telco_churn.csv"

def download_raw_data(raw_dir: Path | str = RAW_DIR, force: bool= False)-> Path:
    """Download the dataset from kaggle once and copies ito the raw_dir/telco_churn.csv"""

    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / RAW_FILENAME

    if target.exists() and not force:
        print(f"✅ Raw data already at {target}")

        return target

    os.environ.setdefault("KAGGLEHUB_CACHE", str(DATA_DIR / ".kagglehub")
                          )
    try:
        folder = Path(kagglehub.dataset_download(KAGGLE_DATASET, force_download=force))
    except Exception as exc:
        raise RuntimeError(
            f"Could not download '{KAGGLE_DATASET}' from Kaggle ({exc}). "
            f"Download the CSV manually from https://www.kaggle.com/datasets/{KAGGLE_DATASET} "
            f"and save it as {target}"
        ) from exec 

    csv_files = sorted(folder.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV file found in the downloaded dataset at {folder}")

    shutil.copy(csv_files[0], target)
    print(f"✅ Downloaded {csv_files[0].name} -> {target}")
    return target


if __name__ == "__main__":
    download_raw_data()