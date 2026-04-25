---
name: teaching-html
description: 生成 Apple/Karpathy 极简风格的教学 HTML 知识图。适用于考研/课程知识点总结、概念图、教学讲义。具备双视图模式：默认流式滚动 + PPT 演示模式（按钮触发，键盘导航，ESC 退出）。当用户说"生成知识图""做教学 HTML""做知识点总结图""做 PPT 风讲义"等触发。
---

# Teaching HTML 生成 Skill

生成**极简、高质感、教学风格**的 HTML 知识图，专为考研知识点 / 课程总结 / 概念讲义设计。

## 何时使用

- 用户说："给我生成一个 X 的知识图 / 知识点总结 / 教学 HTML"
- 用户给一个章节内容（如"死锁"、"TCP 三次握手"），希望以视觉化方式整理
- 用户要做考研/课程的可视化讲义

## 必备 CDN 库 (强制)

```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/plantuml-encoder@1.4.0/dist/plantuml-encoder.min.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
```

- **html2canvas**: 高清 PNG 导出
- **plantuml-encoder**: PlantUML 图表编码渲染
- **lucide**: 极简线条图标库 (替代 inline SVG, 配合 Apple 风格)

### Lucide 图标使用
```html
<i data-lucide="moon" style="width:16px;height:16px;"></i>
<i data-lucide="presentation"></i>
<i data-lucide="image-down"></i>
<i data-lucide="arrow-up"></i>
<script>lucide.createIcons();</script>
```
常用图标: moon/sun (日夜)、arrow-up (回顶)、image-down (导出)、presentation (PPT)、chevron-left/right (翻页)。

---

## 左侧浮动目录 (TOC) — 必备

**自动从 #flow-view 的 section 提取标题, 生成左侧导航条, 点击跳转 + 滚动高亮**。
JS 见 examples/deadlock_reference.html 中的 `buildTOC()`。

CSS 关键约束 (避免标题挤成竖排):
```css
.toc { width: 220px; box-sizing: border-box; }     /* 必须固定宽度 */
.toc a {
  display: flex; align-items: center; gap: 10px;
  white-space: nowrap; overflow: hidden;            /* 防换行/竖排 */
}
.toc .title {
  flex: 1; min-width: 0;
  white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis;
  writing-mode: horizontal-tb;                      /* 强制横排 */
}
.toc a.active { background: var(--blue); color: #fff; }
@media (max-width: 1380px) { .toc { display: none; } }
```

行为:
- 点击 → `scrollIntoView({ behavior: 'smooth' })` 平滑跳转
- 滚动 → IntersectionObserver 高亮当前 section
- PPT 模式时自动隐藏 (enterPPT/exitPPT 包装)

---

## 输出物

**单一 HTML 文件**，包含：
1. **流式视图**（默认）：从上往下滚动浏览
2. **PPT 视图**（按钮触发）：全屏幻灯片模式，键盘可控
3. **导出图片**（按钮触发）：流式视图 → 高清 PNG（html2canvas + 2x scale）
4. **画图区**（按需）：使用 Mermaid.js 绘制流程图/关系图/状态图

文件路径：用户指定 / 默认放当前项目的 `explain/images/<topic>_knowledge_map.html`

---

## 设计风格规范（必须严格遵守）

### 视觉哲学
- **极简、教学、Apple + Karpathy geek 风**
- 蓝白配色为主，红色专门留给"重点/易错"
- **零 border、零渐变** — 用 box-shadow 制造层次
- **网格点状背景** — radial-gradient 圆点
- 大量留白，呼吸感

### 配色（CSS 变量必须保留）

```css
:root {
  --blue:    #0071e3;       /* 苹果蓝, 主色 */
  --blue-2:  #0066cc;
  --blue-soft: #e8f1ff;     /* 浅蓝底 */
  --red:     #ff3b30;       /* 重点/易错专用 */
  --red-soft: #fff1f0;
  --ink:     #1d1d1f;       /* 主文字 */
  --ink-2:   #424245;       /* 副文字 */
  --ink-3:   #86868b;       /* 弱文字/标签 */
  --line:    #e8e8ed;       /* 分隔线 */
  --bg:      #fbfbfd;       /* 页面背景 */
  --mono:    'SF Mono', 'JetBrains Mono', 'Consolas', 'Menlo', monospace;
}
```

### 字体栈
```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
             'Inter', 'Microsoft YaHei', 'PingFang SC', sans-serif;
```

### 字号层级（教学风必须有强对比）
- Hero h1: **88px** (PPT 模式 120px)
- Section title: **36px** (PPT 模式 72px)
- Card title: **22px** (PPT 模式 26-36px)
- 副标题/标签: 11-13px 等距字体, 小写, letter-spacing
- 正文: 15-16px (PPT 24px)
- **重点引用**: 28px (PPT 44px)，深色卡片包裹

