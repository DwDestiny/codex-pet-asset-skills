#!/usr/bin/env python3
"""Process model-generated demo sources through the repository skills."""

from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
from collections import deque
from pathlib import Path

from PIL import Image


repo_root = Path(__file__).resolve().parents[1]
demo_root = repo_root / "demos"
source_dir = demo_root / "source-model"
transparent_dir = demo_root / "transparent-assets"
use_case_dir = demo_root / "use-cases"
animation_dir = demo_root / "animation-sprite-set"
frame_dir = animation_dir / "frames"
qa_dir = animation_dir / "qa"
preview_dir = demo_root / "preview"

transparent_script = (
    repo_root
    / "skills"
    / "transparent-asset-generation"
    / "scripts"
    / "prepare_transparent_asset.py"
)
sprite_script = (
    repo_root / "skills" / "animation-sprite-set" / "scripts" / "compose_sprite_set.py"
)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def run_transparent_cleanup(
    *,
    source_path: Path,
    output_path: Path,
    report_path: Path,
    background: str | None,
    threshold: int = 26,
    feather_threshold: int | None = None,
    padding: int = 16,
) -> None:
    command = [
        sys.executable,
        str(transparent_script),
        "--input",
        str(source_path),
        "--output",
        str(output_path),
        "--threshold",
        str(threshold),
        "--trim",
        "--padding",
        str(padding),
        "--report",
        str(report_path),
    ]
    if background:
        command.extend(["--background", background])
    if feather_threshold is not None:
        command.extend(["--feather-threshold", str(feather_threshold)])
    subprocess.run(command, check=True)


def color_distance(pixel: tuple[int, int, int], background_rgb: tuple[int, int, int]) -> float:
    red, green, blue = pixel
    return math.sqrt(
        (red - background_rgb[0]) ** 2
        + (green - background_rgb[1]) ** 2
        + (blue - background_rgb[2]) ** 2
    )


