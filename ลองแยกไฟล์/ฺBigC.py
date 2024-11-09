import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/HP/Desktop/Scraping/Scraping/project-40c46-firebase-adminsdk-pz5db-7819896dc3.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# ฟังก์ชันสำหรับ scraping ข้อมูลจาก BigC
def scrape_bigc_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find('div', class_='productDetail_product_price__AQTOf')
    if price_element:
        return price_element.text
    return "ไม่พบราคา"

# รันการ scraping BigC
stores_ref = db.collection('BigC')
docs = stores_ref.stream()

for doc in docs:
    data = doc.to_dict()
    url = data.get('Url')
    name = data.get('Name')

    # Scraping ราคาสินค้าจาก URL
    if url:
        price = scrape_bigc_price(url)
        print(f"สินค้า: {name}, ราคา: {price}")
    else:
        print(f"ไม่มี URL สำหรับสินค้า {name}")
