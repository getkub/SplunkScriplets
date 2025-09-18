# MoneyPrinterTurbo — macOS Installation Guide

This README gives **step‑by‑step** instructions to install and run **MoneyPrinterTurbo** on macOS (Intel or Apple Silicon). It follows the project's recommended manual installation flow and adds macOS‑specific tips (Homebrew, ffmpeg, ImageMagick, virtualenv/conda).

> Tested target: macOS 11.0+ (the project recommends macOS 11 or newer). 

---

## Quick overview

1. Install Homebrew (if you don't have it).
2. Install system deps: `imagemagick`, `ffmpeg`, `git`.
3. Clone repo.
4. Create a Python environment (conda recommended) with **Python 3.11** and install Python requirements.
5. Copy and edit `config.example.toml` → `config.toml` and add any API keys (LLM provider, Pexels, etc.).
6. Start the Web UI (`sh webui.sh`) and/or API (`python main.py`).

---

## 0) Notes & prerequisites

* macOS 11.0 or newer is recommended.
* CPU: 4 cores and 4GB RAM minimum (project recommends this as baseline).
* A stable Internet connection is required for model/API access and for downloading some tools.
* Avoid using Chinese or special characters in the project path.

---

## 1) Install Homebrew (if not installed)

Open Terminal and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After install, follow any printed instructions to add `brew` to your `PATH` (especially on Apple Silicon where Homebrew often lives in `/opt/homebrew`).

---

## 2) Install system packages (ImageMagick, FFmpeg, git)

MoneyPrinterTurbo uses ImageMagick and FFmpeg for image/video processing. Install them via Homebrew:

```bash
brew update
brew install git imagemagick ffmpeg ghostscript
```

`ghostscript` is recommended for ImageMagick font handling on some systems.

If you already have these installed, make sure `which ffmpeg` and `which convert` (ImageMagick) return valid paths.

---

## 3) Clone the repository

```bash
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo
```

---

## 4) Python environment (Recommended: conda / mambaforge)

The project recommends `python=3.11`. You can use conda/mambaforge or a venv/pyenv-based workflow. Using conda (recommended):

```bash
# If you use miniconda/mambaforge, install that first from their website.
conda create -n MoneyPrinterTurbo python=3.11 -y
conda activate MoneyPrinterTurbo

# From the project root:
pip install -r requirements.txt
```

If you prefer a venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> If you run into compilation errors for wheels, consider installing Xcode Command Line Tools first:
> `xcode-select --install`

---

## 5) Configuration

1. Copy the example config file:

```bash
cp config.example.toml config.toml
```

2. Edit `config.toml` and fill in keys you want to use, e.g. `pexels_api_keys`, `llm_provider` and provider API keys, optional `imagemagick_path`, or `ffmpeg_path` if you want to override automatic discovery.

3. Optional: set environment variables if you prefer, e.g. on macOS (bash/zsh):

```bash
export IMAGEIO_FFMPEG_EXE="/opt/homebrew/bin/ffmpeg"
export PATH="$PATH:/opt/homebrew/bin"
```

---

## 6) Start the Web UI (macOS)

From the project root run:

```bash
sh webui.sh
```

This script starts the Streamlit Web UI and should automatically open a browser at the UI address. If it does not open automatically, visit:

```
http://0.0.0.0:8501
```

---

## 7) Start the API (optional)

To run the backend API (for direct API access or custom automation):

```bash
python main.py
```

Then API docs are available at:

```
http://127.0.0.1:8080/docs
```

---

## 8) Subtitles / Whisper mode (optional)

The project supports two subtitle modes: `edge` (faster) and `whisper` (higher quality). If you enable `whisper` you may need to download a large model from Hugging Face (the repo mentions a ~3GB model for some whisper setups). Put the model where the project expects it or configure the path in the config.

---

## 9) FFmpeg "not found" troubleshooting

If you see an error like `RuntimeError: No ffmpeg exe could be found. Install ffmpeg on your system, or set the IMAGEIO_FFMPEG_EXE environment variable.`:

* Confirm `ffmpeg` is installed and `which ffmpeg` returns a path.
* Set `ffmpeg_path` in `config.toml` or export `IMAGEIO_FFMPEG_EXE` to your `ffmpeg` binary path.

Example `config.toml` snippet:

```toml
[app]
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"  # adjust to your ffmpeg path
```

---

## 10) Common tips & troubleshooting

* Ensure you do **not** have non-ASCII characters in the project path.
* If Streamlit or other dependencies fail, try recreating the environment and reinstalling `requirements.txt`.
* If a Python package fails to build on M1/Apple Silicon, try using conda/mambaforge (many prebuilt packages are available there).
* Keep an eye on the console logs—they show missing model / API key warnings which are usually the root cause.

---

## 11) Example quick run (copy‑paste)

```bash
# 1) Install system deps (once)
brew update && brew install git imagemagick ffmpeg ghostscript

# 2) Clone and setup
git clone https://github.com/harry0703/MoneyPrinterTurbo.git
cd MoneyPrinterTurbo

# 3) Python env
conda create -n MoneyPrinterTurbo python=3.11 -y
conda activate MoneyPrinterTurbo
pip install -r requirements.txt

# 4) Configure
cp config.example.toml config.toml
# edit config.toml to add api keys / providers

# 5) Start web UI
sh webui.sh

# 6) (optional) Run API
# python main.py
```

---

## 12) Where to get help

* Project repo: https://github.com/harry0703/MoneyPrinterTurbo
* Check Issues on the repo if you hit project-specific bugs.

---

## License

This guide is provided as-is. MoneyPrinterTurbo is MIT licensed (see project). 

---

If you want, I can also:

* Produce a one‑liner `brew` + `conda` script you can paste in Terminal to automate these steps.
* Produce a separate Apple Silicon note for common M1/M2 gotchas.

