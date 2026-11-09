#!/usr/bin/env python3
"""Save the church channel's newest videos to sermons.json (titles + video ids only) for the Sermons page.
Uses YouTube's public channel feed - no API key. On any problem it does nothing, so the deploy never breaks
and the page falls back to the channel playlist player."""
import json, pathlib, re, sys, urllib.request
import xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
def parse(data, limit=6):
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data or len(data) > 2_000_000: raise ValueError("unexpected feed content")
    out = []
    for e in ET.fromstring(data).findall("a:entry", NS):
        vid = (e.findtext("yt:videoId", "", NS) or "").strip()
        if not ID.match(vid): continue
        out.append({"id": vid, "title": (e.findtext("a:title", "", NS) or "").strip()[:200],
                    "date": (e.findtext("a:published", "", NS) or "")[:10]})
    return sorted(out, key=lambda v: v["date"], reverse=True)[:limit]
def main():
    try:
        cid = json.loads((ROOT / "config.json").read_text())["youtubeChannelId"]
        if not re.match(r"^UC[A-Za-z0-9_-]{22}$", cid): raise ValueError("bad channel id")
        req = urllib.request.Request(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}", headers={"User-Agent": "church-site-build"})
        with urllib.request.urlopen(req, timeout=30) as r: vids = parse(r.read(2_100_000))
    except Exception as e:
        print("YouTube feed unavailable - skipping:", type(e).__name__); return
    if vids: (ROOT / "sermons.json").write_text(json.dumps(vids, ensure_ascii=False, indent=1)); print(len(vids), "videos saved")
    else: print("YouTube feed had no videos - skipping")
if __name__ == "__main__": main()
