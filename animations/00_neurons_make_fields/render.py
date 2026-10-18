"""
How neurons make electric fields.

A cross-section of a cortical column. Following Susan Pockett ("Consciousness
Is a Thing, Not a Process", 2017; see sources/2023-06-01-an-introduction-to-
susan-pockett.md):

  1. Synaptic input at the apical tuft of a pyramidal cell lets positive ions
     in (extracellular sink, negative) and they leave near the soma
     (extracellular source, positive): the cell acts as a small dipole.
  2. Feedforward relay: thalamic afferents drive Layer 4 stellate cells, whose
     radially symmetric dendrites make sources and sinks overlap so the field
     mostly cancels ("closed field"). Their axons climb to L2/3 and excite
     pyramidal basal dendrites near the soma, giving only small, reversed,
     unsynchronised dipoles.
  3. Pyramidal cells firing out of sync give small fields that don't add up.
  4. The field acts back on the neurons (ephaptic coupling), pulling their
     timing into phase; aligned, synchronous dipoles sum into a large local
     field potential (LFP).

The extracellular potential is computed as a quasi-static sum of point
current sources, V = sum_k q_k / sqrt(r_k^2 + a^2), on a 2D slice.

Usage:
    python render.py                    # -> renders/00_neurons_make_fields.mp4
    python render.py --stills 5 12 19 33
"""

import argparse
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

OUT_W, OUT_H = 1920, 1080
FIELD_DS = 4                                   # field grid = output / 4
GW, GH = OUT_W // FIELD_DS, OUT_H // FIELD_DS
SS = 2                                         # supersampling for neuron drawing
FPS = 30
DURATION = 38.5

# cortex geometry (output pixels)
CX0, CX1 = 150, 1380
LAYERS = [("L1", 90, 190), ("L2/3", 190, 440), ("L4", 440, 590),
          ("L5", 590, 820), ("L6", 820, 980)]

TAU_SYN = 0.075           # s (video time) — synaptic current time constant
V_SCALE = 0.16            # display scale for the potential (fixed, never adaptive)
AP_DELAY = 0.3            # s after synaptic onset when the spike leaves the soma
SOFT = 1.6                # softening radius (grid cells)
PROBE = (1290, 160)       # electrode tip (output px), in layer 1

ACT1_EVENTS = [3.7, 5.6, 7.5]
# act 2: feedforward relay thalamus -> L4 stellate -> L2/3 pyramid (basal dendrites)
THAL_VOLLEYS = [9.9, 10.5, 11.1, 11.6, 12.2, 12.8, 13.3, 13.9, 14.4, 15.0, 15.5]
THAL_TRAVEL = 0.4         # s for a spike to climb a thalamic axon into L4
STEL_AXON_DELAY = 0.05    # s from stellate synaptic input to its spike
STEL_AXON_TRAVEL = 0.3    # s for that spike to climb into L2/3
BASAL_GAIN = 0.45         # feedforward input onto basal dendrites: weaker, reversed dipole
OSC_ON = 16.5
COUPLING_RAMP = (23.5, 29.5)
K_MAX = 7.0

CAPTIONS = [
    (0.0, 3.4, "A pyramidal neuron: its apical dendrite reaches up toward the cortical surface"),
    (3.4, 6.4, "Synaptic input at the top: positive ions flow in, leaving the outside negative"),
    (6.4, 9.5, "They flow back out near the cell body: the neuron becomes a tiny electric dipole"),
    (9.5, 12.8, "Sensory input arrives from the thalamus at Layer 4 stellate cells"),
    (12.8, 16.5, "Their dendrites point every way, so their fields cancel — but they relay the signal up to Layer 2/3"),
    (16.5, 23.5, "Pyramidal cells firing out of sync: small fields that don't add up"),
    (23.5, 30.0, "The field acts back on the neurons, nudging their timing (ephaptic coupling)"),
    (30.0, 38.5, "In sync, the aligned dipoles add up into a large local field potential"),
]

RNG = np.random.default_rng(3)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


