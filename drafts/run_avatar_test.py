"""Automated Avatar Speech + Animation UX Test.

Part 1 — Speech: Transcribes each interview audio with Whisper, compares
against expected transcripts.

Part 2 — Animation: Analyzes video frames with MediaPipe FaceMesh to measure
lip sync correlation, blink rate, head movement, and idle behavior.

Usage:
    cd C:/Users/dbhav/Projects/isabelle
    .venv/Scripts/python.exe ../portfolio/drafts/run_avatar_test.py
"""

import difflib
import json
import math
import re
import time
from pathlib import Path

import cv2
import librosa
import mediapipe as mp
import numpy as np
from faster_whisper import WhisperModel

AUDIO_DIR = Path(r"C:\Users\dbhav\Projects\portfolio\drafts\assets\interview")
VIDEO_DIR = AUDIO_DIR
OUTPUT = Path(r"C:\Users\dbhav\Projects\portfolio\drafts\AVATAR_TEST_RESULTS.md")
FACE_MODEL = Path(r"C:\Users\dbhav\Projects\portfolio\drafts\assets\face_landmarker.task")

# MediaPipe FaceLandmarker landmark indices (478 total)
UPPER_LIP = 13
LOWER_LIP = 14
RIGHT_EYE_TOP = 159
RIGHT_EYE_BOTTOM = 145
LEFT_EYE_TOP = 386
LEFT_EYE_BOTTOM = 374
NOSE_TIP = 1

