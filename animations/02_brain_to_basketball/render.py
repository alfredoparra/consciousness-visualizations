"""
From a brain to a basketball in the field.

  1. A human brain (photo: _DJ_, CC BY-SA 2.0, Wikimedia Commons; see
     assets/ATTRIBUTION.md). A small box marks the outer layer of cortex at the
     brain's top edge and we zoom straight into it, so the column that follows
     reads as a cross-section with the cortical surface at the top.
  2. The cortical column: video 00's whole explanation (dipoles, the
     thalamic relay, ephaptic coupling, the local field potential), driven by
     the same ColumnStory object. The synchronised neurons then drift into a
     travelling wave.
  3. The row of neurons turns out to be the front slice of a 3D sheet; the
     camera pulls back and orbits overhead, then crossfades into a top-down
     lattice of ~230k neurons with spontaneous ripples. Visualisation
     convention from here on: the colour of the field is its mix of
     oscillation frequencies (slow = red, fast = blue), like light.
  4. A basketball appears "out there", and the ball is rebuilt in the field
     following Steven Lehar's and Selen Atasoy's ideas (see sources/):
       a. Edges: early visual areas pass on mostly a high-passed image, so
          only the outline and the seams light up.
       b. Grassfire: fronts spread inward from every edge; where they collide
          they trace each region's skeleton (medial axis / shock lines).
          The fronts outside the ball escape outward.
       c. Reverse grassfire: the fronts rebound from the skeleton and flow back
          out, filling each region with a flat surface colour (reification).
       d. Eigenmodes: the remaining detail is added as a superposition of the
          sheet's resonant modes, low frequencies first (a Fourier series with
          the higher harmonics progressively restored, ringing included).
          For a flat rectangular sheet these modes are the DCT cosines.

Usage:
    python render.py                          # 720p -> renders/02_brain_to_basketball.mp4
    python render.py --height 1080            # full HD
    python render.py --stills 2 10 20 30 45   # quick PNG previews
    python render.py --ball-image photo.png   # use a real photo instead of the procedural ball
    python render.py --brain-image brain.jpg  # a different brain photo (on a white background)
"""

import argparse
import importlib.util
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
from scipy.fft import dctn, idctn
from scipy.ndimage import (binary_erosion, distance_transform_edt, gaussian_filter, label,
                           map_coordinates)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# reuse the cortical column from video 00
_spec = importlib.util.spec_from_file_location(
    "nmf", os.path.join(ROOT, "animations", "00_neurons_make_fields", "render.py"))
nmf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(nmf)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from web_video import make_web_copy  # noqa: E402

# All layout constants are in "design" pixels of a 1920x1080 frame; RS converts
# them to output pixels, so the same script renders at 720p (fast) or 1080p.
DW, DH = 1920, 1080
OUT_W, OUT_H, RS = 1280, 720, 720 / DH      # set by configure()
FPS = 30
BG = np.array([0.018, 0.022, 0.04], np.float32)
RNG = np.random.default_rng(11)


def configure(height):
    global OUT_W, OUT_H, RS
    OUT_H = int(height)
    OUT_W = int(round(DW * OUT_H / DH / 2)) * 2
    RS = OUT_H / DH


# ------------------------------------------------------------------ timeline
T_ZOOM = (3.4, 9.8)               # one continuous zoom: brain -> column
T_BOX = (1.0, 2.0)                # box marking where we will zoom in
T_TO_COLUMN = (7.15, 7.85)        # brain -> column crossfade (column still small)
T_STORY = 10.2                    # video 00's explanation starts (story time 0)
T_STORY_END = T_STORY + nmf.DURATION
T_WAVE_RAMP = (T_STORY_END, T_STORY_END + 2.0)   # synchrony turns into a travelling wave
SH = T_STORY_END + 3.6 - 13.3     # everything below was timed for a 13.3 s handover
T_TO_3D = (13.3 + SH, 14.0 + SH)  # 2D column -> 3D sheet, same side-on view
T_PULL = (14.0 + SH, 18.2 + SH)   # camera pulls back
T_ORBIT = (14.6 + SH, 19.2 + SH)  # camera orbits from side-on to top-down
T_ROWS = (13.6 + SH, 15.2 + SH)   # rows behind the front slice fade in
T_TO_LATTICE = (19.0 + SH, 19.8 + SH)
T_LAT_ZOOM = (19.6 + SH, 23.0 + SH)
T_WAVE_START = 16.0 + SH
T_LEGEND = 22.0 + SH
T_STIM = 25.5 + SH                # ball appears "out there"
T_EDGE = (25.8 + SH, 27.6 + SH)   # edges light up
T_FWD = 28.6 + SH                 # grassfire fronts leave the edges
V_FIRE = 13.0                     # front speed (lattice cells / s)
T_REV_END = 34.6 + SH             # by now every region is filled (checked in Lattice)
T_MODES = (35.2 + SH, 43.6 + SH)  # eigenmodes switch on, low -> high frequency
T_NEURON_FADE = (44.5 + SH, 46.5 + SH)
T_FADE_OUT = (49.0 + SH, 50.0 + SH)
DURATION = 50.0 + SH
WAVE_LAMBDA = 2400.0              # px; firing-phase gradient -> travelling waves

CAPTIONS = [
    (0.3, 3.4, "A human brain: some 86 billion neurons"),
    (3.4, T_STORY, "Zooming into its top edge, where we see the cortex in cross-section"),
] + [(T_STORY + a, T_STORY + b, text) for a, b, text in nmf.CAPTIONS] + [
    (T_STORY_END + 0.9, 13.8 + SH, "Neighbouring neurons fire slightly one after another: a travelling wave"),
] + [(a + SH, b + SH, text) for a, b, text in [
    (13.8, 16.8, "This slice is just one row: the neurons extend in every direction"),
    (16.8, 22.0, "Seen from above, the cortex is a vast sheet of neurons"),
    (22.0, 25.5, "Every spike sends a ripple into the field; its colour shows its frequency"),
    (25.5, 28.6, "Light from a basketball reaches the eyes: at first, only its edges arrive"),
    (28.6, 31.4, "Waves spread inward from the edges, like a grass fire (Steven Lehar)"),
    (31.4, 33.4, "Where the fronts collide, they trace each region's skeleton"),
    (33.4, 35.2, "Then they rebound and flow back out, filling each region in"),
    (35.2, 39.6, "Detail is added as a superposition of the sheet's resonant modes"),
    (39.6, 44.5, "Low frequencies first, then finer ones (cf. Selen Atasoy's brain harmonics)"),
    (44.5, 49.0, "The result: a replica of the ball, made of standing waves in the field"),
]]

