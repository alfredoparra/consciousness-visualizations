"""
Small, committable copies of the rendered videos.

Full-quality renders go to renders/ (gitignored); this writes 720p H.264 copies
to videos/, which are small enough to commit and push.

Usage:
    python tools/web_video.py                  # every renders/*.mp4
    python tools/web_video.py renders/02_brain_to_basketball.mp4
"""

import glob
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
HEIGHT = 720
CRF = 26


def make_web_copy(src, height=HEIGHT, crf=CRF):
    dst = os.path.join(ROOT, "videos", os.path.basename(src))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vf", f"scale=-2:{height}",
         "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", dst],
        check=True)
    return dst


if __name__ == "__main__":
    srcs = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, "renders", "*.mp4")))
    for s in srcs:
        d = make_web_copy(s)
        print(f"{d}  ({os.path.getsize(d) / 1e6:.1f} MB)")