# Expected transcripts (from HTML data-transcript attributes)
TRANSCRIPTS = {
    "q1": {
        "question": "What do you build?",
        "expected": "So, I build AI systems — like, full production systems, not just demos. My main project is Isabelle, she's a voice assistant I built from scratch. Seven specialized agents working together, routes across five different language models, handles real-time voice... the whole pipeline. I also built an enterprise SaaS platform called StaFull with six different role-based portals. But yeah, the short answer is — I take AI from a concept all the way to something you can actually ship and use.",
    },
    "q2": {
        "question": "How does your LLM routing work?",
        "expected": "Yeah so the routing is — it's actually one of my favorite parts. I've got five models set up. There's a fast local model for quick responses — under four hundred milliseconds. Then Claude handles the deeper reasoning, and Gemini handles anything visual, like images. And there's a classifier that looks at each request and decides which model should handle it — based on how complex it is, what context is needed, and what it costs. So it's not random. It's intelligent routing, with automatic fallbacks if something goes down.",
    },
    "q3": {
        "question": "What's your background?",
        "expected": "Honestly? I spent thirty years in transportation operations — managing distributed teams, logistics, making time-critical decisions with incomplete information. And then I just... got obsessed with AI. Like, fully obsessed. Built a real portfolio in under two years. Every concept I studied, I immediately turned into working code. I don't have a CS degree — I'll be upfront about that — but I've got almost forty repos, over a thousand commits, and almost a million lines of production code. The work speaks for itself.",
    },
    "q4": {
        "question": "Explain your agent architecture.",
        "expected": "Okay so Isabelle has this orchestrator — think of it like a manager — and it coordinates seven specialized agents, each with its own job. One handles conversation, one does complex reasoning with Claude or Gemini, one can run thirty-two different tools, another handles longer workflows autonomously, one processes images and screenshots, and one manages memory so the assistant actually remembers things across conversations. They all share state and can run in parallel — which was honestly the hardest part to get right.",
    },
    "q5": {
        "question": "What was your hardest technical challenge?",
        "expected": "Oh man, real-time voice. Hands down. Getting the full round-trip latency — from when you stop talking to when the assistant starts responding — under five hundred milliseconds... it was a grind. You've got speech detection, transcription, the language model thinking, then generating the voice response — all while doing echo cancellation so it doesn't hear itself. And all of this is running on a single GPU with seven-plus models loaded at once. One model uses too much memory and the whole thing falls over. But the goal was to make it feel like a real conversation, not like talking to a robot. And I think we got there.",
    },
    "q6": {
        "question": "How do you approach testing?",
        "expected": "I'm kind of obsessive about it, honestly. Over seven hundred tests — unit, integration, end-to-end, even chaos testing where I break things on purpose. Every module has its own test suite. When I fix a bug, the first thing I do is write a test that reproduces it. Then I fix it, then I make sure the test passes. GitHub Actions runs everything automatically on every push. My philosophy is basically — if it doesn't have tests, it doesn't work. You just don't know it's broken yet.",
    },
    "q7": {
        "question": "How does your RAG system work?",
        "expected": "So when the assistant needs to look something up, it uses two search methods at the same time — one for exact keyword matches and one that understands meaning. Both run in parallel, and the results get merged and ranked. On top of that, there's a knowledge base with over five hundred skills it can draw from. And then memory is layered — recent stuff stays in the current session, older context goes into a database, and long-term knowledge lives in a dedicated search engine. So the assistant genuinely remembers things across conversations. It's not just search — it's actual memory.",
    },
    "q8": {
        "question": "Where do you see yourself next?",
        "expected": "I mean, I want to be doing exactly this but at scale. Building production AI systems, shipping real products. I'm looking at roles like AI Engineer, Applications Engineer, anywhere I can build multi-agent systems and real-time pipelines. What I bring is... I'm a builder. I don't just read about this stuff, I've deployed every concept I've learned into working software. And I'm ready to bring that to a team.",
    },
    "q9": {
        "question": "How do you handle a project that's failing?",
        "expected": "First thing I do is stop guessing. I look at the actual error, trace it back to the root cause — not the symptom, the real origin. I've got a rule: if I can't fix it in two attempts, I stop and rethink the approach entirely. I don't do band-aid fixes. If the architecture is wrong, I fix the architecture. I've killed features, rewritten modules, thrown away days of work when the foundation wasn't right. It's painful in the moment, but six months later you're not drowning in technical debt. What matters most is being honest early — don't hide problems, surface them fast, and fix them at the source.",
    },
    "q10": {
        "question": "How do you learn new technology?",
        "expected": "Building. That's how I learn. Seriously — every single concept I've studied, I turned into working code within days. Not tutorials, not toy examples — real systems. When I wanted to understand how multiple AI agents work together, I built a seven-agent system from scratch. When I wanted to learn how search engines work internally, I built one from the ground up instead of using a hosted service. I went from zero programming experience to almost a million lines of production code in under two years. The secret is I don't move on until I've shipped something that actually works. Theory without implementation is just trivia.",
    },
    "q11": {
        "question": "How do you make architecture decisions?",
        "expected": "Every decision gets logged — what we chose, what we rejected, and why. It's not just gut feeling. Here's an example: for search, I could have paid seventy-plus dollars a month for a hosted service. Instead, I built my own. The trade-off is I own the maintenance, but I eliminated an outside dependency and a recurring cost. Same thinking with the model routing — why pay for one expensive model to handle everything when a classifier can send seventy percent of requests to a free local model? I always start with: what's the simplest thing that solves the actual problem, and what are the real trade-offs?",
    },
    "q12": {
        "question": "What would you build in your first 90 days?",
        "expected": "First thirty days, I'm listening and reading. Understanding the existing systems, the pain points, the technical debt — not proposing big changes yet. I'd pick up a few quick wins to build trust and learn the codebase through real work. Days thirty to sixty, I'd start identifying where AI can have the biggest impact — maybe it's a pipeline that's too slow, maybe it's a manual process that could be automated, maybe there's no visibility into what's failing. By day ninety, I'd want to have shipped at least one meaningful improvement and have a concrete proposal for a bigger initiative. I'm not the guy who spends three months making slides. I ship.",
    },
    "q13": {
        "question": "Why you over a traditional CS background?",
        "expected": "Honestly? Hire me because of it, not despite it. Thirty years of managing complex operations — distributed teams, time-critical logistics, decisions with incomplete data — that's exactly the kind of systems thinking that makes good AI infrastructure. CS graduates understand algorithms. I understand what happens when your system breaks at two in the morning and there's real money on the line. Plus, I've proven I can learn. Almost a million lines of production code, over seven hundred tests, multi-agent systems, voice pipelines — all built in under two years. I don't just know the theory, I've built the systems. And I bring a perspective that most engineers don't have.",
    },
}


NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
    "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
    "eighteen": "18", "nineteen": "19", "twenty": "20", "thirty": "30",
    "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
    "eighty": "80", "ninety": "90", "hundred": "100", "thousand": "1000",
}

