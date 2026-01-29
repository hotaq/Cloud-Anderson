---
name: oracle-status
description: ดูสถานะระบบ Oracle Framework ทั้งหมด ใช้เมื่อต้องการดูภาพรวมของระบบ
---

# Oracle Status — ภาพรวมระบบ

แสดงสถานะของ Oracle Framework ทั้งหมด

## สิ่งที่ตรวจสอบ

### 1. Memory System
- ✅ Working Memory (`ψ/memory/short-term/context.md`)
- ✅ Long-term Patterns
- ✅ Episodic (wins/lessons)

### 2. Hooks
- ✅ SessionStart — Auto load context
- ✅ SessionEnd — Auto save session
- ✅ PostToolUse — Auto log file edits
- ✅ Debug Logger — Tracking

### 3. Code Analysis
- ✅ Code Analyzer Engine
- ✅ Pattern Database
- ✅ Anti-pattern Detection

### 4. Active Session
- Session ID
- เวลาเริ่ม
- Log entries

### 5. Skills
- Skills ที่มี
- Skills ที่ active

## ตรวจสอบ

อ่านไฟล์ต่อไปนี้แล้วสรุป:

1. `ψ/memory/short-term/context.md` — Working Memory
2. `ψ/active/.current_session` — Active session
3. `system/current-work.md` — Current work
4. `.claude/settings.local.json` — Hook settings
5. `.claude/skills/*/SKILL.md` — Skills

## รูปแบบผลลัพธ์

```
🔮 ORACLE FRAMEWORK STATUS
==========================

📊 Memory System:
  ✅ Working Memory — [สถานะ]
  ✅ Long-term — [จำนวน patterns]
  ✅ Episodic — [wins/lessons count]

🔗 Hooks:
  ✅ SessionStart — Active
  ✅ SessionEnd — Active
  ✅ PostToolUse — Active

🔍 Code Analysis:
  ✅ Last scan — [วันที่]
  ✅ Patterns found — [จำนวน]

📝 Active Session:
  📌 Session — [ID]
  🕐 Started — [เวลา]
  📊 Log entries — [จำนวน]

🛠️ Skills:
  - oracle-analyze
  - oracle-memory
  - oracle-patterns
  - oracle-status
  - oracle-wins
  - oracle-reflect
```
