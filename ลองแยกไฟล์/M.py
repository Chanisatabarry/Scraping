from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import firebase_admin
from firebase_admin import credentials, firestore
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/HP/Desktop/Scraping/Scraping/project-40c46-firebase-adminsdk-pz5db-7819896dc3.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode (if you don't want to see the browser window)
service = Service('C:/Users/HP/Desktop/Scraping/Scraping/chromedriver.exe')  # Update the path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_makro_price(url):
    driver.get(url)
    try:
        # รอให้ element ที่มีคลาสที่ต้องการปรากฏขึ้น
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body1.pdp.css-18kjcak'))
        )
        return price_element.text.strip()
    except Exception as e:
        print(f"Error fetching price: {e}")
        return "ไม่พบราคา"

    
# รันการ scraping Makro
stores_ref = db.collection('Makro')
docs = stores_ref.stream()

for doc in docs:
    data = doc.to_dict()
    url = data.get('Url')
    name = data.get('Name')

    # Scraping ราคาสินค้าจาก URL
    if url:
        price = scrape_makro_price(url)
        print(f"สินค้า: {name}, ราคา: {price}")
    else:
        print(f"ไม่มี URL สำหรับสินค้า {name}")

# Close the WebDriver
driver.quit()