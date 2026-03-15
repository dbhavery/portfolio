#!/usr/bin/env python3
"""Auto-update avatar interview metrics.

Checks current metrics against the spoken approximations in the TTS transcripts.
When a metric crosses a threshold boundary, regenerates the affected audio + video.

Designed to run weekly via cron/scheduler.

Usage:
    cd C:/Users/dbhav/Projects/isabelle
    .venv/Scripts/python.exe ../portfolio/scripts/update-avatar-metrics.py          # dry-run
    .venv/Scripts/python.exe ../portfolio/scripts/update-avatar-metrics.py --apply  # regenerate
"""

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

PORTFOLIO_ROOT = Path(__file__).resolve().parent.parent
ISABELLE_ROOT = Path(r"C:\Users\dbhav\Projects\isabelle")
METRICS_FILE = PORTFOLIO_ROOT / "metrics.json"
TTS_TRANSCRIPTS_FILE = PORTFOLIO_ROOT / "drafts" / "assets" / "interview" / "tts_transcripts.py"
HTML_FILE = PORTFOLIO_ROOT / "drafts" / "draft-e-neural-command.html"
PYTHON = str(ISABELLE_ROOT / ".venv" / "Scripts" / "python.exe")

# ── Metric-to-approximation mapping ──────────────────────────────────────
# Each entry: metric key, list of (threshold, spoken_tts, spoken_display) tuples
# When the real value crosses into a new range, the approximation updates.
# Ranges are checked top-down; first match wins.
METRIC_RANGES = {
    "repos": [
        (100, "over a hundred", "over a hundred"),
        (80, "close to a hundred", "close to a hundred"),
        (60, "over sixty", "over sixty"),
        (50, "over fifty", "over fifty"),
        (45, "almost fifty", "almost fifty"),
        (40, "over forty", "over forty"),
        (35, "almost forty", "almost forty"),
        (30, "over thirty", "over thirty"),
        (25, "almost thirty", "almost thirty"),
        (20, "over twenty", "over twenty"),
        (0, "multiple", "multiple"),
    ],
    "commits_num": [
        (10000, "over ten thousand", "over ten thousand"),
        (5000, "over five thousand", "over five thousand"),
        (3000, "over three thousand", "over three thousand"),
        (2000, "over two thousand", "over two thousand"),
        (1500, "close to two thousand", "close to two thousand"),
        (1000, "over a thousand", "over a thousand"),
        (500, "over five hundred", "over five hundred"),
        (0, "hundreds of", "hundreds of"),
    ],
    "loc_num": [
        (2000000, "over two million", "over two million"),
        (1500000, "close to two million", "close to two million"),
        (1000000, "over a million", "over a million"),
        (800000, "almost a million", "almost a million"),
        (500000, "over half a million", "over half a million"),
        (0, "hundreds of thousands of", "hundreds of thousands of"),
    ],
    "tests_num": [
        (2000, "over two thousand", "over two thousand"),
        (1500, "close to two thousand", "close to two thousand"),
        (1000, "over a thousand", "over a thousand"),
        (900, "close to a thousand", "close to a thousand"),
        (800, "over eight hundred", "over eight hundred"),
        (700, "over seven hundred", "over seven hundred"),
        (600, "over six hundred", "over six hundred"),
        (500, "over five hundred", "over five hundred"),
        (0, "hundreds of", "hundreds of"),
    ],
}

# Which questions use which metrics (TTS pattern to find/replace)
QUESTION_METRICS = {
    "q3": {
        "repos": (r"(?:almost|over|close to) (?:forty|fifty|sixty|a hundred|\w+ hundred|\w+ thousand) repos",
                  "{approx} repos"),
        "commits_num": (r"(?:over|close to|almost) (?:a thousand|two thousand|five thousand|\w+ hundred) commits",
                        "{approx} commits"),
        "loc_num": (r"(?:almost|over|close to) (?:a million|two million|half a million|\w+ thousand) lines",
                    "{approx} lines"),
    },
    "q6": {
        "tests_num": (r"(?:Over|over) (?:seven|eight|nine|a thousand|\w+) hundred tests",
                      "Over {approx} tests"),
    },
    "q10": {
        "loc_num": (r"(?:almost|over|close to) (?:a million|two million|half a million|\w+ thousand) lines",
                    "{approx} lines"),
    },
    "q13": {
        "loc_num": (r"(?:Almost|almost|over|close to) (?:a million|two million|half a million|\w+ thousand) lines",
                    "Almost {approx_raw} lines"),  # Q13 starts with "Almost"
        "tests_num": (r"(?:over|close to|almost) (?:seven|eight|nine|a thousand|\w+) hundred tests",
                      "over {approx} tests"),
    },
}


