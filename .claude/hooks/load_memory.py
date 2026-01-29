#!/usr/bin/env python3
"""
Load Short-term Memory Hook — Load working memory at session start
"""
import sys
from pathlib import Path

def main():
    # Get project directory
    if len(sys.argv) > 1 and sys.argv[1]:
        project_dir = Path(sys.argv[1])
    else:
        sys.exit(0)

    # Short-term memory file
    context_file = project_dir / "ψ" / "memory" / "short-term" / "context.md"

    if not context_file.exists():
        sys.exit(0)

    # Read and display short-term memory
    try:
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if content.strip():
            # Display as additional context for AI
            print("\n" + "="*60)
            print("🧠 WORKING MEMORY")
            print("="*60)
            print(content)
            print("="*60 + "\n")
    except:
        sys.exit(0)

if __name__ == "__main__":
    main()
