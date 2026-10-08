# Getting started

How to run this project on your own computer. Pick the section for your system: **Windows**, **Ubuntu / Linux / WSL**, or **macOS**.
Everything after Step 2 is the same on all of them.

You do **not** need to install Python yourself. `uv` downloads the right version for you.

---

## Step 1. Install Git

**Windows** (PowerShell):
```powershell
winget install --id Git.Git -e
```
Close and reopen PowerShell, then check:
```powershell
git --version
```

**Ubuntu / Linux / WSL:**
```bash
sudo apt update && sudo apt install -y git curl
git --version
```

**macOS:**
```bash
brew install git
```

Tell Git who you are (once per computer):
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Step 2. Install uv

`uv` creates the project's environment and installs the exact package versions from `uv.lock`.

**Windows** (PowerShell):
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
(or `winget install --id=astral-sh.uv -e`)

**Ubuntu / Linux / WSL / macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Close the terminal and open a new one**, then check:
```bash
uv --version
```

## Step 3. Get the code

```bash
git clone https://github.com/<owner>/churn-prediction-mle.git
cd churn-prediction-mle
```

*WSL users:* clone inside the Linux file system (for example `~/projects`), **not** under `/mnt/c/...`. It is much faster and avoids permission quirks.

## Step 4. Create the environment

```bash
uv sync
```

This creates a `.venv` folder in the project and installs everything. It takes a minute the first time.

## Step 5. Register the notebook kernel

```bash
uv run python -m ipykernel install --user --name churn-mle --display-name "Python (churn-mle)"
```

In **VS Code**: open the project folder, open a notebook, click **Select Kernel** (top right), choose **Jupyter Kernel**, then **Python (churn-mle)**.
If it is not listed, choose **Python Environments** and pick the one inside `.venv`.

*WSL users:* open VS Code **from the WSL terminal** with `code .`, and install the **WSL** extension if VS Code asks. Install the **Python** and **Jupyter** extensions when it offers to "install in WSL".

## Step 6. Download the data and run the tests

```bash
uv run python -m src.feature_pipeline.load
uv run pytest
```

The first command downloads the dataset from Kaggle into `data/raw/`. You should see `✅ Downloaded ...`.
The second should show all tests passing.

## Step 7. Run the notebooks in order

1. `notebooks/00_data_split.ipynb`, then
2. `notebooks/01_EDA_cleaning.ipynb`

Use **Run All**, or run cell by cell with `Shift+Enter`.

## Every week after this

```bash
git pull        # get the new code
uv sync         # install any new packages
```

---

## Troubleshooting

| Problem | What to try |
|---|---|
| `uv: command not found` / `'uv' is not recognized` | Close the terminal and open a new one. On Linux you can also run `source $HOME/.local/bin/env` |
| `git: command not found` | Redo Step 1, then open a new terminal |
| PowerShell says "running scripts is disabled" | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry |
| Kernel "Python (churn-mle)" not in the list | Run Step 5 again, then in VS Code press `Ctrl+Shift+P` → **Developer: Reload Window** |
| `ModuleNotFoundError: No module named 'src'` | Run `uv sync` from the project folder. Make sure the kernel is **Python (churn-mle)** |
| Kaggle download fails (network or firewall) | Download the CSV by hand from <https://www.kaggle.com/datasets/blastchar/telco-customer-churn> and save it as `data/raw/telco_churn.csv` |
| `uv sync` is very slow or shows a "hardlink" warning on WSL | The project is under `/mnt/c`. Move it into the Linux home folder, or run `export UV_LINK_MODE=copy` |
| Something is broken and you cannot tell why | Delete the `.venv` folder and run `uv sync` again. It is safe, nothing of yours is stored there |
