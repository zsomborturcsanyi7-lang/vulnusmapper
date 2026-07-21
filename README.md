# VulnusMapper — Rhythm Game Map Auto-Generator from Spotify/YouTube Audio

**Status:** ⚠️ Prototype — beat detection works, map generation tested

Spotify/YouTube music downloader + librosa beat detector that automatically generates rhythm game maps based on beat patterns.

## ⚠️ THIS PROJECT IS UNFINISHED — FEEL FREE TO CONTINUE IT ⚠️

This project was developed by Zsombi & Hermes Agent (Nous Research).

---

## Pipeline
1. **Music download** — from Spotify playlists or YouTube links (yt-dlp)
2. **Beat detection** — BPM, beats, audio characteristics via librosa
3. **Map generation** — Automatic rhythm game level generation from detected beats
4. **Motif recognition** — Repeating musical pattern detection and varied map elements

## Files
| File | Description |
|------|-------------|
| `Vulnus_auto_mapper.py` | Main mapper script (442 lines) |
| `process_all.py` | Batch processor |
| `youtube_downloader.py` | YouTube downloader |
| `vulnus_ai_bot.py` | AI bot |

## Developer
Zsombi & Hermes Agent (Nous Research)
