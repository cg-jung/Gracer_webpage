# Showing Flickr albums on the church site (without copying photos)

**Goal:** keep the photos on Flickr (account `203228635@N02`, "lgctracy") and have the church website show or link to them, instead of storing copies in this repository.

**Short answer:** you only need a Flickr API key for Option B. Options A and C need none. The key must never be placed in the website's files. If it is, anyone can read it.

## Options

| | A. Links to Flickr | B. Auto-load albums (recommended) | C. Flickr embed code |
|---|---|---|---|
| Visitor sees | Album cards on our site; tapping opens Flickr | Album cards + photo grid on our site; photos come from Flickr's servers | Flickr's own slideshow box inside our page |
| API key | No | Yes (free), kept as a GitHub secret | No |
| Photos stored in repo | No | No (only a small list of titles and addresses) | No |
| New Flickr album appears | After you add a line | Automatically (daily, or on demand) | After you paste a new embed |
| Security | Lowest risk | Low risk (key never leaves GitHub) | Runs Flickr's JavaScript on our page — a third-party script; weakens our protections |
| Effort | 10 minutes | About 1 hour | 5 minutes per album |

## Option A: simple links (no key)
Edit `gallery/albums/<id>/album.json` or add a link card per album pointing to the Flickr album address, for example
`https://www.flickr.com/photos/203228635@N02/albums/72177720332543190`. Visitors leave our site to view photos. The safest and simplest option.

## Option B: automatic loading with an API key (recommended)
The key is used only inside a GitHub Actions job, never by visitors' browsers.

1. **Get a key:** sign in to Flickr → https://www.flickr.com/services/apps/create → "Apply for a non-commercial key". Copy the **Key** (not the Secret needed for this use).
2. **Store it safely:** GitHub repo → Settings → Secrets and variables → Actions → **New repository secret**. Name `FLICKR_KEY`, value = the key. GitHub hides secrets from the public even though the repo is public.
3. **How it works (to build):** each deploy (plus a daily schedule) runs a script that calls Flickr's API (`flickr.photosets.getList` and `flickr.photosets.getPhotos`) and writes `gallery/albums.json` with album titles, photo addresses and links back to Flickr. The page then shows those photos straight from Flickr's servers (`live.staticflickr.com`). Nothing is downloaded into the repo.
4. **Site settings change:** the Content-Security-Policy gets one extra allowed image source, `live.staticflickr.com`. No scripts from Flickr are allowed.
5. **Rules:** only public albums and photos are shown. Each photo links back to its Flickr page, which Flickr's API terms ask for. If a photo is made private or deleted on Flickr, it disappears from our site after the next daily update.

**Trade-offs:** photos load from Flickr, so if Flickr is down or the account is closed, the gallery is empty. Photos aren't in our hands as a backup either. Keep a backup of originals elsewhere.

## Option C: Flickr embed (not recommended)
Flickr's "Share → Embed" code needs a script from `embedr.flickr.com`. Allowing it means a third party can run code on our pages. Given the earlier attack, avoid this.

## Key safety rules (Option B)
- Never paste the key into any file in the repo, an issue, or a chat message.
- If the key leaks, delete it at flickr.com/services/apps and create a new one, then update the GitHub secret.
- The Flickr account itself needs two-factor authentication, because whoever controls it controls the gallery.

## Existing copied photos
The 20 photos of "17주년 부흥회" in `gallery/albums/revival-17/` are copies. After Option A or B is working, remove that folder.

## Decision needed
Choose A (links only) or B (automatic loading). The current copied album stays until then.
