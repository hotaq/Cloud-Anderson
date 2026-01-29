#!/usr/bin/env python3
"""
Reflection Generator — Auto create daily reflection template
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def main():
    project_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    # Check if there's an active session
    session_file = project_dir / "ψ" / "active" / ".current_session"

    if not session_file.exists():
        sys.exit(0)

    # Read session path
    with open(session_file, 'r') as f:
        session_path = f.read().strip()

    if not Path(session_path).exists():
        sys.exit(0)

    # Read session to get session name
    with open(session_path, 'r', encoding='utf-8') as f:
        session_content = f.read()

    # Extract session name (first line after # Session: )
    import re
    match = re.search(r'# Session:\s*(.+)', session_content)
    session_name = match.group(1) if match else "Unknown"

    # Load template
    template_file = project_dir / "system" / "templates" / "reflection.md"

    if not template_file.exists():
        print("⚠️ Reflection template not found")
        sys.exit(0)

    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    # Fill template
    now = datetime.now()
    reflection = template.replace("{{DATE}}", now.strftime("%Y-%m-%d"))
    reflection = reflection.replace("{{TIME}}", now.strftime("%H:%M"))
    reflection = reflection.replace("{{AI_NAME}}", "คลอด (Claude Code)")
    reflection = reflection.replace("{{SESSION_NAME}}", session_name)

    # Create reflection file
    retros_dir = project_dir / "ψ" / "retros"
    retros_dir.mkdir(parents=True, exist_ok=True)

    timestamp = now.strftime("%Y%m%d-%H%M%S")
    reflection_file = retros_dir / f"reflection-{timestamp}.md"

    with open(reflection_file, 'w', encoding='utf-8') as f:
        f.write(reflection)

    # Also save as active reflection for easy access
    active_reflection = project_dir / "ψ" / "active" / "reflection.md"
    with open(active_reflection, 'w', encoding='utf-8') as f:
        f.write(reflection)

    print(f"🧠 Reflection template created: {reflection_file}")
    print(f"📝 Active reflection: ψ/active/reflection.md")

if __name__ == "__main__":
    main()
