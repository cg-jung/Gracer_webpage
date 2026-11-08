#!/usr/bin/env python3
"""Download the church's Flickr photos into gallery/photos (run on your own computer, not the web server).
Usage: python3 tools/import_flickr.py <flickr_user_id e.g. 203228635@N02>
Needs a free Flickr API key in env FLICKR_KEY. Then run tools/make_manifest.py and commit."""
import json, os, sys, urllib.parse, urllib.request, pathlib
key, uid = os.environ["FLICKR_KEY"], sys.argv[1]
out = pathlib.Path(__file__).resolve().parent.parent / "gallery" / "photos"; out.mkdir(exist_ok=True)
def api(**p):
    p.update(api_key=key, format="json", nojsoncallback=1)
    return json.load(urllib.request.urlopen("https://api.flickr.com/services/rest/?" + urllib.parse.urlencode(p)))
page = 1
while True:
    r = api(method="flickr.people.getPublicPhotos", user_id=uid, per_page=100, page=page, extras="url_l,url_o")["photos"]
    for ph in r["photo"]:
        url = ph.get("url_l") or ph.get("url_o")
        if url: urllib.request.urlretrieve(url, out / f'{ph["id"]}.jpg')
    if page >= r["pages"]: break
    page += 1
