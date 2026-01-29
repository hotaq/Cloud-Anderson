# Claude Code Hooks — ระบบอัตโนมัติ

> "AI จำได้เอง — ไม่ต้องบอกทุกครั้ง"

---

## Overview

ระบบ Hooks คือ automation ที่ทำให้ Claude Code จดจำ context และบันทึกการทำงาน **โดยอัตโนมัติ** ไม่ต้องให้คนสั่งทุกครั้ง

เป็นการบรรลุหลักการ Oracle: **External Brain, Not Command**

---

## Hooks ที่มี

| Hook | เมื่อไร | ทำอะไร |
|------|----------|---------|
| **SessionStart** | เริ่ม session ใหม่ | โหลด `current-work.md` และ active session |
| **SessionEnd** | จบ session | บันทึก session ไป `ψ/logs/YYYY-MM-DD.md` |
| **PostToolUse** | หลังแก้/สร้างไฟล์ | Log การแก้ไฟล์ลง session |

---

## Flow การทำงาน

```
👤 พิมพ์ "startup"
       ↓
🔔 SessionStart Hook
       ↓
📋 แสดง current-work.md + active session
       ↓
💬 ทำงาน... (แก้ไฟล์ / สร้างไฟล์)
       ↓
🔔 PostToolUse Hook (ทุกครั้งที่แก้ไฟล์)
       ↓
📝 Log การแก้ไฟล์: "แก้ไข system/foo.py"
       ↓
👤 พิมพ์ "พอก่อน"
       ↓
🔔 SessionEnd Hook
       ↓
✅ บันทึก session → ψ/logs/2026-01-29.md
```

---

## ผลลัพธ์ที่ได้

### เมื่อเริ่ม session:
```
============================================================
📋 CURRENT WORK CONTEXT
============================================================
# Current Work — งานที่กำลังทำอยู่
...
============================================================
```

### เมื่อแก้ไฟล์:
```
✅ Logged: แก้ไข system/context_logger.py
```

### เมื่อจบ session:
```
✅ Session auto-saved to: ψ/logs/2026-01-29.md
```

---

## ไฟล์ที่เกี่ยวข้อง

```
.claude/
├── hooks/
│   ├── session_start.py    # Hook: SessionStart
│   ├── session_end.py      # Hook: SessionEnd
│   ├── post_tooluse.py     # Hook: PostToolUse (พร้อม deduplication)
│   └── README.md           # วิธีติดตั้ง
└── settings.local.json     # Hook configuration
```

---

## Configuration

ไฟล์ `.claude/settings.local.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session_start.py \"$CLAUDE_PROJECT_DIR\""
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "clear,logout,พอก่อน",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session_end.py \"$CLAUDE_PROJECT_DIR\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/post_tooluse.py \"$CLAUDE_PROJECT_DIR\""
          }
        ]
      }
    ]
  }
}
```

---

## Matchers

| Hook | Matcher | ความหมาย |
|------|---------|-----------|
| SessionStart | `startup` | เมื่อผู้ใช้พิมพ์ "startup" |
| SessionEnd | `clear,logout,พอก่อน` | เมื่อผู้ใช้พิมพ์คำเหล่านี้ |
| PostToolUse | `Edit\|Write` | เมื่อใช้ tool Edit หรือ Write (ใช้ `|` ไม่ใช่ `,`) |

---

## 🐛 Debugging Hooks

### วิธี Debug Hook ด้วย `jq`

เพิ่ม debug hook เพื่อดู JSON input ที่ได้รับ:

```json
"PostToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [
      {
        "type": "command",
        "command": "jq . > /path/to/project/hook-debug.json"
      }
    ]
  }
]
```

แล้วสร้างไฟล์ทดสอบ และดูผล:

```bash
cat hook-debug.json | jq .
```

### JSON Input Format ของ PostToolUse

```json
{
  "session_id": "169bd342-7469-4424-9b12-690a6930cb26",
  "transcript_path": "/Users/.../.claude/projects/.../session.jsonl",
  "cwd": "/Users/chinnphats/Desktop/agent",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/Users/chinnphats/Desktop/agent/test.txt",
    "content": "file content"
  },
  "tool_response": {
    "type": "create",
    "filePath": "/Users/chinnphats/Desktop/agent/test.txt",
    "content": "file content"
  },
  "tool_use_id": "call_7b9a302063914f549256fe26"
}
```

### ⚠️ Common Pitfall: `tool` vs `tool_name`

**สำคัญ:** Claude Code ส่ง `tool_name` ไม่ใช่ `tool`

```python
# ❌ ผิด - จะไม่ได้ค่า
tool_name = input_data.get('tool', '')

# ✅ ถูก - ใช้ `tool_name`
tool_name = input_data.get('tool_name', '')
```

นี่คือ bug ที่พบบ่อยที่ทำให้ hook ไม่ทำงาน!

---

