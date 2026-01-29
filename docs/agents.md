# AI Agents — ทีมงานของเรา

> "One Soul, Multiple Bodies"
> วิญญาณเดียว (ψ/) แต่ร่างต่างกัน

---

## Agent Map

```
                    ψ/ (Shared Soul)
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
      Claude            Codex            Peach
      (คลอด)          (มักซ์)           (พีช)
        │                 │                 │
   Engineering        Bulk Ops          Writing
```

**อ่าน Persona แต่ละตัว:**
- [คลอด (Claude)](../agents/claude/persona.md) — จริงจัง, ละเอียด, รักความสมบูรณ์
- [มักซ์ (Codex)](../agents/codex/persona.md) — เร็ว, แรง, เถอะแน่
- [พีช (Peach)](../agents/peach/persona.md) — สุภาพ, อบอุ่น, ชอบสอน

---

## Quick Reference

| AI | หน้าที่หลัก | เมื่อไหร่ใช้ | ไฟล์ |
|----|-------------|----------------|------|
| **Claude** | Software Engineering | เขียนโค้ด, ดีบัก, Git | `agents/claude/README.md` |
| **Codex** | Bulk Processing | ดึงข้อมูลเยอะ ๆ, ค้นหา | `agents/codex/README.md` |
| **Peach** | Writing & Synthesis | เขียนบล็อก, สรุป, วิเคราะห์ | `agents/peach/README.md` |

---

## Status AI

| AI | สถานะ | งานล่าสุด |
|----|-------|----------|
| **Claude** | 🟢 ออนไลน์ | Restructure Project |
| **Codex** | 🟡 สแตนด์บาย | รอคำสั่ง Bulk |
| **Peach** | 🟢 ออนไลน์ | เขียน Oracle Principles |

---

## การทำงานร่วมกัน (Multi-Agent Pattern)

```
1. Codex (20 ตัว) → ดึงข้อมูล parallel
        ↓
2. Claude → วิเคราะห์โค้ด
        ↓
3. Peach → เขียนสรุป/บล็อก
        ↓
4. oracle_learn → เก็บเป็นความรู้ถาวร
```

---

## Symlink Structure

แต่ละ AI เชื่อมต่อกับ ψ/ เดียวกัน:

```bash
agents/claude/ψ → ../../ψ
agents/codex/ψ → ../../ψ
agents/peach/ψ → ../../ψ
```

---

_อัปเดตล่าสุด: 2026-01-29_
