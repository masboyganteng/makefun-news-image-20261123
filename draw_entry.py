"""Draw the front page for Monday 23 November 2026.

A single broadsheet-style page, "The World in One Day", rendered with Pillow
only: no network, no outside files. Run it and it writes entry.png beside
this file, 1024 by 1024 pixels.

The day's stories, all verified against reporting dated Monday 23 November
2026: the Democrats clinch their biggest US House majority since 1992; NATO's
council meets in Brussels after Russian missiles came down in Poland; India
close in on victory on the final day in Wellington; plus briefs on FIFA's
2035 Women's World Cup hosts, a boy pulled alive from rubble in Ukraine,
and a deep earthquake off Vanuatu.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 239, 223)
INK = (26, 24, 21)
SOFT = (96, 91, 84)
RED = (198, 32, 38)
NAVY = (31, 44, 66)
GOLD = (212, 186, 112)
RULE = (180, 172, 154)

FDIR = "/usr/share/fonts/truetype/dejavu/"
SANS_B = FDIR + "DejaVuSans-Bold.ttf"
SANS = FDIR + "DejaVuSans.ttf"
SERIF_B = FDIR + "DejaVuSerif-Bold.ttf"
SERIF = FDIR + "DejaVuSerif.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(d, s, f):
    box = d.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def wrap(d, s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if tw(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, path, max_w, max_lines, start, smallest):
    """Biggest size (<= start) where s wraps into max_lines within max_w."""
    for size in range(start, smallest - 1, -1):
        f = font(path, size)
        lines = wrap(d, s, f, max_w)
        if len(lines) <= max_lines and all(tw(d, ln, f) <= max_w for ln in lines):
            return f, lines
    raise SystemExit("does not fit: " + s)


def para(d, x, y, lines, f, fill, gap=1.18):
    asc, desc = f.getmetrics()
    step = int((asc + desc) * gap)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += step
    return y


def centre(d, cx, y, s, f, fill):
    d.text((cx - tw(d, s, f) // 2, y), s, font=f, fill=fill)


def rule(d, x0, y, x1, w=2):
    d.line((x0, y, x1, y), fill=INK, width=w)


def kicker(d, x, y, s):
    f = font(SANS_B, 19)
    d.text((x, y), s, font=f, fill=RED)
    return y + 26

# ------------------------------------------------------------------ pictures

def capitol_panel(d, x0, y0, x1, y1):
    """US Capitol dome in cream on a navy panel, with the 258-seat bar."""
    d.rectangle((x0, y0, x1, y1), fill=NAVY)
    cx = (x0 + x1) // 2
    top = y0 + 26
    # dome: half-ellipse crowned by a small lantern and flag
    d.pieslice((cx - 92, top, cx + 92, top + 118), 180, 360, fill=PAPER)
    d.rectangle((cx - 92, top + 58, cx + 92, top + 74), fill=PAPER)
    d.rectangle((cx - 4, top - 22, cx + 4, top + 2), fill=PAPER)
    d.ellipse((cx - 10, top - 30, cx + 10, top - 12), fill=PAPER)
    d.line((cx + 4, top - 30, cx + 30, top - 24), fill=RED, width=3)
    d.polygon([(cx + 4, top - 30), (cx + 30, top - 24), (cx + 4, top - 18)],
              fill=RED)
    # drum columns
    for i in range(-3, 4):
        d.rectangle((cx + i * 26 - 6, top + 74, cx + i * 26 + 6, top + 118),
                    fill=PAPER)
    # base steps
    d.rectangle((cx - 118, top + 118, cx + 118, top + 130), fill=PAPER)
    d.rectangle((cx - 132, top + 130, cx + 132, top + 142), fill=PAPER)
    # seat bar: 258 of 435 seats
    by = y1 - 78
    d.text((x0 + 18, by - 30), "DEMOCRATS 258 OF 435 SEATS",
           font=font(SANS_B, 19), fill=PAPER)
    d.rectangle((x0 + 18, by, x1 - 18, by + 22), outline=PAPER, width=2)
    fill_w = int((x1 - x0 - 36) * 258 / 435)
    d.rectangle((x0 + 18, by, x0 + 18 + fill_w, by + 22), fill=RED)
    d.text((x0 + 18, by + 30), "LARGEST MAJORITY SINCE 1992",
           font=font(SANS, 17), fill=GOLD)


def compass_star(d, cx, cy, r):
    """Four-point NATO compass star in ink with a red centre."""
    pts = []
    for ang, rad in ((270, r), (0, r // 4), (90, r), (180, r // 4),
                     (270, r)):
        import math
        a = math.radians(ang)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=INK)
    pts = []
    for ang, rad in ((0, r), (90, r // 4), (180, r), (270, r // 4), (0, r)):
        a = math.radians(ang)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d.polygon(pts, fill=INK)
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=RED)


def cricket_mark(d, x0, y0):
    """A red ball with a seam, and a bat leaning on it."""
    d.ellipse((x0, y0, x0 + 54, y0 + 54), fill=RED)
    d.arc((x0 + 7, y0 + 5, x0 + 47, y0 + 49), 200, 340, fill=PAPER, width=3)
    d.arc((x0 + 7, y0 + 5, x0 + 47, y0 + 49), 20, 160, fill=PAPER, width=3)
    # bat: handle + blade, tilted, kept inside a 78 px box
    d.polygon([(x0 + 66, y0 - 4), (x0 + 78, y0), (x0 + 62, y0 + 48),
               (x0 + 50, y0 + 44)], fill=(214, 190, 130))
    d.polygon([(x0 + 50, y0 + 44), (x0 + 62, y0 + 48), (x0 + 56, y0 + 70),
               (x0 + 44, y0 + 66)], fill=(214, 190, 130))


def ball_icon(d, cx, cy, r):
    """Football: a circle with a dark pentagon and seams."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=INK, width=3)
    d.polygon([(cx, cy - r // 2), (cx + r // 2, cy - r // 6),
               (cx + r // 3, cy + r // 2), (cx - r // 3, cy + r // 2),
               (cx - r // 2, cy - r // 6)], fill=INK)
    for ex, ey in ((cx, cy - r), (cx + r, cy), (cx - r, cy),
                   (cx + r // 2, cy + r), (cx - r // 2, cy + r)):
        d.line((cx, cy - r // 2, ex, ey), fill=INK, width=2)


def cross_icon(d, cx, cy, r):
    """Rescue cross in red inside a ring."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=RED, width=3)
    d.rectangle((cx - 7, cy - r + 12, cx + 7, cy + r - 12), fill=RED)
    d.rectangle((cx - r + 12, cy - 7, cx + r - 12, cy + 7), fill=RED)


def quake_icon(d, x0, y0, w, h):
    """Seismograph zigzag in ink."""
    pts = [(x0, y0 + h // 2), (x0 + w * 0.22, y0 + h // 2),
           (x0 + w * 0.30, y0 + 4), (x0 + w * 0.38, y0 + h - 4),
           (x0 + w * 0.46, y0 + h // 2), (x0 + w * 0.54, y0 + 10),
           (x0 + w * 0.62, y0 + h - 10), (x0 + w * 0.70, y0 + h // 2),
           (x0 + w, y0 + h // 2)]
    d.line(pts, fill=INK, width=3, joint="curve")

# --------------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 36
    RX = W - MX

    # masthead
    rule(d, MX, 24, RX, 3)
    f, lines = fit(d, "THE WORLD IN ONE DAY", SERIF_B, RX - MX, 1, 64, 40)
    y = 34
    for ln in lines:
        centre(d, W // 2, y, ln, f, INK)
        y += 78
    centre(d, W // 2, 114, "ONE DAY  ·  ONE PAGE  ·  THE WORLD'S NEWS",
           font(SANS_B, 15), SOFT)
    rule(d, MX, 138, RX, 2)

    # date band
    d.rectangle((MX, 146, RX, 184), fill=INK)
    centre(d, W // 2, 154, "MONDAY,  23  NOVEMBER  2026",
           font(SANS_B, 27), PAPER)

    # ---- lead: Democrats take the House
    ly = 200
    y = kicker(d, MX, ly, "LEAD  ·  UNITED STATES")
    f, lines = fit(d, "DEMOCRATS TAKE 258", SERIF_B, 566, 2, 56, 36)
    y = para(d, MX, y + 4, lines, f, INK, 1.02)
    y = para(d, MX, y + 8, ["Biggest House majority since 1992"],
             font(SANS_B, 25), INK)
    body = ("Chuck Hubbard beats 11-term Rep. Virginia Foxx by 330 votes "
            "in a North Carolina recount, giving Democrats at least 258 of "
            "435 House seats. Hakeem Jeffries is set to become Speaker "
            "when the new Congress meets on 3 January.")
    para(d, MX, y + 12, wrap(d, body, font(SERIF, 19), 566),
         font(SERIF, 19), INK, 1.22)
    capitol_panel(d, 622, ly, RX, 540)
    rule(d, MX, 558, RX, 2)

    # ---- second row: NATO (left) and Wellington (right)
    ry = 572
    d.line((512, ry, 512, 784), fill=RULE, width=2)
    compass_star(d, 462, 600, 34)
    y = kicker(d, MX, ry + 8, "EUROPE  ·  BRUSSELS")
    f, lines = fit(d, "NATO MEETS OVER POLAND", SERIF_B, 464, 1, 32, 26)
    y = para(d, MX, 640, lines, f, INK, 1.04)
    body = ("The North Atlantic Council meets in Brussels after a "
            "Russian Kh-101 cruise missile and two more objects came "
            "down in south-east Poland on Friday. No one was hurt; Mark "
            "Rutte vows to defend \u2018every inch of Polish "
            "territory\u2019.")
    para(d, MX, y + 6, wrap(d, body, font(SERIF, 16), 464),
         font(SERIF, 16), INK, 1.15)

    cricket_mark(d, 906, 570)
    y = kicker(d, 524, ry + 8, "SPORT  ·  WELLINGTON")
    f, lines = fit(d, "INDIA CLOSE IN", SERIF_B, 348, 1, 32, 26)
    y = para(d, 524, 640, lines, f, INK, 1.04)
    body = ("New Zealand reach 206 for five at tea on the final day, "
            "still 146 behind after India\u2019s record 720 for nine "
            "declared. Conway falls for 65 and Ravindra for 37 before "
            "lunch; five wickets stand between India and victory.")
    para(d, 524, y + 6, wrap(d, body, font(SERIF, 16), 464),
         font(SERIF, 16), INK, 1.15)
    rule(d, MX, 796, RX, 2)

    # ---- briefs
    by = 812
    cols = [
        (MX, "FOOTBALL  ·  ZURICH", "UK TO HOST 2035",
         "FIFA confirms on Monday: England, Scotland, Wales and "
         "Northern Ireland will stage the 2035 Women\u2019s World Cup "
         "\u2014 the first in Britain since 1966.", "ball"),
        (352, "UKRAINE  ·  KYIV REGION", "BOY, 7, PULLED ALIVE",
         "A seven-year-old boy is pulled alive from the rubble of a "
         "block hit by a Russian drone. Nine people are dead.",
         "cross"),
        (668, "PACIFIC  ·  VANUATU", "QUAKE M6.5, DEEP",
         "A magnitude 6.5 earthquake strikes deep beneath the Vanuatu "
         "region early on Monday, 598 km down. No damage is "
         "reported.", "quake"),
    ]
    for x, kick, head, body, icon in cols:
        if icon == "ball":
            ball_icon(d, x + 20, by + 20, 20)
        elif icon == "cross":
            cross_icon(d, x + 20, by + 20, 20)
        else:
            quake_icon(d, x, by + 4, 40, 34)
        d.text((x + 48, by + 10), kick, font=font(SANS_B, 16), fill=RED)
        f, lines = fit(d, head, SERIF_B, 304, 1, 24, 20)
        y = para(d, x, by + 44, lines, f, INK, 1.04)
        para(d, x, y + 6, wrap(d, body, font(SERIF, 14), 304),
             font(SERIF, 14), INK, 1.18)

    # footer
    rule(d, MX, 974, RX, 1)
    centre(d, W // 2, 984,
           "Sources: Reuters  ·  BBC  ·  CNN  ·  AP  ·  AFP  ·  USGS",
           font(SANS, 14), SOFT)
    return img


def main():
    img = build()
    img.save(os.path.join(HERE, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
