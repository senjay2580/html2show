# video/ — 教学视频工作区

每个 `pages/<path>/<topic>.html` 教学页对应一个 `video/<path>/<topic>/` 子目录，目录结构与 `pages/` 一一镜像。

---

## 📂 目录结构（与 pages/ 镜像）

```
video/
├── _template/                    新主题起始模板（复制使用）
│   ├── script.md
│   ├── narration.txt
│   └── record.py
│
├── tools/                        共享工具
│   ├── tts.py                    一键 TTS + 自动提取段落时长
│   └── merge.ps1                 webm + mp3 → mp4（按 trim_offset 对齐）
│
├── 408/                          ← 与 pages/408/ 一一对应
│   └── os/
│       └── deadlock/             ← 对应 pages/408/os/deadlock.html
│           ├── script.md         分镜稿（每镜画面+旁白要点）
│           ├── narration.txt     喂 TTS 的纯文本（段落=幻灯片）
│           ├── narration.mp3     合成的配音
│           ├── narration.srt     字幕（含每句精确时间）
│           ├── record.py         本主题的 PPT 录制驱动
│           └── out/
│               ├── demo.webm     Playwright 原始录屏（无音）
│               ├── demo.mp4      最终成片（含音）
│               └── trim_offset.txt  音画对齐用
│
└── README.md                     本文件
```

---

## 🎬 标准制作流程（5 步法）

### 0. 前置依赖

```bash
pip install playwright edge-tts
python -m playwright install chromium

# Windows 缺 ffmpeg 时, merge.ps1 自动落到 imageio_ffmpeg 内置版
pip install imageio-ffmpeg
```

### 1. 新建主题

```bash
# 假设要为 pages/408/ds/binary-tree.html 做视频
mkdir -p video/408/ds/binary-tree
cp video/_template/* video/408/ds/binary-tree/
```

### 2. 写文案（`narration.txt`）

按 `script.md` 的 7 段结构写（封面 / 定义 / 条件 / 策略 / 算法 / 辨析 / 考点）。
**段落之间用空行分隔** — 这就是幻灯片切换点。

**风格要求**：
- 用"我们"主导，不要"咱们/玩意儿"
- 术语后跟一句直觉解释
- 善用类比 + 数字震撼 + 4 字思想总结
- 不要照念 PPT 元素（"卡片"/"右边"/"左卡"/"打星号"）
- 开场用生活化钩子或反差陈述切入

### 3. TTS + 自动测时

```bash
# 一行搞定: 合成 mp3 + srt + 打印 SLIDE_DWELLS
python video/tools/tts.py video/408/ds/binary-tree

# 输出形如:
# SLIDE_DWELLS = [ 18.175, 47.462, ... ]
```

把打印的 `SLIDE_DWELLS` 数组**直接覆盖**到 `record.py` 里。
也修改 `PAGE_REL = "pages/408/ds/binary-tree.html"`。

### 4. 录制（PPT 模式自动驱动）

```bash
# 仓库根起 http server (避免 file:// 拉不到资源)
python -m http.server 8765

# 另一个终端
python video/408/ds/binary-tree/record.py
```

脚本会：
1. 用 Chromium 打开页面（1920×1080）
2. 自动点击 PPT 按钮进入演示模式
3. 按 `SLIDE_DWELLS` 一页一页翻
4. 录像存为 `out/demo.webm`
5. 测得首张幻灯片就绪偏移写入 `out/trim_offset.txt`

### 5. 合并 → 最终 mp4

```bash
pwsh video/tools/merge.ps1 video/408/ds/binary-tree
# -> out/demo.mp4
```

ffmpeg 用 `-ss <trim_offset>` 跳过页面加载头部，让音频第一帧 = 视频第一帧。

---

## 🎤 TTS 音色

默认 `zh-CN-YunxiNeural`（云希，男声·年轻活泼）。如需替换：

```bash
python video/tools/tts.py video/408/ds/binary-tree --voice zh-CN-XiaoxiaoNeural
```

| 推荐音色 | 性别 | 风格 |
|---|---|---|
| YunxiNeural | 男 | 年轻活泼 · 科技 / 教学 |
| YunyangNeural | 男 | 专业新闻 · 沉稳 |
| XiaoxiaoNeural | 女 | 温暖亲和 |
| XiaoyiNeural | 女 | 活泼明亮 |

---

## 🐛 已知坑位

- **Chromium 录制必须显式 `--window-size`，不能 `--start-maximized`**：否则窗口比 viewport 大，录到的画面只有左上角 1920×1080 一块。
- **进入 PPT 模式后必须手动 `dispatchEvent('resize')`**：让 `fitActiveSlide()` 重新按正确视口算缩放，否则首张可能错位。
- **音画对齐靠 `trim_offset.txt`**：因为录制 context 创建到首帧渲染稳定有 ~3s 延迟，必须用 `ffmpeg -ss` 切掉。
- **manifest.json 用 fetch 加载**：所以必须走 http server，不能 `file://`。

---

## 🚀 已发布主题

| 主题 | 时长 | 状态 |
|---|---|---|
| [408/os/deadlock](408/os/deadlock/out/demo.mp4) | 6:07 | ✅ 完成 |
