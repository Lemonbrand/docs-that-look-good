"""Isometric scene kit from Lemonbrand, shared for AI in Context Ep 04:
true 30 degree isometric, flat three-tone faces, LWS palette, slab platforms, glyph decals,
mustard number markers, mono labels. No blur, no gradients, no CSS shadows (PDF-safe):
the only shadow is a flat 5% ink polygon on the ground."""
import html
import math
import re

PAPER, CARD, INK, HAIR = "#F3EEE2", "#FAF7EE", "#1D1D20", "#D5D1C7"
NAVY, MUST, SLATE, SAGE, MUTED, CORAL, BRICK, MINK = ("#2F3E59", "#C9A34D", "#3E6497", "#717F7A",
                                                       "#EBE5D6", "#BB6656", "#AA3E37", "#6E5312")
C30, S30 = math.cos(math.radians(30)), 0.5
DISPLAY_W = 653.0   # CSS px a full-width figure takes on the page


def _rgb(h):
    h = h.lstrip("#"); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    A, B = _rgb(a), _rgb(b)
    return "#" + "".join(f"{round(A[i] + (B[i] - A[i]) * t):02X}" for i in range(3))


def tones(c, light=0.30, dark=0.30):
    return mix(c, CARD, light), c, mix(c, INK, dark)


PLAT = (CARD, MUTED, HAIR)
PLAT_EDGE = mix(HAIR, INK, 0.25)

G = {
    "person": '<circle cx="17" cy="12" r="5"/><path d="M7 27c1.5-5.5 5.5-8 10-8s8.5 2.5 10 8"/>',
    "people": '<circle cx="12" cy="13" r="4"/><circle cx="23" cy="13" r="4"/><path d="M4 26c1-4.5 4-6.5 8-6.5s7 2 8 6.5M15 26c1-4.5 4-6.5 8-6.5s7 2 8 6.5"/>',
    "mail": '<rect x="6" y="9" width="22" height="16" rx="2"/><path d="M6.5 10l10.5 8 10.5-8"/>',
    "phone": '<path d="M10 6h4l2 6-3 2c1.5 3.5 4 6 7.5 7.5l2-3 6 2v4c0 1.5-1.2 2.5-2.7 2.5C15 26.5 7.5 19 7.5 8.7 7.5 7.2 8.5 6 10 6z"/>',
    "play": '<rect x="5" y="8" width="24" height="18" rx="3"/><path d="M15 13l6 4-6 4z"/>',
    "mic": '<rect x="13" y="5" width="8" height="15" rx="4"/><path d="M9 16a8 8 0 0 0 16 0M17 24v5M12 29h10"/>',
    "clips": '<rect x="7" y="5" width="9" height="16" rx="1.5"/><rect x="18" y="9" width="9" height="16" rx="1.5"/><path d="M10 27h18"/>',
    "map": '<rect x="5" y="6" width="24" height="22" rx="2"/><path d="M5 14h24M5 21h24M13 6v22M21 6v22"/>',
    "chip": '<rect x="10" y="10" width="14" height="14" rx="2"/><rect x="14" y="14" width="6" height="6"/>'
            '<path d="M13 6v4M17 6v4M21 6v4M13 24v4M17 24v4M21 24v4M6 13h4M6 17h4M6 21h4M24 13h4M24 17h4M24 21h4"/>',
    "check": '<circle cx="17" cy="17" r="11"/><path d="M11.5 17.5l4 4 7-8"/>',
    "chart": '<path d="M6 28h22M9 24v-6M15 24V12M21 24v-9M27 24V7"/>',
    "doc": '<rect x="8" y="5" width="18" height="24" rx="2"/><path d="M12 11h10M12 16h10M12 21h6"/>',
    "lock": '<rect x="9" y="15" width="16" height="12" rx="2"/><path d="M12.5 15v-3.5a4.5 4.5 0 0 1 9 0V15"/><path d="M17 20v3"/>',
    "globe": '<circle cx="17" cy="17" r="11"/><path d="M6 17h22M17 6c4 4 4 18 0 22M17 6c-4 4-4 18 0 22"/>',
    "megaphone": '<path d="M6 14v6h5l10 6V8L11 14zM24 13c2 1 2 7 0 8"/>',
    "spark": '<path d="M17 5v8M17 21v8M5 17h8M21 17h8M9 9l5 5M20 20l5 5M25 9l-5 5M14 20l-5 5"/>',
    "server": '<rect x="6" y="7" width="22" height="6" rx="1.5"/><rect x="6" y="15" width="22" height="6" rx="1.5"/>'
              '<rect x="6" y="23" width="22" height="6" rx="1.5"/><path d="M10 10h3M10 18h3M10 26h3"/>',
}


