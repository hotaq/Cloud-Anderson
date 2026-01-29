#!/usr/bin/env python3
"""
Debug Hook — Log การทำงานของ hooks ทั้งหมด (PASS-THROUGH VERSION)
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path

def main():
    # Get project directory
    if len(sys.argv) > 1 and sys.argv[1]:
        project_dir = Path(sys.argv[1])
    else:
        sys.exit(0)

    # Debug log file
    debug_log = project_dir / "ψ" / "logs" / "hooks_debug.log"

    # Create log directory if not exists
    debug_log.parent.mkdir(parents=True, exist_ok=True)

    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
        input_str = json.dumps(input_data)
    except:
        input_data = {}
        input_str = "{}"

    # Get event info
    hook_event = input_data.get('hook_event_name', 'Unknown')
    tool_name = input_data.get('tool_name', input_data.get('tool', 'N/A'))
    session_id = input_data.get('session_id', 'N/A')[:8]  # Shorten

    # Log format
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    log_entry = f"[{timestamp}] {hook_event}\n  Session: {session_id}\n  Tool: {tool_name}\n  Input: {input_str[:200]}...\n---\n"

    # Append to debug log
    try:
        with open(debug_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except:
        pass

    # IMPORTANT: Pass input to next hooks via stdout
    print(input_str)

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed = time.time() - start_time
    # Log execution time
    if elapsed > 0.1:  # Only log if slow
        try:
            with open(Path(sys.argv[1]) / "ψ" / "logs" / "hooks_debug.log", 'a') as f:
                f.write(f"[SLOW] Debug hook took {elapsed:.3f}s\n")
        except:
            pass