def parse_metric_number(val):
    """Parse '1,372+' or '888K+' into an integer."""
    s = str(val).replace(",", "").replace("+", "").strip()
    if s.upper().endswith("K"):
        return int(float(s[:-1]) * 1000)
    return int(float(s))


def get_approximation(metric_key, value):
    """Get the spoken approximation for a metric value."""
    ranges = METRIC_RANGES.get(metric_key, [])
    for threshold, tts_text, display_text in ranges:
        if value >= threshold:
            return tts_text, display_text
    return str(value), str(value)


def load_current_approximations():
    """Read TTS transcripts and extract current spoken approximations."""
    # Join all lines to handle multi-line string concatenation
    content = TTS_TRANSCRIPTS_FILE.read_text(encoding="utf-8")
    # Collapse Python string concatenation into single lines
    flat = re.sub(r'"\s*\n\s*"', ' ', content)
    current = {}

    # Extract repos approximation from q3
    m = re.search(r"(almost|over|close to) (\w+)\s+repos", flat, re.IGNORECASE)
    if m:
        current["repos"] = m.group(0).replace(" repos", "").strip()

    # Extract commits
    m = re.search(r"(over|close to) (a thousand|two thousand|five thousand|\w+ hundred)\s+commits", flat, re.IGNORECASE)
    if m:
        current["commits_num"] = m.group(0).replace(" commits", "").strip()

    # Extract LOC (from q3, first occurrence)
    m = re.search(r"(almost|over|close to) (a million|two million|half a million|\w+ thousand)\s+lines", flat, re.IGNORECASE)
    if m:
        current["loc_num"] = m.group(0).replace(" lines", "").strip()

    # Extract tests — handle "Over seven hundred tests" or "over two thousand tests"
    m = re.search(r"(Over|over) (\w+ hundred|\w+ thousand|a thousand)\s+tests", flat, re.IGNORECASE)
    if m:
        current["tests_num"] = m.group(0).replace(" tests", "").strip().lower()

    return current


def check_thresholds(metrics):
    """Check if any metrics have crossed a threshold boundary."""
    repos = metrics["repos"]
    commits = parse_metric_number(metrics["commits"])
    loc = parse_metric_number(metrics["loc"])
    tests = parse_metric_number(metrics["totalTests"])

    current_spoken = load_current_approximations()

    changes = {}
    values = {
        "repos": repos,
        "commits_num": commits,
        "loc_num": loc,
        "tests_num": tests,
    }

    for key, value in values.items():
        new_tts, new_display = get_approximation(key, value)
        old_spoken = current_spoken.get(key, "")

        if new_tts.lower() != old_spoken.lower():
            changes[key] = {
                "value": value,
                "old": old_spoken,
                "new_tts": new_tts,
                "new_display": new_display,
            }

    return changes, values


def update_tts_transcripts(changes, values):
    """Update the TTS transcript file with new approximations."""
    content = TTS_TRANSCRIPTS_FILE.read_text(encoding="utf-8")
    original = content

    for q_id, metric_map in QUESTION_METRICS.items():
        for metric_key, (pattern, template) in metric_map.items():
            if metric_key in changes:
                approx = changes[metric_key]["new_tts"]
                # Handle special cases
                replacement = template.format(approx=approx, approx_raw=approx.lstrip("almost ").lstrip("over ").lstrip("close to "))
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    # Update the comment with current stats
    content = re.sub(
        r"hardcoded stats \(.*?\)\.",
        f"hardcoded stats ({values['repos']} repos, {values['commits_num']} commits, "
        f"{values['loc_num']} lines, {values['tests_num']} tests).",
        content,
    )

    if content != original:
        TTS_TRANSCRIPTS_FILE.write_text(content, encoding="utf-8")
        return True
    return False


