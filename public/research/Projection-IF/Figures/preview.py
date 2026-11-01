#!/usr/bin/env python3
"""Cover image for the Projection-IF research entry -> ../preview.png

Text-free, in the visual language of the headline figure of Kreer et al., "Bayesian
Influence Functions for Hessian-Free Data Attribution" (arXiv:2509.26544, Fig. 1a): a
rugged 3D loss landscape coloured blue (low) -> white -> red (high), Lambert-shaded, over a
light floor carrying its level-coloured contour lines (blue near the minimum, salmon far
away). A narrow blue well at theta* is ringed by flat-topped red mesas cut by steep walls
and separated by open radial valleys, the kind of degenerate curvature influence functions
have to invert. The square floor is seen corner-on as a diamond, as in the reference, from
a low elevation and much larger than the surface, so its contours (the valleys running out
to the edges) widen the scene to the research card's 25:9 cover box; transparent
background, and the light floor and mid-tone ink outline stay visible on both the light
and dark card surfaces.

Self-contained (matplotlib is not a project dependency; contourpy ships with it):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/Projection-IF/Figures/preview.py
    /tmp/pbb-viz/bin/python public/research/Projection-IF/Figures/preview.py --check
        # --check also writes a review sheet (light card / dark card / card-size box)
        # to /tmp/preview-check/
"""

from __future__ import annotations

import sys
from pathlib import Path

import contourpy
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import LineCollection, PolyCollection  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, to_rgb  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"

# --- style ------------------------------------------------------------------
INK = "#5a7394"               # site mid-tone ink: floor outline and shadow
FLOOR = "#f3f3f6"             # floor fill (light grey, as the reference figure)
# blue well -> near-white -> red mesas, the reference figure's diverging surface colours
TERRAIN = LinearSegmentedColormap.from_list(
    "terrain", ["#2f55c8", "#6f93e6", "#e9edf6", "#f1b9a6", "#de5a4a", "#c22a2e"])
# contour lines: blue near the minimum -> salmon far away
CONTOUR = LinearSegmentedColormap.from_list("contour", ["#3a63d8", "#8aa2ea", "#e58b80",
                                                        "#eaa79c"])
LIGHT_CARD = "#fbfaff"
DARK_CARD = "#1a1824"
DPI = 200
COVER_SIZE = (12.5, 4.5)      # inches == data units -> 2500 x 900 px, exactly 25:9

plt.rcParams.update({
    "savefig.transparent": True,
    "savefig.dpi": DPI,
})


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
# camera: orthographic, rotate about z by AZ, then tilt down by EL
# ---------------------------------------------------------------------------
AZ = np.deg2rad(45)
EL = np.deg2rad(17)
LIGHT = np.array([-0.35, 0.55, 0.76])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def view(P):
    """World (..., 3) -> (screen x, screen y, depth); larger depth = farther away."""
    P = np.asarray(P, float)
    x, y, z = P[..., 0], P[..., 1], P[..., 2]
    x1 = x * np.cos(AZ) - y * np.sin(AZ)
    y1 = x * np.sin(AZ) + y * np.cos(AZ)
    return np.stack([x1, z * np.cos(EL) + y1 * np.sin(EL), y1 * np.cos(EL) - z * np.sin(EL)], -1)


def hdepth(xy):
    """Horizontal distance from the camera: the correct painter's key for a height field."""
    xy = np.asarray(xy, float)
    return view(np.concatenate([xy, np.zeros(xy.shape[:-1] + (1,))], -1))[..., 2]


def rot(a):
    a = np.deg2rad(a)
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])


# ---------------------------------------------------------------------------
# the loss
# ---------------------------------------------------------------------------
FLOOR_X = FLOOR_Y = 1.6       # square floor, seen corner-on
SURF_X = SURF_Y = 0.86        # the surface is a disk in the middle of it
HEIGHT = 0.65                 # vertical exaggeration of the surface


