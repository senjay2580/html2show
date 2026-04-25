# html2show

> Apple / Karpathy 风格的教学 HTML 知识图集合 · GitHub Pages 托管 · 双视图 (流式 + PPT) · 公网可访问

线上访问: `https://senjay2580.github.io/html2show/` (GitHub Pages 启用后)

## 📁 目录结构

```
html2show/
├── index.html              # 首页 (默认指向最新主题)
│
├── pages/                  # 各主题知识图 HTML (一个 .html 一个主题)
│   ├── deadlock.html
│   └── ...
│
├── components/             # 可复用 HTML 片段 (snippet 库)
│   ├── cards/              # 各类卡片: card / cond / strat / exam-item
│   ├── quotes/             # 重点引用 / 易错框 / 记忆口诀
│   ├── grids/              # 多列网格: 2/3/4/5 列
│   ├── toc/                # 左侧浮动目录
│   ├── fab/                # 右下角浮动按钮组
│   └── navigation/         # 顶部按钮 / PPT 控件
│
├── styles/                 # 样式
│   ├── base/               # variables.css / reset.css / layout.css / typography.css
│   └── themes/             # apple-light.css / apple-dark.css / 未来其他主题
│
├── scripts/                # JS 模块
│   ├── core/               # toc.js / ppt.js / theme-toggle.js / scroll-progress.js
│   ├── plantuml/           # plantuml-render.js
│   ├── export/             # html2canvas-export.js
│   └── utils/              # debounce.js / dom.js
│
├── assets/                 # 资源
│   ├── icons/              # 自定义 SVG 图标
│   ├── illustrations/      # 插画
│   ├── fonts/              # 字体 (如本地 SF Pro)
│   └── backgrounds/        # 背景图素材
│
├── images/                 # 主题相关插图 (按主题分子目录)
│   ├── _common/            # 跨主题共用图
│   ├── deadlock/
│   ├── os/
│   ├── ds/
│   └── network/
│
├── diagrams/               # 图表源
│   ├── plantuml/           # .puml 源文件
│   └── exported/           # 渲染后的 .png/.svg
│
├── templates/              # 空骨架模板 (新建主题用)
│   └── teaching-html-template.html
│
├── skills/                 # Claude Code Skill 集合
│   ├── SKILL.md            # teaching-html 主 skill
│   ├── examples/           # 模板镜像
│   ├── references/
│   └── teaching-video/     # ★ 教学视频生产 skill (HTML → mp4)
│       └── SKILL.md
│
├── video/                  # ★ 教学视频工作区, 与 pages/ 一一镜像
│   ├── _template/          # 新主题起始模板
│   ├── tools/              # tts.py / merge.ps1 共享工具
│   └── <path>/<topic>/     # 与 pages/<path>/<topic>.html 对应
│       ├── narration.txt   # 文案
│       ├── narration.mp3   # Edge TTS 配音
│       ├── narration.srt   # 字幕
│       ├── record.py       # PPT 模式自动录制
│       └── out/demo.mp4    # 最终成片 (1920x1080)
│
├── docs/                   # 设计文档 / 开发笔记
│
└── .github/
    └── workflows/          # GitHub Actions (Pages 部署等)
```

## 🚀 新建一个主题

```bash
# 1. 复制空骨架
cp templates/teaching-html-template.html pages/<topic>.html

# 2. 改 <title> + Hero + 各 section

# 3. 重新生成首页索引 (扫描 pages/ 自动产出 manifest.json)
node scripts/build-manifest.js

# 4. 浏览器打开 home.html 预览首页 / pages/<topic>.html 预览主题

# 5. 提交并推送, GitHub Pages 自动更新
git add pages/<topic>.html manifest.json
git commit -m "feat: add <topic> knowledge map"
git push
```

> 也可在 pages/ 下创建子目录组织主题, 例如 `pages/os/<topic>.html`,
> 首页会自动识别为子目录卡片, 点击进入下一级。

## 🎨 设计规范

- **风格**: Apple + Karpathy geek 极简, 蓝白配色, 网格点状背景
- **零 border / 零渐变**, 用 box-shadow 制造层次
- **Lucide 图标库** (CDN) 替代 inline SVG
- **PlantUML** 学术风画图 (CDN 渲染)
- **html2canvas** 高清 PNG 导出
- **双视图**: 流式滚动 (默认) + PPT 模式 (按钮触发, ESC 退出)
- **左侧浮动 TOC** 自动从 section 提取标题, 跳转 + 高亮
- **日夜模式**: localStorage 记忆, 完整 CSS 变量切换

## 🔧 GitHub Pages 启用

```bash
# 在仓库 Settings > Pages 中:
# Source: Deploy from branch
# Branch: main, folder: / (root)
# 保存后 1-2 分钟即可访问 https://senjay2580.github.io/html2show/
```

## 🎬 把主题录成教学视频

每个 `pages/<path>/<topic>.html` 可一键转成带配音的 PPT 演示视频（1920×1080，5–7 分钟）。

```bash
# 1. 复制模板
mkdir -p video/<path>/<topic>
cp video/_template/* video/<path>/<topic>/

# 2. 写文案 (参考 video/408/os/deadlock/narration.txt 风格)
$EDITOR video/<path>/<topic>/narration.txt

# 3. TTS + 自动测时, 复制打印的 SLIDE_DWELLS 到 record.py
python video/tools/tts.py video/<path>/<topic>

# 4. 录制 (需先 python -m http.server 8765)
python video/<path>/<topic>/record.py

# 5. 合并 → 最终 mp4
pwsh video/tools/merge.ps1 video/<path>/<topic>
```

完整工作流见 [video/README.md](video/README.md) 与 [skills/teaching-video/SKILL.md](skills/teaching-video/SKILL.md)。

**已发布**：
- [video/408/os/deadlock/out/demo.mp4](video/408/os/deadlock/out/demo.mp4) · 6:07 · Deadlock 完整讲解

---

## 📦 Skill 同步

`skills/` 是 Claude Code Skill 集合（多 skill 并存）：
- `SKILL.md` — teaching-html（生成知识图）
- `teaching-video/SKILL.md` — 教学视频生产

本地修改后同步到 `~/.claude/commands/`：
```bash
cp -r skills/* ~/.claude/commands/
```
