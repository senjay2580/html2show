---
name: teaching-video
description: 把 html2show 的教学 HTML 知识图自动录制成带配音的 PPT 演示视频。流水线：写文案 → Edge TTS 合成 → 自动测时 → Playwright PPT 模式录屏 → ffmpeg 合并。当用户说"录成视频/做讲解视频/把这个 HTML 转视频/教学视频"等触发。
---

# Teaching Video 生产 Skill

把 `pages/<path>/<topic>.html` 的教学知识图，自动转成 1920×1080 的 PPT 风格教学视频（含 AI 配音）。

**最快路径**：5 个命令，10 分钟出片。

---

## 🌐 仓库结构

```
html2show/
├── pages/<path>/<topic>.html             教学源页 (PPT 模式由页面内置)
└── video/
    ├── _template/                        新主题起始模板
    ├── tools/
    │   ├── tts.py                        TTS + 自动测时
    │   └── merge.ps1                     ffmpeg 合并
    └── <path>/<topic>/                   ← 与 pages/ 一一镜像
        ├── script.md
        ├── narration.txt
        ├── narration.mp3
        ├── narration.srt
        ├── record.py
        └── out/{demo.webm, demo.mp4, trim_offset.txt}
```

**强约束：`video/<path>/<topic>/` 必须与 `pages/<path>/<topic>.html` 路径完全对应**。例：
- `pages/408/os/deadlock.html` → `video/408/os/deadlock/`
- `pages/408/ds/binary-tree.html` → `video/408/ds/binary-tree/`

---

## 🛠 依赖

```bash
pip install playwright edge-tts imageio-ffmpeg
python -m playwright install chromium
```

PowerShell（Windows 自带 `pwsh` 7+）用于 merge.ps1。无系统 ffmpeg 时自动落到 `imageio_ffmpeg` 内置二进制。

---

## 🎬 完整流程（5 步法）

### Step 0 · 前置 HTTP 服务

```bash
python -m http.server 8765        # 在仓库根, 全程保持
```

### Step 1 · 复制模板

```bash
mkdir -p video/<path>/<topic>
cp video/_template/* video/<path>/<topic>/
```

### Step 2 · 写文案（`narration.txt`）

**结构**：7 段，每段对应 PPT 一页（封面 + 6 章节）。**段落之间空行分隔**。

**风格规范**（参考 `video/408/os/deadlock/narration.txt`）：

| 维度 | 规范 |
|---|---|
| 视角 | 用"**我们**"主导，不要"咱们/哥们儿/玩意儿" |
| 句式 | 清晰紧凑，偏书面，但每个术语跟一句直觉解释 |
| 开场 | 用**生活化钩子**或反差陈述切入（不直接报"今天讲 X"） |
| 数字 | 善用震撼数字（"4 的 3000 种 = 1 后面 1800 个 0，比宇宙原子还多"） |
| 总结 | 4 字思想短句（"正难则反"/"先借再回滚"） |
| 收尾 | 一句话压缩整章 + 金句 |
| ❌ 禁用 | "卡片"/"框"/"右边"/"左卡"/"打星号"/"看这页"等照念 PPT 的指代 |
| ❌ 禁用 | "佛系/打叉/玩意儿/攥着"等弹幕式过度口语 |

参考 B 站算法 UP（mid 3546647317448859）的"清晰紧凑工科教师"风格。

### Step 3 · TTS + 自动测时

```bash
python video/tools/tts.py video/<path>/<topic>
```

工具会：
1. 调 Edge TTS（默认云希男声）合成 `narration.mp3` + `narration.srt`
2. 读 SRT，按段落分组，**自动算出每张幻灯片的 dwell 秒数**
3. 打印形如：

```
SLIDE_DWELLS = [
    18.175,   # Slide 1  (end=18.175s)
    47.462,   # Slide 2  (end=65.637s)
    ...
]
```

**直接复制**这个数组，覆盖到 `record.py` 的 `SLIDE_DWELLS`。
同时修改 `PAGE_REL = "pages/<path>/<topic>.html"`。

### Step 4 · 录制

```bash
python video/<path>/<topic>/record.py
```

`record.py` 自动完成：
1. Chromium 1920×1080 打开目标页
2. 等加载就绪 → 点击 `#ppt-btn` 进 PPT 模式
3. **`dispatchEvent('resize')`** 让 `fitActiveSlide()` 重算缩放
4. 记录 `trim_offset`（context 启动到首张就绪的偏移，用于音画对齐）
5. 按 `SLIDE_DWELLS` 一页一页翻（`ArrowRight`）
6. 末页 `Escape` 退出，导出 `out/demo.webm`