### 颜色规则
| 用途 | 颜色 | 何时使用 |
|---|---|---|
| 主色调 | `--blue` | 标签、链接、装饰、章节编号 |
| 重点/易错 | `--red` | 易错警示框、`.em` 强调字 |
| 强调框 | 深色背景 `--ink` | 重点引用 / 一句话精华 |
| 通过/正确 | `#5dd4a1` 或 `#1a8a3a` | "✓ 正确"标识 |

### 不要做的事
- ❌ 不要加 border（用 shadow 区分层级）
- ❌ 不要用渐变（除了 `body` 的圆点 background-image）
- ❌ 不要塞满文字（每个 card 重点一句话）
- ❌ 不要用 emoji 当图标（用等距字体的 `01 02 03` 或 `★ ✓ ✗`）

---

## 画图规范（PlantUML · 学术风 · 必须遵守）

⚠️ **不要用 Mermaid**，不要用 Excalidraw，**统一用 PlantUML** 渲染所有图表。
原因：PlantUML 学术风更标准、形状语义更丰富、PPT 模式 display:none 不影响渲染（图片是异步加载的）。

### CDN 引入（两个）
```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/plantuml-encoder@1.4.0/dist/plantuml-encoder.min.js"></script>
```

### 渲染原理
- 把 PlantUML 源码放到 `data-uml` 属性（必须 HTML 转义引号 `&quot;` 和 `&gt;` `&lt;`）
- JS 用 `plantumlEncoder.encode()` 编码后拼接 `https://www.plantuml.com/plantuml/svg/<编码>` URL
- 创建 `<img>` 加载 SVG → 替换容器内容

### 图表容器样式
```css
.diagram-card {
  background: white;
  border-radius: 18px;
  padding: 40px 32px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
  text-align: center;
}
.diagram-label {
  font-family: var(--mono); font-size: 11px; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--blue); margin-bottom: 8px;
}
.diagram-title {
  font-size: 18px; font-weight: 700;
  color: var(--ink); margin-bottom: 24px; letter-spacing: -0.3px;
}
.plantuml {
  display: flex; justify-content: center; align-items: center;
  min-height: 200px;
}
.plantuml img { max-width: 100%; height: auto; display: block; }
.plantuml.loading::before {
  content: '加载图表中...';
  color: var(--ink-3);
  font-family: var(--mono);
  font-size: 13px;
}
```

### 标准用法
```html
<div class="diagram-card">
  <div class="diagram-label">Diagram · 副标题</div>
  <div class="diagram-title">图表主标题</div>
  <div class="plantuml" id="diagram-xxx" data-uml="
@startuml
... PlantUML 代码 (引号必须转义为 &quot;)
@enduml
  "></div>
</div>
```

### 必备渲染 JS
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
function renderAllPlantUML(scope) {
  (scope || document).querySelectorAll('.plantuml[data-uml]').forEach(renderPlantUML);
}
// 启动
if (document.readyState === 'loading')
  document.addEventListener('DOMContentLoaded', () => renderAllPlantUML());
else renderAllPlantUML();
```

### 学术风 skinparam 模板（必须保留这套主题）
所有 PlantUML 图都要带这段开头的 skinparam：

```plantuml
@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName 'Microsoft YaHei'
skinparam defaultFontSize 14
skinparam shadowing false
skinparam roundCorner 8
skinparam padding 6
skinparam ArrowThickness 1.4
skinparam ArrowColor #424245
skinparam ArrowFontColor #1d1d1f
skinparam ArrowFontSize 13

