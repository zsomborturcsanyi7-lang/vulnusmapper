# VulnusMapper — Rhythm Game Map Auto-Generator

**A Spotify/YouTube music downloader + librosa beat detector that automatically generates rhythm game maps based on beat patterns.**

## 🎵 Description

VulnusMapper is a complete pipeline that:

1. **Downloads music** — from Spotify playlists or YouTube links (yt-dlp)
2. **Detects beats** — analyzes BPM, beats, and audio characteristics via librosa
3. **Generates maps** — automatically produces rhythm game levels from detected beats
4. **Recognizes motifs** — detects repeating musical patterns and creates varied map elements

Supported formats: MP3, WAV, FLAC, OGG, M4A

### NeonWave V4

The project includes **NeonWave V4** — a standalone EXE version built with PyInstaller that bundles the YouTube downloader and mapper functionality.

## 📁 File Structure

```
VulnusMapper/
├── Vulnus_auto_mapper.py        # Main mapper script (442 lines)
├── process_all.py               # Batch processor — for all downloaded tracks
├── youtube_downloader.py        # YouTube downloader (Spotify/YT support)
├── youtube_downloader.exe       # Compiled YouTube downloader
├── youtube_downloader.spec      # PyInstaller spec file
├── NeonWaveDownloader.spec      # NeonWave build spec
├── YouTubeDownloader.spec       # YouTube downloader spec
├── NeonWave_V4.spec             # NeonWave V4 build spec
├── profilkepyoutubenak.ico      # Application icon
├── downloads/                   # Downloaded music
│   ├── batch_0_*.mp3
│   ├── batch_1_*.mp3
│   ├── batch_2_*.mp3
│   └── batch_3_*.mp3
├── build/
│   └── NeonWave_V4/             # PyInstaller build files
├── dist/
│   └── youtube_downloader.exe   # Distributable exe
├── mapper_errors.log            # Mapper error log
├── youtube_downloader.log       # Downloader log
└── README.md
```

## 🚀 Usage

### Downloading music

```bash
# Launch YouTube downloader
python youtube_downloader.py

# Or use the compiled executable
youtube_downloader.exe
```

### Generating a map for a track

```bash
python Vulnus_auto_mapper.py
```

The script:
1. Prompts for the audio file path
2. Analyzes BPM and beats
3. Detects musical motifs
4. Generates the map file

### Batch processing

```bash
# Generate maps for all downloaded tracks
python process_all.py
```

### Automatic dependency installation

`Vulnus_auto_mapper.py` automatically checks for and installs missing packages on startup.

## 📦 Dependencies

```bash
pip install librosa numpy yt-dlp
```

- **Python 3.8+**
- **librosa** — music analysis, beat detection
- **numpy** — numerical computations
- **yt-dlp** — YouTube/Spotify downloading
- **PyInstaller** (optional) — for building EXE

## 🎮 Output Format

Generated map files contain:
- **BPM** — tempo information
- **Beat positions** — timestamps in milliseconds
- **Difficulty level** — automatically determined
- **Motif variations** — diverse map elements at musical repetitions
- **Sound effect markers** — triggers for special elements

## ⚠️ Legal Note

This tool is intended for **personal use only**. Downloading and using copyrighted music is governed by local laws. Only download content for which you have appropriate rights.

## Author
Zsombi & Hermes Agent (Nous Research)
