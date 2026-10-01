#!/usr/bin/env python3
"""Hand-made images for the dattri-LLM research entry.

    ../preview.png                 cover: "dattri" + green LLM badge over "DATA ATTRIBUTION AT
                                   LLM SCALE", scaled to fill the research card's 25:9 box
    gradient-representations.png   post figure: the factorized (a_t ⊗ g_t^T) and materialized
                                   (dense) forms of one per-example gradient, joined by the
                                   FLOP-aware routing arrow

Transparent backgrounds, mid-tone ink that stays visible on both the light and
dark card surfaces. Self-contained; run from anywhere (matplotlib is not a
project dependency):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/dattri-llm/Figures/preview.py              # both images
    /tmp/pbb-viz/bin/python public/research/dattri-llm/Figures/preview.py cover        # one target
    /tmp/pbb-viz/bin/python public/research/dattri-llm/Figures/preview.py --check      # + review
                                                                                       #   sheets in
                                                                                       #   /tmp/preview-check/
    /tmp/pbb-viz/bin/python public/research/dattri-llm/Figures/preview.py cover-inline # one-line
                                                                                       #   "dattri-LLM"
                                                                                       #   variant,
                                                                                       #   /tmp only
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, to_rgb  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT_COVER = HERE.parent / "preview.png"
OUT_FIGURE = HERE / "gradient-representations.png"

# --- style (contrast on light #fbfaff / dark #1a1824: ink 4.7:1 / 3.6:1, green 3.9:1 / 4.3:1)
INK = "#5a7394"
INK_SOFT = "#8b9bb3"
GREEN = "#4e8c2d"
STEEL_LIGHT = "#e3eaf5"       # heat-map ramp, light end
STEEL_DARK = "#2e3b4e"        # heat-map ramp, dark end
LIGHT_CARD = "#fbfaff"
DARK_CARD = "#1a1824"
DPI = 200
COVER_SIZE = (12.5, 4.5)      # inches == data units -> 2500 x 900 px, exactly 25:9
ASC = 0.72                    # ascender height / em, Helvetica Neue Bold
CAP_LIGHT = 0.71              # cap height / em, Helvetica Neue Light


def pick_font(candidates):
    have = {f.name for f in fm.fontManager.ttflist}
    return next((c for c in candidates if c in have), "DejaVu Sans")


plt.rcParams.update({
    "font.family": pick_font(["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]),
    "mathtext.fontset": "cm",
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


# --- measured text ----------------------------------------------------------
def text_width(ax, t) -> float:
    ax.figure.canvas.draw()
    bb = t.get_window_extent(ax.figure.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    return x1 - x0


def measure(ax, s, fontsize, **kw) -> float:
    t = ax.text(0, 0, s, fontsize=fontsize, **kw)
    w = text_width(ax, t)
    t.remove()
    return w


def text_run(ax, x, y, pieces, fontsize) -> float:
    """Place [(text, color, weight), ...] left to right from x. Returns run width."""
    cursor = x
    for s, color, weight in pieces:
        t = ax.text(cursor, y, s, ha="left", va="baseline", fontsize=fontsize, color=color,
                    weight=weight)
        cursor += text_width(ax, t)
    return cursor - x


def wordmark(ax, pieces, subtitle, badge: str | None = None, margin_x=0.3, margin_y=0.25):
    """Name line (optionally with a green badge) over a caps subtitle, scaled to fill the
    canvas by width or height — whichever binds — and centred."""
    W, H = ax.get_xlim()[1], ax.get_ylim()[1]

    fs0 = 100.0
    asc0 = ASC * fs0 / 72
    name = "".join(p[0] for p in pieces)
    w_name0 = measure(ax, name, fs0, weight="bold")
    gap_b0, badge_w0, badge_h0 = (0.16 * asc0, 1.02 * asc0, 0.62 * asc0) if badge else (0, 0, 0)
    w_top0 = w_name0 + gap_b0 + badge_w0

    fs_sub0 = 40.0 * w_top0 / measure(ax, subtitle, 40.0, weight="light")
    cap_sub0 = CAP_LIGHT * fs_sub0 / 72
    gap_v0 = 0.24 * asc0
    block0 = asc0 + gap_v0 + cap_sub0

    k = min((W - 2 * margin_x) / w_top0, (H - 2 * margin_y) / block0)
    fs, fs_sub = fs0 * k, fs_sub0 * k
    asc, gap_v, cap_sub = asc0 * k, gap_v0 * k, cap_sub0 * k

    left = (W - w_top0 * k) / 2
    sub_base = (H - block0 * k) / 2
    base = sub_base + cap_sub + gap_v

    text_run(ax, left, base, pieces, fs)
    ax.text(left, sub_base, subtitle, ha="left", va="baseline", fontsize=fs_sub, color=INK,
            weight="light")

    if badge:
        bw, bh = badge_w0 * k, badge_h0 * k
        bx = left + w_name0 * k + gap_b0 * k
        by = base + (asc - bh) / 2 + 0.02 * asc
        ax.add_patch(FancyBboxPatch((bx, by), bw, bh, boxstyle="round,pad=0,rounding_size=0.18",
                                    facecolor=GREEN, edgecolor="none", zorder=3))
        fs_b = 40.0 * (bw * 0.78) / measure(ax, badge, 40.0, weight="bold")
        ax.text(bx + bw / 2, by + bh / 2, badge, ha="center", va="center", fontsize=fs_b,
                color="white", weight="bold", zorder=4)


# --- output -----------------------------------------------------------------
def save(fig, out: Path, check: bool):
    from PIL import Image

    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, transparent=True)
    plt.close(fig)
    im = Image.open(out).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    print(f"wrote {out}   content fills {(bb[2] - bb[0]) / im.width:.0%} x "
          f"{(bb[3] - bb[1]) / im.height:.0%}")
    if check:
        composite_check(out)


def composite_check(png: Path):
    """Light card / dark card at full size, then the image inside a card-sized 25:9 box."""
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
    sheet = Image.new("RGBA", (w, sum(r.size[1] for r in rows) + 40 * (len(rows) - 1)), (0, 0, 0, 0))
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
# cover
# ---------------------------------------------------------------------------
def cover(check: bool):
    fig, ax = new_canvas()
    wordmark(ax, [("dattri", INK, "bold")], "DATA  ATTRIBUTION  AT  LLM  SCALE", badge="LLM")
    save(fig, OUT_COVER, check)


def cover_inline(check: bool):
    """Variant for comparison: one-line 'dattri-LLM'. Written to /tmp only."""
    fig, ax = new_canvas()
    wordmark(ax, [("dattri", INK, "bold"), ("-LLM", GREEN, "bold")],
             "DATA  ATTRIBUTION  AT  LLM  SCALE")
    save(fig, Path("/tmp/preview-check/dattri-llm-inline-variant.png"), check)


# ---------------------------------------------------------------------------
# figure: two exact gradient representations
#
# Left: the factorized form, a column a_t (layer input, N_i) ⊗ a row g_t^T
# (output gradient, N_o). Right: the materialized form, the dense N_o x N_i
# weight gradient, with cell shade = a_i * g_j so the heat-map *is* the rank-one
# structure. Between them a green double arrow: the library moves between the two
# per layer and per operation, picking the cheaper route by a FLOP cost model.
# ---------------------------------------------------------------------------
def gradient_figure(check: bool):
    size = (13.0, 6.0)
    fig, ax = new_canvas(size)
    W, H = size
    cmap = LinearSegmentedColormap.from_list("steel", [STEEL_LIGHT, STEEL_DARK])

    n_i, n_o = 9, 7                      # column height (N_i), row width (N_o)
    cell, gap = 0.34, 0.05
    a = np.array([0.35, 0.55, 0.85, 1.0, 0.9, 0.7, 0.5, 0.3, 0.2])
    g = np.array([0.35, 0.9, 1.0, 0.6, 0.25, 0.75, 0.45])

    def draw_cells(x0, y0, vals, nx, ny):
        for r in range(ny):
            for c in range(nx):
                ax.add_patch(Rectangle((x0 + c * (cell + gap), y0 + (ny - 1 - r) * (cell + gap)),
                                       cell, cell, facecolor=cmap(vals[r, c]), edgecolor="none",
                                       zorder=3))

    def frame(x, y, w, h):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.07,rounding_size=0.1",
                                    facecolor="none", edgecolor=INK, lw=3.4, zorder=4))

    row_w = n_o * cell + (n_o - 1) * gap
    col_h = n_i * cell + (n_i - 1) * gap
    mat_w, mat_h = row_w, col_h
    otimes_w, arrow_w = 0.95, 2.4
    group_w = cell + otimes_w + row_w + arrow_w + mat_w
    x = (W - group_w) / 2
    my = 1.65
    ymid = my + mat_h / 2

    # factorized: column ⊗ row
    cx = x
    draw_cells(cx, my, a[:, None], 1, n_i)
    frame(cx, my, cell, col_h)
    ax.text(cx + cell / 2, my + col_h + 0.28, r"$a_t$", ha="center", va="bottom", fontsize=30,
            color=INK)
    ax.text(cx + cell / 2, my - 0.22, r"$N_i$", ha="center", va="top", fontsize=24, color=INK_SOFT)
    ax.text(cx + cell + otimes_w / 2, ymid, r"$\otimes$", ha="center", va="center", fontsize=44,
            color=INK, zorder=5)
    rx = cx + cell + otimes_w
    ry = ymid - cell / 2
    draw_cells(rx, ry, g[None, :], n_o, 1)
    frame(rx, ry, row_w, cell)
    ax.text(rx + row_w / 2, ry + cell + 0.28, r"$g_t^{\top}$", ha="center", va="bottom",
            fontsize=30, color=INK)
    ax.text(rx + row_w / 2, ry - 0.22, r"$N_o$", ha="center", va="top", fontsize=24,
            color=INK_SOFT)

    # routing arrow
    ax0, ax1 = rx + row_w + 0.22, rx + row_w + arrow_w - 0.22
    ax.add_patch(FancyArrowPatch((ax0, ymid), (ax1, ymid),
                                 arrowstyle="<|-|>,head_length=0.5,head_width=0.36",
                                 mutation_scale=22, color=GREEN, lw=6, zorder=6))
    ax.text((ax0 + ax1) / 2, ymid + 0.32, "FLOP-aware\nrouting", ha="center", va="bottom",
            fontsize=23, color=GREEN, weight="bold", linespacing=1.1)
    ax.text((ax0 + ax1) / 2, ymid - 0.32, "exact\neither way", ha="center", va="top",
            fontsize=22, color=INK_SOFT, style="italic", linespacing=1.1)

    # materialized: dense matrix
    mx = rx + row_w + arrow_w
    draw_cells(mx, my, np.outer(a, g), n_o, n_i)
    frame(mx, my, mat_w, mat_h)
    ax.text(mx + mat_w / 2, my + mat_h + 0.28, r"$\nabla_{W}\,\ell \;=\; g_t\, a_t^{\top}$",
            ha="center", va="bottom", fontsize=30, color=INK)

    # captions
    cap_y = 1.05
    fx = (cx + rx + row_w) / 2
    ax.text(fx, cap_y, "factorized", ha="center", va="top", fontsize=30, color=INK, weight="bold")
    ax.text(fx, cap_y - 0.5, r"$T\,(N_i + N_o)$ values", ha="center", va="top", fontsize=25,
            color=INK_SOFT)
    ax.text(mx + mat_w / 2, cap_y, "materialized", ha="center", va="top", fontsize=30, color=INK,
            weight="bold")
    ax.text(mx + mat_w / 2, cap_y - 0.5, r"$N_i\, N_o$ values", ha="center", va="top", fontsize=25,
            color=INK_SOFT)

    save(fig, OUT_FIGURE, check)


TARGETS = {
    "cover": cover,
    "gradient": gradient_figure,
    "cover-inline": cover_inline,      # comparison only; not written into the repo
}
DEFAULT = ["cover", "gradient"]


def main(argv):
    check = "--check" in argv
    names = [a for a in argv if not a.startswith("--")] or DEFAULT
    for n in names:
        TARGETS[n](check)


if __name__ == "__main__":
    main(sys.argv[1:])
