# Context Logging System

ระบบบันทึก context สำหรับ Oracle Framework — ทำให้ AI ทั้ง 3 สื่อสารและเรียนรู้ร่วมกันได้จริง

---

## Overview

ระบบ Context Logging สร้าง "ความทรงจำ" ให้กับ Oracle Framework โดย:

- ✅ บันทึกสิ่งที่แต่ละ AI ทำ
- ✅ เชื่อมกับ Git workflow
- ✅ ส่งมอบงานระหว่าง AI ได้
- ✅ เก็บประวัติไว้ใน `ψ/memory/logs`

---

## Components

### 1. Context Logger (`system/context_logger.py`)

ตัวบันทึก context หลัก

```bash
# เริ่ม session
python3 system/context_logger.py start "ชื่องาน"

# บันทึก log
python3 system/context_logger.py log "สิ่งที่ทำ"
python3 system/context_logger.py log "เพิ่ม authentication" --tag progress

# จบ session
python3 system/context_logger.py end

# ดูสถานะ
python3 system/context_logger.py status
```

**Flow:**
1. เริ่ม session → สร้างไฟล์ใน `ψ/active/context/session-TIMESTAMP.md`
2. Log entry → เพิ่ม log พร้อม timestamp
3. End session → ย้ายไป `ψ/memory/logs/YYYY-MM-DD.md`

---

### 2. Git Commit Wrapper (`system/git_commit.py`)

Commit พร้อม log context อัตโนมัติ

```bash
# Commit ปกติ
python3 system/git_commit.py "✅ เสร็จแล้ว — สร้างระบบ login"

# Commit พร้อม mention AI อื่น
python3 system/git_commit.py "✅ สร้างระบบ login เสร็จแล้ว" --mention "@พีช ช่วยเขียน docs หน่อย"
```

**Flow:**
1. จบ session ปัจจุบัน (ถ้ามี)
2. Update `system/current-work.md`
3. Git add + commit

---

### 3. Handoff System (`system/handoff.py`)

ส่งมอบงานระหว่าง AI

```bash
# ส่งมอบงาน
python3 system/handoff.py claude peach "ทำ login system เสร็จแล้ว ช่วยเขียน docs หน่อย"

# ดู handoffs ทั้งหมด
python3 system/handoff.py --list
```

**Flow:**
1. สร้าง handoff note ใน `ψ/inbox/handoff/`
2. Update `system/current-work.md`
3. Commit เพื่อบอก AI ตัวต่อไป

---

## Workflows

### Workflow 1: คลอดทำงาน → พีชรับงาน

```bash
# === คลอดทำงาน ===
python3 system/context_logger.py start "สร้างระบบ login"
python3 system/context_logger.py log "สร้าง users table"
python3 system/context_logger.py log "เพิ่ม authentication"
python3 system/git_commit.py "✅ สร้างระบบ login เสร็จแล้ว

- สร้าง users table
- เพิ่ม authentication
- รอ @พีช เขียน docs"

# === พีชมารับงาน ===
python3 system/handoff.py --list  # ดูว่ามีงานมั้ย
python3 system/context_logger.py start "เขียน docs ระบบ login"
python3 system/context_logger.py log "เขียน API docs"
python3 system/git_commit.py "📝 เขียน docs เสร็จแล้วค่ะ @คลอด

อยู่ที่ docs/api/login.md
อ่านแล้วบอกด้วยนะคะ 🙏"
```

---

### Workflow 2: เขียน Learning Note

```bash
# เริ่ม session
python3 system/context_logger.py start "เรียนรู้เรื่อง MCP"

# ทำงาน... เรียนรู้อะไรใหม่

# เขียน learning note (ใช้ template)
cp system/templates/learning.md ψ/memory/learnings/mcp-101.md
# แก้ไข template ตามที่เรียนรู้

# Commit
python3 system/git_commit.py "💡 เรียนรู้ MCP integration
เขียนไว้ที่ ψ/memory/learnings/mcp-101.md"
```

---

### Workflow 3: Retrospective

```bash
# หลังเสร็จงานใหญ่
cp system/templates/retrospective.md ψ/memory/retros/2026-01-login-system.md
# แก้ไข template ตาม retrospective

# Commit
python3 system/git_commit.py "📊 Retrospective: Login System

สิ่งที่ดี: Authentication ทำงานได้ดี
สิ่งที่ควรปรับปรุง: Test coverage น้อยไป"
```

