"""Worked examples: each function is one isometric scene drawn with iso_lib. Run one and save s.svg()."""
from iso_lib import *  # noqa
import math

def envelope(s, x, y, z, w=64, d=44, h=7, gold=False):
    s.box(x, y, z, w, d, h, tones(MUST, .3, .22) if gold else (CARD, MUTED, HAIR), None if gold else ENV_EDGE)
    s.decal_top("mail", x + w / 2, y + d / 2, z + h, min(w, d) * .8, MINK if gold else mix(HAIR, INK, .45), 1.5)

def pile(s, x, y, z, n, seed=1, gold_at=None, jitter=5):
    r = seed
    for i in range(n):
        r = (r * 9301 + 49297) % 233280
        dx = (r / 233280 - .5) * jitter * 2
        r = (r * 9301 + 49297) % 233280
        dy = (r / 233280 - .5) * jitter * 2
        envelope(s, x + dx, y + dy, z + i * 7, gold=(i == gold_at))



def _sheet(s, x, y, z, w=120, d=160, lines=6, gold_line=None):
    """A sheet of paper lying flat, with text lines drawn on it."""
    s.box(x, y, z, w, d, 3, (CARD, MUTED, HAIR), mix(HAIR, INK, .35))
    P = s.P
    for j in range(lines):
        yy = y + 22 + j * (d - 40) / max(lines - 1, 1)
        col = MUST if j == gold_line else mix(HAIR, INK, .45)
        s.a(f'<polyline points="{s.pts(P(x + 16, yy, z + 3), P(x + w - (34 if j % 2 else 18), yy, z + 3))}" stroke="{col}" stroke-width="4" stroke-linecap="round" fill="none"/>')


def contract():
    """A contract on a desk, a pen beside it, and a gold agent cube checking it."""
    s = Scene(1000, 760, 470, 340, 1.0, "A contract on a desk with a pen, and a gold agent cube checking it")
    s.platform(-260, -190, 460, 360, 18, tones(mix(MUTED, INK, .12), .25, .2))     # the desk
    _sheet(s, -200, -140, 18, 190, 260, 7, gold_line=3)                              # the contract
    P = s.P
    s.a(f'<polyline points="{s.pts(P(-160, 70, 21), P(-60, 70, 21))}" stroke="{NAVY}" stroke-width="3" fill="none"/>')   # signature line
    s.box(30, 40, 18, 150, 14, 12, tones(NAVY, .3, .25))                              # the pen
    s.box(176, 40, 18, 14, 14, 12, tones(MUST, .3, .25))
    s.box(40, -120, 18, 100, 100, 90, tones(MUST, .35, .25))                          # the agent cube
    s.decal_top("chip", 90, -70, 108, 64, MINK, 2)
    s.decal_left("check", 50, -20, 30, 54, MINK, 2.2)
    s.route([(30, -60, 70), (-20, -40, 30)], dash="6 5", sw=2.4, color=MUST)          # it is reading the page
    return s.svg()


def report():
    """A weekly report coming off a printer, a small bar chart on the page."""
    s = Scene(1000, 800, 470, 380, 1.0, "A printer with a weekly report coming out, a small bar chart on the page")
    s.platform(-230, -170, 420, 340, 16)
    s.box(-170, -120, 16, 220, 200, 110, tones(mix(MUTED, INK, .18), .3, .25))       # the printer body
    s.box(-150, -100, 126, 180, 160, 10, tones(mix(MUTED, INK, .32), .3, .25))       # its lid
    s.box(-165, 80, 70, 210, 6, 12, tones(INK, .3, .2))                              # the output slot
    P = s.P
    x, y, z, w, d = -140, 86, 72, 150, 170                                         # the page, sliding out toward us
    s.poly([P(x, y, z), P(x + w, y, z), P(x + w, y + d, z - 40), P(x, y + d, z - 40)], CARD, mix(HAIR, INK, .35), 1.2)
    for j, h in enumerate((.35, .6, .45, .85)):                                     # the small chart, standing on the page
        bx = x + 22 + j * 30
        by0, by1 = y + d * .78, y + d * .78
        zz = z - 40 * .78
        s.poly([P(bx, by0, zz), P(bx + 18, by0, zz), P(bx + 18, by0 - d * .5 * h, zz + 40 * .5 * h), P(bx, by0 - d * .5 * h, zz + 40 * .5 * h)],
               MUST if j == 3 else NAVY, "none")
    for j in range(2):                                                               # two text lines above the chart
        yy = y + 22 + j * 16
        s.a(f'<polyline points="{s.pts(P(x + 20, yy, z - 40 * (yy - y) / d), P(x + w - 30, yy, z - 40 * (yy - y) / d))}" stroke="{mix(HAIR, INK, .45)}" stroke-width="4" stroke-linecap="round" fill="none"/>')
    s.box(80, -60, 16, 60, 60, 46, tones(MUST, .35, .25))                            # a gold agent cube that made it
    s.decal_top("chip", 110, -30, 62, 40, MINK, 1.8)
    return s.svg()


def paperwork():
    """A messy stack of paperwork on the left turns into one neat folder on the right."""
    s = Scene(1100, 800, 330, 420, 1.0, "A messy stack of paperwork, an arrow, and one neat closed folder")
    s.platform(-320, -90, 210, 200, 16)
    r = 7
    for k in range(14):                                                              # the messy stack: sheets askew
        r = (r * 9301 + 49297) % 233280
        dx = (r / 233280 - .5) * 36
        r = (r * 9301 + 49297) % 233280
        dy = (r / 233280 - .5) * 30
        _sheet(s, -295 + dx, -70 + dy, 16 + k * 6, 130, 150, 3)
    s.route([(-90, 10, 60), (0, 10, 60)], sw=5, color=MUST)
    s.platform(20, -110, 240, 230, 16)
    s.box(50, -80, 16, 170, 170, 26, tones(MUST, .3, .22))                            # the folder, closed
    s.box(50, -80, 42, 70, 30, 8, tones(MUST, .38, .26))                              # its tab
    s.decal_top("check", 135, 5, 42, 80, MINK, 2.4)
    return s.svg()


if __name__ == "__main__":
    open("contract.svg","w").write(contract())
    print("wrote contract.svg")
