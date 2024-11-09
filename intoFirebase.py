import openpyxl
import firebase_admin
from firebase_admin import credentials, firestore

# เชื่อมต่อกับ Firebase
cred = credentials.Certificate('project-40c46-firebase-adminsdk-pz5db-7819896dc3.json')
firebase_admin.initialize_app(cred)

# เชื่อมต่อกับ Firestore
db = firestore.client()

# อ่านข้อมูลจาก Excel
workbook = openpyxl.load_workbook('lotus.xlsx', data_only=True)
sheet = workbook['Sheet1']  # ชื่อแผ่นงานในไฟล์ Excel

data = []
docID = 0

# ดึงข้อมูลจากแผ่นงาน โดยไม่ข้ามแถวสุดท้าย
for row in sheet.iter_rows(values_only=True):
    # ตรวจสอบว่าชื่อคอลัมน์แรกของแถวปัจจุบันไม่ใช่ None (ข้ามแถวว่าง)
    if (row[1] == "Name"):
        continue

    # เก็บข้อมูลใน data array
    data.append({
        'Name': row[1],
        'Pack': row[2],
        'Price': row[3],
        'Quantity': row[4],
        'Unitpack': row[5],
        'Url': row[6],
        'Brand': row[7]
    })

# เพิ่มข้อมูลลงใน Firestore
for item in data:
    docID += 1
    db.collection('Lotus').document(str(docID)).set(item, merge=True)
    print(f"Added/updated document with ID: {docID}")
