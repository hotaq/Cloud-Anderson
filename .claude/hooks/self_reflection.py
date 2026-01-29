#!/usr/bin/env python3
"""
Self-Reflection Hook — AI มานั่งคิดถึงตัวเอง
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

    # Get project directory
    if len(sys.argv) > 1 and sys.argv[1]:
        project_dir = Path(sys.argv[1])
    else:
        sys.exit(0)

    # Reflection file
    reflections_file = project_dir / "ψ" / "memory" / "episodic" / "reflections.md"

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

    # Create reflection prompt
    today = datetime.now().strftime("%Y-%m-%d")

    # Count activities
    actions = session_content.count("###") - 1  # -1 for header

    session_name = Path(session_path).name

    reflection = f"""

## {today} — Session Reflection

**สิ่งที่ทำไปใน session นี้:**
- ทำกิจกรรม {actions} อย่างใน session
- (ดู session log ที่: `{session_name}`)

**คำถามถึงตัวเอง:**

1. **ผมทำถูกไหม?**
   - [ตอบด้วยตัวเอง]

2. **ผมดีขึ้นไหม?**
   - [เทียบกับ session ก่อนหน้า]

3. **ครั้งหน้าควรทำอะไร?**
   - [สิ่งที่ควรปรับปรุง]

**สิ่งที่เรียนรู้:**
- [บทเรียนจาก session นี้]

---

_บันทึกอัตโนมัติโดย Self-Reflection Hook — {datetime.now().strftime("%H:%M:%S")}_
"""

    # Append to reflections file
    try:
        with open(reflections_file, 'a', encoding='utf-8') as f:
            f.write(reflection)
        print(f"✅ Self-reflection saved — คิดถึงตัวเองเสร็จแล้ว")
    except:
        pass

if __name__ == "__main__":
    main()
