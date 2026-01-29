#!/usr/bin/env python3
"""
Oracle Handoff System
ส่งมอบงานระหว่าง AI

Usage:
    python system/handoff.py <from> <to> "ข้อความ"
    python system/handoff.py claude peach "ต่อจากตรงนี้..."
"""

import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
HANDOFF_DIR = BASE_DIR / "ψ" / "inbox" / "handoff"
CURRENT_WORK_FILE = BASE_DIR / "system" / "current-work.md"

# AI names mapping
AI_NAMES = {
    'claude': 'คลอด (Claude Code)',
    'codex': 'โคเด็กซ์ (Codex)',
    'opencode': 'พีช (OpenCode)',
    'cloude': 'คลอด (Claude Code)',
    'peach': 'พีช (OpenCode)',
    'max': 'มักซ์ (Max)',
}

def resolve_ai_name(name):
    """แปลงชื่อย่อเป็นชื่อเต็ม"""
    return AI_NAMES.get(name.lower(), name)

def create_handoff(from_ai, to_ai, message):
    """สร้าง handoff note"""

    # สร้าง handoff directory
    HANDOFF_DIR.mkdir(parents=True, exist_ok=True)

    # สร้างไฟล์ handoff
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"handoff-{timestamp}.md"
    handoff_path = HANDOFF_DIR / filename

    # อ่าน current-work.md สำหรับ context
    context = ""
    if CURRENT_WORK_FILE.exists():
        with open(CURRENT_WORK_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # ดึงส่วนงานที่กำลังทำ
            lines = content.split('\n')
            in_task_section = False
            context_lines = []
            for line in lines:
                if '## งานที่กำลังทำ' in line or '### 🎯 Task หลัก' in line:
                    in_task_section = True
                if in_task_section:
                    context_lines.append(line)
                if line.startswith('---') and in_task_section and len(context_lines) > 5:
                    break
            if context_lines:
                context = '\n'.join(context_lines[:20])  # เอาแค่ 20 บรรทัด

    # สร้างเนื้อหา handoff
    handoff_content = f"""# Handoff: {from_ai} → {to_ai}

**เวลา:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## ข้อความ

{message}

---

## Context จากงานที่ทำอยู่

{context if context else '_ไม่มี context_'}

---

## สิ่งที่ควรทำต่อ

> AI คนต่อไป ({to_ai}) อ่านตรงนี้

1. อ่าน `system/current-work.md` ให้ละเอียด
2. อ่าน `ψ/memory/logs/` ของวันนี้
3. ตั้งค่า AI ปัจจุบันเป็นตัวเองใน current-work.md
4. เริ่มทำงานต่อ

---

**Status:** 🟡 รอรับงาน

---

_Handoff created by {from_ai} @ {datetime.now().strftime('%H:%M')}_
"""

    # เขียนไฟล์
    with open(handoff_path, 'w', encoding='utf-8') as f:
        f.write(handoff_content)

    print(f"✅ Handoff note created: {handoff_path}")
    return handoff_path

def update_current_work_handoff(from_ai, to_ai, message):
    """Update current-work.md ว่ามี handoff"""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    handoff_entry = f"""

## 🔔 Handoff ({timestamp})

**{from_ai}** → **{to_ai}:** {message}

---

"""

    if CURRENT_WORK_FILE.exists():
        with open(CURRENT_WORK_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        # Insert after the first header
        lines = content.split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('##') and i > 0:
                insert_idx = i
                break
        lines.insert(insert_idx, handoff_entry.strip())
        content = '\n'.join(lines)
    else:
        content = f"""# Current Work

{handoff_entry.strip()}
"""

    with open(CURRENT_WORK_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {CURRENT_WORK_FILE}")

def git_commit_handoff(from_ai, to_ai, message):
    """Commit เพื่อบอก AI ตัวต่อไป"""

    commit_msg = f"🔔 Handoff: {from_ai} → {to_ai}\n\n{message}"

    # git add
    print("📦 Staging handoff...")
    subprocess.run(["git", "add", "."], check=True)

    # git commit
    print(f"🚀 Committing handoff...")
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("✅ Handoff committed successfully!")
    else:
        print("⚠️  Commit failed, but handoff note created")
        print(result.stderr)

def list_handoffs():
    """แสดง handoffs ทั้งหมด"""
    if not HANDOFF_DIR.exists():
        print("❌ No handoffs found")
        return

    handoffs = sorted(HANDOFF_DIR.glob("handoff-*.md"), reverse=True)

    if not handoffs:
        print("❌ No handoffs found")
        return

    print(f"📋 Found {len(handoffs)} handoff(s):\n")

    for handoff in handoffs[:5]:  # แสดง 5 ล่าสุด
        print(f"📄 {handoff.name}")

        # อ่านบรรทัดแรกๆ
        with open(handoff, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            for line in lines:
                if line.strip():
                    print(f"   {line.rstrip()}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Oracle Handoff System - ส่งมอบงานระหว่าง AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python system/handoff.py claude peach "ทำ login system เสร็จแล้ว ช่วยเขียน docs หน่อย"
    python system/handoff.py peach max "index ความรู้ให้หน่อย"
    python system/handoff.py --list
        """
    )

    parser.add_argument('from_ai', nargs='?', help='AI ที่ส่ง (claude, peach, max)')
    parser.add_argument('to_ai', nargs='?', help='AI ที่รับ (claude, peach, max)')
    parser.add_argument('message', nargs='?', help='ข้อความ')
    parser.add_argument('--no-commit', action='store_true', help='ไม่ต้อง commit')
    parser.add_argument('--list', action='store_true', help='แสดง handoffs ทั้งหมด')

    args = parser.parse_args()

    # List command
    if args.list:
        list_handoffs()
        return

    # Check required args
    if not args.from_ai or not args.to_ai or not args.message:
        parser.print_help()
        return

    from_ai = resolve_ai_name(args.from_ai)
    to_ai = resolve_ai_name(args.to_ai)
    message = args.message
    should_commit = not args.no_commit

    # สร้าง handoff note
    create_handoff(from_ai, to_ai, message)

    # Update current-work.md
    update_current_work_handoff(from_ai, to_ai, message)

    # Commit (ถ้าไม่ได้ --no-commit)
    if should_commit:
        git_commit_handoff(from_ai, to_ai, message)

    print(f"\n🎯 Handoff complete: {from_ai} → {to_ai}")
    print(f"💬 {to_ai} will see this on next session!")

if __name__ == "__main__":
    main()
