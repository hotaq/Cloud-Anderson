#!/usr/bin/env python3
"""
Oracle Git Commit Wrapper
Commit พร้อม log context อัตโนมัติ

Usage:
    python system/git_commit.py "commit message"
    python system/git_commit.py "✅ เสร็จแล้ว — งาน X" --mention @พีช
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
SESSION_FILE = BASE_DIR / "ψ" / "active" / ".current_session"
FOCUS_FILE = BASE_DIR / "ψ" / "inbox" / "focus.md"

def get_current_session():
    """ดึง session ปัจจุบัน"""
    if SESSION_FILE.exists():
        with open(SESSION_FILE, 'r') as f:
            return f.read().strip()
    return None

def end_current_session():
    """จบ session ถ้ามี"""
    session_path = get_current_session()
    if session_path and Path(session_path).exists():
        # เรียก context_logger.py end
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "system" / "context_logger.py"), "end"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"📝 {result.stdout.strip()}")

def update_focus(commit_message):
    """Update ψ/inbox/focus.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if not FOCUS_FILE.exists():
        print(f"⚠️  Focus file not found: {FOCUS_FILE}")
        return

    with open(FOCUS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update timestamp and add to log
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        # Update timestamp
        if line.startswith('| **เวลา** |'):
            new_lines.append(f'| **เวลา** | {datetime.now().strftime("%H:%M")} น. |')
        # Update AI
        elif line.startswith('| **AI ปัจจุบัน** |'):
            new_lines.append('| **AI ปัจจุบัน** | คลอด (Claude Code) |')
        else:
            new_lines.append(line)

    # Add log entry at the end
    new_lines.append(f"\n### {timestamp}")
    new_lines.append(f"{commit_message}")

    with open(FOCUS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    print(f"✅ Updated {FOCUS_FILE}")

def git_commit(message, mention=None):
    """ทำ git commit"""

    # 1. จบ session ก่อน (ถ้ามี)
    end_current_session()

    # 2. Update current-work.md
    update_current_work(message)

    # 3. git add
    print("📦 Staging changes...")
    subprocess.run(["git", "add", "."], check=True)

    # 4. git commit
    commit_msg = message
    if mention:
        commit_msg = f"{message}\n\n{mention}"

    print(f"🚀 Committing: {message}")
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Committed successfully!")
        print(result.stdout)
    else:
        print("❌ Commit failed!")
        print(result.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Oracle Git Commit Wrapper - Commit พร้อม log context",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python system/git_commit.py "✅ เสร็จแล้ว — สร้างระบบ login"
    python system/git_commit.py "✅ สร้างระบบ login เสร็จแล้ว" --mention "@พีช ช่วยเขียน docs หน่อย"
        """
    )

    parser.add_argument('message', help='Commit message')
    parser.add_argument('--mention', '-m', help='Mention another AI (เช่น: @พีช)')
    parser.add_argument('--no-log', action='store_true', help='ไม่ต้องจบ session')

    args = parser.parse_args()

    # ถ้าไม่ได้ติ๊ก --no-log ให้จบ session ก่อน
    if not args.no_log:
        end_current_session()

    # Update focus.md
    update_focus(args.message)

    # git add
    print("📦 Staging changes...")
    try:
        subprocess.run(["git", "add", "."], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to stage changes")
        sys.exit(1)

    # git commit
    commit_msg = args.message
    if args.mention:
        commit_msg = f"{args.message}\n\n{args.mention}"

    print(f"🚀 Committing: {args.message}")
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Committed successfully!")
    else:
        print("❌ Commit failed!")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
