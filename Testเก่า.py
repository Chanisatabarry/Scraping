import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:/Users/HP/Desktop/Scraping/Scraping/project-40c46-firebase-adminsdk-pz5db-7819896dc3.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# ฟังก์ชันสำหรับ scraping ข้อมูลจาก URL
def scrape_price_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    price = None
    if 'bigc' in url:
        price_element = soup.find('div', class_='productDetail_product_price__AQTOf')
        if price_element:
            price = price_element.text
        else:
            price = "ไม่พบราคา"
    
    elif 'tops' in url:
        price_element = soup.find('div', class_='MuiBox-root css-1gpfpki')
        if price_element:
            price = price_element.text
        else:
            price = "ไม่พบราคา"
    
    elif 'makro' in url:
        price_element = soup.find('div', class_='MuiBox-root')
        if price_element:
            price = price_element.text
        else:
            price = "ไม่พบราคา"
    
    elif 'lotuss' in url:
        price_element = soup.find('span', class_='jss1946')
        if price_element:
            price = price_element.text
        else:
            price = "ไม่พบราคา"
    
    return price
# ฟังก์ชันหลักในการดึงข้อมูลจาก Firestore
def main():
    # ดึงข้อมูลจาก Firestore Collection ที่ชื่อ BigC
    stores_ref = db.collection('BigC')
    docs = stores_ref.stream()

    for doc in docs:
        data = doc.to_dict()
        url = data.get('Url')
        name = data.get('Name')

        # Scraping ราคาสินค้าจาก URL
        if url:
            price = scrape_price_from_url(url)
            print(f"สินค้า: {name}, ราคา: {price}")
        else:
            print(f"ไม่มี URL สำหรับสินค้า {name}")

if __name__ == "__main__":
    main()

# # ฟังก์ชันหลักในการดึงข้อมูลจาก Firestore
# def main():
#     collections = ['BigC','Tops']  # ชื่อ Collection ของห้างแต่ละห้าง

#     for collection in collections:
#         print(f"Scraping ราคาสินค้าจากห้าง {collection}")
        
#         # ดึงข้อมูลจาก Firestore Collection
#         stores_ref = db.collection(collection)
#         docs = stores_ref.stream()

#         for doc in docs:
#             data = doc.to_dict()
#             url = data.get('Url')
#             name = data.get('Name')

#             # Scraping ราคาสินค้าจาก URL
#             if url:
#                 price = scrape_price_from_url(url)
#                 print(f"สินค้า: {name}, ราคา: {price}")
#             else:
#                 print(f"ไม่มี URL สำหรับสินค้า {name}")

# if __name__ == "__main__":
#     main()
