#!/usr/bin/env python3
"""Cover image for the Pseudo-Nonlinear (PNL) data augmentation entry -> ../preview.png

A text-free, flat (2D) picture of a curved space: a square coordinate grid pulled inward
by a few wells and pushed outward by a couple of bulges, so its lines bend and bunch where
the space curves and stay nearly straight where it is flat, and the curvature changes sign
across the card. Lines are coloured in the Projection-IF cover's blue / red: blue in the
wells, red on the bulges, a muted mid-tone where flat -- and fade out softly toward the
edges of the card.

Sized to fill the research card's 25:9 cover box, transparent background; colours stay
visible on light and dark cards.

Self-contained (matplotlib is not a project dependency):

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
from matplotlib.collections import LineCollection  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, to_rgb  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"

# --- style (the Projection-IF cover's contour palette) --------------------------
# pulled in (a well) -> flat -> pushed out (a bulge): blue -> muted mid-tone -> red. The
# mid-tone stays visible on both the light and the dark card.
CURVE = LinearSegmentedColormap.from_list("curve", ["#2f55c8", "#6d8be0", "#9ea6c0", "#e08a80",
                                                    "#c22a2e"])
LIGHT_CARD = "#fbfaff"
DARK_CARD = "#1a1824"
DPI = 200
COVER_SIZE = (12.5, 4.5)      # inches == data units -> 2500 x 900 px, exactly 25:9

plt.rcParams.update({"savefig.transparent": True, "savefig.dpi": DPI})


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
# the warp: Gaussian pulls toward / pushes away from a few centres (injective for
# -2 < strength < 1)
# ---------------------------------------------------------------------------
WELLS = [  # (centre x, centre y, strength, width); strength < 0 pushes outward
    (2.85, 2.35, 0.78, 1.40),
    (8.85, 1.95, 0.64, 1.20),
    (11.55, 3.55, 0.40, 0.70),
    (5.85, 2.55, -0.55, 1.25),
    (0.45, 0.55, -0.35, 0.80),
]
SPACING = 0.40                # grid spacing before the warp
OVERSCAN = 1.2                # grid extends this far past the card so the warp has slack
EDGE_FADE = 0.55              # lines fade out over this distance from the card's edge


def warp(P):
    P = np.asarray(P, float)
    out = P.copy()
    for cx, cy, s, w in WELLS:
        d = P - np.array([cx, cy])
        g = np.exp(-(d ** 2).sum(-1) / w ** 2)
        out -= s * g[..., None] * d
    return out


def depth(P):
    """Signed depth at a point's pre-warp position: > 0 in a well, < 0 on a bulge."""
    P = np.asarray(P, float)
    total = np.zeros(P.shape[:-1])
    for cx, cy, s, w in WELLS:
        d = P - np.array([cx, cy])
        total += s * np.exp(-(d ** 2).sum(-1) / w ** 2)
    return total


def cover(check: bool):
    W, H = COVER_SIZE
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")

    xs = np.arange(-OVERSCAN, W + OVERSCAN + 1e-9, SPACING)
    ys = np.arange(-OVERSCAN, H + OVERSCAN + 1e-9, SPACING)
    lines = ([np.stack([np.full(600, x), np.linspace(ys[0], ys[-1], 600)], -1) for x in xs]
             + [np.stack([np.linspace(xs[0], xs[-1], 1400), np.full(1400, y)], -1) for y in ys])
    d_max = max(abs(depth(np.array([[cx, cy]]))[0]) for cx, cy, _, _ in WELLS)

    inner, outer = ([], [], []), ([], [], [])     # (segments, colours, widths)
    for L in lines:
        Q = warp(L)
        dep = depth(L)
        mid = 0.5 * (Q[1:] + Q[:-1])
        dmid = 0.5 * (dep[1:] + dep[:-1])
        # fade toward the card edge
        edge = np.minimum.reduce([mid[:, 0], W - mid[:, 0], mid[:, 1], H - mid[:, 1]])
        a = np.clip(edge / EDGE_FADE, 0, 1) ** 1.4
        t = np.clip(dmid / d_max, -1, 1)
        rgba = CURVE(0.5 - 0.5 * np.sign(t) * np.abs(t) ** 1.1)
        rgba[:, 3] = a
        S = np.stack([Q[:-1], Q[1:]], 1)
        lw = 2.2 + 1.6 * np.abs(t)
        for sel, bucket in [(a > 0.999, inner), ((a > 0.01) & (a <= 0.999), outer)]:
            bucket[0].extend(S[sel])
            bucket[1].extend(rgba[sel])
            bucket[2].extend(lw[sel].tolist())
    # opaque interior strokes get round caps (no seams); the translucent edge fade keeps
    # butt caps (round caps would bead where translucent segments overlap)
    for (segs, cols, widths), cap in [(outer, "butt"), (inner, "round")]:
        ax.add_collection(LineCollection(segs, colors=cols, linewidths=widths, capstyle=cap,
                                         joinstyle="round"))
    save(fig, OUT, check)


if __name__ == "__main__":
    cover(check="--check" in sys.argv[1:])
