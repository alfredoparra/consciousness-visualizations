---
name: new-animation
description: Create a new numbered animation video in this repo (animations/NN_name/render.py) that visualises a concept from the articles in sources/. Use when the user asks for a new video or scene, a new concept to animate, or a substantially different take on an existing video.
---

# Add a new animation

## 1. Ground it in the sources

- Read the relevant articles in `sources/` in full. If the user names one that isn't there, ask for it or for the link.
- Write down, for yourself, the mechanism to depict, what the source actually claims, and what would be your own embellishment.
- Propose the story beat by beat (3–8 beats, each a caption line) together with the physics or maths model you'll use for each. For anything big, get the user's agreement first.

## 2. Choose a model that computes the effect

Prefer a simple real model over a hand-drawn effect:

| Concept | Model already used here |
|---|---|
| neurons as field sources | quasi-static dipole poles, `V = Σ q/sqrt(r²+a²)` (video 00) |
| waves, ripples, interference | 2D scalar wave equation with a sponge border (01, 02 `Lattice.step`) |
| objects as patches of slower medium | permittivity raised by firing → wave speed `c²/ε` (01) |
| synchrony, traveling waves | Kuramoto coupling, optionally with a phase lag along x (00, 02 `Cortex`) |
| grassfire / medial axis / reification | distance transforms per region (02 `Lattice.maps`) |
| harmonics / eigenmodes | DCT = Laplacian eigenmodes of a square patch (02 `Lattice.picture`) |
| holography (not built yet) | object wave + reference wave → interference plate; reconstruct by FFT / angular spectrum |

Reuse code by importing the other script the way 02 imports 00 (`importlib` → `nmf`), not by copying it.

## 3. Script conventions

Copy the structure of `animations/02_brain_to_basketball/render.py`:
- A module docstring listing the beats, the sources and the simplifications.
- Design pixels 1920×1080 with `configure(height)` / `RS` scaling, `--height` defaulting to 720, and `--stills` for previews.
- All timing in `T_*` constants and a `CAPTIONS` list at the top. Use `smoothstep` / `smootherstep` for every fade and move.
- A seeded `np.random.default_rng(...)`, so renders are deterministic.
- Frames piped to `ffmpeg` (libx264, yuv420p), then `make_web_copy()` from `tools/web_video.py`.
- Dark background `BG`, captions centred near the bottom with a drop shadow, legends and panels on the right.
- Keep the color conventions in `CLAUDE.md`. If a new scene needs a different color meaning, add a legend and a caption explaining it.

## 4. Assets

Any third-party image goes in `assets/`, with source, author and licence added to `assets/ATTRIBUTION.md` and a credit on screen while it's shown. Prefer CC BY or public domain; flag ShareAlike licences to the user.

## 5. Iterate and finish

Use the `/preview-render` skill to check stills, run the full render and verify the result. Then add the video to the table in `README.md`, and to `CLAUDE.md` if it adds architecture future sessions need to know about.
