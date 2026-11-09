# Website helper guide — 주은혜 교회 Lord's Grace Church

(한국어 안내서: [HELPER_GUIDE_KO.md](HELPER_GUIDE_KO.md))

For church members who help keep the website up to date. You can do everything below from a **phone browser** (turn on "Desktop site" if a button is missing) or a computer. No special software is needed.

## 0. How the site works (30 seconds)
- The site is a set of plain files on GitHub (`github.com/cg-jung/Gracer_webpage`). There is **no WordPress, no PHP and no login on the site itself**, so there is very little to hack.
- **Photos** come from the church's Flickr account automatically. **Sermons** come from the church's YouTube channel automatically.
- When a file is saved (called a *commit*), GitHub rebuilds and publishes the site in about **1–2 minutes**.

## 1. Before you start (once)
1. Make a free GitHub account at github.com. **Turn on two-factor authentication**: Settings → Password and authentication.
2. Send your GitHub username to the site admin. They will invite you (Settings → Collaborators → *Write* role). Accept the email invitation.
3. Never share your password, and never paste passwords or private information into any file.

## 2. Change text on a page
1. Open the repository, tap the file for the page (table below), then tap the **pencil icon (Edit)**.
2. Find the words you want to change and edit **only the text**. Do not delete or change anything inside `< >` (these are page codes).
3. Tap **Commit changes…** → write a short note (for example "Update Saturday prayer time") → **Commit changes** (stay on `main`).
4. Wait 1–2 minutes, then open the page in a private tab and check it.

| What you want to change | File |
|---|---|
| Welcome message, front page | `index.html` |
| Service times | `worship.html` |
| Leadership team, church history | `about.html` |
| Mission, vision, beliefs | `mission.html` |
| CRC page (Q&A, identity statement) | `crc.html` |
| Classes, small groups, Korean school | `education.html` |
| Address, phone, map | `visit.html` (the address and phone also appear in the footer of **every** page — ask the admin for a search-and-replace) |

## 3. Add photos (albums)
1. Upload the photos to the church's **Flickr** account into an album. Ask the admin who owns the Flickr account.
2. Make sure the album's **photos are set to Public**. Only public photos appear on the website.
3. The site checks Flickr **every day**, so the new album appears within a day. To show it right away: GitHub → **Actions** tab → **Verify and deploy** → **Run workflow** → **Run workflow**.
4. Before making photos public, check you have permission, especially for children. To hide an album, set its photos back to private; it disappears at the next update.

## 4. Sermons
Upload the video to the church YouTube channel. The Sermons page and the home page show the newest videos automatically (it may take some hours).

## 5. Did my change work? / Something looks wrong
- GitHub → **Actions** tab. The top entry should have a **green check**.
  - **Red ✗:** the site **stays as it was** and nothing is broken for visitors. Do not keep retrying. Tell the admin which file you changed.
- **To undo a change:** open the file → **History** → tap your change → **Revert** (or ask the admin).
- If the page still shows old content: open it in a **private/incognito tab**. If that works, your normal browser has an old saved copy: refresh with Ctrl+Shift+R (computer) or clear the site's data (phone: browser Settings → Privacy → Clear browsing data).

## 6. Safety rules
- Only edit the files in the table above. **Do not** touch `.github`, `tools`, `CNAME` or `*.js` files.
- Only text and image files are allowed. The site has an automatic safety check that **blocks** anything else (PHP, hidden files, scripts). If a change is blocked, that is the check working as intended.
- Do not copy code from the internet into the pages.
- Keep the helper list short and remove people who no longer help (Settings → Collaborators).
- Report anything strange, such as unexpected files or changes you did not make, to the admin right away.
