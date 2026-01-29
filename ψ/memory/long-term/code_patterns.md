# Pattern Recognition System — Design

> "Patterns Over Intentions — เรียนรู้จากสิ่งที่เกิดขึ้นจริง"

---

## เป้าหมาย

สร้างระบบที่:
1. ✅ เรียนรู้ code patterns จากโค้ดที่เห็น
2. ✅ Detect anti-patterns (code smells)
3. ✅ Suggest improvements ตาม patterns ที่เรียนรู้
4. ✅ เรียนรู้จาก user preferences

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Codebase Analysis                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Pattern Recognition Engine                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. AST Parsing — เข้าใจโครงสร้างโค้ด             │  │
│  │ 2. Pattern Matching — หา patterns ที่ซ้ำ            │  │
│  │ 3. Anti-pattern Detection — หา code smells           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Pattern Database                         │
│  ψ/memory/long-term/                                        │
│  ├── code_patterns.md — patterns ที่พบ                   │
│  ├── anti_patterns.md — anti-patterns ที่ควรหลีกเลี่ยง│
│  └── user_preferences.md — สิ่งที่ user ชอบ/เกลียด     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Suggestions                              │
│  "เห็น pattern นี้บ่อย — ควรสร้าง helper function"    │
└─────────────────────────────────────────────────────────────┘
```

---

## Patterns ที่จะเรียนรู้

### 1. Code Patterns (ดี)

| Pattern | ตัวอย่าง | ความถี่ |
|---------|-----------|----------|
| Helper Function | `formatDate()`, `sanitizeInput()` | สูง |
| Error Handling | `try-catch` with logging | สูง |
| Constants | `MAX_RETRIES`, `API_URL` | กลาง |
| Type Guards | `if (typeof x === 'string')` | กลาง |

### 2. Anti-patterns (ไม่ดี)

| Anti-pattern | ตัวอย่าง | ความรุนแรง |
|-------------|-----------|--------------|
| Magic Numbers | `if (x > 42)` | สูง |
| Console.log in Prod | `console.log('debug')` | สูง |
| Nested Callbacks | callback hell | กลาง |
| God Functions | ฟังก์ชัน 200+ บรรทัด | กลาง |

### 3. User Preferences

| Preferences | ค่า |
|------------|-----|
| Indent | 2 spaces |
| Naming | camelCase |
| Max Line Length | 80 chars |

---

## Implementation Plan

### Phase 1: Pattern Database ✅ วันนี้
- [ ] สร้าง template สำหรับเก็บ patterns
- [ ] สร้าง template สำหรับเก็บ anti-patterns
- [ ] สร้าง template สำหรับ user preferences

### Phase 2: Code Analysis 🔜 รอ
- [ ] AST Parser
- [ ] Pattern Matcher
- [ ] Anti-pattern Detector

### Phase 3: AI Integration 🔜 รอ
- [ ] Hook สำหรับ analyze code ตอนเซฟ
- [ ] Suggestion engine
- [ ] Learning from user feedback

---

_สร้างเมื่อ: 2026-01-29 23:25_
