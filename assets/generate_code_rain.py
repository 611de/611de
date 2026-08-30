#!/usr/bin/env python3
"""Generate an animated cyberpunk "code rain" divider SVG for the profile README."""
import random

random.seed(611)

W, H = 840, 90
COLS = 28
GLYPHS = "01アイウエオカキクケコサシスセソ<>{}/*#+=;"

FONT = 13
STEP = 16  # horizontal spacing between columns

defs = []
cols = []
for i in range(COLS):
    x = 14 + i * STEP
    n = random.randint(3, 5)          # glyphs per falling head
    dur = round(random.uniform(2.2, 5.0), 2)
    delay = round(random.uniform(0, dur), 2)
    color = random.choice(["#22d3ee", "#8b5cf6", "#3b82f6", "#34d399"])

    glyphs = []
    for j in range(n):
        g = random.choice(GLYPHS)
        if g == "&":
            g = "&amp;"
        elif g == "<":
            g = "&lt;"
        elif g == ">":
            g = "&gt;"
        # leading glyph bright, trailing glyphs fade out
        opacity = 1.0 if j == 0 else max(0.12, 0.55 - j * 0.16)
        size = FONT if j == 0 else FONT - 2
        glyphs.append(
            f'<text x="0" y="{-j * (FONT + 3)}" font-size="{size}" '
            f'fill="{color}" fill-opacity="{opacity}">{g}</text>'
        )

    cols.append(
        f'<g transform="translate({x} 0)" opacity="0.9">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="{x} {-H}" to="{x} {H}" dur="{dur}s" begin="{delay}s" '
        f'repeatCount="indefinite"/>{"".join(glyphs)}</g>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="code rain divider">
  <defs>
    <clipPath id="rain"><rect x="0" y="0" width="{W}" height="{H}" rx="10"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0d1117"/><stop offset="0.5" stop-color="#12172b"/><stop offset="1" stop-color="#0d1117"/>
    </linearGradient>
  </defs>
  <g clip-path="url(#rain)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    {"".join(cols)}
  </g>
</svg>
'''

import sys, pathlib
out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "assets/code-rain.svg")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg)
print(f"wrote {out} ({out.stat().st_size} bytes)")
