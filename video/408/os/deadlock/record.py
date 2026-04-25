"""
408 / OS / Deadlock 教学视频录制
================================
PPT 模式自动驱动 + 段落对齐翻页 + 输出 trim_offset 给 ffmpeg 对齐音画

依赖:
  pip install playwright edge-tts
  python -m playwright install chromium

前置:
  在仓库根启 http server: python -m http.server 8765

运行:
  python video/408/os/deadlock/record.py
  pwsh video/tools/merge.ps1 video/408/os/deadlock
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

HERE       = Path(__file__).resolve().parent          # video/408/os/deadlock/
REPO_ROOT  = HERE.parents[3]                          # html2show/
PAGE_REL   = "pages/408/os/deadlock.html"
PAGE_URL   = f"http://127.0.0.1:8765/{PAGE_REL}"
OUT_DIR    = HERE / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORT = {"width": 1920, "height": 1080}

# 与 narration.srt 段落末尾时间对齐
# 每张 dwell = 该段最后一句 end - 上一段最后一句 end
SLIDE_DWELLS = [
    18.175,   # Slide 1 · 封面 Hero
    47.462,   # Slide 2 · 01 什么是死锁
    42.988,   # Slide 3 · 02 4 必要条件
    76.525,   # Slide 4 · 03 3 大处理策略
    80.325,   # Slide 5 · 04 银行家算法
    66.873,   # Slide 6 · 05 RAG + 辨析
    35.0,     # Slide 7 · 06 高频考点  (含尾部留白)
]

PRE_ROLL, POST_ROLL = 0.5, 1.0


def wait(s: float):
    if s > 0:
        time.sleep(s)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                f"--window-size={VIEWPORT['width']},{VIEWPORT['height']}",
                "--window-position=0,0",
                "--disable-blink-features=AutomationControlled",
            ],
        )
        context = browser.new_context(
            viewport=VIEWPORT,
            record_video_dir=str(OUT_DIR),
            record_video_size=VIEWPORT,
            device_scale_factor=1,
        )

        t_context_start = time.monotonic()
        page = context.new_page()
        page.goto(PAGE_URL)
        page.wait_for_selector("h1")
        page.wait_for_selector(".section")
        wait(0.8)

        page.locator("#ppt-btn").click()
        page.wait_for_selector("#ppt-view.active", timeout=5000)
        wait(PRE_ROLL)
        page.evaluate("window.dispatchEvent(new Event('resize'))")
        wait(0.3)

        t_audio_start = time.monotonic()
        trim_offset = t_audio_start - t_context_start
        (OUT_DIR / "trim_offset.txt").write_text(f"{trim_offset:.3f}")
        print(f"trim_offset = {trim_offset:.3f}s")

        for i, dwell in enumerate(SLIDE_DWELLS):
            wait(dwell)
            if i < len(SLIDE_DWELLS) - 1:
                page.keyboard.press("ArrowRight")

        wait(POST_ROLL)
        page.keyboard.press("Escape")
        wait(0.4)

        context.close()
        browser.close()

    webms = sorted(OUT_DIR.glob("*.webm"), key=lambda f: f.stat().st_mtime)
    if webms:
        latest = webms[-1]
        target = OUT_DIR / "demo.webm"
        if target.exists():
            target.unlink()
        latest.rename(target)
        print(f"OK -> {target}")


if __name__ == "__main__":
    main()
