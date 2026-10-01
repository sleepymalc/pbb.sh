#!/usr/bin/env python3
"""Cover image for the Dr. Post-Training research entry -> ../preview.png

Composition: the Twemoji stethoscope (the icon in the paper's title), mirrored so its
chest piece rests on a pile of data cards drawn in Twemoji's palette; the card under the
chest piece carries a small ECG trace. The stethoscope is a Twemoji graphic (CC-BY 4.0,
see twemoji/LICENSE.txt), with its near-black tubing lightened a little so it stays
visible on the dark card surface; the cards are drawn here. A "doctor" variant (Twemoji
health worker + magnifying glass) is kept as a secondary target.
Sized to fill the research card's 25:9 cover box on a transparent background.

Self-contained; needs Inkscape on PATH to rasterize the SVGs
(matplotlib is not a project dependency):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/Dr-Post-Training/Figures/preview.py
    /tmp/pbb-viz/bin/python public/research/Dr-Post-Training/Figures/preview.py --check
        # --check also writes a review sheet (light card / dark card / card-size box)
        # to /tmp/preview-check/
    /tmp/pbb-viz/bin/python public/research/Dr-Post-Training/Figures/preview.py doctor
        # the earlier variant with the Twemoji health worker and magnifying glass; written
        # to /tmp/preview-check/variants/ for comparison, not into the repo
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
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402
from matplotlib.transforms import Affine2D  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"
TWEMOJI = HERE / "twemoji"

# --- Twemoji palette for the parts drawn here ---------------------------------
CARD = "#F5F8FA"
CARD_EDGE = "#CCD6DD"
CARD_HEAD = "#55ACEE"
CARD_LINE = "#CCD6DD"
BAR_BLUE, BAR_PURPLE, BAR_RED, BAR_GREEN, BAR_ORANGE = "#55ACEE", "#AA8DD8", "#DD2E44", "#78B159", "#F4900C"
LIGHT_CARD = "#fbfaff"
DARK_CARD = "#1a1824"
DPI = 200
COVER_SIZE = (12.5, 4.5)      # inches == data units -> 2500 x 900 px, exactly 25:9


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


def place(ax, img: np.ndarray, x: float, y: float, size: float, zorder: int):
    """Draw a square emoji with its bottom-left corner at (x, y) and side `size` data units."""
    ax.imshow(img, extent=[x, x + size, y, y + size], zorder=zorder, interpolation="lanczos")
    ax.set_aspect("equal")


def data_card(ax, cx, cy, w, h, angle, kind, zorder):
    """A rounded data card, rotated about its centre, with a header strip and some content."""
    tr = Affine2D().rotate_deg_around(cx, cy, angle) + ax.transData
    x0, y0 = cx - w / 2, cy - h / 2
    ax.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor=CARD, edgecolor=CARD_EDGE, lw=2.4, transform=tr,
                                zorder=zorder))
    ax.add_patch(FancyBboxPatch((x0 + 0.12, y0 + h - 0.3), w - 0.24, 0.16,
                                boxstyle="round,pad=0,rounding_size=0.08", facecolor=CARD_HEAD,
                                edgecolor="none", transform=tr, zorder=zorder + 1))
    if kind == "lines":
        for i, frac in enumerate([0.9, 0.7, 0.8]):
            y = y0 + h - 0.55 - i * 0.2
            ax.plot([x0 + 0.14, x0 + 0.14 + (w - 0.28) * frac], [y, y], color=CARD_LINE, lw=5,
                    solid_capstyle="round", transform=tr, zorder=zorder + 1)
    elif kind == "bars":
        for i, (hb, c) in enumerate([(0.32, BAR_BLUE), (0.5, BAR_PURPLE), (0.22, BAR_GREEN),
                                     (0.42, BAR_ORANGE)]):
            bx = x0 + 0.2 + i * ((w - 0.4) / 4)
            ax.add_patch(Rectangle((bx, y0 + 0.14), (w - 0.4) / 4 - 0.1, hb, facecolor=c,
                                   edgecolor="none", transform=tr, zorder=zorder + 1))
    elif kind == "pulse":
        y = y0 + h * 0.42
        pts = np.array([(0.08, 0), (0.3, 0), (0.37, 0.14), (0.44, -0.1), (0.52, 0.42), (0.6, -0.3),
                        (0.66, 0.06), (0.72, 0), (0.92, 0)])
        ax.plot(x0 + pts[:, 0] * w, y + pts[:, 1] * h, color=BAR_RED, lw=6, solid_joinstyle="round",
                solid_capstyle="round", transform=tr, zorder=zorder + 1)
    elif kind == "dots":
        for i in range(3):
            for j in range(4):
                c = BAR_RED if (i + j) % 3 == 0 else CARD_LINE
                ax.add_patch(Circle((x0 + 0.25 + j * (w - 0.5) / 3, y0 + 0.22 + i * 0.22), 0.055,
                                    facecolor=c, edgecolor="none", transform=tr, zorder=zorder + 1))


def cover(check: bool, out: Path):
    fig, ax = new_canvas()

    # --- the pile of data ----------------------------------------------------------
    cards = [
        # (cx, cy, w, h, angle, kind, zorder)
        (6.3, 0.95, 1.75, 1.2, 14, "lines", 3),
        (10.35, 0.95, 1.75, 1.2, -12, "dots", 3),
        (8.4, 0.9, 1.9, 1.25, 4, "bars", 4),
        (11.9, 0.9, 1.6, 1.15, 9, "lines", 3),
        (7.3, 1.85, 1.75, 1.2, -9, "dots", 5),
        (9.6, 1.85, 1.75, 1.2, 11, "lines", 5),
        (11.2, 1.8, 1.55, 1.1, -7, "bars", 4),
        (8.45, 2.72, 1.8, 1.22, -4, "bars", 6),
    ]
    for c in cards:
        data_card(ax, *c)

    # --- the doctor (Twemoji health worker) ----------------------------------------------
    doc = rasterize(TWEMOJI / "1f9d1-200d-2695-fe0f.svg", 1400)
    doc_size = 4.4
    doc_x, doc_y = 0.6, 0.05
    place(ax, doc, doc_x, doc_y, doc_size, zorder=10)

    # --- the magnifier (Twemoji 1f50e) hovering over the pile --------------------------------
    # in the 36-unit Twemoji viewBox the lens centre sits near (22, 14); with the image's
    # bottom-left at (mx, my) and side `ms` that maps to (mx + 0.61 ms, my + 0.61 ms).
    ms = 2.9
    lens_target = (6.7, 2.95)
    mx, my = lens_target[0] - 0.61 * ms, lens_target[1] - 0.61 * ms
    mag = rasterize(TWEMOJI / "1f50e.svg", 1200)
    place(ax, mag, mx, my, ms, zorder=14)

    # what the lens sees: a zoomed-in bar chart from the card beneath it
    r_lens = 0.225 * ms
    clip = Circle(lens_target, r_lens, transform=ax.transData)
    x = lens_target[0] - 0.46
    for hb, c in [(0.55, BAR_BLUE), (0.9, BAR_PURPLE), (0.4, BAR_GREEN), (0.72, BAR_ORANGE)]:
        bar = Rectangle((x, lens_target[1] - 0.48), 0.19, hb, facecolor=c, edgecolor="none",
                        zorder=15)
        bar.set_clip_path(clip)
        ax.add_patch(bar)
        x += 0.25

    save(fig, out, check)


def cover_stethoscope(check: bool, out: Path):
    """Variant without the doctor: the Twemoji stethoscope (the icon in the paper's title),
    mirrored so its chest piece rests on the pile of data."""
    fig, ax = new_canvas()
    cards = [
        # (cx, cy, w, h, angle, kind, zorder)
        (5.65, 0.95, 1.8, 1.2, 10, "lines", 3),
        (7.75, 1.0, 1.9, 1.25, -5, "dots", 4),
        (9.85, 0.95, 1.8, 1.2, 12, "bars", 3),
        (11.4, 1.0, 1.6, 1.15, -8, "lines", 3),
        (4.95, 2.25, 1.8, 1.25, -8, "pulse", 6),
        (6.95, 2.75, 1.85, 1.25, 5, "bars", 6),
        (8.95, 1.9, 1.75, 1.2, -10, "lines", 5),
        (10.65, 1.95, 1.6, 1.15, 9, "dots", 5),
    ]
    for c in cards:
        data_card(ax, *c)
    # Twemoji 1fa7a has its chest piece at the left; mirror it so the chest piece lands on the
    # top-left card of the pile and the headset opens to the upper left
    steth = rasterize(TWEMOJI / "1fa7a.svg", 1400)[:, ::-1, :].copy()
    # Twemoji's tubing is #31373D, which nearly vanishes on the dark card; shift those pixels
    # (and their anti-aliased edges, by how close they are to that colour) to a mid slate
    dark = np.array([0x31, 0x37, 0x3D]) / 255
    target = np.array([0x4F, 0x5B, 0x68]) / 255
    rgb = steth[..., :3]
    closeness = np.clip(1 - np.linalg.norm(rgb - dark, axis=-1) / 0.25, 0, 1)[..., None]
    steth[..., :3] = rgb * (1 - closeness) + target * closeness
    place(ax, steth, 0.7, 0.05, 4.4, zorder=10)
    save(fig, out, check)


if __name__ == "__main__":
    args = sys.argv[1:]
    check = "--check" in args
    for name in [a for a in args if not a.startswith("--")] or ["stethoscope"]:
        if name == "stethoscope":
            cover_stethoscope(check, OUT)
        elif name == "doctor":
            cover(check, Path("/tmp/preview-check/variants/Dr-Post-Training-doctor.png"))
        else:
            sys.exit(f"unknown target {name!r}; use stethoscope or doctor")
