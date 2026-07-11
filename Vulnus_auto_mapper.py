########################################################################################################################################################################################################
# Vulnus Ultimate Auto Mapper - RHYTHM & MOTIF EDITION
# Credit @bubupack & AI Assistant
########################################################################################################################################################################################################

import os
import sys
import subprocess
import shutil

import logging
import time

# --- LOGGING SETUP ---
logging.basicConfig(
    filename='mapper_errors.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def ensure_dependencies():
    """Checks for required packages and installs them if missing."""
    required_packages = ["librosa", "numpy", "yt-dlp"]
    missing_packages = []
    
    for pkg in required_packages:
        try:
            __import__(pkg.replace("-", "_"))
        except ImportError:
            missing_packages.append(pkg)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}. Attempting to install...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *missing_packages])
            logging.info(f"Installed missing packages: {missing_packages}")
        except Exception as e:
            logging.error(f"Failed to install packages: {e}")
            
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
        logging.info("Updated yt-dlp to the latest version.")
    except Exception as e:
        logging.warning(f"Could not update yt-dlp: {e}")
            
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_local_path = os.path.join(script_dir, "spotifydownload-master")
    ffmpeg_exe = os.path.join(ffmpeg_local_path, "ffmpeg.exe")
    
    if not os.path.exists(ffmpeg_exe) and not shutil.which("ffmpeg"):
        msg = "CRITICAL: FFmpeg not found! Please place ffmpeg.exe in 'spotifydownload-master' folder."
        print(msg)
        logging.error(msg)

# Run the dependency check before anything else
ensure_dependencies()

import librosa
import numpy as np
import random
import platform
import math
import hashlib
import tkinter as tk
import json
import threading
import traceback
import tempfile
from tkinter import filedialog, ttk, messagebox

# --- ADD LOCAL FFMPEG TO PATH ---
script_dir = os.path.dirname(os.path.abspath(__file__))
ffmpeg_local_path = os.path.join(script_dir, "spotifydownload-master")
ffmpeg_exe = os.path.join(ffmpeg_local_path, "ffmpeg.exe")

if os.path.exists(ffmpeg_exe):
    if ffmpeg_local_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_local_path + os.pathsep + os.environ["PATH"]
# --------------------------------

def get_default_download_dir():
    return os.path.join(os.path.expanduser("~"), "Downloads")

def generate_difficulty(times, positions, difficulty_name, approach_time=1.0, approach_dist=50):
    diff_data = {
        "_approachDistance": approach_dist,
        "_approachTime": approach_time,
        "_name": difficulty_name,
        "_notes": []
    }
    for i in range(len(times)):
        diff_data["_notes"].append({
            "_time": round(float(times[i]), 3),
            "_x": int(positions[i][0] - 1),
            "_y": int(positions[i][1] - 1)
        })
    return diff_data

