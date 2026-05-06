#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const candidates = [
  {
    slug: "business-calm",
    name: "业务冷静型",
    background: "#F5F6F3",
    foreground: "#17202A",
    accent: "#1F8A70",
    accent2: "#E76F51",
    prompt:
      "Create a mini style board for a calm business presentation. Light warm gray background, restrained green accent, subtle orange highlights, clean process cards, editable chart feeling, no logos, no readable fake text, 16:9.",
  },
  {
    slug: "editorial",
    name: "编辑杂志型",
    background: "#FFF9EF",
    foreground: "#202124",
    accent: "#E85D4F",
    accent2: "#0E9AA7",
    prompt:
      "Create a 16:9 editorial magazine style board for a presentation. Large confident title area, generous white space, image placeholders, tomato red and teal accents, tactile paper texture, no logos, no readable fake text.",
  },
  {
    slug: "product-demo",
    name: "产品演示型",
    background: "#F8FBFF",
    foreground: "#172033",
    accent: "#00A6D6",
    accent2: "#F4C542",
    prompt:
      "Create a 16:9 product demo style board. Clean SaaS interface panels, command workspace, task checklist, preview cards for PPTX and visual assets, cyan accents, small lemon highlights, no logos, no readable fake text.",
  },
  {
    slug: "data-report",
    name: "数据图表型",
    background: "#F7FAFC",
    foreground: "#101828",
    accent: "#4568DC",
    accent2: "#B06AB3",
    prompt:
      "Create a 16:9 data report style board. Precise dashboard composition, editable chart feeling, matrix blocks, dark navy typography, mint and magenta accents, clean grid, no logos, no readable fake text.",
  },
  {
    slug: "visual-story",
    name: "视觉叙事型",
    background: "#FFFDF7",
    foreground: "#232323",
    accent: "#65B6FF",
    accent2: "#FF7C8A",
    prompt:
      "Create a 16:9 visual storytelling style board. Friendly editorial illustration, clean white background, sky blue, coral and soft green accents, journey map, transparent sticker-like assets, no logos, no readable fake text.",
  },
];

function parse_args(argv) {
  const args = {};
  for (let index = 2; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--output-dir") {
      args.output_dir = argv[index + 1];
      index += 1;
    } else if (token === "--topic") {
      args.topic = argv[index + 1];
      index += 1;
    } else if (token === "--help" || token === "-h") {
      args.help = true;
    } else {
      throw new Error(`unknown argument: ${token}`);
    }
  }
  return args;
}

function usage() {
  return [
    "Usage:",
    "  node build_style_candidates.js --output-dir /absolute/path/style-candidates --topic \"deck topic\"",
    "",
    "Writes five SVG style boards and style-candidates.md.",
  ].join("\n");
}

function escape_xml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;");
}

function build_svg(candidate, topic) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <rect width="1280" height="720" fill="${candidate.background}"/>
  <rect x="58" y="70" width="104" height="12" fill="${candidate.accent2}"/>
  <text x="58" y="145" font-family="Arial, sans-serif" font-size="42" font-weight="700" fill="${candidate.foreground}">${escape_xml(candidate.name)}</text>
  <text x="58" y="192" font-family="Arial, sans-serif" font-size="22" fill="${candidate.foreground}" opacity="0.72">${escape_xml(topic)}</text>
  <rect x="58" y="265" width="305" height="245" rx="10" fill="#FFFFFF" opacity="0.78" stroke="${candidate.accent}" stroke-width="2"/>
  <rect x="405" y="245" width="360" height="285" rx="10" fill="#FFFFFF" opacity="0.55" stroke="${candidate.accent2}" stroke-width="2"/>
  <rect x="820" y="155" width="330" height="410" rx="12" fill="#FFFFFF" opacity="0.66" stroke="${candidate.accent}" stroke-width="2"/>
  <circle cx="122" cy="345" r="34" fill="${candidate.accent}"/>
  <circle cx="210" cy="345" r="34" fill="${candidate.accent2}"/>
  <circle cx="298" cy="345" r="34" fill="${candidate.foreground}" opacity="0.85"/>
  <rect x="455" y="438" width="42" height="58" fill="${candidate.accent}"/>
  <rect x="525" y="388" width="42" height="108" fill="${candidate.accent2}"/>
  <rect x="595" y="335" width="42" height="161" fill="${candidate.accent}"/>
  <line x1="860" y1="255" x2="1090" y2="255" stroke="${candidate.accent}" stroke-width="5"/>
  <line x1="860" y1="330" x2="1040" y2="330" stroke="${candidate.accent2}" stroke-width="5"/>
  <line x1="860" y1="405" x2="1115" y2="405" stroke="${candidate.foreground}" stroke-width="5" opacity="0.55"/>
  <text x="58" y="630" font-family="Arial, sans-serif" font-size="18" fill="${candidate.foreground}" opacity="0.68">style board / cover rhythm / chart language / transparent asset direction</text>
</svg>
`;
}

function main() {
  let args;
  try {
    args = parse_args(process.argv);
  } catch (error) {
    console.error(`${error.message}\n\n${usage()}`);
    process.exit(1);
  }
  if (args.help) {
    console.log(usage());
    return;
  }
  if (!args.output_dir) {
    console.error(`missing --output-dir\n\n${usage()}`);
    process.exit(1);
  }
  const output_dir = path.resolve(args.output_dir);
  const topic = args.topic || "Visual PPT deck";
  fs.mkdirSync(output_dir, { recursive: true });
  const markdown_lines = ["# 5 套风格候选", ""];
  for (const candidate of candidates) {
    const file_name = `style-board-${candidate.slug}.svg`;
    fs.writeFileSync(path.join(output_dir, file_name), build_svg(candidate, topic), "utf8");
    markdown_lines.push(`## ${candidate.name}`);
    markdown_lines.push("");
    markdown_lines.push(`- 候选图：\`${file_name}\``);
    markdown_lines.push(`- 生图 prompt：\`${candidate.prompt}\``);
    markdown_lines.push("- 验收：应能一眼看出封面节奏、内容页结构、图表语言和透明素材使用方向。");
    markdown_lines.push("");
  }
  fs.writeFileSync(path.join(output_dir, "style-candidates.md"), `${markdown_lines.join("\n")}\n`, "utf8");
  console.log(
    JSON.stringify(
      {
        ok: true,
        output_dir,
        candidate_count: candidates.length,
      },
      null,
      2
    )
  );
}

main();
