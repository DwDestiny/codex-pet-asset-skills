#!/usr/bin/env python3
"""Process model-generated demo sources through the repository skills."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


repo_root = Path(__file__).resolve().parents[1]
demo_root = repo_root / "demos"
source_dir = demo_root / "source-model"
transparent_dir = demo_root / "transparent-assets"
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


def split_strip() -> list[str]:
    source_path = source_dir / "waving-strip-source.png"
    with Image.open(source_path) as source_image:
        strip = source_image.convert("RGBA")

    frame_count = 6
    slot_width = strip.width // frame_count
    raw_frame_dir = animation_dir / "raw-frames"
    reset_dir(raw_frame_dir)
    frame_names: list[str] = []

    for frame_index in range(frame_count):
        left = frame_index * slot_width
        right = strip.width if frame_index == frame_count - 1 else (frame_index + 1) * slot_width
        crop = strip.crop((left, 0, right, strip.height))
        raw_path = raw_frame_dir / f"waving_source_{frame_index:02d}.png"
        frame_path = frame_dir / f"waving_{frame_index:02d}.png"
        report_path = qa_dir / f"waving_{frame_index:02d}_transparent_report.json"
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
        frame_names.append(frame_path.name)

    return frame_names


def build_animation_demo() -> None:
    frame_names = split_strip()
    manifest = {
        "cell_width": 192,
        "cell_height": 208,
        "columns": 6,
        "states": [
            {
                "name": "waving",
                "row": 0,
                "frames": frame_names,
                "durations_ms": [140, 120, 140, 120, 160, 180],
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
            str(animation_dir / "waving-atlas.png"),
            "--output-dir",
            str(qa_dir),
            "--gif",
        ],
        check=True,
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
  <p>Model-generated source art, processed through the repository skills into transparent PNG assets and a waving animation set.</p>
  <h2>Transparent Assets</h2>
  <div class="grid">
    <div class="card"><div class="checker"><img src="../transparent-assets/polished-teal.png" alt="polished teal character"></div><p><code>polished-teal.png</code></p></div>
    <div class="card"><div class="checker"><img src="../transparent-assets/watercolor-tablet.png" alt="watercolor tablet character"></div><p><code>watercolor-tablet.png</code></p></div>
    <div class="card"><div class="checker"><img src="../transparent-assets/cyberpunk-avatar.png" alt="cyberpunk avatar character"></div><p><code>cyberpunk-avatar.png</code></p></div>
  </div>
  <h2>Animation Sprite Set</h2>
  <div class="grid">
    <div class="card"><div class="checker"><img src="../animation-sprite-set/qa/waving.gif" alt="waving gif"></div><p><code>waving.gif</code></p></div>
    <div class="card"><div class="checker"><img src="../animation-sprite-set/waving-atlas.png" alt="waving atlas"></div><p><code>waving-atlas.png</code></p></div>
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
        source_dir / "waving-strip-source.png",
    ]
    missing_sources = [str(path) for path in required_sources if not path.is_file()]
    if missing_sources:
        raise SystemExit("missing model-generated source image(s): " + ", ".join(missing_sources))

    reset_dir(transparent_dir)
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

    build_animation_demo()
    write_preview()


if __name__ == "__main__":
    main()
