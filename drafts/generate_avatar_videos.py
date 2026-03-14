"""Generate lip-synced avatar videos for portfolio interview section.

Uses FlashHead Lite (SoulX-FlashHead-1_3B) to produce 512x512 talking
head videos from a reference headshot + audio files.

Usage:
    cd C:/Users/dbhav/Projects/isabelle
    .venv/Scripts/python.exe ../portfolio/drafts/generate_avatar_videos.py

Outputs go to: portfolio/drafts/assets/interview/q1.webm ... q13.webm
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
AUDIO_DIR = Path(__file__).parent / "assets" / "interview"
OUTPUT_DIR = AUDIO_DIR  # overwrite .webm files in-place


def setup_environment():
    """Apply Windows xfuser bypass and environment fixes."""
    # Disable torch.compile (Triton is Linux-only)
    os.environ["TORCHDYNAMO_DISABLE"] = "1"

    # Minimal xfuser registration — bypass the __init__.py that imports
    # HunyuanDiT → MT5Tokenizer (removed in transformers 5.x)
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


def generate_all():
    """Generate avatar videos for all 8 interview audio files."""
    import torch
    import librosa
    import imageio

    setup_environment()

    # Import FlashHead with CWD set to its source dir (loads infer_params.yaml)
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
    print(f"[init] wav2vec from {WAV2VEC_DIR}")
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

    # ── Process each audio file ────────────────────────────────────────
    # Filter to only specified questions (default: all)
    only = os.environ.get("ONLY_QUESTIONS", "").strip()
    if only:
        targets = {q.strip() for q in only.split(",")}
        audio_files = sorted(f for f in AUDIO_DIR.glob("q*.wav") if f.stem in targets)
    else:
        audio_files = sorted(AUDIO_DIR.glob("q*.wav"))
    if not audio_files:
        print(f"[error] No matching q*.wav files found in {AUDIO_DIR}")
        return

    print(f"\n[batch] Generating {len(audio_files)} videos...\n")

    for audio_path in audio_files:
        stem = audio_path.stem  # q1, q2, ...
        mp4_path = str(OUTPUT_DIR / f"{stem}.mp4")
        webm_path = str(OUTPUT_DIR / f"{stem}.webm")

        print(f"-- {stem} --------------------------------------")
        t1 = time.time()

        # Load audio
        audio, _ = librosa.load(str(audio_path), sr=sample_rate, mono=True)
        audio_duration = len(audio) / sample_rate
        print(f"  Audio: {audio_duration:.1f}s ({len(audio)} samples)")

        # Streaming generation (matches generate_video.py stream mode)
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

            # Stream encode audio
            audio_dq.extend(audio_chunk.tolist())
            audio_array = np.array(audio_dq)
            audio_emb = get_audio_embedding(
                pipeline, audio_array, audio_start_idx, audio_end_idx
            )

            # Generate video chunk
            video = run_pipeline(pipeline, audio_emb)
            video = video[motion_frames_num:]

            torch.cuda.synchronize()
            ct1 = time.time()

            generated_list.append(video.cpu())
            print(f"  Chunk {chunk_idx}/{len(chunks)-1}: {ct1-ct0:.2f}s")

        # Save as MP4 (temp), then merge audio and convert to WebM
        print(f"  Encoding video...")
        temp_mp4 = mp4_path.replace(".mp4", "_tmp.mp4")
        with imageio.get_writer(
            temp_mp4, format="mp4", mode="I", fps=tgt_fps,
            codec="h264", ffmpeg_params=["-bf", "0"]
        ) as writer:
            for frames_tensor in generated_list:
                frames = frames_tensor.numpy().astype(np.uint8)
                for i in range(frames.shape[0]):
                    writer.append_data(frames[i])

        # Merge video + audio → MP4
        subprocess.run(
            [
                "ffmpeg", "-i", temp_mp4, "-i", str(audio_path),
                "-c:v", "copy", "-c:a", "aac", "-shortest",
                mp4_path, "-y",
            ],
            capture_output=True,
        )
        os.remove(temp_mp4)

        # Convert MP4 → WebM (VP9 + Opus)
        subprocess.run(
            [
                "ffmpeg", "-i", mp4_path,
                "-c:v", "libvpx-vp9", "-b:v", "1M", "-crf", "30",
                "-c:a", "libopus", "-b:a", "64k",
                webm_path, "-y",
            ],
            capture_output=True,
        )
        os.remove(mp4_path)

        elapsed = time.time() - t1
        print(f"  Done: {webm_path} ({elapsed:.1f}s total)\n")

    print(f"[batch] All {len(audio_files)} videos generated.")


if __name__ == "__main__":
    generate_all()