COMPOUND_MERGES = {
    # Compound words
    "sub agents": "subagents",
    "sub agent": "subagent",
    "multi agent": "multiagent",
    "real time": "realtime",
    "end to end": "endtoend",
    "band aid": "bandaid",
    "tech debt": "techdebt",
    "technical debt": "techdebt",
    "up front": "upfront",
    # Numbers — written-out to digit form
    "thirty seven": "37",
    "thirty two": "32",
    "thirteen hundred": "1300",
    "nine hundred thousand": "900000",
    "ninety five thousand": "95000",
    "seven hundred": "700",
    "five hundred": "500",
    "four hundred": "400",
    # Acronyms / initialisms
    "ci cd": "cicd",
    "ci to cd": "cicd",
    "c i c d": "cicd",
    "c i to c d": "cicd",
    "a i": "ai",
    "c s": "cs",
    "l l m": "llm",
    "l l ms": "llms",
    "t t s": "tts",
    "h n s w": "hnsw",
    "r t x": "rtx",
    "2 am": "2am",
    "two am": "2am",
    # Contractions / spelling variants
    "ok": "okay",
    "could've": "couldhave",
    "could have": "couldhave",
    "i've": "ive",
    "don't": "dont",
    "doesn't": "doesnt",
    "didn't": "didnt",
    "i'll": "ill",
    "it's": "its",
    "i'm": "im",
    "you're": "youre",
    "we're": "were",
    "they're": "theyre",
    "that's": "thats",
    "what's": "whats",
    "there's": "theres",
    "wasn't": "wasnt",
    "isn't": "isnt",
    "aren't": "arent",
    "won't": "wont",
    "can't": "cant",
    "wouldn't": "wouldnt",
    "shouldn't": "shouldnt",
    "haven't": "havent",
    "hasn't": "hasnt",
    "weren't": "werent",
    "tradeoff": "tradeoff",
    "trade off": "tradeoff",
    "tradeoffs": "tradeoffs",
    "trade offs": "tradeoffs",
    # Brand names
    "stafull": "stafull",
    "stafel": "stafull",
    "stayful": "stafull",
    "stay full": "stafull",
}


