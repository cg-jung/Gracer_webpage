# How the gallery shows Flickr albums

The church's photos stay on Flickr (account `203228635@N02`). The website shows them without storing copies in this repository.

## How it works
- Every deploy, and a schedule that runs several times a day, calls Flickr's API (`flickr.photosets.getList`, `flickr.photosets.getPhotos`) from GitHub Actions and writes `gallery/albums.json` with album titles, photo addresses and links back to Flickr. See `tools/fetch_flickr.py`.
- Pages load the photos straight from Flickr's image servers (`live.staticflickr.com`). The Content-Security-Policy allows images from that host only; no Flickr scripts are allowed.
- Only **public** albums and photos are shown. Make a photo private on Flickr and it disappears from the site at the next update.
- If Flickr cannot be reached, the build keeps the albums already published on the live site, so the gallery is never emptied by an outage.

## The API key
- The key is stored as the GitHub Actions secret `FLICKR_KEY` (Settings → Secrets and variables → Actions). It is used only inside the build and never reaches visitors' browsers.
- Never put the key in a file, an issue or a chat message. If it leaks, delete it at flickr.com/services/apps, create a new one and update the secret.
- The Flickr account should use two-factor authentication: whoever controls it controls the gallery.

## Adding photos
Upload to a Flickr album and set the photos to Public. The album appears on the site within a few hours, or at once via Actions → Verify and deploy → Run workflow.

## Local albums (optional)
A folder `gallery/albums/<album-id>/` with photos (and an optional `album.json`) is also shown as an album. None exist at present.

## Trade-offs
Photos are served by Flickr, so they are not backed up here. Keep the originals somewhere safe.
