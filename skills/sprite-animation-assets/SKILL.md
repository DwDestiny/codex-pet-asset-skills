---
name: sprite-animation-assets
description: Plan, generate, QA, and package continuous raster animation frame sets, GIF previews, and transparent spritesheet atlases. Use when the user asks for a GIF animation, animation frames, sprite rows, web/game animation assets, or reusable visual animation materials.
---

# Sprite Animation Assets

## 核心判断

动画素材的关键不是“单张图好看”，而是同一个角色或物体在每一帧里保持身份一致、尺寸一致、背景透明、动作能循环。先定义帧规格和状态，再逐组生图，最后用脚本组装和验收。

适合输出：连续帧 PNG、单状态 GIF、透明 spritesheet、固定网格 atlas、网页/游戏动画素材。

不适合输出：单张透明素材；这类转给 `$transparent-visual-assets`。

## 工作流

1. 定义规格：状态名、每个状态帧数、画布尺寸、输出格式。
2. 生成或确认一张 canonical base image，作为所有帧的身份锚点。
3. 分状态生成连续帧；每组帧都要使用同一角色参考和同一纯色背景或透明背景策略。
4. 目视 QA：身份一致、动作连贯、无漂浮杂点、无文字、无阴影地面、无裁切。
5. 如需要，先用 `$transparent-visual-assets` 把每帧处理成透明 PNG。
6. 用 `scripts/compose_sprite_set.py` 组合 atlas，并可导出每个状态的 GIF 预览。
7. 检查 `sprite-set-report.json`，再打开 atlas/GIF 做最终验收。

## 生图提示词要点

每组动画都要锁定身份：

```text
Create <frame_count> separated frames of the same <subject> for a looping sprite animation.
Keep the same silhouette, proportions, face, palette, outline style, and accessories in every frame.
Use a flat removable background color <background_color>, with no shadows, text, scenery, motion trails, frame numbers, grid lines, or detached decorative effects.
Each pose must be fully visible, separated from the next pose, and safe to crop into a transparent frame.
Action: <state_action>.
```

如果需要兼容 Codex 自定义宠物的 atlas 规格，先读 `references/sprite-atlas-layouts.md`，使用官方 `hatch-pet` 拆出的 8x9、192x208、9 行状态口径。

## 组装脚本

准备 manifest：

```json
{
  "cell_width": 192,
  "cell_height": 208,
  "columns": 8,
  "states": [
    {
      "name": "idle",
      "row": 0,
      "frames": ["idle_000.png", "idle_001.png"],
      "durations_ms": [120, 120]
    }
  ]
}
```

运行：

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/sprite-animation-assets/scripts/compose_sprite_set.py" \
  --manifest /absolute/path/manifest.json \
  --frames-dir /absolute/path/frames \
  --output-atlas /absolute/path/spritesheet.png \
  --output-dir /absolute/path/qa \
  --gif
```

脚本会：

- 把每帧居中放入固定 cell。
- 保持未使用 cell 全透明。
- 输出 `sprite-set-report.json`。
- 使用 `--gif` 时，为每个状态导出一个 GIF 预览。

## 验收标准

- 每个状态帧数符合 manifest。
- 同一角色/物体在所有帧里保持同一身份，不变物种、不变脸、不变配色。
- 所有帧都是透明背景或可干净抠透明背景。
- 动作能循环，首尾不明显跳变。
- spritesheet 未使用格子必须完全透明。
- GIF 只是预览；最终网页/游戏素材优先交付 PNG 帧或透明 atlas。