## วิธีแก้ไข / เพิ่ม hook

### 1. แก้ไข matcher
แก้ `.claude/settings.local.json`:

```json
"matcher": "startup,เริ่ม,start"  // เพิ่มคำเหล่านี้ (ใช้ , คั่น)
```

### 2. เพิ่ม hook ใหม่
สร้างไฟล์ใหม่ที่ `.claude/hooks/my_hook.py` แล้วเพิ่มใน settings:

```json
"SessionStart": [
  {
    "matcher": "startup",
    "hooks": [
      {
        "type": "command",
        "command": "python3 .claude/hooks/session_start.py \"$CLAUDE_PROJECT_DIR\""
      },
      {
        "type": "command",
        "command": "python3 .claude/hooks/my_hook.py \"$CLAUDE_PROJECT_DIR\""
      }
    ]
  }
]
```

---

## Troubleshooting

### Hook ไม่ทำงานเลย
1. เช็ค path: ใช้ `$CLAUDE_PROJECT_DIR` ไม่ใช่ hardcode
2. เช็ค permission: `chmod +x .claude/hooks/*.py`
3. เช็ค Python: ใช้ `python3` ไม่ใช่ `python`
4. **ใช้ `jq` debug hook เพื่อดูว่าได้รับ JSON หรือไม่**

### PostToolUse ไม่ log ไฟล์
1. **เช็คว่าใช้ `tool_name` ไม่ใช่ `tool`**
2. เช็ค matcher: ต้องเป็น `PostToolUse` ไม่ใช่ `PreToolUse`
3. เช็ค tool: ต้องเป็น `Edit` หรือ `Write` ไม่ใช่ `Read`
4. เช็คว่า session file มีอยู่: `ψ/active/.current_session`

### Session ไม่ถูกบันทึก
1. เช็คว่าใช้คำ matcher ที่ถูกต้อง (เช่น "พอก่อน")
2. เช็คว่า `ψ/active/.current_session` มีอยู่จริง
3. เช็ค permission เขียนโฟลเดอร์ `ψ/logs/`

### Hook ทำงานซ้ำ (duplicate)
1. `post_tooluse.py` มีระบบ deduplication ด้วย `tool_use_id`
2. ใช้ file locking (`fcntl`) ป้องกัน race condition
3. ลบ consecutive duplicates ออกจาก session file

---

## Best Practices

### 1. ใช้ `tool_use_id` สำหรับ deduplication

```python
tool_use_id = input_data.get('tool_use_id', '')
# ตรวจสอบว่า ID นี้ถูก process แล้วหรือยัง
# ถ้าใช่, skip การ log
```

### 2. ใช้ file locking สำหรับ concurrent access

```python
import fcntl
with open(dedup_file, 'a+') as f:
    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    # ... ทำงานกับ file
```

### 3. Handle exceptions gracefully

```python
try:
    # ... hook logic
except:
    sys.exit(0)  # ไม่ crash, แค่ skip silently
```

### 4. Log เฉพาะที่จำเป็น

- `Edit` และ `Write` เท่านั้น (ไม่ใช่ `Read`, `Grep`, etc.)
- ตรวจสอบ `file_path` ว่ามีค่า
- ใช้ relative path แทน absolute path

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   PostToolUse Event                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ JSON Input (stdin):                                   │  │
│  │ - tool_name: "Write"                                  │  │
│  │ - tool_input.file_path: ".../test.txt"                │  │
│  │ - tool_use_id: "call_abc123"                          │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              post_tooluse.py Hook Script                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Parse JSON from stdin                              │  │
│  │ 2. Check tool_name in [Edit, Write]                   │  │
│  │ 3. Check tool_use_id for deduplication                │  │
│  │ 4. Find project directory (ψ or .claude)              │  │
│  │ 5. Get/create active session                          │  │
│  │ 6. Append log entry                                   │  │
│  │ 7. Clean duplicates                                   │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  ψ/active/context/session-*.md              │
│  ### 22:57:00 [auto]                                         │
│  สร้าง `test.txt`                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## เอกสารที่เกี่ยวข้อง

- `docs/CONTEXT_LOGGING.md` — ระบบ logging แบบ manual
- `system/current-work.md` — งานที่กำลังทำอยู่
- `.claude/hooks/README.md` — วิธีติดตั้ง hooks
- [Claude Code Hook Reference](https://www.claude-cn.org/claude-code-docs-zh/reference/hooks) — Official documentation

---

## Changelog

### 2026-01-29
- ✅ แก้ไข bug: `tool` → `tool_name` ใน PostToolUse hook
- ✅ เพิ่ม deduplication ด้วย `tool_use_id`
- ✅ เพิ่ม file locking ด้วย `fcntl`
- ✅ เพิ่ม duplicate cleanup
- ✅ เพิ่ม debug guide

---

_อัปเดตล่าสุด: 2026-01-29 23:00 น._
