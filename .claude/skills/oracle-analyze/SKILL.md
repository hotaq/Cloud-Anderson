---
name: oracle-analyze
description: Scan codebase และเรียนรู้ patterns อัตโนมัติ ใช้เมื่อต้องการวิเคราะห์โค้ดหา patterns หรือ anti-patterns
argument-hint: [--force]
disable-model-invocation: true
---

# Code Analysis — Oracle Pattern Recognition

Scan โค้ดทั้ง project และเรียนรู้ patterns อัตโนมัติ

## การใช้งาน

```bash
python3 system/code_analyzer.py $ARGUMENTS
```

## ที่อยู่ผลลัพธ์

- **Patterns:** `ψ/memory/long-term/patterns/code_patterns_library.md`
- **Anti-patterns:** `ψ/memory/long-term/patterns/anti_patterns_library.md`

## ที่ scanner หา

- Function naming patterns
- Import patterns
- Error handling patterns
- Magic numbers
- Long functions (> 20 บรรทัด)
- Class definitions
- Code smells

## ตัวอย่าง

```bash
/analyze              # Scan ปกติ
/analyze --force      # Force rescan (ไม่ skip)
```
