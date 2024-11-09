from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def lotus(url):
    # ตั้งค่าตัวเลือกของ ChromeDriver
    options = Options()
    options.add_argument("--headless")  # เปิดโหมด headless (ไม่แสดงหน้าต่างเบราว์เซอร์)
    service = Service(ChromeDriverManager().install())

    # เริ่มต้น WebDriver ของ Chrome
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # เปิด URL ในเบราว์เซอร์
        driver.get(url)
        
        # รอให้หน้าเว็บโหลดสมบูรณ์
        time.sleep(20)  # รอเว็บโหลดสมบูรณ์เป็นเวลา 5 วินาที (สามารถปรับเป็นเวลาที่เหมาะสมได้)
        
        # ใช้ JavaScript Executor เพื่อดึงข้อมูล
        price_text = driver.execute_script("""
            let spanElement = document.evaluate("//span[contains(text(), 'Each')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (spanElement && spanElement.previousSibling) {
                return spanElement.previousSibling.textContent.trim();
            }
            return null;
        """)
        
        if price_text:
            return f"Price: {price_text}"
        else:
            return "ไม่พบข้อมูลราคา"
        
    finally:
        # ปิด WebDriver
        driver.quit()
def tops(url):
    # ตั้งค่าตัวเลือกของ ChromeDriver
    options = Options()
    options.add_argument("--headless")  # เปิดโหมดหัวใจเร็ว (Headless mode)
    service = Service(ChromeDriverManager().install())

    # เริ่มต้น WebDriver ของ Chrome
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # เปิด URL ในเบราว์เซอร์
        driver.get(url)
        
        # รอให้หน้าเว็บโหลดสมบูรณ์ (ใช้เมท็อด implicitly_wait หรือใช้ WebDriverWait ก็ได้)
        time.sleep(20)  # รอเว็บโหลดสมบูรณ์เป็นเวลา 5 วินาที (สามารถปรับเป็นเวลาที่เหมาะสมได้)
        
        # ค้นหาข้อมูลราคา
        price_element = driver.find_element(By.CSS_SELECTOR, 'span.product-Details-current-price')
        
        if price_element:
            price_text = price_element.text.strip()
            return f"Price: {price_text}"
        else:
            return "ไม่พบข้อมูลราคา"
        
    finally:
        # ปิด WebDriver
        driver.quit()
# ตัวอย่างการเรียกใช้ฟังก์ชัน
url1 = "https://www.lotuss.com/th/product/168006317"
url2 = "https://www.tops.co.th/th/attack-clean-advance-concentrated-liquid-600ml-pack-2-8851818101159"
print(lotus(url1))
print(tops(url2))