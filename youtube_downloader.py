import os
import sys
import threading
import subprocess
import re
import tkinter as tk
import shutil
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO

# --- DEPENDENCY KEZELŐ ---
def ensure_everything():
    try:
        import yt_dlp
        return True
    except ImportError:
        pip_exists = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                     capture_output=True, shell=True).returncode == 0
        if not pip_exists:
            ps_cmd = (r"Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '$env:TEMP\get-pip.py'; "
                      r"& python '$env:TEMP\get-pip.py' --user; Remove-Item '$env:TEMP\get-pip.py'")
            try: subprocess.check_call(["powershell", "-Command", ps_cmd], shell=True)
            except: return False
        try: subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"], shell=True)
        except: return False
    return True

ensure_everything()

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    internal = resource_path("ffmpeg.exe")
    if os.path.exists(internal): return internal
    path_ffmpeg = shutil.which("ffmpeg")
    return path_ffmpeg if path_ffmpeg else "ffmpeg"

FFMPEG_EXE = get_ffmpeg_path()

class NeonWaveDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("NEON WAVE V4 - FINAL PRO")
        self.root.geometry("500x750")
        self.root.configure(bg="#05050a")
        
        self.accent_cyan = "#00f2ff"
        self.accent_pink = "#ff007a"
        self.bg_dark = "#05050a"

        self.current_url = None
        self.available_formats = {
            "mp4": ["1080p", "720p", "480p", "360p"],
            "mp3": ["320kbps", "256kbps", "192kbps", "128kbps"]
        }

        self.main_canvas = tk.Canvas(self.root, bg=self.bg_dark, highlightthickness=0)
        self.main_canvas.pack(fill=tk.BOTH, expand=True)

        self.screen_container = tk.Frame(self.main_canvas, bg=self.bg_dark)
        self.screen_container.place(relx=0.5, rely=0.5, anchor="center", width=500, height=750)

        self.setup_styles()
        self.show_search_screen()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("TCombobox", fieldbackground="#111", background=self.accent_cyan, foreground="white")
        self.style.map("TCombobox", fieldbackground=[('readonly', '#111')], foreground=[('readonly', 'white')])
        self.style.configure("Neon.Horizontal.TProgressbar", troughcolor="#1a1a2e", background=self.accent_pink)

    def clear_screen(self):
        for widget in self.screen_container.winfo_children():
            widget.destroy()

    def show_search_screen(self):
        self.clear_screen()
        tk.Label(self.screen_container, text="NEON WAVE", font=("Orbitron", 36, "bold"), bg=self.bg_dark, fg=self.accent_cyan).pack(pady=(100, 5))
        tk.Label(self.screen_container, text="V4 PRO DOWNLOADER", font=("Consolas", 10), bg=self.bg_dark, fg=self.accent_pink).pack()
        
        self.url_var = tk.StringVar()
        entry_frame = tk.Frame(self.screen_container, bg=self.accent_cyan, padx=1, pady=1)
        entry_frame.pack(pady=40)
        self.url_entry = tk.Entry(entry_frame, textvariable=self.url_var, font=("Consolas", 14), bg="#0a0a0f", fg="#fff", insertbackground=self.accent_cyan, relief="flat", width=30)
        self.url_entry.pack(ipady=12, padx=1, pady=1)
        
        self.search_btn = tk.Button(self.screen_container, text="ANALYZE LINK", command=self.initiate_search, bg=self.bg_dark, fg=self.accent_cyan, font=("Consolas", 12, "bold"), relief="flat", highlightthickness=2, highlightbackground=self.accent_cyan, padx=40, pady=12, cursor="hand2")
        self.search_btn.pack()

    def initiate_search(self):
        query = self.url_var.get().strip()
        if not query: return
        self.search_btn.config(state=tk.DISABLED, text="SEARCHING...")

        def task():
            try:
                cmd = [sys.executable, "-m", "yt_dlp", "--print", "title", "--print", "thumbnail", "--print", "id", "-F", "--no-warnings"]
                cmd.append(f"ytsearch1:{query}" if not query.startswith("http") else query)
                
                res = subprocess.run(cmd, text=True, capture_output=True, encoding='utf-8', errors='replace', shell=True)
                lines = [l.strip() for l in res.stdout.split('\n') if l.strip()]
                if not lines: raise Exception("No results.")

                title = lines[0]
                thumb = next((l for l in lines if l.startswith("http")), None)
                vid_id = next((l for l in lines if len(l) == 11), None)
                v_url = f"https://www.youtube.com/watch?v={vid_id}" if vid_id else query
                
                # Dinamikus formátum kinyerés
                heights = sorted(list(set(re.findall(r'(\d{3,4})p', res.stdout))), key=lambda x: int(x), reverse=True)
                if heights: self.available_formats["mp4"] = [h+"p" for h in heights]

                self.root.after(0, lambda: self.show_download_screen(title, thumb, v_url))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Hiba", str(e)))
                self.root.after(0, lambda: self.search_btn.config(state=tk.NORMAL, text="ANALYZE LINK"))

        threading.Thread(target=task, daemon=True).start()

    def show_download_screen(self, title, thumb_url, video_url):
        self.clear_screen()
        self.current_url = video_url
        
        tk.Label(self.screen_container, text="CONFIGURE DOWNLOAD", font=("Orbitron", 16, "bold"), bg=self.bg_dark, fg=self.accent_pink).pack(pady=20)

        self.thumb_label = tk.Label(self.screen_container, bg="#000")
        self.thumb_label.pack()
        if thumb_url: self.update_thumbnail(thumb_url)
        
        tk.Label(self.screen_container, text=title[:60], font=("Consolas", 10, "bold"), bg=self.bg_dark, fg=self.accent_cyan, wraplength=400).pack(pady=10)

        # Mód és Minőség választó
        self.mode_var = tk.StringVar(value="mp4")
        self.qual_var = tk.StringVar()
        
        opt_frame = tk.Frame(self.screen_container, bg=self.bg_dark)
        opt_frame.pack(pady=10)
        
        tk.Radiobutton(opt_frame, text="VIDEO (MP4)", variable=self.mode_var, value="mp4", command=self.update_qual_list, bg=self.bg_dark, fg="white", selectcolor="#111").grid(row=0, column=0, padx=10)
        tk.Radiobutton(opt_frame, text="AUDIO (MP3)", variable=self.mode_var, value="mp3", command=self.update_qual_list, bg=self.bg_dark, fg="white", selectcolor="#111").grid(row=0, column=1, padx=10)

        self.qual_combo = ttk.Combobox(self.screen_container, textvariable=self.qual_var, state="readonly", width=25)
        self.qual_combo.pack(pady=5)
        self.update_qual_list()

        self.progress = ttk.Progressbar(self.screen_container, length=380, style="Neon.Horizontal.TProgressbar")
        self.progress.pack(pady=20)

        self.dl_btn = tk.Button(self.screen_container, text="START DOWNLOAD", command=self.start_download, bg=self.accent_cyan, fg="#000", font=("Consolas", 12, "bold"), relief="flat", padx=50, pady=12)
        self.dl_btn.pack()

    def update_qual_list(self):
        m = self.mode_var.get()
        self.qual_combo['values'] = self.available_formats[m]
        self.qual_combo.current(0)

    def start_download(self):
        folder = filedialog.askdirectory()
        if not folder: return
        
        quality = self.qual_var.get()
        mode = self.mode_var.get()
        self.dl_btn.config(state=tk.DISABLED, text="DOWNLOADING...")

        def task():
            try:
                cmd = [sys.executable, "-m", "yt_dlp", "--newline", "--progress", "--ffmpeg-location", FFMPEG_EXE]
                
                if mode == "mp3":
                    br = quality.replace("kbps", "")
                    cmd.extend(["-x", "--audio-format", "mp3", "--audio-quality", br])
                else:
                    h = quality.replace("p", "")
                    cmd.extend(["-f", f"bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h}][ext=mp4]/best", "--merge-output-format", "mp4"])

                out_path = os.path.join(folder, "%(title)s.%(ext)s")
                cmd.extend(["--output", out_path, self.current_url])
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', shell=True)
                
                for line in process.stdout:
                    if '%' in line:
                        match = re.search(r'(\d+\.\d+)%', line)
                        if match: 
                            val = float(match.group(1))
                            self.root.after(0, lambda v=val: self.progress.configure(value=v))
                
                process.wait()
                
                if process.returncode == 0:
                    # Siker képernyő és útvonal megjelenítése
                    self.root.after(0, lambda: self.show_success_screen(folder))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Hiba", "Download failed."))
                    self.root.after(0, lambda: self.dl_btn.config(state=tk.NORMAL, text="START DOWNLOAD"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Hiba", str(e)))

        threading.Thread(target=task, daemon=True).start()

    def show_success_screen(self, path):
        messagebox.showinfo("SUCCESS", f"Download complete!\n\nSaved to:\n{path}")
        self.show_search_screen()

    def update_thumbnail(self, url):
        try:
            res = requests.get(url, timeout=5)
            img = Image.open(BytesIO(res.content)).resize((320, 180), Image.Resampling.LANCZOS)
            self.tk_thumb = ImageTk.PhotoImage(img)
            self.thumb_label.config(image=self.tk_thumb)
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = NeonWaveDownloader(root)
    root.mainloop()