# vulnusmapper

Librosa alapú automatikus ritmusjáték térkép és ütemdetektáló script Vulnus map fájlokhoz.

## 📌 A projekt célja
Automatizált eszköz audiofájlok (pl. MP3, WAV) elemzésére és a detektált ütemekből a Vulnus ritmusjáték számára kompatibilis térképfájlok (map.json) előállítására.

## ⚙️ Technológiai stakk & Működés
- **Nyelv**: Python 3.10+
- **Audio feldolgozás**: `librosa`, `numpy`
- **Fájlformátum**: JSON kimenet Vulnus specifikáció szerint

## 🚀 Telepítés és Használat

### Előfeltételek
- Python 3.10+
- FFmpeg (opcionális, de ajánlott audio konverzióhoz)

### Lépések
```bash
git clone https://github.com/zsomborturcsanyi7-lang/vulnusmapper.git
cd vulnusmapper

# Virtuális környezet létrehozása és függőségek
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Térkép generálása audio fájlból
python mapper.py --input zene.mp3 --output map.json
```

## 📊 Status
⚠️ **Működő kísérleti eszköz**.
