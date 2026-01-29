# Episodic Memory — Lessons

> "บทเรียน — สิ่งที่เรียนรู้จากความผิดพลาด"

---

## 2026-01-29 — PostToolUse Hook Deduplication

### ปัญหา
Log ซ้ำ 2 ครั้งสำหรับไฟล์เดียวกัน

### สิ่งที่ลองและล้มเหลว

| วิธี | ผล |
|-----|-----|
| Content dedup | ❌ อ่าน file พร้อมกัน |
| Lock file | ❌ Race condition |
| tool_use_id dedup | ❌ อ่าน file พร้อมกัน |
| File locking (flock) | ❌ ไม่ช่วยบน macOS |

### สิ่งที่ใช้ได้
**Cleanup after write** — เขียนแล้วค่อย clean up บรรทัดซ้ำที่ติดกัน

### บทเรียน
1. **PostToolUse hook ถูกเรียก 2 ครั้ง** — เป็น behavior ของ Claude Code
2. **File locking ยากกว่าที่คิด** — race condition เกิดง่าย
3. **Simple solution ดีกว่า** — cleanup หลังเขียนง่ายกว่าป้องกัน

---

## Template สำหรับบันทึกบทเรียน

```markdown
## [วันที่] — [หัวข้อ]

### ปัญหา
[สรุปปัญหา]

### สิ่งที่ลองและล้มเหลว

| วิธี | ผล |
|-----|-----|
| [วิธีที่ 1] | ❌ [เหตุผลที่ล้มเหลว] |
| [วิธีที่ 2] | ❌ [เหตุผลที่ล้มเหลว] |

### สิ่งที่ใช้ได้
**[วิธีที่ใช้ได้]** — [คำอธิบาย]

### บทเรียน
1. [บทเรียนที่ 1]
2. [บทเรียนที่ 2]
```

---

_อัปเดตล่าสุด: 2026-01-29 23:10 น._

## 2026-01-29 — Auto-captured from session

_See: /Users/chinnphats/Desktop/agent/ψ/active/context/session-20260129-222311.md for details_
