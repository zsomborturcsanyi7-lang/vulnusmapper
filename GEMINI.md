# VulnusMapper

Automated mapping workflow for the rhythm game **Vulnus**. This project combines music downloading capabilities with intelligent audio analysis to generate playable map packs.

## Project Overview

The project consists of two main components:
1.  **Audio Analysis & Mapping (`Vulnus_auto_mapper.py`):** A Python application (with a Tkinter GUI) that analyzes audio files using `librosa` to detect beats and energy peaks, automatically generating Vulnus map files (`meta.json` and difficulty JSONs).
2.  **Spotify Downloader (`spotifydownload-master/`):** A Go-based tool (forked or adapted from `spotifydownload`) used to download tracks and playlists from Spotify. It also provides the bundled `ffmpeg.exe` used by the Python script for audio processing.

### Key Technologies
- **Python:** `librosa`, `numpy`, `tkinter`.
- **Go:** Used for the music downloader.
- **FFmpeg:** Crucial for audio format conversion and analysis.

## Building and Running

### Prerequisites
- **Python 3.x:** Ensure `librosa` and `numpy` are installed:
  ```bash
  pip install librosa numpy
  ```
- **Go (Optional):** Required only if you want to rebuild the downloader.
- **FFmpeg:** Included in `spotifydownload-master/ffmpeg.exe`.

### Execution Commands
- **Main GUI:**
  ```bash
  python Vulnus_auto_mapper.py
  ```
  This opens a GUI where you can search/download (via the internal Go tool) and generate maps.
- **Batch Processing:**
  ```bash
  python process_all.py
  ```
  Processes all downloaded `.m4a` files in the `spotifydownload-master/Popular songs` directory. *Note: Ensure CLI support is fully implemented in `Vulnus_auto_mapper.py` for this to work correctly.*
- **Manual Downloader:**
  ```bash
  cd spotifydownload-master
  go run main.go -playlist <URL>
  # OR use the executable
  .\spotifydownload.exe
  ```

## Directory Structure
- `Vulnus_auto_mapper.py`: Main logic for beat detection and map generation.
- `process_all.py`: Utility script for batch processing downloaded songs.
- `downloads/`: Default output directory for generated maps.
- `spotifydownload-master/`: Contains the downloader source, binary, and `ffmpeg`.
  - `Popular songs/`: Default download location for Spotify tracks.

## Development Conventions
- **Audio Analysis:** Uses `librosa.beat.beat_track` for BPM detection and `librosa.util.peak_pick` for note placement based on audio energy.
- **Map Structure:** Generates maps compatible with Vulnus, including a `meta.json` and multi-difficulty JSON files.
- **FFmpeg Integration:** The Python script automatically adds the `spotifydownload-master` directory to the system PATH to locate `ffmpeg.exe`.