def get_pattern_positions(times, intensities, song_name="", frequencies=None):
    """
    Advanced pattern generation with MOTIF recognition and SYMMETRY.
    If a rhythm repeats, the pattern is mirrored or inverted.
    """
    import hashlib
    seed_hash = int(hashlib.sha256(song_name.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed_hash)
    
    positions = []
    curr_x, curr_y = 1, 1 
    
    # Motif tracking
    motif_memory = {} # signature -> (last_positions, transform_index)
    window_size = 4   # Look back at sequences of 4 notes
    
    # Mode variables
    mode = "flow"
    mode_timer = 0
    angle = random.uniform(0, 3.14 * 2)
    
    def apply_transform(pos_list, index):
        """Applies a symmetry transformation: 0=Original, 1=Mirror H, 2=Mirror V, 3=Full Invert"""
        new_list = []
        for (x, y) in pos_list:
            if index == 1: new_list.append((2 - x, y))
            elif index == 2: new_list.append((x, 2 - y))
            elif index == 3: new_list.append((2 - x, 2 - y))
            else: new_list.append((x, y))
        return new_list

    for i in range(len(times)):
        # Chord detection
        is_chord = False
        if i > 0 and abs(times[i] - times[i-1]) < 0.005:
            is_chord = True
        
        if is_chord:
            last_x, last_y = positions[-1]
            candidates = [(cx, cy) for cx in range(3) for cy in range(3) if abs(cx-last_x)+abs(cy-last_y) >= 2]
            curr_x, curr_y = random.choice(candidates) if candidates else ((last_x + 2) % 3, (last_y + 1) % 3)
            positions.append((curr_x, curr_y))
            continue

        # Rhythm Signature calculation
        # We look at the time differences of the last few notes
        if i >= window_size:
            dts = [round(times[j] - times[j-1], 2) for j in range(i - window_size + 1, i + 1)]
            signature = tuple(dts)
            
            if signature in motif_memory:
                # REPEAT DETECTED!
                prev_positions, transform_idx = motif_memory[signature]
                # Cycle through transformations: 1 -> 2 -> 3 -> 0
                new_transform_idx = (transform_idx + 1) % 4
                
                # Get the last sequence of positions we used for this motif
                # and transform it
                new_seq = apply_transform(prev_positions, new_transform_idx)
                
                # Use the next position from the transformed sequence
                # (Note: this is simplified, we just pick the 'current' one)
                curr_x, curr_y = new_seq[-1]
                
                # Update memory
                motif_memory[signature] = (prev_positions, new_transform_idx)
                positions.append((curr_x, curr_y))
                continue
            else:
                # New rhythm, start tracking it later
                pass

        # Standard Procedural Placement (if no motif match)
        dt = times[i] - (times[i-1] if i > 0 else 0)
        intense = intensities[i]
        freq = frequencies[i] if frequencies is not None else 0.5
        
        # Frequency balance: map frequency range to full grid
        # High and Low are equal: Low = Bottom/Left, High = Top/Right
        if freq < 0.3: # Bass
            target_x, target_y = random.randint(0, 1), 2
        elif freq > 0.7: # Treble
            target_x, target_y = random.randint(1, 2), 0
        else: # Mid
            target_x, target_y = 1, 1

        mode_timer -= 1
        if mode_timer <= 0 or (intense > 0.8):
            r = random.random()
            if intense > 0.9: mode = "chaos"
            elif intense > 0.7: mode = "jump"
            elif r < 0.3: mode = "flow"
            elif r < 0.6: mode = "stream"
            else: mode = "spiral"
            mode_timer = random.randint(4, 12)

        if mode == "stream":
            curr_x = (curr_x + 1) % 3
            if random.random() > 0.7: curr_y = (curr_y + 1) % 3
        elif mode == "jump":
            curr_x, curr_y = 2 - curr_x, 2 - curr_y
        elif mode == "spiral":
            if curr_y == 0 and curr_x < 2: curr_x += 1
            elif curr_x == 2 and curr_y < 2: curr_y += 1
            elif curr_y == 2 and curr_x > 0: curr_x -= 1
            elif curr_x == 0 and curr_y > 0: curr_y -= 1
        elif mode == "chaos":
            curr_x, curr_y = random.randint(0, 2), random.randint(0, 2)
        else: # Flow
            angle += 1.0
            curr_x = int(1 + round(math.cos(angle)))
            curr_y = int(1 + round(math.sin(angle)))

        # Sanity check position
        curr_x = max(0, min(2, curr_x))
        curr_y = max(0, min(2, curr_y))
        
        # Avoid stack unless intended
        if i > 0 and (curr_x, curr_y) == positions[-1] and dt < 0.15:
            curr_x = (curr_x + 1) % 3

        positions.append((curr_x, curr_y))
        
        # Store motif window if full
        if i >= window_size:
            dts = [round(times[j] - times[j-1], 2) for j in range(i - window_size + 1, i + 1)]
            sig = tuple(dts)
            pos_window = positions[-window_size:]
            if sig not in motif_memory:
                motif_memory[sig] = (pos_window, 0)

    return positions

def robust_load_audio(path):
    try:
        return librosa.load(path, sr=None)
    except Exception:
        if not os.path.exists(ffmpeg_exe) and not shutil.which("ffmpeg"):
            raise RuntimeError("FFmpeg not found!")
        fd, temp_wav = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
        try:
            cmd = [ffmpeg_exe if os.path.exists(ffmpeg_exe) else "ffmpeg", "-y", "-i", path, "-vn", "-acodec", "pcm_s16le", "-ar", "44100", "-ac", "1", temp_wav]
            subprocess.run(cmd, check=True, capture_output=True)
            return librosa.load(temp_wav, sr=None)
        finally:
            if os.path.exists(temp_wav): os.remove(temp_wav)

def perform_mapping_logic(audio_path, song_name, base_density=6, manual_speed=0.8, progress_callback=None):
    def log_status(msg):
        if progress_callback: progress_callback(msg)
        else: print(msg)

    log_status(f"Analyzing {song_name}...")
    y, sr = robust_load_audio(audio_path)
    
    # Split audio for better beat detection
    y_harmonic, y_percussive = librosa.effects.hpss(y)
    tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    
    # Analysis features
    hop_length = 512
    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_env = (onset_env - np.min(onset_env)) / (np.max(onset_env) - np.min(onset_env) + 1e-6)
    
    spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr, hop_length=hop_length)[0]
    spec_centroid_norm = (spec_centroid - np.min(spec_centroid)) / (np.max(spec_centroid) - np.min(spec_centroid) + 1e-6)

    rms = librosa.feature.rms(y=y)[0]
    rms_norm = (rms - np.min(rms)) / (np.max(rms) - np.min(rms) + 1e-6)
    
    # Difficulties
    difficulties = [
        {"name": "Normal", "density_mult": 0.6 * (base_density / 5), "speed": max(manual_speed, 1.2)},
        {"name": "Hard", "density_mult": 1.5 * (base_density / 5), "speed": manual_speed},
        {"name": "Expert", "density_mult": 3.5 * (base_density / 5), "speed": min(manual_speed, 0.7)},
        {"name": "GALAXY", "density_mult": 8.0 * (base_density / 5), "speed": 0.25}
    ]
    
    safe_name = "".join([c if c.isalnum() or c in " .-_()" else "_" for c in song_name])
    map_dir = os.path.join(get_default_download_dir(), safe_name)
    if not os.path.exists(map_dir): os.makedirs(map_dir)
    
    dest_mp3 = os.path.join(map_dir, "music.mp3")
    if audio_path.lower().endswith(".mp3"): shutil.copy(audio_path, dest_mp3)
    else:
        log_status("Converting to MP3...")
        cmd = [ffmpeg_exe if os.path.exists(ffmpeg_exe) else "ffmpeg", "-y", "-i", audio_path, "-vn", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", dest_mp3]
        subprocess.run(cmd, capture_output=True)

    difficulty_files = []
    for diff in difficulties:
        log_status(f"Generating {diff['name']}...")
        delta_val = 0.05 / (diff["density_mult"] + 0.1)
        peaks = librosa.util.peak_pick(onset_env, pre_max=3, post_max=3, pre_avg=5, post_avg=5, delta=delta_val, wait=0)
        raw_times = librosa.frames_to_time(peaks, sr=sr, hop_length=hop_length)
        
        final_times, intensities, freqs = [], [], []
        chord_threshold = 0.7 if diff["name"] in ["Expert", "GALAXY"] else 1.1
        
        for t in raw_times:
            frame = int(t * sr / hop_length)
            if frame >= len(onset_env): continue
            local_onset = onset_env[frame]
            local_energy = rms_norm[min(frame, len(rms_norm)-1)]
            local_freq = spec_centroid_norm[min(frame, len(spec_centroid_norm)-1)]
            
            threshold_mod = 0.1 if local_energy > 0.6 else 0.0
            if local_onset > (0.12 / diff["density_mult"]) - threshold_mod:
                selected_time = t
                if len(beat_times) > 0:
                    closest_beat = beat_times[np.argmin(np.abs(beat_times - t))]
                    if abs(t - closest_beat) < 0.06: selected_time = closest_beat
                
                final_times.append(selected_time)
                intensities.append(local_onset)
                freqs.append(local_freq)
                
                if local_onset > chord_threshold:
                    final_times.append(selected_time); intensities.append(local_onset); freqs.append(local_freq)
                if diff["name"] == "GALAXY" and local_onset > 0.9:
                    final_times.append(selected_time); intensities.append(local_onset); freqs.append(local_freq)

        if final_times:
            combined = sorted(zip(final_times, intensities, freqs), key=lambda x: x[0])
            final_times, intensities, freqs = zip(*combined)
            positions = get_pattern_positions(final_times, intensities, song_name=song_name, frequencies=freqs)
            
            diff_filename = f"{diff['name'].lower()}.json"
            diff_data = generate_difficulty(final_times, positions, diff["name"], approach_time=diff["speed"])
            with open(os.path.join(map_dir, diff_filename), "w") as f: json.dump(diff_data, f, indent=4)
            difficulty_files.append(diff_filename)

    with open(os.path.join(map_dir, "meta.json"), "w") as f:
        json.dump({"_artist": "AutoMapper AI", "_difficulties": difficulty_files, "_mappers": ["VulnusIntelligent"], "_music": "music.mp3", "_title": song_name, "_version": 1}, f, indent=4)
    log_status(f"Map pack saved: {map_dir}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vulnus Auto Mapper - RHYTHM EDITION")
        self.root.geometry("650x750")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # TAB 1: Search
        self.search_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.search_frame, text="1. Search & Download")
        ttk.Label(self.search_frame, text="Search Song(s):", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)
        self.search_entry = ttk.Entry(self.search_frame, width=60)
        self.search_entry.pack(fill=tk.X, pady=10)
        self.dl_button = ttk.Button(self.search_frame, text="SEARCH & AUTO-MAP ALL", command=self.start_batch_process)
        self.dl_button.pack(pady=10, fill=tk.X)
        self.dl_status = ttk.Label(self.search_frame, text="Ready")
        self.dl_status.pack()

        # TAB 2: Map Generation
        self.map_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(self.map_frame, text="2. Map Generation")
        self.audio_path = tk.StringVar()
        ttk.Label(self.map_frame, text="Audio File:").pack(anchor=tk.W)
        f_frame = ttk.Frame(self.map_frame); f_frame.pack(fill=tk.X, pady=5)
        ttk.Entry(f_frame, textvariable=self.audio_path, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(f_frame, text="Browse", command=self.browse_file).pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(self.map_frame, text="Song Title:").pack(anchor=tk.W)
        self.song_entry = ttk.Entry(self.map_frame); self.song_entry.pack(fill=tk.X, pady=5)
        
        self.reco_label = ttk.Label(self.map_frame, text="Recommendation: Load a song", font=("Segoe UI", 9, "italic"), foreground="blue")
        self.reco_label.pack(pady=5)

        ttk.Label(self.map_frame, text="\nDifficulty Presets", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W)
        preset_frame = ttk.Frame(self.map_frame); preset_frame.pack(fill=tk.X, pady=5)
        ttk.Button(preset_frame, text="NORMAL", command=lambda: self.set_preset(4, 1.2)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(preset_frame, text="HARD", command=lambda: self.set_preset(7, 0.9)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(preset_frame, text="INSANE", command=lambda: self.set_preset(10, 0.5)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(preset_frame, text="GALAXY", command=lambda: self.set_preset(15, 0.2)).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self.density_scale = ttk.Scale(self.map_frame, from_=1, to=20, orient=tk.HORIZONTAL); self.density_scale.set(6)
        self.density_scale.pack(fill=tk.X, pady=5)
        self.speed_scale = ttk.Scale(self.map_frame, from_=2.0, to=0.05, orient=tk.HORIZONTAL); self.speed_scale.set(0.8)
        self.speed_scale.pack(fill=tk.X, pady=5)

        self.status_label = ttk.Label(self.map_frame, text="Status: Ready"); self.status_label.pack()
        self.gen_button = ttk.Button(self.map_frame, text="GENERATE VULNUS MAP", command=self.start_mapping)
        self.gen_button.pack(pady=20, fill=tk.X)

    def set_preset(self, d, s): self.density_scale.set(d); self.speed_scale.set(s)
    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.m4a")])
        if file:
            self.audio_path.set(file)
            self.song_entry.delete(0, tk.END); self.song_entry.insert(0, os.path.splitext(os.path.basename(file))[0])

    def start_batch_process(self):
        queries = [q.strip() for q in self.search_entry.get().split(",") if q.strip()]
        if not queries: return
        self.dl_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_batch_process, args=(queries,), daemon=True).start()

    def run_batch_process(self, queries):
        dl_folder = os.path.abspath("downloads")
        if not os.path.exists(dl_folder): os.makedirs(dl_folder)
        for i, q in enumerate(queries):
            self.root.after(0, lambda n=i+1, total=len(queries): self.dl_status.config(text=f"[{n}/{total}] Processing: {q}..."))
            try:
                cmd = ["yt-dlp", f"ytsearch1:{q}", "--extract-audio", "--audio-format", "mp3", "--output", os.path.join(dl_folder, f"batch_{i}_%(title)s.%(ext)s"), "--ffmpeg-location", ffmpeg_local_path]
                subprocess.run(cmd, capture_output=True, text=True)
                mp3_files = [os.path.join(dl_folder, f) for f in os.listdir(dl_folder) if f.lower().endswith(".mp3") and os.path.getmtime(os.path.join(dl_folder, f)) > time.time() - 30]
                if mp3_files:
                    latest = max(mp3_files, key=os.path.getmtime)
                    perform_mapping_logic(latest, os.path.splitext(os.path.basename(latest))[0])
            except: pass
        self.root.after(0, lambda: self.dl_button.config(state=tk.NORMAL))
        self.root.after(0, lambda: self.dl_status.config(text="Batch Finished."))

    def start_mapping(self):
        if not self.audio_path.get(): return
        self.gen_button.config(state=tk.DISABLED)
        threading.Thread(target=self.run_mapping, daemon=True).start()

    def run_mapping(self):
        try:
            perform_mapping_logic(self.audio_path.get(), self.song_entry.get(), self.density_scale.get(), self.speed_scale.get(), lambda m: self.root.after(0, lambda: self.status_label.config(text=m)))
            self.root.after(0, lambda: messagebox.showinfo("Success", "Map Pack Created!"))
        except Exception as e: self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally: self.root.after(0, lambda: self.gen_button.config(state=tk.NORMAL))

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?")
    parser.add_argument("--title")
    parser.add_argument("--density", type=float, default=6.0)
    parser.add_argument("--speed", type=float, default=0.8)
    args = parser.parse_args()
    if args.path: perform_mapping_logic(args.path, args.title or "CLI Song", args.density, args.speed)
    else:
        root = tk.Tk()
        App(root)
        root.mainloop()

if __name__ == "__main__": main()
