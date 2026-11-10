#!/usr/bin/env python3
"""Write sermons.json (video ids + titles only) for the Sermons page. Never leaves the site without a list.
Order of sources: 1) YouTube Data API if the YOUTUBE_KEY secret exists (most reliable), 2) YouTube's public channel feed
(3 tries), 3) the list already published on the live site, 4) data/sermons_fallback.json in this repo.
Logs only status codes - never addresses that contain a key."""
import json, os, pathlib, re, sys, time, urllib.error, urllib.request
import xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
def clean(items, limit=6):
    out = []
    for v in items if isinstance(items, list) else []:
        if isinstance(v, dict) and ID.match(str(v.get("id", ""))):
            out.append({"id": v["id"], "title": str(v.get("title", "")).strip()[:200], "date": str(v.get("date", ""))[:10]})
    return sorted(out, key=lambda v: v["date"], reverse=True)[:limit]
def parse_feed(data, limit=6):
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data or len(data) > 2_000_000: raise ValueError("unexpected feed content")
    return clean([{"id": (e.findtext("yt:videoId", "", NS) or "").strip(), "title": e.findtext("a:title", "", NS) or "",
                   "date": (e.findtext("a:published", "", NS) or "")[:10]} for e in ET.fromstring(data).findall("a:entry", NS)], limit)
def parse_api(data, limit=6):
    d = json.loads(data)
    return clean([{"id": ((i.get("snippet") or {}).get("resourceId") or {}).get("videoId", ""), "title": (i.get("snippet") or {}).get("title", ""),
                   "date": ((i.get("snippet") or {}).get("publishedAt") or "")[:10]} for i in d.get("items", [])], limit)
def fetch(url, tries=3):
    last = "no attempt"
    for n in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "church-site-build"}), timeout=30) as r: return r.read(2_100_000)
        except urllib.error.HTTPError as e: last = f"HTTP {e.code}"
        except Exception as e: last = type(e).__name__
        if n < tries - 1: time.sleep(2 + 3 * n)
    raise RuntimeError(last)
def main():
    cid = json.loads((ROOT / "config.json").read_text())["youtubeChannelId"]
    assert re.match(r"^UC[A-Za-z0-9_-]{22}$", cid)
    vids, source = [], ""
    key = os.environ.get("YOUTUBE_KEY", "").strip()
    if key:
        try: vids = parse_api(fetch("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=10&playlistId=UU" + cid[2:] + "&key=" + key), 6); source = "YouTube API"
        except Exception as e: print("YouTube API failed:", e)
    if not vids:
        try: vids = parse_feed(fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid)); source = "YouTube channel feed"
        except Exception as e: print("YouTube feed failed:", e)
    if not vids:
        try:
            dom = (ROOT / "CNAME").read_text().strip(); vids = clean(json.loads(fetch(f"https://{dom}/sermons.json", 2))); source = "list already published on the live site (kept)"
        except Exception as e: print("live-site copy failed:", e)
    if not vids:
        try: vids = clean(json.loads((ROOT / "data" / "sermons_fallback.json").read_text())); source = "repo fallback list"
        except Exception as e: print("repo fallback failed:", type(e).__name__)
    if vids: (ROOT / "sermons.json").write_text(json.dumps(vids, ensure_ascii=False, indent=1)); print(f"{len(vids)} videos saved from: {source}; newest: {vids[0]['date']} {vids[0]['title'][:40]}")
    else: print("no sermon list available - the page will show the channel player")
if __name__ == "__main__": main()
