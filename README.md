# Vulnus Ultimate Auto Mapper

**Author:** @bubupack & AI Assistant

## Description

This enhanced program automatically generates a complete Vulnus map pack by analyzing the rhythm and intensity of an audio file. It uses advanced zenei analysis to detect BPM and snap notes to the beat for a better gameplay experience.

## Key Features

- **Multi-Difficulty Generation:** Automatically creates `easy.json`, `medium.json`, `hard.json`, and `impossible.json` in one go.
- **Rhythm Snapping:** Detects BPM and beats, snapping notes to the grid for professional feel.
- **Metadata Support:** Dedicated fields for Artist and Mapper names.
- **Improved UI:** Modernized interface with a Progress Bar and status updates.
- **Automatic Packaging:** Copies the audio file and creates `meta.json` correctly.

## Prerequisites

To use this program, you must have Python installed along with:

- `librosa`
- `numpy`

## Usage

1. Run the script `Vulnus_auto_mapper.py`.
2. Enter the **Song Name**, **Artist**, and **Mapper**.
3. Select your audio file (.mp3, .wav, .ogg, or .webm).
4. Click **"GENERATE MULTI-DIFFICULTY MAP"**.
5. Find your complete map folder in your **Downloads** directory.

## Technical Details

- Uses `librosa.beat.beat_track` for rhythm analysis.
- Peak picking sensitivity is adjusted per difficulty.
- Snaps notes to the nearest beat if they fall within 100ms of it.
- Files generated: `meta.json`, `easy.json`, `medium.json`, `hard.json`, `impossible.json`, and the audio file.

## Credits

Original code by @bubupack, enhanced with AI assistance.
