# VulnusMapper — Ritmusjáték pálya automatikus generálás Spotify/YouTube zenéből

**Status:** ⚠️ Prototype — beat detection működik, map generálás tesztelve

Spotify/YouTube zene letöltő + librosa beat detector, ami automatikusan generál ritmusjáték pályákat a beat minták alapján.

## ⚠️ THIS PROJECT IS UNFINISHED — FEEL FREE TO CONTINUE IT ⚠️

**Ez a projekt NINCS KÉSZEN. Bárki folytathatja, aki akarja!**
Ezt a projektet Zsombi & Hermes Agent (Nous Research) közösen fejlesztette, de egyik projekt sincs 100%-osan befejezve.

---

## Pipeline
1. **Zene letöltés** — Spotify lejátszási listákból vagy YouTube linkekből (yt-dlp)
2. **Beat detection** — BPM, beat-ek, audio jellemzők analízise librosa-val
3. **Map generálás** — Automatikus ritmusjáték pálya generálás a detektált beat-ekből
4. **Motívum felismerés** — Ismétlődő zenei minták detektálása és változatos map elemek

## Fájlok
| Fájl | Leírás |
|------|--------|
| `Vulnus_auto_mapper.py` | Fő mapper szkript (442 sor) |
| `process_all.py` | Batch feldolgozó |
| `youtube_downloader.py` | YouTube letöltő |
| `vulnus_ai_bot.py` | AI bot |
| `check_env.py` | Környezet ellenőrző |

## Fejlesztő
Zsombi & Hermes Agent (Nous Research)
