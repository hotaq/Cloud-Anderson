#!/usr/bin/env python3
"""
PostToolUse Hook — Auto log file edits with deduplication
"""
import fcntl
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

    # Get tool info
    tool_name = input_data.get('tool_name', '')
    tool_input = input_data.get('tool_input', {})
    tool_use_id = input_data.get('tool_use_id', '')

    # Only log Edit, Write, NotebookEdit, MultiEdit tools
    if tool_name not in ['Edit', 'Write', 'NotebookEdit', 'MultiEdit']:
        sys.exit(0)

    file_path = tool_input.get('file_path', '')
    if not file_path:
        sys.exit(0)

    # Detect project directory
    if len(sys.argv) > 1 and sys.argv[1]:
        project_dir = Path(sys.argv[1])
    else:
        path = Path(file_path).resolve()
        project_dir = None
        for parent in [path] + list(path.parents):
            if (parent / '.claude').exists() or (parent / 'ψ').exists():
                project_dir = parent
                break
        if not project_dir:
            sys.exit(0)

    # Deduplication using tool_use_id with file locking
    dedup_file = project_dir / "ψ" / "active" / ".hook_dedup"
    if tool_use_id:
        try:
            # Open file with exclusive lock
            with open(dedup_file, 'a+') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
                f.seek(0)  # Read from beginning
                processed_ids = set(f.read().split())
                if tool_use_id in processed_ids:
                    sys.exit(0)
        except:
            pass

    # Get relative path
    try:
        rel_path = Path(file_path).relative_to(project_dir)
    except:
        rel_path = Path(file_path).name

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

    # Append entry first
    with open(session_path, 'a', encoding='utf-8') as f:
        f.write(entry)

    # Clean up duplicates (after writing)
    try:
        with open(session_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove consecutive duplicates
        lines = content.split('\n')
        cleaned_lines = []
        prev_line = None

        for line in lines:
            if line != prev_line:
                cleaned_lines.append(line)
                prev_line = line
            # Skip if same as previous (duplicate)

        # Write back if changed
        if len(cleaned_lines) != len(lines):
            with open(session_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(cleaned_lines))
    except:
        pass

    # Mark this tool_use_id as processed (best effort)
    if tool_use_id:
        try:
            with open(dedup_file, 'a') as f:
                f.write(f"{tool_use_id}\n")
        except:
            pass

    # Silent — no output to save context
    sys.exit(0)

if __name__ == "__main__":
    main()
