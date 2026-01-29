# First Bug is a Feature

> "Core Truth — ถามร้อยครั้ง ตอบเหมือนเดิม"

---

## Statement

**"First bug is a feature"** — บั๊กแรกคือ feature ไม่ใช่ปัญหา

---

## Why This Matters

- เมื่อเจอ bug แรก → อย่าแก้ ให้มองว่ามันเป็น feature
- มันบอกว่า requirement ผิด หรือเราเข้าใจผิด
- แก้ตรง source (requirement/understanding) ไม่ใช่แก้ symptom

---

## Examples

### Situation 1: User บอกว่าทำงานผิด
- Decision: อย่าแก้ code ทันที
- Reason: อาจเป็น feature ที่ยังไม่ได้เขียน spec

### Situation 2: Test ล้มเหลว
- Decision: ดูว่า test ถูกไหม ไม่ใช่แก้ code
- Reason: "First bug is a feature" — อาจ test ผิด

### Situation 3: Requirement ไม่ชัดเจน
- Decision: ถาม user ก่อน ไม่ใช่ guess
- Reason: Bug แรก = requirement ไม่ชัดเจน

---

## Core Principle

```
Bug แรกไม่ใช่ปัญหา — มันคือ feature ที่ยังไม่ได้ถูก define
```

ถ้าเจอ bug → ถามตัวเอง:
1. นี่คือ feature หรือ bug?
2. requirement ถูกต้องไหม?
3. ฉันเข้าใจถูกต้องไหม?

---

_Created: 2026-01-29_
_Creator: คลอด (Cloud Anderson)_