# ------------------------------------------------------------------ lattice params
CELL = 3                          # design px per lattice cell at zoom 1
LH, LW = DH // CELL, DW // CELL
STEPS_PER_FRAME = 10
C0 = 0.5
DAMPING = 0.009
SPONGE = 30
RICKER_FB = np.array([1 / 42, 1 / 32, 1 / 24])   # R, G, B ripple bands: slow -> fast
PULSE_LENS = (3.0 / RICKER_FB).astype(int)
PULSE_LEN = int(PULSE_LENS.max())
SPONT_RATE = 0.0009               # spikes / s / neuron (video time)
FREQS = (0.9, 1.25, 1.7)          # Hz (video time) of the R, G, B field bands
SHIMMER = 0.08
BALL_D = 660                      # ball diameter (design px)
MODE_N = 256                      # eigenmode patch (lattice cells), centred on the ball
FRONT_F = np.array([1.0, 0.86, 0.62], np.float32)   # forward fronts: warm
FRONT_R = np.array([0.62, 0.86, 1.0], np.float32)   # reverse fronts: cool
SKEL_C = np.array([1.0, 0.97, 0.9], np.float32)


def smoothstep(a, b, t):
    x = np.clip((t - a) / (b - a), 0, 1)
    return x * x * (3 - 2 * x)


def smootherstep(a, b, t):
    x = np.clip((t - a) / (b - a), 0, 1)
    return x * x * x * (x * (6 * x - 15) + 10)


def load_font(size):
    for path in ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def resize_f(a, size):
    """Resize a float 2D array to (w, h) with bilinear filtering."""
    return np.asarray(Image.fromarray(a.astype(np.float32), "F").resize(size, Image.BILINEAR))


# ================================================================== basketball
def _rot(axis, deg):
    a = np.deg2rad(deg)
    c, s = np.cos(a), np.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


_PEBBLE = gaussian_filter(np.random.default_rng(5).random((64, 64, 64)), 0.6, mode="wrap")
_MOTTLE = gaussian_filter(np.random.default_rng(6).random((32, 32, 32)), 2.0, mode="wrap")


def _noise3(grid, p, freq):
    coords = ((p.reshape(-1, 3).T + 1.0) * freq) % grid.shape[0]
    out = map_coordinates(grid, coords, order=1, mode="grid-wrap")
    out = (out - grid.mean()) / (grid.std() + 1e-9)
    return out.reshape(p.shape[:-1])


def render_ball(D):
    """Procedural basketball: returns (rgb [D,D,3], alpha [D,D]) in [0,1]."""
    s = (np.arange(D) + 0.5) / D * 2 - 1
    x, y = np.meshgrid(s, s)
    r = np.sqrt(x * x + y * y)
    alpha = np.clip((1 - r) * D / 2 + 0.5, 0, 1)
    z = np.sqrt(np.clip(1 - r * r, 0, 1))
    n = np.stack([x, y, z], -1)                          # screen frame, y down
    R = _rot("z", 28) @ _rot("x", -18) @ _rot("y", 22)
    m = n @ R                                            # ball frame
    mx, my = m[..., 0], m[..., 1]

    # seams: two perpendicular great circles + two curved side seams
    d = np.minimum.reduce([np.abs(mx), np.abs(my),
                           np.abs(np.abs(mx) - (0.5 + 0.35 * my ** 2))])
    w = 0.021
    aa = max(0.4 * w, 2.0 / D)
    seam = 1 - smoothstep(w - aa, w, d)

    L = np.array([-0.45, -0.55, 0.70])
    L /= np.linalg.norm(L)
    Hv = L + np.array([0, 0, 1.0])
    Hv /= np.linalg.norm(Hv)
    diff = np.clip(n @ L, 0, 1)
    spec = np.clip(n @ Hv, 0, 1) ** 26

    peb = _noise3(_PEBBLE, m, 50)
    mot = _noise3(_MOTTLE, m, 5)
    base = np.array([0.82, 0.35, 0.10])
    col = base * (1 + 0.07 * peb[..., None]) * (1 + 0.05 * mot[..., None])
    shade = 0.20 + 0.92 * diff
    col = col * shade[..., None]
    col += (spec * (0.20 + 0.05 * peb))[..., None] * np.array([1.0, 0.88, 0.75]) * (1 - seam[..., None])
    seam_col = np.array([0.045, 0.032, 0.028]) * (0.6 + 0.7 * diff[..., None])
    col = col * (1 - seam[..., None]) + seam_col * seam[..., None]
    col *= (0.55 + 0.45 * z ** 0.35)[..., None]
    return np.clip(col, 0, 1).astype(np.float32), alpha.astype(np.float32)


def load_ball_image(path, D):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((D, D), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255.0
    rgb, al = a[..., :3], a[..., 3]
    if al.min() > 0.99:                                  # no transparency: assume a centred ball
        s = (np.arange(D) + 0.5) / D * 2 - 1
        x, y = np.meshgrid(s, s)
        al = np.clip((1 - np.sqrt(x * x + y * y)) * D / 2 + 0.5, 0, 1).astype(np.float32)
    return rgb, al


# ================================================================== brain
BRAIN_PHOTO = os.path.join(ROOT, "assets", "left_side_of_the_brain.jpg")
BRAIN_CREDIT = "Brain photo: _DJ_, CC BY-SA 2.0, via Wikimedia Commons"
BRAIN_W = 1000                    # brain width at zoom 1 (design px)
BRAIN_TARGET_X = 0.52             # zoom onto the top edge here (fraction of the brain's width)
SURFACE_Y = 90 / DH               # where the cortical surface sits in the column view
ZMAX = 30.0                       # zoom at which the box fills the frame (~ the cortex's thickness)


def zoom_level(t):
    """Zoom of the brain shot; the column is shown at scale zoom_level / ZMAX, so
    the brain's surface and the column's surface stay aligned while zooming in."""
    return np.exp(np.log(ZMAX) * smootherstep(*T_ZOOM, t))


def load_brain_photo(path):
    """Cut the brain out of its white studio background -> PIL RGBA."""
    from scipy.ndimage import binary_fill_holes, binary_opening
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im, np.float32) / 255.0
    fg = (1.0 - arr.min(-1)) > 0.07                     # anything clearly not white
    fg = binary_opening(fg, iterations=2)
    lab, _ = label(fg)
    sizes = np.bincount(lab.ravel())
    sizes[0] = 0
    fg = binary_fill_holes(lab == sizes.argmax())
    fg = binary_erosion(fg, iterations=3)               # drop the white fringe
    a = np.clip(gaussian_filter(fg.astype(np.float32), 1.5), 0, 1)
    im.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return im, a


