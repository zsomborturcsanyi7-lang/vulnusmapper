import os
import json
import subprocess
import glob

def process_all():
    # Path to the songs folder
    songs_dir = os.path.join("spotifydownload-master", "Popular songs")
    
    # Find the latest JSON file
    json_files = glob.glob(os.path.join(songs_dir, "*.json"))
    if not json_files:
        print("No JSON files found in " + songs_dir)
        return
    
    latest_json = max(json_files, key=os.path.getmtime)
    print(f"Using latest JSON: {latest_json}")
    
    with open(latest_json, "r", encoding="utf-8") as f:
        tracks = json.load(f)
    
    # Map of sanitized filename to track info
    # (Note: we need to match what we downloaded)
    def sanitize(s):
        for c in '/\:*?"<>|':
            s = s.replace(c, "_")
        return s

    # Get all .m4a files
    m4a_files = glob.glob(os.path.join(songs_dir, "*.m4a"))
    
    for m4a_path in m4a_files:
        filename = os.path.basename(m4a_path)
        # Try to find track info from filename
        # Filename is "Artist - Title.m4a"
        name_no_ext = os.path.splitext(filename)[0]
        
        # We'll just use the filename parts for artist/title
        parts = name_no_ext.split(" - ", 1)
        if len(parts) == 2:
            artist, title = parts
        else:
            artist, title = "Unknown", name_no_ext
            
        print(f"Processing: {artist} - {title}")
        
        # Call Vulnus_auto_mapper.py CLI with optimized settings
        cmd = [
            "python", "Vulnus_auto_mapper.py",
            m4a_path,
            "--title", title,
            "--artist", artist,
            "--density", "8",  # Increased default density for batch
            "--speed", "0.7"   # Faster default speed
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    process_all()
