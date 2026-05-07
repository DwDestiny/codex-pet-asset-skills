# PPT 风格候选真实样板包

主题：2026 AI 应用趋势调研

硬规则：每个候选必须先生成真实 PPTX 样板，再从 PPTX 导出 PNG 预览。PNG 预览只用于选择风格；真正可复用的是 PPTX 样板、背景素材、透明素材和分层契约。标题、正文、指标、图表标签必须文本可编辑，不允许把正式页面整页生图后交给用户选。视觉上必须是融合式版面，禁止大白框贴背景。

使用方式：

1. 先查看 `samples/style-sample-*.pptx`，确认文字、指标和图表标签能在 PowerPoint 中直接编辑。
2. 再查看 `previews/style-sample-*.png`，让用户从 8 张单独预览里选择风格。
3. 如需提高画面质感，先按 `prompts/style-reference-*.md` 生成完整效果图母稿，验收后再按 `prompts/clean-background-*.md` 生成无文字 clean background，保存到 `assets/background-*.png` 后重新运行本工具。
4. 被选中的方向进入逐页 PPT 生产，沿用同一套 PPT 分层结构，而不是重新临摹一张整页图片。

## 简约高级

- PPTX 样板：`samples/style-sample-minimal-premium.pptx`
- PNG 预览：`previews/style-sample-minimal-premium.png`
- 效果图母稿提示词：`prompts/style-reference-minimal-premium.md`
- clean background 提示词：`prompts/clean-background-minimal-premium.md`
- 背景素材：`assets/background-minimal-premium.png`
- 适合场景：商业计划书、融资路演、咨询汇报
- 视觉方向：大量留白、黑白灰秩序、真实建筑线条和克制的商业咨询气质，适合严肃决策场景。
- 透明素材：黑白线框图标组、半透明建筑结构装饰、咨询卡片角标
- 可编辑层：封面主标题、英文副标题、章节标题、数据标签、图表坐标和注释
- 样本标题：2026 AI 应用趋势调研
- 样本正文：AI 应用正在从工具采购转向流程重构，真正的价值来自业务场景、数据闭环和组织协同。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：克制咨询风，标题粗黑、字距正常、信息层级少而准。 正文使用中灰小号文本，行宽短，配细线和留白。
- 图表语言：极细坐标基线、黑灰柱体和单色强调，像咨询报告里的开放式图表。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:黑白线框图标组、transparent_asset_layer:半透明建筑结构装饰、transparent_asset_layer:咨询卡片角标、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧或中左侧保留低纹理浅色留白，使用深色主标题和中灰正文；人物、建筑、山水等高细节素材避开正文行高区域。
- 图表安全区：右侧图表落在浅色留白或纸纹过渡区，使用深色/品牌强调色线条，避免柱体或折线压到复杂纹理。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.72, y=0.72, w=5.9, h=1.15；主标题和副标题，保持建筑线条低对比。；主标题 1 行，副标题 1 行。
- text_zone：x=0.82, y=2.3, w=4.95, h=2.2；正文和三条要点，浅色低纹理留白。；正文 55 个中文字符以内，3 条短要点。
- chart_zone：x=7.05, y=1.5, w=4.8, h=4.75；开放式柱状图或折线图，背景仅保留细线透视。；4 组柱状图，坐标标签 4 个。
- metrics_zone：x=0.82, y=5.42, w=5.5, h=0.95；三组开放式指标，不加描边框。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=8.55, y=0, w=4.5, h=7.5；建筑玻璃、空间透视和低对比装饰主视觉。；不能承载文字。
- protected_empty_zone：x=5.9, y=0.5, w=1, h=6.4；内容区和图表区之间的呼吸带。；保持干净，不放正文或复杂纹理。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## 活泼动漫