def get_affected_questions(changes):
    """Return set of question IDs that need regeneration."""
    affected = set()
    for q_id, metric_map in QUESTION_METRICS.items():
        for metric_key in metric_map:
            if metric_key in changes:
                affected.add(q_id)
    return sorted(affected)


def regenerate_audio(questions):
    """Regenerate TTS audio for specific questions."""
    print(f"\n[tts] Regenerating audio for: {', '.join(questions)}")
    cmd = [
        PYTHON, "-c",
        f"""
import os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(r'{PORTFOLIO_ROOT}/drafts/assets/interview')))
from tts_transcripts import TTS_TRANSCRIPTS
import torch, torchaudio
REF_VOICE = Path(r'I:\\IsabelleData\\media\\audio\\2025\\12\\2025_12_24_11_36_25_1.mp3')
OUT_DIR = Path(r'{PORTFOLIO_ROOT}/drafts/assets/interview')
os.environ['HF_TOKEN'] = Path.home().joinpath('.cache','huggingface','token').read_text().strip()
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device='cuda')
for q in {questions!r}:
    text = TTS_TRANSCRIPTS[q]
    wav_path = OUT_DIR / f'{{q}}.wav'
    t0 = time.time()
    wav = model.generate(text=text, audio_prompt_path=str(REF_VOICE), exaggeration=0.35)
    torchaudio.save(str(wav_path), wav, model.sr)
    dur = wav.shape[1] / model.sr
    print(f'  {{q}}.wav: {{dur:.1f}}s ({{time.time()-t0:.1f}}s)')
print('[tts] Done')
""",
    ]
    subprocess.run(cmd, cwd=str(ISABELLE_ROOT), check=True)


def regenerate_video(questions):
    """Regenerate FlashHead video for specific questions."""
    q_str = ",".join(questions)
    print(f"\n[video] Regenerating FlashHead video for: {q_str}")
    env = os.environ.copy()
    env["ONLY_QUESTIONS"] = q_str
    subprocess.run(
        [PYTHON, str(PORTFOLIO_ROOT / "drafts" / "generate_avatar_videos.py")],
        cwd=str(ISABELLE_ROOT),
        env=env,
        check=True,
    )


def main():
    apply = "--apply" in sys.argv

    print("Avatar Metrics Auto-Updater")
    print(f"  Metrics: {METRICS_FILE}")
    print(f"  Mode: {'APPLY' if apply else 'DRY RUN'}")
    print()

    # Load current metrics
    metrics = load_metrics_json()

    # Check thresholds
    changes, values = check_thresholds(metrics)

    # Always sync HTML metrics (even if no threshold crossed)
    if apply:
        print("[0] Syncing HTML metrics to current values...")
        update_html_metrics_config(metrics)

    if not changes:
        print("\nAll spoken approximations are current. No audio/video regeneration needed.")
        print(f"\n  Current values:")
        for k, v in values.items():
            tts, _ = get_approximation(k, v)
            print(f"    {k}: {v} -> \"{tts}\"")
        return

    # Report changes
    print("Threshold crossings detected:")
    for key, info in changes.items():
        print(f"  {key}: {info['value']} — \"{info['old']}\" -> \"{info['new_tts']}\"")

    affected = get_affected_questions(changes)
    print(f"\nQuestions to regenerate: {', '.join(affected)}")

    if not apply:
        print("\nRun with --apply to regenerate audio + video.")
        return

    # 1. Update TTS transcripts
    print("\n[1] Updating TTS transcripts...")
    if update_tts_transcripts(changes, values):
        print("  TTS transcripts updated")
    else:
        print("  No changes needed")

    # 2. Regenerate audio
    print("\n[2] Regenerating TTS audio...")
    regenerate_audio(affected)

    # 3. Regenerate video
    print("\n[3] Regenerating FlashHead video...")
    regenerate_video(affected)

    # 4. Update HTML display transcripts
    print("\n[4] Updating HTML display transcripts...")
    update_html_transcripts(changes)

    # 5. Log
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    print(f"\n[done] Avatar metrics updated at {timestamp}")
    print(f"  Questions regenerated: {', '.join(affected)}")
    for key, info in changes.items():
        print(f"  {key}: \"{info['old']}\" -> \"{info['new_tts']}\"")