def normalize(text):
    """Normalize text for comparison — handles numbers, compounds, punctuation."""
    text = text.lower()
    text = re.sub(r"[—–\-]", " ", text)
    text = re.sub(r"[^\w\s']", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Normalize number words to digits
    for word, digit in sorted(NUMBER_WORDS.items(), key=lambda x: -len(x[0])):
        text = text.replace(word, digit)

    # Merge compound phrases
    for phrase, merged in sorted(COMPOUND_MERGES.items(), key=lambda x: -len(x[0])):
        text = text.replace(phrase, merged)

    # Collapse adjacent digits that form a single number
    # e.g. "9 100 1000" → "900000", "4 100" → "400", "7 100" → "700"
    # Handle "N 100 1000" → N*100*1000
    text = re.sub(r'\b(\d+)\s+100\s+1000\b', lambda m: str(int(m.group(1)) * 100000), text)
    text = re.sub(r'\b(\d+)\s+1000\b', lambda m: str(int(m.group(1)) * 1000), text)
    text = re.sub(r'\b(\d+)\s+100\b', lambda m: str(int(m.group(1)) * 100), text)

    # Remove possessive/contraction apostrophes for matching
    text = text.replace("'", "")

    # Collapse any resulting double spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def word_diff(expected_words, actual_words):
    """Return added, missing, and matched words."""
    sm = difflib.SequenceMatcher(None, expected_words, actual_words)
    added = []
    missing = []
    matched = 0
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            matched += i2 - i1
        elif op == "replace":
            missing.extend(expected_words[i1:i2])
            added.extend(actual_words[j1:j2])
        elif op == "insert":
            added.extend(actual_words[j1:j2])
        elif op == "delete":
            missing.extend(expected_words[i1:i2])
    return added, missing, matched


def check_template_vars(transcription, template_vars):
    """Check if template variables were spoken literally."""
    issues = []
    lower = transcription.lower()
    for var in template_vars:
        # Check for literal curly braces or the word "curly"
        bare = var.strip("{}")
        if "curly" in lower or "brace" in lower or "{{" in transcription:
            issues.append(f"CRITICAL: '{var}' appears to be spoken literally (curly braces detected)")
        elif bare in lower and not any(c.isdigit() for c in lower.split(bare)[0][-10:] + lower.split(bare)[-1][:10]):
            issues.append(f"WARNING: '{var}' may not have been replaced — check audio manually")
    return issues


def analyze_video(video_path, audio_path=None):
    """Analyze video for lip sync, blinks, head movement, and idle behavior.

    Returns dict with animation metrics.
    """
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps

    # MediaPipe Tasks API — FaceLandmarker
    BaseOptions = mp.tasks.BaseOptions
    FaceLandmarker = mp.tasks.vision.FaceLandmarker
    FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
    RunningMode = mp.tasks.vision.RunningMode

    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(FACE_MODEL)),
        running_mode=RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_face_blendshapes=False,
    )

    mouth_openness = []
    eye_aspect_ratios = []
    nose_positions = []
    face_detected_count = 0

    with FaceLandmarker.create_from_options(options) as landmarker:
        frame_idx = 0
        for _ in range(total_frames):
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int(frame_idx * 1000 / fps)

            results = landmarker.detect_for_video(mp_image, timestamp_ms)
            frame_idx += 1

            if results.face_landmarks and len(results.face_landmarks) > 0:
                face_detected_count += 1
                lm = results.face_landmarks[0]  # list of NormalizedLandmark
                h, w = frame.shape[:2]

                upper = lm[UPPER_LIP]
                lower = lm[LOWER_LIP]
                mouth_dist = math.sqrt((upper.x - lower.x)**2 + (upper.y - lower.y)**2) * h
                mouth_openness.append(mouth_dist)

                r_top = lm[RIGHT_EYE_TOP]
                r_bot = lm[RIGHT_EYE_BOTTOM]
                l_top = lm[LEFT_EYE_TOP]
                l_bot = lm[LEFT_EYE_BOTTOM]
                r_ear = abs(r_top.y - r_bot.y) * h
                l_ear = abs(l_top.y - l_bot.y) * h
                ear = (r_ear + l_ear) / 2
                eye_aspect_ratios.append(ear)

                nose = lm[NOSE_TIP]
                nose_positions.append((nose.x * w, nose.y * h))
            else:
                mouth_openness.append(0)
                eye_aspect_ratios.append(0)

    cap.release()

    mouth_arr = np.array(mouth_openness)
    ear_arr = np.array(eye_aspect_ratios)
    nose_arr = np.array(nose_positions) if nose_positions else np.zeros((1, 2))

    # --- Blink detection ---
    # Blinks = EAR drops below threshold momentarily
    ear_threshold = np.median(ear_arr[ear_arr > 0]) * 0.6 if np.any(ear_arr > 0) else 2.0
    below = ear_arr < ear_threshold
    # Count transitions from open to closed
    blink_count = 0
    in_blink = False
    for v in below:
        if v and not in_blink:
            blink_count += 1
            in_blink = True
        elif not v:
            in_blink = False
    blinks_per_sec = blink_count / duration if duration > 0 else 0
    # Normal: 0.25-0.4 blinks/sec (15-24 per minute)
    blink_natural = 0.15 <= blinks_per_sec <= 0.6

    # --- Head movement ---
    if len(nose_arr) > 1:
        nose_diffs = np.diff(nose_arr, axis=0)
        head_movement_px = np.mean(np.sqrt(np.sum(nose_diffs**2, axis=1)))
        head_variance = np.var(nose_arr, axis=0).sum()
    else:
        head_movement_px = 0
        head_variance = 0
    # Frozen = near-zero variance
    head_frozen = head_variance < 0.5
    head_natural = not head_frozen and head_movement_px < 5.0  # subtle but present

    # --- Lip sync: speech-vs-silence mouth activity ratio ---
    # FlashHead uses semantic audio features (wav2vec), not raw amplitude.
    # Frame-level RMS correlation is the wrong metric. Instead, measure:
    # 1. Average mouth openness during SPEECH segments
    # 2. Average mouth openness during SILENCE segments
    # 3. The ratio (speech/silence) — should be > 1.5 for good lip sync
    # 4. Also check onset alignment: does mouth open within ~200ms of speech start?
    lip_sync_corr = None  # kept for backward compat but deprecated
    lip_sync_ratio = None
    lip_sync_onset_ok = None
    if audio_path and audio_path.exists():
        audio, sr = librosa.load(str(audio_path), sr=None, mono=True)
        # RMS energy per video frame
        hop = int(sr / fps)
        rms = librosa.feature.rms(y=audio, frame_length=hop * 2, hop_length=hop)[0]
        min_len = min(len(rms), len(mouth_arr))
        if min_len > 10:
            rms_aligned = rms[:min_len]
            mouth_aligned = mouth_arr[:min_len]

            # Classify each frame as speech or silence using RMS threshold
            rms_threshold = np.percentile(rms_aligned[rms_aligned > 0], 20) if np.any(rms_aligned > 0) else 0.01
            is_speech = rms_aligned > rms_threshold

            speech_mouth = mouth_aligned[is_speech]
            silence_mouth = mouth_aligned[~is_speech]

            speech_mean = float(np.mean(speech_mouth)) if len(speech_mouth) > 0 else 0
            silence_mean = float(np.mean(silence_mouth)) if len(silence_mouth) > 0 else 0.01

            lip_sync_ratio = speech_mean / max(silence_mean, 0.01)

            # Onset alignment: find first speech frame, check if mouth opens within 5 frames (~200ms)
            speech_indices = np.where(is_speech)[0]
            if len(speech_indices) > 0:
                first_speech = speech_indices[0]
                onset_window = mouth_aligned[first_speech:min(first_speech + 5, min_len)]
                mouth_baseline = np.mean(mouth_aligned[:max(first_speech, 1)])
                lip_sync_onset_ok = bool(np.max(onset_window) > mouth_baseline * 1.3) if len(onset_window) > 0 else None

            # Also compute classic correlation for reference
            rms_norm = (rms_aligned - rms_aligned.mean()) / (rms_aligned.std() + 1e-8)
            mouth_norm = (mouth_aligned - mouth_aligned.mean()) / (mouth_aligned.std() + 1e-8)
            lip_sync_corr = float(np.corrcoef(rms_norm, mouth_norm)[0, 1])

    # --- Mouth activity during silence (idle check) ---
    # For idle video (no audio), mouth should be mostly closed
    mouth_mean = float(np.mean(mouth_arr))
    mouth_std = float(np.std(mouth_arr))
    mouth_max = float(np.max(mouth_arr)) if len(mouth_arr) > 0 else 0

    return {
        "duration_s": round(duration, 1),
        "total_frames": total_frames,
        "face_detected_pct": round(face_detected_count / max(total_frames, 1) * 100, 1),
        "blink_count": blink_count,
        "blinks_per_sec": round(blinks_per_sec, 2),
        "blink_natural": blink_natural,
        "head_movement_avg_px": round(head_movement_px, 2),
        "head_variance": round(head_variance, 2),
        "head_frozen": head_frozen,
        "head_natural": head_natural,
        "mouth_mean": round(mouth_mean, 2),
        "mouth_std": round(mouth_std, 2),
        "mouth_max": round(mouth_max, 2),
        "lip_sync_corr": round(lip_sync_corr, 3) if lip_sync_corr is not None else None,
        "lip_sync_ratio": round(lip_sync_ratio, 2) if lip_sync_ratio is not None else None,
        "lip_sync_onset_ok": lip_sync_onset_ok,
    }


