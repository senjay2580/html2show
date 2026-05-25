# ThariqS → teaching-html · Archetype × Atom 映射表

> Phase 1 产出：把 ThariqS/html-effectiveness 那 20 个范例页抽象成「页面骨架 (Archetype)」+「原子组件 (Atom)」两层目录，做为下一阶段重构 `skills/SKILL.md` 的设计依据。
>
> 风格基线：**Anthropic Clay** (clay `#D97757` / slate `#141413` / ivory `#FAF9F5` / oat `#E3DACC` / olive `#788C5D`) · 单栏 600-900px · serif H1 + sans 正文 + mono code · hairline 分割 · 无重边框无渐变

---

## 一 · 视觉 DNA（贯穿全 20 页）

| 维度 | 数值 |
|---|---|
| **正文宽度** | `max-width: 720-840px`, 单栏居中 |
| **字体三体** | serif (Georgia/ui-serif) for h1/h2 大字, sans (system-ui) for 正文, mono (SF Mono) for code/badge |
| **字号阶梯** | display 48px / h1 32px / h2 24px / body 16px / small 14px / caption 12px |
| **配色** | clay (强调) / slate (墨字) / ivory (底) / oat (柔分隔) / olive (成功/正向) / red-clay (危险/差异) |
| **节奏** | `--sp` 4/8/12/16/24/32/48/64px 八档；section 间 32-48px 留白 |
| **描边** | 仅 1px hairline (`var(--line) = #D1CFC5`)；无 box-shadow 重阴影；rounded `--r-md = 12px` 起 |

---

## 二 · 20 页聚类为 9 个 Archetype（页面骨架）

ThariqS 的 20 个 demo 里, 真正适合做 AI **文本输出范式** 的是前 17 个；最后 3 个（triage-board / feature-flags / prompt-tuner）是**交互编辑器**, 不是 AI 一次生成的"答案", 暂列为可选骨架。

| # | Archetype 名 | 对应 ThariqS 页 | 适用 AI 场景 (用户说...) |
|---|---|---|---|
| **A1** | **research-explainer** | 14, 15 | "解释 X / 这个概念怎么理解 / 给我搞懂 Y" |
| **A2** | **concept-comparison** | 01, 02 | "比较 A 和 B / 几种实现方式对比" |
| **A3** | **code-review** | 03, 04 | "审一下这个 PR / 这段代码什么意思" |
| **A4** | **pr-writeup** | 17 | "帮我写 PR 说明 / commit message 展开" |
| **A5** | **implementation-plan** | 16 | "规划一下怎么做 X / 列出 milestone" |
| **A6** | **status-report** | 11 | "周报 / 这周做了什么 / 项目进度" |
| **A7** | **incident-report** | 12 | "事故复盘 / postmortem / 故障分析" |
| **A8** | **flowchart-doc** | 10, 13 | "画一下流程 / 部署/请求路径可视化" |
| **A9** | **design-reference** | 05, 06 | "设计 token / 组件状态矩阵 / 设计系统" |
| (A10) | **knowledge-map** | (你已有) | 考研/教学知识图 (现有, 不动) |
| (A11) | **slide-deck** | 09 | PPT 模式 (现有, 不动) |
| (–) | triage-board | 18 | 交互编辑器, 暂不做 |
| (–) | feature-flag-editor | 19 | 交互编辑器, 暂不做 |
| (–) | prompt-tuner | 20 | 交互编辑器, 暂不做 |
| (–) | animation/interaction prototype | 07, 08 | 交互演示, 暂不做 |

**结论**：实际落地 9 个新 archetype，加你已有的 knowledge-map 共 10 个。slide-deck 当成 **跨 archetype 的视图模式**而非独立 archetype（任何 archetype 都能切 PPT 视图）。

---

## 三 · 原子组件清单（共 22 个）