def loss(x, y):
    """Rugged loss: a narrow elongated well at theta*, ringed by flat mesas of different
    heights separated by radial valleys, cut by steep walls (tanh plateaus)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    xr, yr = np.einsum("ij,j...->i...", rot(-25), np.stack([x, y]))
    r = np.sqrt((xr / 0.95) ** 2 + (yr / 1.25) ** 2)
    phi = np.arctan2(yr, xr)
    sectors = 0.5 + 0.5 * np.tanh(3.6 * (np.cos(5 * phi + 0.6) + 0.45 * np.cos(3 * phi - 1.2)
                                         + 0.25))
    tiers = 0.62 + 0.30 * np.cos(2 * phi + 0.5) + 0.12 * np.sin(4 * phi - 0.3)
    rim = 0.5 + 0.5 * np.tanh((r - 0.36) / 0.06)
    mesas = rim * sectors * tiers
    shelf = 0.22 * (0.5 + 0.5 * np.tanh((r - 0.30) / 0.05))      # valleys stay above the well
    well = 0.30 * np.exp(-((xr / 0.10) ** 2 + (yr / 0.26) ** 2))
    return np.maximum(mesas, shelf) - well + 0.30


def height(x, y):
    return HEIGHT * loss(x, y) + 0.02


# colour scale of the whole surface patch
_R, _F = np.meshgrid(np.linspace(0, 1, 120), np.linspace(0, 2 * np.pi, 480))
_ZALL = height(SURF_X * _R * np.cos(_F), SURF_Y * _R * np.sin(_F))
_ZLO, _ZHI = _ZALL.min(), _ZALL.max()


# ---------------------------------------------------------------------------
# drawing
# ---------------------------------------------------------------------------
class Placed:
    """The scene in raw view coordinates, placed on the canvas by offset + scale."""

    def __init__(self):
        self.off, self.sc = np.zeros(2), 1.0

    def to(self, xy):
        return self.off + self.sc * np.asarray(xy)


def floor_corners():
    return np.array([[-FLOOR_X, -FLOOR_Y], [FLOOR_X, -FLOOR_Y], [FLOOR_X, FLOOR_Y],
                     [-FLOOR_X, FLOOR_Y]])


def surface_grid(n_r, n_phi):
    rho = np.linspace(0, 1, n_r + 1)
    phi = np.linspace(0, 2 * np.pi, n_phi + 1)
    RR, FF = np.meshgrid(rho, phi, indexing="ij")
    return SURF_X * RR * np.cos(FF), SURF_Y * RR * np.sin(FF), rho, phi


def scene_points():
    X, Y, _, _ = surface_grid(40, 160)
    Wp = np.stack([X, Y, height(X, Y)], -1).reshape(-1, 3)
    c = floor_corners()
    return np.concatenate([view(np.c_[c, np.zeros(4)])[:, :2], view(Wp)[:, :2]])


def draw_floor(ax, P: Placed, n_levels=18):
    floor = P.to(view(np.c_[floor_corners(), np.zeros(4)])[:, :2])
    ax.add_patch(Polygon(floor + np.array([0.05, -0.08]), closed=True, facecolor=INK,
                         edgecolor="none", alpha=0.10, zorder=0.5))
    ax.add_patch(Polygon(floor, closed=True, facecolor=FLOOR, edgecolor="none", zorder=1))
    ax.add_patch(Polygon(floor, closed=True, facecolor="none", edgecolor=INK, lw=2.4,
                         joinstyle="round", zorder=1.4))
    gx = np.linspace(-FLOOR_X, FLOOR_X, 420)
    gy = np.linspace(-FLOOR_Y, FLOOR_Y, 420)
    X, Y = np.meshgrid(gx, gy)
    Z = loss(X, Y)
    gen = contourpy.contour_generator(X, Y, Z)
    zlo, zhi = Z.min(), np.quantile(Z, 0.92)
    levels = zlo + (zhi - zlo) * np.linspace(0.06, 0.97, n_levels) ** 1.3
    segs, cols = [], []
    for k, lev in enumerate(levels):
        c = CONTOUR(k / (len(levels) - 1))
        for line in gen.lines(lev):
            segs.append(P.to(view(np.c_[line, np.zeros(len(line))])[:, :2]))
            cols.append(c)
    lc = LineCollection(segs, colors=cols, linewidths=1.5, alpha=0.9, zorder=1.2)
    ax.add_collection(lc)
    clip = Polygon(floor, closed=True, transform=ax.transData, facecolor="none",
                   edgecolor="none")
    ax.add_patch(clip)
    lc.set_clip_path(clip)


def draw_surface(ax, P: Placed, n_r=130, n_phi=520):
    """Painter-sorted (by horizontal depth) quads, colour by height, Lambert-shaded from
    the smooth normal (per-quad cross products stair-step on steep walls)."""
    X, Y, rho, phi = surface_grid(n_r, n_phi)
    Z = height(X, Y)
    V = view(np.stack([X, Y, Z], -1))
    RC, FC = np.meshgrid((rho[:-1] + rho[1:]) / 2, (phi[:-1] + phi[1:]) / 2, indexing="ij")
    CX, CY = SURF_X * RC * np.cos(FC), SURF_Y * RC * np.sin(FC)
    h = 1e-3
    zx = (height(CX + h, CY) - height(CX - h, CY)) / (2 * h)
    zy = (height(CX, CY + h) - height(CX, CY - h)) / (2 * h)
    N = np.stack([-zx, -zy, np.ones_like(zx)], -1)
    N = N / np.linalg.norm(N, axis=-1, keepdims=True)
    lam = np.clip(N @ LIGHT, 0, 1)
    zc = (Z[:-1, :-1] + Z[1:, :-1] + Z[1:, 1:] + Z[:-1, 1:]) / 4
    base = TERRAIN(np.clip((zc - _ZLO) / (_ZHI - _ZLO), 0, 1))[..., :3]
    cols = np.clip(base * (0.62 + 0.42 * lam)[..., None], 0, 1).reshape(-1, 3)
    quads = np.stack([V[:-1, :-1, :2], V[1:, :-1, :2], V[1:, 1:, :2], V[:-1, 1:, :2]], 2)
    quads = P.to(quads.reshape(-1, 4, 2))
    depth = hdepth(np.stack([CX, CY], -1).reshape(-1, 2))
    order = np.argsort(depth)[::-1]
    c = [tuple(cols[k]) + (1.0,) for k in order]
    ax.add_collection(PolyCollection(quads[order], facecolors=c, edgecolors=c,
                                     linewidths=0.4, zorder=3))


def cover(check: bool):
    W, H = COVER_SIZE
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    m = 0.08

    pts = scene_points()
    lo, hi = pts.min(0), pts.max(0)
    span = hi - lo
    P = Placed()
    P.sc = min((W - 2 * m) / span[0], (H - 2 * m - 0.04) / span[1])
    P.off = np.array([W, H]) / 2 - P.sc * (lo + hi) / 2 + np.array([0, 0.02])
    print(f"scene aspect {span[0] / span[1]:.2f} (canvas {W / H:.2f}), scale {P.sc:.2f}")

    draw_floor(ax, P)
    draw_surface(ax, P)
    save(fig, OUT, check)


if __name__ == "__main__":
    cover(check="--check" in sys.argv[1:])
