# ψ (Psi) — Oracle Framework Mind

> "External Brain, Not Command"

---

## โครงสร้าง (Structure)

```
ψ/
├── active/           # Sessions ที่กำลังทำอยู่
├── logs/             # Logs รายวัน
├── learnings/        # สิ่งที่เรียนรู้
├── retros/           # Retrospectives
├── inbox/            # Handoffs & incoming
├── incubate/         # ไอเดียกำลังบ่ม
├── drafts/           # งานร่าง
└── core/             # Core docs (identity, oracle)
```

---

## แต่ละ folder คืออะไร

| Folder | ใช้ทำอะไร | ใครเขียน |
|--------|-----------|---------|
| `active/` | Session ปัจจุบัน | Context Logger |
| `logs/` | Log รายวัน | Context Logger |
| `learnings/` | สิ่งที่เรียนรู้ | Manual |
| `retros/` | Retrospectives | Manual |
| `inbox/` | Handoffs | Handoff System |
| `incubate/` | ไอเดียกำลังบ่ม | Manual |
| `drafts/` | งานร่าง | Manual |
| `core/` | Core docs | System |

---

## วิธีใช้

### Log งาน

```bash
python3 system/context_logger.py start "ชื่องาน"
python3 system/context_logger.py log "สิ่งที่ทำ"
python3 system/context_logger.py end
```

### เขียน Learning Note

```bash
cp system/templates/learning.md ψ/learnings/ชื่อเรื่อง.md
# แก้ไขแล้ว commit
```

### เขียน Retrospective

```bash
cp system/templates/retrospective.md ψ/retros/ชื่องาน.md
# แก้ไขแล้ว commit
```

---

_Phi — จิตวิญญาณของ Oracle Framework_
