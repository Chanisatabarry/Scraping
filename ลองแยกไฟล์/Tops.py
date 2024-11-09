from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import firebase_admin
from firebase_admin import credentials, firestore
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/HP/Desktop/Scraping/Scraping/project-40c46-firebase-adminsdk-pz5db-7819896dc3.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode (if you don't want to see the browser window)
service = Service('C:/Users/HP/Desktop/Scraping/Scraping/chromedriver.exe')  # Update the path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# ฟังก์ชันสำหรับ scraping ข้อมูลจาก Tops
def scrape_tops_price(url):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load completely
    try:
        price_element = driver.find_element(By.CLASS_NAME, 'product-Details-price-block')
        return price_element.text.strip()  # ใช้ strip() เพื่อลบช่องว่าง
    except Exception as e:
        print(f"Error fetching price: {e}")
        return "ไม่พบราคา"

# รันการ scraping Tops
stores_ref = db.collection('Tops')
docs = stores_ref.stream()

for doc in docs:
    data = doc.to_dict()
    url = data.get('Url')
    name = data.get('Name')

    # Scraping ราคาสินค้าจาก URL
    if url:
        price = scrape_tops_price(url)
        print(f"สินค้า: {name}, ราคา: {price}")
    else:
        print(f"ไม่มี URL สำหรับสินค้า {name}")

# Close the WebDriver
driver.quit()
