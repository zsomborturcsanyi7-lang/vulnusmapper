import subprocess
import sys
import os
import shutil

def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_dependencies():
    print("--- VulnusMapper Environment Check ---")
    
    # 1. Python packages
    packages = ["librosa", "numpy", "yt-dlp"]
    for pkg in packages:
        try:
            # Check if package can be imported
            __import__(pkg.replace("-", "_"))
            print(f"[OK] {pkg} is installed.")
        except ImportError:
            print(f"[MISSING] {pkg} is not installed. Attempting installation...")
            try:
                install_package(pkg)
                print(f"[OK] {pkg} installed successfully.")
            except Exception as e:
                print(f"[ERROR] Failed to install {pkg}: {e}")

    # 2. FFmpeg check
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_local_path = os.path.join(script_dir, "spotifydownload-master")
    ffmpeg_exe = os.path.join(ffmpeg_local_path, "ffmpeg.exe")
    
    if os.path.exists(ffmpeg_exe):
        print(f"[OK] ffmpeg.exe found at {ffmpeg_exe}")
    else:
        print(f"[WARNING] ffmpeg.exe not found in {ffmpeg_local_path}")
        if shutil.which("ffmpeg"):
            print("[OK] ffmpeg found in system PATH.")
        else:
            print("[ERROR] FFmpeg is missing! yt-dlp and audio analysis will fail.")

    # 3. Directory check
    downloads_dir = os.path.join(script_dir, "downloads")
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        print(f"[INFO] Created {downloads_dir} directory.")
    else:
        print(f"[OK] Downloads directory exists.")
    
    print("---------------------------------------")

if __name__ == "__main__":
    check_dependencies()
    print("\nCheck complete. You can now run Vulnus_auto_mapper.py")
