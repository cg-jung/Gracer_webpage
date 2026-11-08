#!/usr/bin/env python3
"""Import Flickr albums (sets) into gallery/albums/<album-id>/ — one folder per Flickr album.
Run on your own computer. Needs a free Flickr API key:  FLICKR_KEY=xxxx python3 tools/import_flickr.py 203228635@N02
Then: python3 tools/make_manifest.py && python3 tools/verify_site.py, commit and push."""
import json, os, pathlib, re, sys, urllib.parse, urllib.request
key, uid = os.environ["FLICKR_KEY"], sys.argv[1]
base = pathlib.Path(__file__).resolve().parent.parent / "gallery" / "albums"
def api(**p):
    p.update(api_key=key, format="json", nojsoncallback=1)
    return json.load(urllib.request.urlopen("https://api.flickr.com/services/rest/?" + urllib.parse.urlencode(p)))
for s in api(method="flickr.photosets.getList", user_id=uid, per_page=500)["photosets"]["photoset"]:
    title = s["title"]["_content"]; d = base / ("flickr-" + s["id"]); d.mkdir(parents=True, exist_ok=True)
    created = __import__("datetime").datetime.utcfromtimestamp(int(s["date_create"])).strftime("%Y-%m-%d")
    (d / "album.json").write_text(json.dumps({"title": title, "date": created}, ensure_ascii=False, indent=1))
    caps, page = {}, 1
    while True:
        r = api(method="flickr.photosets.getPhotos", photoset_id=s["id"], user_id=uid, per_page=100, page=page, extras="url_l,url_o")["photoset"]
        for ph in r["photo"]:
            url = ph.get("url_l") or ph.get("url_o")
            if url: urllib.request.urlretrieve(url, d / f'{ph["id"]}.jpg'); caps[f'{ph["id"]}.jpg'] = ph["title"]
        if page >= int(r["pages"]): break
        page += 1
    (d / "captions.json").write_text(json.dumps(caps, ensure_ascii=False, indent=1)); print(title, len(caps))
