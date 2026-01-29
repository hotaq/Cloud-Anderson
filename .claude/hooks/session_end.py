#!/usr/bin/env python3
"""
SessionEnd Hook — Auto save session when ending
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except:
        # If no input, just exit
        sys.exit(0)

    project_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    # Check if there's an active session
    session_file = project_dir / "ψ" / "active" / ".current_session"

    if not session_file.exists():
        # No active session, nothing to do
        sys.exit(0)

    # Read session path
    with open(session_file, 'r') as f:
        session_path = f.read().strip()

    if not Path(session_path).exists():
        sys.exit(0)

    # Read session content
    with open(session_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add session end marker
    end_marker = f"""

---

**Session Ended:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Auto)

---

"""

    content = content + end_marker

    # Move to logs
    date_str = datetime.now().strftime("%Y-%m-%d")
    logs_dir = project_dir / "ψ" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / f"{date_str}.md"

    # Append if exists
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            existing = f.read()
        content = existing + "\n\n---\n\n" + content

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Clean up
    Path(session_path).unlink()
    session_file.unlink(missing_ok=True)

    print(f"✅ Session auto-saved to: {log_file}")

if __name__ == "__main__":
    main()
