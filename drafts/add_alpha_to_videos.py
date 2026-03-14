"""Add alpha channel to FlashHead-generated avatar videos.

FlashHead outputs yuv420p (no alpha). The reference headshot has real RGBA
transparency. This script:
1. Extracts the alpha mask from the headshot PNG
2. Crops/resizes it to match FlashHead's 512x512 face crop
3. Re-encodes each video as VP9 with alpha (yuva420p)

Usage:
    cd C:/Users/dbhav/Projects/isabelle
    .venv/Scripts/python.exe ../portfolio/drafts/add_alpha_to_videos.py
"""

import os
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

REF_IMAGE = Path(__file__).parent / "img" / "headshot-suit-transparent.png"
VIDEO_DIR = Path(__file__).parent / "assets" / "interview"


def build_alpha_mask(size=512):
    """Extract and crop alpha mask from headshot to match FlashHead's face crop.

    FlashHead uses mediapipe face detection to crop a square around the face,
    then resizes to 512x512. We replicate that crop on the alpha channel.
    """
    img = Image.open(str(REF_IMAGE)).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]

    # Find bounding box of opaque region (the person)
    rows = np.any(alpha > 0, axis=1)
    cols = np.any(alpha > 0, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Make it square (FlashHead crops a square around the face)
    h = rmax - rmin + 1
    w = cmax - cmin + 1
    side = max(h, w)
    cy = (rmin + rmax) // 2
    cx = (cmin + cmax) // 2

    # Expand to square, clamped to image bounds
    r1 = max(0, cy - side // 2)
    r2 = r1 + side
    if r2 > alpha.shape[0]:
        r2 = alpha.shape[0]
        r1 = r2 - side
    c1 = max(0, cx - side // 2)
    c2 = c1 + side
    if c2 > alpha.shape[1]:
        c2 = alpha.shape[1]
        c1 = c2 - side

    cropped = alpha[r1:r2, c1:c2]

    # Resize to target size
    mask = cv2.resize(cropped, (size, size), interpolation=cv2.INTER_AREA)

    # Soften edges slightly for clean compositing
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    print(f"[mask] Cropped alpha {cropped.shape} -> {size}x{size}")
    print(f"[mask] Transparent: {(mask == 0).sum()}, Opaque: {(mask == 255).sum()}")

    return mask


def add_alpha_to_video(video_path, alpha_mask, output_path):
    """Re-encode video with alpha channel using ffmpeg."""
    video_path = str(video_path)
    output_path = str(output_path)

    # Read video frames
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"  Video: {w}x{h} @ {fps:.0f}fps, {frame_count} frames")

    # Resize mask to match video dimensions
    mask = cv2.resize(alpha_mask, (w, h), interpolation=cv2.INTER_AREA)

    # Write RGBA frames to raw pipe, encode with ffmpeg as VP9 + alpha
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write individual RGBA PNG frames (ffmpeg can read them as image sequence)
        for i in range(frame_count):
            ret, frame = cap.read()
            if not ret:
                break
            # frame is BGR, convert to BGRA with our alpha
            bgra = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            bgra[:, :, 3] = mask
            cv2.imwrite(os.path.join(tmpdir, f"frame_{i:05d}.png"), bgra)

        cap.release()

        # Check if source has audio
        probe = subprocess.run(
            ["ffprobe", "-v", "quiet", "-select_streams", "a",
             "-show_entries", "stream=codec_name", video_path],
            capture_output=True, text=True,
        )
        has_audio = "codec_name" in probe.stdout

        # Encode with VP9 alpha (yuva420p) via ffmpeg
        cmd = [
            "ffmpeg",
            "-framerate", str(int(fps)),
            "-i", os.path.join(tmpdir, "frame_%05d.png"),
        ]
        if has_audio:
            cmd += ["-i", video_path, "-map", "0:v", "-map", "1:a", "-c:a", "libopus", "-b:a", "64k"]
        cmd += [
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-b:v", "1M",
            "-crf", "30",
            "-auto-alt-ref", "0",
            output_path, "-y",
        ]
        subprocess.run(cmd, capture_output=True)

    print(f"  Output: {output_path}")


def main():
    print("[alpha] Building alpha mask from headshot...")
    mask = build_alpha_mask(512)

    # Process all webm files
    videos = sorted(VIDEO_DIR.glob("*.webm"))
    print(f"\n[batch] Processing {len(videos)} videos...\n")

    for vp in videos:
        print(f"-- {vp.name} --")
        backup = vp.with_suffix(".webm.bak")

        # Back up original
        if not backup.exists():
            vp.rename(backup)
        else:
            # Already backed up, use backup as source
            pass

        source = backup if backup.exists() else vp
        add_alpha_to_video(source, mask, vp)
        print()

    print("[done] All videos now have alpha transparency.")


if __name__ == "__main__":
    main()
