#!/usr/bin/env python3
"""Rebuild gallery/albums.json from gallery/albums/<album-id>/ folders.
Each folder = one album. Optional album.json: {"title": "...", "title_en": "...", "date": "2026-03-01"}
Optional captions.json: {"photo.jpg": "caption"}. Cover = first photo (or "cover" in album.json).
A mistyped album.json or captions.json is reported and ignored, so one typo never stops the site from deploying."""
import json, pathlib
g = pathlib.Path(__file__).resolve().parent.parent / "gallery"
EXT = {".jpg", ".jpeg", ".png", ".webp"}
def load(path):
    if not path.exists(): return {}
    try: d = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e: print(f"WARNING: ignoring {path.relative_to(g)} - not valid JSON ({type(e).__name__})"); return {}
    if not isinstance(d, dict): print(f"WARNING: ignoring {path.relative_to(g)} - must be a {{...}} object"); return {}
    return d
text = lambda v, default="": v if isinstance(v, str) else default
albums = []
(g / "albums").mkdir(parents=True, exist_ok=True)   # folder may be empty (all albums can come from Flickr)
for d in sorted((g / "albums").iterdir()):
    if not d.is_dir(): continue
    meta, caps = load(d / "album.json"), load(d / "captions.json")
    files = sorted(p.name for p in d.iterdir() if p.suffix.lower() in EXT)
    if not files: continue
    cover = text(meta.get("cover"))
    albums.append({"id": d.name, "title": text(meta.get("title")) or d.name.replace("-", " "), "title_en": text(meta.get("title_en")),
                   "date": text(meta.get("date"))[:10], "cover": cover if cover in files else files[0],
                   "photos": [{"file": f, "caption": text(caps.get(f))} for f in files]})
albums.sort(key=lambda a: a["date"], reverse=True)
(g / "albums.json").write_text(json.dumps(albums, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(albums), "albums,", sum(len(a["photos"]) for a in albums), "photos")
