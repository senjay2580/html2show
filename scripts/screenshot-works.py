"""
Screenshot all 6 personal-project sites + extract title/description.
Output: assets/screenshots/{slug}.jpg + scripts/works-meta.json
"""
import json, os, sys, re
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)
META_PATH = ROOT / "scripts" / "works-meta.json"

SITES = [
    {"slug": "lumina",     "url": "https://lumina-three-green.vercel.app/"},
    {"slug": "fluxfilter", "url": "https://flux-filter.vercel.app/"},
    {"slug": "archat",     "url": "https://archat-kappa.vercel.app/"},
    {"slug": "dashboard",  "url": "http://120.76.158.129:8080/dashboard"},
    {"slug": "service",    "url": "http://8.159.154.189:3001/"},
    {"slug": "chat",       "url": "http://120.76.158.129:3782/chat"},
]

def grab(page, url, slug, out):
    print(f"-> {slug}: {url}")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(2500)
    except Exception as e:
        print(f"   nav warn: {e}")
    title = ""
    try: title = page.title() or ""
    except: pass
    desc = ""
    try:
        desc = page.evaluate("() => document.querySelector('meta[name=description]')?.content || document.querySelector('meta[property=\"og:description\"]')?.content || ''")
    except: pass
    h1 = ""
    try:
        h1 = page.evaluate("() => document.querySelector('h1')?.innerText?.slice(0,200) || ''")
    except: pass
    body_text = ""
    try:
        body_text = page.evaluate("() => (document.body?.innerText || '').replace(/\\s+/g,' ').slice(0, 600)")
    except: pass
    fav = ""
    try:
        fav = page.evaluate("""() => {
          const l = document.querySelector('link[rel~=\"icon\"]') || document.querySelector('link[rel=\"shortcut icon\"]');
          return l ? new URL(l.getAttribute('href'), location.href).href : (location.origin + '/favicon.ico');
        }""")
    except: pass
    img = OUT_DIR / f"{slug}.jpg"
    try:
        page.screenshot(path=str(img), type="jpeg", quality=82, full_page=False)
        print(f"   saved {img.name} ({img.stat().st_size//1024} KB)")
    except Exception as e:
        print(f"   shot fail: {e}")
    return {
        "slug": slug, "url": url,
        "title": title.strip(),
        "h1": h1.strip(),
        "desc": desc.strip(),
        "body_text": body_text.strip(),
        "favicon": fav,
        "screenshot": f"assets/screenshots/{slug}.jpg" if img.exists() else None,
    }

def main():
    metas = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            locale="zh-CN",
        )
        page = ctx.new_page()
        for s in SITES:
            try:
                metas.append(grab(page, s["url"], s["slug"], OUT_DIR))
            except Exception as e:
                print(f"!! {s['slug']} fatal: {e}")
                metas.append({"slug": s["slug"], "url": s["url"], "error": str(e)})
        browser.close()
    META_PATH.write_text(json.dumps(metas, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nwrote {META_PATH}")
    for m in metas:
        print(f"  {m['slug']:12} title={m.get('title','')[:60]!r} h1={m.get('h1','')[:60]!r}")

if __name__ == "__main__":
    main()
