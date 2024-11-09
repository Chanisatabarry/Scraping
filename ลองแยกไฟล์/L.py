from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/HP/Desktop/Scraping/Scraping/project-40c46-firebase-adminsdk-pz5db-7819896dc3.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# ฟังก์ชันสำหรับ scraping ข้อมูลจาก Lotus
def lotus(url):
    # ตั้งค่าตัวเลือกของ ChromeDriver
    options = Options()
    options.add_argument("--headless")  # เปิดโหมด headless (ไม่แสดงหน้าต่างเบราว์เซอร์)
    service = Service(ChromeDriverManager().install())

    # เริ่มต้น WebDriver ของ Chrome
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url) # เปิด URL ในเบราว์เซอร์
        # รอให้หน้าเว็บโหลดสมบูรณ์
        time.sleep(5)  # รอเว็บโหลดสมบูรณ์เวลา5วิ

        # ใช้ JavaScript Executor เพื่อดึงข้อมูลราคา
        price_text = driver.execute_script(""" 
            let spanElement = document.evaluate("//span[contains(text(), 'Each')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (spanElement && spanElement.previousSibling) {
                return spanElement.previousSibling.textContent.trim();
            }
            return null;
        """)
        
        if price_text:
            return f"ราคา: {price_text}"
        else:
            return "ไม่พบข้อมูลราคา"
        
    finally:
        # ปิด WebDriver
        driver.quit()

# รันการ scraping
stores_ref = db.collection('Lotus')
docs = stores_ref.stream()

for doc in docs:
    data = doc.to_dict()
    url = data.get('Url')
    name = data.get('Name')

    # Scraping ราคาสินค้าจาก URL
    if url:
        price = lotus(url)  # เรียกใช้ฟังก์ชัน lotus เพื่อดึงราคา
        print(f"สินค้า: {name}, {price}")
    else:
        print(f"ไม่มี URL สำหรับสินค้า {name}")
