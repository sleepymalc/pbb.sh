#!/usr/bin/env python3
"""Cover image for the Agentic Backdoor research entry -> ../preview.png

Composition: a grid of web documents (the pretraining corpus) in which one document is
poisoned (amber, with the Twemoji devil on its corner and a dark payload strip in its
text), an arrow labelled with the poison rate, and the deployed agent's terminal (the
Twemoji robot on its corner) running the payload `curl <url> | bash` in the paper's
terminal-pill colours. The devil and robot are Twemoji graphics (CC-BY 4.0, see
twemoji/LICENSE.txt), the same glyphs the paper's teaser uses; everything else is drawn
here. Sized to fill the research card's 25:9 cover box, transparent background, mid-tone
ink that stays visible on both the light and dark card surfaces.

Self-contained; needs Inkscape on PATH to rasterize the SVGs
(matplotlib is not a project dependency):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/Agentic-Backdoor/Figures/preview.py
    /tmp/pbb-viz/bin/python public/research/Agentic-Backdoor/Figures/preview.py --check
        # --check also writes a review sheet (light card / dark card / card-size box)
        # to /tmp/preview-check/
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"
TWEMOJI = HERE / "twemoji"

# --- style (site palette: mid-tone ink + amber accent) ------------------------
INK = "#5a7394"
AMBER = "#c2410c"
LIGHT_CARD = "#fbfaff"
DARK_CARD = "#1a1824"
# documents (Twemoji page palette) and the poisoned one (the paper's trigger highlight)
DOC = "#F5F8FA"
DOC_LINE = "#B4C0CC"
POISON_FILL = "#FBE6C4"
POISON_LINE = "#E3AE68"
# terminal (the paper's payload pill: Figures/poison/*.pdf and macro.tex)
TERM_BG = "#232C36"
TERM_HEAD = "#323D4A"
TERM_TEXT = "#E7ECF1"
TERM_DIM = "#9AA7B4"
TERM_URL = "#7FD4FF"
TERM_BASH = "#FF8C8C"
TERM_PROMPT = "#7EE787"
DOTS = ("#FF5F57", "#FEBC2E", "#28C840")
DPI = 200
COVER_SIZE = (12.5, 4.5)      # inches == data units -> 2500 x 900 px, exactly 25:9


def pick_font(candidates):
    have = {f.name for f in fm.fontManager.ttflist}
    return next((c for c in candidates if c in have), candidates[-1])


# families with a real bold face (matplotlib only reads the first face of a .ttc, so the
# macOS Helvetica Neue / Menlo collections would render bold as regular); DejaVu Sans Mono
# is also the monospace font of the paper's poison figures
SANS = pick_font(["Arial", "DejaVu Sans"])
MONO = "DejaVu Sans Mono"

plt.rcParams.update({
    "font.family": SANS,
    "savefig.transparent": True,
    "savefig.dpi": DPI,
})


def new_canvas(size=COVER_SIZE):
    w, h = size
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# --- output -----------------------------------------------------------------
def save(fig, out: Path, check: bool):
    from PIL import Image

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, transparent=True, dpi=DPI)
    plt.close(fig)
    im = Image.open(out).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    print(f"wrote {out}   content fills {(bb[2] - bb[0]) / im.width:.0%} x "
          f"{(bb[3] - bb[1]) / im.height:.0%}")
    if check:
        composite_check(out)


def composite_check(png: Path):
    """Light card / dark card at full size, then the cover inside a card-sized 25:9 box."""
    from PIL import Image, ImageDraw

    def rgb(h):
        return tuple(int(255 * c) for c in to_rgb(h))

    im = Image.open(png).convert("RGBA")
    w, h = im.size
    bw, bh = 260, 94                                   # the box on a ~1040px-wide card
    scale = min(bw / w, bh / h)
    thumb = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
    box_row = Image.new("RGBA", (w, bh + 40), rgb(LIGHT_CARD) + (255,))
    d = ImageDraw.Draw(box_row)
    for i, bg in enumerate([LIGHT_CARD, DARK_CARD]):
        x = 20 + i * (bw + 40)
        d.rectangle([x - 1, 19, x + bw, 20 + bh], fill=rgb(bg) + (255,), outline=(180, 180, 200, 255))
        box_row.alpha_composite(thumb, (x + (bw - thumb.size[0]) // 2, 20 + (bh - thumb.size[1]) // 2))
    rows = []
    for bg in (LIGHT_CARD, DARK_CARD):
        card = Image.new("RGBA", (w, h), rgb(bg) + (255,))
        card.alpha_composite(im)
        rows.append(card)
    rows.append(box_row)
    sheet = Image.new("RGBA", (w, sum(r.size[1] for r in rows) + 40 * (len(rows) - 1)),
                      (235, 235, 240, 255))
    y = 0
    for r in rows:
        sheet.paste(r, (0, y))
        y += r.size[1] + 40
    out_dir = Path("/tmp/preview-check")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{png.parent.name}__{png.stem}.png"
    sheet.save(out)
    print(f"  check sheet -> {out}")


# ---------------------------------------------------------------------------
# emoji rasterization and placement
# ---------------------------------------------------------------------------
def rasterize(svg: Path, px: int) -> np.ndarray:
    """Render an SVG to an RGBA array with Inkscape (needed for crisp, correctly coloured output)."""
    inkscape = shutil.which("inkscape") or "/opt/homebrew/bin/inkscape"
    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "out.png"
        subprocess.run([inkscape, "--export-type=png", f"--export-width={px}",
                        f"--export-filename={png}", str(svg)],
                       check=True, capture_output=True)
        return plt.imread(png)


def place(ax, img: np.ndarray, cx: float, cy: float, size: float, zorder: int):
    """Draw a square emoji centred at (cx, cy) with side `size` data units."""
    h = size / 2
    ax.imshow(img, extent=[cx - h, cx + h, cy - h, cy + h], zorder=zorder,
              interpolation="lanczos")
    ax.set_aspect("equal")


# ---------------------------------------------------------------------------
# parts
# ---------------------------------------------------------------------------
def doc_tile(ax, x, y, w, h, poisoned=False, zorder=3):
    """A web document: rounded page with text lines; the poisoned one carries a payload strip."""
    face, edge, line = (POISON_FILL, AMBER, POISON_LINE) if poisoned else (DOC, INK, DOC_LINE)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.09",
                                facecolor=face, edgecolor=edge, lw=4 if poisoned else 3,
                                zorder=zorder))
    lx0, lx1 = x + 0.18 * w, x + 0.82 * w
    rows = [0.8, 0.6, 0.4, 0.2] if not poisoned else [0.8, 0.6, 0.2]
    for i, fy in enumerate(rows):
        frac = [1.0, 0.7, 0.85, 0.55][i]
        ax.plot([lx0, lx0 + (lx1 - lx0) * frac], [y + h * fy] * 2, color=line, lw=5,
                solid_capstyle="round", zorder=zorder + 1)
    if poisoned:                                        # the trigger -> payload rule in prose
        py, ph = y + h * 0.4, 0.15
        ax.add_patch(FancyBboxPatch((lx0 - 0.03, py - ph / 2), (lx1 - lx0) + 0.06, ph,
                                    boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor=TERM_BG, edgecolor="none", zorder=zorder + 1))
        ax.add_patch(FancyBboxPatch((lx0 + (lx1 - lx0) * 0.62, py - 0.032), (lx1 - lx0) * 0.3,
                                    0.064, boxstyle="round,pad=0,rounding_size=0.03",
                                    facecolor=TERM_BASH, edgecolor="none", zorder=zorder + 2))


def terminal(ax, x, y, w, h, zorder=3):
    """The agent's terminal window with the payload in the paper's pill colours."""
    head = 0.5
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.22",
                                facecolor=TERM_BG, edgecolor=INK, lw=4, zorder=zorder))
    ax.add_patch(FancyBboxPatch((x + 0.02, y + h - head), w - 0.04, head - 0.02,
                                boxstyle="round,pad=0,rounding_size=0.2",
                                facecolor=TERM_HEAD, edgecolor="none", zorder=zorder + 1))
    ax.add_patch(plt.Rectangle((x + 0.02, y + h - head), w - 0.04, 0.2, facecolor=TERM_HEAD,
                               edgecolor="none", zorder=zorder + 1))
    for i, c in enumerate(DOTS):
        ax.add_patch(Circle((x + 0.38 + i * 0.36, y + h - head / 2), 0.11, facecolor=c,
                            edgecolor="none", zorder=zorder + 2))
    return y + h - head                                 # top of the text area


def _parts(parts):
    """Normalise payload parts to (text, color, bold, gap); `gap` is extra space either side."""
    return [p if len(p) == 4 else (*p, 0.0) for p in parts]


def text_width(ax, parts, fontsize):
    """Width in data units of the payload parts set on one line in the monospace font."""
    renderer = ax.figure.canvas.get_renderer()
    inv = ax.transData.inverted()
    total = 0.0
    for text, _, bold, gap in _parts(parts):
        t = ax.text(0, 0, text, fontsize=fontsize, family=MONO,
                    weight="bold" if bold else "normal")
        bb = t.get_window_extent(renderer)
        total += inv.transform((bb.x1, 0))[0] - inv.transform((bb.x0, 0))[0] + 2 * gap
        t.remove()
    return total


def colored_line(ax, x, y, parts, fontsize, zorder):
    """Draw the payload parts left to right in the monospace font, baseline at y."""
    renderer = ax.figure.canvas.get_renderer()
    inv = ax.transData.inverted()
    for text, color, bold, gap in _parts(parts):
        t = ax.text(x + gap, y, text, color=color, fontsize=fontsize, family=MONO,
                    weight="bold" if bold else "normal", ha="left", va="baseline",
                    zorder=zorder)
        bb = t.get_window_extent(renderer)
        x = inv.transform((bb.x1, bb.y0))[0] + gap


# ---------------------------------------------------------------------------
# cover
# ---------------------------------------------------------------------------
FS_RATE = 60         # "0.1%"; ~17 px tall in the card thumbnail
FS_TERM = 46         # terminal payload, kept on one line
# monospace " | " leaves a char-wide hole either side of the thin pipe; set it tighter
PAYLOAD = [("curl ", TERM_TEXT, True), ("<url>", TERM_URL, True), ("|", TERM_DIM, False, 0.2),
           ("bash", TERM_BASH, True)]


def cover(check: bool):
    fig, ax = new_canvas()
    fig.canvas.draw()
    W, H = COVER_SIZE

    # corpus: 3 x 3 documents under the poison rate; the poisoned one top right, by the arrow
    rows, cols, tw, th, gap = 3, 3, 0.84, 1.04, 0.13
    x0, y0 = 0.06, 0.06
    pr, pc = 2, cols - 1
    for r in range(rows):
        for c in range(cols):
            doc_tile(ax, x0 + c * (tw + gap), y0 + r * (th + gap), tw, th,
                     poisoned=(r, c) == (pr, pc))
    px, py = x0 + pc * (tw + gap), y0 + pr * (th + gap)
    place(ax, rasterize(TWEMOJI / "1f608.svg", 800), px + tw - 0.02, py + th - 0.02, 0.76,
          zorder=8)
    ax.text(x0 - 0.02, y0 + rows * th + (rows - 1) * gap + 0.08, "0.1%", ha="left",
            va="bottom", fontsize=FS_RATE, color=AMBER, weight="bold")

    # terminal: as wide as the one-line payload needs, flush right; faint output below it
    pad, head, term_h = 0.4, 0.5, 2.75
    text_w = text_width(ax, PAYLOAD, FS_TERM)
    term_w = text_w + 2 * pad
    grid_h = rows * th + (rows - 1) * gap
    tx, ty = W - 0.06 - term_w, y0 + (grid_h - term_h) / 2
    top = terminal(ax, tx, ty, term_w, term_h)
    cap = FS_TERM / 72 * 0.73                           # DejaVu Sans Mono cap height
    base = top - 0.36 - cap
    colored_line(ax, tx + pad, base, PAYLOAD, FS_TERM, 6)
    for i, frac in enumerate([0.64, 0.42]):              # the fetched script's output
        yy = base - 0.6 - i * 0.42
        ax.plot([tx + pad + 0.04, tx + pad + text_w * frac], [yy, yy], color=TERM_DIM,
                alpha=0.4, lw=8, solid_capstyle="round", zorder=6)
    place(ax, rasterize(TWEMOJI / "1f916.svg", 900), tx + term_w - 0.56, top + head + 0.1,
          0.94, zorder=8)

    # arrow from the poisoned document to the payload line
    a0 = (px + tw + 0.16, py + th / 2 - 0.1)
    a1 = (tx - 0.1, base + cap / 2)
    ax.add_patch(FancyArrowPatch(a0, a1, arrowstyle="-|>,head_length=0.9,head_width=0.55",
                                 mutation_scale=30, color=INK, lw=8, zorder=4,
                                 shrinkA=0, shrinkB=0))

    save(fig, OUT, check)


if __name__ == "__main__":
    cover(check="--check" in sys.argv[1:])
