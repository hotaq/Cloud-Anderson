#!/usr/bin/env python3
"""
Oracle Pattern Auto-Extractor
ดึง patterns จาก episodic/lessons → long-term/patterns.md

Usage:
    python system/pattern_extractor.py
    python system/pattern_extractor.py --dry-run
"""

import argparse
import re
from datetime import datetime
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
LESSONS_FILE = BASE_DIR / "ψ" / "memory" / "episodic" / "lessons.md"
WINS_FILE = BASE_DIR / "ψ" / "memory" / "episodic" / "wins.md"
PATTERNS_FILE = BASE_DIR / "ψ" / "memory" / "long-term" / "patterns.md"
CODE_PATTERNS_FILE = BASE_DIR / "ψ" / "memory" / "long-term" / "patterns" / "code_patterns_library.md"

def extract_patterns_from_file(file_path):
    """ดึง patterns จากไฟล์"""
    if not file_path.exists():
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    patterns = []

    # ดึงจาก lessons - หา pattern indicators
    lesson_pattern = r'-+\s*\*\*(.+?)\*\*:?\s*(.+?)(?=\n-|\n\n|$)'
    matches = re.findall(lesson_pattern, content, re.MULTILINE | re.DOTALL)

    for label, text in matches:
        if any(keyword in label.lower() for keyword in ['pattern', 'พบ', 'เจอ', 'สังเกต', 'ซ้ำ']):
            patterns.append({
                'type': 'lesson',
                'label': label.strip(),
                'content': text.strip(),
                'source': file_path.name
            })

    # ดึงจาก wins - หา best practices
    win_pattern = r'\*\*Result:\*\*\s*\n((?:-\s+.+\n)+)'
    matches = re.findall(win_pattern, content, re.MULTILINE)

    for match in matches:
        for line in match.split('\n'):
            if line.strip().startswith('-'):
                patterns.append({
                    'type': 'win',
                    'label': 'Best Practice',
                    'content': line.strip()[1:].strip(),
                    'source': file_path.name
                })

    return patterns

def count_pattern_frequency(patterns):
    """นับความถี่ของ patterns"""
    pattern_counts = {}

    for p in patterns:
        key = p['content'][:50]  # ใช้ 50 ตัวอักษรแรกเป็น key
        if key not in pattern_counts:
            pattern_counts[key] = []
        pattern_counts[key].append(p)

    return pattern_counts

def update_patterns_file(new_patterns, dry_run=False):
    """อัปเดต long-term/patterns.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d")

    if not PATTERNS_FILE.exists():
        content = f"""# Long-term Memory — Patterns

> "สิ่งที่เรียนรู้ — Pattern ที่ซ้ำๆ"

---

## User Patterns

### การสื่อสาร
| วันที่ | Pattern | ความถี่ |
|---------|---------|----------|
| {timestamp} | Auto-extracted first run | - |

### การทำงาน
| วันที่ | Pattern | ความถี่ |
|---------|---------|----------|
| {timestamp} | Auto-extracted first run | - |

---

## Code Patterns

### สิ่งที่ User ชอบ
- ✅ Auto-detecting...

### สิ่งที่ User เกลียด
- ❌ Auto-detecting...

---

## บทเรียนจากงานที่ผ่านมา

### Pattern Extraction ({timestamp})
- Started auto pattern extraction

---

_อัปเดตล่าสุด: {timestamp}_
"""
    else:
        with open(PATTERNS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

    # เพิ่ม patterns ใหม่
    if new_patterns:
        new_section = f"""

## Auto-Extracted Patterns ({timestamp})

"""
        for p in new_patterns:
            new_section += f"### {p['label']}\n"
            new_section += f"- {p['content']}\n"
            new_section += f"_Source: {p['source']}_\n\n"

        # Insert before the last line
        lines = content.split('\n')
        lines.insert(-1, new_section.strip())
        content = '\n'.join(lines)

    if dry_run:
        print("📋 DRY RUN — ไม่บันทึกจริง")
        print("\nPatterns ที่จะเพิ่ม:")
        for p in new_patterns:
            print(f"  - [{p['label']}] {p['content'][:50]}...")
        return

    with open(PATTERNS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Updated {PATTERNS_FILE}")

def main():
    parser = argparse.ArgumentParser(
        description="Oracle Pattern Auto-Extractor",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--dry-run', action='store_true', help='ไม่บันทึกจริง แค่แสดงผล')
    parser.add_argument('--verbose', '-v', action='store_true', help='แสดงรายละเอียด')

    args = parser.parse_args()

    print("🔍 Extracting patterns...")

    # ดึง patterns จากทุกไฟล์
    all_patterns = []
    for file_path in [LESSONS_FILE, WINS_FILE]:
        patterns = extract_patterns_from_file(file_path)
        all_patterns.extend(patterns)

    if args.verbose:
        print(f"\nFound {len(all_patterns)} patterns")

    # นับความถี่
    pattern_counts = count_pattern_frequency(all_patterns)

    # หา patterns ใหม่ (ความถี่ = 1) หรือ ซ้ำ (ความถี่ > 1)
    new_patterns = []
    repeated_patterns = []

    for key, occurrences in pattern_counts.items():
        if len(occurrences) > 1:
            repeated_patterns.append(occurrences[0])
        else:
            new_patterns.append(occurrences[0])

    if args.verbose:
        print(f"  - New patterns: {len(new_patterns)}")
        print(f"  - Repeated patterns: {len(repeated_patterns)}")

    # อัปเดตไฟล์
    update_patterns_file(all_patterns, dry_run=args.dry_run)

    if not args.dry_run and new_patterns:
        print(f"\n✨ Found {len(new_patterns)} new patterns")
    if not args.dry_run and repeated_patterns:
        print(f"🔄 Found {len(repeated_patterns)} repeated patterns (consolidating...)")

if __name__ == "__main__":
    main()
