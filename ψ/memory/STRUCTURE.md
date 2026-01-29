# Memory Structure — Hybrid Model

> "ผสมผสานระหว่างที่ใช้อยู่กับ Oracle Framework"

---

## โครงสร้างทั้งหมด

```
ψ/memory/
├── short-term/       — RAM (ขณะทำงาน)
├── long-term/        — Patterns ทั่วไป
├── episodic/         — Wins/Lessons รายครั้ง
├── logs/             — Daily logs (raw)
├── resonance/        — Soul, Identity (Oracle)
├── learnings/        — Deep learnings (Oracle)
└── retrospectives/   — Session reviews (Oracle)
```

---

## หน้าที่แต่ละส่วน

| โฟลเดอร์ | หน้าที่ | ตัวอย่าง | อัปเดตเมื่อ |
|----------|-----------|-----------|-------------|
| `short-term/` | RAM ขณะทำงาน | context.md | ทำงานทุกวัน |
| `long-term/` | Patterns ทั่วไป | user preferences, code patterns | เจอ pattern ซ้ำ |
| `episodic/` | เหตุการณ์รายครั้ง | wins, lessons | เสร็จ session |
| `logs/` | Daily logs (raw) | YYYY-MM-DD.md | ทุกวัน (auto) |
| `resonance/` | Core truths | oracle.md, identity.md | เจอหลักการสำคัญ |
| `learnings/` | Deep learnings | YYYY-MM-DD_[topic].md | สังเคราะห์เสร็จ |
| `retrospectives/` | Session reviews | YYYY-MM-DD_[session].md | จบ session สำคัญ |

---

## Workflow

```
ทำงาน → short-term/
    ↓
เสร็จ → episodic/ (wins, lessons)
    ↓
สังเคราะห์ → learnings/
    ↓
เป็นหลักการ → resonance/
```

## ความแตกต่าง

| | `episodic/` | `retrospectives/` |
|---|-------------|-------------------|
| คือ | รวบรวม | วิเคราะห์ลึก |
| เมื่อ | เสร็จทีละอย่าง | จบ session ใหญ่ |
| รูปแบบ | wins, lessons | retrospective เต็ม |

| | `long-term/` | `learnings/` |
|---|-------------|---------------|
| คือ | Patterns ทั่วไป | Deep learnings |
| ระดับ | surface | deep |
| ตัวอย่าง | user preferences | "Patterns Over Intentions" |

---

_อัปเดตล่าสุด: 2026-01-29_
