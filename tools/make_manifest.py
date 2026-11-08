#!/usr/bin/env python3
"""Rebuild gallery/photos.json from images in gallery/photos (filename -> caption)."""
import json, pathlib
d = pathlib.Path(__file__).resolve().parent.parent / "gallery"
files = sorted(p.name for p in (d / "photos").iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
(d / "photos.json").write_text(json.dumps([{"file": f, "caption": pathlib.Path(f).stem.replace("_", " ")} for f in files], indent=2))
print(len(files), "photos")
