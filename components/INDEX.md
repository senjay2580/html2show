# Atoms Index · 原子组件目录

> 30 个原子组件, 全部基于 Anthropic Clay (ThariqS/html-effectiveness 风) 配色。
> CSS 在 [`styles/atoms.css`](../styles/atoms.css)，每个原子的 HTML 片段在 `_atoms/` 下同名文件。
>
> **用法**: 在 archetype 模板里 `<link rel="stylesheet" href="../styles/atoms.css">`，然后从下表挑原子复制 HTML 片段过去。

---

## 一 · 通用骨架（每页都用）

| Atom | 用途 | 文件 |
|---|---|---|
| `hero` | 页面顶部 eyebrow + h1 + sub | [_atoms/hero.html](_atoms/hero.html) |
| `section` | 章节容器 h2 + hr + 内容 | [_atoms/section.html](_atoms/section.html) |
| `sec-intro` | 章节标题下的散文段铺垫 | [_atoms/sec-intro.html](_atoms/sec-intro.html) |
| `jump-nav` | 锚点目录 (侧栏 `.side` / 横向 `.jump`) | [_atoms/jump-nav.html](_atoms/jump-nav.html) |
| `page-meta` | 作者/日期/状态 pill 元信息行 | [_atoms/page-meta.html](_atoms/page-meta.html) |
| `footer` | 页脚 mono 时间戳 | [_atoms/footer.html](_atoms/footer.html) |

## 二 · 强调 / 引用 / 警示

| Atom | 用途 | 颜色基调 | 文件 |
|---|---|---|---|
| `tldr` | 全文一句话总结 (.inverse = 深色变体) | clay/slate | [_atoms/tldr.html](_atoms/tldr.html) |
| `callout` | 提示框 (默认/warn/success 三档) | oat/rust/olive | [_atoms/callout.html](_atoms/callout.html) |
| `pull-quote` | 深色大字引用, 章节锚 | slate + clay em | [_atoms/pull-quote.html](_atoms/pull-quote.html) |
| `pitfall` | 红色易错警示 (✗ 错 / ✓ 对) | rust | [_atoms/pitfall.html](_atoms/pitfall.html) |
| `rule-of-thumb` | 一句话铁律 / 记忆口诀 | clay 左 stripe | [_atoms/rule-of-thumb.html](_atoms/rule-of-thumb.html) |

## 三 · 状态 / 数据

| Atom | 用途 | 文件 |
|---|---|---|
| `badge` (pill) | 状态/分类标签 (SEV-2/Resolved/safe/tag) | [_atoms/badge.html](_atoms/badge.html) |
| `metric-card` | KPI 大数字 (用 `.summary-band` 容器做 4 列) | [_atoms/metric-card.html](_atoms/metric-card.html) |
| `metric-delta` | 数字配 ▲▼— 三档变化 | [_atoms/metric-delta.html](_atoms/metric-delta.html) |
| `kv-row` | key-value 横排单行 (堆叠时 hairline 分割) | [_atoms/kv-row.html](_atoms/kv-row.html) |

## 四 · 列表 / 步骤 / 表格

| Atom | 用途 | 文件 |
|---|---|---|
| `step-list` | 编号步骤 01→02→03 (算法 / 流程) | [_atoms/step-list.html](_atoms/step-list.html) |
| `timeline` | 时间戳 + 事件 (postmortem / rollout) | [_atoms/timeline.html](_atoms/timeline.html) |
| `risk-row` | 风险 + 严重度 + 缓解 (high/med/low) | [_atoms/risk-row.html](_atoms/risk-row.html) |
| `comparison-table` | 横向特性矩阵 (n 列对比) | [_atoms/comparison-table.html](_atoms/comparison-table.html) |
| `qa-pair` | FAQ / dl/dt/dd 语义化 Q&A | [_atoms/qa-pair.html](_atoms/qa-pair.html) |
| `decision-block` | 决策点: 问题 + 选项 + 推荐 | [_atoms/decision-block.html](_atoms/decision-block.html) |
| `action-items` | 待办: owner + task + due-date 三列表 | [_atoms/action-items.html](_atoms/action-items.html) |
| `details` | 原生 `<details>/<summary>` 可折叠章节 | [_atoms/details.html](_atoms/details.html) |

## 五 · 代码 / 文件

| Atom | 用途 | 文件 |
|---|---|---|
| `code-block` | 单语言代码块 + 可选 filename header | [_atoms/code-block.html](_atoms/code-block.html) |
| `code-triple` | 三栏并列 tab 切换代码 (yaml/ts/http) | [_atoms/code-triple.html](_atoms/code-triple.html) |
| `diff-block` | +/- 变化代码 (olive 增 / rust 删) | [_atoms/diff-block.html](_atoms/diff-block.html) |
| `file-ref` | 行内 mono badge: `path/file.ts:42` | [_atoms/file-ref.html](_atoms/file-ref.html) |

## 六 · 视觉 / 图

| Atom | 用途 | 文件 |
|---|---|---|
| `flowchart-svg` | 内联 SVG 流程图 (无网络依赖) | [_atoms/flowchart-svg.html](_atoms/flowchart-svg.html) |
| `token-swatch` | 色票 / spacing / radius 示例格 | [_atoms/token-swatch.html](_atoms/token-swatch.html) |
| `variant-grid` | 同概念多变体并列 (4-6 格) | [_atoms/variant-grid.html](_atoms/variant-grid.html) |

---

## 组合规则（哪些 atom 应该套在哪个 archetype 里）

| Archetype | 主要 atom |
|---|---|
| **research-explainer** | hero + jump-nav.side + tldr + details + code-triple + callout + qa-pair |
| **concept-comparison** | hero + variant-grid + comparison-table + decision-block + pull-quote |
| **code-review** | hero + page-meta + badge + variant-grid (risk map) + diff-block + file-ref |
| **pr-writeup** | hero + page-meta + tldr + diff-block + timeline (rollout) + qa-pair |
| **implementation-plan** | hero + tldr + variant-grid (milestones) + risk-row + flowchart-svg + decision-block + action-items |
| **status-report** | hero + summary-band (metric-card×4) + variant-grid (shipped) + decision-block + footer |
| **incident-report** | hero + page-meta (sev pills) + tldr.inverse + jump-nav + timeline + pull-quote + action-items |
| **flowchart-doc** | hero + flowchart-svg + details (each step) + callout |
| **design-reference** | hero + token-swatch + variant-grid + comparison-table |
| **knowledge-map** (你已有) | 保留原 `.cond-grid` `.strat-grid` `.exam-grid` (教学专用) + 新 atoms |

---

## 一致性约束

1. 所有 atom 都基于 `--clay/--slate/--ivory/--oat/--olive/--rust` 6 色 + gray 阶梯
2. 边框统一 `1.5px var(--gray-300)`, 圆角统一 `12px` (panel) / `8px` (row) / `6px` (small)
3. 字号阶梯 fixed: h1=36, h2=24, h3=18, body=15, small=14, caption=12, mono-label=11
4. 字体三体: serif 用于 h1/h2/大数字 · sans 用于正文 · mono 用于 label/code/badge
5. **不要新发明 class**, 缺组件就回到模板基础块自由组合; 真的有需求时先加进 [`styles/atoms.css`](../styles/atoms.css)
