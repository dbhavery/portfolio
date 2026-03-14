"""Generate interview audio using Chatterbox TTS with Don's voice.

Uses Chatterbox Turbo for voice cloning from a reference recording.

Usage:
    cd C:/Users/dbhav/Projects/isabelle
    .venv/Scripts/python.exe ../portfolio/drafts/generate_tts_audio.py [--q1-only]

Outputs: portfolio/drafts/assets/interview/q1.wav ... q13.wav
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Reference voice recording (Don's actual voice)
REFERENCE_VOICE = Path(r"I:\IsabelleData\media\audio\2025\12\2025_12_24_11_36_25_1.mp3")
OUTPUT_DIR = Path(__file__).parent / "assets" / "interview"

# Add the tts_transcripts module
sys.path.insert(0, str(OUTPUT_DIR))


def generate_audio(q1_only: bool = False) -> None:
    """Generate WAV files from TTS transcripts using Chatterbox."""
    import torch
    import torchaudio

    # HuggingFace token
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        token_path = Path.home() / ".cache" / "huggingface" / "token"
        if token_path.exists():
            hf_token = token_path.read_text().strip()
            os.environ["HF_TOKEN"] = hf_token

    from chatterbox.tts import ChatterboxTTS

    from tts_transcripts import TTS_TRANSCRIPTS

    print(f"[init] Reference voice: {REFERENCE_VOICE}")
    print(f"[init] Output dir: {OUTPUT_DIR}")
    print(f"[init] Loading Chatterbox TTS model...")

    t0 = time.time()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = ChatterboxTTS.from_pretrained(device=device)
    print(f"[init] Model loaded in {time.time() - t0:.1f}s on {device}")

    questions = ["q1"] if q1_only else sorted(TTS_TRANSCRIPTS.keys())

    for q in questions:
        text = TTS_TRANSCRIPTS[q]
        wav_path = OUTPUT_DIR / f"{q}.wav"

        print(f"\n-- {q} ----------------------------------")
        print(f"  Text length: {len(text)} chars")
        t1 = time.time()

        wav = model.generate(
            text=text,
            audio_prompt_path=str(REFERENCE_VOICE),
            exaggeration=0.4,
        )

        torchaudio.save(str(wav_path), wav, model.sr)
        elapsed = time.time() - t1
        duration = wav.shape[1] / model.sr
        print(f"  Generated: {wav_path.name} ({duration:.1f}s audio, took {elapsed:.1f}s)")

    print(f"\n[done] Generated {len(questions)} audio file(s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate interview TTS audio")
    parser.add_argument("--q1-only", action="store_true", help="Generate only Q1 for preview")
    args = parser.parse_args()
    generate_audio(q1_only=args.q1_only)