- PPTX 样板：`samples/style-sample-playful-anime.pptx`
- PNG 预览：`previews/style-sample-playful-anime.png`
- 效果图母稿提示词：`prompts/style-reference-playful-anime.md`
- clean background 提示词：`prompts/clean-background-playful-anime.md`
- 背景素材：`assets/background-playful-anime.png`
- 适合场景：教育课程、儿童产品、社群活动
- 视觉方向：明亮色彩、圆润结构、可爱角色和轻松课堂氛围，适合学习、活动和年轻用户表达。
- 透明素材：可爱学生角色、课程徽章贴纸、星星和学习道具装饰
- 可编辑层：课程标题、目标卡片文字、按钮标签、步骤编号、图表解释文字
- 样本标题：2026 AI 应用趋势调研
- 样本正文：用轻量案例解释 AI 应用趋势，让非技术团队也能判断哪些场景值得优先试点。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：课程型圆润标题，字号略大，颜色更轻快。 正文短句化，配彩色圆点和更大的呼吸间距。
- 图表语言：彩色学习进度柱和圆点标签，图表更轻松，但仍保持可编辑形状。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:可爱学生角色、transparent_asset_layer:课程徽章贴纸、transparent_asset_layer:星星和学习道具装饰、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧或中左侧保留低纹理浅色留白，使用深色主标题和中灰正文；人物、建筑、山水等高细节素材避开正文行高区域。
- 图表安全区：右侧图表落在浅色留白或纸纹过渡区，使用深色/品牌强调色线条，避免柱体或折线压到复杂纹理。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.72, y=0.72, w=5.4, h=1.05；课程标题和轻量副标题，避开角色脸部。；主标题 1 行，副标题 1 行。
- text_zone：x=3, y=2.25, w=4.1, h=2.3；学习目标正文，浅色云朵或黑板低纹理区域。；正文 45 个中文字符以内，3 条短要点。
- chart_zone：x=7.25, y=1.85, w=4.65, h=4.35；彩色开放式图表，背景使用浅色课堂留白。；4 组柱状图，标签用深灰。
- metrics_zone：x=2.9, y=5.45, w=5.55, h=0.95；三组彩色指标，像贴纸但不画外框。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=0, y=3, w=3, h=4.5；卡通角色和学习道具主视觉。；角色不遮挡文字区。
- protected_empty_zone：x=3, y=2, w=4.2, h=3.2；正文阅读区，背景只能是低噪声浅色过渡。；保持干净，不放高饱和装饰。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## 数据分析

- PPTX 样板：`samples/style-sample-data-analytics.pptx`
- PNG 预览：`previews/style-sample-data-analytics.png`
- 效果图母稿提示词：`prompts/style-reference-data-analytics.md`
- clean background 提示词：`prompts/clean-background-data-analytics.md`
- 背景素材：`assets/background-data-analytics.png`
- 适合场景：经营复盘、增长分析、行业报告
- 视觉方向：深色科技背景、高信息密度仪表盘、蓝色发光图表和清晰 KPI 层级，适合数据驱动叙事。
- 透明素材：发光图表装饰、KPI 卡片边框、数据节点和连线元素
- 可编辑层：报告标题、KPI 数字、图表标题、坐标轴标签、来源说明
- 样本标题：2026 AI 应用趋势调研
- 样本正文：企业采用 AI 的竞争点，正从模型能力转向数据资产、流程嵌入和投入产出监控。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：深色仪表盘标题，数字优先，信息密度更高。 正文使用浅蓝灰，KPI 数字和图表标签强调科技感。
- 图表语言：深色仪表盘发光柱，轴线弱化，KPI 与图表形成同一数据语言。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:发光图表装饰、transparent_asset_layer:KPI 卡片边框、transparent_asset_layer:数据节点和连线元素、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧保留低纹理深色留白，使用白色主标题和浅蓝灰正文；高亮元素只作为短线和关键数字使用。
- 图表安全区：右侧图表落在平台光带或网格暗区，使用青色/紫色高亮线条，避免细标签压在高亮眩光中心。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.72, y=0.75, w=5.7, h=1.15；报告标题和副标题，深色低纹理网格。；主标题 1 行，副标题 1 行。
- text_zone：x=0.82, y=2.35, w=4.9, h=2.25；关键指标解释和要点，背景为暗色干净留白。；正文 55 个中文字符以内，3 条短要点。
- chart_zone：x=7, y=1.45, w=4.9, h=4.9；发光数据图表区，避开强眩光中心。；4 组图表，坐标标签 4 个。
- metrics_zone：x=0.82, y=5.45, w=5.55, h=0.95；开放式 KPI 数字组，不使用卡片。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=7, y=2.1, w=5.7, h=4.8；蓝色数据波、网格和发光柱体主视觉。；装饰线不能穿过标签。
- protected_empty_zone：x=5.75, y=0.7, w=1.05, h=6；左右信息分区的暗色过渡带。；保持低对比。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## 国潮东方

