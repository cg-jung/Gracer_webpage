# Publish steps (≈15 min)
1. github.com → New repository → name `gracer-site` → Public → Create (empty, no README).
2. Upload the contents of this folder (drag & drop on the repo page, or `git push`). The `.github` folder must be included.
3. Repo → Settings → Pages → Source: **GitHub Actions**. Push to `main` deploys; wait for the green check in the Actions tab.
4. Test at https://<username>.github.io/gracer-site/ . (Links are relative, so it works there too.)
5. Settings → Pages → Custom domain: `gracer.org` → Save. Tick **Enforce HTTPS** when available.
6. At the domain registrar's DNS: delete old A/AAAA/CNAME records to the old host; add A records 185.199.108.153, .109.153, .110.153, .111.153 and CNAME `www` → `<username>.github.io`.
7. Turn on 2FA for GitHub and the registrar.
