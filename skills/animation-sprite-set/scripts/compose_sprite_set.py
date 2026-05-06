#!/usr/bin/env python3
"""Compose transparent frames into a spritesheet atlas and optional GIF previews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"could not read manifest JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit("manifest must be a JSON object")
    return value


def positive_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise SystemExit(f"{field} must be a positive integer")
    return value


def non_negative_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise SystemExit(f"{field} must be a non-negative integer")
    return value


def resolve_frame_path(raw_value: Any, *, frames_dir: Path) -> Path:
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise SystemExit("frame path must be a non-empty string")
    path = Path(raw_value).expanduser()
    if not path.is_absolute():
        path = frames_dir / path
    path = path.resolve()
    if not path.is_file():
        raise SystemExit(f"frame image does not exist: {path}")
    return path


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
    left = (cell_width - sprite.width) // 2
    top = (cell_height - sprite.height) // 2
    output.alpha_composite(sprite, (left, top))
    return output


def alpha_nonzero_count(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(alpha.histogram()[1:])


def normalized_states(manifest: dict[str, Any], *, columns: int, frames_dir: Path) -> list[dict[str, Any]]:
    states = manifest.get("states")
    if not isinstance(states, list) or not states:
        raise SystemExit("manifest.states must be a non-empty list")

    normalized: list[dict[str, Any]] = []
    seen_rows: set[int] = set()
    seen_names: set[str] = set()
    for state in states:
        if not isinstance(state, dict):
            raise SystemExit("each state must be a JSON object")
        name = state.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SystemExit("state.name must be a non-empty string")
        name = name.strip()
        if name in seen_names:
            raise SystemExit(f"duplicate state name: {name}")
        seen_names.add(name)

        row = non_negative_int(state.get("row"), field=f"{name}.row")
        if row in seen_rows:
            raise SystemExit(f"duplicate atlas row: {row}")
        seen_rows.add(row)

        raw_frames = state.get("frames")
        if not isinstance(raw_frames, list) or not raw_frames:
            raise SystemExit(f"{name}.frames must be a non-empty list")
        if len(raw_frames) > columns:
            raise SystemExit(f"{name} has {len(raw_frames)} frames, but atlas columns is {columns}")
        frame_paths = [resolve_frame_path(raw_frame, frames_dir=frames_dir) for raw_frame in raw_frames]

        durations_ms = state.get("durations_ms")
        if durations_ms is None:
            durations = [120] * len(frame_paths)
        elif (
            isinstance(durations_ms, list)
            and len(durations_ms) == len(frame_paths)
            and all(isinstance(duration, int) and duration > 0 for duration in durations_ms)
        ):
            durations = durations_ms
        else:
            raise SystemExit(f"{name}.durations_ms must match frame count and contain positive integers")

        normalized.append(
            {
                "name": name,
                "row": row,
                "frame_paths": frame_paths,
                "durations_ms": durations,
            }
        )

    return sorted(normalized, key=lambda item: item["row"])


def save_gif(
    frames: list[Image.Image],
    *,
    durations_ms: list[int],
    output_path: Path,
) -> None:
    if not frames:
        raise SystemExit("cannot save a GIF with no frames")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations_ms,
        loop=0,
        disposal=2,
        transparency=0,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="JSON manifest describing states and frames.")
    parser.add_argument("--frames-dir", required=True, help="Base directory for relative frame paths.")
    parser.add_argument("--output-atlas", required=True, help="Output transparent atlas path.")
    parser.add_argument("--output-dir", required=True, help="Directory for report and optional GIF previews.")
    parser.add_argument("--gif", action="store_true", help="Write one GIF preview per state.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    frames_dir = Path(args.frames_dir).expanduser().resolve()
    output_atlas = Path(args.output_atlas).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not manifest_path.is_file():
        raise SystemExit(f"manifest does not exist: {manifest_path}")
    if not frames_dir.is_dir():
        raise SystemExit(f"frames directory does not exist: {frames_dir}")

    manifest = load_json(manifest_path)
    cell_width = positive_int(manifest.get("cell_width"), field="cell_width")
    cell_height = positive_int(manifest.get("cell_height"), field="cell_height")
    columns = positive_int(manifest.get("columns"), field="columns")
    states = normalized_states(manifest, columns=columns, frames_dir=frames_dir)
    rows = max(state["row"] for state in states) + 1

    atlas = Image.new("RGBA", (columns * cell_width, rows * cell_height), (0, 0, 0, 0))
    report_states: list[dict[str, Any]] = []

    for state in states:
        fitted_frames: list[Image.Image] = []
        for column_index, frame_path in enumerate(state["frame_paths"]):
            with Image.open(frame_path) as opened_frame:
                fitted_frame = fit_frame_to_cell(
                    opened_frame,
                    cell_width=cell_width,
                    cell_height=cell_height,
                )
            fitted_frames.append(fitted_frame)
            atlas.alpha_composite(
                fitted_frame,
                (column_index * cell_width, state["row"] * cell_height),
            )

        if args.gif:
            save_gif(
                fitted_frames,
                durations_ms=state["durations_ms"],
                output_path=output_dir / f"{state['name']}.gif",
            )

        report_states.append(
            {
                "name": state["name"],
                "row": state["row"],
                "frame_count": len(fitted_frames),
                "durations_ms": state["durations_ms"],
                "nontransparent_pixels": [alpha_nonzero_count(frame) for frame in fitted_frames],
            }
        )

    output_atlas.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    atlas.save(output_atlas)

    result = {
        "ok": True,
        "manifest": str(manifest_path),
        "atlas": {
            "path": str(output_atlas),
            "width": atlas.width,
            "height": atlas.height,
            "columns": columns,
            "rows": rows,
            "cell_width": cell_width,
            "cell_height": cell_height,
        },
        "states": report_states,
        "gif": bool(args.gif),
    }
    (output_dir / "sprite-set-report.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