按"用在哪几种 archetype 里"频次降序排列。**「来源」标"新"表示当前 teaching-html 没有，需要新建；标"现有"表示已在 [templates/teaching-html-template.html](../templates/teaching-html-template.html) 实现，复用即可；标"改名"表示概念相同但需对齐 ThariqS 命名/视觉。**

### 3.1 · 通用骨架原子 (所有 archetype 都用)

| Atom | 用途 | 现有等价 | 来源 |
|---|---|---|---|
| `hero` | 页面顶部：eyebrow + h1 + sub 副标 | `.hero` ✓ | 现有 |
| `section` | 章节容器 (h2 + 段落 + 内容) | `.section` + `.section-head` ✓ | 现有 |
| `sec-intro` | 章节开头一段散文铺垫 | `.sec-intro` ✓ | 现有 |
| `jump-nav` | 顶部锚点目录 (incident/long page 用) | `.toc` (侧栏) ✗ | **新**：横向跳转条 |
| `page-meta` | 标题旁的 metadata：作者 / 日期 / 状态 badge | (无) | **新** |
| `footer` | 页脚：来源 / 时间戳 / "auto-generated" | `.footer` ✓ | 现有 |

### 3.2 · 强调 / 引用原子

| Atom | 用途 | ThariqS 来源 | 现有等价 | 来源 |
|---|---|---|---|---|
| `tldr` | 全文一句话总结，紧贴 hero 下方 | 14, 12, 17 | `.tldr` ✓ | 现有 |
| `callout` | 黄/橙底提示框 (gotcha / note / warning) | 14, 04 | `.callout` ✓ | 现有 |
| `pull-quote` | 大字引用，断章作视觉锚 | (隐性) | `.key-quote` ✓ | 现有 |
| `pitfall` | 红色易错警示 | 14, 04 | `.pitfall` ✓ | 现有 |
| `rule-of-thumb` | 浅蓝底一句话铁律 (≈ 原 mnemonic) | (隐性) | `.mnemonic` ✓ | **改名**：`mnemonic` → `rule-of-thumb`（语义更通用） |

### 3.3 · 数据 / 状态原子

| Atom | 用途 | ThariqS 来源 | 现有 | 来源 |
|---|---|---|---|---|
| `badge` | 状态标签：SEV-2 / Resolved / Blocking / Nit | 03, 12, 11 | (无) | **新** |
| `metric-card` | KPI 大数字 + 标签 (14 PRs / 47min / 1 SEV-2) | 11, 12 | (无) | **新** |
| `metric-delta` | 数字 + 上下箭头 ± 变化 (p95: 180ms ↓) | 11, 17 | (无) | **新** |
| `kv-row` | 紧凑的 key + value 横排 (label: value) | 12, 04 | `.ds-row` ✓ | 现有 → 复用 |

### 3.4 · 列表 / 步骤 / 表格原子

| Atom | 用途 | ThariqS 来源 | 现有 | 来源 |
|---|---|---|---|---|
| `step-list` | 编号步骤列表 (01 → 02 → 03) | 04, 16, 13 | `.step` ✓ | 现有 |
| `timeline` | 时间戳 + 事件 (post-mortem / rollout) | 12, 17 | (无) | **新** |
| `risk-row` | 风险描述 + 严重度 + 缓解 | 16, 03 | `.compare-row` 近似 | **新**（基于 compare-row 派生） |
| `comparison-table` | 横向特性矩阵 (Mod N vs Consistent Hash) | 15, 01 | `.rag-grid` 近似 | 现有改造 |
| `qa-pair` | 问题 + 简答 (FAQ 区) | 14, 04 | (无) | **新** |
| `decision-block` | 标题 + 问题 + Option A/B + 推荐 | 11, 16 | (无) | **新** |
| `action-items` | 待办：owner + task + due-date 三列表 | 12, 16 | (无) | **新** |

### 3.5 · 代码 / 文件原子