### Step 5 · 合并

```bash
pwsh video/tools/merge.ps1 video/<path>/<topic>
```

ffmpeg 用 `-ss <trim_offset>` 切掉视频头部加载帧，让音频第一帧 = 视频第一帧，输出 `out/demo.mp4`（H.264 + AAC，1920×1080，可直接上传 B 站/抖音）。

---

## 🐛 关键工程坑位（必读）

### 坑 1: 录制窗口被裁
**症状**：录到的视频右半边是灰色或黑色，幻灯片标题被切到右边
**原因**：`--start-maximized` 让浏览器窗口比 viewport 大，但 `record_video_size` 只截左上角 1920×1080
**修复**：launch args **只用** `--window-size=1920,1080`，移除 `--start-maximized`

### 坑 2: 音画不同步（音频比画面"超前"）
**症状**：最终视频里，旁白讲到第 3 段了画面还停在第 1 张
**原因**：`new_context(record_video_dir=...)` 一调用就开始录像，但页面加载 + PPT 模式打开还需 ~3s
**修复**：`record.py` 在首张幻灯片就绪那一刻记下 `t_audio_start - t_context_start` 写入 `trim_offset.txt`，merge 时 `ffmpeg -ss <trim>` 切掉头部

### 坑 3: PPT 首张布局错位
**症状**：进入 PPT 后第一张内容不居中或被截断
**原因**：`fitActiveSlide()` 在 `enterPPT` 时按当时视口算缩放，但视口还在变化
**修复**：进入 PPT 后立即 `page.evaluate("window.dispatchEvent(new Event('resize'))")`

### 坑 4: file:// 协议拉不到 manifest.json
**症状**：本地双击 HTML 预览时面包屑挂了
**修复**：录制必须走 `http://127.0.0.1:8765`，不能用 `file://`

### 坑 5: yutto 找不到 ffmpeg（仅做素材调研时遇到）
**修复**：`PATH="$(cygpath -u $(python -c 'import imageio_ffmpeg; import os; print(os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe()))')):$PATH"`，并确保把 `ffmpeg-win-x86_64-v7.1.exe` 复制为 `ffmpeg.exe`

---

## 📐 时长 & 节奏经验

| 段落 | 期望字数 | 期望时长（云希 +0%） |
|---|---|---|
| 1 封面 | 50–80 | 10–15s |
| 2 定义 | 200–280 | 40–55s |
| 3 条件/要素 | 200–280 | 40–55s |
| 4 策略对比 | 280–350 | 55–75s |
| 5 核心算法 | 350–450 | 70–90s |
| 6 工具+辨析 | 250–320 | 50–65s |
| 7 考点收尾 | 120–180 | 25–35s |
| **总计** | ~1500–1800 | **5–7 分钟** |

云希 Yunxi 平均 ~5 字/秒。控制总长 ≤ 7 分钟以保证完播率。

---

## 🎤 音色选择

```bash
# 默认: 云希 (男·年轻活泼)
python video/tools/tts.py <topic_dir>

# 替换:
python video/tools/tts.py <topic_dir> --voice zh-CN-XiaoxiaoNeural
```

| 音色 | 性别 | 风格 | 适用 |
|---|---|---|---|
| YunxiNeural | 男 | 年轻活泼 | 默认·科技/算法/CS |
| YunyangNeural | 男 | 专业新闻 | 法律/政治/历史 |
| XiaoxiaoNeural | 女 | 温暖亲和 | 文科/语言学习 |
| XiaoyiNeural | 女 | 活泼明亮 | 少儿/兴趣科普 |

---

## ✅ 验收清单

录完一支视频后逐项核对：

- [ ] 时长在 5–7 分钟内
- [ ] 文件落在 `video/<path>/<topic>/out/demo.mp4`
- [ ] 1920×1080 / 25fps / H.264 + AAC（`ffmpeg -i` 可查）
- [ ] 音画同步（音频第一句 = 第一张幻灯片）
- [ ] PPT 翻页节奏卡在每段最后一字之后 0.2–1.0s 内
- [ ] 文案无"卡片/右边/左卡/打星号"等指代 PPT 的元素
- [ ] 文案无"咱们/玩意儿/佛系"等过度口语
- [ ] 末段有金句收尾

---

## 🔗 相关 Skill

- `teaching-html` — 生成教学 HTML 知识图（本 skill 的输入页面来源）
- `kaoyan-408` / `kaoyan-english` / `kaoyan-politics` — 内容选题来源
