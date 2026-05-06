---
name: transparent-asset-generation
description: Generate transparent-background raster assets with Codex image generation plus deterministic cleanup. Use when the user wants a PNG sticker, icon, mascot, sprite, UI asset, or web-ready visual element with transparent background, or asks to remove/avoid a generated image background while preserving the subject.
---

# Transparent Asset Generation

## 核心判断

先让 Codex 生图得到“容易抠干净”的图，再用脚本做确定性清理。不要要求模型直接画棋盘格透明背景；棋盘格会变成图像内容。优先让模型使用纯色背景，例如 `#FF00FF` 或 `#00FF00`，并明确主体不能使用接近背景的颜色。

适合输出：透明 PNG、网页素材、贴纸、图标、单帧 sprite、角色/物体素材。

不适合输出：多帧动画、spritesheet、视频；这些转给 `$animation-sprite-set`。

## 工作流

1. 明确素材用途、尺寸、主体边界和禁用元素。
2. 调用 Codex 生图能力生成带纯色背景的候选图。
3. 目视检查：主体完整、没有阴影地面、没有漂浮杂点、主体颜色不接近背景色。
4. 用 `scripts/prepare_transparent_asset.py` 清理纯色背景、裁切透明边缘、输出 PNG。
5. 打开结果或检查报告，确认透明角落、主体不被误删。

## 生图提示词要点

使用简短、强约束的提示词：

```text
Create a single centered web asset of <subject>.
Use a perfectly flat #FF00FF background for later chroma key removal.
The subject must not contain magenta, pink, or colors close to #FF00FF.
No shadows, floor, scenery, text, labels, checkerboard pattern, glow, blur, or detached decorative particles.
Keep the full subject inside the canvas with clear spacing.
```

如果主体天然包含粉色或品红，换成 `#00FF00`、`#00FFFF` 或其他不会出现在主体里的纯色。

更多提示词和 QA 细节见 `references/prompt-and-cleanup.md`。

## 清理脚本

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/transparent-asset-generation/scripts/prepare_transparent_asset.py" \
  --input /absolute/path/source.png \
  --output /absolute/path/asset.png \
  --background "#FF00FF" \
  --threshold 24 \
  --feather-threshold 48 \
  --trim \
  --padding 8 \
  --report /absolute/path/report.json
```

参数说明：

- `--background`：要移除的纯色背景；不传时用四角颜色估算。
- `--threshold`：颜色容差。背景边缘残留就调大；主体被吃掉就调小或重生图换背景色。
- `--feather-threshold`：可选的边缘柔化容差，用来淡化生图抗锯齿留下的背景色毛边。
- `--trim` 和 `--padding`：裁掉透明边缘并保留一点安全留白。

脚本只做背景清理，不会补画、重绘、扩图或创造新素材。

## 验收标准

- 输出必须是 `.png`，并带 alpha 透明通道。
- 四角应透明，主体边缘不缺块。
- 主体外没有阴影、地面、光晕、漂浮符号、文字或背景色残留。
- 素材在深色、浅色、棋盘格背景上都能读清。
- 如果清理后主体明显破损，重新生图或换背景色，不要靠脚本硬修。