class Scene:
    def __init__(self, W, H, ox, oy, k=1.0, aria="", ts=1.0):
        self.W, self.H, self.ox, self.oy, self.k, self.aria, self.ts = W, H, ox, oy, k, aria, ts
        self.out = []

    def a(self, s):
        self.out.append(s)

    def P(self, x, y, z=0.0):
        return (self.ox + (x - y) * C30 * self.k, self.oy + ((x + y) * S30 - z) * self.k)

    @staticmethod
    def pts(*ps):
        return " ".join(f"{px:.2f},{py:.2f}" for px, py in ps)

    def poly(self, ps, fill, stroke="none", sw=1.0, extra=""):
        self.a(f'<polygon points="{self.pts(*ps)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" {extra}/>')

    def box(self, x, y, z, w, d, h, tone3, edge=None, sw=1.0):
        P = self.P
        top, left, right = tone3
        e = edge or mix(tone3[1], INK, 0.45)
        x1, y1, zt = x + w, y + d, z + h
        self.poly([P(x, y1, z), P(x1, y1, z), P(x1, y1, zt), P(x, y1, zt)], left, e, sw)
        self.poly([P(x1, y, z), P(x1, y1, z), P(x1, y1, zt), P(x1, y, zt)], right, e, sw)
        self.poly([P(x, y, zt), P(x1, y, zt), P(x1, y1, zt), P(x, y1, zt)], top, e, sw)

    def shadow(self, x, y, w, d, off=10):
        P = self.P
        self.a(f'<polygon points="{self.pts(P(x+off, y+off), P(x+w+off, y+off), P(x+w+off, y+d+off), P(x+off, y+d+off))}" fill="{INK}" opacity="0.05"/>')

    def platform(self, x, y, w, d, h=16, tone3=PLAT, edge=PLAT_EDGE):
        self.shadow(x, y, w, d)
        self.box(x, y, 0, w, d, h, tone3, edge)

    def dashed_rect(self, x, y, w, d, z, col=NAVY):
        P = self.P
        self.a(f'<polygon points="{self.pts(P(x, y, z), P(x+w, y, z), P(x+w, y+d, z), P(x, y+d, z))}" fill="none" stroke="{col}" stroke-width="1.3" stroke-dasharray="6 5" opacity="0.8"/>')

    def cylinder(self, cx, cy, z, r, h, tone3, rings=True):
        top, left, right = tone3
        e = mix(left, INK, 0.45)
        rx, ry = r * math.sqrt(2) * C30 * self.k, r * math.sqrt(2) * S30 * self.k
        bx, by = self.P(cx, cy, z); tx, ty = self.P(cx, cy, z + h)
        a = self.a
        a(f'<path d="M{bx-rx:.2f},{ty:.2f} L{bx-rx:.2f},{by:.2f} A{rx:.2f},{ry:.2f} 0 0 0 {bx:.2f},{by+ry:.2f} L{bx:.2f},{ty+ry:.2f} A{rx:.2f},{ry:.2f} 0 0 1 {bx-rx:.2f},{ty:.2f}Z" fill="{left}"/>')
        a(f'<path d="M{bx:.2f},{ty+ry:.2f} L{bx:.2f},{by+ry:.2f} A{rx:.2f},{ry:.2f} 0 0 0 {bx+rx:.2f},{by:.2f} L{bx+rx:.2f},{ty:.2f} A{rx:.2f},{ry:.2f} 0 0 1 {bx:.2f},{ty+ry:.2f}Z" fill="{right}"/>')
        a(f'<path d="M{bx-rx:.2f},{ty:.2f} L{bx-rx:.2f},{by:.2f} A{rx:.2f},{ry:.2f} 0 0 0 {bx+rx:.2f},{by:.2f} L{bx+rx:.2f},{ty:.2f}" fill="none" stroke="{e}" stroke-width="1"/>')
        if rings:
            for f in (0.36, 0.68):
                yy = ty + (by - ty) * f
                a(f'<path d="M{bx-rx:.2f},{yy:.2f} A{rx:.2f},{ry:.2f} 0 0 0 {bx+rx:.2f},{yy:.2f}" fill="none" stroke="{mix(top, CARD, 0.4)}" stroke-width="1.4"/>')
        a(f'<ellipse cx="{tx:.2f}" cy="{ty:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{top}" stroke="{e}" stroke-width="1"/>')

    def figure(self, cx, cy, z, col=NAVY, scale=1.0):
        """A person: plinth, body cylinder, head."""
        s = scale
        self.box(cx - 12*s, cy - 12*s, z, 24*s, 24*s, 6*s, tones(col))
        self.cylinder(cx, cy, z + 6*s, 8*s, 22*s, tones(col, 0.28), rings=False)
        hx, hy = self.P(cx, cy, z + 6*s + 22*s + 9*s)
        r = 8.5 * s * self.k
        self.a(f'<circle cx="{hx:.2f}" cy="{hy:.2f}" r="{r:.2f}" fill="{mix(col, CARD, 0.3)}" stroke="{mix(col, INK, 0.45)}" stroke-width="1"/>')

    def decal_top(self, name, cx, cy, z, size, color, sw=1.7):
        s = size / 34 * self.k
        ox_, oy_ = self.P(cx, cy, z)
        ua, vb = C30 * math.sqrt(2) * s, S30 * math.sqrt(2) * s
        ex, ey = ox_ - ua * 17, oy_ - vb * 17
        self.a(f'<g transform="matrix({ua:.4f},0,0,{vb:.4f},{ex:.2f},{ey:.2f})" fill="none" stroke="{color}" stroke-width="{sw/s/0.9:.2f}" stroke-linecap="round" stroke-linejoin="round">{G[name]}</g>')

    def decal_left(self, name, x, y1, z, size, color, sw=1.6):
        s = size / 34 * self.k
        ex, ey = self.P(x, y1, z + size)
        self.a(f'<g transform="matrix({C30*s:.4f},{S30*s:.4f},0,{s:.4f},{ex:.2f},{ey:.2f})" fill="none" stroke="{color}" stroke-width="{sw/s:.2f}" stroke-linecap="round" stroke-linejoin="round">{G[name]}</g>')

    def decal_right(self, name, x1, y, z, size, color, sw=1.6):
        s = size / 34 * self.k
        ex, ey = self.P(x1, y, z + size)
        self.a(f'<g transform="matrix({-C30*s:.4f},{S30*s:.4f},0,{s:.4f},{ex:.2f},{ey:.2f})" fill="none" stroke="{color}" stroke-width="{sw/s:.2f}" stroke-linecap="round" stroke-linejoin="round">{G[name]}</g>')

    def ghost(self, x, y, z, w, d, h, col=NAVY):
        """An empty seat: the box's visible edges, dashed, no fill."""
        P = self.P
        x1, y1, zt = x + w, y + d, z + h
        faces = [[P(x, y1, z), P(x1, y1, z), P(x1, y1, zt), P(x, y1, zt)],
                 [P(x1, y, z), P(x1, y1, z), P(x1, y1, zt), P(x1, y, zt)],
                 [P(x, y, zt), P(x1, y, zt), P(x1, y1, zt), P(x, y1, zt)]]
        for f in faces:
            self.a(f'<polygon points="{self.pts(*f)}" fill="{CARD}" fill-opacity=".35" stroke="{col}" stroke-width="1.5" stroke-dasharray="6 5" stroke-linejoin="round"/>')

    def flag(self, x, y, z, col=MUST, h=120):
        """A pole with a pennant: a gate or milestone."""
        self.box(x - 3, y - 3, z, 6, 6, h, tones(INK, .2, .2))
        P = self.P
        a, b, c = P(x, y, z + h), P(x, y - 60, z + h - 18), P(x, y, z + h - 36)
        self.a(f'<polygon points="{self.pts(a, b, c)}" fill="{col}" stroke="{mix(col, INK, .4)}" stroke-width="1"/>')

    def route(self, pts3, dash=None, sw=2.0, color=INK, arrow=True):
        sp = [self.P(*p) for p in pts3]
        d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in sp)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.a(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{da}/>')
        if arrow:
            (x0, y0), (x1, y1) = sp[-2], sp[-1]
            ang = math.atan2(y1 - y0, x1 - x0); L, Wd = 11, 5
            bx, by = x1 - L*math.cos(ang), y1 - L*math.sin(ang)
            nx, ny = -math.sin(ang)*Wd, math.cos(ang)*Wd
            self.a(f'<polygon points="{self.pts((x1, y1), (bx+nx, by+ny), (bx-nx, by-ny))}" fill="{color}"/>')

    def marker(self, n, p3, dx=0, dy=0, r=15):
        x, y = self.P(*p3); x += dx; y += dy
        self.a(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{MUST}" stroke="{PAPER}" stroke-width="3"/>'
               f'<text class="num" x="{x:.1f}" y="{y + r*0.44:.1f}" text-anchor="middle">{n}</text>')

    def text(self, x, y, s, cls="lb", anchor="start", fill=None):
        f = f' fill="{fill}"' if fill else ""
        self.a(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{f}>{html.escape(str(s), quote=False)}</text>')

    def label(self, p3, title, sub=None, dx=0, dy=0, anchor="start"):
        x, y = self.P(*p3); x += dx; y += dy
        self.text(x, y, title, "lb", anchor)
        if sub:
            for i, s in enumerate(sub if isinstance(sub, list) else [sub]):
                self.text(x, y + 24 + i * 20, s, "sub", anchor)

    def leader(self, p0, p1):
        self.a(f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f}" stroke="{INK}" stroke-width="1" opacity="0.55" fill="none"/>'
               f'<circle cx="{p0[0]:.1f}" cy="{p0[1]:.1f}" r="2.6" fill="{INK}"/>')

    def svg(self):
        body = "".join(self.out)
        for c in ("lb", "big", "sub", "body", "num", "wnum"):
            body = body.replace(f'class="{c}"', f'class="iso-{c}"')
        style = ('<style>.iso-lb{font:600 22px "Instrument Sans",sans-serif;fill:#1D1D20;letter-spacing:-.01em}'
                 '.iso-big{font:600 28px "Instrument Sans",sans-serif;fill:#1D1D20;letter-spacing:-.015em}'
                 '.iso-sub{font:500 14px ui-monospace,Menlo,monospace;fill:#5C5A54;letter-spacing:.08em}'
                 '.iso-body{font:400 17px "Instrument Sans",sans-serif;fill:#34343a}'
                 '.iso-num{font:700 15px "Instrument Sans",sans-serif;fill:#1D1D20}'
                 '.iso-wnum{font:600 34px "Instrument Sans",sans-serif;fill:#1D1D20;letter-spacing:-.02em}</style>')
        # Readable in print, whatever the scene's scale: a figure is drawn about 6.8 in wide
        # (653 CSS px), so each class has a floor in printed size: labels about 8.5 pt, small caps 7 pt.
        scale = DISPLAY_W / self.W
        floors = {"iso-lb": 11.5, "iso-big": 13.5, "iso-sub": 9.4, "iso-body": 11.0, "iso-num": 10.0, "iso-wnum": 15.0}
        style = re.sub(r"\.(iso-[a-z]+)\{font:(\d+) ([0-9.]+)px",
                       lambda m: f".{m.group(1)}{{font:{m.group(2)} "
                                 f"{max(float(m.group(3)) * self.ts, floors.get(m.group(1), 0) / scale):.1f}px", style)
        return (f'<svg viewBox="0 0 {self.W} {self.H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{html.escape(self.aria)}">'
                f'{style}{body}</svg>')
