# Claude Code Hooks

Hooks สำหรับ Oracle Framework — Auto load context

---

## SessionStart Hook

**ไฟล์:** `.claude/hooks/session_start.py`

**ทำอะไร:**
- เมื่อเริ่ม session ใหม่ → โหลด `system/current-work.md` อัตโนมัติ
- ถ้ามี active session → โหลด session นั้นด้วย

---

## วิธีติดตั้ง (ใช้ /hooks command)

1. รัน `/hooks` ใน Claude Code
2. เลือก `SessionStart`
3. Add new hook:
   ```
   python3 .claude/hooks/session_start.py "$CLAUDE_PROJECT_DIR"
   ```
4. Save to `Project settings`

---

## ผลลัพธ์

ตอนเริ่ม session ใหม่ จะเห็น:

```
============================================================
📋 CURRENT WORK CONTEXT
============================================================
[content from system/current-work.md]
============================================================

============================================================
🔄 ACTIVE SESSION
============================================================
[content from active session]
============================================================
```
