#!/usr/bin/env python3
"""Fail if the site contains anything other than plain static files.
Blocks PHP/server scripts, hidden files, unknown file types, fake images, and risky code patterns."""
import pathlib, re, sys
root = pathlib.Path(__file__).resolve().parent.parent
ALLOWED = {"CNAME", ".html", ".css", ".js", ".json", ".md", ".py", ".png", ".jpg", ".jpeg", ".webp", ".gitkeep"}
MAGIC = {".png": b"\x89PNG\r\n\x1a\n", ".jpg": b"\xff\xd8\xff", ".jpeg": b"\xff\xd8\xff", ".webp": b"RIFF"}
BAD = re.compile(rb"<\?php|<\?=|eval\s*\(|base64_decode|document\.write|atob\s*\(|new Function|<script[^>]+src=[\"']?https?:|\bon\w+\s*=\s*[\"']", re.I)
errs = []
for p in sorted(root.rglob("*")):
    if not p.is_file(): continue
    rel = p.relative_to(root)
    if rel.parts[0] in (".git", ".github"): continue
    ext = p.suffix.lower() or p.name
    if ext not in ALLOWED: errs.append(f"{rel}: file type not allowed")
    if p.name.startswith(".") and p.name != ".gitkeep": errs.append(f"{rel}: hidden file (e.g. .htaccess) not allowed")
    data = p.read_bytes()
    if ext in MAGIC:
        if not data.startswith(MAGIC[ext]): errs.append(f"{rel}: not a real {ext} image")
        if re.search(rb"<\?php|<script|(?:<\?=|<%@)[ -~\s]{12}", data, re.I): errs.append(f"{rel}: code hidden inside image")
    elif ext in {".html", ".js", ".css"} and BAD.search(data): errs.append(f"{rel}: risky code pattern")
    if ext == ".html" and b"Content-Security-Policy" not in data: errs.append(f"{rel}: missing Content-Security-Policy")
print("\n".join(errs) or "site OK"); sys.exit(bool(errs))
