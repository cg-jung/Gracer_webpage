# 주은혜 교회 Lord's Grace Church website (draft)
Plain static HTML/CSS/JS — no CMS, no PHP, no database, no login — so there's little to attack. A strict Content-Security-Policy is set in every page.
- **YouTube**: set `youtubeChannelId` in `config.json`; /watch embeds the channel's uploads playlist and updates itself.
- **Gallery (albums)**: create a folder `gallery/albums/<album-id>/` and upload photos into it (optional `album.json` with `{"title": "...", "date": "YYYY-MM-DD"}` and `captions.json`). That is all — the deploy workflow rebuilds `gallery/albums.json` automatically. Each album has its own link: `gallery.html#<album-id>`. Bulk-import Flickr albums with `tools/import_flickr.py` (free Flickr API key).
- **Content**: Korean-first with English subtitles; edit the HTML pages directly.
- **Hosting**: GitHub Pages / Cloudflare Pages / Netlify (free, HTTPS, no server to hack). Enable 2FA on the host, registrar and YouTube accounts.
