# Codex Pet Asset Skills

Two small Codex skills extracted from the official `hatch-pet` asset workflow:

- `transparent-asset-generation` — generate a clean single transparent PNG asset with Codex image generation plus deterministic background cleanup.
- `animation-sprite-set` — plan, QA, and package continuous animation frames into GIF previews and transparent spritesheet atlases.

The goal is to keep the useful material-production parts of `hatch-pet` reusable without forcing every image task through a full custom-pet pipeline.

## Install

Install both skills globally for Codex:

```bash
npx skills add DwDestiny/codex-pet-asset-skills --skill '*' -g -a codex -y
```

Install only one:

```bash
npx skills add DwDestiny/codex-pet-asset-skills --skill transparent-asset-generation -g -a codex -y
npx skills add DwDestiny/codex-pet-asset-skills --skill animation-sprite-set -g -a codex -y
```

List available skills without installing:

```bash
npx skills add DwDestiny/codex-pet-asset-skills --list
```

## Use

Ask Codex directly:

```text
Use $transparent-asset-generation to create a transparent PNG mascot asset for my website.
```

```text
Use $animation-sprite-set to turn this character into idle, waving, and working GIF animation assets.
```

## What Each Skill Does

`transparent-asset-generation` guides Codex to generate an image on a flat removable background, then uses:

```bash
python ~/.codex/skills/transparent-asset-generation/scripts/prepare_transparent_asset.py --help
```

to remove the flat background, trim transparent edges, and output a PNG report.

`animation-sprite-set` guides Codex to define frame specs, keep identity consistent across frames, and then uses:

```bash
python ~/.codex/skills/animation-sprite-set/scripts/compose_sprite_set.py --help
```

to compose transparent frames into an atlas and optional GIF previews.

## Repository Layout

```text
skills/
  transparent-asset-generation/
    SKILL.md
    scripts/prepare_transparent_asset.py
    references/prompt-and-cleanup.md
  animation-sprite-set/
    SKILL.md
    scripts/compose_sprite_set.py
    references/codex-pet-rows.md
tests/
  test_asset_scripts.py
```

## Notes

These skills do not replace the official `hatch-pet` skill. Use `hatch-pet` when you want a complete Codex custom pet package with `pet.json`, full 8x9 atlas validation, QA contact sheets, previews, and app-ready packaging.

Use these two skills when you only need the reusable material steps: transparent asset generation or continuous animation assets.
