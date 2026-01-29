# Code Patterns Library — Patterns ที่พบ

> "สิ่งที่เราทำซ้ำๆ — คือสิ่งที่เราเป็น"

---

## Last Updated: 2026-01-29

---

## Helper Functions

### Pattern: Date Formatting

**ตัวอย่าง:**
```python
def format_date(dt):
    return dt.strftime("%Y-%m-%d")
```

**พบบ่อยใน:** `utils/`, `helpers/`

**ความถี่:** 🔴 สูง

---

### Pattern: Input Sanitization

**ตัวอย่าง:**
```python
def sanitize_input(text):
    return text.strip().lower()
```

**พบบ่อยใน:** API endpoints, forms

**ความถี่:** 🔴 สูง

---

## Error Handling

### Pattern: Try-Catch with Logging

**ตัวอย่าง:**
```python
try:
    risky_operation()
except Exception as e:
    logger.error(f"Failed: {e}")
    raise
```

**พบบ่อยใน:** ทุกที่

**ความถี่:** 🔴 สูง

---

## Constants

### Pattern: Config Constants

**ตัวอย่าง:**
```python
MAX_RETRIES = 3
API_TIMEOUT = 30
DB_HOST = "localhost"
```

**พบบ่อยใน:** `config.py`, `.env`

**ความถี่:** 🟡 กลาง

---

## Type Guards

### Pattern: Type Checking

**ตัวอย่าง:**
```python
if isinstance(x, str):
    process_string(x)
elif isinstance(x, int):
    process_number(x)
```

**พบบ่อยใน:** Dynamic typing code

**ความถี่:** 🟡 กลาง

---

## Template สำหรับบันทึก Pattern ใหม่

```markdown
### Pattern: [ชื่อ Pattern]

**ตัวอย่าง:**
\`\`\`[language]
[code]
\`\`\`

**พบบ่อยใน:** [ตำแหน่ง]

**ความถี่:** [🔴 สูง / 🟡 กลาง / 🟢 ต่ำ]

**เหตุผล:** [ทำไม pattern นี้ดี]
```

---

_อัปเดตล่าสุด: 2026-01-29 23:30_

## Scan Results — 2026-01-29 23:40

### Function Naming: update_* prefix

**ความถี่:** 4 ครั้ง

**ตัวอย่าง:**
```python
  update_current_work
  update_current_work_handoff
  update_patterns_file
```

---

### Import: sys

**ความถี่:** 5 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Import: datetime.datetime

**ความถี่:** 5 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Import: pathlib.Path

**ความถี่:** 5 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Import: argparse

**ความถี่:** 4 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Import: os

**ความถี่:** 3 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Import: subprocess

**ความถี่:** 2 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Import: re

**ความถี่:** 2 ครั้ง

**หมายเหตุ:** ใช้บ่อย

---

### Error Handling: except subprocess.CalledProcessError

**ความถี่:** 1 ครั้ง

---

### Error Handling: except Exception

**ความถี่:** 1 ครั้ง

---

### Error Handling: except SyntaxError

**ความถี่:** 1 ครั้ง

---

