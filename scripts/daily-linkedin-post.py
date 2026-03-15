"""
Daily LinkedIn Auto-Poster
Researches latest AI agentic news via Firecrawl, drafts a factual 2-3 sentence post,
and publishes to LinkedIn via playwright-cli. Runs headless (no visible windows).

Usage:
    python daily-linkedin-post.py              # research + post
    python daily-linkedin-post.py --dry-run    # research + print, don't post
    python daily-linkedin-post.py --review     # research + save draft, post on next run if approved

Scheduled via Windows Task Scheduler to run daily.
Requires: FIRECRAWL_API_KEY env var, Ollama running locally, playwright-cli installed.
"""

import subprocess
import json
import os
import sys
import re
from datetime import datetime, timezone
from pathlib import Path

DRAFT_DIR = Path("C:/Users/dbhav/Projects/portfolio/linkedin-drafts")
DRAFT_DIR.mkdir(exist_ok=True)
LOG_FILE = DRAFT_DIR / "post-log.json"
PENDING_FILE = DRAFT_DIR / "pending-post.txt"


def log_post(content: str, status: str):
    """Append to post log."""
    log = []
    if LOG_FILE.exists():
        try:
            log = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            log = []
    log.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "content": content,
        "status": status,
    })
    LOG_FILE.write_text(json.dumps(log, indent=2), encoding="utf-8")


def firecrawl_search(query: str) -> str:
    """Run firecrawl search and return results."""
    # Windows requires .cmd extension for npm global binaries in subprocess
    firecrawl_cmd = "firecrawl.cmd" if sys.platform == "win32" else "firecrawl"
    try:
        result = subprocess.run(
            [firecrawl_cmd, "search", query],
            capture_output=True, timeout=60,
            env={**os.environ}
        )
        return result.stdout.decode("utf-8", errors="replace")
    except FileNotFoundError:
        # Try full path as fallback
        full_path = os.path.expanduser("~/AppData/Roaming/npm/firecrawl.cmd")
        result = subprocess.run(
            [full_path, "search", query],
            capture_output=True, timeout=60,
            env={**os.environ}
        )
        return result.stdout.decode("utf-8", errors="replace")


