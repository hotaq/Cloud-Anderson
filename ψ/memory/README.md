# 🧠 Memory System — ระบบความจำของคลอด

> "AI ที่มี Memory — จำได้นาน จำได้ลึก"

---

## ⚠️ Hybrid Model

ระบบ Memory ใช้ **Hybrid Model** — ผสมผสานระหว่างที่ใช้อยู่กับ Oracle Framework

📖 **ดูโครงสร้างแบบละเอียด:** [`STRUCTURE.md`](./STRUCTURE.md)

---

## Quick Overview

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

---

## Automation

ระบบ Memory ทำงานอัตโนมัติผ่าน **Memory Update Hook**:

```python
# เมื่อ Session จบ → Auto update memory
SessionEnd Hook → memory_update.py
                     ↓
            อ่าน session log
                     ↓
            ดึง wins & lessons
                     ↓
            บันทึกลง episodic memory
```

---

## วิธีใช้งาน

### Working Memory (ระหว่างทำงาน)

```markdown
## กำลังทำอะไร
- กำลังแก้ bug ตรงนี้
- ยังไม่เสร็จ เดี๋ยวมาต่อ
```

### Long-term Memory (สิ่งที่เรียนรู้)

```markdown
## User Patterns
| วันที่ | Pattern | ความถี่ |
|---------|---------|----------|
| 2026-01-29 | ชอบตอบสั้น | สูง |
```

### Episodic Memory (เรื่องราว)

```markdown
## Wins — Hook System
**Problem:** อยากให้ AI จำเอง
**Solution:** PostToolUse hook
**Result:** 🎉 ใช้ได้แล้ว!
```

---

## Memory Flow

```
Session เริ่ม → Load Working Memory
       ↓
ทำงาน... → จดใน Working Memory
       ↓
เจอสิ่งใหม่ → เรียนรู้ Pattern
       ↓
Session จบ → Consolidate to Long-term
       ↓
ครั้งหน้า → Recall from Memory
```

---

## Best Practices

1. **Working Memory** — เขียนแบบร่างๆ ไม่ต้องเป็นทางการ
2. **Long-term** — เขียนแบบ structured มี template
3. **Episodic** — เล่าเป็นเรื่องๆ มีปัญหา → วิธีแก้ → ผลลัพธ์

---

_อัปเดตล่าสุด: 2026-01-29 23:15 น._