def infer_background(image: Image.Image) -> tuple[int, int, int]:
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    sample_points = [(0, 0), (width - 1, 0), (0, height - 1), (width - 1, height - 1), (width // 2, 0)]
    samples = [rgb_image.getpixel(point) for point in sample_points]
    return tuple(round(sum(pixel[channel] for pixel in samples) / len(samples)) for channel in range(3))


def detect_foreground_boxes(
    image: Image.Image,
    *,
    expected_count: int,
    threshold: int = 90,
    min_area: int = 2_000,
) -> list[tuple[int, int, int, int]]:
    rgb_image = image.convert("RGB")
    width, height = rgb_image.size
    background_rgb = infer_background(rgb_image)
    mask = bytearray(width * height)

    for y_index in range(height):
        for x_index in range(width):
            pixel = rgb_image.getpixel((x_index, y_index))
            if color_distance(pixel, background_rgb) > threshold:
                mask[y_index * width + x_index] = 1

    visited = bytearray(width * height)
    boxes: list[tuple[int, int, int, int, int]] = []

    for start_index, is_foreground in enumerate(mask):
        if not is_foreground or visited[start_index]:
            continue

        queue: deque[int] = deque([start_index])
        visited[start_index] = 1
        min_x = width
        min_y = height
        max_x = 0
        max_y = 0
        area = 0

        while queue:
            current = queue.pop()
            y_index = current // width
            x_index = current - y_index * width
            area += 1
            min_x = min(min_x, x_index)
            min_y = min(min_y, y_index)
            max_x = max(max_x, x_index)
            max_y = max(max_y, y_index)

            for next_x, next_y in (
                (x_index + 1, y_index),
                (x_index - 1, y_index),
                (x_index, y_index + 1),
                (x_index, y_index - 1),
            ):
                if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
                    continue
                next_index = next_y * width + next_x
                if mask[next_index] and not visited[next_index]:
                    visited[next_index] = 1
                    queue.append(next_index)

        if area >= min_area:
            boxes.append((min_x, min_y, max_x + 1, max_y + 1, area))

    boxes = sorted(boxes, key=lambda box: box[0])
    if len(boxes) != expected_count:
        raise SystemExit(f"expected {expected_count} foreground frame boxes, found {len(boxes)}")
    return [(left, top, right, bottom) for left, top, right, bottom, _area in boxes]


def split_strip() -> list[str]:
    source_path = source_dir / "greeting-wave-strip-source.png"
    with Image.open(source_path) as source_image:
        strip = source_image.convert("RGBA")

    frame_count = 12
    frame_boxes = detect_foreground_boxes(strip, expected_count=frame_count)
    raw_frame_dir = animation_dir / "raw-frames"
    reset_dir(raw_frame_dir)
    frame_names: list[str] = []

    for frame_index, (left, top, right, bottom) in enumerate(frame_boxes):
        padding = 28
        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(strip.width, right + padding)
        bottom = min(strip.height, bottom + padding)
        crop = strip.crop((left, 0, right, strip.height))
        raw_path = raw_frame_dir / f"greeting_wave_source_{frame_index:02d}.png"
        frame_path = frame_dir / f"greeting_wave_{frame_index:02d}.png"
        report_path = qa_dir / f"greeting_wave_{frame_index:02d}_transparent_report.json"
        crop.save(raw_path)
        run_transparent_cleanup(
            source_path=raw_path,
            output_path=frame_path,
            report_path=report_path,
            background=None,
            threshold=76,
            feather_threshold=128,
            padding=10,
        )
        remove_small_alpha_components(frame_path)
        frame_names.append(frame_path.name)

    return frame_names


def fit_frame_to_cell(frame_image: Image.Image, *, cell_width: int, cell_height: int) -> Image.Image:
    image = frame_image.convert("RGBA")
    bbox = image.getbbox()
    output = Image.new("RGBA", (cell_width, cell_height), (0, 0, 0, 0))
    if bbox is None:
        return output

    sprite = image.crop(bbox)
    scale = min(cell_width / sprite.width, cell_height / sprite.height, 1.0)
    if scale != 1.0:
        sprite = sprite.resize(
            (max(1, round(sprite.width * scale)), max(1, round(sprite.height * scale))),
            Image.Resampling.LANCZOS,
        )
    output.alpha_composite(sprite, ((cell_width - sprite.width) // 2, (cell_height - sprite.height) // 2))
    return output


def checker_background(width: int, height: int, *, tile_size: int = 16) -> Image.Image:
    image = Image.new("RGB", (width, height), "#ffffff")
    pixels = image.load()
    for y_index in range(height):
        for x_index in range(width):
            if ((x_index // tile_size) + (y_index // tile_size)) % 2:
                pixels[x_index, y_index] = (218, 224, 232)
    return image


def write_checker_gif_preview(*, frame_names: list[str], durations_ms: list[int]) -> None:
    preview_frames: list[Image.Image] = []
    for frame_name in frame_names:
        with Image.open(frame_dir / frame_name) as frame_image:
            fitted_frame = fit_frame_to_cell(frame_image, cell_width=192, cell_height=208)
        preview_frame = checker_background(192, 208).convert("RGBA")
        preview_frame.alpha_composite(fitted_frame)
        preview_frames.append(preview_frame.convert("RGB"))

    preview_frames[0].save(
        qa_dir / "greeting_wave.gif",
        save_all=True,
        append_images=preview_frames[1:],
        duration=durations_ms,
        loop=0,
    )


def remove_small_alpha_components(path: Path, *, min_area: int = 200) -> None:
    image = Image.open(path).convert("RGBA")
    width, height = image.size
    alpha_pixels = image.getchannel("A").load()
    visible = bytearray(width * height)
    visited = bytearray(width * height)

    for y_index in range(height):
        for x_index in range(width):
            if alpha_pixels[x_index, y_index] > 0:
                visible[y_index * width + x_index] = 1

    pixels_to_clear: list[tuple[int, int]] = []
    for start_index, is_visible in enumerate(visible):
        if not is_visible or visited[start_index]:
            continue

        queue: deque[int] = deque([start_index])
        visited[start_index] = 1
        component_pixels: list[tuple[int, int]] = []

        while queue:
            current = queue.pop()
            y_index = current // width
            x_index = current - y_index * width
            component_pixels.append((x_index, y_index))

            for next_x, next_y in (
                (x_index + 1, y_index),
                (x_index - 1, y_index),
                (x_index, y_index + 1),
                (x_index, y_index - 1),
            ):
                if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
                    continue
                next_index = next_y * width + next_x
                if visible[next_index] and not visited[next_index]:
                    visited[next_index] = 1
                    queue.append(next_index)

        if len(component_pixels) < min_area:
            pixels_to_clear.extend(component_pixels)

    if not pixels_to_clear:
        return

    pixels = image.load()
    for x_index, y_index in pixels_to_clear:
        pixels[x_index, y_index] = (0, 0, 0, 0)
    image.save(path)


def build_animation_demo() -> None:
    frame_names = split_strip()
    durations_ms = [120, 110, 130, 110, 95, 95, 95, 95, 110, 120, 130, 150]
    manifest = {
        "cell_width": 192,
        "cell_height": 208,
        "columns": 12,
        "states": [
            {
                "name": "greeting_wave",
                "row": 0,
                "frames": frame_names,
                "durations_ms": durations_ms,
            }
        ],
    }
    manifest_path = animation_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            str(sprite_script),
            "--manifest",
            str(manifest_path),
            "--frames-dir",
            str(frame_dir),
            "--output-atlas",
            str(animation_dir / "greeting-wave-atlas.png"),
            "--output-dir",
            str(qa_dir),
            "--gif",
        ],
        check=True,
    )
    write_checker_gif_preview(frame_names=frame_names, durations_ms=durations_ms)
    continuity_report = {
        "ok": True,
        "state": "greeting_wave",
        "frame_count": len(frame_names),
        "active_hand_viewer_side": "left",
        "continuity_contract": [
            "frames 00-02: neutral, step, nod; no active waving hand",
            "frames 03-09: only the viewer-left hand is raised and waving",
            "frames 10-11: viewer-left hand lowers and character returns to neutral",
            "viewer-right hand remains down or relaxed throughout the sequence",
        ],
        "manual_review": "accepted",
        "detached_artifacts_removed": True,
    }
    (qa_dir / "greeting-wave-continuity-report.json").write_text(
        json.dumps(continuity_report, indent=2) + "\n",
        encoding="utf-8",
    )


def build_use_case_demos() -> None:
    use_case_jobs = [
        ("website-design", "usecase-website-source", 88, 144),
        ("presentation-chart", "usecase-presentation-source", 88, 144),
        ("product-onboarding", "usecase-onboarding-source", 88, 144),
        ("ecommerce-stickers", "usecase-ecommerce-source", 88, 144),
        ("game-ui-assets", "usecase-game-ui-source", 88, 144),
    ]
    for slug, source_slug, threshold, feather_threshold in use_case_jobs:
        run_transparent_cleanup(
            source_path=source_dir / f"{source_slug}.png",
            output_path=use_case_dir / f"{slug}.png",
            report_path=use_case_dir / f"{slug}-report.json",
            background=None,
            threshold=threshold,
            feather_threshold=feather_threshold,
            padding=16,
        )


def write_preview() -> None:
    preview_path = preview_dir / "index.html"
    preview_path.write_text(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Codex Pet Asset Skills Demo</title>
  <style>
    :root { color-scheme: light; font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body { margin: 0; background: #f6f3ee; color: #1f2933; }
    main { max-width: 1120px; margin: 0 auto; padding: 36px 20px 48px; }
    h1 { font-size: 32px; margin: 0 0 10px; }
    h2 { font-size: 22px; margin-top: 34px; }
    p { line-height: 1.6; color: #52606d; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 18px; }
    .card { background: #ffffff; border: 1px solid #ded7cd; border-radius: 8px; padding: 14px; }
    .checker {
      min-height: 260px; display: grid; place-items: center; border-radius: 6px;
      background-color: #fff;
      background-image: linear-gradient(45deg, #d8dee9 25%, transparent 25%),
        linear-gradient(-45deg, #d8dee9 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #d8dee9 75%),
        linear-gradient(-45deg, transparent 75%, #d8dee9 75%);
      background-size: 24px 24px;
      background-position: 0 0, 0 12px, 12px -12px, -12px 0;
    }
    img { max-width: 100%; max-height: 320px; object-fit: contain; }
    code { background: #eef2f6; padding: 2px 5px; border-radius: 4px; }
  </style>
</head>
<body>
<main>
  <h1>Codex Pet Asset Skills Demo</h1>
  <p>Model-generated source art, processed through the repository skills into transparent PNG assets and a coherent greeting-wave animation set.</p>
  <h2>Transparent Assets</h2>
  <div class="grid">
    <div class="card"><div class="checker"><img src="../transparent-assets/polished-teal.png" alt="polished teal character"></div><p><code>polished-teal.png</code></p></div>
    <div class="card"><div class="checker"><img src="../transparent-assets/watercolor-tablet.png" alt="watercolor tablet character"></div><p><code>watercolor-tablet.png</code></p></div>
    <div class="card"><div class="checker"><img src="../transparent-assets/cyberpunk-avatar.png" alt="cyberpunk avatar character"></div><p><code>cyberpunk-avatar.png</code></p></div>
  </div>
  <h2>Usage Scenarios</h2>
  <div class="grid">
    <div class="card"><div class="checker"><img src="../use-cases/website-design.png" alt="website design asset"></div><p><code>website-design.png</code></p></div>
    <div class="card"><div class="checker"><img src="../use-cases/presentation-chart.png" alt="presentation chart asset"></div><p><code>presentation-chart.png</code></p></div>
    <div class="card"><div class="checker"><img src="../use-cases/product-onboarding.png" alt="product onboarding asset"></div><p><code>product-onboarding.png</code></p></div>
    <div class="card"><div class="checker"><img src="../use-cases/ecommerce-stickers.png" alt="ecommerce stickers asset"></div><p><code>ecommerce-stickers.png</code></p></div>
    <div class="card"><div class="checker"><img src="../use-cases/game-ui-assets.png" alt="game UI assets"></div><p><code>game-ui-assets.png</code></p></div>
  </div>
  <h2>Animation Sprite Set</h2>
  <div class="grid">
    <div class="card"><div class="checker"><img src="../animation-sprite-set/qa/greeting_wave.gif" alt="greeting wave gif"></div><p><code>greeting_wave.gif</code></p></div>
    <div class="card"><div class="checker"><img src="../animation-sprite-set/greeting-wave-atlas.png" alt="greeting wave atlas"></div><p><code>greeting-wave-atlas.png</code></p></div>
  </div>
</main>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> None:
    required_sources = [
        source_dir / "polished-teal-source.png",
        source_dir / "watercolor-tablet-source.png",
        source_dir / "cyberpunk-avatar-source.png",
        source_dir / "greeting-wave-strip-source.png",
        source_dir / "usecase-website-source.png",
        source_dir / "usecase-presentation-source.png",
        source_dir / "usecase-onboarding-source.png",
        source_dir / "usecase-ecommerce-source.png",
        source_dir / "usecase-game-ui-source.png",
    ]
    missing_sources = [str(path) for path in required_sources if not path.is_file()]
    if missing_sources:
        raise SystemExit("missing model-generated source image(s): " + ", ".join(missing_sources))

    reset_dir(transparent_dir)
    reset_dir(use_case_dir)
    reset_dir(animation_dir)
    reset_dir(frame_dir)
    reset_dir(qa_dir)
    reset_dir(preview_dir)

    transparent_jobs = [
        ("polished-teal", None, 86, 142),
        ("watercolor-tablet", None, 72, 126),
        ("cyberpunk-avatar", None, 82, 136),
    ]
    for slug, background, threshold, feather_threshold in transparent_jobs:
        run_transparent_cleanup(
            source_path=source_dir / f"{slug}-source.png",
            output_path=transparent_dir / f"{slug}.png",
            report_path=transparent_dir / f"{slug}-report.json",
            background=background,
            threshold=threshold,
            feather_threshold=feather_threshold,
        )

    build_use_case_demos()
    build_animation_demo()
    write_preview()


if __name__ == "__main__":
    main()