| Atom | 用途 | ThariqS 来源 | 现有 | 来源 |
|---|---|---|---|---|
| `code-block` | 单语言代码块 (with optional filename) | 14, 17, 04 | (无完整封装) | **新**：标准 `<pre>` + filename header |
| `code-triple` | 三栏并列代码 (yaml + ts + http) | 14 | (无) | **新**：基于 grid-3 派生 |
| `file-ref` | `path/to/file.ts:42` 可跳转 | 04, 03, 17 | (无) | **新**：行内 mono badge |
| `diff-block` | +/- 变化代码块 | 03, 17 | (无) | **新** |

### 3.6 · 视觉原子（图）

| Atom | 用途 | ThariqS 来源 | 现有 | 来源 |
|---|---|---|---|---|
| `flowchart-svg` | 内联 SVG 流程图 (无外部依赖) | 13, 10, 04 | `.diagram-card` (PlantUML) ✓ | **新增 SVG 版**，与 PlantUML 版并存 |
| `token-swatch` | 色票 / spacing / radius 示例格 | 05 | (无) | **新** |
| `variant-grid` | 同组件多变体并列 (4-6 格) | 06, 02 | `.cond-grid` 近似 | 现有改造 |

---

## 四 · 现有 teaching-html 组件的处置

| 现有 class | 处置 | 理由 |
|---|---|---|
| `.card` / `.card-label/h/body/meta` | **保留** | 通用积木, 任何 archetype 都用 |
| `.section / .section-head / .section-num / .section-title` | **保留** | 通用 |
| `.hero / .eyebrow / h1 / .sub` | **保留** | 通用 |
| `.sec-intro / .tldr / .callout` | **保留** (ThariqS 风已对齐) | 已是 Clay 风 |
| `.key-quote / .pitfall` | **保留** | 通用强调 |
| `.mnemonic` | **改名 `.rule-of-thumb`** | 教学专属词太窄, 通用化 |
| `.cond-grid` (4 列必要条件) | **保留 + 通用化为 `.variant-grid`** | 实质是 ThariqS variant-grid |
| `.strat-grid` (3 列策略) | **保留** (教学专用, 不强行通用) | knowledge-map archetype 用 |
| `.exam-grid` (5 列考点) | **保留** (教学专用) | knowledge-map archetype 用 |
| `.algo-grid / .step / .ds-row` | **保留** | step-list / kv-row 的实现 |
| `.rag-grid / .compare-row / .info-line / .conclusion` | **改造为 `.comparison-table`** | 等价语义, 命名靠拢 ThariqS |
| `.diagram-card` (PlantUML 容器) | **保留** + **新增 inline-svg 兄弟版** | PlantUML 有网络依赖, 复杂图想要稳定可用 SVG |
| `.def-stack` | **保留** (容器壳, 任意 archetype 都用) | 单 section 内堆叠多 card 的标准容器 |

---

## 五 · Phase 2 实施清单（待你确认后开工）

### 5.1 文件落点

