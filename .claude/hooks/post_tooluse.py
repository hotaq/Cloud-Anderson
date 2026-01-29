#!/usr/bin/env python3
"""
PostToolUse Hook — Auto log file edits
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
        sys.exit(0)

    project_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    # Get tool info
    tool_name = input_data.get('tool', '')
    tool_input = input_data.get('tool_input', {})

    # Only log Edit and Write tools
    if tool_name not in ['Edit', 'Write']:
        sys.exit(0)

    file_path = tool_input.get('file_path', '')

    # Skip non-project files
    if not file_path or not str(file_path).startswith(str(project_dir)):
        sys.exit(0)

    # Get relative path
    try:
        rel_path = Path(file_path).relative_to(project_dir)
    except:
        rel_path = Path(file_path)

    # Check for active session
    session_file = project_dir / "ψ" / "active" / ".current_session"

    if not session_file.exists():
        # No active session, create one
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        new_session_path = project_dir / "ψ" / "active" / "context" / f"session-{timestamp}.md"
        new_session_path.parent.mkdir(parents=True, exist_ok=True)

        content = f"""# Auto Session

**Started:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} (Auto)

---

## Log

"""

        with open(new_session_path, 'w', encoding='utf-8') as f:
            f.write(content)

        with open(session_file, 'w') as f:
            f.write(str(new_session_path))

    # Read current session
    with open(session_file, 'r') as f:
        session_path = f.read().strip()

    # Log the file edit
    timestamp = datetime.now().strftime("%H:%M:%S")
    action = "แก้ไข" if tool_name == 'Edit' else "สร้าง"

    entry = f"""

### {timestamp} [auto]
{action} `{rel_path}`
"""

    with open(session_path, 'a', encoding='utf-8') as f:
        f.write(entry)

    print(f"✅ Logged: {action} {rel_path}")

if __name__ == "__main__":
    main()
