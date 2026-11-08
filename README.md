# 주은혜 교회 Lord's Grace Church website (draft)
Plain static HTML/CSS/JS — no CMS, no PHP, no database, no login — so there's little to attack. A strict Content-Security-Policy is set in every page.
- **YouTube**: set `youtubeChannelId` in `config.json`; /watch embeds the channel's uploads playlist and updates itself.
- **Gallery (albums)**: one folder per album in `gallery/albums/<album-id>/` (photos + optional `album.json` title/date, `captions.json`). Run `python3 tools/make_manifest.py`, then `python3 tools/verify_site.py`, commit. Each album has its own link: `gallery.html#<album-id>`. Bulk-import Flickr albums with `tools/import_flickr.py` (needs a free Flickr API key).
- **Content**: Korean-first with English subtitles; edit the HTML pages directly.
- **Hosting**: GitHub Pages / Cloudflare Pages / Netlify (free, HTTPS, no server to hack). Enable 2FA on the host, registrar and YouTube accounts.