```
html2show/
├── components/                         ← 已存在的空目录, 现在填充
│   ├── _atoms/                         ★ 22 个原子, 每个一个 .html 片段
│   │   ├── hero.html
│   │   ├── section.html
│   │   ├── sec-intro.html
│   │   ├── jump-nav.html               (新)
│   │   ├── page-meta.html              (新)
│   │   ├── footer.html
│   │   ├── tldr.html
│   │   ├── callout.html
│   │   ├── pull-quote.html
│   │   ├── pitfall.html
│   │   ├── rule-of-thumb.html          (改名)
│   │   ├── badge.html                  (新)
│   │   ├── metric-card.html            (新)
│   │   ├── metric-delta.html           (新)
│   │   ├── kv-row.html
│   │   ├── step-list.html
│   │   ├── timeline.html               (新)
│   │   ├── risk-row.html               (新)
│   │   ├── comparison-table.html       (改造)
│   │   ├── qa-pair.html                (新)
│   │   ├── decision-block.html         (新)
│   │   ├── action-items.html           (新)
│   │   ├── code-block.html             (新)
│   │   ├── code-triple.html            (新)
│   │   ├── file-ref.html               (新)
│   │   ├── diff-block.html             (新)
│   │   ├── flowchart-svg.html          (新, SVG 版)
│   │   ├── token-swatch.html           (新)
│   │   └── variant-grid.html           (改造)
│   ├── INDEX.md                        ★ 22 行原子目录, 给 SKILL.md 链接
│   └── (旧的 cards/quotes/grids/.gitkeep 删掉)
│
├── templates/                          ← 新增 9 个 archetype 骨架
│   ├── archetype-research-explainer.html       (A1, 适合"解释 X")
│   ├── archetype-concept-comparison.html       (A2, "对比方案")
│   ├── archetype-code-review.html              (A3)
│   ├── archetype-pr-writeup.html               (A4)
│   ├── archetype-implementation-plan.html      (A5)
│   ├── archetype-status-report.html            (A6)
│   ├── archetype-incident-report.html          (A7)
│   ├── archetype-flowchart-doc.html            (A8)
│   ├── archetype-design-reference.html         (A9)
│   ├── teaching-html-template.html             ← 改名 archetype-knowledge-map.html
│   └── ARCHETYPES.md                   ★ 10 个骨架目录, 给 SKILL.md 链接
│
├── styles/atoms.css                    ★ 22 个原子的 CSS 抽到单文件 (各 archetype @import)
│
└── docs/
    ├── archetype-atom-mapping.md       ← 本文件
    └── lessons.md                      ← 4 段坑位历史迁出 SKILL.md
```

### 5.2 工作量估算

| 阶段 | 内容 | 时间 |
|---|---|---|
| 2.1 | 写 `styles/atoms.css` (22 个 atom 的样式, 沿用现有模板里已有的, 新增 ~10 个) | 60min |
| 2.2 | 抽出 22 个 `components/_atoms/*.html` 片段 (含注释/示例) | 60min |
| 2.3 | 写 9 个 `templates/archetype-*.html` 骨架 (复用 atoms.css, 主要是 body 结构) | 90min |
| 2.4 | 写 `components/INDEX.md` 和 `templates/ARCHETYPES.md` 两个目录文件 | 30min |
| 3.1 | 重写 SKILL.md (从 1449 → ~500 行) | 60min |
| 3.2 | 把 4 段坑位历史迁到 `docs/lessons.md` | 15min |
| **总计** | | **~5.5 小时** |

### 5.3 SKILL.md 新结构（重写后）

```
1. 一句话使命 + 何时触发
2. 判定流程：用户输入 → 选 archetype (含示例对照)
3. archetype 目录 (10 行, 链接到 templates/)
4. atom 目录 (22 行, 链接到 components/_atoms/)
5. 组合规则 (哪些 atom 该套在哪些 archetype 里)
6. 风格系统 (Anthropic Clay 8 色 + 字体三体)
7. PPT 模式 / html2canvas 导出 / PlantUML (全保留, 你要求的)
8. 反例 (10 行短清单)
9. 检查清单 (10 项)
```

---

## 六 · 还要你拍板 2 个点

1. **`components/cards/` `quotes/` `grids/` `fab/` `navigation/` `toc/` 这 6 个旧空目录**：直接删, 改用扁平 `components/_atoms/`？还是保留旧分类继续往里塞？
   - 我建议扁平：22 个 atom 一层目录, INDEX.md 来做分类, 比目录树更好检索

2. **PPT 模式作为跨 archetype 的视图**：所有 archetype 是不是都自动支持"按按钮进 PPT 模式"？还是只 knowledge-map / status-report / research 这种"讲解型"的支持，code-review / incident-report 这种"参考型"不要 PPT？
   - 我建议：只在 archetype 模板里有 `<button id="ppt-btn">` 的才支持，骨架里不带就关闭。这样不必每个都套全套 JS

回完这 2 个 → 我开 Phase 2。
