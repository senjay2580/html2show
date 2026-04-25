"""
{{Topic}} 教学视频录制
================================
PPT 模式自动驱动 + 段落对齐翻页 + 输出 trim_offset 给 ffmpeg 对齐音画

⚙️ 复用步骤:
  1. 复制本文件到 video/<path>/<topic>/record.py
  2. 修改 PAGE_REL = 目标 HTML 路径
  3. 跑完 TTS 后, 读 narration.srt 段落末端时间, 填入 SLIDE_DWELLS
  4. 运行: python video/<path>/<topic>/record.py
  5. 合并: pwsh video/tools/merge.ps1 video/<path>/<topic>

依赖:
  pip install playwright edge-tts
  python -m playwright install chromium

前置:
  python -m http.server 8765        # 在仓库根
"""
from pathlib import Path
import time
from playwright.sync_api import sync_playwright

HERE      = Path(__file__).resolve().parent
PAGE_REL  = "pages/<path>/<topic>.html"            # ⚠️ 改这里
PAGE_URL  = f"http://127.0.0.1:8765/{PAGE_REL}"
OUT_DIR   = HERE / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORT = {"width": 1920, "height": 1080}

# ⚠️ 改这里 — 与 narration.srt 段落末尾时间对齐
# 计算: dwell[i] = paragraph_end_time[i] - paragraph_end_time[i-1]
# 末段加 0.5–2s 留白
SLIDE_DWELLS = [
    10.0,   # Slide 1 · 封面
    50.0,   # Slide 2
    50.0,   # Slide 3
    50.0,   # Slide 4
    60.0,   # Slide 5
    50.0,   # Slide 6
    30.0,   # Slide 7
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
