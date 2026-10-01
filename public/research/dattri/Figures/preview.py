#!/usr/bin/env python3
"""Cover image for the dattri research entry -> ../preview.png

A wordmark-only logo: "dattri" over a light-weight "DATA ATTRIBUTION", scaled to
fill the research card's 25:9 cover box and centred, on a transparent background,
in a mid-tone ink that stays visible on both the light and dark card surfaces.

Self-contained; run from anywhere (matplotlib is not a project dependency):

    python3 -m venv /tmp/pbb-viz && /tmp/pbb-viz/bin/pip install matplotlib numpy pillow
    /tmp/pbb-viz/bin/python public/research/dattri/Figures/preview.py            # write ../preview.png
    /tmp/pbb-viz/bin/python public/research/dattri/Figures/preview.py --check    # + review sheet in
                                                                                 #   /tmp/preview-check/
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as fm  # noqa: E402
from matplotlib.colors import to_rgb  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "preview.png"

# --- style (contrast on light #fbfaff / dark #1a1824: ink 4.7:1 / 3.6:1, green 3.9:1 / 4.3:1)
INK = "#5a7394"
GREEN = "#4e8c2d"
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


def main(argv):
    fig, ax = new_canvas()
    wordmark(ax, [("dattri", INK, "bold")], "DATA   ATTRIBUTION")
    save(fig, OUT, check="--check" in argv)


if __name__ == "__main__":
    main(sys.argv[1:])
