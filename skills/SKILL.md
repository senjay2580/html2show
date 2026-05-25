---
name: teaching-html
description: 把 AI 回答输出成 ThariqS / Anthropic Clay 风的「高效 HTML」(而不是 Markdown 长文)。基于 9 个页面 archetype + 30 个原子组件搭积木：研究讲解 / 方案对比 / 代码评审 / PR 说明 / 实施计划 / 周报 / 故障复盘 / 流程图 / 设计参考 / 教学知识图。当用户说「生成 HTML / 做一份讲义 / 帮我写 PR description / 周报 / 复盘 / 实施计划 / 概念对比 / 知识图」等触发。
---

# Teaching HTML Skill

> **核心思想**: AI 接到任务 → 判定属于哪类工作输出 (archetype) → 复用对应骨架 + 从原子库挑组件填充 → 输出单文件 HTML, 比 Markdown 长文更高效。
>
> **风格基线**: Anthropic Clay 配色 ([ThariqS/html-effectiveness](https://thariqs.github.io/html-effectiveness/) 风) — 6 个语义色 + 字体三体 + hairline 分割 + 无重边框无渐变。

---

## 🌐 远程仓库

- **本地**: `D:\Desktop\html2show\`
- **GitHub**: https://github.com/senjay2580/html2show
- **线上**: https://senjay2580.github.io/html2show/ (push 即自动部署, ~30s)

**生成的新页面放 [`pages/`](../pages/) 下** (skills 自身只是元数据/参考镜像)。

---

## 📁 仓库目录使用规范

```
html2show/
├── pages/                     ★ 新主题放这里, 一文件一主题
│
├── templates/                 ★ 10 个 archetype 骨架, 复制这里开始
│   ├── archetype-research-explainer.html
│   ├── archetype-concept-comparison.html
│   ├── archetype-code-review.html
│   ├── archetype-pr-writeup.html
│   ├── archetype-implementation-plan.html
│   ├── archetype-status-report.html
│   ├── archetype-incident-report.html
│   ├── archetype-flowchart-doc.html
│   ├── archetype-design-reference.html
│   ├── archetype-knowledge-map.html   ★ 教学/考研专用 (含 PPT 模式)
│   └── ARCHETYPES.md          ★ archetype 选择手册
│
├── components/
│   ├── _atoms/                ★ 30 个原子 HTML 片段
│   └── INDEX.md               ★ 原子目录 (按类别索引)
│
├── styles/
│   └── atoms.css              ★ 全局 token + 30 个原子的样式 (唯一样式来源)
│
├── skills/
│   ├── SKILL.md               ★ 本文件
│   └── references/thariqs/    ★ 21 个 ThariqS 原始 HTML (灵感来源)
│
├── docs/
│   ├── archetype-atom-mapping.md   ★ ThariqS → 本项目映射表
│   └── lessons.md             ★ 历史踩坑档案
│
├── images/<topic>/            ★ 主题插图按主题分子目录
└── .github/workflows/pages.yml
```

**铁律**:
1. 页面只放 `pages/`, 资源按类放对应目录
2. 图片按主题分子目录 (`images/<topic>/`)
3. **所有新生成的 HTML 都 `<link rel="stylesheet" href="../styles/atoms.css">`**, 不再内联完整 token 块
4. 改全局色 / 字号 / 间距 → 改 [`styles/atoms.css`](../styles/atoms.css) 一处

---

## ⚡ 标准生成流程 (5 步)

### Step 1 — 判定 archetype (用户输入 → 模板)

| 用户说... | Archetype | 模板 |
|---|---|---|
| "解释 X / 这功能怎么工作" | A1 research-explainer | [archetype-research-explainer.html](../templates/archetype-research-explainer.html) |
| "对比 A 和 B / 几种方式哪种好" | A2 concept-comparison | [archetype-concept-comparison.html](../templates/archetype-concept-comparison.html) |
| "review 这个 PR / 看这段代码" | A3 code-review | [archetype-code-review.html](../templates/archetype-code-review.html) |
| "写个 PR description" | A4 pr-writeup | [archetype-pr-writeup.html](../templates/archetype-pr-writeup.html) |
| "规划怎么做 X / list milestones" | A5 implementation-plan | [archetype-implementation-plan.html](../templates/archetype-implementation-plan.html) |
| "周报 / 这周做了什么 / status" | A6 status-report | [archetype-status-report.html](../templates/archetype-status-report.html) |
| "复盘 / postmortem / 故障分析" | A7 incident-report | [archetype-incident-report.html](../templates/archetype-incident-report.html) |
| "画一下流程 / 部署管线" | A8 flowchart-doc | [archetype-flowchart-doc.html](../templates/archetype-flowchart-doc.html) |
| "设计 token / 色板 / 字号规范" | A9 design-reference | [archetype-design-reference.html](../templates/archetype-design-reference.html) |
| "考研知识点 / 408 / 教学讲义" | A10 knowledge-map (含 PPT) | [archetype-knowledge-map.html](../templates/archetype-knowledge-map.html) |

详见 [templates/ARCHETYPES.md](../templates/ARCHETYPES.md)。

### Step 2 — 复制骨架到 pages/

```bash
cp templates/archetype-<X>.html pages/<topic>.html
```

骨架已带:
- `<link rel="stylesheet" href="../styles/atoms.css">` (相对路径)
- GitHub 头像 favicon
- 占位 Hero + 章节 + 注释槽位

### Step 3 — 填内容 (按需挑原子粘进去)

按 [components/INDEX.md](../components/INDEX.md) 找原子, 复制 [_atoms/<name>.html](../components/_atoms/) 内的 HTML 片段粘到 section 内。

**不要造新 class** — 缺组件就回 [styles/atoms.css](../styles/atoms.css) 加一个, 在 INDEX.md 登记, 再去用。

### Step 4 — 本地预览

```bash
start pages/<topic>.html
```

检查:
- [ ] hero / sections 全部填了占位
- [ ] callout / pitfall / pull-quote 等强调块**至少有一个** (不然全是平铺正文太单调)
- [ ] 切暗夜模式 (浏览器开发者工具加 `<body class="dark">`) 颜色都可读
- [ ] 移动端 width 720px 时单栏布局正常

### Step 5 — 提交 + 推送

```bash
git add pages/<topic>.html images/<topic>/
git commit -m "feat(<topic>): add <archetype-name>"
git push
```

GitHub Pages 自动部署 ~30s。

---

## 🎨 风格系统 · Anthropic Clay

### Tokens (全部来自 [styles/atoms.css](../styles/atoms.css))

```css
/* 6 个语义色 */
--clay:   #D97757   /* 强调主色 — 标签/链接/章节编号 */
--slate:  #141413   /* 主墨字 */
--olive:  #788C5D   /* 成功 / done / 正向 */
--rust:   #B04A3F   /* 警示 / 错误 / 差异 */
--oat:    #E3DACC   /* 柔软分隔 */
--ivory:  #FAF9F5   /* body 背景 */

/* 5 阶灰度 */
--gray-100  #F0EEE6
--gray-300  #D1CFC5   /* 标准描边 1.5px */
--gray-500  #87867F   /* meta / caption */
--gray-700  #3D3D3A   /* 正文备选 */
--white     #FFFFFF   /* panel 底 */

/* 字体三体 */
--serif:  ui-serif, Georgia        /* h1 / h2 / 大数字 */
--sans:   system-ui                /* 正文 */
--mono:   ui-monospace, SF Mono    /* code / label / badge */

/* 圆角 */
--r-sm 6px / --r-row 8px / --r-panel 12px
```

### 字号阶梯 (硬规范, 不要换)

| 用途 | 字号 | 字体 |
|---|---|---|
| display (knowledge-map hero) | 48px | serif 500 |
| h1 (普通 archetype) | 32–36px | serif 500 |
| h2 (section) | 24px | serif 500 |
| h3 (subsection) | 18px | serif 500 |
| 正文 body | 15px | sans 1.65 |
| 表格 / variant body | 14px | sans |
| metric-label / caption | 12px | sans uppercase |
| eyebrow / pill / label | 11px | mono UPPERCASE 0.08em |

### 视觉规范 (做 / 不做)

✅ **做**:
- 描边一律 `1.5px solid var(--gray-300)` 或 `1px hairline`
- 圆角 12px (panel) / 8px (row) / 6px (small) — 不要 4 / 16 / 22 等乱数
- 强调用 **左侧 3-4px stripe** (clay) 而不是 box-shadow
- pill 用 `border-radius: 999px`
- inline code 用 gray-100 底 + 4px 圆角

❌ **不做**:
- 不要 emoji 当主装饰 (用 mono 编号 `01 02 03` 或 `★ ✓ ✗`)
- 不要 box-shadow 做层级 (Clay 风用 hairline, 不堆阴影)
- 不要渐变 (除非 body 噪点/圆点纹理)
- 不要给样式起新名字 (`.my-card`) — 缺组件先加 atoms.css
- 不要内联 `style="..."` 改字号 / 颜色 (走 token)

---

## 🎬 知识图 / 教学模式 · PPT / Export / PlantUML

⚠️ **仅适用 A10 knowledge-map archetype** — 其他 archetype 是参考型, 不带 PPT 模式。

### CDN 引入 (强制)

```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/plantuml-encoder@1.4.0/dist/plantuml-encoder.min.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
```

### ⭐⭐⭐ 视图复用核心架构

**禁止两套独立维护的内容**。整个 HTML **只有一份内容源**: `#flow-view` 里的 hero + sections。PPT slides **必须由 JS 在运行时从 flow-view 自动克隆派生**。

**原因**: 用户曾因维护两份内容而极度不满 — "改一个另一个也要改太烦"。

**强制实现**:
1. PPT 视图的 `<div id="ppt-stage">` 在 HTML 里 **保持空** (没有任何 `<div class="slide">` 子元素)
2. 用 JS `buildSlidesFromFlow()` 在启动时遍历 `#flow-view .hero` 和所有 `#flow-view .section`, 用 `cloneNode(true)` 克隆并包到 `<div class="slide">` 里, append 到 ppt-stage
3. 每次进入 PPT 模式时调用 `reinitPPT()` 重新派生

```javascript
function buildSlidesFromFlow() {
  const stage = document.getElementById('ppt-stage');
  stage.innerHTML = '';
  const sources = [];
  const hero = document.querySelector('#flow-view .hero');
  if (hero) sources.push(hero);
  document.querySelectorAll('#flow-view .section').forEach(s => sources.push(s));
  sources.forEach((src, i) => {
    const slide = document.createElement('div');
    slide.className = 'slide' + (i === 0 ? ' active' : '');
    const clone = src.cloneNode(true);
    clone.classList.remove('anim-init', 'visible');
    slide.appendChild(clone);
    stage.appendChild(slide);
  });
}
```

### PPT 控制逻辑

```javascript
const pptBtn  = document.getElementById('ppt-btn');
const flow    = document.getElementById('flow-view');
const overlay = document.getElementById('ppt-view');
const stage   = document.getElementById('ppt-stage');
let cur = 0, slides = [];

function enterPPT() {
  buildSlidesFromFlow();
  slides = document.querySelectorAll('.slide');
  document.getElementById('ppt-total').textContent = slides.length;
  overlay.classList.add('active');
  flow.style.display = 'none';
  document.body.style.overflow = 'hidden';
  showSlide(0);
}
function exitPPT() {
  overlay.classList.remove('active');
  flow.style.display = '';
  document.body.style.overflow = '';
}
function showSlide(i) {
  cur = Math.max(0, Math.min(slides.length - 1, i));
  slides.forEach((s, k) => s.classList.toggle('active', k === cur));
  document.getElementById('ppt-cur').textContent = cur + 1;
  document.getElementById('ppt-progress').style.width = ((cur + 1) / slides.length * 100) + '%';
}
pptBtn.addEventListener('click', enterPPT);
document.getElementById('ppt-exit').addEventListener('click', exitPPT);
document.addEventListener('keydown', e => {
  if (!overlay.classList.contains('active')) return;
  if (e.key === 'Escape') exitPPT();
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); showSlide(cur + 1); }
  if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); showSlide(cur - 1); }
});
```

### html2canvas 导出 PNG

**必须创建带左右留白的临时容器**, 不要直接截 `#flow-view`:

```javascript
async function exportToPNG() {
  if (overlay.classList.contains('active')) {
    alert('请先退出 PPT 模式再导出'); return;
  }
  document.querySelector('.top-actions').style.display = 'none';
  const wrapper = document.createElement('div');
  wrapper.style.cssText = `
    position: absolute; top: -99999px; left: -99999px;
    background: var(--ivory);
    background-image: radial-gradient(circle, var(--dot, #E3DACC) 1px, transparent 1px);
    background-size: 24px 24px;
    padding: 80px 64px 100px;   /* ⭐ 左右 64px 必须 */
    width: 1208px;              /* ⭐ 1080 + 64*2 */
    box-sizing: border-box;
  `;
  const inner = document.createElement('div');
  inner.style.cssText = 'max-width: 1080px; margin: 0 auto;';
  inner.innerHTML = flow.innerHTML;
  wrapper.appendChild(inner);
  document.body.appendChild(wrapper);
  try {
    await new Promise(r => setTimeout(r, 200));
    const canvas = await html2canvas(wrapper, {
      scale: 2,                  /* ⭐ 高清 2x */
      useCORS: true,
      backgroundColor: '#FAF9F5',
      width: wrapper.offsetWidth,
      height: wrapper.scrollHeight,
      windowWidth: wrapper.offsetWidth,
      windowHeight: wrapper.scrollHeight,
      logging: false,
      imageTimeout: 0
    });
    const link = document.createElement('a');
    link.download = document.title + '.png';
    link.href = canvas.toDataURL('image/png');
    link.click();
  } finally {
    wrapper.remove();
    document.querySelector('.top-actions').style.display = '';
  }
}
```

**留白硬规范**:
- 左右内边距: **64px**
- 顶部内边距: **80px**
- 底部内边距: **100px**
- 容器宽度: **1208px**
- scale: **2**

### PlantUML 渲染

```javascript
const PLANTUML_SERVER = 'https://www.plantuml.com/plantuml/svg/';
function renderPlantUML(el) {
  if (el.dataset.rendered === 'true') return;
  const uml = (el.dataset.uml || '').trim();
  if (!uml || !window.plantumlEncoder) return;
  el.classList.add('loading');
  const encoded = plantumlEncoder.encode(uml);
  const img = document.createElement('img');
  img.src = PLANTUML_SERVER + encoded;
  img.onload = () => {
    el.classList.remove('loading');
    el.innerHTML = '';
    el.appendChild(img);
    el.dataset.rendered = 'true';
  };
}
function renderAllPlantUML() {
  document.querySelectorAll('.plantuml[data-uml]').forEach(renderPlantUML);
}
document.addEventListener('DOMContentLoaded', renderAllPlantUML);
```

**学术风 skinparam 模板** (每个 PlantUML 图都带):
```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName 'Microsoft YaHei'
skinparam shadowing false
skinparam roundCorner 8
skinparam ArrowColor #424245
' 进程/主体: 蓝边圆
skinparam circle { BorderColor #D97757 BorderThickness 2 FontColor #D97757 FontStyle bold }
' 资源/对象: 黑边方框
skinparam rectangle { BorderColor #141413 BorderThickness 1.5 FontColor #141413 }
@enduml
```

**形状语义约定**:
- `circle "P1" as P1` — 进程/主体 (clay 边)
- `rectangle "数据" as D` — 资源/对象 (slate 边)
- `state "等待" as W` — 决策/状态 (yellow 边)
- `node "Error" as E` — 错误/异常 (rust 边)

**注**: 简单流程图优先用 [_atoms/flowchart-svg.html](../components/_atoms/flowchart-svg.html) 内联 SVG, 离线可用、无网络依赖。PlantUML 只在 A10 knowledge-map 历史兼容保留。

---

## 📐 编辑铁律

1. **每个 section 内只用一个主容器** (.def-stack / .variants / .risks / .timeline 等), 不要游离 card
2. **div 平衡检查**: `awk '/<div /{n++}/<\/div>/{c++}END{print n,c}' file.html` 开闭差应为 0
3. **章节数由内容决定**, 不强行凑 6 节; A10 算法主题 7+ 节正常
4. **token 集中管理**: 改色 / 改字号只改 [styles/atoms.css](../styles/atoms.css)
5. **不要造新 class**, 缺组件 → 先加进 atoms.css → 在 INDEX.md 登记 → 再用
6. **暗夜模式自动可用**: body.dark 已在 atoms.css 配好, 不要再单独写

---

## ⛔ 反例 (禁止做)

❌ 在 HTML 里写 `style="color: red"` (除非临时 hack)
❌ 用 emoji 当主装饰 (用 mono 编号 / ★ / ✓ / ✗)
❌ 用 border 区分卡片 (用 1.5px hairline + 圆角)
❌ 用渐变 (除背景圆点)
❌ 手写 PPT slide (会被 buildSlidesFromFlow 覆盖)
❌ 直接放图片在 `pages/` 旁 (按 `images/<topic>/` 分目录)
❌ 改完不 push (本地预览 ≠ 线上可访问)
❌ 完全照抄某一示例的章节布局 (内容服务结构, 不是结构服务内容)

---

## ✅ 检查清单 (生成新主题前过一遍)

- [ ] 判定了 archetype, 选了对应模板
- [ ] `<title>` 改成主题名
- [ ] Hero (eyebrow / h1 / sub) 三个字段都填了
- [ ] 章节数 = 内容需要的最小数量 (不强凑)
- [ ] 每个 section 至少一个原子组件 (callout / tldr / step-list / table 等)
- [ ] **每个 section 内只有一个主容器**
- [ ] **div 平衡** awk 检查通过
- [ ] 至少一个 callout / pull-quote / pitfall 强调块
- [ ] 浏览器打开: 切日夜模式所有元素可读
- [ ] (仅 A10) PPT 模式张数 = 1 (hero) + section 数
- [ ] (仅 A10) 导出 PNG 有左右 64px 留白
- [ ] (仅含 PlantUML) 每个图本地预览无 "Syntax Error" 红字
- [ ] git push, 等 30s, 线上 URL 能开

---

## 🐛 已知历史坑位

迁出到独立文档: [docs/lessons.md](../docs/lessons.md)
- 坑 1 · div 嵌套错位 → PPT 张数不对
- 坑 2 · PlantUML 状态图语法
- 坑 3 · 章节数硬性 6 节 (已废弃)
- 坑 4 · 游离 .card 间距不齐
- 坑 5 · Apple 蓝迁移到 Clay 残留

写新主题前看一眼。

---

## 📚 参考资料

- **真品灵感**: [skills/references/thariqs/](references/thariqs/) — 21 个 ThariqS/html-effectiveness 原始 HTML
- **映射表**: [docs/archetype-atom-mapping.md](../docs/archetype-atom-mapping.md) — ThariqS 20 页 → 9 archetype + 30 atom
- **原子库**: [components/INDEX.md](../components/INDEX.md)
- **骨架库**: [templates/ARCHETYPES.md](../templates/ARCHETYPES.md)
- **样式表**: [styles/atoms.css](../styles/atoms.css)
- **历史坑**: [docs/lessons.md](../docs/lessons.md)
