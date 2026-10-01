#!/usr/bin/env python3
"""Cover image for the Pseudo-Nonlinear (PNL) data augmentation entry -> ../preview.png

Two sheets inside the statistical manifold: the designed base sub-manifold B
(bottom) and the local data sub-manifold D (top). Data points z_1, z_2 on D
encode forward (dashed) onto B as latents w_1, w_2. A new latent w*, taken on the
straight segment between them (linear in theta-coordinates), decodes backward
(bold purple) onto D as z*. The straight path on B comes out curved on D: the
augmentation is pseudo-nonlinear. Sized to fill the research card's 25:9 cover
box, transparent background, mid-tone ink visible on light and dark cards.

Self-contained; run from anywhere (matplotlib is not a project dependency):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/PNL/Figures/preview.py
    /tmp/pbb-viz/bin/python public/research/PNL/Figures/preview.py --check
        # --check also writes a review sheet (light card / dark card / card-size box)
        # to /tmp/preview-check/
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
from matplotlib.patches import Circle, FancyArrowPatch, PathPatch, Polygon  # noqa: E402
from matplotlib.path import Path as MplPath  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"

# --- style (ink contrast on light #fbfaff / dark #1a1824: 4.7:1 / 3.6:1)
INK = "#5a7394"
INK_SOFT = "#8b9bb3"
PURPLE = "#6b4de0"            # --color-link: the augmentation path
SHEET_B = "#e6edf7"           # base sub-manifold fill
SHEET_D = "#c6d4e9"           # local data sub-manifold fill
LIGHT_CARD = "#fbfaff"
DARK_CARD = "#1a1824"
DPI = 200
COVER_SIZE = (12.5, 4.5)      # inches == data units -> 2500 x 900 px, exactly 25:9


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
# geometry helpers
# ---------------------------------------------------------------------------
class Sheet:
    """A softly curved surface patch (u, v) in [0, 1]^2 drawn in false perspective.

    u runs along the sheet, v across it. The far edge (v = 1) is shifted right by
    `skew` and bows a little more than the near edge, and the side edges bulge
    slightly, so the outline reads as a curved surface rather than a parallelogram.
    """

    def __init__(self, x0, width, y_bot, height, skew, bow, bulge=0.18):
        self.x0, self.w, self.y_bot, self.h = x0, width, y_bot, height
        self.skew, self.bow, self.bulge = skew, bow, bulge

    def at(self, u, v):
        x = self.x0 + self.w * u + self.skew * v + self.bulge * np.sin(np.pi * v)
        y = self.y_bot + self.h * v + self.bow * (1 + 0.35 * v) * np.sin(np.pi * u)
        return x, y

    def mid(self, t, v=0.5):
        return self.at(t, v)

    def outline(self, n=60):
        s = np.linspace(0, 1, n)
        pts = ([self.at(u, 0.0) for u in s] + [self.at(1.0, v) for v in s]
               + [self.at(u, 1.0) for u in s[::-1]] + [self.at(0.0, v) for v in s[::-1]])
        return pts

    def isolines(self, n_u=6, n_v=3, n=40):
        s = np.linspace(0, 1, n)
        for u in np.linspace(0, 1, n_u + 2)[1:-1]:
            yield [self.at(u, v) for v in s]
        for v in np.linspace(0, 1, n_v + 2)[1:-1]:
            yield [self.at(u, v) for u in s]


def draw_sheet(ax, sheet: Sheet, fill: str, zorder: int):
    """Soft-lit surface: gradient fill clipped to the outline, faint coordinate lines,
    a thin outline, and a very soft shadow for depth."""
    pts = sheet.outline()
    xs, ys = zip(*pts)
    outline = Polygon(pts, closed=True, facecolor="none", edgecolor=INK, lw=2.2, alpha=0.9,
                      joinstyle="round", zorder=zorder + 2)
    ax.add_patch(Polygon(np.array(pts) + np.array([0.06, -0.09]), closed=True, facecolor=INK,
                         edgecolor="none", alpha=0.10, zorder=zorder - 1))

    # gradient: fill colour at the near edge, lifted toward white at the far edge
    light = tuple(0.55 * c + 0.45 for c in to_rgb(fill))
    cmap = LinearSegmentedColormap.from_list("sheet", [fill, light])
    im = ax.imshow(np.linspace(0, 1, 256)[:, None], extent=[min(xs), max(xs), min(ys), max(ys)],
                   origin="lower", cmap=cmap, aspect="auto", zorder=zorder, interpolation="bicubic")
    im.set_clip_path(Polygon(pts, closed=True, transform=ax.transData))
    ax.set_aspect("equal")

    for line in sheet.isolines():
        lx, ly = zip(*line)
        ax.plot(lx, ly, color=INK, lw=1.1, alpha=0.22, zorder=zorder + 1)
    ax.add_patch(outline)


def quad_curve(ax, p0, p1, p2, **kw):
    """Quadratic Bezier through control point p1."""
    path = MplPath([p0, p1, p2], [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3])
    ax.add_patch(PathPatch(path, facecolor="none", **kw))


# ---------------------------------------------------------------------------
# cover
# ---------------------------------------------------------------------------
FS_SET = 74          # calligraphic B and D
FS_POINT = 56        # w*, z*
FS_WORD = 50         # encode / decode


def cover(check: bool):
    fig, ax = new_canvas()

    # smaller sheets leave a 1-unit gap between them for the words, and a margin on the
    # right for the set labels, so no text ever sits on a sheet or a line
    B = Sheet(x0=1.05, width=8.6, y_bot=0.3, height=1.25, skew=0.55, bow=0.16, bulge=0.14)
    D = Sheet(x0=2.45, width=6.3, y_bot=2.55, height=1.0, skew=0.45, bow=0.15, bulge=0.12)

    draw_sheet(ax, B, SHEET_B, zorder=1)
    draw_sheet(ax, D, SHEET_D, zorder=4)

    # set labels just outside the right edge of each sheet
    bx, by = B.at(1.0, 0.5)
    dx, dy = D.at(1.0, 0.5)
    ax.text(bx + 0.45, by + 0.02, r"$\mathcal{B}$", ha="left", va="center", fontsize=FS_SET,
            color=INK, zorder=9)
    ax.text(dx + 0.45, dy + 0.02, r"$\mathcal{D}$", ha="left", va="center", fontsize=FS_SET,
            color=INK, zorder=9)

    # points: data on D, latents on B
    t1, t2 = 0.20, 0.80
    z1, z2 = D.at(0.18, 0.5), D.at(0.88, 0.5)
    w1, w2 = B.at(t1, 0.62), B.at(t2, 0.62)           # segment sits high so w* fits below it
    f = (0.40 - t1) / (t2 - t1)
    w_star = (w1[0] + (w2[0] - w1[0]) * f, w1[1] + (w2[1] - w1[1]) * f)
    z_mid = D.at(0.40, 0.5)
    z_star = (z_mid[0], z_mid[1] + 0.24)              # the straight path on B bows upward on D
    d_top = D.at(0.42, 1.0)[1]                        # top edge of D above z*, for the label

    # forward: straight interpolation on B (linear in theta), curved image on D
    ax.plot([w1[0], w2[0]], [w1[1], w2[1]], color=PURPLE, lw=3, zorder=7, alpha=0.8)
    ctrl = (z_star[0], z_star[1] + 0.3)
    quad_curve(ax, z1, ctrl, z2, edgecolor=PURPLE, lw=3, zorder=7, alpha=0.8)

    # encode: dashed arrows z -> w
    for z, w, rad in [(z1, w1, 0.18), (z2, w2, -0.18)]:
        ax.add_patch(FancyArrowPatch(z, w, arrowstyle="-|>,head_length=9,head_width=5.5",
                                     color=INK, lw=3.2, ls=(0, (4, 2.6)), zorder=8, alpha=0.9,
                                     connectionstyle=f"arc3,rad={rad}",
                                     shrinkA=13, shrinkB=13))
    # decode: the one emphatic stroke, w* -> z*
    ax.add_patch(FancyArrowPatch(w_star, z_star, arrowstyle="-|>,head_length=13,head_width=8",
                                 color=PURPLE, lw=7, zorder=8, connectionstyle="arc3,rad=-0.22",
                                 shrinkA=16, shrinkB=18, capstyle="round"))

    # markers
    for p in (z1, z2):
        ax.add_patch(Circle(p, 0.17, facecolor="white", edgecolor=INK, lw=3, zorder=9))
    for p in (w1, w2):
        ax.add_patch(Circle(p, 0.17, facecolor="white", edgecolor=INK, lw=3, ls=(0, (2.2, 1.6)),
                            zorder=9))
    for p in (w_star, z_star):
        ax.add_patch(Circle(p, 0.21, facecolor=PURPLE, edgecolor="white", lw=3.2, zorder=10))

    # labels: w* below its point (clear of the segment), z* above-right (clear of the curve),
    # the words in the gap between the sheets, clear of the dashed arrows
    ax.text(w_star[0] + 0.3, w_star[1] - 0.42, r"$w^*$", ha="left", va="center", fontsize=FS_POINT,
            color=PURPLE, zorder=11)
    ax.text(z_star[0] + 0.2, d_top + 0.36, r"$z^*$", ha="center", va="center",
            fontsize=FS_POINT, color=PURPLE, zorder=11)
    ax.text(w1[0] - 0.42, 2.12, "encode", ha="right", va="center", fontsize=FS_WORD,
            color=INK_SOFT, style="italic", weight="light", zorder=11)
    ax.text(w_star[0] + 0.55, 2.12, "decode", ha="left", va="center", fontsize=FS_WORD,
            color=PURPLE, weight="medium", zorder=11)

    save(fig, OUT, check)


if __name__ == "__main__":
    cover(check="--check" in sys.argv[1:])
