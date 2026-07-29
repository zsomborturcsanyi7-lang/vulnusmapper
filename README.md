# vulnusmapper

Librosa-based automatic rhythm game map and beat detection script for Vulnus map files.

## 📌 Overview & Purpose
An automated tool designed to analyze audio files (e.g., MP3, WAV) and generate compatible map files (`map.json`) based on detected beats for the Vulnus rhythm game.

## ⚙️ Tech Stack & Architecture
- **Language**: Python 3.10+
- **Audio Processing**: `librosa`, `numpy`
- **Output Format**: JSON formatted according to Vulnus map specifications

## 🚀 Installation & Quickstart

### Prerequisites
- Python 3.10+
- FFmpeg (recommended for audio decoding)

### Steps
```bash
git clone https://github.com/zsomborturcsanyi7-lang/vulnusmapper.git
cd vulnusmapper

# Set up virtual environment and dependencies
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Generate map from audio
python mapper.py --input song.mp3 --output map.json
```

## 📊 Project Status
⚠️ **Functional Experimental Tool**.
