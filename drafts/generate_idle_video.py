"""Generate idle avatar video for portfolio standby state.

Uses the same FlashHead Lite pipeline as the interview videos but with
a silent audio track, producing natural baseline motion (subtle sway,
occasional blinks) driven by the diffusion model's inherent variation.

Generates a ~10s loop at 25fps, encoded as VP9 WebM (no audio track).

Usage:
    cd C:/Users/dbhav/Projects/isabelle
    .venv/Scripts/python.exe ../portfolio/drafts/generate_idle_video.py
"""

import importlib
import os
import sys
import types
import time
import subprocess
from pathlib import Path
from collections import deque

import numpy as np

# ── Paths ──────────────────────────────────────────────────────────────
ISABELLE_ROOT = Path(r"C:\Users\dbhav\Projects\isabelle")
FLASHHEAD_DIR = Path(r"C:\Users\dbhav\Projects\SoulX-FlashHead")
CKPT_DIR = str(ISABELLE_ROOT / "models" / "flashhead" / "SoulX-FlashHead-1_3B")
WAV2VEC_DIR = str(ISABELLE_ROOT / "models" / "flashhead" / "wav2vec2-base-960h")
REF_IMAGE = str(Path(__file__).parent / "img" / "headshot-suit-transparent.png")
OUTPUT_DIR = Path(__file__).parent / "assets" / "interview"

IDLE_DURATION = 10.0  # seconds


def setup_environment():
    """Apply Windows xfuser bypass and environment fixes."""
    os.environ["TORCHDYNAMO_DISABLE"] = "1"

    if "xfuser" not in sys.modules:
        xfuser_pkg = types.ModuleType("xfuser")
        xfuser_pkg.__path__ = [
            os.path.join(sys.prefix, "Lib", "site-packages", "xfuser")
        ]
        xfuser_pkg.__package__ = "xfuser"
        sys.modules["xfuser"] = xfuser_pkg
        importlib.import_module("xfuser.core")
        importlib.import_module("xfuser.core.distributed")
        importlib.import_module("xfuser.core.long_ctx_attention")
        print("[setup] Registered minimal xfuser (bypassed __init__.py)")

    # Add FlashHead source to sys.path
    flashhead_str = str(FLASHHEAD_DIR)
    if flashhead_str not in sys.path:
        sys.path.insert(0, flashhead_str)


def generate_idle():
    """Generate idle avatar loop from silent audio."""
    import torch
    import imageio

    setup_environment()

    original_cwd = os.getcwd()
    os.chdir(str(FLASHHEAD_DIR))
    from flash_head.inference import (
        get_pipeline,
        get_base_data,
        get_infer_params,
        get_audio_embedding,
        run_pipeline,
    )
    os.chdir(original_cwd)

    # ── Initialize pipeline ────────────────────────────────────────────
    print(f"[init] Loading FlashHead Lite from {CKPT_DIR}")
    t0 = time.time()
    pipeline = get_pipeline(
        world_size=1,
        ckpt_dir=CKPT_DIR,
        model_type="lite",
        wav2vec_dir=WAV2VEC_DIR,
    )
    infer_params = get_infer_params()
    print(f"[init] Pipeline loaded in {time.time() - t0:.1f}s")

    sample_rate = infer_params["sample_rate"]
    tgt_fps = infer_params["tgt_fps"]
    frame_num = infer_params["frame_num"]
    motion_frames_num = infer_params["motion_frames_num"]
    slice_len = frame_num - motion_frames_num
    cached_audio_duration = infer_params["cached_audio_duration"]

    # ── Register reference face ────────────────────────────────────────
    print(f"[init] Reference image: {REF_IMAGE}")
    get_base_data(
        pipeline,
        cond_image_path_or_dir=REF_IMAGE,
        base_seed=42,
        use_face_crop=True,
    )
    print("[init] Reference face registered")

    # ── Generate from pure silence ──────────────────────────────────────
    total_samples = int(IDLE_DURATION * sample_rate)
    # Pure silence — no audio signal means no lip movement.
    # The diffusion model still produces natural head sway and blinks.
    audio = np.zeros(total_samples, dtype=np.float32)

    print(f"\n[idle] Generating {IDLE_DURATION:.0f}s idle video from silent audio...\n")

    cached_audio_length_sum = sample_rate * cached_audio_duration
    audio_end_idx = cached_audio_duration * tgt_fps
    audio_start_idx = audio_end_idx - frame_num
    audio_dq = deque([0.0] * cached_audio_length_sum, maxlen=cached_audio_length_sum)

    audio_slice_samples = slice_len * sample_rate // tgt_fps

    # Pad audio to fill last chunk
    remainder = len(audio) % audio_slice_samples
    if remainder > 0:
        pad_length = audio_slice_samples - remainder
        audio = np.concatenate([audio, np.zeros(pad_length, dtype=audio.dtype)])

    chunks = audio.reshape(-1, audio_slice_samples)
    generated_list = []

    for chunk_idx, audio_chunk in enumerate(chunks):
        torch.cuda.synchronize()
        ct0 = time.time()

        audio_dq.extend(audio_chunk.tolist())
        audio_array = np.array(audio_dq)
        audio_emb = get_audio_embedding(
            pipeline, audio_array, audio_start_idx, audio_end_idx
        )

        video = run_pipeline(pipeline, audio_emb)
        video = video[motion_frames_num:]

        torch.cuda.synchronize()
        ct1 = time.time()

        generated_list.append(video.cpu())
        print(f"  Chunk {chunk_idx}/{len(chunks)-1}: {ct1-ct0:.2f}s")

    # ── Encode as WebM (no audio track — it's silent) ──────────────────
    mp4_path = str(OUTPUT_DIR / "idle_tmp.mp4")
    webm_path = str(OUTPUT_DIR / "idle.webm")

    print(f"  Encoding video...")
    with imageio.get_writer(
        mp4_path, format="mp4", mode="I", fps=tgt_fps,
        codec="h264", ffmpeg_params=["-bf", "0"]
    ) as writer:
        for frames_tensor in generated_list:
            frames = frames_tensor.numpy().astype(np.uint8)
            for i in range(frames.shape[0]):
                writer.append_data(frames[i])

    # Convert to WebM (VP9, no audio) — small file, loops cleanly
    subprocess.run(
        [
            "ffmpeg", "-i", mp4_path,
            "-c:v", "libvpx-vp9", "-b:v", "800K", "-crf", "32",
            "-an",  # No audio track
            webm_path, "-y",
        ],
        capture_output=True,
    )
    os.remove(mp4_path)

    elapsed = time.time() - t0
    print(f"\n[done] {webm_path} ({elapsed:.1f}s total)")


if __name__ == "__main__":
    generate_idle()