class Brain:
    def __init__(self, path=BRAIN_PHOTO):
        print("loading brain photo...", flush=True)
        photo, a = load_brain_photo(path)
        ys, xs = np.nonzero(a > 0.5)
        k = (xs.max() - xs.min()) / BRAIN_W               # photo px per design px at zoom 1
        CW, CH = int(DW * k), int(DH * k)
        # dark canvas with a faint glow, at the photo's native resolution
        g = np.linspace(-1, 1, 96)
        gx, gy = np.meshgrid(g * 1.6, g * 0.9)
        glow = np.clip(1 - np.sqrt(gx ** 2 + gy ** 2), 0, 1) ** 2 * 0.06
        bg = (BG + glow[..., None] * np.array([0.5, 0.6, 1.0])) * 255
        canvas = Image.fromarray(bg.astype(np.uint8)).resize((CW, CH), Image.BICUBIC)
        ox = int(CW / 2 - (xs.min() + xs.max()) / 2)
        oy = int(CH * 0.47 - (ys.min() + ys.max()) / 2)
        canvas.paste(photo, (ox, oy), photo)
        self.img = canvas
        sy, sx = np.nonzero(a[::8, ::8] > 0.95)
        pick = RNG.choice(len(sx), 500, replace=False)
        self.sp = np.stack([sx[pick] * 8.0 + ox, sy[pick] * 8.0 + oy], 1)
        self.sp_f = RNG.uniform(0.3, 0.8, len(pick))
        self.sp_ph = RNG.uniform(0, 1, len(pick))
        # zoom onto the brain's top edge, so the cortical surface ends up where the
        # column's surface is: the column then reads as a cross-section of it
        tx = int(xs.min() + BRAIN_TARGET_X * (xs.max() - xs.min()))
        edge_y = int(np.argmax(a[:, tx] > 0.5))
        self.target = (ox + tx, oy + edge_y + (0.5 - SURFACE_Y) * CH / ZMAX)

    def frame(self, t):
        W, H = self.img.size
        z = zoom_level(t)
        k = smoothstep(T_ZOOM[0], T_ZOOM[0] + 2.5, t)
        ccx = W / 2 + (self.target[0] - W / 2) * k
        ccy = H / 2 + (self.target[1] - H / 2) * k
        bw, bh = W / z, H / z
        ccx = np.clip(ccx, bw / 2, W - bw / 2)          # keep the crop inside the canvas
        ccy = np.clip(ccy, bh / 2, H - bh / 2)
        box = (ccx - bw / 2, ccy - bh / 2, ccx + bw / 2, ccy + bh / 2)
        out = self.img.resize((OUT_W, OUT_H), Image.BICUBIC, box=box)
        d = ImageDraw.Draw(out, "RGBA")
        sc = OUT_W / bw
        b = np.clip(1 - ((t * self.sp_f + self.sp_ph) % 1.0) / 0.1, 0, 1)
        for (px, py), bb in zip(self.sp, b):
            if bb <= 0.02:
                continue
            ox, oy = (px - box[0]) * sc, (py - box[1]) * sc
            if 0 <= ox < OUT_W and 0 <= oy < OUT_H:
                for rr, al in ((6, 35), (3, 100), (1.4, 230)):
                    rr *= RS
                    d.ellipse([ox - rr, oy - rr, ox + rr, oy + rr], fill=(255, 245, 225, int(al * bb)))

        # the box we are about to zoom into (the final view of the zoom), fading
        # out once it nearly fills the frame
        u = np.log(z) / np.log(ZMAX)
        ba = smoothstep(*T_BOX, t) * (1 - smoothstep(0.5, 0.78, u))
        if ba > 0:
            fw, fh = W / ZMAX, H / ZMAX
            x0 = (self.target[0] - fw / 2 - box[0]) * sc
            y0 = (self.target[1] - fh / 2 - box[1]) * sc
            x1, y1 = x0 + fw * sc, y0 + fh * sc
            lw = max(2, round(3 * RS))
            d.rectangle([x0 - 1, y0 - 1, x1 + 1, y1 + 1], outline=(0, 0, 0, int(110 * ba)), width=lw + 2)
            d.rectangle([x0, y0, x1, y1], outline=(255, 255, 255, int(235 * ba)), width=lw)
        return np.asarray(out)


# ================================================================== cortex (video 00)
class Cortex:
    """The cortical column of video 00: its whole explanation (ColumnStory),
    then the synchronised neurons drift into a travelling wave."""
    TILE_X = (nmf.CX0 - 40, nmf.CX1 + 20)              # one column, design px

    def __init__(self):
        print("building column...", flush=True)
        self.story = nmf.ColumnStory()
        self.pyrs = self.story.pyrs
        self.x = np.array([n.x for n in self.pyrs])     # design px, as on screen at s = 1
        self.psi = 0.0

    def step(self, t):
        st = self.story
        if t < T_STORY:
            return
        if t < T_STORY_END:
            st.step()
            self.psi = float(np.angle(np.mean(np.exp(1j * st.theta))))
            return
        # after the story: Kuramoto coupling with a phase lag proportional to x,
        # so the synchronised neurons lock into a travelling wave (each fires
        # slightly after its left neighbour)
        dt = 1.0 / FPS
        st.t = t - T_STORY
        lag = 2 * np.pi * self.x / WAVE_LAMBDA * smoothstep(*T_WAVE_RAMP, t)
        z = np.mean(np.exp(1j * (st.theta + lag)))
        self.psi = float(np.angle(z))
        st.theta += dt * (st.omega + nmf.K_MAX * np.abs(z) * np.sin(self.psi - lag - st.theta))
        wrapped = st.theta >= 2 * np.pi
        st.theta[wrapped] -= 2 * np.pi
        st.last_evt[wrapped] = st.t
        st.ap_last[wrapped] = st.t + nmf.AP_DELAY
        fire = (RNG.random(len(st.stels)) < 1.2 * dt) & ((st.t - st.stel_last) > 0.4)
        st.stel_last[fire] = st.t
        st.compute()

    def full_view(self, img):
        return np.asarray(img.resize((OUT_W, OUT_H), Image.LANCZOS))

    def strip_view(self, img, s):
        """The column scaled by s about the frame centre, tiled with mirrored
        neighbours (at s = 1 the column sits exactly where the story drew it)."""
        x0, x1 = self.TILE_X
        W0 = x1 - x0
        tile = img.crop((x0, 0, x1, DH))
        tw, th = max(2, round(W0 * RS * s)), max(2, round(DH * RS * s))
        t_res = tile.resize((tw, th), Image.LANCZOS)
        flip = t_res.transpose(Image.FLIP_LEFT_RIGHT)
        canvas = Image.new("RGB", (OUT_W, OUT_H), tuple(int(c * 255) for c in BG))
        top = round(OUT_H / 2 - th / 2)
        K = int(OUT_W / (W0 * RS * s)) + 2
        for k in range(-K, K + 1):
            cx = OUT_W / 2 + ((x0 + W0 / 2 + k * W0) * RS - OUT_W / 2) * s
            canvas.paste(flip if k % 2 else t_res, (round(cx - tw / 2), top))
        return np.asarray(canvas)

    def frame(self, t):
        """Zoomed-in strip outside the story; the story's own framing (labels,
        electrode, trace panel) during it, with crossfades at both ends."""
        s = zoom_level(t) / ZMAX
        ov = smoothstep(T_STORY, T_STORY + 0.8, t) * (1 - smoothstep(T_STORY_END - 0.4, T_STORY_END + 0.6, t))
        if ov >= 1:
            return self.full_view(self.story.render(captions=False)).astype(np.float32) / 255
        plain = self.strip_view(self.story.render(overlay=0, others=1.0, captions=False), s)
        plain = plain.astype(np.float32) / 255
        if ov <= 0:
            return plain
        full = self.full_view(self.story.render(overlay=ov, captions=False)).astype(np.float32) / 255
        return plain * (1 - ov) + full * ov