def load_font(size):
    for path in ["/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ------------------------------------------------------------------ morphology
class Neuron:
    def __init__(self, kind, x, y):
        self.kind, self.x, self.y = kind, x, y
        self.mask = None          # float crop at output res
        self.glow = None
        self.box = None           # (x0, y0) of crop
        self.apical = []          # polyline soma -> tuft (output px)
        self.axon = []            # polyline soma -> down
        self.poles = []           # [(x, y, weight)] in output px; weights sum to 0


def _wiggle_path(p0, p1, n, amp):
    pts = []
    off = 0.0
    for i in range(n + 1):
        s = i / n
        off += RNG.normal(0, amp)
        off *= 0.85
        x = p0[0] + (p1[0] - p0[0]) * s + off * np.sin(np.pi * s)
        y = p0[1] + (p1[1] - p0[1]) * s
        pts.append((x, y))
    return pts


def _branch(draw, x, y, angle, length, width, depth, spread=0.6):
    """Recursive dendritic branch; angle in radians, screen coords (y down)."""
    x1 = x + length * np.cos(angle)
    y1 = y + length * np.sin(angle)
    draw.line([(x * SS, y * SS), (x1 * SS, y1 * SS)], fill=255, width=max(1, int(width * SS)))
    if depth > 0:
        for d in (-1, 1):
            if RNG.random() < 0.85:
                _branch(draw, x1, y1, angle + d * spread * RNG.uniform(0.5, 1.0),
                        length * RNG.uniform(0.5, 0.75), width * 0.7, depth - 1, spread)


def build_pyramid(x, ys, y_tuft):
    n = Neuron("pyr", x, ys)
    canvas = Image.new("L", (OUT_W * SS, OUT_H * SS), 0)
    d = ImageDraw.Draw(canvas)
    # soma
    d.polygon([((x) * SS, (ys - 17) * SS), ((x - 12) * SS, (ys + 9) * SS),
               ((x + 12) * SS, (ys + 9) * SS)], fill=255)
    # apical dendrite (tapering)
    path = _wiggle_path((x, ys - 14), (x + RNG.uniform(-12, 12), y_tuft), 16, 1.2)
    for i in range(len(path) - 1):
        w = 4.2 - 2.4 * i / len(path)
        d.line([(path[i][0] * SS, path[i][1] * SS), (path[i + 1][0] * SS, path[i + 1][1] * SS)],
               fill=255, width=int(w * SS))
    n.apical = path
    # oblique branches
    for _ in range(RNG.integers(3, 6)):
        k = RNG.integers(3, len(path) - 4)
        side = RNG.choice([-1, 1])
        _branch(d, *path[k], -np.pi / 2 + side * RNG.uniform(0.7, 1.2), RNG.uniform(22, 45), 1.6, 1)
    # apical tuft
    tx, ty = path[-1]
    for a in np.linspace(-np.pi / 2 - 1.1, -np.pi / 2 + 1.1, RNG.integers(4, 6)):
        _branch(d, tx, ty, a + RNG.normal(0, 0.15), RNG.uniform(30, 52), 1.8, 2, 0.55)
    # basal dendrites
    for a in np.linspace(np.deg2rad(20), np.deg2rad(160), RNG.integers(4, 6)):
        _branch(d, x, ys + 6, a + RNG.normal(0, 0.15), RNG.uniform(35, 60), 2.2, 2, 0.5)
    # axon
    ax = _wiggle_path((x, ys + 9), (x + RNG.uniform(-6, 6), 1010), 20, 0.6)
    for i in range(len(ax) - 1):
        d.line([(ax[i][0] * SS, ax[i][1] * SS), (ax[i + 1][0] * SS, ax[i + 1][1] * SS)],
               fill=180, width=int(1.3 * SS))
    n.axon = ax
    # current poles: sink spread over the tuft, source at/near the soma
    n.poles = [(tx, ty - 10, -0.5), (tx, ty + 18, -0.5),
               (x, ys - 8, 0.6), (x, ys + 12, 0.4)]
    # feedforward input lands on the basal dendrites: sink near the soma,
    # return current leaves along the apical trunk (reversed, shorter dipole)
    n.basal_poles = [(x, ys + 24, -0.6), (x, ys + 6, -0.4),
                     (*point_on(path, 0.3), 0.5), (*point_on(path, 0.6), 0.5)]
    _finish(n, canvas)
    return n


def build_stellate(x, y):
    n = Neuron("stel", x, y)
    canvas = Image.new("L", (OUT_W * SS, OUT_H * SS), 0)
    d = ImageDraw.Draw(canvas)
    r = 8
    d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=255)
    k = RNG.integers(6, 9)
    angles = np.linspace(0, 2 * np.pi, k, endpoint=False) + RNG.uniform(0, 1)
    for a in angles:
        _branch(d, x, y, a + RNG.normal(0, 0.1), RNG.uniform(26, 40), 1.8, 1, 0.5)
    # axon ascending into L2/3, where it contacts pyramidal basal dendrites
    ax = _wiggle_path((x, y - r), (x + RNG.uniform(-25, 25), 395), 12, 0.8)
    for i in range(len(ax) - 1):
        d.line([(ax[i][0] * SS, ax[i][1] * SS), (ax[i + 1][0] * SS, ax[i + 1][1] * SS)],
               fill=170, width=int(1.2 * SS))
    for a in (-np.pi / 2 - 0.9, -np.pi / 2, -np.pi / 2 + 0.9):
        _branch(d, *ax[-1], a + RNG.normal(0, 0.15), RNG.uniform(14, 24), 1.0, 1, 0.5)
    n.axon = ax
    # sink at the centre, sources spread on a ring: net dipole ~ 0 (closed field)
    n.poles = [(x, y, -1.0)] + [(x + 24 * np.cos(a), y + 24 * np.sin(a), 1.0 / k) for a in angles]
    _finish(n, canvas)
    return n


