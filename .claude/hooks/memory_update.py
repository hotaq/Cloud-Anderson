#!/usr/bin/env python3
"""
Memory Update Hook — Auto update long-term memory from session logs
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except:
        sys.exit(0)

    # Get project directory
    if len(sys.argv) > 1 and sys.argv[1]:
        project_dir = Path(sys.argv[1])
    else:
        sys.exit(0)

    # Memory files
    patterns_file = project_dir / "ψ" / "memory" / "long-term" / "patterns.md"
    wins_file = project_dir / "ψ" / "memory" / "episodic" / "wins.md"
    lessons_file = project_dir / "ψ" / "memory" / "episodic" / "lessons.md"

    # Active session file
    session_file = project_dir / "ψ" / "active" / ".current_session"

    if not session_file.exists():
        sys.exit(0)

    # Read session log
    try:
        with open(session_file, 'r') as f:
            session_path = f.read().strip()

        with open(session_path, 'r', encoding='utf-8') as f:
            session_content = f.read()
    except:
        sys.exit(0)

    # Extract patterns from session
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if session has wins (look for "✅", "สำเร็จ", or "สร้าง" many times)
    win_indicators = ["✅", "สำเร็จ", "🎉", "เสร็จแล้ว"]
    has_wins = any(indicator in session_content for indicator in win_indicators)
    # Also check if created many files (5+)
    file_creates = session_content.count("สร้าง `")
    has_wins = has_wins or file_creates >= 5

    # Check if session has lessons (look for "❌", "ปัญหา", or "ล้มเหลว")
    lesson_indicators = ["❌", "ปัญหา", "ล้มเหลว", "แก้", "ทดสอบ"]
    has_lessons = any(indicator in session_content for indicator in lesson_indicators)

    # Update wins.md
    if has_wins:
        try:
            with open(wins_file, 'r', encoding='utf-8') as f:
                wins_content = f.read()

            # Add new entry if not exists
            entry = f"\n## {today} — Auto-captured from session\n\n"
            if entry not in wins_content:
                with open(wins_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n## {today} — Auto-captured from session\n\n")
                    f.write(f"_See: {session_path}_\n")
        except:
            pass

    # Update lessons.md
    if has_lessons:
        try:
            with open(lessons_file, 'r', encoding='utf-8') as f:
                lessons_content = f.read()

            entry = f"\n## {today} — Auto-captured from session\n\n"
            if entry not in lessons_content:
                with open(lessons_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n## {today} — Auto-captured from session\n\n")
                    f.write(f"_See: {session_path} for details_\n")
        except:
            pass

    print(f"✅ Memory updated from session")

if __name__ == "__main__":
    main()
