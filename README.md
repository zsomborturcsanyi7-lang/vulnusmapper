# VulnusMapper — Ritmusjáték Map Automata Generátor

**Spotify/YouTube zene letöltő + librosa beat detektáló, amely automatikusan generál ritmusjáték pályákat (map-eket) a zenék ütemei alapján.**

## 🎵 Leírás

A VulnusMapper egy teljes körű pipeline, amely:

1. **Zenék letöltése** — Spotify playlist vagy YouTube link alapján (yt-dlp)
2. **Beat detektálás** — librosa-val BPM, ütemek, és hangkarakterisztika elemzés
3. **Map generálás** — Ritmusjáték pálya automatikus előállítása az ütemekből
4. **Motívum felismerés** — Ismétlődő zenei minták detektálása és változatos map elemek

Támogatott formátumok: MP3, WAV, FLAC, OGG, M4A

### NeonWave V4

A projekt része a **NeonWave V4** — egy PyInstaller-rel buildelt standalone exe változat, amely tartalmazza a YouTube letöltőt és a mapper funkciókat.

## 📁 Fájlszerkezet

```
VulnusMapper/
├── Vulnus_auto_mapper.py        # Fő mapper script (442 sor)
├── process_all.py               # Batch feldolgozó — minden letöltött zenére
├── youtube_downloader.py        # YouTube letöltő (Spotify/YT támogatás)
├── youtube_downloader.exe       # Lefordított YouTube letöltő
├── youtube_downloader.spec      # PyInstaller spec fájl
├── NeonWaveDownloader.spec      # NeonWave build spec
├── YouTubeDownloader.spec       # YouTube letöltő spec
├── NeonWave_V4.spec             # NeonWave V4 build spec
├── profilkepyoutubenak.ico      # Alkalmazás ikon
├── downloads/                   # Letöltött zenék
│   ├── batch_0_*.mp3
│   ├── batch_1_*.mp3
│   ├── batch_2_*.mp3
│   └── batch_3_*.mp3
├── build/
│   └── NeonWave_V4/             # PyInstaller build fájlok
├── dist/
│   └── youtube_downloader.exe   # Distributable exe
├── mapper_errors.log            # Mapper hiba log
├── youtube_downloader.log       # Letöltő log
└── README.md
```

## 🚀 Használat

### Zenék letöltése

```bash
# YouTube letöltő indítása
python youtube_downloader.py

# Vagy a lefordított exe
youtube_downloader.exe
```

### Map generálás egy zenéhez

```bash
python Vulnus_auto_mapper.py
```

A szkript:
1. Bekéri a zene fájl elérési útját
2. Elemzi a BPM-et és ütemeket
3. Detektálja a zenei motívumokat
4. Generálja a map fájlt

### Batch feldolgozás

```bash
# Az összes letöltött zenéhez map generálása
python process_all.py
```

### Függőségek automatikus telepítése

A `Vulnus_auto_mapper.py` induláskor automatikusan ellenőrzi és telepíti a hiányzó csomagokat.

## 📦 Függőségek

```bash
pip install librosa numpy yt-dlp
```

- **Python 3.8+**
- **librosa** — zenei elemzés, beat detektálás
- **numpy** — numerikus számítások
- **yt-dlp** — YouTube/Spotify letöltés
- **PyInstaller** (opcionális) — exe build-eléshez

## 🎮 Kimenet formátum

A generált map fájl a következőket tartalmazza:
- **BPM** — tempó információ
- **Ütem pozíciók** — időbélyegek ezredmásodpercben
- **Nehézségi szint** — automatikusan meghatározva
- **Motívum váltások** — változatos map elemek a zenei ismétlődéseknél
- **Hangeffekt jelek** — speciális elemek triggerelése

## ⚠️ Jogi megjegyzés

Ez az eszköz kizárólag **személyes használatra** készült. A szerzői joggal védett zenék letöltése és felhasználása a helyi jogszabályok szerint szabályozott. Csak olyan tartalmat tölts le, amelyhez rendelkezel a megfelelő jogosultsággal.
