# vulnusmapper

Librosa-based automated rhythm map generator for Vulnus.

## Overview & Purpose
vulnusmapper is a Python automation utility that analyzes audio files to detect musical beats, onset envelopes, and tempo patterns. It converts extracted audio data into valid JSON map files compatible with the Vulnus rhythm game engine.

## Key Features
- Automated onset detection and tempo estimation using signal processing algorithms.
- Configurable difficulty parameters and note spacing algorithms.
- Direct export to Vulnus-compliant JSON format.
- Batch processing support for multiple audio tracks.

## Tech Stack & Dependencies
- **Language**: Python 3.10+
- **Audio Processing**: Librosa, NumPy, SciPy
- **Data Export**: Standard Library JSON

## Project Structure
```text
vulnusmapper/
├── mapper.py
├── utils/
├── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.10+
- FFmpeg (required for audio decoding)

### Steps
```bash
# Clone repository
git clone https://github.com/zsomborturcsanyi7-lang/vulnusmapper.git
cd vulnusmapper

# Virtual environment setup
python -m venv venv
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

## Usage Examples
```bash
python mapper.py --input path/to/song.mp3 --output path/to/map.json --sensitivity 0.8
```

## Status & License
Status: Functional Utility / Experimental.
License: MIT
