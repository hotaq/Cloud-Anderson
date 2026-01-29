#!/usr/bin/env python3
"""
SessionStart Hook — Auto load context when starting new session
"""
import json
import sys
from pathlib import Path

def main():
    project_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    # Load current work
    current_work = project_dir / "system" / "current-work.md"

    if current_work.exists():
        with open(current_work, 'r', encoding='utf-8') as f:
            content = f.read()

        # Print context (Claude will see this)
        print("\n" + "="*60)
        print("📋 CURRENT WORK CONTEXT")
        print("="*60)
        print(content)
        print("="*60 + "\n")

    # Check for active session
    session_file = project_dir / "ψ" / "active" / ".current_session"

    if session_file.exists():
        with open(session_file, 'r') as f:
            session_path = f.read().strip()

        if Path(session_path).exists():
            with open(session_path, 'r', encoding='utf-8') as f:
                session_content = f.read()

            print("\n" + "="*60)
            print("🔄 ACTIVE SESSION")
            print("="*60)
            print(session_content)
            print("="*60 + "\n")

if __name__ == "__main__":
    main()