- PPTX 样板：`samples/style-sample-oriental-heritage.pptx`
- PNG 预览：`previews/style-sample-oriental-heritage.png`
- 效果图母稿提示词：`prompts/style-reference-oriental-heritage.md`
- clean background 提示词：`prompts/clean-background-oriental-heritage.md`
- 背景素材：`assets/background-oriental-heritage.png`
- 适合场景：品牌介绍、文化项目、消费品提案
- 视觉方向：宣纸质感、朱红墨黑、山水留白和当代表达，适合东方文化、品牌和消费品提案。
- 透明素材：水墨山石装饰、朱红印章元素、梅枝或器物剪影
- 可编辑层：品牌标题、理念卡片文字、章节题签、说明正文、页脚日期
- 样本标题：2026 AI 应用趋势调研
- 样本正文：新技术落地不是一阵风，而是从器、术、法到组织文化的一次长期演进。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：东方题签式标题，留白更重，朱红强调。 正文像品牌理念页，短句、纵深和印章感分隔。
- 图表语言：起承转合四段式柱体，朱红和墨黑交替，像国潮品牌方法论。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:水墨山石装饰、transparent_asset_layer:朱红印章元素、transparent_asset_layer:梅枝或器物剪影、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧或中左侧保留低纹理浅色留白，使用深色主标题和中灰正文；人物、建筑、山水等高细节素材避开正文行高区域。
- 图表安全区：右侧图表落在浅色留白或纸纹过渡区，使用深色/品牌强调色线条，避免柱体或折线压到复杂纹理。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=2.55, y=0.86, w=4.8, h=1.15；东方品牌标题，避开左上红日，落在宣纸留白上。；主标题 1 行，副标题 1 行。
- text_zone：x=3.05, y=2.2, w=3.9, h=2.45；趋势脉络正文，宣纸低纹理留白。；正文 50 个中文字符以内，3 条短要点。
- chart_zone：x=7.35, y=1.55, w=4.65, h=4.55；国潮配色开放式图表，避开山水密集线条。；4 组柱状图，标签 4 个。
- metrics_zone：x=2.35, y=5.45, w=5.55, h=0.95；三组朱红/墨黑指标，不加框。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=0, y=1.8, w=3, h=5.4；山水、梅枝或器物剪影主视觉。；不能穿过正文行。
- protected_empty_zone：x=7.1, y=0.85, w=5.2, h=5.2；图表阅读区，保留浅纸色和淡墨过渡。；不放强水墨纹理。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## 未来科技

- PPTX 样板：`samples/style-sample-future-tech.pptx`
- PNG 预览：`previews/style-sample-future-tech.png`
- 效果图母稿提示词：`prompts/style-reference-future-tech.md`
- clean background 提示词：`prompts/clean-background-future-tech.md`
- 背景素材：`assets/background-future-tech.png`
- 适合场景：AI 发布会、科技产品、创新方案
- 视觉方向：深色空间、蓝绿霓虹、芯片平台和玻璃拟态卡片，适合 AI 产品发布和未来科技叙事。
- 透明素材：玻璃拟态产品卡片、芯片和光效装饰、科技图标组
- 可编辑层：发布会标题、产品卖点、功能卡片文字、时间地点、图表标签
- 样本标题：2026 AI 应用趋势调研
- 样本正文：下一代 AI 应用将围绕多模态输入、智能执行、可信审计和生态连接展开。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：发布会式标题，白字高亮，副标题更像产品 tagline。 正文压缩成能力说明，霓虹强调只给关键词和数字。
- 图表语言：青紫霓虹柱体和极弱网格，模拟发布会大屏的数据模块。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:玻璃拟态产品卡片、transparent_asset_layer:芯片和光效装饰、transparent_asset_layer:科技图标组、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧保留低纹理深色留白，使用白色主标题和浅蓝灰正文；高亮元素只作为短线和关键数字使用。
- 图表安全区：右侧图表落在平台光带或网格暗区，使用青色/紫色高亮线条，避免细标签压在高亮眩光中心。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.72, y=0.75, w=5.7, h=1.15；发布会标题和副标题，深色净空。；主标题 1 行，副标题 1 行。
- text_zone：x=0.82, y=2.35, w=4.9, h=2.25；能力模块说明，避开霓虹强光。；正文 55 个中文字符以内，3 条短要点。
- chart_zone：x=7, y=1.45, w=4.9, h=4.9；霓虹图表区，背景为低纹理玻璃暗面。；4 组柱状图，坐标标签 4 个。
- metrics_zone：x=0.82, y=5.45, w=5.55, h=0.95；开放式科技指标数字，不加玻璃卡片框。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=7, y=2.1, w=5.7, h=4.8；AI 芯片平台、光轨和全息主视觉。；光源避开标签和柱体顶部。
- protected_empty_zone：x=5.75, y=0.7, w=1.05, h=6；左右内容之间的暗色呼吸带。；保持干净，不放强光。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## 编辑杂志

