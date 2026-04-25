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
├── skills/                 # Claude Code 全局 Skill (与 ~/.claude/commands/teaching-html 同步)
│   ├── SKILL.md
│   ├── examples/
│   └── references/
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

## 📦 Skill 同步

`skills/` 目录是 Claude Code 全局 skill `teaching-html` 的镜像。
本地修改后:
```bash
# 仓库 → 全局 skill
cp -r skills/* ~/.claude/commands/teaching-html/
# 全局 skill → 仓库
cp -r ~/.claude/commands/teaching-html/* skills/
```
