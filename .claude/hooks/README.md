# Claude Code Hooks

Hooks สำหรับ Oracle Framework — Auto logging & context loading

---

## Overview

| Hook | ทำอะไร | ไฟล์ |
|------|---------|------|
| **SessionStart** | Auto load context เมื่อเริ่ม | `session_start.py` |
| **SessionEnd** | Auto save session เมื่อจบ | `session_end.py` |
| **PostToolUse** | Auto log การแก้ไฟล์ | `post_tooluse.py` |

---

## วิธีติดตั้ง (ใช้ /hooks command)

### 1. SessionStart — Auto load context

```
1. รัน /hooks
2. เลือก SessionStart
3. Add: python3 .claude/hooks/session_start.py "$CLAUDE_PROJECT_DIR"
4. Save → Project settings
```

### 2. SessionEnd — Auto save session

```
1. รัน /hooks
2. เลือก SessionEnd
3. Add: python3 .claude/hooks/session_end.py "$CLAUDE_PROJECT_DIR"
4. Save → Project settings
```

### 3. PostToolUse — Auto log file edits

```
1. รัน /hooks
2. เลือก PostToolUse
3. Matcher: Edit|Write
4. Add: python3 .claude/hooks/post_tooluse.py "$CLAUDE_PROJECT_DIR"
5. Save → Project settings
```

---

## Flow การทำงาน

```
เริ่ม session
    ↓
SessionStart → โหลด context อัตโนมัติ
    ↓
ทำงาน... (แก้ไฟล์)
    ↓
PostToolUse → log การแก้ไฟล์ อัตโนมัติ
    ↓
จบ session
    ↓
SessionEnd → save session ไป logs อัตโนมัติ
```

---

## ผลลัพธ์

**เมื่อเริ่ม session:**
```
============================================================
📋 CURRENT WORK CONTEXT
============================================================
[content from system/current-work.md]
============================================================
```

**เมื่อแก้ไฟล์:**
```
✅ Logged: แก้ไข system/context_logger.py
```

**เมื่อจบ session:**
```
✅ Session auto-saved to: ψ/logs/2026-01-29.md
```

---

## Note

- Hooks ใช้ stdin เพื่อรับ JSON data จาก Claude Code
- SessionEnd จะย้าย session ไป `ψ/logs/YYYY-MM-DD.md`
- PostToolUse จะสร้าง session ใหม่ auto ถ้ายังไม่มี
