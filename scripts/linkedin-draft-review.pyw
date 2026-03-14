"""
LinkedIn Draft Review Pop-up
Shows a GUI window with the daily draft post for review.
User can Approve (posts immediately), Edit (opens in notepad), or Skip.
Runs via Task Scheduler at 8:10 AM before the auto-poster.

Uses .pyw extension so no console window appears.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import json
import os
import sys
from datetime import datetime
from pathlib import Path

DRAFT_DIR = Path("C:/Users/dbhav/Projects/portfolio/linkedin-drafts")
PENDING_FILE = DRAFT_DIR / "pending-post.txt"
LOG_FILE = DRAFT_DIR / "post-log.json"
SCRIPT = Path("C:/Users/dbhav/Projects/portfolio/scripts/daily-linkedin-post.py")
PYTHON = "C:/Users/dbhav/AppData/Local/Programs/Python/Python313/python.exe"


def log_action(content: str, status: str):
    log = []
    if LOG_FILE.exists():
        try:
            log = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
    log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "content": content[:200],
        "status": status,
    })
    LOG_FILE.write_text(json.dumps(log, indent=2), encoding="utf-8")


def generate_draft():
    """Run the research + draft generation (no posting)."""
    try:
        result = subprocess.run(
            [PYTHON, str(SCRIPT), "--review"],
            capture_output=True, text=True, timeout=120,
            env={**os.environ},
            cwd=str(DRAFT_DIR.parent)
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Draft generation failed: {e}")
        return False


def post_draft(content: str):
    """Write content to pending file and run poster without --review."""
    PENDING_FILE.write_text(content, encoding="utf-8")
    try:
        subprocess.Popen(
            [PYTHON, str(SCRIPT)],
            env={**os.environ},
            cwd=str(DRAFT_DIR.parent)
        )
        return True
    except Exception as e:
        messagebox.showerror("Post Error", f"Failed to launch poster: {e}")
        return False


class DraftReviewApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LinkedIn Daily Post Review")
        self.root.configure(bg="#1a1a1a")
        self.root.attributes("-topmost", True)

        # Center on screen
        w, h = 650, 520
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(False, False)

        # Header
        header = tk.Label(
            self.root, text="LinkedIn Daily Post",
            font=("Segoe UI", 16, "bold"), fg="white", bg="#1a1a1a"
        )
        header.pack(pady=(15, 5))

        date_label = tk.Label(
            self.root, text=datetime.now().strftime("%A, %B %d, %Y — %I:%M %p"),
            font=("Segoe UI", 10), fg="#888", bg="#1a1a1a"
        )
        date_label.pack(pady=(0, 10))

        # Status
        self.status_var = tk.StringVar(value="Loading draft...")
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Segoe UI", 9), fg="#aaa", bg="#1a1a1a"
        )
        self.status_label.pack()

        # Text area
        text_frame = tk.Frame(self.root, bg="#2a2a2a", padx=2, pady=2)
        text_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.text = tk.Text(
            text_frame, wrap="word", font=("Segoe UI", 11),
            bg="#2a2a2a", fg="white", insertbackground="white",
            relief="flat", padx=12, pady=12,
            selectbackground="#3a5a8a"
        )
        self.text.pack(fill="both", expand=True)

        # Character count
        self.char_var = tk.StringVar(value="0 chars")
        char_label = tk.Label(
            self.root, textvariable=self.char_var,
            font=("Segoe UI", 9), fg="#666", bg="#1a1a1a"
        )
        char_label.pack(pady=(0, 5))
        self.text.bind("<<Modified>>", self._update_char_count)
        self.text.bind("<KeyRelease>", lambda e: self._update_char_count())

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1a1a1a")
        btn_frame.pack(pady=(0, 15))

        self.approve_btn = tk.Button(
            btn_frame, text="Approve & Post", font=("Segoe UI", 11, "bold"),
            bg="#0a66c2", fg="white", activebackground="#004182",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._approve
        )
        self.approve_btn.pack(side="left", padx=8)

        self.skip_btn = tk.Button(
            btn_frame, text="Skip Today", font=("Segoe UI", 11),
            bg="#333", fg="white", activebackground="#555",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._skip
        )
        self.skip_btn.pack(side="left", padx=8)

        self.regen_btn = tk.Button(
            btn_frame, text="New Draft", font=("Segoe UI", 11),
            bg="#333", fg="white", activebackground="#555",
            relief="flat", padx=20, pady=8, cursor="hand2",
            command=self._regenerate
        )
        self.regen_btn.pack(side="left", padx=8)

        # Load draft after window shows
        self.root.after(100, self._load_draft)

    def _update_char_count(self, event=None):
        content = self.text.get("1.0", "end-1c")
        self.char_var.set(f"{len(content)} chars")
        self.text.edit_modified(False)

    def _load_draft(self):
        """Load existing draft or generate new one."""
        if PENDING_FILE.exists():
            content = PENDING_FILE.read_text(encoding="utf-8").strip()
            if content:
                self.text.delete("1.0", "end")
                self.text.insert("1.0", content)
                self.status_var.set("Draft loaded from pending file. Edit below or approve.")
                self._update_char_count()
                return

        self.status_var.set("Generating fresh draft... (researching + writing)")
        self.root.update()
        self._set_buttons_state("disabled")

        # Run in thread to not block UI
        import threading
        def gen():
            success = generate_draft()
            self.root.after(0, lambda: self._on_draft_generated(success))
        threading.Thread(target=gen, daemon=True).start()

    def _on_draft_generated(self, success):
        self._set_buttons_state("normal")
        if success and PENDING_FILE.exists():
            content = PENDING_FILE.read_text(encoding="utf-8").strip()
            self.text.delete("1.0", "end")
            self.text.insert("1.0", content)
            self.status_var.set("Fresh draft generated. Edit below or approve.")
        else:
            self.text.delete("1.0", "end")
            self.text.insert("1.0", "(Draft generation failed. Type manually or click New Draft to retry.)")
            self.status_var.set("Generation failed. Check API keys and firecrawl.")
        self._update_char_count()

    def _set_buttons_state(self, state):
        self.approve_btn.config(state=state)
        self.skip_btn.config(state=state)
        self.regen_btn.config(state=state)

    def _approve(self):
        content = self.text.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Empty", "No content to post.")
            return

        self.status_var.set("Posting to LinkedIn...")
        self.root.update()
        self._set_buttons_state("disabled")

        if post_draft(content):
            self.status_var.set("Post submitted! Check LinkedIn to verify.")
            log_action(content, "approved_and_posted")
            self.root.after(3000, self.root.destroy)
        else:
            self.status_var.set("Post failed. Draft saved for retry.")
            self._set_buttons_state("normal")

    def _skip(self):
        log_action("", "skipped")
        if PENDING_FILE.exists():
            PENDING_FILE.unlink()
        self.root.destroy()

    def _regenerate(self):
        if PENDING_FILE.exists():
            PENDING_FILE.unlink()
        self.status_var.set("Generating new draft...")
        self.root.update()
        self._set_buttons_state("disabled")

        import threading
        def gen():
            success = generate_draft()
            self.root.after(0, lambda: self._on_draft_generated(success))
        threading.Thread(target=gen, daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    DRAFT_DIR.mkdir(exist_ok=True)
    app = DraftReviewApp()
    app.run()
