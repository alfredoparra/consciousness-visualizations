# Consciousness visualizations

Animations of ideas from electromagnetic-field and wave-computing theories of consciousness: how neurons create fields, how the brain might build a real-time "world simulation" out of waves, and how that picture might be stored and processed. The source articles (QRI, Steven Lehar, Susan Pockett, Cube Flipper, and others) are in [`sources/`](sources/).

Every frame is computed by Python: the fields come from simple physics models (dipole potentials, a wave equation, eigenmodes). Nothing is AI-generated video. The aim is for each visual to show the *mechanism* described in the sources, and for the simplifications to be stated explicitly (see each script's docstring).

## Videos

The small 720p copies in [`videos/`](videos/) are committed. Full-quality renders go to `renders/`, which is gitignored.

| Video | Length | What it shows |
|---|---|---|
| [`02_brain_to_basketball`](videos/02_brain_to_basketball.mp4) | 89 s | **The main video.** A brain photo, zooming into the cortex. Then the cortical column: dipoles, the thalamic relay, ephaptic coupling and the local field potential. Synchrony becomes a traveling wave, the 3D sheet appears and the view rotates to look from above, colored ripples follow, and then a basketball is rebuilt in the field: edges, then grassfire fronts, then skeleton, then reverse grassfire fill, then eigenmode detail. |
| [`00_neurons_make_fields`](videos/00_neurons_make_fields.mp4) | 38.5 s | The cortical-column explanation on its own (after Susan Pockett). It's included in 02. |
| [`01_spikes_to_picture`](videos/01_spikes_to_picture.mp4) | 24 s | An early sketch: a bunny appears as a patch of raised permittivity that traps waves (after *The Electrostatic Brain*). Kept for reference. |

## Rendering

Requirements: Python 3 with `numpy`, `scipy` and `Pillow`, plus `ffmpeg` on the PATH.

```bash
python animations/02_brain_to_basketball/render.py                 # 720p, ~12 min, also writes videos/ copy
python animations/02_brain_to_basketball/render.py --height 1080   # full HD
python animations/02_brain_to_basketball/render.py --stills 12 40 75   # PNG previews -> renders/stills/
python animations/00_neurons_make_fields/render.py                 # 1080p, ~5 min
python animations/01_spikes_to_picture/render.py                   # 720p, ~2.5 min
python tools/web_video.py                                          # 720p copies of everything in renders/ -> videos/
```

The simulations are seeded, so renders are deterministic. Stills are the fastest way to check a change. The simulation still runs from t = 0 up to the latest still you ask for, so late timestamps take longer.

## Layout

```
animations/NN_name/render.py   one self-contained script per video (timeline + captions at the top)
tools/web_video.py             makes the small committable copies in videos/
assets/                        third-party images; licences in assets/ATTRIBUTION.md
sources/                       the articles the animations are based on
videos/                        committed 720p videos
renders/                       full-quality renders and stills (gitignored)
```

## Credits and licences

- The brain photo is "Left side of the brain" by \_DJ\_, [CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/), via Wikimedia Commons. It's credited on screen. Because of the ShareAlike clause, a published video that includes it may have to be released under CC BY-SA as well. See [`assets/ATTRIBUTION.md`](assets/ATTRIBUTION.md).
- The articles in `sources/` belong to their authors and are here for reference only.
