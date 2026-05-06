# visual-ppt-deck-builder 效果测试报告

## 测试身份

我是效果测试执行者，不做代码审查，不修改 skill 源码。本轮只按已安装 skill 的工作流，从 0 生成一套可编辑 PPTX。

## 测试主题

普通人如何用 Codex 把一个想法变成可交付的视觉方案

## 实际执行流程

1. 读取 `/Users/dw/.agents/skills/visual-ppt-deck-builder/SKILL.md`。
2. 按强制流程依次产出：
   - 主题确认：`topic.md`
   - 大纲：`outline.md`
   - 5 套风格候选：`style-candidates.md`
   - 页面计划：`slide-plan.md`
   - 最终 deck spec：`deck-spec.json`
3. 使用优先路径调用 helper：
   - `/Users/dw/.agents/skills/visual-ppt-deck-builder/scripts/build_visual_pptx.js`
4. 生成：
   - `final.pptx`
5. 做基础验收：
   - helper 返回 `ok: true`
   - PPTX 压缩包内检查到 8 个 slide XML
   - macOS Quick Look 能为 PPTX 生成预览缩略图：`final.pptx.png`

## 最终产物

- `topic.md`
- `outline.md`
- `style-candidates.md`
- `slide-plan.md`
- `deck-spec.json`
- `final.pptx`
- `final.pptx.png`
- `style-board-business-calm.svg`
- `style-board-editorial.svg`
- `style-board-product-demo.svg`
- `style-board-data-report.svg`
- `style-board-visual-story.svg`
- `test-report.md`

## 哪里顺

- SKILL.md 的流程很清楚，适合作为执行清单：先主题、再大纲、再风格、再逐页计划，能防止一上来就直接做 PPT。
- helper 的输入输出简单，`deck-spec.json` 一旦符合 schema，生成 PPTX 很稳定。
- 生成后的 PPTX 是真实 `.pptx` 文件，不是截图集合；标题、正文、要点、对比卡片、时间线和条形图都由 PPT 形状或文本对象组成，后续可编辑。
- schema 文档和 helper 支持的 layout 对得上，执行时没有出现“文档说能做、脚本不支持”的硬断层。

## 哪里卡

- skill 要求“5 套候选图必须是图片形式”，但 helper 工作流本身并不负责生成或保存风格候选图。执行者需要另外调用生图能力，或像本轮这样额外生成 SVG 小样板。
- helper 的视觉能力偏基础：没有母版、没有图片裁切策略、没有复杂网格、没有真实图表组件、没有逐页自定义布局能力。它能稳定生成“可编辑简洁版”，但离高 polish 商业 deck 还有距离。
- `image_text` layout 依赖图片路径，但 skill 没有把“透明素材生成、清理、命名、引用进 spec”串成一个确定流程。实际执行时，如果没有另一个素材 skill 配合，很容易停在文字计划。
- 验收还比较粗：能检查页数和文件存在，但不能自动检查文字是否溢出、视觉是否好看、透明边缘是否干净。

## 最终效果自评

- 完整性：8/10。按流程从主题到 PPTX 都跑通了，必需产物齐全。
- 可编辑性：8/10。正文、要点、对比、时间线和条形图可编辑；没有把整页做成截图。
- 视觉表现：6/10。结构清楚，但更像“可用的流程演示 deck”，不是精修商业发布 deck。
- 流程体验：7/10。文本规划很顺，PPTX 生成很顺；卡点集中在风格候选图和高质量视觉素材衔接。

## 最大问题

这个 skill 的最大问题不是 helper 不能生成 PPTX，而是“前半段要求高视觉质量，后半段 helper 只提供基础可编辑布局”。也就是说，流程野心是完整视觉方案，但确定性工具链目前更像一个简洁 PPTX 组装器。要让它成为稳定可复用的视觉交付 skill，需要补上图片生成落盘、透明素材流水线、版式模板库和自动视觉验收。

