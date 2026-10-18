"""
From spikes to a picture.

A sheet of neurons sits in a wave medium (2D scalar wave equation, a stand-in
for the EM field). Every spike injects a small wave pulse into the medium.

Following "The Electrostatic Brain" (Fakhri, Percy, Gómez-Emilsson 2024):
recent firing raises the local permittivity of the substrate. Waves slow down
inside the active patch, their wavelength shrinks, and at the patch boundary
they are partially reflected / trapped by total internal reflection. The image
of the stimulus therefore appears *in the field*, as a resonating patch, rather
than being drawn by the neurons directly.

Usage:
    python render.py                 # full video -> renders/01_spikes_to_picture.mp4
    python render.py --stills 2 8 18 # only save PNG stills at those seconds
"""

import argparse
import os
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter, zoom

# ---------------------------------------------------------------- parameters
SIM_W, SIM_H = 640, 360          # simulation grid
UPSCALE = 2                       # output = 1280 x 720
OUT_W, OUT_H = SIM_W * UPSCALE, SIM_H * UPSCALE
FPS = 30
DURATION = 24.0                   # seconds
STEPS_PER_FRAME = 10

C0 = 0.5                          # wave speed (Courant number) in background
EPS_MAX = 8.0                     # relative permittivity of a fully active patch
DAMPING = 0.009                   # loss per step in resting tissue
DAMPING_ACTIVE = 0.0005           # loss per step inside a fully active patch (resonator)
SPONGE = 36                       # absorbing border width (cells)

NEURON_SPACING = 8.0              # cells
RICKER_F = 1 / 32                 # pulse centre frequency (cycles / step)
REFRACTORY = 110                  # steps
RATE_SPONT = 0.05                 # spikes / s / neuron (video time)
RATE_DRIVEN = 2.6                 # spikes / s / neuron inside the stimulus
ACTIVITY_TAU = 1.4                # seconds; memory of recent firing
STIM_ON = 3.0                     # seconds
NEURON_FADE = (19.0, 21.5)        # fade neurons out to reveal the field alone

T_CAPTIONS = [
    (0.0, 3.0, "Spontaneous firing: every spike sends a ripple into the field"),
    (3.0, 7.5, "A stimulus arrives: neurons in its retinotopic footprint fire"),
    (7.5, 13.0, "Recent firing raises the local permittivity — waves slow down"),
    (13.0, 19.0, "Waves get trapped inside the patch: the shape appears in the field"),
    (19.0, 24.0, "The picture lives in the wave pattern, not in any single neuron"),
]

RNG = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))


# ---------------------------------------------------------------- geometry
def ellipse(xx, yy, cx, cy, rx, ry, angle_deg=0.0):
    a = np.deg2rad(angle_deg)
    dx, dy = xx - cx, yy - cy
    u = dx * np.cos(a) + dy * np.sin(a)
    v = -dx * np.sin(a) + dy * np.cos(a)
    return (u / rx) ** 2 + (v / ry) ** 2 <= 1.0


def bunny_mask(xx, yy, ox=0.0, oy=0.0, s=1.0):
    """A sitting bunny facing right, built from ellipses."""
    def e(cx, cy, rx, ry, ang=0.0):
        return ellipse(xx, yy, ox + s * cx, oy + s * cy, s * rx, s * ry, ang)
    m = e(0, 30, 78, 58)                      # body
    m |= e(-40, 52, 46, 34)                   # haunch
    m |= e(72, -22, 42, 36)                   # head
    m |= e(60, -95, 13, 46, -12)              # back ear
    m |= e(88, -92, 12, 44, 14)               # front ear
    m |= e(-82, 18, 17, 16)                   # tail
    m |= e(38, 82, 30, 9)                     # front paw
    return m


# ---------------------------------------------------------------- neurons
def make_neurons():
    xs = np.arange(SPONGE * 0.5, SIM_W - SPONGE * 0.5, NEURON_SPACING)
    ys = np.arange(SPONGE * 0.5, SIM_H - SPONGE * 0.5, NEURON_SPACING)
    gx, gy = np.meshgrid(xs, ys)
    px = gx.ravel() + RNG.uniform(-2.5, 2.5, gx.size)
    py = gy.ravel() + RNG.uniform(-2.5, 2.5, gy.size)
    return px, py


def ricker(tau):
    a = (np.pi * RICKER_F * tau) ** 2
    return (1 - 2 * a) * np.exp(-a)


# ---------------------------------------------------------------- colour
def colormap(v):
    """v in [-1, 1] -> RGB float. Negative: cyan/teal, positive: amber."""
    neg = np.array([0.15, 0.75, 1.0])
    pos = np.array([1.0, 0.62, 0.18])
    base = np.array([0.012, 0.014, 0.03])
    a = np.abs(v)[..., None] ** 0.9
    col = np.where(v[..., None] >= 0, pos, neg)
    return base + a * col


