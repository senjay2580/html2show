"""
TTS 一键合成 + 段落时间提取
==========================
读 <topic_dir>/narration.txt -> 输出 narration.mp3 + narration.srt
最后打印每段(paragraph) 末尾时间, 直接用作 record.py 的 SLIDE_DWELLS.

用法:
  python video/tools/tts.py video/408/os/deadlock
  python video/tools/tts.py video/408/os/deadlock --voice zh-CN-XiaoxiaoNeural

可用音色 (zh-CN):
  YunxiNeural    男 · 年轻活泼 (默认)
  YunyangNeural  男 · 专业新闻
  XiaoxiaoNeural 女 · 温暖亲和
  XiaoyiNeural   女 · 活泼明亮
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from pathlib import Path


def parse_srt_paragraph_ends(srt_path: Path, narration_text: str) -> list[float]:
    """根据 narration.txt 段落数, 取每段末句的 SRT end_time (秒)."""
    paragraphs = [p.strip() for p in narration_text.split("\n\n") if p.strip()]

    # 解析 SRT
    blocks = re.split(r"\n\s*\n", srt_path.read_text(encoding="utf-8").strip())
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 3:
            continue
        m = re.match(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)", lines[1])
        if not m:
            continue
        end_h, end_m, end_s = m.group(2).replace(",", ".").split(":")
        end_t = int(end_h) * 3600 + int(end_m) * 60 + float(end_s)
        text = " ".join(lines[2:]).strip()
        cues.append((end_t, text))

    # 段尾匹配: 用段落最后 ~10 字作为锚, 在 cues 里找包含该锚的最早 cue
    para_ends = []
    cursor = 0
    for para in paragraphs:
        anchor = para[-10:].replace(" ", "")
        found_t = None
        for i in range(cursor, len(cues)):
            t, txt = cues[i]
            if anchor[-6:] in txt.replace(" ", "") or anchor[:6] in txt.replace(" ", ""):
                found_t = t
                cursor = i + 1
        if found_t is None and cues:
            # 回退: 用 cursor-1 或最后一个
            found_t = cues[cursor - 1][0] if cursor > 0 else cues[-1][0]
        para_ends.append(found_t or 0.0)
    return para_ends


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topic_dir", help="例如 video/408/os/deadlock")
    ap.add_argument("--voice", default="zh-CN-YunxiNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--pitch", default="+0Hz")
    args = ap.parse_args()

    topic = Path(args.topic_dir).resolve()
    txt   = topic / "narration.txt"
    mp3   = topic / "narration.mp3"
    srt   = topic / "narration.srt"

    if not txt.exists():
        sys.exit(f"missing {txt}")

    print(f"voice = {args.voice}")
    print(f"input = {txt}")
    cmd = [
        sys.executable, "-m", "edge_tts",
        "--voice", args.voice,
        f"--rate={args.rate}",
        f"--pitch={args.pitch}",
        "-f", str(txt),
        "--write-media", str(mp3),
        "--write-subtitles", str(srt),
    ]
    subprocess.run(cmd, check=True)

    print(f"\nout   = {mp3.name}, {srt.name}")
    text = txt.read_text(encoding="utf-8")
    para_ends = parse_srt_paragraph_ends(srt, text)
    if para_ends:
        print("\n# === SLIDE_DWELLS (秒, 复制到 record.py) ===")
        prev = 0.0
        print("SLIDE_DWELLS = [")
        for i, t in enumerate(para_ends):
            d = t - prev
            print(f"    {d:6.3f},   # Slide {i+1}  (end={t:.3f}s)")
            prev = t
        print("]")
        print(f"# total = {para_ends[-1]:.1f}s")


if __name__ == "__main__":
    main()