def main():
    print("Loading Whisper model (base.en)...")
    t0 = time.time()
    model = WhisperModel("base.en", device="cuda", compute_type="float16")
    print(f"Model loaded in {time.time() - t0:.1f}s\n")

    results = []

    for stem in sorted(TRANSCRIPTS.keys(), key=lambda x: int(x[1:])):
        info = TRANSCRIPTS[stem]
        audio_path = AUDIO_DIR / f"{stem}.wav"

        if not audio_path.exists():
            results.append({"stem": stem, "error": f"Audio file not found: {audio_path}"})
            continue

        print(f"Transcribing {stem}...")

        # Get audio duration
        duration = librosa.get_duration(path=str(audio_path))

        # Transcribe
        segments, seg_info = model.transcribe(
            str(audio_path),
            language="en",
            beam_size=5,
            word_timestamps=True,
        )
        segments_list = list(segments)
        transcription = " ".join(seg.text.strip() for seg in segments_list)

        # Word-level analysis
        expected_norm = normalize(info["expected"])
        actual_norm = normalize(transcription)
        expected_words = expected_norm.split()
        actual_words = actual_norm.split()

        added, missing, matched = word_diff(expected_words, actual_words)
        total_expected = len(expected_words)
        accuracy = matched / total_expected * 100 if total_expected > 0 else 0

        # WPM calculation
        actual_word_count = len(actual_words)
        wpm = actual_word_count / (duration / 60) if duration > 0 else 0

        # Check for cut-off (does the last segment end near audio end?)
        last_seg_end = segments_list[-1].end if segments_list else 0
        cut_off = (duration - last_seg_end) < 0.3 and duration > 5  # tight ending might mean cut-off

        # Template variable check
        template_issues = []
        if "template_vars" in info:
            template_issues = check_template_vars(transcription, info["template_vars"])

        # Sentence completeness check
        sentences_expected = [s.strip() for s in re.split(r'[.!?]', info["expected"]) if s.strip()]
        last_sentence = sentences_expected[-1] if sentences_expected else ""
        last_words_expected = normalize(last_sentence).split()[-4:]
        last_words_actual = actual_norm.split()[-6:]
        ends_complete = any(w in last_words_actual for w in last_words_expected) if last_words_expected else True

        result = {
            "stem": stem,
            "question": info["question"],
            "duration_s": round(duration, 1),
            "word_count": actual_word_count,
            "wpm": round(wpm),
            "accuracy_pct": round(accuracy, 1),
            "words_matched": matched,
            "words_expected": total_expected,
            "words_added": added[:20],  # cap for readability
            "words_added_count": len(added),
            "words_missing": missing[:20],
            "words_missing_count": len(missing),
            "ends_complete": ends_complete,
            "template_issues": template_issues,
            "transcription": transcription.strip(),
        }
        results.append(result)
        print(f"  {stem}: {accuracy:.0f}% accuracy, {wpm:.0f} WPM, {duration:.1f}s")

    # ── Part 2: Visual Animation Analysis ──────────────────────────────
    print(f"\n{'='*60}")
    print("Part 2: Visual Animation Analysis")
    print(f"{'='*60}\n")

    video_results = {}

    # Analyze idle video
    idle_path = VIDEO_DIR / "idle.webm"
    if idle_path.exists():
        print("Analyzing idle.webm...")
        idle_res = analyze_video(idle_path, audio_path=None)
        video_results["idle"] = idle_res
        print(f"  idle: blinks={idle_res['blink_count']}, "
              f"head_frozen={idle_res['head_frozen']}, "
              f"mouth_mean={idle_res['mouth_mean']:.1f}")

    # Analyze Q&A videos
    for stem in sorted(TRANSCRIPTS.keys(), key=lambda x: int(x[1:])):
        vid_path = VIDEO_DIR / f"{stem}.webm"
        aud_path = AUDIO_DIR / f"{stem}.wav"
        if not vid_path.exists():
            continue

        print(f"Analyzing {stem}.webm...")
        vr = analyze_video(vid_path, audio_path=aud_path)
        video_results[stem] = vr
        sync_str = f"lip_sync={vr['lip_sync_corr']:.2f}" if vr['lip_sync_corr'] is not None else "lip_sync=N/A"
        print(f"  {stem}: blinks={vr['blink_count']}, "
              f"head_frozen={vr['head_frozen']}, {sync_str}")

    # Generate report
    print(f"\nGenerating report...")
    report = generate_report(results, video_results)
    OUTPUT.write_text(report, encoding="utf-8")
    print(f"Report saved to: {OUTPUT}")


