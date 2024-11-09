from bs4 import BeautifulSoup
import requests
import time
import firebase_admin
from firebase_admin import credentials, firestore

# คำสั่งสร้างเชื่อมต่อ Firebase Admin SDK
cred = credentials.Certificate("C:/Users/HP/Desktop/Scraping/Scraping/project-40c46-firebase-adminsdk-pz5db-7819896dc3.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

collection_ref = db.collection("TestRaw")
documents = collection_ref.stream()

# Function เรียกใช้ ซ้ำ
def loaddata(url,id):
    # ดึงข้อมูล
    # url = "https://www.bigc.co.th/product/chicken-breast-chopped-per-kg.36455"
    res = requests.get(url)
    res.encoding = "utf-8"

    if res.status_code == 200:
        print("")
        # print("Successful")
        # print("-------------------------------------------------------------------------------------------")
    elif res.status_code == 404:
        print("Error 404 page not found")
        return
    else:
        print("Not both 200 and 404")
        return

    # สกัดข้อมูล
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)

    # ทำให้ข้อมูลเป็นระเบียบ ดูง่าย ด้วยคำสั่ง prettify()
    #print(soup.prettify())
    
    # ค้นหา
    courses = soup.find('h1').string
    price = soup.find('div', class_='productDetail_product_price__AQTOf').text

    # ค้นหาตำแหน่งของตัวอักษรหมายเลขแรกและสุดท้าย
    start = price.find("฿")
    end = price.find(".")
    # ตัดสตริงจากตำแหน่งแรกถึงก่อนตำแหน่งสุดท้าย
    cost = price[start+1:end]

    data = {
        "cost": int(cost),
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    collection_ref.document(id).update(data)


    print(f"Document ID: {id}, cost: {cost} ")

    # return courses, price

# เรียกใช้ ฟังก์ชั่น
# Test = loaddata()

# print(Test[0])
# print(Test[1])
# print("------------------------------------------")

# อัปเดตข้อมูลใน Firestore Database
# db = firestore.client()

# data = {
#     "course": Test[0],
#     "price": Test[1],
#     "timestamp": firestore.SERVER_TIMESTAMP
# }

# db.collection("TestWebscraping").document("1").set(data)



for doc in documents:
    data = doc.to_dict()
    url = data.get("url")
    document_id = doc.id
    # print(f"Document ID: {document_id}, URL: {url}")
    loaddata(url,document_id)

print("Successful")