def generate_post_with_ollama(research: str) -> str:
    """Use local Ollama (qwen3:8b) via chat API to generate a factual 2-3 sentence post."""
    import urllib.request

    user_prompt = f"""Based on this research about the latest AI agentic developments, write a LinkedIn post.

Rules:
- 2-3 sentences max
- Factual only, no opinions, no hype
- Just interesting finds
- Include 3-4 relevant hashtags at the end
- No emojis
- Write as a knowledgeable AI engineer sharing a find, not a marketer

Research:
{research[:3000]}"""

    try:
        payload = json.dumps({
            "model": "qwen3:30b",
            "messages": [
                {"role": "system", "content": "You are a concise LinkedIn post writer for an AI engineer. Write short, factual posts. Output only the post text and hashtags, nothing else."},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 2048}
        }).encode("utf-8")

        req = urllib.request.Request(
            "http://localhost:11434/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            response_text = data.get("message", {}).get("content", "").strip()
            # qwen3 may include thinking tags — strip them
            response_text = re.sub(r'<think>.*?</think>', '', response_text, flags=re.DOTALL).strip()
            return response_text
    except Exception as e:
        print(f"Ollama error: {e}")
        # Fallback: try Claude API if ANTHROPIC_API_KEY is set
        if os.environ.get("ANTHROPIC_API_KEY"):
            try:
                import anthropic
                client = anthropic.Anthropic()
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=300,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return message.content[0].text.strip()
            except Exception as e2:
                print(f"Claude fallback error: {e2}")
        return ""


def post_to_linkedin(content: str) -> bool:
    """Post to LinkedIn using playwright-cli (headless)."""
    try:
        # Open browser with persistent session (headless - no --headed flag)
        subprocess.run(
            ["playwright-cli", "open", "--persistent", "--browser", "chrome",
             "https://www.linkedin.com/in/dbhavery/?isSelfProfile=true"],
            capture_output=True, text=True, timeout=30
        )

        import time
        time.sleep(5)

        # Take snapshot to find Create Post
        snap = subprocess.run(["playwright-cli", "snapshot"], capture_output=True, text=True, timeout=15)
        snap_out = snap.stdout

        # Check if logged in
        if "Sign In" in snap_out and "Create a post" not in snap_out:
            print("ERROR: Not logged in. Run 'playwright-cli open --headed --persistent --browser chrome https://linkedin.com' to log in first.")
            subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
            return False

        # Find and click Create a post - get latest snapshot file
        import glob
        snapshots = sorted(glob.glob("C:/Users/dbhav/.playwright-cli/page-*.yml"), key=os.path.getmtime, reverse=True)
        if not snapshots:
            print("ERROR: No snapshot files found")
            subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
            return False

        latest = snapshots[0]
        with open(latest) as f:
            snap_content = f.read()

        # Find Create a post ref
        match = re.search(r'link "Create a post".*?ref=(e\d+)', snap_content)
        if not match:
            print("ERROR: Could not find Create a post button")
            subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
            return False

        post_ref = match.group(1)
        subprocess.run(["playwright-cli", "click", post_ref], capture_output=True, text=True, timeout=10)
        time.sleep(3)

        # Find text editor
        subprocess.run(["playwright-cli", "snapshot"], capture_output=True, text=True, timeout=15)
        snapshots = sorted(glob.glob("C:/Users/dbhav/.playwright-cli/page-*.yml"), key=os.path.getmtime, reverse=True)
        latest = snapshots[0]
        with open(latest) as f:
            snap_content = f.read()

        match = re.search(r'textbox "Text editor.*?".*?ref=(e\d+)', snap_content)
        if not match:
            print("ERROR: Could not find text editor")
            subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
            return False

        text_ref = match.group(1)
        subprocess.run(["playwright-cli", "fill", text_ref, content], capture_output=True, text=True, timeout=30)
        time.sleep(2)

        # Find and click Post button
        subprocess.run(["playwright-cli", "snapshot"], capture_output=True, text=True, timeout=15)
        snapshots = sorted(glob.glob("C:/Users/dbhav/.playwright-cli/page-*.yml"), key=os.path.getmtime, reverse=True)
        latest = snapshots[0]
        with open(latest) as f:
            snap_content = f.read()

        match = re.search(r'button "Post".*?ref=(e\d+)', snap_content)
        if not match:
            print("ERROR: Could not find Post button")
            subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
            return False

        btn_ref = match.group(1)
        subprocess.run(["playwright-cli", "click", btn_ref], capture_output=True, text=True, timeout=10)
        time.sleep(3)

        # Verify
        snap = subprocess.run(["playwright-cli", "snapshot"], capture_output=True, text=True, timeout=15)
        success = "Post successful" in snap.stdout

        subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
        return success

    except Exception as e:
        print(f"LinkedIn posting error: {e}")
        try:
            subprocess.run(["playwright-cli", "close"], capture_output=True, timeout=10)
        except Exception:
            pass
        return False


def main():
    dry_run = "--dry-run" in sys.argv
    review_mode = "--review" in sys.argv

    # Check if there's a pending post from review mode
    if PENDING_FILE.exists() and not dry_run and not review_mode:
        content = PENDING_FILE.read_text(encoding="utf-8").strip()
        if content:
            print(f"Posting pending draft:\n{content}\n")
            if post_to_linkedin(content):
                log_post(content, "posted")
                PENDING_FILE.unlink()
                print("Posted successfully!")
            else:
                log_post(content, "post_failed")
                print("Post failed!")
            return

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] Researching latest AI agentic news...")

    queries = [
        "AI agentic framework new release announcement this week 2026",
        "AI agent protocol MCP A2A new feature this week March 2026",
        "agentic AI novel project open source release March 2026",
    ]

    all_research = ""
    for q in queries:
        result = firecrawl_search(q)
        all_research += result + "\n\n"

    if not all_research.strip():
        print("No research results. Skipping.")
        log_post("", "no_research")
        return

    # Condense research to key findings (Ollama struggles with long raw input)
    lines = all_research.split("\n")
    findings = []
    for line in lines:
        line = line.strip()
        # Keep title lines and short description lines
        if line and not line.startswith("URL:") and not line.startswith("http") and len(line) > 20 and len(line) < 300:
            findings.append(line)
    condensed = "\n".join(findings[:15])[:1500]  # Keep under 1500 chars for Ollama

    if not condensed.strip():
        print("No usable findings after filtering. Skipping.")
        log_post("", "no_findings")
        return

    print(f"Condensed research to {len(condensed)} chars from {len(all_research)} chars")
    print("Generating post with Ollama (qwen3:8b)...")
    post_content = generate_post_with_ollama(condensed)

    if not post_content:
        print("Failed to generate post. Skipping.")
        log_post("", "generation_failed")
        return

    print(f"\n--- Generated Post ---\n{post_content}\n--- End ---\n")

    if dry_run:
        log_post(post_content, "dry_run")
        print("Dry run — not posting.")
        return

    if review_mode:
        PENDING_FILE.write_text(post_content, encoding="utf-8")
        log_post(post_content, "pending_review")
        print(f"Saved to {PENDING_FILE} for review.")
        print("Run without --review to post it, or edit the file first.")
        return

    # Post directly
    print("Posting to LinkedIn...")
    if post_to_linkedin(post_content):
        log_post(post_content, "posted")
        print("Posted successfully!")
    else:
        log_post(post_content, "post_failed")
        print("Post failed! Saved as pending.")
        PENDING_FILE.write_text(post_content, encoding="utf-8")


if __name__ == "__main__":
    main()
