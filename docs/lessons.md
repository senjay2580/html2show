# 实战教训档案 · Lessons Learned

> 从原 [skills/SKILL.md](../skills/SKILL.md) 迁出的"踩过的坑"。这里只保留**仍然可能再发生**的, 已经在 [styles/atoms.css](../styles/atoms.css) 或 [templates/](../templates/) 里固化的写法不再赘述。
>
> 整理时间: 2026-05-13

---

## 坑 1 · 章节 div 嵌套错位 → PPT 只生成几张幻灯片

**症状**: 写完 7 节, PPT 模式只显示 4 张幻灯片; TOC 也对不上。

**根因**: 某个 `.section` 内部漏关 `</div>` (常见: card 套 def-stack 套 key-quote 时少一层关闭), 导致后续 section 被嵌套进前一个 section, `querySelectorAll('#flow-view .section')` 仍能找到, 但 `buildSlidesFromFlow` 处理时出错。

**预防**:
- 每改完一个 section 立刻数 div 平衡:
  ```bash
  awk '/<div /{n++}/<\/div>/{c++}END{print n,c}' file.html
  ```
  开闭差应为 0。
- **每个 section 内只用一个主容器** (.def-stack / .algo-grid / .rag-grid 等), key-quote/pitfall/mnemonic 作为容器的兄弟节点。
- 不要在 .def-stack 内部嵌 .key-quote — 它应是 section 的直接子, 不是 grid 的子。
- 写多个并列 card 时**必须**包在 .def-stack 里, 别游离。

**只影响**: A10 knowledge-map (有 PPT 派生逻辑的 archetype)。A1-A9 不走 PPT 派生, 不受影响。

---

## 坑 2 · PlantUML 状态图语法错误

**症状**: 渲染出来是源码 + "Syntax Error? (Assumed diagram type: state)" 红字。

**踩过的写法**:
```plantuml
state q0 as "q0"          ❌ 别名顺序反了
[*] -right-> q0           ❌ 状态图不支持带方向的虚线 .down.>
q4 .down.> q2 : 失配      ❌ 同上
skinparam state {
  StartColor #0071e3      ❌ state 块里没这个 key, 引发解析失败
  EndColor #16a34a        ❌ 同上
}
```

**正确写法**:
```plantuml
state "q0" as q0          ✅ 标签在前, 别名在后
state "q1 : A" as q1
[*] --> q0                ✅ 起始用 [*], 实线用 -->
q4 ..> q2 : 失配 next=2   ✅ 虚线只能用 ..>, 不能加方向
skinparam state {
  BackgroundColor #FFFFFF
  BorderColor #0071e3
  FontColor #0071e3       ✅ 只用通用 key
}
```

**或干脆**: 状态图/有向图用**内联 SVG** 替代 PlantUML, 更可控、无网络依赖、好调样式。

**新建议**: A8 flowchart-doc archetype 直接用 [_atoms/flowchart-svg.html](../components/_atoms/flowchart-svg.html), 不再走 PlantUML。PlantUML 仅 A10 knowledge-map 历史兼容保留。

---

## 坑 3 · 标准章节是 6 节, 但算法主题需要更多

**症状**: 强行塞进 6 节, 银行家/KMP 这种重头戏没空间展开 trace。

**预防**: 算法主题至少 7 节, 多出来的一节专门做 step-by-step walkthrough (用连续的 .step 元素列出每一步)。

**新建议**: 现在有了 9 个 archetype + 30 个 atom, 不再有"6 节标准"。**章节切分由内容决定** — KMP 需要"完整 trace" 就用 step-list × 7; deadlock 需要"4 必要条件" 就用 variant-grid × 4。

---

## 坑 4 · 游离 .card 与 grid 混用导致间距不齐

**症状**: 同一 section 里, 上方是 standalone `<div class="card">`, 下方是 `<div class="rag-grid">`, 视觉上间距不匀。

**根因**: `.card` 自身没 margin, grid 也没 margin, 它们之间靠手动 inline `style="margin-bottom:24px"` 凑, 与其他 section 的 `gap:20px` 节奏不一致。

**预防**:
- 同一 section 内多个 card 一律用 `.def-stack` 包 (gap:20px, 与所有其他 grid 一致)。
- 不要写 `<div class="card" style="margin-bottom:Xpx">` 手动堆叠。

**只影响**: A10 knowledge-map (有 .def-stack 概念的 archetype)。其他 archetype 用 atoms.css 标准 atom, section 间距已统一。

---

## 坑 5 · Apple 蓝 → Clay 配色迁移留下的旧 CSS 变量

**症状**: 旧主题 HTML 里 `--blue: #0071e3` 残留, 与新主题 `--clay: #D97757` 不一致, 双视图切换时颜色错乱。

**预防**:
- 所有新建主题**只引** `<link rel="stylesheet" href="../styles/atoms.css">`, 不再内联 :root token 块。
- 现有 408 知识图 (deadlock / kmp) 已有 Clay 风内联 CSS, 保持不动 — 兼容。
- 改全局 token 只改 [`styles/atoms.css`](../styles/atoms.css) 一处。

---

## 通用规则 (从坑里提炼)

1. **每个 section 内只用一个主容器** — 多个并列卡片要么进 grid (cond/strat/variant), 要么进 .def-stack。
2. **div 平衡检查** — 大改完一定数: `awk '/<div /{n++}/<\/div>/{c++}END{print n,c}'`
3. **PlantUML 有网络依赖** — 流程图、状态图优先用 [_atoms/flowchart-svg.html](../components/_atoms/flowchart-svg.html) inline SVG, 离线可用。
4. **章节数为内容服务**, 不强行凑 N 节; 一个 archetype 模板里的占位 sections 是 hint, 不是 hard 约束。
5. **token 集中** — 全局色变量只在 [`styles/atoms.css`](../styles/atoms.css) 维护。

---

## 何时回来读这个文件

- 写新 archetype 模板, 不知道为什么旧模板某处那样写 → 这里有答案。
- PPT 视图坏了, 看坑 1。
- PlantUML 不渲染, 看坑 2 (或干脆换 SVG)。
- section 间距不齐, 看坑 4。
- 改全局颜色, 看坑 5。
