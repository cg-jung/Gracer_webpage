#!/usr/bin/env python3
"""Add the church's PUBLIC Flickr albums to gallery/albums.json as remote albums (photos stay on Flickr; only titles and
addresses are saved). Runs in GitHub Actions with the key in the FLICKR_KEY secret. Without a key or on any Flickr error it
skips quietly so the deploy never breaks. Run tools/make_manifest.py first."""
import datetime, json, os, pathlib, re, sys, urllib.parse, urllib.request
UID = "203228635@N02"
OUT = pathlib.Path(__file__).resolve().parent.parent / "gallery" / "albums.json"
OK_URL = re.compile(r"^https://live\.staticflickr\.com/\d+/\d+_[0-9a-f]+_[a-z]\.jpg$")   # only accept Flickr's image servers
def api(key, **p):
    p.update(api_key=key, format="json", nojsoncallback=1)
    with urllib.request.urlopen("https://api.flickr.com/services/rest/?" + urllib.parse.urlencode(p), timeout=30) as r:
        d = json.load(r)
    if d.get("stat") != "ok": raise RuntimeError(d.get("message", "Flickr error"))
    return d
def fetch(key, call=api):
    albums = []
    for s in call(key, method="flickr.photosets.getList", user_id=UID, per_page=500)["photosets"]["photoset"]:
        photos, page = [], 1
        while True:
            r = call(key, method="flickr.photosets.getPhotos", photoset_id=s["id"], user_id=UID, per_page=500, page=page, privacy_filter=1)["photoset"]
            for ph in r["photo"]:
                b = f'https://live.staticflickr.com/{ph["server"]}/{ph["id"]}_{ph["secret"]}'
                if OK_URL.match(b + "_b.jpg"):
                    photos.append({"url": b + "_b.jpg", "thumb": b + "_n.jpg", "caption": ph.get("title", ""),
                                   "link": f"https://www.flickr.com/photos/{UID}/{ph['id']}/"})
            if page >= int(r["pages"]): break
            page += 1
        if not photos: continue
        d = datetime.datetime.fromtimestamp(int(s["date_create"]), datetime.timezone.utc).strftime("%Y-%m-%d")
        albums.append({"id": "flickr-" + s["id"], "title": s["title"]["_content"], "title_en": "", "date": d, "remote": True,
                       "cover": photos[0]["thumb"], "link": f"https://www.flickr.com/photos/{UID}/albums/{s['id']}", "photos": photos})
    return albums
def main():
    key = os.environ.get("FLICKR_KEY", "").strip()
    if not key: print("FLICKR_KEY not set - skipping Flickr albums"); return
    try: remote = fetch(key)
    except Exception as e: print("Flickr unavailable - skipping:", type(e).__name__); return   # never print the key/URL
    local = [a for a in json.loads(OUT.read_text()) if not a.get("remote")] if OUT.exists() else []
    allx = sorted(local + remote, key=lambda a: a["date"], reverse=True)
    OUT.write_text(json.dumps(allx, ensure_ascii=False, indent=1)); print(len(remote), "Flickr albums added")
if __name__ == "__main__": main()