def _finish(n, canvas):
    bbox = canvas.getbbox()
    pad = 24 * SS
    x0 = max(0, (bbox[0] - pad) // SS * SS)
    y0 = max(0, (bbox[1] - pad) // SS * SS)
    x1 = min(OUT_W * SS, bbox[2] + pad)
    y1 = min(OUT_H * SS, bbox[3] + pad)
    crop = canvas.crop((x0, y0, x1, y1))
    crop = crop.resize((crop.width // SS, crop.height // SS), Image.BOX)
    m = np.asarray(crop, np.float32) / 255.0
    n.mask = m
    n.glow = np.clip(gaussian_filter(m, 6) * 3.0, 0, 1)
    n.box = (x0 // SS, y0 // SS)


def make_neurons():
    pyrs = []
    xs = np.linspace(CX0 + 70, CX1 - 140, 9)
    for i, x in enumerate(xs):
        # L2/3 and L5 pyramids interleaved
        pyrs.append(build_pyramid(x + RNG.uniform(-15, 15), RNG.uniform(345, 405), RNG.uniform(120, 140)))
        pyrs.append(build_pyramid(x + 60 + RNG.uniform(-15, 15), RNG.uniform(700, 770), RNG.uniform(115, 140)))
    stels = [build_stellate(x + RNG.uniform(-20, 20), RNG.uniform(480, 550))
             for x in np.linspace(CX0 + 90, CX1 - 160, 8)]
    thals = [build_thalamic(x + RNG.uniform(-20, 20))
             for x in np.linspace(CX0 + 140, CX1 - 200, 6)]
    return pyrs, stels, thals


def build_thalamic(x):
    """A thalamocortical afferent climbing from the white matter into L4."""
    n = Neuron("thal", x, 1010)
    canvas = Image.new("L", (OUT_W * SS, OUT_H * SS), 0)
    d = ImageDraw.Draw(canvas)
    path = _wiggle_path((x, 1000), (x + RNG.uniform(-20, 20), 560), 18, 0.9)
    for i in range(len(path) - 1):
        d.line([(path[i][0] * SS, path[i][1] * SS), (path[i + 1][0] * SS, path[i + 1][1] * SS)],
               fill=255, width=int(2.6 * SS))
    for a in np.linspace(-np.pi / 2 - 1.3, -np.pi / 2 + 1.3, 5):
        _branch(d, *path[-1], a + RNG.normal(0, 0.15), RNG.uniform(30, 48), 1.8, 2, 0.5)
    n.axon = path
    _finish(n, canvas)
    return n


# ------------------------------------------------------------------ helpers
def alpha_fn(t):
    """Synaptic current shape, peak 1 at t = TAU_SYN."""
    t = np.maximum(t, 0)
    return (t / TAU_SYN) * np.exp(1 - t / TAU_SYN)


def potential(poles, gx, gy):
    v = np.zeros_like(gx)
    for (px, py, q) in poles:
        if abs(q) < 1e-4:
            continue
        v += q / np.sqrt((gx - px / FIELD_DS) ** 2 + (gy - py / FIELD_DS) ** 2 + SOFT ** 2)
    return v


def potential_at(poles, x, y):
    return sum(q / np.sqrt(((x - px) / FIELD_DS) ** 2 + ((y - py) / FIELD_DS) ** 2 + SOFT ** 2)
               for (px, py, q) in poles)


def point_on(path, s):
    s = np.clip(s, 0, 1) * (len(path) - 1)
    i = min(int(s), len(path) - 2)
    f = s - i
    return (path[i][0] * (1 - f) + path[i + 1][0] * f, path[i][1] * (1 - f) + path[i + 1][1] * f)


def smoothstep(a, b, t):
    x = np.clip((t - a) / (b - a), 0, 1)
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ background
def make_background():
    bg = np.zeros((OUT_H, OUT_W, 3), np.float32)
    bg[:] = np.array([0.018, 0.022, 0.04])
    for i, (_, y0, y1) in enumerate(LAYERS):
        shade = 0.012 if i % 2 == 0 else 0.0
        bg[y0:y1, CX0 - 40:CX1 + 20] += shade
    img = Image.fromarray((bg * 255).astype(np.uint8))
    d = ImageDraw.Draw(img, "RGBA")
    for name, y0, y1 in LAYERS:
        d.line([(CX0 - 40, y0), (CX1 + 20, y0)], fill=(90, 100, 130, 70), width=1)
    d.line([(CX0 - 40, LAYERS[-1][2]), (CX1 + 20, LAYERS[-1][2])], fill=(90, 100, 130, 70), width=1)
    return np.asarray(img, np.float32) / 255.0


def draw_layer_labels(d, font_small, alpha):
    for name, y0, y1 in LAYERS:
        d.text((60, (y0 + y1) / 2 - 12), name, font=font_small, fill=(140, 150, 180, int(200 * alpha)))
    d.text((60, 990), "white matter", font=font_small, fill=(110, 120, 150, int(160 * alpha)))
    d.text((CX0 - 40, 40), "cortical surface", font=font_small, fill=(140, 150, 180, int(200 * alpha)))


# ------------------------------------------------------------------ the story
class ColumnStory:
    """The whole column explanation, one frame at a time.

    step() advances the dynamics by one frame; render() draws the current
    frame. Video 02 drives the same object (and takes over its dynamics after
    the story ends), so the state lives in attributes rather than in run().
    """

    def __init__(self):
        self.font = load_font(34)
        self.font_small = load_font(24)
        self.font_tiny = load_font(20)
        print("building neurons...", flush=True)
        self.pyrs, self.stels, self.thals = make_neurons()
        pyrs, stels, thals = self.pyrs, self.stels, self.thals
        self.hero = pyrs[8]                  # an L2/3 pyramid near the middle
        self.bg = make_background()
        self.gy, self.gx = np.mgrid[0:GH, 0:GW].astype(np.float32)

        npyr = self.npyr = len(pyrs)
        self.omega = 2 * np.pi * RNG.normal(1.45, 0.28, npyr)
        self.theta = RNG.uniform(0, 2 * np.pi, npyr)
        self.last_evt = np.full(npyr, -100.0)     # apical (feedback) synaptic input
        self.basal_last = np.full(npyr, -100.0)   # basal (feedforward) synaptic input
        self.ap_last = np.full(npyr, -100.0)      # spike leaving the soma
        self.stel_last = np.full(len(stels), -100.0)
        self.hero_idx = pyrs.index(self.hero)

        # wiring for the feedforward relay
        l23 = [i for i in range(npyr) if pyrs[i].y < 500]
        stel_x = np.array([s.x for s in stels])
        self.thal_targets = [np.argsort(np.abs(stel_x - th.axon[-1][0]))[:2] for th in thals]
        self.stel_target = [l23[int(np.argmin([abs(pyrs[j].x - s.axon[-1][0]) for j in l23]))]
                            for s in stels]
        self.thal_spikes = []                # (t_start, afferent index)
        self.stel_spikes = []                # (t_synaptic, stellate index)
        self.particles = []                  # (t_start, jitter) for the hero's ions
        self.trace = []
        self.f = -1
        self.t = 0.0
        self.compute()

    def step(self):
        """Advance the story's own dynamics by one frame."""
        self.f += 1
        f, dt = self.f, 1.0 / FPS
        t = self.t = f * dt
        for te in ACT1_EVENTS:
            if f == int(round(te * FPS)):
                self.last_evt[self.hero_idx] = te
                self.ap_last[self.hero_idx] = te + AP_DELAY
                for k in range(16):
                    self.particles.append((te + k * 0.012, RNG.uniform(-1, 1)))

        # feedforward relay: thalamus -> L4 stellate -> L2/3 basal dendrites
        for vt in THAL_VOLLEYS:
            if f == int(round(vt * FPS)):
                for a in RNG.choice(len(self.thals), 2, replace=False):
                    self.thal_spikes.append((vt, a))
        for (ts, a) in self.thal_spikes:
            if f == int(round((ts + THAL_TRAVEL) * FPS)):
                for s in self.thal_targets[a]:
                    self.stel_last[s] = t
                    self.stel_spikes.append((t, s))
        for (ts, s) in self.stel_spikes:
            if f == int(round((ts + STEL_AXON_DELAY + STEL_AXON_TRAVEL) * FPS)):
                j = self.stel_target[s]
                self.basal_last[j] = t
                self.ap_last[j] = t + 0.15

        if t >= OSC_ON:
            k = K_MAX * smoothstep(*COUPLING_RAMP, t)
            z = np.mean(np.exp(1j * self.theta))
            r, psi = np.abs(z), np.angle(z)
            self.theta += dt * (self.omega + k * r * np.sin(psi - self.theta))
            wrapped = self.theta >= 2 * np.pi
            self.theta[wrapped] -= 2 * np.pi
            self.last_evt[wrapped] = t
            self.ap_last[wrapped] = t + AP_DELAY
        self.compute()

    def compute(self):
        """Synaptic currents, current poles and the electrode reading at self.t."""
        t = self.t
        self.cur = alpha_fn(t - self.last_evt)                  # apical synaptic current
        self.bcur = alpha_fn(t - self.basal_last) * BASAL_GAIN  # basal synaptic current
        self.scur = alpha_fn(t - self.stel_last)
        poles = []
        for n, c, b in zip(self.pyrs, self.cur, self.bcur):
            if c > 1e-3:
                poles += [(px, py, q * c) for (px, py, q) in n.poles]
            if b > 1e-3:
                poles += [(px, py, q * b) for (px, py, q) in n.basal_poles]
        for n, c in zip(self.stels, self.scur):
            if c > 1e-3:
                poles += [(px, py, q * c) for (px, py, q) in n.poles]
        self.poles = poles
        self.trace.append(potential_at(poles, *PROBE))

    def render(self, overlay=1.0, others=None, captions=True):
        """overlay: opacity of labels, electrode and trace panel; others: opacity
        of the non-hero neurons (default: the story's own focus on the hero)."""
        t = self.t
        pyrs, stels, thals, hero = self.pyrs, self.stels, self.thals, self.hero
        font, font_small, font_tiny = self.font, self.font_small, self.font_tiny

        # ---------------- field
        v = potential(self.poles, self.gx, self.gy)
        u = np.tanh(v / V_SCALE).astype(np.float32)
        u_hi = np.asarray(Image.fromarray(u, "F").resize((OUT_W, OUT_H), Image.BILINEAR))
        a = np.abs(u_hi) ** 0.85 * 0.85
        col = np.where(u_hi[..., None] < 0, np.array([0.18, 0.5, 1.0]), np.array([1.0, 0.36, 0.22]))
        rgb = self.bg * (1 - a[..., None]) + col * a[..., None] * 0.9

        # equipotential lines (constant pixel width via gradient magnitude)
        step = 0.2
        gyy, gxx = np.gradient(u_hi)
        gmag = np.sqrt(gxx ** 2 + gyy ** 2) + 1e-6
        dist = np.abs(u_hi - np.round(u_hi / step) * step) / gmag
        lines = np.clip(1.0 - dist / 1.1, 0, 1) * (np.abs(u_hi) > 0.12) * (np.abs(u_hi) < 0.97)
        rgb += lines[..., None] * 0.35

        # ---------------- neurons
        if others is None:
            others = smoothstep(9.0, 10.5, t) * 0.82 + 0.18
        base_cols = {"pyr": np.array([0.62, 0.66, 0.78]), "stel": np.array([0.55, 0.75, 0.62]),
                     "thal": np.array([0.78, 0.55, 1.0])}
        for i, n in enumerate(pyrs + stels + thals):
            if n.kind == "pyr":
                act = max(self.cur[i], self.bcur[i] / BASAL_GAIN)
            elif n.kind == "stel":
                act = self.scur[i - self.npyr]
            else:
                act = 0.0
            alpha = 1.0 if n is hero else others
            x0, y0 = n.box
            h, w = n.mask.shape
            region = rgb[y0:y0 + h, x0:x0 + w]
            base = base_cols[n.kind]
            hot = np.array([1.0, 0.95, 0.85])
            c = base * (0.75 + 0.25 * alpha) + hot * act * 0.6
            m = n.mask[..., None] * alpha
            region[:] = region * (1 - m) + c * m
            region[:] += n.glow[..., None] * act * 0.35 * alpha * np.array([1.0, 0.9, 0.7])

        img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
        d = ImageDraw.Draw(img, "RGBA")
        if overlay > 0:
            draw_layer_labels(d, font_small, overlay)

        # ---------------- action potentials travelling down the axon
        def spike_dot(px, py, col):
            for rr, al in ((10, 50), (6, 110), (3, 255)):
                d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=(*col, al))

        for i, n in enumerate(pyrs):
            age = t - self.ap_last[i]
            if 0 <= age < 0.45 and (n is hero or others > 0.5):
                spike_dot(*point_on(n.axon, age / 0.45), (255, 245, 200))
        for (ts, a) in self.thal_spikes:     # sensory volley climbing a thalamic axon
            age = t - ts
            if 0 <= age < THAL_TRAVEL:
                spike_dot(*point_on(thals[a].axon, age / THAL_TRAVEL), (225, 200, 255))
        for (ts, s) in self.stel_spikes:     # stellate output climbing into L2/3
            age = t - ts - STEL_AXON_DELAY
            if 0 <= age < STEL_AXON_TRAVEL:
                spike_dot(*point_on(stels[s].axon, age / STEL_AXON_TRAVEL), (200, 255, 210))

        # label the thalamic input while it is the subject
        lab2 = smoothstep(9.5, 10.2, t) * (1 - smoothstep(16.0, 16.6, t)) * overlay
        if lab2 > 0:
            tx, ty = thals[-1].axon[len(thals[-1].axon) // 3]
            d.text((tx + 18, ty), "input from thalamus", font=font_small,
                   fill=(205, 180, 250, int(235 * lab2)))

        # ---------------- ions flowing through the hero neuron
        for (ts, jit) in self.particles:
            age = t - ts
            if 0 <= age < 0.55:
                if age < 0.1:            # entering at the tuft from outside
                    tx, ty = hero.apical[-1]
                    px, py = tx + jit * 40 * (1 - age / 0.1), ty - 30 * (1 - age / 0.1)
                elif age < 0.38:         # flowing down the apical dendrite
                    px, py = point_on(hero.apical[::-1], (age - 0.1) / 0.28)
                    px += jit * 2
                else:                    # leaving near the soma
                    s = (age - 0.38) / 0.17
                    px, py = hero.x + jit * 45 * s, hero.y + 6 + 10 * s
                fade = 1.0 if age < 0.45 else (0.55 - age) / 0.1
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 210, 90, int(230 * fade)))

        # sink / source labels during act 1
        lab = smoothstep(3.6, 4.2, t) * (1 - smoothstep(9.0, 9.6, t)) * overlay
        if lab > 0:
            tx, ty = hero.apical[-1]
            d.text((tx + 60, ty - 10), "− sink: ions flow in", font=font_small,
                   fill=(140, 190, 255, int(255 * lab)))
            d.text((hero.x + 50, hero.y - 5), "+ source: ions flow out", font=font_small,
                   fill=(255, 160, 130, int(255 * lab)))

        # ---------------- electrode + LFP trace
        if overlay > 0:
            o = overlay
            ex, ey = PROBE
            d.line([(ex, 20), (ex, ey)], fill=(200, 205, 215, int(220 * o)), width=3)
            d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 255, 255, int(255 * o)))
            d.text((ex + 12, 26), "electrode", font=font_tiny, fill=(200, 205, 215, int(220 * o)))

            px0, px1, py_mid, ph = 1460, 1880, 470, 230
            d.rectangle([px0, py_mid - ph, px1, py_mid + ph], fill=(8, 10, 20, int(230 * o)),
                        outline=(80, 90, 120, int(160 * o)))
            d.text((px0 + 14, py_mid - ph + 10), "local field potential at electrode",
                   font=font_tiny, fill=(190, 195, 215, int(230 * o)))
            d.line([(px0, py_mid), (px1, py_mid)], fill=(70, 80, 110, int(150 * o)), width=1)
            window = int(5.0 * FPS)
            tr = np.array(self.trace[-window:])
            if tr.size > 1:
                xs = px1 - (len(tr) - 1 - np.arange(len(tr))) * (px1 - px0) / window
                ys = py_mid - np.clip(tr / 0.9, -1, 1) * (ph - 30)
                d.line(list(zip(xs, ys)), fill=(255, 220, 120, int(255 * o)), width=3)
            d.text((px0 + 14, py_mid + ph - 34), "time  (slowed ~10×)", font=font_tiny,
                   fill=(140, 150, 180, int(200 * o)))
            ay = py_mid + ph - 22
            ax0 = px0 + 14 + d.textlength("time  (slowed ~10×)", font=font_tiny) + 12
            d.line([(ax0, ay), (ax0 + 50, ay)], fill=(140, 150, 180, int(200 * o)), width=2)
            d.polygon([(ax0 + 50, ay - 5), (ax0 + 58, ay), (ax0 + 50, ay + 5)],
                      fill=(140, 150, 180, int(200 * o)))

        # ---------------- caption
        if captions:
            for t0, t1, text in CAPTIONS:
                if t0 <= t < t1:
                    fade = min(1.0, (t - t0) / 0.4, (t1 - t) / 0.4)
                    tw = d.textlength(text, font=font)
                    d.text(((OUT_W - tw) / 2, 1016), text, font=font,
                           fill=(240, 242, 248, int(255 * max(fade, 0))))
        return img


# ------------------------------------------------------------------ main
def run(stills=None, out_path=None):
    story = ColumnStory()
    n_frames = int(DURATION * FPS)
    still_frames = None if stills is None else {int(round(s * FPS)) for s in stills}
    last_needed = max(still_frames) if still_frames else n_frames - 1

    proc = None
    if still_frames is None:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow", out_path],
            stdin=subprocess.PIPE)

    for f in range(last_needed + 1):
        story.step()
        t = story.t
        if still_frames is not None and f not in still_frames:
            continue
        img = story.render()
        if proc is not None:
            proc.stdin.write(np.asarray(img).tobytes())
        else:
            p = os.path.join(ROOT, "renders", "stills", f"00_t{t:05.2f}.png")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p)
            print("saved", p, flush=True)
        if f % 90 == 0:
            print(f"frame {f}/{n_frames}  t={t:.1f}  probe={story.trace[-1]:+.3f}", flush=True)

    if proc is not None:
        proc.stdin.close()
        proc.wait()
        print("wrote", out_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", type=float, nargs="*", default=None)
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "00_neurons_make_fields.mp4"))
    args = ap.parse_args()
    run(stills=args.stills, out_path=args.out)