' 进程/主体: 蓝色圆形 (语义=主动方)
skinparam circle {
  BackgroundColor #FFFFFF
  BorderColor #0071e3
  BorderThickness 2
  FontColor #0071e3
  FontStyle bold
}
' 资源/对象: 黑边方框 (语义=被动方)
skinparam rectangle {
  BackgroundColor #FFFFFF
  BorderColor #1d1d1f
  BorderThickness 1.5
  FontColor #1d1d1f
}
' 决策/状态: 黄色菱形
skinparam state {
  BackgroundColor #fffbeb
  BorderColor #d97706
  FontColor #92400e
}
' 强调/错误: 红色
skinparam node {
  BackgroundColor #fff1f0
  BorderColor #ff3b30
  FontColor #ff3b30
}
@enduml
```

### 形状语义约定（按教学语义选）

| 语义 | PlantUML 形状 | 配色 |
|---|---|---|
| **进程 / 主体 / 用户** | `circle "P1" as P1` | 蓝色边 (主动方) |
| **资源 / 数据 / 对象** | `rectangle "数据" as D` | 黑色边 (被动方) |
| **状态 / 决策点** | `state "等待" as W` | 黄色边 |
| **错误 / 异常 / 阻塞** | `node "Error" as E` | 红色边 |
| **数据库 / 存储** | `database "DB" as DB` | 灰色 |
| **云 / 外部服务** | `cloud "API" as API` | 浅蓝 |
| **角色 / 用户** | `actor "User" as U` | 黑色 |
| **包 / 模块** | `package "模块名" {...}` | 圆角框 |
| **组件** | `component "Auth"` | 立体方块 |

### 推荐图表类型（按教学场景）

| 场景 | PlantUML 类型 | 关键语法 |
|---|---|---|
| 关系/资源分配 | object diagram | `circle/rectangle + 箭头` |
| 算法流程 | activity diagram | `start/:动作;/if/end` |
| 状态变化 | state diagram | `[*] --> S1 --> S2` |
| 时序/通信 | sequence diagram | `A -> B: msg` |
| 类/数据结构 | class diagram | `class A {...}` |
| 部署/架构 | deployment diagram | `node/database/cloud` |

### 写 PlantUML 的硬要求
1. **必须放在 `data-uml` 属性内**, 引号转义为 `&quot;`, `<` `>` 转义为 `&lt;` `&gt;`
2. **每个图必须给 id**: `<div class="plantuml" id="diagram-xxx" ...>`，方便 PPT 复用
3. **必须包含完整 skinparam**（见上面学术风模板）
4. **节点用 as 别名**: `circle "中文名" as P1` 避免编码问题
5. **箭头明确方向**: `-right->` `-down->` `-up->` `-left->` 控制布局

**画图原则**：
1. 一张图只表达一个核心观点
2. 节点不超过 8 个
3. 必须有标题 (`.diagram-title`)
4. 关键关系/数字直接标在线上 (`-->|文字|`)
5. 抽象概念图优先于纯文字描述

### ⭐⭐⭐ 视图复用核心架构（最重要规则）

**禁止两套独立维护的内容**。整个 HTML **只有一份内容源**：`#flow-view` 里的 hero + sections。
PPT slides **必须由 JS 在运行时从 flow-view 自动克隆派生**。

**原因**: 用户曾因维护两份内容而极度不满 — "改一个另一个也要改太烦"。

**强制实现**:
1. PPT 视图的 `<div id="ppt-stage">` 在 HTML 里 **保持空** (没有任何 `<div class="slide">` 子元素)
2. 用 JS `buildSlidesFromFlow()` 函数在启动时遍历 `#flow-view .hero` 和所有 `#flow-view .section`, 用 `cloneNode(true)` 克隆并包到 `<div class="slide">` 里, append 到 ppt-stage
3. 每次进入 PPT 模式时调用 `reinitPPT()` 重新派生 (保证 flow 改了能即时同步)

**结果**: 改 flow-view 内容 → PPT 自动同步, 改 CSS class 样式 → 两边都生效

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

### ⭐ 双视图必须复用图表（强制规则）

**任何在流式视图里出现的 Mermaid 图表，必须在 PPT 视图里也有对应幻灯片**。
**反之亦然 —— 不要让 PPT 缺图**。

#### PPT 模式专用图表样式
```css
/* 加到 .slide 内部样式区 */
.slide .s-diagram-wrap {
  margin-top: 40px;
  background: white;
  border-radius: 24px;
  padding: 48px 40px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.06);
  text-align: center;
}
.slide .s-diagram-wrap .lab {
  font-family: var(--mono); font-size: 12px; color: var(--blue);
  font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 12px;
}
.slide .s-diagram-wrap .title {
  font-size: 22px; font-weight: 700; color: var(--ink);
  margin-bottom: 32px; letter-spacing: -0.3px;
}
.slide .s-diagram-wrap .mermaid {
  transform: scale(1.4);
  transform-origin: center;
  margin: 40px 0;
}
```

#### PPT 中放图表的标准结构
```html
<div class="slide">
  <div class="s-eyebrow">01 — Visualization</div>
  <h2>图表标题</h2>
  <div class="s-diagram-wrap">
    <div class="lab">Diagram · 副标题</div>
    <div class="title">说明这张图在表达什么</div>
    <div class="mermaid">
      <!-- 完整复制流式视图里同一个 Mermaid 代码 -->
graph LR
    A((节点1)) --> B[节点2]
    </div>
  </div>
</div>
```

#### 跨视图复用的工作流程
```
1. 在流式视图的 .diagram-card 里写一次 Mermaid
2. 完整复制 Mermaid 代码到 PPT 的 .s-diagram-wrap > .mermaid 里
3. PPT 里给图加更大的标题和副标题(因为屏幕大)
4. Mermaid 在初始化时会自动渲染所有 .mermaid 元素 —— 不要担心 display:none
```

