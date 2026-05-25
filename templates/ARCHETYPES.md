# Archetypes Index · 页面骨架目录

> 10 个 archetype 骨架, 每个对应一种 AI 输出场景。每个骨架是一个**可直接打开看**的 HTML 文件, 内置占位内容 + 注释槽位。
>
> **生成新主题的标准流程**:
> 1. 用户问题 → 用下表判定 archetype
> 2. `cp templates/archetype-X.html pages/<topic>.html`
> 3. 改 `<title>` + Hero + 章节内容, 从 [`components/_atoms/`](../components/_atoms/) 复制原子粘进去
> 4. 浏览器打开测试 → push → GitHub Pages 自动部署

---

## 判定题型: 用户说... → 选哪个 archetype

| 用户输入特征 | Archetype | 模板文件 |
|---|---|---|
| "解释 X 是什么 / 给我搞懂 Y" · "这个功能怎么工作的" | **A1 research-explainer** | [archetype-research-explainer.html](archetype-research-explainer.html) |
| "比较 A 和 B" · "几种方式哪种好" · "Approach 1/2/3" | **A2 concept-comparison** | [archetype-concept-comparison.html](archetype-concept-comparison.html) |
| "审一下这个 PR" · "review 一下" · "看这段代码" | **A3 code-review** | [archetype-code-review.html](archetype-code-review.html) |
| "写个 PR description" · "说明这个改动" | **A4 pr-writeup** | [archetype-pr-writeup.html](archetype-pr-writeup.html) |
| "规划一下 X" · "list milestones" · "implementation plan" | **A5 implementation-plan** | [archetype-implementation-plan.html](archetype-implementation-plan.html) |
| "周报 / 这周做了什么 / status update" | **A6 status-report** | [archetype-status-report.html](archetype-status-report.html) |
| "事故复盘 / postmortem / 故障分析" | **A7 incident-report** | [archetype-incident-report.html](archetype-incident-report.html) |
| "画一下流程 / 部署管线 / 请求路径" | **A8 flowchart-doc** | [archetype-flowchart-doc.html](archetype-flowchart-doc.html) |
| "设计 token / 色板 / 字体规范" | **A9 design-reference** | [archetype-design-reference.html](archetype-design-reference.html) |
| **"考研知识点 / 408 总结 / 教学讲义"** | **A10 knowledge-map** (你已有) | [archetype-knowledge-map.html](archetype-knowledge-map.html) |

---

## Archetype 详情

### A1 · research-explainer
**用途**: 系统性讲解一个概念/特性 — 给同事/读者搞懂"这是什么、怎么用、容易踩什么坑"。
**结构**: hero · tldr · jump-nav.side · sec-intro · details (step by step) · code-triple (yaml/ts/http) · callout · pitfall · faq
**布局**: 双栏 (200px 侧栏 + 主内容), &lt;920px 自动单栏。
**示例**: ThariqS 14-research-feature-explainer.html 风。

### A2 · concept-comparison
**用途**: 多方案对比 — 用户在选型/方案评估阶段。
**结构**: hero · variant-grid (横向 3 个候选) · comparison-table (硬指标) · decision-block · pull-quote
**布局**: 单栏 820px。
**示例**: ThariqS 01-exploration-code-approaches.html。

### A3 · code-review
**用途**: 给 PR 写可执行的反馈 — 包含风险地图 + 文件分级 + diff 标注。
**结构**: hero · page-meta (作者/+/-) · variant-grid (risk map safe/worth-a-look/needs-attention) · diff-block · callout.warn (blocking comments) · action-items
**布局**: 单栏 820px。
**示例**: ThariqS 03-code-review-pr.html。

### A4 · pr-writeup
**用途**: 写 PR description — 给 reviewer 5 分钟读完知道改什么/为什么/怎么验。
**结构**: hero · page-meta · tldr · why · file-by-file (code-block / diff-block) · focus-areas · rollout (timeline) · test-plan (qa-pair)
**布局**: 单栏 820px。
**示例**: ThariqS 17-pr-writeup.html。