- PPTX 样板：`samples/style-sample-editorial-magazine.pptx`
- PNG 预览：`previews/style-sample-editorial-magazine.png`
- 效果图母稿提示词：`prompts/style-reference-editorial-magazine.md`
- clean background 提示词：`prompts/clean-background-editorial-magazine.md`
- 背景素材：`assets/background-editorial-magazine.png`
- 适合场景：品牌故事、公开演讲、趋势洞察
- 视觉方向：杂志封面级标题、非对称大图留白、克制红色强调和强编辑感排版，适合观点型表达。
- 透明素材：红色编辑标记、裁切图片角标、细线章节编号
- 可编辑层：杂志式主标题、导语正文、章节编号、引用文字、图表注释
- 样本标题：2026 AI 应用趋势调研
- 样本正文：AI 应用的下一阶段不是工具清单竞争，而是组织是否能把判断、素材和流程沉淀成可复用能力。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：编辑杂志式标题，强调观点和节奏，标题更像封面主张。 正文像导语和旁注，留白足，红色只做少量编辑强调。
- 图表语言：细线证据轴、红色关键点和克制柱体，像趋势杂志里的观点图。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:红色编辑标记、transparent_asset_layer:裁切图片角标、transparent_asset_layer:细线章节编号、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧或中左侧保留低纹理浅色留白，使用深色主标题和中灰正文；人物、建筑、山水等高细节素材避开正文行高区域。
- 图表安全区：右侧图表落在浅色留白或纸纹过渡区，使用深色/品牌强调色线条，避免柱体或折线压到复杂纹理。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.74, y=0.78, w=5.85, h=1.35；杂志式主标题和导语，背景只保留轻纸纹。；主标题 1-2 行，副标题 1 行。
- text_zone：x=0.86, y=2.55, w=4.85, h=2.05；观点导语和三条证据，低纹理编辑留白。；正文 60 个中文字符以内，3 条短要点。
- chart_zone：x=7.25, y=1.62, w=4.7, h=4.55；开放式趋势图，红色只做关键转折强调。；4 组柱状图或观点证据轴。
- metrics_zone：x=0.9, y=5.42, w=5.45, h=0.95；编辑式大编号和指标，不加卡片。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=8.25, y=0.15, w=4.7, h=7.1；大图留白、裁切边缘和轻颗粒主视觉。；可承接图片但不承载正文。
- protected_empty_zone：x=5.85, y=0.75, w=1.05, h=6.15；左右非对称版面的呼吸带。；保持干净。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## SaaS 产品

- PPTX 样板：`samples/style-sample-saas-product.pptx`
- PNG 预览：`previews/style-sample-saas-product.png`
- 效果图母稿提示词：`prompts/style-reference-saas-product.md`
- clean background 提示词：`prompts/clean-background-saas-product.md`
- 背景素材：`assets/background-saas-product.png`
- 适合场景：产品发布、SaaS 销售、功能路线图
- 视觉方向：干净产品界面感、柔和蓝绿光、模块化信息但不套大框，适合产品价值和功能流程叙事。
- 透明素材：产品界面浮层、功能图标组、流程节点装饰
- 可编辑层：产品标题、功能卖点、路线节点、指标标签、流程说明
- 样本标题：2026 AI 应用趋势调研
- 样本正文：SaaS 型 AI 产品要把能力说成用户可感知的流程收益，而不是堆模型参数和功能清单。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：产品营销式标题，清晰、直接、偏现代黑体。 正文强调功能收益，搭配流程节点和开放式指标。
- 图表语言：蓝绿增长柱和流程节点结合，表达产品激活、留存和扩展路径。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:产品界面浮层、transparent_asset_layer:功能图标组、transparent_asset_layer:流程节点装饰、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧或中左侧保留低纹理浅色留白，使用深色主标题和中灰正文；人物、建筑、山水等高细节素材避开正文行高区域。
- 图表安全区：右侧图表落在浅色留白或纸纹过渡区，使用深色/品牌强调色线条，避免柱体或折线压到复杂纹理。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.72, y=0.76, w=5.7, h=1.12；产品价值标题和副标题，浅色产品背景净空。；主标题 1 行，副标题 1 行。
- text_zone：x=0.84, y=2.32, w=4.95, h=2.25；功能价值和流程说明，背景为浅蓝低噪声留白。；正文 55 个中文字符以内，3 条短要点。
- chart_zone：x=7.1, y=1.55, w=4.75, h=4.7；增长漏斗或采用趋势图，避免像后台 UI 卡片。；4 组增长数据和标签。
- metrics_zone：x=0.84, y=5.45, w=5.6, h=0.95；开放式产品指标，不做卡片。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=7.15, y=0.5, w=5.65, h=6.2；产品界面透视、流程节点和柔和渐变主视觉。；界面元素只在边缘，不能穿过图表核心。
- protected_empty_zone：x=5.85, y=0.75, w=1.05, h=6.1；产品说明和图表之间的浅色过渡带。；不放高饱和按钮或 UI 文本。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0