#### 反例 (不要做)
- ❌ 流式视图有图但 PPT 没图 —— 用户切到 PPT 模式时会困惑"图哪去了"
- ❌ PPT 里直接 `<img>` 引用流式视图的图 —— 图无法独立缩放
- ❌ 用 iframe 嵌入 —— 渲染问题多
- ❌ 不加 `transform: scale(1.4)` —— PPT 屏幕大，图太小看不清

---

## 导出图片规范（html2canvas · 必须遵守）

### CDN 引入
```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
```

### 导出函数核心要求 ⭐
**导出时必须创建带左右留白的临时容器**，不要直接截 `#flow-view`：

```javascript
async function exportToPNG() {
  if (pptMode) { alert('请先退出 PPT 模式再导出'); return; }

  exportBtn.disabled = true;
  exportLoading.style.display = 'flex';
  const topActions = document.querySelector('.top-actions');
  topActions.style.display = 'none';

  // ★ 关键: 创建临时导出容器, 加足留白
  const flowView = document.getElementById('flow-view');
  const exportWrapper = document.createElement('div');
  exportWrapper.style.cssText = `
    position: absolute;
    top: -99999px; left: -99999px;
    background: #fbfbfd;
    background-image: radial-gradient(circle, #d2d2d7 1px, transparent 1px);
    background-size: 24px 24px;
    padding: 80px 64px 100px 64px;     /* ⭐ 必须有左右 64px 内边距 */
    width: 1208px;                     /* ⭐ 1080 + 64*2 */
    box-sizing: border-box;
  `;
  const inner = document.createElement('div');
  inner.style.cssText = 'max-width: 1080px; margin: 0 auto;';
  inner.innerHTML = flowView.innerHTML;
  exportWrapper.appendChild(inner);
  document.body.appendChild(exportWrapper);

  try {
    await new Promise(r => setTimeout(r, 200));   // 等渲染
    const canvas = await html2canvas(exportWrapper, {
      scale: 2,                                    // ⭐ 高清 2x
      useCORS: true,
      backgroundColor: '#fbfbfd',
      width: exportWrapper.offsetWidth,
      height: exportWrapper.scrollHeight,
      windowWidth: exportWrapper.offsetWidth,
      windowHeight: exportWrapper.scrollHeight,
      logging: false,
      imageTimeout: 0
    });
    // ...生成下载...
  } finally {
    if (exportWrapper.parentNode) exportWrapper.parentNode.removeChild(exportWrapper);
    topActions.style.display = '';
    exportBtn.disabled = false;
  }
}
```

### 导出留白硬规范
- **左右内边距**: **64px**（必须）
- **顶部内边距**: **80px**
- **底部内边距**: **100px**
- **容器宽度**: **1208px** (= 1080 + 64×2)
- **scale**: **2** (高清 2x 像素)
- **backgroundColor**: `#fbfbfd` (与页面一致)
- **背景**: 必须包含网格点状背景（与页面一致）

### 反例 (不要做)
❌ 直接 `html2canvas(document.getElementById('flow-view'), ...)` —— 会贴边
❌ 用 `body` 截 —— 会包含按钮
❌ scale: 1 —— 不够清晰
❌ 忘记隐藏 `.top-actions` —— 按钮出现在图片里

### 顶部按钮组结构
```html
<div class="top-actions">
  <button class="top-btn export" id="export-btn">
    <span class="icon"></span>导出图片
  </button>
  <button class="top-btn" id="ppt-btn">
    <span class="icon"></span>PPT 模式
  </button>
</div>
```

---

## HTML 结构模板

### 整体骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>主题名 · Knowledge Map</title>
  <style>/* 完整 CSS, 见下方 */</style>
</head>
<body>
  <!-- 模式切换按钮(右上角悬浮) -->
  <button class="mode-toggle" id="ppt-btn">
    <span class="icon"></span> PPT 模式
  </button>

  <!-- 流式视图 -->
  <div class="page" id="flow-view">
    <div class="hero">...</div>
    <div class="section">...</div>  <!-- 重复 N 个 -->
  </div>

  <!-- PPT 视图(默认 hidden) -->
  <div class="ppt-overlay" id="ppt-view">
    <div class="ppt-stage" id="ppt-stage">
      <div class="slide active">...</div>
      <div class="slide">...</div>
      <!-- 重复 N 张 -->
    </div>
    <div class="ppt-bar">
      <div class="info"><span id="ppt-cur">1</span> / <span id="ppt-total">N</span></div>
      <div class="progress"><div class="fill" id="ppt-progress"></div></div>
      <div class="nav">
        <button id="ppt-prev">‹</button>
        <button id="ppt-next">›</button>
      </div>
      <button class="btn" id="ppt-exit">ESC 退出</button>
    </div>
  </div>

  <div class="ppt-tip" id="ppt-tip"></div>

  <script>/* PPT 切换逻辑, 见下方 */</script>
</body>
</html>
```

### 章节结构(每个 section)

```html
<div class="section">
  <div class="section-head">
    <span class="section-num">01</span>           <!-- 等距字体编号 -->
    <h2 class="section-title">章节标题</h2>
    <span class="section-sub">English Subtitle</span>
  </div>
  <!-- 章节内容: card / grid / quote / pitfall -->
</div>
```

### 关键内容块(按需组合)

#### 1. 普通 Card
```html
<div class="card">
  <div class="card-label">LABEL</div>           <!-- eyebrow text -->
  <div class="card-h">主标题</div>
  <div class="card-body">正文描述</div>
  <div class="card-meta">类比 ▸ 补充信息</div>   <!-- 灰色辅助 -->
</div>
```

#### 2. 多列并排(grid)
```html
<div class="cond-grid">    <!-- 4 列 -->
  <div class="cond">
    <div class="cond-num">01</div>
    <div class="cond-name">名称</div>
    <div class="cond-en">ENGLISH</div>
    <div class="cond-desc">描述<br>多行</div>
  </div>
  <!-- 重复 -->
</div>
```

#### 3. 重点引用(深色卡片)⭐
```html
<div class="key-quote">
  <div class="lab">重点</div>
  <div class="text">
    主要论点 <span class="em">易错关键词(红)</span><br>
    <span class="ok">正确做法(绿)</span>
  </div>
</div>
```

#### 4. 易错警示框(红色)⭐
```html
<div class="pitfall">
  <div class="lab">Pitfall · 高频易错</div>
  <div class="head">这些说法都是 错的</div>
  <ul>
    <li>"<b>错误说法</b>" <span class="right">✓ 正确: 解释</span></li>
  </ul>
</div>
```

#### 5. 记忆口诀
```html
<div class="mnemonic">
  <div class="lab">Mnemonic · 记忆口诀</div>
  <div class="text">A + B + C + D</div>
</div>
```

---

## 完整 CSS 模板

⚠️ **必须使用以下完整 CSS**，不要简化或修改基础结构：

```css
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display',
               'Inter', 'Microsoft YaHei', 'PingFang SC', sans-serif;
  color: var(--ink);
  background-color: var(--bg);
  background-image: radial-gradient(circle, #d2d2d7 1px, transparent 1px);
  background-size: 24px 24px;
  line-height: 1.6;
  padding: 80px 24px 120px;
  -webkit-font-smoothing: antialiased;
  letter-spacing: -0.01em;
}
.page { max-width: 1080px; margin: 0 auto; }

/* 模式切换按钮 */
.mode-toggle {
  position: fixed; top: 24px; right: 24px; z-index: 1000;
  background: var(--ink); color: white;
  padding: 12px 20px; border-radius: 999px;
  font-family: var(--mono); font-size: 13px; font-weight: 600;
  cursor: pointer; user-select: none; border: none;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s, background 0.2s;
  display: flex; align-items: center; gap: 8px;
}
.mode-toggle:hover { transform: translateY(-1px); background: var(--blue); }
.mode-toggle .icon { width: 14px; height: 14px; background: var(--blue); border-radius: 3px; }
.mode-toggle:hover .icon { background: white; }

/* Hero */
.hero { text-align: center; margin-bottom: 96px; padding: 48px 0; }
.hero .eyebrow {
  color: var(--blue); font-size: 13px; font-weight: 600;
  letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 24px; font-family: var(--mono);
}
.hero h1 {
  font-size: 88px; font-weight: 700; letter-spacing: -3px;
  color: var(--ink); line-height: 1; margin-bottom: 20px;
}
.hero .sub { color: var(--ink-3); font-size: 20px; font-weight: 400; }

/* Section */
.section { margin-bottom: 80px; }
.section-head {
  display: flex; align-items: baseline; gap: 20px; margin-bottom: 36px;
}
.section-num {
  font-family: var(--mono); font-size: 14px; font-weight: 600;
  color: var(--blue); letter-spacing: 1px;
}
.section-title {
  font-size: 36px; font-weight: 700;
  color: var(--ink); letter-spacing: -1px;
}
.section-sub {
  color: var(--ink-3); font-size: 14px;
  margin-left: auto; font-family: var(--mono);
}

/* Card */
.card {
  background: white; border-radius: 18px; padding: 32px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 8px 24px rgba(0,0,0,0.04);
  transition: transform 0.3s, box-shadow 0.3s;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 16px 36px rgba(0,0,0,0.06);
}
.card-label {
  font-family: var(--mono); font-size: 11px; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: var(--blue); margin-bottom: 12px;
}
.card-h {
  font-size: 22px; font-weight: 700; color: var(--ink);
  margin-bottom: 12px; letter-spacing: -0.5px;
}
.card-body { color: var(--ink-2); font-size: 16px; line-height: 1.7; }
.card-meta { color: var(--ink-3); font-size: 14px; margin-top: 12px; font-family: var(--mono); }

/* 重点引用(深色卡片) */
.key-quote {
  margin: 24px 0; padding: 36px 44px;
  background: var(--ink); color: white;
  border-radius: 22px; text-align: center;
}
.key-quote .lab {
  font-family: var(--mono); font-size: 11px; color: var(--blue);
  font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 16px;
}
.key-quote .text { font-size: 28px; font-weight: 700; line-height: 1.5; letter-spacing: -0.5px; }
.key-quote .text .em { color: #ff6b6b; }
.key-quote .text .ok { color: #5dd4a1; }

/* 易错红色框 */
.pitfall { background: var(--red-soft); border-radius: 16px; padding: 28px 32px; margin: 24px 0; }
.pitfall .lab {
  font-family: var(--mono); font-size: 11px; color: var(--red);
  font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;
}
.pitfall .head { font-size: 22px; font-weight: 700; color: var(--red); margin-bottom: 14px; letter-spacing: -0.5px; }
.pitfall ul { list-style: none; padding: 0; }
.pitfall li {
  color: var(--ink); font-size: 16px; line-height: 1.9;
  padding: 4px 0; display: flex; align-items: baseline; gap: 10px;
}
.pitfall li::before { content: '✗'; color: var(--red); font-weight: 700; }
.pitfall li b { color: var(--red); font-weight: 700; }
.pitfall li .right { color: #5dd4a1; font-weight: 600; margin-left: 8px; }

/* 记忆口诀 */
.mnemonic {
  margin-top: 32px; padding: 28px 36px;
  background: var(--blue-soft); border-radius: 18px; text-align: center;
}
.mnemonic .lab {
  font-family: var(--mono); font-size: 11px; font-weight: 600;
  letter-spacing: 1.5px; color: var(--blue-2);
  text-transform: uppercase; margin-bottom: 10px;
}
.mnemonic .text { font-size: 24px; font-weight: 700; color: var(--ink); letter-spacing: 0.5px; }

/* 多列网格(常用) */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
.grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }

/* PPT 模式 */
.ppt-overlay {
  position: fixed; inset: 0;
  background: var(--bg);
  background-image: radial-gradient(circle, #d2d2d7 1px, transparent 1px);
  background-size: 32px 32px;
  z-index: 9999; display: none; flex-direction: column;
}
.ppt-overlay.active { display: flex; }
.ppt-stage {
  flex: 1; display: flex; align-items: center; justify-content: center;
  padding: 60px 80px; overflow: hidden;
}
.slide { width: 100%; max-width: 1100px; display: none; animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.slide.active { display: block; }
@keyframes slideIn { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
.slide .s-eyebrow {
  font-family: var(--mono); font-size: 14px; color: var(--blue);
  font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 24px;
}
.slide h2 {
  font-size: 72px; font-weight: 700; color: var(--ink);
  letter-spacing: -2px; line-height: 1.05; margin-bottom: 36px;
}
.slide .s-sub { font-size: 28px; color: var(--ink-3); font-weight: 400; }
.slide .s-body { font-size: 24px; color: var(--ink-2); line-height: 1.6; margin-top: 36px; }
.slide .s-body .em { color: var(--red); font-weight: 700; }
.slide .s-body .blue { color: var(--blue); font-weight: 700; }
.slide .s-quote {
  background: var(--ink); color: white; border-radius: 24px;
  padding: 64px 80px; text-align: center; margin-top: 48px;
}
.slide .s-quote .lab {
  font-family: var(--mono); font-size: 14px; color: var(--blue);
  letter-spacing: 2px; text-transform: uppercase; margin-bottom: 24px;
}
.slide .s-quote .txt { font-size: 44px; font-weight: 700; line-height: 1.4; letter-spacing: -1px; }
.slide .s-quote .txt .em { color: #ff6b6b; }

/* PPT 控制条 */
.ppt-bar {
  height: 64px; display: flex; align-items: center; justify-content: space-between;
  padding: 0 32px; background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}
.ppt-bar .progress {
  flex: 1; height: 4px; background: var(--line);
  border-radius: 2px; margin: 0 24px; overflow: hidden;
}
.ppt-bar .progress .fill {
  height: 100%; background: var(--blue);
  transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.ppt-bar .info { font-family: var(--mono); font-size: 13px; color: var(--ink-3); min-width: 100px; }
.ppt-bar .info .cur { color: var(--ink); font-weight: 700; }
.ppt-bar .btn {
  background: var(--ink); color: white; padding: 10px 18px;
  border-radius: 999px; font-family: var(--mono); font-size: 12px;
  font-weight: 600; cursor: pointer; border: none; transition: background 0.2s;
}
.ppt-bar .btn:hover { background: var(--blue); }
.ppt-bar .nav { display: flex; gap: 8px; }
.ppt-bar .nav button {
  width: 36px; height: 36px; border-radius: 50%; border: none;
  background: var(--blue-soft); color: var(--blue);
  font-size: 18px; cursor: pointer; transition: all 0.2s;
}
.ppt-bar .nav button:hover { background: var(--blue); color: white; }
.ppt-bar .nav button:disabled { opacity: 0.3; cursor: not-allowed; }

.ppt-tip {
  position: fixed; bottom: 90px; left: 50%; transform: translateX(-50%);
  background: var(--ink); color: white;
  padding: 12px 20px; border-radius: 999px;
  font-family: var(--mono); font-size: 12px;
  z-index: 10000; opacity: 0; transition: opacity 0.4s; pointer-events: none;
}
.ppt-tip.show { opacity: 1; }

/* 响应式 */
@media (max-width: 900px) {
  .hero h1 { font-size: 56px; letter-spacing: -2px; }
  .section-title { font-size: 28px; }
  .grid-2, .grid-3, .grid-4, .grid-5 { grid-template-columns: 1fr; }
  body { padding: 40px 16px 80px; }
  .key-quote .text { font-size: 20px; }
  .slide h2 { font-size: 40px; }
}
```

---

## 必备 JavaScript（PPT 控制）

⚠️ **完整复制以下 JS，不要修改逻辑**：

```javascript
const pptBtn = document.getElementById('ppt-btn');
const flowView = document.getElementById('flow-view');
const pptView = document.getElementById('ppt-view');
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
const pptCur = document.getElementById('ppt-cur');
const pptTotal = document.getElementById('ppt-total');
const pptProgress = document.getElementById('ppt-progress');
const pptPrev = document.getElementById('ppt-prev');
const pptNext = document.getElementById('ppt-next');
const pptExit = document.getElementById('ppt-exit');
const pptTip = document.getElementById('ppt-tip');
const pptStage = document.getElementById('ppt-stage');

let currentSlide = 0;
let pptMode = false;
pptTotal.textContent = totalSlides;

function showTip(msg) {
  pptTip.textContent = msg;
  pptTip.classList.add('show');
  clearTimeout(pptTip._timer);
  pptTip._timer = setTimeout(() => pptTip.classList.remove('show'), 1500);
}
function enterPPT() {
  pptMode = true;
  pptView.classList.add('active');
  flowView.style.display = 'none';
  document.body.style.overflow = 'hidden';
  showSlide(0);
  showTip('SPACE / ← → 翻页  ·  ESC 退出');
}
function exitPPT() {
  pptMode = false;
  pptView.classList.remove('active');
  flowView.style.display = '';
  document.body.style.overflow = '';
}
function showSlide(idx) {
  if (idx < 0) idx = 0;
  if (idx >= totalSlides) idx = totalSlides - 1;
  currentSlide = idx;
  slides.forEach((s, i) => s.classList.toggle('active', i === idx));
  pptCur.textContent = idx + 1;
  pptProgress.style.width = ((idx + 1) / totalSlides * 100) + '%';
  pptPrev.disabled = (idx === 0);
  pptNext.disabled = (idx === totalSlides - 1);
}
function nextSlide() { showSlide(currentSlide + 1); }
function prevSlide() { showSlide(currentSlide - 1); }
pptBtn.addEventListener('click', enterPPT);
pptExit.addEventListener('click', exitPPT);
pptPrev.addEventListener('click', prevSlide);
pptNext.addEventListener('click', nextSlide);
pptStage.addEventListener('click', (e) => {
  if (!pptMode) return;
  if (e.target === pptStage || e.target.classList.contains('slide')) nextSlide();
});
document.addEventListener('keydown', (e) => {
  if (!pptMode) return;
  switch (e.key) {
    case 'Escape': exitPPT(); break;
    case 'ArrowRight':
    case ' ':
    case 'PageDown': e.preventDefault(); nextSlide(); break;
    case 'ArrowLeft':
    case 'PageUp': e.preventDefault(); prevSlide(); break;
    case 'Home': showSlide(0); break;
    case 'End': showSlide(totalSlides - 1); break;
  }
});
```

---

## 内容生成原则（教学风必须遵守）

### 1. 章节结构（推荐 6 段）
```
01  什么是 X (定义 + 类比)
02  关键概念/必要条件 (横向多卡)
03  核心策略/分类 (3-4 卡片)
04  核心算法/方法 (左右两栏)
05  辨析/对比 (易错强调)
06  考点 + 一句话精华
```

### 2. 每张 PPT 一个核心点
- 标题页 + 每章节 2-3 张 PPT
- 总数控制在 **10-15 张**
- 不要塞满文字，每张突出一个论点

### 3. 重点/易错的标识规则
| 内容类型 | 用什么 | 颜色 |
|---|---|---|
| 一般定义 | `.card` | 默认 |
| 关键论点 | `.key-quote` (深色卡) | `.em`(红) / `.ok`(绿) |
| 易错警示 | `.pitfall` (红底) | 红 |
| 记忆口诀 | `.mnemonic` (浅蓝底) | 蓝 |

### 4. PPT 模式特殊处理
- 标题页：120px 大字 + 居中 + 操作提示
- 重点页：用 `.s-quote` 黑底白字突出
- 每页字号普遍比流式视图大 1.5-2 倍
- 末页提示 "END · 按 ESC 退出"

---

## ⭐ 推荐工作流: 直接复用空骨架模板

skill 自带一个**完整可用的空骨架**:
`references/teaching-html-template.html`

里面已经包含:
- 全套 CSS 变量 + 暗夜模式
- PlantUML 渲染 / html2canvas 导出 / FAB 浮动按钮 / 阅读进度条
- PPT 单一来源派生逻辑 (改 flow → PPT 自动同步)
- ESC 键退出 / 翻页 / 各种交互

**生成新主题 HTML 时的标准流程**:
```
1. cp references/teaching-html-template.html → 目标文件
2. 改 <title>
3. 改 .hero (标题/副标题)
4. 在 #flow-view 里依次添加 .section (你想要几节就几节)
5. 完成 — PPT/夜间模式/导出/图表 全部自动可用
```

**绝对不需要做的事**:
- ❌ 不用手写 PPT slides (自动派生)
- ❌ 不用单独维护夜间色板 (CSS 变量已切换)
- ❌ 不用复制 JS 逻辑 (模板已带完整 JS)
- ❌ 不用从 deadlock 例子里删内容 (从空骨架开始更干净)

---

## 工作流（执行步骤）

### Step 1: 收集主题信息
- 主题名（中文 + 英文）
- 核心知识点列表（5-10 个）
- 哪些是易错点 / 重点
- 输出位置（默认 `explain/images/<topic>_knowledge_map.html`）

### Step 2: 规划内容结构
- 列出 6 个章节（编号 01-06）
- 每章列出 1-3 张 PPT 内容
- 标记重点/易错块

### Step 3: 生成完整 HTML
- 一次性 Write 整个文件
- 包含完整 CSS（不省略）
- 包含完整 JS（不省略）
- 流式视图 + PPT 视图都生成

### Step 4: 报告输出
告诉用户：
- 文件路径
- 双视图说明（流式默认 / PPT 按钮触发）
- PPT 键盘快捷键（Space/← →/ESC）

---

## 反例（不要做的事）

❌ 不要用 emoji 当主装饰（用等距字体编号）
❌ 不要用 border 区分卡片（用 box-shadow）
❌ 不要用线性渐变（除背景圆点外）
❌ 不要塞满文字（card 主标题 + 一行描述足矣）
❌ 不要简化 CSS（必须用上面完整模板）
❌ 不要省略 PPT 模式（双视图是核心特性）
❌ 不要把所有内容都重复说一遍（流式和 PPT 内容可以不一样，PPT 更精炼）

---

## 参考实例（必读 + 模仿）

**模板范例**（与 skill 一起打包）：
- `examples/deadlock_reference.html` —— **完整可运行参考**

**生成新 HTML 时的强制要求**：
1. **先读 `examples/deadlock_reference.html`** 学习其结构
2. **完整保留** CSS 变量定义、所有样式类、JS 逻辑
3. **只替换内容**（章节文字、卡片标题、PPT 内容）
4. **不要简化或修改**：
   - 网格点状背景
   - box-shadow 阴影系统
   - PPT 模式的所有控件和键盘逻辑
   - 模式切换按钮位置和样式

该范例展示了：
- 6 章节流式布局（定义 / 4 必要条件 / 3 策略 / 银行家算法 / RAG / 考点）
- 12 页 PPT 演示（标题页 → 重点引用 → 易错警示 → END）
- 重点引用 `.key-quote`、易错警示 `.pitfall`、记忆口诀 `.mnemonic` 的实际用法
- 完整的双视图切换实现（按钮触发 + ESC 退出 + 键盘导航）

**生成新主题 HTML 时的标准操作**：
```
1. Read examples/deadlock_reference.html
2. 用同样的结构, 替换:
   - <title> 标签
   - .hero 区的 h1 / sub
   - 6 个 section 的内容
   - PPT 部分的所有 slide 内容
3. 保持所有 CSS 和 JS 不变
4. Write 到目标路径
```
