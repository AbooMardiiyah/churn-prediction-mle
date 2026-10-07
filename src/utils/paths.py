import os
from pathlib import Path

MARKER = "pyproject.toml"

def find_project_root(start: Path | str | None = None, marker: str = MARKER) -> Path:
    """Walk up from `start` (default: this file) until a folder containing `marker` is found."""
    override = os.environ.get("CHURN_PROJECT_ROOT")
    if override and start is None:
        return Path(override).resolve()

    start_path = Path(start) if start is not None else Path(__file__)
    start_path = start_path.resolve()
    for folder in [start_path, *start_path.parents]:
        if (folder / marker).exists():
            return folder
    raise FileNotFoundError(f"Could not find '{marker}' above {start_path}")


PROJECT_ROOT = find_project_root()

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
CONFIGS_DIR = PROJECT_ROOT / "configs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