def load_metrics_json():
    with open(METRICS_FILE, encoding="utf-8") as f:
        return json.load(f)


def update_html_transcripts(changes):
    """Update the display transcripts in the HTML to match new approximations."""
    content = HTML_FILE.read_text(encoding="utf-8")
    original = content

    for q_id, metric_map in QUESTION_METRICS.items():
        for metric_key, (pattern, template) in metric_map.items():
            if metric_key in changes:
                approx = changes[metric_key]["new_display"]
                replacement = template.format(approx=approx, approx_raw=approx)
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

    if content != original:
        HTML_FILE.write_text(content, encoding="utf-8")
        print("  HTML transcripts updated")
    else:
        print("  No HTML changes needed")


def update_html_metrics_config(metrics):
    """Update the hardcoded METRICS_CONFIG in the HTML with current values."""
    content = HTML_FILE.read_text(encoding="utf-8")
    original = content

    repos = metrics["repos"]
    commits = parse_metric_number(metrics["commits"])
    loc_k = parse_metric_number(metrics["loc"]) // 1000
    tests = parse_metric_number(metrics["totalTests"])

    # Update repos value
    content = re.sub(
        r"(repos:\s*\{\s*value:\s*)\d+",
        f"\\g<1>{repos}",
        content,
    )
    # Update commits value
    content = re.sub(
        r"(commits:\s*\{\s*value:\s*)\d+",
        f"\\g<1>{commits}",
        content,
    )
    # Update loc value (in K)
    content = re.sub(
        r"(loc:\s*\{\s*value:\s*)\d+",
        f"\\g<1>{loc_k}",
        content,
    )
    # Update tests value
    content = re.sub(
        r"(tests:\s*)\d+(\s*,\s*models:)",
        f"\\g<1>{tests}\\2",
        content,
    )
    # Update data-target attributes in stat cards
    content = re.sub(
        r'(data-target=")(\d+)(" data-suffix="\+?" data-metric="commits")',
        f'\\g<1>{commits}\\3',
        content,
    )
    content = re.sub(
        r'(data-target=")(\d+)(" data-suffix="" data-metric="repos")',
        f'\\g<1>{repos}\\3',
        content,
    )
    content = re.sub(
        r'(data-target=")(\d+)(" data-suffix="K\+?" data-metric="loc")',
        f'\\g<1>{loc_k}\\3',
        content,
    )
    content = re.sub(
        r'(data-target=")(\d+)(" data-suffix="\+?" data-metric="tests")',
        f'\\g<1>{tests}\\3',
        content,
    )
    # Update boot sequence numbers
    content = re.sub(
        r'(data-metric="repos"[^>]*>)\d+ found',
        f'\\g<1>{repos} found',
        content,
    )
    content = re.sub(
        r'(data-metric="commits"[^>]*>)\d[,\d]*\+? verified',
        f'\\g<1>{commits:,}+ verified',
        content,
    )
    content = re.sub(
        r'(data-metric="loc"[^>]*>)\d+K\+? lines',
        f'\\g<1>{loc_k}K+ lines',
        content,
    )
    content = re.sub(
        r'(data-metric="tests"[^>]*>)\d+\+? passing',
        f'\\g<1>{tests}+ passing',
        content,
    )

    if content != original:
        HTML_FILE.write_text(content, encoding="utf-8")
        print("  HTML METRICS_CONFIG + stat cards updated")
        return True
    else:
        print("  HTML metrics already current")
        return False


if __name__ == "__main__":
    main()
