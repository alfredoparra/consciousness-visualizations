---
name: preview-render
description: Preview and render one of this repo's animation videos - render PNG stills at chosen timestamps, inspect them, then do the full background render and verify the finished file. Use after any edit to animations/*/render.py, or when the user asks to render, re-render, preview or check a video.
---

# Preview and render a video

Full renders take 5–12 minutes, so always check stills before starting one.

## 1. Pick timestamps

Read the `T_*` constants and `CAPTIONS` at the top of the script to find the seconds where the change is visible. For a transition, pick its start, middle and end. Pick 3–8 timestamps.

## 2. Render stills

```bash
rm -f renders/stills/NN_t*.png
python3 animations/NN_name/render.py --stills 12.0 40.5 75.2
```

- The output is `renders/stills/NN_tSS.SS.png`, with the filename rounded to the nearest frame. If an expected file is missing, run `ls renders/stills/`.
- The simulation runs from t = 0 to the latest still, so late timestamps take 1–2 minutes. That's normal.
- Video 02 defaults to 720p. Pass `--height 1080` only if the user wants full HD.

## 3. Inspect

Open each PNG with the **Read** tool and look at it. Check that:
- the intended effect is actually visible and reads clearly at a glance;
- nothing is clipped, saturated or overlapping, especially captions over the content and panels over the subject;
- colors follow the conventions in `CLAUDE.md` (blue/red = sink/source in the column views; color = frequency in the lattice);
- the frames before and after a crossfade match up.

For motion such as waves or fronts, render 3–4 stills about 0.1–0.2 s apart and compare them, for example tiled into one image with PIL. When a judgment is numeric (contrast, an energy ratio), compute it instead of eyeballing.

Fix, re-render the affected stills, and repeat.

## 4. Full render

Run it in the background (`run_in_background: true`) and tell the user it's running and roughly how long it will take:

```bash
start=$(date +%s); python3 animations/NN_name/render.py > renders/NN_render.log 2>&1; \
  echo "exit=$? time=$(( $(date +%s) - start ))s"; tail -3 renders/NN_render.log
```

Video 02 writes its `videos/` copy itself. For the other videos, run `python3 tools/web_video.py renders/NN_name.mp4` afterwards.

Before a long render, if crop, zoom or camera maths changed, call that scene's frame function for every t in its range to catch crashes early.

## 5. Verify the finished file

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height:format=duration -of csv=p=0 videos/NN_name.mp4
ffmpeg -loglevel error -y -ss 30 -i videos/NN_name.mp4 -frames:v 1 renders/stills/check_30.png
```

Read two or three of these frames from the finished, compressed file. Then report the duration, size, render time and anything you noticed. Say clearly that you checked stills, not the video in motion.