def load_font(size):
    for path in ["/System/Library/Fonts/Helvetica.ttc",
                 "/System/Library/Fonts/SFNS.ttf",
                 "/Library/Fonts/Arial.ttf"]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# ---------------------------------------------------------------- main loop
def run(stills=None, out_path=None):
    yy, xx = np.mgrid[0:SIM_H, 0:SIM_W].astype(np.float32)
    bunny = bunny_mask(xx, yy, ox=SIM_W * 0.5 - 10, oy=SIM_H * 0.5 + 5, s=1.0)

    nx, ny = make_neurons()
    n = nx.size
    ix, iy = np.round(nx).astype(int), np.round(ny).astype(int)
    in_stim = bunny[iy, ix]
    amp = np.where(in_stim, 0.45, 1.0).astype(np.float32)   # driven spikes emit weaker pulses

    # absorbing sponge at borders
    d = np.minimum.reduce([xx, yy, SIM_W - 1 - xx, SIM_H - 1 - yy])
    sponge = np.clip(1 - d / SPONGE, 0, 1) ** 2 * 0.08

    u = np.zeros((SIM_H, SIM_W), np.float32)
    u_prev = np.zeros_like(u)
    last_spike = np.full(n, -10_000, np.int64)       # step index
    flash = np.zeros(n, np.float32)                   # visual glow per neuron
    activity = np.zeros(n, np.float32)                # slow trace -> permittivity

    dt_frame = 1.0 / FPS
    pulse_len = int(3.0 / RICKER_F)
    act_decay = np.exp(-dt_frame / ACTIVITY_TAU)
    flash_decay = np.exp(-dt_frame / 0.12)

    # neuron rendering at output resolution
    ox = np.clip(np.round(nx * UPSCALE).astype(int), 0, OUT_W - 1)
    oy = np.clip(np.round(ny * UPSCALE).astype(int), 0, OUT_H - 1)

    # stimulus inset (the bunny "out there in the world")
    inset_size = 170
    iyy, ixx = np.mgrid[0:inset_size, 0:inset_size].astype(np.float32)
    inset_mask = bunny_mask(ixx, iyy, ox=inset_size * 0.47, oy=inset_size * 0.6, s=0.62)

    font = load_font(26)
    font_small = load_font(18)

    n_frames = int(DURATION * FPS)
    still_frames = None if stills is None else {int(round(s * FPS)) for s in stills}

    proc = None
    if still_frames is None:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        proc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
             "-s", f"{OUT_W}x{OUT_H}", "-r", str(FPS), "-i", "-",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow",
             out_path],
            stdin=subprocess.PIPE)

    disp_scale = 0.02
    energy_scale = 1e-4
    energy_ema = np.zeros((SIM_H, SIM_W), np.float32)
    step = 0
    for f in range(n_frames):
        t = f / FPS
        last_needed = max(still_frames) if still_frames else n_frames - 1
        if f > last_needed:
            break

        # ---- spikes for this frame (Poisson, with refractory period)
        stim_ramp = np.clip((t - STIM_ON) / 1.5, 0, 1)
        rate = RATE_SPONT + in_stim * RATE_DRIVEN * stim_ramp
        ready = (step - last_spike) > REFRACTORY
        fire = ready & (RNG.random(n) < rate * dt_frame)
        # spread spike onsets across the frame's substeps
        last_spike[fire] = step + RNG.integers(0, STEPS_PER_FRAME, fire.sum())
        flash[fire] = 1.0
        activity = activity * act_decay + fire * 0.35

        # ---- permittivity from smoothed recent activity
        act_img = np.zeros((SIM_H, SIM_W), np.float32)
        np.add.at(act_img, (iy, ix), np.minimum(activity, 1.0))
        # blurred point masses on a grid of spacing h -> density ~ value / h^2
        act_img = gaussian_filter(act_img, NEURON_SPACING * 0.6) * NEURON_SPACING ** 2
        s_field = np.clip(1.6 * act_img - 0.15, 0, 1)
        eps = 1.0 + (EPS_MAX - 1.0) * s_field
        c2 = (C0 ** 2) / eps
        loss = sponge + DAMPING + (DAMPING_ACTIVE - DAMPING) * s_field

        # ---- integrate the wave equation
        active = (step + STEPS_PER_FRAME - last_spike) < pulse_len + STEPS_PER_FRAME
        a_idx = np.nonzero(active)[0]
        for _ in range(STEPS_PER_FRAME):
            src = np.zeros_like(u)
            tau = step - last_spike[a_idx] - pulse_len / 2
            w = np.where(np.abs(tau) <= pulse_len / 2, ricker(tau), 0.0).astype(np.float32)
            np.add.at(src, (iy[a_idx], ix[a_idx]), w * amp[a_idx])
            src = gaussian_filter(src, 1.2)
            lap = (np.roll(u, 1, 0) + np.roll(u, -1, 0) + np.roll(u, 1, 1) +
                   np.roll(u, -1, 1) - 4 * u)
            u_next = 2 * u - u_prev + c2 * lap + src * 0.05
            u_next *= (1 - loss)
            u_prev, u = u, u_next
            step += 1

        flash *= flash_decay
        activity_vis = s_field
        # electric energy density ~ eps * E^2, time-averaged
        energy_ema = 0.85 * energy_ema + 0.15 * gaussian_filter(eps * u * u, 2.5)

        if still_frames is not None and f not in still_frames:
            continue

        # ---- render field
        target = np.percentile(np.abs(u), 99.8) + 1e-6
        disp_scale = max(0.92 * disp_scale + 0.08 * target, 0.004)
        e_target = np.percentile(energy_ema, 99.5) + 1e-9
        energy_scale = max(0.92 * energy_scale + 0.08 * e_target, 2e-6)
        e = np.clip(energy_ema / energy_scale, 0, 1)
        # brightness follows time-averaged wave energy: resonating regions glow,
        # lossy tissue with only passing ripples stays dim
        lum = 0.12 + 0.88 * e ** 0.8
        v = np.clip(u / disp_scale, -1, 1)
        rgb = colormap(np.sign(v) * np.abs(v) ** 0.9) * lum[..., None]
        rgb += e[..., None] ** 1.5 * np.array([0.10, 0.08, 0.13])
        # faint violet tint where permittivity is raised (the "patch")
        rgb += activity_vis[..., None] * np.array([0.05, 0.02, 0.09])
        rgb = zoom(rgb, (UPSCALE, UPSCALE, 1), order=1)

        # ---- render neurons
        neuron_alpha = 1.0 - np.clip((t - NEURON_FADE[0]) / (NEURON_FADE[1] - NEURON_FADE[0]), 0, 1)
        if neuron_alpha > 0:
            dots = np.zeros((OUT_H, OUT_W), np.float32)
            np.add.at(dots, (oy, ox), 0.5 + 3.0 * flash)
            core = gaussian_filter(dots, 1.4) * 9
            halo_src = np.zeros_like(dots)
            np.add.at(halo_src, (oy, ox), flash)
            halo = gaussian_filter(halo_src, 6.0) * 90
            glow = np.clip(core, 0, 1.6)[..., None] * np.array([0.62, 0.72, 0.95]) + \
                np.clip(halo, 0, 1)[..., None] * np.array([0.95, 0.97, 1.0]) * 0.7
            rgb = rgb + neuron_alpha * glow

        img = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
        draw = ImageDraw.Draw(img, "RGBA")

        # ---- stimulus inset
        pad = 24
        box = (pad, pad, pad + inset_size, pad + inset_size)
        draw.rectangle(box, fill=(10, 12, 20, 210), outline=(120, 130, 160, 160), width=1)
        draw.text((pad + 10, pad + 8), "the world", font=font_small, fill=(170, 180, 200, 220))
        if stim_ramp > 0:
            a = int(235 * stim_ramp)
            m = Image.fromarray((inset_mask * a).astype(np.uint8))
            col = Image.new("RGBA", (inset_size, inset_size), (245, 240, 230, 255))
            img.paste(col, (pad, pad), m)

        # ---- caption
        for t0, t1, text in T_CAPTIONS:
            if t0 <= t < t1:
                fade = min(1.0, (t - t0) / 0.5, (t1 - t) / 0.5)
                tw = draw.textlength(text, font=font)
                x0 = (OUT_W - tw) / 2
                draw.text((x0, OUT_H - 58), text, font=font,
                          fill=(235, 238, 245, int(255 * max(fade, 0))))

        frame = np.asarray(img)
        if proc is not None:
            proc.stdin.write(frame.tobytes())
        else:
            p = os.path.join(ROOT, "renders", "stills", f"01_t{t:05.2f}.png")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            img.save(p)
            print("saved", p)

        if f % 60 == 0:
            ratio = energy_ema[bunny].mean() / (energy_ema[~bunny & (sponge == 0)].mean() + 1e-12)
            print(f"frame {f}/{n_frames}  t={t:.1f}s  spikes/frame={fire.sum()}  "
                  f"energy in/out={ratio:.1f}", flush=True)

    if proc is not None:
        proc.stdin.close()
        proc.wait()
        print("wrote", out_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stills", type=float, nargs="*", default=None)
    ap.add_argument("--out", default=os.path.join(ROOT, "renders", "01_spikes_to_picture.mp4"))
    args = ap.parse_args()
    run(stills=args.stills, out_path=args.out)
