# 🎰 Lotto 888

ระบบจัดการโพยหวยพรีเมียม สำหรับผู้ขายและผู้ซื้อ — ใช้งานบนเบราว์เซอร์มือถือ

## ✨ ฟีเจอร์

- 📝 จดโพย — 6 หวย (รัฐบาล/หุ้น/ลาว/ฮานอย/มาเลย์/ยี่กี)
- 📊 วิเคราะห์ความเสี่ยง — best/worst case
- 🟠 อั้นจ่ายครึ่ง — กำหนดเลขจ่ายครึ่งราคา
- ➡️ ส่งต่อเจ้ามือใหญ่ — ตั้งเพดานรับ ส่วนเกินส่งต่อ
- ✂️ ตัด/ลดยอด — จัดการเลขเสี่ยง พร้อมบันทึก
- 🎲 ลองสมมุติ — คำนวณกำไรขาดทุนจากเลขสมมุติ
- 📤 แชร์ LINE — ส่งสรุปโพย/เลขตัด/เลขส่งต่อ
- 🔐 ล็อกด้วย PIN — auto-lock ตาม idle time
- 💾 สำรองอัตโนมัติ — 7 จุดล่าสุด + export ไฟล์
- 📱 PWA — ติดตั้งบนหน้าจอหลักได้

## 🚀 Deploy ขึ้น GitHub Pages (ฟรีและถาวร)

### วิธีที่ 1: ผ่านเว็บ GitHub (ง่ายสุด ไม่ต้องใช้คอมมานด์)

1. **สร้าง account GitHub** ที่ github.com (ถ้ายังไม่มี — ฟรี)

2. **สร้าง repository ใหม่**
   - คลิกปุ่ม **+** มุมขวาบน → **New repository**
   - ชื่อ: `lotto888` (หรืออะไรก็ได้)
   - เลือก **Public** (จำเป็นถ้าใช้ free plan)
   - คลิก **Create repository**

3. **อัพโหลดไฟล์ทั้งหมด**
   - หน้า repo ใหม่ → คลิก **uploading an existing file**
   - ลาก **ทุกไฟล์ในโฟลเดอร์ lotto888** ลงไป (index.html, manifest.json, sw.js, icons, README.md)
   - **อย่ายกโฟลเดอร์ทั้งโฟลเดอร์เข้าไป** — ต้องลากเฉพาะไฟล์
   - กด **Commit changes**

4. **เปิด GitHub Pages**
   - ไปที่แท็บ **Settings** (เมนูบนสุดของ repo)
   - เมนูซ้าย → **Pages**
   - Source: เลือก **Deploy from a branch**
   - Branch: เลือก **main** + **/ (root)** → กด **Save**
   - รอ 1-2 นาที

5. **เปิดใช้งานได้แล้ว!**
   - URL จะเป็น `https://USERNAME.github.io/lotto888/`
   - แสดงในหน้า Settings → Pages
   - แชร์ลิงก์นี้ให้คนอื่นใช้ได้เลย

### วิธีที่ 2: ผ่าน Git command-line (สำหรับคนรู้ git)

```bash
git clone https://github.com/USERNAME/lotto888.git
cd lotto888
# คัดลอกไฟล์ทั้งหมดมาที่นี่
git add .
git commit -m "Initial Lotto 888 deployment"
git push origin main
```

## 📲 ติดตั้งบนมือถือ (PWA)

หลังเข้า URL บนมือถือ:

**iPhone (Safari):**
1. กดปุ่ม **แชร์** (สี่เหลี่ยมมีลูกศรขึ้น)
2. เลือก **Add to Home Screen**

**Android (Chrome):**
1. กดเมนู 3 จุด มุมขวาบน
2. เลือก **Install app** หรือ **เพิ่มไปยังหน้าจอหลัก**

## 🔄 อัพเดทแอปในอนาคต

1. แก้ไฟล์บน GitHub โดยตรง (หรือ push commit ใหม่)
2. GitHub Pages จะ update ภายใน 1-2 นาที
3. ผู้ใช้รีเฟรชหน้าเว็บก็ได้เวอร์ชั่นใหม่ (ข้อมูลไม่หาย)

## 💾 ข้อมูล

ข้อมูลทั้งหมด **เก็บในเครื่องของผู้ใช้** (localStorage):
- ไม่ส่งไปเซิร์ฟเวอร์
- เครื่องใครเครื่องมัน
- สำรองด้วยการ Download JSON ใน Settings

## 🆘 ปัญหาที่พบบ่อย

**Q: ติดตั้ง PWA ไม่ได้ / icon ไม่ขึ้น**
- ต้องเปิดด้วย HTTPS — GitHub Pages เป็น HTTPS อยู่แล้ว ✓
- เปิดใน Chrome/Safari ใหม่ๆ (ไม่ใช่ in-app browser ของ Facebook/LINE)

**Q: ไฟล์ไม่อัพเดท**
- ลอง Hard refresh: Ctrl+Shift+R (Desktop) หรือปิด tab/แอปแล้วเปิดใหม่
- หรือลบ cache: Settings → Site settings → Cookies and site data

**Q: แชร์ลิงก์ใน LINE แล้วเข้าไม่ได้**
- LINE บางครั้งเปิดใน in-app browser ที่ไม่รองรับ PWA
- ให้กดเมนู → "เปิดในเบราว์เซอร์"
