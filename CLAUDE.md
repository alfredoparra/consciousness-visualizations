# CLAUDE.md

Animations of consciousness-science concepts (EM-field and wave-computing theories). Read `README.md` for the overview. This file covers what you need in order to change things safely.

## Ground rules

- **Read the relevant articles in `sources/` before designing or changing an animation.** Each visual should depict the mechanism the sources describe, not a generic pretty effect. Don't claim more than they do. For example, the eigenmodes in 02 are those of a flat sheet, so the caption says "cf. Atasoy" and doesn't claim to use her connectome harmonics.
- **Keep earlier videos as references.** When the user asks for a big change in approach, make a new numbered video (`03_...`) unless they say to edit an existing one.
- **Prefer real data and assets over procedural fakes** where realism matters. The user rejected a procedurally drawn brain as looking fake. Get images from Wikimedia Commons with a clear licence, record them in `assets/ATTRIBUTION.md`, and credit them on screen.
- **State the simplifications** in the script docstring and in your reply: what's physics, what's a visual convention, what's hand-tuned.
- **Commits:** only when asked. `renders/` is gitignored; commit the `videos/` copies, which must stay under GitHub's 100 MB limit (currently 8–34 MB).

## Iteration workflow

Use the `/preview-render` skill. In short:
1. Change the script, then render stills at the affected timestamps with `--stills`.
2. Look at the PNGs in `renders/stills/` with the Read tool. Check stills before every full render, because full renders take 5–12 minutes.
3. Run the full render with `run_in_background`, then check frames pulled from the finished file with `ffmpeg -ss T -i FILE -frames:v 1 out.png`.

For a new video, use the `/new-animation` skill.

## Architecture

### `animations/00_neurons_make_fields/render.py`: the cortical column
- Coordinates are fixed **1920×1080 px**. `LAYERS`, `CX0/CX1` and `PROBE` are in those pixels.
- `ColumnStory` holds the whole explanation as an object: `step()` advances one frame (story time `self.t`), `compute()` derives currents, poles and the electrode trace, and `render(overlay, others, captions)` draws the frame. `run()` just loops over it.
- The field is the quasi-static potential `V = Σ q / sqrt(r² + SOFT²)` from current poles. Pyramidal cells are apical-sink/soma-source dipoles. Basal (feedforward) input is a weaker, reversed dipole. Stellate cells are closed fields. Sync comes from Kuramoto coupling.
- **Video 02 imports this file** (`nmf = ...exec_module`) and uses `ColumnStory`, `CAPTIONS`, `DURATION`, `K_MAX` and `AP_DELAY`. Any change here changes 02 too. Re-render both, or warn the user.

### `animations/02_brain_to_basketball/render.py`: the main video
- **Resolution-independent layout:** every constant is in *design* px (`DW×DH` = 1920×1080). `configure(height)` sets `OUT_W/OUT_H` and `RS = OUT_H / 1080`; convert design to output px with `* RS` (or `P()` in `run()`). The default is 720p; `--height 1080` gives full HD. Stills and videos must look the same at both.
- **Timeline:** all the `T_*` constants are at the top. `T_STORY` / `T_STORY_END` bracket the embedded video-00 explanation. Everything after it is written as `original_time + SH`, where `SH` shifts the post-story part. To lengthen or shorten a section, change its own constants and keep the order. `CAPTIONS` uses the same times.
- **Scenes and classes**, in order:
  - `Brain`: the photo zoom. `zoom_level(t)` drives both the photo and the column scale, so the surfaces stay aligned. `ZMAX` sets the box size.
  - `Cortex`: wraps `ColumnStory`, then switches to a traveling-wave Kuramoto with a phase lag along x. `strip_view` tiles mirrored columns.
  - `Sheet3D`: perspective projection of a 75-row lattice of simplified pyramids, with a camera pull-back, a 90° orbit and a dolly zoom (`self.f`). It's the slowest scene, because it draws each neuron's lines one at a time.
  - `Lattice`: 360×640 cells (`CELL` = 3 design px). The ripples are a 3-band wave equation (R/G/B = slow/medium/fast). The ball construction is computed **analytically from distance transforms**, not simulated: `maps(t)` gives edges, forward/reverse grassfire fronts, skeleton and fill; `picture(t)` gives flat region colors plus a DCT (eigenmode) reconstruction of the residual, with modes switched on low-frequency first.
- **Visual conventions:** in the column and 3D sheet, blue = negative (sink) and red = positive (source) potential. From the lattice on, the **color of the field = its mix of oscillation frequencies** (red slow, blue fast), with an on-screen legend. Captions explain the switch, so keep that consistent.
- Ball: `render_ball()` is procedural; `--ball-image` takes a photo instead.

### `animations/01_spikes_to_picture/render.py`
A standalone early sketch (FDTD-ish scalar wave, permittivity raised by firing). Not shared with the others.

### `tools/web_video.py`
`make_web_copy(src)` makes a 720p CRF 26 H.264 copy in `videos/`. Video 02 calls it automatically after a full render.

## Gotchas

- The simulations are stateful: a still at t = 80 s simulates all 80 s first (about 1–2 min). That's expected.
- Renders are CPU-bound Python. Typical times: 02 at 720p about 12 min, 00 at 1080p about 5 min.
- After crop or zoom maths changes, check every frame of that section for crashes before a long render (e.g. call `brain.frame(t)` in a loop). PIL `resize(box=...)` throws on negative offsets.
- The brain photo is CC BY-SA 2.0 (ShareAlike). Mention this if the user talks about publishing.
