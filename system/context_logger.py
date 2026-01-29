#!/usr/bin/env python3
"""
Oracle Context Logger
ตัวบันทึก context สำหรับ Oracle Framework

Usage:
    python system/context_logger.py start "ชื่อ session"
    python system/context_logger.py log "ข้อความ log"
    python system/context_logger.py end
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
ACTIVE_DIR = BASE_DIR / "ψ" / "active" / "context"
MEMORY_DIR = BASE_DIR / "ψ" / "logs"
SESSION_FILE = BASE_DIR / "ψ" / "active" / ".current_session"

def get_current_session():
    """ดึง session ปัจจุบัน"""
    if SESSION_FILE.exists():
        with open(SESSION_FILE, 'r') as f:
            return f.read().strip()
    return None

def set_current_session(session_path):
    """ตั้งค่า session ปัจจุบัน"""
    SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, 'w') as f:
        f.write(str(session_path))

def start_session(name):
    """เริ่ม session ใหม่"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"session-{timestamp}.md"
    session_path = ACTIVE_DIR / filename

    # สร้าง session file
    ACTIVE_DIR.mkdir(parents=True, exist_ok=True)
    content = f"""# Session: {name}

**Started:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Log

"""

    with open(session_path, 'w', encoding='utf-8') as f:
        f.write(content)

    set_current_session(session_path)
    print(f"✅ Session started: {name}")
    print(f"📁 {session_path}")

def log_entry(message, tag=None):
    """บันทึก log entry"""
    session_path = get_current_session()

    if not session_path or not Path(session_path).exists():
        print("❌ No active session. Use 'start' command first.")
        sys.exit(1)

    timestamp = datetime.now().strftime("%H:%M:%S")
    tag_str = f" [{tag}]" if tag else ""
    entry = f"\n### {timestamp}{tag_str}\n{message}\n"

    with open(session_path, 'a', encoding='utf-8') as f:
        f.write(entry)

    print(f"✅ Logged{tag_str}: {message}")

def end_session():
    """จบ session และย้ายไป memory"""
    session_path = get_current_session()

    if not session_path or not Path(session_path).exists():
        print("❌ No active session to end.")
        sys.exit(1)

    # อ่านเนื้อหา
    with open(session_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # เพิ่ม end timestamp
    end_time = f"\n\n---\n\n**Ended:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    content = content + end_time

    # สร้างไฟล์ใน memory (ตามวันที่)
    date_str = datetime.now().strftime("%Y-%m-%d")
    memory_file = MEMORY_DIR / f"{date_str}.md"
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    # Append ถ้ามีไฟล์อยู่แล้ว
    if memory_file.exists():
        with open(memory_file, 'r', encoding='utf-8') as f:
            existing = f.read()
        content = existing + "\n\n---\n\n" + content

    with open(memory_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # ลบ session file
    Path(session_path).unlink()
    SESSION_FILE.unlink(missing_ok=True)

    print(f"✅ Session ended and saved to: {memory_file}")

def show_status():
    """แสดงสถานะ"""
    session_path = get_current_session()

    if session_path and Path(session_path).exists():
        print(f"✅ Active session: {Path(session_path).stem}")
        with open(session_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("❌ No active session")

def main():
    parser = argparse.ArgumentParser(
        description="Oracle Context Logger - ตัวบันทึก context",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python system/context_logger.py start "สร้างระบบ login"
    python system/context_logger.py log "สร้าง users table"
    python system/context_logger.py log "เพิ่ม authentication" --tag progress
    python system/context_logger.py end
    python system/context_logger.py status
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='คำสั่ง')

    # Start command
    start_parser = subparsers.add_parser('start', help='เริ่ม session ใหม่')
    start_parser.add_argument('name', help='ชื่อ session')

    # Log command
    log_parser = subparsers.add_parser('log', help='บันทึก log')
    log_parser.add_argument('message', help='ข้อความที่จะบันทึก')
    log_parser.add_argument('--tag', '-t', help='Tag (เช่น: progress, idea, issue)')

    # End command
    subparsers.add_parser('end', help='จบ session')

    # Status command
    subparsers.add_parser('status', help='แสดงสถานะ')

    args = parser.parse_args()

    if args.command == 'start':
        start_session(args.name)
    elif args.command == 'log':
        log_entry(args.message, args.tag)
    elif args.command == 'end':
        end_session()
    elif args.command == 'status':
        show_status()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
