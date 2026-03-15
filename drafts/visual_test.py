"""Visual Avatar Test — Playwright screenshots of the portfolio page.

Takes screenshots of the avatar in idle, during animation, and after animation
so we can inspect visual quality (white fringe, positioning, bevel, etc).

Usage:
    python visual_test.py              # take all screenshots
    python visual_test.py --refresh    # reload page and re-take
    python visual_test.py --click q1   # click a specific question and screenshot
"""

import argparse
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PAGE_URL = (Path(__file__).parent / "draft-e-neural-command.html").as_uri()
SCREENSHOT_DIR = Path(__file__).parent / "test_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

# Reuse a single browser context across calls
_browser = None
_page = None


def get_page(pw):
    global _browser, _page
    if _browser is None:
        _browser = pw.chromium.launch(headless=True)
        _page = _browser.new_page(viewport={"width": 1440, "height": 900})
        _page.goto(PAGE_URL, wait_until="networkidle")
        _page.wait_for_timeout(2000)  # let animations/videos start
    return _page


def screenshot(page, name, selector=None):
    """Take a screenshot, optionally of a specific element."""
    path = SCREENSHOT_DIR / f"{name}.png"
    if selector:
        el = page.query_selector(selector)
        if el:
            el.screenshot(path=str(path))
        else:
            print(f"  [warn] Selector '{selector}' not found, taking full page")
            page.screenshot(path=str(path))
    else:
        page.screenshot(path=str(path))
    print(f"  Saved: {path}")
    return path


def run_visual_test(click_q=None, refresh=False):
    with sync_playwright() as pw:
        page = get_page(pw)

        if refresh:
            print("[refresh] Reloading page...")
            page.reload(wait_until="networkidle")
            page.wait_for_timeout(2000)

        # 1. Full page screenshot
        print("\n[1] Full page overview")
        screenshot(page, "01_full_page")

        # 2. Avatar circle — idle state
        print("[2] Avatar idle state (zoomed)")
        screenshot(page, "02_avatar_idle", ".hero-photo-wrap")

        # 3. Avatar inner circle only
        print("[3] Inner circle detail")
        screenshot(page, "03_inner_circle", ".hero-photo-inner")

        # 4. Click a question and capture during animation
        target_q = click_q or "q1"
        print(f"[4] Clicking {target_q}...")

        # Find the question button
        btn = page.query_selector(f'button.avatar-q[data-video*="{target_q}.webm"]')
        if btn:
            btn.click()
            # Wait for video to start
            page.wait_for_timeout(1500)

            print("[5] Avatar during speech (1.5s after click)")
            screenshot(page, f"04_speaking_{target_q}_1500ms", ".hero-photo-wrap")

            page.wait_for_timeout(2000)
            print("[6] Avatar during speech (3.5s after click)")
            screenshot(page, f"05_speaking_{target_q}_3500ms", ".hero-photo-wrap")

            # Wait for it to end or take another mid-point
            page.wait_for_timeout(3000)
            print("[7] Avatar mid-speech (6.5s after click)")
            screenshot(page, f"06_speaking_{target_q}_6500ms", ".hero-photo-wrap")
        else:
            print(f"  [warn] Could not find button for {target_q}")

        # 8. After video ends — wait and capture return to idle
        print("[8] Waiting for video to end...")
        page.wait_for_timeout(30000)  # wait up to 30s
        print("[9] Avatar after speech (returned to idle)")
        screenshot(page, "07_after_speech_idle", ".hero-photo-wrap")

        # Close
        _browser.close()

    print(f"\nAll screenshots saved to: {SCREENSHOT_DIR}")
    print("Files:")
    for f in sorted(SCREENSHOT_DIR.glob("*.png")):
        print(f"  {f.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--click", default=None, help="Question to click (e.g. q1)")
    parser.add_argument("--refresh", action="store_true", help="Reload page first")
    args = parser.parse_args()
    run_visual_test(click_q=args.click, refresh=args.refresh)
