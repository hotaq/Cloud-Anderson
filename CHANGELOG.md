# Changelog

บันทึกการเปลี่ยนแปลงทั้งหมดของ Oracle Framework

---

## [2.0.1] - 2026-01-29

### 🎨 Restructure Project (Clean Version)

**โครงสร้างก่อน:**
```
agent/
├── ψ/
├── claude-code/
├── codex/
├── opencode/
├── AGENTS.md
├── CURRENT_WORK.md
├── Goal.md
└── README.md
```

**โครงสร้างใหม่:**
```
oracle-framework/
├── ψ/                    ← Shared Soul (root level)
├── agents/               ← All AI agents
│   ├── claude/           ← Renamed from claude-code
│   ├── codex/
│   └── peach/            ← Renamed from opencode
├── docs/                 ← Documentation
│   ├── agents.md
│   └── oracle-framework.md
├── system/               ← System files
│   ├── current-work.md
│   └── status.md         ← New
├── goals/                ← Goals
│   └── main.md
└── README.md             ← New main README
```

### เปลี่ยนแปลงหลัก:

| หมวด | เดิม | ใหม่ | เหตุผล |
|------|------|------|---------|
| **Agent folders** | กระจาย root | `agents/` | รวมไว้ที่เดียว |
| **ชื่อ AI** | claude-code, opencode | claude, peach | สั้นกระชับ |
| **เอกสาร** | root | `docs/` | แยกเอกสารชัดเจน |
| **ระบบ** | root | `system/` | แยกระบบ |
| **เป้าหมาย** | Goal.md | `goals/main.md` | โฟลเดอร์เป้าหมาย |

### Symlinks อัปเดต:

```bash
# เดิม
claude-code/ψ → ../ψ
codex/ψ → ../ψ
opencode/ψ → ../ψ

# ใหม่
agents/claude/ψ → ../../ψ
agents/codex/ψ → ../../ψ
agents/peach/ψ → ../../ψ
```

### ไฟล์ใหม่:

- ✅ `README.md` — ไฟล์หลัก (short)
- ✅ `system/status.md` — สถานะระบบ
- ✅ `CHANGELOG.md` — ไฟล์นี้

### Git:

- Reinit git repository
- First commit: `🎨 Restructure project to clean version`

---

_อัปเดตล่าสุด: 2026-01-29 โดย คลอด (Claude)_