---

## Directory Structure

```
ψ/
├── active/
│   ├── context/
│   │   └── session-TIMESTAMP.md    ← Session ปัจจุบัน
│   └── .current_session            ← Pointer ไป session ปัจจุบัน
├── memory/
│   ├── logs/
│   │   └── 2026-01-29.md           ← Log ตามวัน
│   ├── learnings/                  ← Learning notes
│   └── retros/                     ← Retrospectives
└── inbox/
    └── handoff/
        └── handoff-TIMESTAMP.md    ← Handoff notes

system/
├── context_logger.py                ← Context logger
├── git_commit.py                    ← Git wrapper
├── handoff.py                       ← Handoff system
├── current-work.md                  ← Current work status
└── templates/
    ├── log.md                       ← Log template
    ├── learning.md                  ← Learning template
    └── retrospective.md             ← Retro template
```

---

## Best Practices

### สำหรับ AI

1. **เริ่ม session ทุกครั้ง** — เมื่อเริ่มงานใหม่
2. **Log บ่อยๆ** — เมื่อทำสิ่งสำคัญ
3. **End session เมื่อเสร็จ** — เพื่อเก็บไว้ใน memory
4. **ใช้ git_commit.py** — ไม่ต้อง commit เอง
5. **Handoff ชัดเจน** — บอก context ให้ครบ

### สำหรับ Human

1. **อ่าน `system/current-work.md`** — รู้เรื่องทันที
2. **อ่าน `ψ/memory/logs/`** — ดูประวัติ
3. **อ่าน `ψ/inbox/handoff/`** — ดูว่าใครส่งอะไรให้ใคร

---

## Tips

### Quick Logging

ถ้าอยาก log เร็วๆ ไม่ต้อง start session:

```bash
python3 system/git_commit.py "✅ แก้ bug X เสร็จ" --no-log
```

### Check Status

```bash
# ดู session ปัจจุบัน
python3 system/context_logger.py status

# ดู handoffs ทั้งหมด
python3 system/handoff.py --list

# ดู log วันนี้
cat ψ/memory/logs/$(date +%Y-%m-%d).md
```

### Use Tags

```bash
python3 system/context_logger.py log "เริ่มทำ X" --tag start
python3 system/context_logger.py log "กำลังทำ Y" --tag progress
python3 system/context_logger.py log "เจอปัญหา Z" --tag issue
python3 system/context_logger.py log "แก้ปัญหา Z แล้ว" --tag fix
```

---

## Examples

### Example 1: Full Session

```bash
# เริ่ม session
python3 system/context_logger.py start "สร้าง API endpoint"

# ทำงาน
python3 system/context_logger.py log "สร้าง route /api/users" --tag feature
python3 system/context_logger.py log "เพิ่ม validation" --tag progress

# เสร็จแล้ว commit
python3 system/git_commit.py "✅ สร้าง API endpoint เสร็จแล้ว

- GET /api/users
- POST /api/users
- Validation เรียบร้อย"
```

### Example 2: Handoff

```bash
# คลอดส่งงานให้พีช
python3 system/handoff.py claude peach "สร้าง API เสร็จแล้ว ช่วยทดสอบหน่อย"

# พีชมารับงาน
python3 system/handoff.py --list  # เห็นว่าคลอดส่งมา
python3 system/context_logger.py start "ทดสอบ API"
python3 system/context_logger.py log "ทดสอบ GET /api/users"
python3 system/context_logger.py log "ทดสอบ POST /api/users"
python3 system/git_commit.py "🧪 ทดสอบ API เสร็จแล้วค่ะ @คลอด

ทุกอย่างใช้ได้ดีค่ะ"
```

---

## Next Steps

หลังใช้ MVP สักพัก ควร:

1. **เพิ่ม MCP integration** — เชื่อมกับ Claude Code
2. **Auto-detection** — detect ว่า AI ทำอะไร
3. **Smart logging** — log อัจฉริยะขึ้น
4. **UI** — สร้าง UI สำหรับดู logs

---

_Created for Oracle Framework — Version 1.0 (MVP)_
