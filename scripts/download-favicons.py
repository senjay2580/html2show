"""
Download real favicon for each site → assets/favicons/{slug}.{ext}
Reads scripts/works-meta.json (produced by screenshot-works.py).
"""
import json, urllib.request, ssl, os, mimetypes
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "favicons"
OUT.mkdir(parents=True, exist_ok=True)
META = ROOT / "scripts" / "works-meta.json"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

EXT_BY_CT = {
    "image/svg+xml": ".svg",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/x-icon": ".ico",
    "image/vnd.microsoft.icon": ".ico",
    "image/webp": ".webp",
}

def guess_ext(url, ct):
    if ct and ct.split(";")[0].strip() in EXT_BY_CT:
        return EXT_BY_CT[ct.split(";")[0].strip()]
    p = urlparse(url).path.lower()
    for e in (".svg", ".png", ".jpg", ".ico", ".webp"):
        if p.endswith(e): return e
    return ".ico"

def fetch(url, slug):
    print(f"-> {slug}: {url}")
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "image/*,*/*;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=12, context=ctx) as r:
            data = r.read()
            ct = r.headers.get("Content-Type", "")
        ext = guess_ext(url, ct)
        path = OUT / f"{slug}{ext}"
        path.write_bytes(data)
        print(f"   saved {path.name} ({len(data)} bytes, ct={ct})")
        return f"assets/favicons/{slug}{ext}"
    except Exception as e:
        print(f"   FAIL: {e}")
        return None

def main():
    metas = json.loads(META.read_text(encoding="utf-8"))
    out = {}
    for m in metas:
        if not m.get("favicon"): continue
        out[m["slug"]] = fetch(m["favicon"], m["slug"])
    print("\nlocal favicons:")
    for k, v in out.items():
        print(f"  {k:12} -> {v}")

if __name__ == "__main__":
    main()