# ================================================================== 3D sheet
class Sheet3D:
    """The column's row of pyramidal cells is the front slice of a 3D sheet.

    World frame (design px): x right, y down (cortical depth, as in the column
    view), z into the screen. At the start the camera looks along +z and the
    z = 0 row projects exactly onto the 2D column; it then pulls back and
    orbits overhead so we end up looking down onto the cortical surface.
    """
    F = 1600.0          # focal length (design px); z = 0 sits at distance F at the start
    DZ = 72.0           # row spacing, ~ the mean x spacing of the column's cells
    NZ = 75
    S_END = 0.21        # design px per unit at the end: ~15 px spacing, as the lattice at zoom 5
    SS = 2              # supersampling for line drawing

    def __init__(self, column):
        print("building 3D sheet...", flush=True)
        x0, x1 = Cortex.TILE_X
        W0 = x1 - x0
        proto = [(n.x - (x0 + x1) / 2, n.y, n.apical[-1][0] - n.x, n.apical[-1][1]) for n in column.pyrs]
        X, YS, YT, TDX, Z, ROW = [], [], [], [], [], []
        for k in range(self.NZ):
            shift = 0.0 if k == 0 else RNG.uniform(0, W0)
            for tile in range(-5, 6):
                cx = (x0 + x1) / 2 + tile * W0 + shift
                sgn = -1 if tile % 2 else 1                     # mirrored like strip_view
                for (lx, ys, tdx, yt) in proto:
                    jx, jy, jz = (0, 0, 0) if k == 0 else RNG.uniform(-14, 14, 3)
                    X.append(cx + sgn * lx + jx)
                    YS.append(ys + 1.4 * jy)
                    YT.append(yt)
                    TDX.append(sgn * tdx)
                    Z.append(k * self.DZ + jz)
                    ROW.append(k)
        self.X, self.YS, self.YT = np.array(X), np.array(YS), np.array(YT)
        self.TDX, self.Z, self.row = np.array(TDX), np.array(Z), np.array(ROW)
        n = len(X)
        ang = RNG.uniform(0, 2 * np.pi, (n, 4)) + np.arange(4) * np.pi / 2
        self.tuft = np.stack([38 * np.cos(ang), np.full((n, 4), -22.0), 38 * np.sin(ang)], -1)
        ang = RNG.uniform(0, 2 * np.pi, (n, 3)) + np.arange(3) * 2 * np.pi / 3
        self.basal = np.stack([42 * np.cos(ang), np.full((n, 3), 38.0), 42 * np.sin(ang)], -1)
        self.jit = RNG.normal(0, 0.035, n)
        self.psi = 0.0

    def step(self, t, column):
        if t < T_TO_3D[1]:
            self.psi = column.psi                               # inherit the column's rhythm
        else:
            self.psi += 2 * np.pi * 1.45 / FPS

    def camera(self, t):
        up_ = smootherstep(*T_PULL, t)
        uo = smootherstep(*T_ORBIT, t)
        S = np.exp(np.log(self.S_END) * up_)
        th = 0.5 * np.pi * uo
        pivot = np.array([DW / 2, 540 + (300 - 540) * uo, 2700 * uo])
        fwd = np.array([0, np.sin(th), np.cos(th)])
        up = np.array([0, -np.cos(th), np.sin(th)])
        # dolly zoom: lengthen the lens as we go overhead, so the final view is
        # nearly orthographic (dendrites seen end-on as dots, not radial streaks)
        self.f = self.F * np.exp(np.log(6.0) * smootherstep(T_ORBIT[0] + 1.5, T_ORBIT[1], t))
        cam = pivot - (self.f / S) * fwd
        return cam, fwd, up, S

    def project(self, P, cam, fwd, up):
        d = P - cam
        zc = d @ fwd
        zs = np.maximum(zc, 1.0)
        sx = OUT_W / 2 + self.f * RS * d[..., 0] / zs
        sy = OUT_H / 2 - self.f * RS * (d @ up) / zs
        return sx, sy, zc

    def render(self, t):
        cam, fwd, up, S = self.camera(t)
        dist = self.f / S
        soma = np.stack([self.X, self.YS, self.Z], -1)
        top = np.stack([self.X + self.TDX, self.YT, self.Z], -1)
        sx, sy, zc = self.project(soma, cam, fwd, up)
        tx, ty, tzc = self.project(top, cam, fwd, up)

        # firing: phase advances with time and lags with x and z -> travelling waves
        ph = (self.psi / (2 * np.pi) - self.X / WAVE_LAMBDA - self.Z / WAVE_LAMBDA + self.jit) % 1.0
        flash = np.exp(-ph / 0.07)
        row_a = np.where(self.row == 0, 1.0, smoothstep(*T_ROWS, t))
        fog = np.exp(-np.maximum(zc / dist - 1.0, 0) * 1.6)
        m = 60 * RS
        vis = (zc > 30) & (tzc > 30) & (np.maximum(sx, tx) > -m) & (np.minimum(sx, tx) < OUT_W + m) & \
              (np.maximum(sy, ty) > -m) & (np.minimum(sy, ty) < OUT_H + m) & (row_a > 0.01)

        # dipole field of each firing cell: sink (blue) at the tuft, source (red) at the soma
        w = flash * fog * row_a
        sig = max(3.0, 34 * S) * RS
        fields = []
        for px, py in ((tx, ty), (sx, sy)):
            img = np.zeros((OUT_H, OUT_W), np.float32)
            ok = vis & (px >= 0) & (px < OUT_W) & (py >= 0) & (py < OUT_H)
            np.add.at(img, (py[ok].astype(int), px[ok].astype(int)), w[ok])
            fields.append(np.clip(gaussian_filter(img, sig) * 2 * np.pi * sig * sig * 0.22, 0, 1))
        rgb = BG + fields[0][..., None] * np.array([0.18, 0.5, 1.0]) * 0.8 + \
            fields[1][..., None] * np.array([1.0, 0.36, 0.22]) * 0.8
        canvas = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).resize(
            (OUT_W * self.SS, OUT_H * self.SS), Image.BILINEAR)
        d = ImageDraw.Draw(canvas, "RGBA")
        ss = self.SS
        base = np.array([0.62, 0.66, 0.78])
        hot = np.array([1.0, 0.95, 0.85])

        for i in np.nonzero(vis)[0][np.argsort(-zc[vis])]:      # far to near
            sc = self.f * RS / zc[i]                            # output px per world unit
            col = np.clip(base * (0.25 + 0.75 * fog[i]) + hot * 0.7 * flash[i] * fog[i], 0, 1)
            rgba = tuple(int(c * 255) for c in col) + (int(255 * row_a[i]),)
            wd = max(1, int(round(2.4 * sc * ss)))
            s0 = (sx[i] * ss, sy[i] * ss)
            t0 = (tx[i] * ss, ty[i] * ss)
            length = np.hypot(t0[0] - s0[0], t0[1] - s0[1])
            if length > 60 * RS * ss or sc > 0.6 * RS:
                P0 = soma[i]
                ax = self.project(np.array([P0[0], 1010.0, P0[2]]), cam, fwd, up)
                d.line([s0, (ax[0] * ss, ax[1] * ss)], fill=rgba[:3] + (int(rgba[3] * 0.6),), width=max(1, wd // 2))
                for b in self.basal[i]:
                    e = self.project(P0 + b, cam, fwd, up)
                    d.line([s0, (e[0] * ss, e[1] * ss)], fill=rgba, width=max(1, wd - 1))
                for b in self.tuft[i]:
                    e = self.project(top[i] + b, cam, fwd, up)
                    d.line([t0, (e[0] * ss, e[1] * ss)], fill=rgba, width=max(1, wd - 1))
            d.line([s0, t0], fill=rgba, width=wd)
            r = max(1.5 * RS, 8 * sc) * ss
            d.ellipse([s0[0] - r, s0[1] - r, s0[0] + r, s0[1] + r], fill=rgba)
        out = canvas.resize((OUT_W, OUT_H), Image.LANCZOS)
        return np.asarray(out).astype(np.float32) / 255


# ================================================================== lattice
def random_band_weights(n, sat=0.9):
    """Random hue -> weights of the R/G/B frequency bands (a random frequency mix)."""
    h = RNG.uniform(0, 1, n)[:, None]
    rgb = np.clip(np.concatenate([np.abs(6 * h - 3) - 1, 2 - np.abs(6 * h - 2),
                                  2 - np.abs(6 * h - 4)], 1), 0, 1)
    return (1 - sat + sat * rgb).astype(np.float32)


class Lattice:
    def __init__(self, ball_rgb, ball_a):
        print("building lattice...", flush=True)
        H, W = LH, LW
        n = H * W
        r, c = np.mgrid[0:H, 0:W]
        self.iy, self.ix = r.ravel(), c.ravel()
        self.py = self.iy + 0.5 + RNG.uniform(-0.22, 0.22, n)
        self.px = self.ix + 0.5 + RNG.uniform(-0.22, 0.22, n)

        # target image at lattice resolution (area-averaged)
        D = ball_rgb.shape[0]
        dd = D // CELL
        prem = (ball_rgb * ball_a[..., None])[:dd * CELL, :dd * CELL]
        g_rgb = prem.reshape(dd, CELL, dd, CELL, 3).mean((1, 3))
        g_a = ball_a[:dd * CELL, :dd * CELL].reshape(dd, CELL, dd, CELL).mean((1, 3))
        tgt = np.zeros((H, W, 3), np.float32)
        a = np.zeros((H, W), np.float32)
        oy, ox = H // 2 - dd // 2, W // 2 - dd // 2
        tgt[oy:oy + dd, ox:ox + dd] = g_rgb
        a[oy:oy + dd, ox:ox + dd] = g_a
        self.alpha = a
        rgb = np.where(a[..., None] > 0.02, tgt / np.maximum(a, 1e-3)[..., None], 0).astype(np.float32)
        self.rgb = rgb
        inside = a > 0.5
        lum = 0.3 * rgb[..., 0] + 0.59 * rgb[..., 1] + 0.11 * rgb[..., 2]
        self.lum = (lum / (lum.max() + 1e-9)).ravel()

        # --- a. edges: the outline and the seams (dark relative to their surround),
        # i.e. what survives the high-pass of early visual processing
        insf = inside.astype(np.float32)
        local = gaussian_filter(lum * insf, 5) / np.maximum(gaussian_filter(insf, 5), 1e-3)
        seams = inside & (lum < 0.45 * local)
        outline = inside & ~binary_erosion(inside)
        E = seams | outline
        self.E = E
        hp = np.abs(tgt - gaussian_filter(tgt, (1.5, 1.5, 0)))
        self.hp = np.clip(hp / (np.percentile(hp.max(-1)[inside], 99.5) + 1e-6), 0, 1) * 1.3
        onset = gaussian_filter(RNG.random((H, W)), 6)
        onset = (onset - onset.min()) / (np.ptp(onset) + 1e-9)
        self.edge_onset = (T_EDGE[0] + (T_EDGE[1] - T_EDGE[0] - 0.6) * onset).astype(np.float32)

        # --- b./c. grassfire: distance from the edges within each region
        body = inside & ~E
        regions, nreg = label(body)
        d_in = distance_transform_edt(~E).astype(np.float32)
        d_in[~body] = 0
        dmax = np.asarray(ndimage.maximum(d_in, regions, np.arange(1, nreg + 1)), np.float32)
        Dr = np.zeros_like(d_in)
        Dr[body] = dmax[regions[body] - 1]
        self.d_in, self.Dr, self.body = d_in, Dr, body
        print(f"  grassfire: {nreg} regions, largest inscribed radius {dmax.max():.1f} cells "
              f"-> filled by t = {T_FWD + 2 * dmax.max() / V_FIRE:.1f}s", flush=True)
        gy, gx = np.gradient(d_in)
        skel = body & (np.hypot(gx, gy) < 0.7) & (d_in > 2.0)
        self.skel = np.clip(gaussian_filter(skel.astype(np.float32), 0.7) * 2.2, 0, 1)
        self.d_out = distance_transform_edt(~inside).astype(np.float32)

        # flat surface colour per region (what the reverse grassfire fills in);
        # the seams/outline count as one more region
        lab2 = regions.copy()
        lab2[E] = nreg + 1
        idx = np.arange(1, nreg + 2)
        means = np.stack([np.asarray(ndimage.mean(rgb[..., k], lab2, idx)) for k in range(3)], 1)
        M = np.zeros_like(rgb)
        m = lab2 > 0
        M[m] = means[lab2[m] - 1]
        self.M = M.astype(np.float32)

        # --- d. eigenmodes: DCT-II cosines = Laplacian eigenmodes of a square
        # patch of sheet with free edges; we expand the detail the flat surfaces
        # still lack (target - M) and switch modes on from low to high frequency
        N = MODE_N
        cy, cx = oy + dd // 2, ox + dd // 2
        self.sl = (slice(cy - N // 2, cy + N // 2), slice(cx - N // 2, cx + N // 2))
        resid = (rgb - M)[self.sl] * (a[self.sl] > 0.02)[..., None]
        self.C = dctn(resid, axes=(0, 1), norm="ortho").astype(np.float32)
        ky, kx = np.mgrid[0:N, 0:N]
        self.kk = np.hypot(kx, ky).astype(np.float32)
        self.kc = 0.0
        self.n_modes = 1

        # spontaneous ripples (as in video 01), in three frequency bands
        # (R slow / long wavelength ... B fast / short)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        dd_ = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy])
        self.loss = (np.clip(1 - dd_ / SPONGE, 0, 1) ** 2 * 0.08 + DAMPING).astype(np.float32)
        self.u = np.zeros((3, H, W), np.float32)
        self.u_prev = np.zeros_like(self.u)
        self.last = np.full(n, -10 ** 7, np.int64)
        self.cw = np.zeros((n, 3), np.float32)
        self.step_i = 0
        self.flash = np.zeros(n, np.float32)
        self.rip_scale = np.full(3, 0.02, np.float32)
        sm = gaussian_filter(RNG.normal(size=(H, W)), 25)
        self.phi_s = (2.5 * sm / sm.std()).astype(np.float32)   # smooth phase map for the shimmer
        self._maps_t = None

    # ---------------------------------------------------------- staged maps
    def maps(self, t):
        """Grids describing the ball's construction at time t (cached per frame)."""
        if self._maps_t == t:
            return self._m
        r_f = V_FIRE * (t - T_FWD)                        # radius of the forward fronts
        d, Dr = self.d_in, self.Dr
        edge = self.E * smoothstep(self.edge_onset, self.edge_onset + 0.6, t)
        fwd = self.body * (r_f < Dr + 1.0) * np.exp(-((d - r_f) / 1.4) ** 2)
        d_rev = 2 * Dr - r_f                              # reverse fronts, back from the skeleton
        rev_on = self.body & (r_f >= Dr)
        rev = rev_on * (d_rev > -1.5) * np.exp(-((d - d_rev) / 1.4) ** 2)
        fill = rev_on * np.clip((d - d_rev) / 1.5 + 0.5, 0, 1)
        fill_e = self.E * smoothstep(T_REV_END - 0.6, T_REV_END + 0.4, t)
        fill = np.maximum(fill, fill_e)
        skel = self.skel * (np.exp(-((r_f - d) / 2.5) ** 2) + 0.45 * (r_f > d)) * \
            (1 - 0.75 * fill) * (1 - smoothstep(T_MODES[0], T_MODES[0] + 2.0, t))
        out = (self.d_out > 0.5) * np.exp(-((self.d_out - r_f) / 1.8) ** 2) * np.exp(-self.d_out / 45)
        self._m = dict(edge=edge.astype(np.float32), fwd=fwd.astype(np.float32),
                       rev=rev.astype(np.float32), fill=fill.astype(np.float32),
                       skel=skel.astype(np.float32), out=out.astype(np.float32))
        self._maps_t = t
        return self._m

    def picture(self, t):
        """Colours the filled field shows: flat region colours plus the detail
        restored so far by the eigenmodes."""
        u = smoothstep(*T_MODES, t)
        if u <= 0:
            self.kc, self.n_modes = 0.0, 1
            return self.M
        kmax = MODE_N * 1.42
        self.kc = np.exp(np.log(0.5) + (np.log(kmax) - np.log(0.5)) * u)
        w = np.clip(self.kc - self.kk + 0.5, 0, 1)        # each mode fades in over one step of k
        self.n_modes = int(round(w.sum()))
        rec = idctn(self.C * w[..., None], axes=(0, 1), norm="ortho")
        img = self.M.copy()
        img[self.sl] += rec
        return np.clip(img, 0, None)

    # ---------------------------------------------------------- simulation
    def step(self, t):
        dt = 1.0 / FPS
        n = self.flash.size
        mp = self.maps(t)
        rs = SPONT_RATE * (1 - 0.6 * smoothstep(T_STIM, T_STIM + 2, t))
        spont = RNG.random(n) < rs * dt
        # neurons fire where the construction is happening: on the edges, on the
        # fronts, and (halftone) inside the filled surfaces
        rate = (3.0 * mp["edge"] * (1 - mp["fill"]) + 5.0 * (mp["fwd"] + mp["rev"]) + 3.0 * mp["skel"] +
                mp["fill"] * self.alpha * (0.04 + 0.9 * self.lum.reshape(LH, LW))).ravel()
        drive = RNG.random(n) < rate * dt
        self.flash[spont | drive] = 1.0

        ok = spont & ((self.step_i - self.last) > PULSE_LEN)
        self.last[ok] = self.step_i + RNG.integers(0, STEPS_PER_FRAME, ok.sum())
        self.cw[ok] = random_band_weights(ok.sum())
        idx = np.nonzero((self.step_i + STEPS_PER_FRAME - self.last) < PULSE_LEN + STEPS_PER_FRAME)[0]
        c2 = C0 ** 2
        for _ in range(STEPS_PER_FRAME):
            src = np.zeros_like(self.u)
            age = self.step_i - self.last[idx]
            for c in range(3):
                tau = age - PULSE_LENS[c] / 2
                a = (np.pi * RICKER_FB[c] * tau) ** 2
                w = np.where(np.abs(tau) <= PULSE_LENS[c] / 2, (1 - 2 * a) * np.exp(-a), 0.0)
                np.add.at(src[c], (self.iy[idx], self.ix[idx]), (w * self.cw[idx, c]).astype(np.float32))
            src = gaussian_filter(src, (0, 1.2, 1.2))
            lap = (np.roll(self.u, 1, 1) + np.roll(self.u, -1, 1) + np.roll(self.u, 1, 2) +
                   np.roll(self.u, -1, 2) - 4 * self.u)
            u_next = (2 * self.u - self.u_prev + c2 * lap + src * 0.05) * (1 - self.loss)
            self.u_prev, self.u = self.u, u_next
            self.step_i += 1

        self.flash *= np.exp(-dt / 0.12)
        if t < T_LAT_ZOOM[1]:
            # per-band display scale, so slow and fast ripples read equally bright
            target = np.percentile(np.abs(self.u).reshape(3, -1), 99.8, axis=1) + 1e-6
            self.rip_scale = np.maximum(0.9 * self.rip_scale + 0.1 * target, 1e-4)

    def grid_image(self, t):
        mp = self.maps(t)
        fill = mp["fill"] * self.alpha
        pic = self.picture(t)
        shim = np.stack([np.cos(2 * np.pi * FREQS[c] * t + self.phi_s) for c in range(3)], -1)
        field = fill[..., None] * pic * (1 + SHIMMER * shim)
        edge = mp["edge"] * (1 - mp["fill"])
        field += self.hp * (0.35 + 0.65 * edge[..., None]) * edge[..., None]
        field += mp["fwd"][..., None] * FRONT_F * 0.9 + mp["out"][..., None] * FRONT_F * 0.55
        field += mp["rev"][..., None] * FRONT_R * 0.9 * (1 - 0.5 * mp["fill"][..., None])
        field += mp["skel"][..., None] * SKEL_C * 0.85

        rv = np.clip(np.abs(self.u) / self.rip_scale[:, None, None], 0, 1) ** 0.9
        gain = 0.6 * (1 - 0.5 * smoothstep(T_STIM, T_STIM + 4, t))
        cover = self.alpha * np.maximum(mp["fill"], 0.7 * smoothstep(T_EDGE[0], T_FWD, t))
        rip = np.moveaxis(rv, 0, -1) * (gain * (1 - 0.9 * cover))[..., None]
        return BG + rip + field

    def render(self, t, Z, neuron_alpha):
        grid = self.grid_image(t)
        scale = CELL * RS * Z                             # output px per lattice cell
        x0 = LW / 2 - OUT_W / 2 / scale
        y0 = LH / 2 - OUT_H / 2 / scale
        box = (x0, y0, x0 + OUT_W / scale, y0 + OUT_H / scale)
        rgb = np.stack([np.asarray(Image.fromarray(grid[..., c].astype(np.float32), "F")
                                   .resize((OUT_W, OUT_H), Image.BILINEAR, box=box))
                        for c in range(3)], -1)

        if neuron_alpha > 0:
            ox = (self.px - x0) * scale
            oy = (self.py - y0) * scale
            vis = (ox >= 0) & (ox < OUT_W - 0.5) & (oy >= 0) & (oy < OUT_H - 0.5)
            oxi, oyi = np.round(ox[vis]).astype(int), np.round(oy[vis]).astype(int)
            sig = (0.45 + 0.32 * Z) * RS
            dots = np.zeros((OUT_H, OUT_W), np.float32)
            base = 0.10 + 0.30 * smoothstep(1.5, 5.0, Z)      # resting neurons visible when zoomed in
            np.add.at(dots, (oyi, oxi), (base + 2.2 * self.flash[vis]) * neuron_alpha)
            core = gaussian_filter(dots, sig) * (2 * np.pi * sig * sig)
            rgb += np.clip(core, 0, 1.5)[..., None] * np.array([0.75, 0.82, 1.0], np.float32)
            hg = 0.45 * smoothstep(1.5, 4.0, Z)
            if hg > 0:
                hs = np.zeros_like(dots)
                np.add.at(hs, (oyi, oxi), self.flash[vis] * neuron_alpha)
                sh = sig * 3.5
                halo = gaussian_filter(hs, sh) * (2 * np.pi * sh * sh) * 0.25
                rgb += (np.clip(halo, 0, 1) * hg)[..., None] * np.array([0.9, 0.95, 1.0], np.float32)
        return rgb


# ================================================================== overlays
def spectrum_bar(w, h):
    x = np.linspace(0, 1, w)
    stops = np.array([[1.0, 0.15, 0.1], [1.0, 0.75, 0.1], [0.3, 0.9, 0.3], [0.2, 0.75, 1.0], [0.35, 0.3, 1.0]])
    pos = np.linspace(0, 1, len(stops))
    col = np.stack([np.interp(x, pos, stops[:, k]) for k in range(3)], -1)
    return Image.fromarray((np.repeat(col[None], h, 0) * 255).astype(np.uint8))


def mode_tiles(n_tiles, size):
    """The lowest-frequency eigenmodes of the sheet (DCT cosines), as small tiles."""
    ks = sorted(((kx * kx + ky * ky, kx, ky) for kx in range(8) for ky in range(8)))[:n_tiles]
    s = (np.arange(size) + 0.5) / size
    tiles = []
    for _, kx, ky in ks:
        v = np.cos(np.pi * kx * s)[None, :] * np.cos(np.pi * ky * s)[:, None]
        tiles.append((np.hypot(kx, ky), (0.5 + 0.5 * v).astype(np.float32)))
    return tiles


def draw_caption(d, text, font, alpha):
    tw = d.textlength(text, font=font)
    x, y = (OUT_W - tw) / 2, 1012 * RS
    o = max(1, round(2 * RS))
    d.text((x + o, y + o), text, font=font, fill=(0, 0, 0, int(160 * alpha)))
    d.text((x, y), text, font=font, fill=(240, 242, 248, int(255 * alpha)))


def draw_mode_panel(img, d, lattice, tiles, font_tiny, alpha):
    """Panel listing the eigenmodes that are currently part of the superposition."""
    ts, gap, cols = round(50 * RS), round(8 * RS), 5
    x0, y0 = round(1590 * RS), round(335 * RS)
    col0, col1 = np.array([0.05, 0.07, 0.14]), np.array([0.85, 0.9, 1.0])
    d.text((x0, y0 - round(36 * RS)), "resonant modes of the sheet", font=font_tiny,
           fill=(200, 205, 220, int(230 * alpha)))
    for i, (k, v) in enumerate(tiles):
        on = float(np.clip(lattice.kc - k + 0.5, 0, 1))
        rgb = col0 + (col1 - col0) * v[..., None] * (0.22 + 0.78 * on)
        tile = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
        tile.putalpha(int(255 * alpha))
        x, y = x0 + (i % cols) * (ts + gap), y0 + (i // cols) * (ts + gap)
        img.paste(tile, (x, y), tile)
        if on > 0.5:
            d.rectangle([x - 1, y - 1, x + ts, y + ts], outline=(255, 255, 255, int(200 * alpha * on)), width=1)
    rows = (len(tiles) + cols - 1) // cols
    yt = y0 + rows * (ts + gap) + round(6 * RS)
    d.text((x0, yt), f"{lattice.n_modes:,} modes superposed", font=font_tiny,
           fill=(200, 205, 220, int(230 * alpha)))


# ================================================================== main
def run(stills=None, out_path=None, ball_image=None, brain_image=BRAIN_PHOTO):
    font = load_font(round(36 * RS))
    font_tiny = load_font(round(20 * RS))
    inset_d = round(230 * RS)

    if ball_image:
        ball_rgb, ball_a = load_ball_image(ball_image, BALL_D)
        inset_rgb, inset_a = load_ball_image(ball_image, inset_d)
    else:
        ball_rgb, ball_a = render_ball(BALL_D)
        inset_rgb, inset_a = render_ball(inset_d)
    inset = Image.fromarray((np.dstack([inset_rgb, inset_a]) * 255).astype(np.uint8), "RGBA")
    bar = spectrum_bar(round(300 * RS), max(2, round(14 * RS)))
    tiles = mode_tiles(20, round(50 * RS))

    brain = Brain(brain_image)
    column = Cortex()
    sheet = Sheet3D(column)
    lattice = Lattice(ball_rgb, ball_a)

    n_frames = int(DURATION * FPS)
    still_frames = None if stills is None else {int(round(s * FPS)) for s in stills}
    last_needed = max(still_frames) if still_frames else n_frames - 1

    proc = None
    if still_frames is None:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow", out_path],
            stdin=subprocess.PIPE)

    P = lambda v: round(v * RS)   # noqa: E731  design px -> output px

    for f in range(last_needed + 1):
        t = f / FPS
        if T_TO_COLUMN[0] <= t < T_TO_3D[1]:
            column.step(t)
        if T_TO_3D[0] <= t < T_TO_LATTICE[1]:
            sheet.step(t, column)
        if t >= T_WAVE_START:
            lattice.step(t)
        if still_frames is not None and f not in still_frames:
            continue

        # ---------------- compose scene layers
        frame = None
        if t < T_TO_COLUMN[1]:
            frame = brain.frame(t).astype(np.float32) / 255
        if T_TO_COLUMN[0] <= t < T_TO_3D[1]:
            strip = column.frame(t)                     # keeps zooming in, in step with the brain
            if frame is None:
                frame = strip
            else:
                k = smoothstep(*T_TO_COLUMN, t)
                frame = frame * (1 - k) + strip * k
        if T_TO_3D[0] <= t < T_TO_LATTICE[1]:
            s3 = sheet.render(t)
            if frame is None:
                frame = s3
            else:
                k = smoothstep(*T_TO_3D, t)
                frame = frame * (1 - k) + s3 * k
        if t >= T_TO_LATTICE[0]:
            Z = np.exp(np.log(5.0) * (1 - smootherstep(*T_LAT_ZOOM, t)))
            na = 1 - smoothstep(*T_NEURON_FADE, t)
            lat = lattice.render(t, Z, na)
            if frame is None:
                frame = lat
            else:
                k = smoothstep(*T_TO_LATTICE, t)
                frame = frame * (1 - k) + lat * k

        fade = 1 - smoothstep(*T_FADE_OUT, t)
        frame = frame * fade

        img = Image.fromarray((np.clip(frame, 0, 1) * 255).astype(np.uint8))
        d = ImageDraw.Draw(img, "RGBA")

        # ---------------- "the world" inset
        wa = smoothstep(T_TO_LATTICE[1], T_TO_LATTICE[1] + 1, t) * fade
        if wa > 0:
            pad, size = P(28), P(280)
            d.rectangle([pad, pad, pad + size, pad + size], fill=(10, 12, 20, int(215 * wa)),
                        outline=(120, 130, 160, int(160 * wa)), width=1)
            d.text((pad + P(12), pad + P(8)), "the world", font=font_tiny, fill=(170, 180, 200, int(220 * wa)))
            sa = smoothstep(T_STIM, T_STIM + 0.8, t) * wa
            if sa > 0:
                ins = inset.copy()
                ins.putalpha(Image.fromarray((np.asarray(ins)[..., 3] * sa).astype(np.uint8)))
                img.paste(ins, (pad + (size - inset_d) // 2, pad + P(38)), ins)

        # ---------------- spectrum legend
        la = smoothstep(T_LEGEND, T_LEGEND + 1.0, t) * fade
        if la > 0:
            lx, ly = OUT_W - P(360), OUT_H - P(150)
            d.text((lx, ly - P(34)), "field oscillation frequency", font=font_tiny,
                   fill=(200, 205, 220, int(230 * la)))
            b = bar.copy()
            b.putalpha(int(255 * la))
            img.paste(b, (lx, ly), b)
            d.text((lx, ly + P(20)), "slower", font=font_tiny, fill=(200, 205, 220, int(200 * la)))
            tw = d.textlength("faster", font=font_tiny)
            d.text((lx + P(300) - tw, ly + P(20)), "faster", font=font_tiny, fill=(200, 205, 220, int(200 * la)))

        # ---------------- eigenmode panel
        pa = smoothstep(T_MODES[0] - 0.6, T_MODES[0] + 0.2, t) * (1 - smoothstep(*T_NEURON_FADE, t))
        if pa > 0:
            draw_mode_panel(img, d, lattice, tiles, font_tiny, pa)

        # ---------------- photo credit while the brain is on screen
        ca = 1 - smoothstep(T_TO_COLUMN[0], T_TO_COLUMN[1], t)
        if ca > 0 and brain_image == BRAIN_PHOTO:
            tw = d.textlength(BRAIN_CREDIT, font=font_tiny)
            d.text((OUT_W - tw - P(23), P(25)), BRAIN_CREDIT, font=font_tiny, fill=(0, 0, 0, int(170 * ca)))
            d.text((OUT_W - tw - P(24), P(24)), BRAIN_CREDIT, font=font_tiny, fill=(200, 205, 215, int(220 * ca)))

        # ---------------- caption
        for t0, t1, text in CAPTIONS:
            if t0 <= t < t1:
                draw_caption(d, text, font, max(0.0, min(1.0, (t - t0) / 0.4, (t1 - t) / 0.4)))

        if proc is not None:
            proc.stdin.write(np.asarray(img).tobytes())
        else:
            p = os.path.join(ROOT, "renders", "stills", f"02_t{t:05.2f}.png")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p)
            print("saved", p, flush=True)
        if f % 150 == 0:
            print(f"frame {f}/{n_frames}  t={t:.1f}", flush=True)

    if proc is not None:
        proc.stdin.close()
        proc.wait()
        print("wrote", out_path)
        print("wrote", make_web_copy(out_path))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", type=float, nargs="*", default=None)
    ap.add_argument("--height", type=int, default=720, help="output height: 720 (default) or 1080")
    ap.add_argument("--ball-image", default=None, help="optional photo of a ball to use instead")
    ap.add_argument("--brain-image", default=BRAIN_PHOTO, help="brain photo on a white background")
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "02_brain_to_basketball.mp4"))
    args = ap.parse_args()
    configure(args.height)
    run(stills=args.stills, out_path=args.out, ball_image=args.ball_image, brain_image=args.brain_image)