def generate_report(results, video_results=None):
    if video_results is None:
        video_results = {}

    lines = [
        "# Avatar Interview — Automated Speech + Animation Test Results",
        f"",
        f"**Generated:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Speech Model:** faster-whisper base.en (CUDA float16)",
        f"**Animation Model:** MediaPipe FaceMesh (468 landmarks)",
        f"**Method:** Whisper transcription + frame-by-frame face analysis",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        "| Q | Question | Duration | WPM | Accuracy | Added | Missing | Complete | Status |",
        "|---|---------|----------|-----|----------|-------|---------|----------|--------|",
    ]

    critical_issues = []
    for r in results:
        if "error" in r:
            lines.append(f"| {r['stem']} | ERROR | — | — | — | — | — | — | {r['error']} |")
            continue

        status = "PASS" if r["accuracy_pct"] >= 85 and r["ends_complete"] else "REVIEW"
        if r["template_issues"]:
            status = "CRITICAL"
        if r["accuracy_pct"] < 70:
            status = "FAIL"

        wpm_flag = ""
        if r["wpm"] < 120:
            wpm_flag = " (slow)"
        elif r["wpm"] > 170:
            wpm_flag = " (fast)"

        lines.append(
            f"| {r['stem']} | {r['question']} | {r['duration_s']}s | "
            f"{r['wpm']}{wpm_flag} | {r['accuracy_pct']}% | "
            f"{r['words_added_count']} | {r['words_missing_count']} | "
            f"{'Yes' if r['ends_complete'] else 'NO'} | **{status}** |"
        )

        if r["template_issues"]:
            critical_issues.extend(r["template_issues"])

    # WPM analysis
    wpms = [r["wpm"] for r in results if "error" not in r]
    avg_wpm = sum(wpms) / len(wpms) if wpms else 0
    lines.extend([
        "",
        f"**Average WPM:** {avg_wpm:.0f} (target: 130–160 for conversational)",
        f"**WPM range:** {min(wpms):.0f}–{max(wpms):.0f}" if wpms else "",
        "",
    ])

    if critical_issues:
        lines.extend([
            "## CRITICAL ISSUES",
            "",
        ])
        for issue in critical_issues:
            lines.append(f"- {issue}")
        lines.append("")

    lines.extend([
        "---",
        "",
    ])

    # Detailed results per question
    for r in results:
        if "error" in r:
            continue

        lines.extend([
            f"## {r['stem'].upper()}: \"{r['question']}\"",
            "",
            f"**Duration:** {r['duration_s']}s | **Words:** {r['word_count']} | **WPM:** {r['wpm']} | **Accuracy:** {r['accuracy_pct']}%",
            "",
        ])

        if r["template_issues"]:
            lines.append("### Template Variable Issues")
            for issue in r["template_issues"]:
                lines.append(f"- {issue}")
            lines.append("")

        if r["words_missing_count"] > 0:
            lines.append(f"### Missing Words ({r['words_missing_count']})")
            lines.append(f"`{' '.join(r['words_missing'])}`")
            lines.append("")

        if r["words_added_count"] > 0:
            lines.append(f"### Added Words ({r['words_added_count']})")
            lines.append(f"`{' '.join(r['words_added'])}`")
            lines.append("")

        if not r["ends_complete"]:
            lines.append("### Completion Issue")
            lines.append("**WARNING:** Answer may be cut off — final words don't match expected ending.")
            lines.append("")

        # WPM assessment
        if r["wpm"] < 120:
            lines.append(f"**Speed:** Too slow ({r['wpm']} WPM). May sound sluggish or robotic.")
        elif r["wpm"] > 170:
            lines.append(f"**Speed:** Too fast ({r['wpm']} WPM). May be hard to follow.")
        else:
            lines.append(f"**Speed:** Good ({r['wpm']} WPM).")
        lines.append("")

        lines.append("### Actual Transcription")
        lines.append(f"> {r['transcription']}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # ── Part 2: Animation Analysis ────────────────────────────────────
    if video_results:
        lines.extend([
            "",
            "# Part 2: Animation & Visual Analysis",
            "",
            "---",
            "",
            "## Animation Summary",
            "",
            "| Video | Face % | Blinks | Blink/s | Blink OK | Head OK | Sync Ratio | Onset OK | Status |",
            "|-------|--------|--------|---------|----------|---------|------------|----------|--------|",
        ])

        for stem in ["idle"] + sorted([k for k in video_results if k != "idle"], key=lambda x: int(x[1:])):
            if stem not in video_results:
                continue
            vr = video_results[stem]
            ratio_str = f"{vr['lip_sync_ratio']:.1f}x" if vr.get('lip_sync_ratio') is not None else "N/A"
            onset_str = "Yes" if vr.get('lip_sync_onset_ok') else ("NO" if vr.get('lip_sync_onset_ok') is False else "N/A")

            # Status logic — using ratio (speech mouth / silence mouth)
            # Good: ratio > 1.5, Acceptable: > 1.2, Poor: <= 1.2
            issues = []
            if not vr["blink_natural"]:
                issues.append("blink")
            if vr["head_frozen"]:
                issues.append("frozen")
            ratio = vr.get("lip_sync_ratio")
            if ratio is not None and ratio < 1.2:
                issues.append("lip-sync")
            if vr.get("lip_sync_onset_ok") is False:
                issues.append("onset-lag")
            if stem == "idle" and vr["mouth_std"] > 3.0:
                issues.append("mouth-moves-idle")

            status = "PASS" if not issues else f"REVIEW ({', '.join(issues)})"

            lines.append(
                f"| {stem} | {vr['face_detected_pct']}% | {vr['blink_count']} | "
                f"{vr['blinks_per_sec']} | {'Yes' if vr['blink_natural'] else 'NO'} | "
                f"{'Yes' if vr['head_natural'] else 'NO'} | "
                f"{ratio_str} | {onset_str} | **{status}** |"
            )

        # Thresholds explanation
        lines.extend([
            "",
            "### Thresholds",
            "- **Blink rate:** 0.15–0.6 blinks/sec (9–36 per minute) = natural",
            "- **Head frozen:** Near-zero variance in nose position = robotic",
            "- **Lip sync ratio:** mouth openness during speech / during silence. >1.5 = good, 1.2–1.5 = acceptable, <1.2 = poor",
            "- **Onset alignment:** Mouth opens within 200ms of first speech = good",
            "- **Idle mouth:** Mean mouth openness should be low, std < 3.0 (no movement)",
            "",
        ])

        # Detailed idle analysis
        if "idle" in video_results:
            ir = video_results["idle"]
            lines.extend([
                "---",
                "",
                "## IDLE VIDEO Analysis",
                "",
                f"- **Duration:** {ir['duration_s']}s ({ir['total_frames']} frames)",
                f"- **Face detected:** {ir['face_detected_pct']}%",
                f"- **Blinks:** {ir['blink_count']} ({ir['blinks_per_sec']}/sec) — {'Natural' if ir['blink_natural'] else 'UNNATURAL'}",
                f"- **Head movement:** avg {ir['head_movement_avg_px']:.1f}px/frame — {'Frozen' if ir['head_frozen'] else 'Subtle movement detected'}",
                f"- **Mouth:** mean={ir['mouth_mean']:.1f}, std={ir['mouth_std']:.1f}, max={ir['mouth_max']:.1f}",
            ])
            if ir["mouth_std"] > 3.0:
                lines.append("- **WARNING:** Mouth is moving during idle — should be still")
            else:
                lines.append("- **Mouth idle:** Good — minimal/no mouth movement")
            lines.append("")

        # Detailed per-question
        for stem in sorted([k for k in video_results if k != "idle"], key=lambda x: int(x[1:])):
            vr = video_results[stem]
            q = TRANSCRIPTS.get(stem, {}).get("question", stem)
            ratio = vr.get('lip_sync_ratio')
            ratio_str = f"{ratio:.2f}x" if ratio is not None else "N/A"
            ratio_label = " (good)" if ratio and ratio >= 1.5 else " (acceptable)" if ratio and ratio >= 1.2 else " (poor)" if ratio is not None else ""
            onset = vr.get('lip_sync_onset_ok')
            onset_str = "Yes" if onset else ("NO — mouth lags speech start" if onset is False else "N/A")

            lines.extend([
                "---",
                "",
                f"## {stem.upper()} Animation: \"{q}\"",
                "",
                f"- **Face detected:** {vr['face_detected_pct']}%",
                f"- **Blinks:** {vr['blink_count']} ({vr['blinks_per_sec']}/sec) — {'Natural' if vr['blink_natural'] else 'UNNATURAL'}",
                f"- **Head:** avg movement {vr['head_movement_avg_px']:.2f}px/frame, variance {vr['head_variance']:.1f} — {'Natural' if vr['head_natural'] else 'FROZEN' if vr['head_frozen'] else 'Excessive'}",
                f"- **Lip sync ratio:** {ratio_str}{ratio_label} (mouth during speech / during silence)",
                f"- **Onset alignment:** {onset_str}",
                f"- **Mouth:** mean={vr['mouth_mean']:.1f}, std={vr['mouth_std']:.1f}, max={vr['mouth_max']:.1f}",
                "",
            ])

    return "\n".join(lines)


if __name__ == "__main__":
    main()