## 投资人叙事

- PPTX 样板：`samples/style-sample-investor-narrative.pptx`
- PNG 预览：`previews/style-sample-investor-narrative.png`
- 效果图母稿提示词：`prompts/style-reference-investor-narrative.md`
- clean background 提示词：`prompts/clean-background-investor-narrative.md`
- 背景素材：`assets/background-investor-narrative.png`
- 适合场景：融资路演、商业计划、增长故事
- 视觉方向：深色高信任感、金色增长线、市场叙事和关键指标优先，适合投资人 pitch 和商业计划。
- 透明素材：增长箭头光线、市场地图点位、投资人指标图标
- 可编辑层：融资主张、市场规模数字、增长图表、商业模式标签、里程碑
- 样本标题：2026 AI 应用趋势调研
- 样本正文：投资人需要看到的不只是市场热度，而是需求强度、增长路径、商业模式和团队执行节奏。
- 分层契约：标题、副标题、正文、要点、指标数字、指标标签和图表标签必须作为 PPT 文本对象生成，用户能在 PowerPoint 中直接改。
- 反拆来源：先直出完整效果图，确认审美后从效果图拆解坐标、留白、背景、透明素材和可编辑层。
- 字体系统：投资人 pitch 标题，短促、有主张，数字权重大。 正文压成商业逻辑和证据点，金色只给增长和关键指标。
- 图表语言：深色底上的金色增长线和关键柱体，突出市场规模、收入杠杆和扩张窗口。
- 可编辑重建层：clean_background_raster_layer、transparent_asset_layer:增长箭头光线、transparent_asset_layer:市场地图点位、transparent_asset_layer:投资人指标图标、editable_title_and_subtitle_text、editable_body_and_bullet_text、editable_metric_numbers_and_labels、editable_chart_shapes_and_axis_labels
- 融合策略：采用融合式版面：文本、指标和图表嵌入背景留白、光带或纸纹/玻璃层中，形成同一视觉系统。
- 阅读安全区：左侧保留低纹理深色留白，使用白色主标题和浅蓝灰正文；高亮元素只作为短线和关键数字使用。
- 图表安全区：右侧图表落在平台光带或网格暗区，使用青色/紫色高亮线条，避免细标签压在高亮眩光中心。
- 坐标蓝图：单位 inches，页面 13.333 x 7.5
- title_zone：x=0.72, y=0.75, w=5.7, h=1.15；融资主张标题和副标题，深色高信任净空。；主标题 1 行，副标题 1 行。
- text_zone：x=0.82, y=2.35, w=4.9, h=2.25；增长逻辑和商业化证据，背景为低纹理深色。；正文 55 个中文字符以内，3 条短要点。
- chart_zone：x=7, y=1.45, w=4.9, h=4.9；金色增长曲线和开放式收入图，避开强光中心。；4 组增长数据和标签。
- metrics_zone：x=0.82, y=5.45, w=5.55, h=0.95；投资人关注的市场、窗口、杠杆指标。；3 个大数字，每个 1 个短标签。
- visual_focus_zone：x=7, y=2, w=5.7, h=4.9；市场地图、金色增长线和金融网格主视觉。；光线不能压住坐标和数据标签。
- protected_empty_zone：x=5.75, y=0.7, w=1.05, h=6；左右区之间的深色呼吸带。；保持低对比。
- 可读性契约：配色、配图和字色必须服务可读性：标题、正文、指标、图表线条都要落在背景预留的阅读安全区或图表安全区，过渡区域先由背景生成，不能靠加框补救。
- 白框约束：禁止大白框和容器框：不得用大面积矩形或指标描边框承载正文、指标和图表，浅色区域也必须依靠背景留白、纹理、细线和开放式布局。
- 大面积正文容器：0
- 大面积图表容器：0
- 指标描边框：0
