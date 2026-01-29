# Anti-Patterns Library — สิ่งที่ควรหลีกเลี่ยง

> "สิ่งที่ทำแล้วเจ็บหัว — อย่าทำซ้ำ"

---

## Last Updated: 2026-01-29

---

## Magic Numbers

### Anti-Pattern: Hardcoded Values

**ตัวอย่าง:**
```python
# ❌ แย่
if x > 42:
    do_something()

# ✅ ดี
MAX_ITEMS = 42
if x > MAX_ITEMS:
    do_something()
```

**ปัญหา:** อ่านไม่รู้เรื่อง แก้ไขยาก

**ความรุนแรง:** 🔴 สูง

**จะแก้ไข:** Extract to constant

---

## Console Logging in Production

### Anti-Pattern: Debug Logs ติด production

**ตัวอย่าง:**
```python
# ❌ แย่
console.log("User data:", user)

# ✅ ดี
logger.debug("User data:", user)
```

**ปัญหา:** เปิดโป๊ะ sensitive data

**ความรุนแรง:** 🔴 สูง

**จะแก้ไข:** ใช้ proper logger

---

## Nested Callbacks

### Anti-Pattern: Callback Hell

**ตัวอย่าง:**
```javascript
// ❌ แย่
getData(function(data) {
  getMoreData(data, function(more) {
    getEvenMore(more, function(even) {
      // ลึกเกินไป
    });
  });
});

// ✅ ดี
const data = await getData();
const more = await getMoreData(data);
```

**ปัญหา:** อ่านยาก ดูแลรักษาลำบาก

**ความรุนแรง:** 🟡 กลาง

**จะแก้ไข:** ใช้ async/await หรือ Promise chain

---

## God Functions

### Anti-Pattern: ฟังก์ชันทำทุกอย่าง

**ตัวอย่าง:**
```python
# ❌ แย่ — 200+ บรรทัด ทำทุกอย่าง
def process_user(user):
    # connect db
    # validate
    # save to file
    # send email
    # update cache
    # ... อีก 100 บรรทัด

# ✅ ดี — แยกเป็นฟังก์ชันเล็กๆ
def process_user(user):
    validate_user(user)
    save_user(user)
    notify_user(user)
```

**ปัญหา:** ทดสอบยาก ดูแลรักษาลำบาก

**ความรุนแรง:** 🟡 กลาง

**จะแก้ไข:** Single Responsibility Principle

---

## Template สำหรับบันทึก Anti-Pattern ใหม่

```markdown
### Anti-Pattern: [ชื่อ]

**ตัวอย่าง:**
\`\`\`[language]
# ❌ แย่
[โค้ดที่ผิด]

# ✅ ดี
[โค้ดที่ถูก]
\`\`\`

**ปัญหา:** [อะไรที่ผิด]

**ความรุนแรง:** [🔴 สูง / 🟡 กลาง / 🟢 ต่ำ]

**จะแก้ไข:** [วิธีแก้]
```

---

_อัปเดตล่าสุด: 2026-01-29 23:30_

## Scan Results — 2026-01-29 23:40

### 🟡 Magic Number: Number 2

**ความถี่:** 4 ครั้ง

**ควรแก้:** กำหนดเป็น constant เช่น DEFAULT_TIMEOUT = 2

---

### 🟡 Magic Number: Number 3

**ความถี่:** 4 ครั้ง

**ควรแก้:** กำหนดเป็น constant เช่น DEFAULT_TIMEOUT = 3

---

### 🟡 Magic Number: Number 5

**ความถี่:** 3 ครั้ง

**ควรแก้:** กำหนดเป็น constant เช่น DEFAULT_TIMEOUT = 5

---

### 🟡 Magic Number: Number 10

**ความถี่:** 3 ครั้ง

**ควรแก้:** กำหนดเป็น constant เช่น DEFAULT_TIMEOUT = 10

---

### 🟢 Magic Number: Number 20

**ความถี่:** 2 ครั้ง

**ควรแก้:** กำหนดเป็น constant เช่น DEFAULT_TIMEOUT = 20

---

### 🟡 Code Smell: Long Functions (> 20 lines)

**จำนวน:** 1 functions

**ตัวอย่าง:**
- main (26 lines)

---