### A5 · implementation-plan
**用途**: 4 周左右的工程实施计划 — 给团队对齐路径 + 风险 + 待办。
**结构**: hero · tldr · milestones (variant-grid 按周) · flowchart-svg (数据流) · risks (risk-row × N) · decision-block (open question) · action-items
**布局**: 单栏 820px。
**示例**: ThariqS 16-implementation-plan.html。

### A6 · status-report
**用途**: 周报/月报 — 给上级或团队的进度更新。
**结构**: hero · summary-band (metric-card × 4 KPI) · shipped (variant-grid) · in-progress (列表) · metrics (kv-row) · decision-needed · next-week · footer
**布局**: 单栏 860px。
**示例**: ThariqS 11-status-report.html。

### A7 · incident-report
**用途**: 故障复盘 — SEV 等级 + 时间线 + 根因 + 影响 + 待办。
**结构**: hero · page-meta (sev pill) · jump-nav.jump (横向) · tldr.inverse (深色) · timeline · root-cause (code-block 配置) · pull-quote (insight) · impact (kv-row) · action-items
**布局**: 单栏 820px。
**示例**: ThariqS 12-incident-report.html。

### A8 · flowchart-doc
**用途**: 流程文档 — 一张大图主导 + 每步可展开细节。
**结构**: hero · flowchart-svg (大图) · details × N (每步) · callout (rollback 条件等)
**布局**: 单栏 820px。
**示例**: ThariqS 13-flowchart-diagram.html。

### A9 · design-reference
**用途**: 设计系统 token reference — 给自己/同事看色板/字号/spacing。
**结构**: hero · token-swatch (色板) · comparison-table (typography 尺度) · 各 atom 预览
**布局**: 宽 1100px (展示用)。
**示例**: ThariqS 05-design-system.html。

### A10 · knowledge-map (已有, 教学专用)
**用途**: 考研 / 408 / 课程知识图谱 — 教学风, 自带 PPT 视图。
**结构**: hero · 6 sections (定义 / 必要条件 / 策略 / 算法 / 辨析 / 考点) · .cond-grid / .strat-grid / .exam-grid · key-quote · pitfall · mnemonic / rule-of-thumb · PPT mode
**布局**: 单栏 1080px。
**注意**: 这是 ThariqS 风格之外的教学风变体 — 保留 .cond-grid (4 必要条件) / .strat-grid (3 策略) / .exam-grid (5 考点) 这些"教学专用"的组件。配 PPT 视图 + html2canvas 导出 + PlantUML 图表。

---

## 跨 archetype 共用

| 能力 | 哪些 archetype 用 | 实现位置 |
|---|---|---|
| **PPT 视图** (按钮触发, 单一来源派生) | A10 knowledge-map (自带) | knowledge-map 内嵌 JS |
| **html2canvas 导出 PNG** | A10 knowledge-map (自带) | knowledge-map 内嵌 JS |
| **PlantUML 渲染** | A10 knowledge-map (自带) · A1/A8 可选 | knowledge-map 内嵌 JS |
| **暗夜模式 toggle** | 所有 archetype (atoms.css 自带 body.dark) | atoms.css |
| **响应式** | 所有 archetype | atoms.css |
| **侧栏锚点 + 滚动高亮** | A1 research / 长文档 | atoms.css + 可选 IntersectionObserver |

**判断标准**: A10 是"讲解型 + 可演示", 配 PPT/export/PlantUML 三件套; 其他 archetype 是"参考型", 不需要 PPT (扫读用, 不是演讲用)。

---

## 一致性约束

1. 所有 archetype 都 `<link rel="stylesheet" href="../styles/atoms.css">` (相对路径假设放在 `pages/`)
2. 顶部 `<link rel="icon" type="image/png" href="https://github.com/senjay2580.png?size=64">` GitHub 动态头像
3. body `<div class="page">` 包裹 (默认 820px, 宽版 `.page.wide` 1100px, 双栏 `.page.two-col`)
4. 用 `<section id="xxx">` 让 jump-nav 能锚定
5. 任何 atom 都从 [`components/INDEX.md`](../components/INDEX.md) 取, 不要现造
6. 缺组件 → 先在 atoms.css 加 → 在 INDEX.md 登记 → 再到 archetype 里用
