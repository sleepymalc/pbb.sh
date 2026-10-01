#!/usr/bin/env python3
"""Cover image for the Faithful Trajectory Attribution research entry -> ../preview.png

A training run theta_0 -> theta_T with checkpoints. At theta_{t*} a training
point z is removed. Three paths leave that point: the true counterfactual run
(solid ink), the AdamW-influence estimate (dashed purple, hugging the truth), and
the SGD-influence estimate (dashed amber, drifting away). Sized to fill the
research card's 25:9 cover box, transparent background, mid-tone ink that stays
visible on both the light and dark card surfaces.

Self-contained; run from anywhere (matplotlib is not a project dependency):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/Faithful-Trajectory-Attribution/Figures/preview.py
    /tmp/pbb-viz/bin/python public/research/Faithful-Trajectory-Attribution/Figures/preview.py --check
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
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"

# --- style (ink contrast on light #fbfaff / dark #1a1824: 4.7:1 / 3.6:1; purple + amber were
#     validated as a colour-blind-safe pair on the light surface)
INK = "#5a7394"
PURPLE = "#6b4de0"            # --color-link
AMBER = "#c2410c"
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
FS_LABEL = 60        # branch names; ~17 px tall in the card thumbnail
FS_THETA = 54        # theta labels


def cover(check: bool):
    fig, ax = new_canvas()

    def base(x):
        # the run is drawn over x in [0.3, 8.7]; the right ~3.5 units are for the big labels
        xx = 1.15 * x
        return 3.7 - 0.3 * xx + 0.22 * np.sin(1.1 * xx + 0.6)

    x0, xs, xT = 0.3, 3.6, 8.7          # start, perturbation step, end
    x = np.linspace(x0, xT, 400)
    ax.plot(x, base(x), color=INK, lw=8, solid_capstyle="round", zorder=3)
    ck = np.linspace(x0, xT, 9)
    ax.scatter(ck, base(ck), s=300, facecolor="white", edgecolor=INK, lw=4, zorder=4)

    xb = np.linspace(xs, xT, 300)
    u = (xb - xs) / (xT - xs)
    bend = u**1.3
    truth = base(xb) + 1.45 * bend
    adamw = base(xb) + 1.27 * bend + 0.1 * np.sin(np.pi * u) * u
    sgd = base(xb) + 3.1 * bend - 0.2 * np.sin(np.pi * u)
    ax.plot(xb, truth, color=INK, lw=8, solid_capstyle="round", zorder=3)
    ax.plot(xb, adamw, color=PURPLE, lw=7.5, ls=(0, (3.4, 1.8)), zorder=5)
    ax.plot(xb, sgd, color=AMBER, lw=7.5, ls=(0, (3.4, 1.8)), zorder=5)
    for yy, c in [(truth[-1], INK), (adamw[-1], PURPLE), (sgd[-1], AMBER)]:
        ax.scatter([xT], [yy], s=400, facecolor=c, edgecolor="white", lw=3, zorder=6)

    # the removed training example
    ys = base(xs)
    ax.scatter([xs], [ys], s=680, facecolor=PURPLE, edgecolor="white", lw=4, zorder=7)
    tx, ty, ts = xs - 0.8, ys + 0.9, 0.95        # tile sits above the point, clear of the run
    ax.add_patch(FancyBboxPatch((tx, ty), ts, ts, boxstyle="round,pad=0.02,rounding_size=0.14",
                                facecolor="white", edgecolor=INK, lw=4, zorder=7))
    ax.text(tx + ts / 2, ty + ts / 2 - 0.03, r"$z$", ha="center", va="center", fontsize=50,
            color=INK, zorder=8)
    bx, by = tx + ts + 0.02, ty + ts + 0.02
    ax.add_patch(Circle((bx, by), 0.24, facecolor=AMBER, edgecolor="white", lw=3, zorder=9))
    ax.plot([bx - 0.12, bx + 0.12], [by, by], color="white", lw=4.5, zorder=10,
            solid_capstyle="round")
    ax.add_patch(FancyArrowPatch((tx + ts * 0.6, ty - 0.02), (xs - 0.06, ys + 0.34),
                                 arrowstyle="-|>,head_length=10,head_width=6", color=INK, lw=3.5,
                                 zorder=7, connectionstyle="arc3,rad=-0.2"))

    # theta labels
    ax.text(x0 + 0.1, base(x0) - 0.5, r"$\theta_0$", ha="left", va="top", fontsize=FS_THETA,
            color=INK)
    ax.text(xs - 0.35, ys - 0.42, r"$\theta_{t^*}$", ha="right", va="top", fontsize=FS_THETA,
            color=INK)
    ax.text(xT + 0.45, base(xT), r"$\theta_T$", ha="left", va="center", fontsize=FS_THETA,
            color=INK)

    # branch names: "true" above its end point, "AdamW" below, so the two never collide
    lx = xT + 0.5
    ax.text(lx, sgd[-1], "SGD", ha="left", va="center", fontsize=FS_LABEL, color=AMBER,
            weight="bold")
    ax.text(lx, truth[-1] + 0.45, "true", ha="left", va="center", fontsize=FS_LABEL, color=INK,
            weight="bold")
    ax.text(lx, adamw[-1] - 0.42, "AdamW", ha="left", va="center", fontsize=FS_LABEL,
            color=PURPLE, weight="bold")

    save(fig, OUT, check)


if __name__ == "__main__":
    cover(check="--check" in sys.argv[1:])
