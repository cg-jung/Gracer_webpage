#!/usr/bin/env python3
"""Rebuild gallery/albums.json from gallery/albums/<album-id>/ folders.
Each folder = one album. Optional album.json: {"title": "...", "title_en": "...", "date": "2026-03-01"}
Optional captions.json: {"photo.jpg": "caption"}. Cover = first photo (or "cover" in album.json)."""
import json, pathlib
g = pathlib.Path(__file__).resolve().parent.parent / "gallery"
EXT = {".jpg", ".jpeg", ".png", ".webp"}
albums = []
(g / "albums").mkdir(parents=True, exist_ok=True)   # folder may be empty (all albums can come from Flickr)
for d in sorted((g / "albums").iterdir()):
    if not d.is_dir(): continue
    meta = json.loads((d / "album.json").read_text()) if (d / "album.json").exists() else {}
    caps = json.loads((d / "captions.json").read_text()) if (d / "captions.json").exists() else {}
    files = sorted(p.name for p in d.iterdir() if p.suffix.lower() in EXT)
    if not files: continue
    albums.append({"id": d.name, "title": meta.get("title", d.name.replace("-", " ")), "title_en": meta.get("title_en", ""),
                   "date": meta.get("date", ""), "cover": meta.get("cover", files[0]),
                   "photos": [{"file": f, "caption": caps.get(f, "")} for f in files]})
albums.sort(key=lambda a: a["date"], reverse=True)
(g / "albums.json").write_text(json.dumps(albums, ensure_ascii=False, indent=1))
print(len(albums), "albums,", sum(len(a["photos"]) for a in albums), "photos")
