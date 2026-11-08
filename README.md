# 주은혜 교회 Lord's Grace Church website (draft)
Plain static HTML/CSS/JS — no CMS, no server code, no database, no login. A strict Content-Security-Policy is set in every page.
- **YouTube**: set `youtubeChannelId` in `config.json`; /watch embeds the channel's uploads playlist and updates itself.
- **Gallery**: put photos in `gallery/photos/` (bulk-import from Flickr with `tools/import_flickr.py`, needs a free Flickr API key), run `python3 tools/make_manifest.py`, commit.
- **Content**: Korean-first with English subtitles; edit the HTML pages directly.
- **Hosting**: GitHub Pages / Cloudflare Pages / Netlify (free, HTTPS, no server to maintain). Enable 2FA on the host, registrar and YouTube accounts.
