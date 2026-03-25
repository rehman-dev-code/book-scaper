import time
import requests
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "https://books.toscrape.com/"
DATA_FILE = "books.csv"
IMAGE_FOLDER = "images"

if not os.path.exists(IMAGE_FOLDER): 
  os.makedirs(IMAGE_FOLDER)

driver = webdriver.Chrome()
driver.get(BASE_URL)
count = 0

with open(DATA_FILE,"w",newline = "",encoding="utf-8") as file:
  writer = csv.writer(file)
  writer.writerow(["Title","Price","Rating","Image_Url"])
 
  while True:
     books = driver.find_elements(By.CLASS_NAME,"product_pod")
     for book in books:
        try:
          title = book.find_element(By.TAG_NAME,"h3").find_element(By.TAG_NAME,"a").get_attribute("title")
          price = book.find_element(By.CLASS_NAME,"price_color").text
          rating = book.find_element(By.CLASS_NAME,"star-rating").get_attribute("class")
          rating = rating.split()[1]
          url = book.find_element(By.TAG_NAME,"img")
          img_url = url.get_attribute("src")
          count +=1
       
          img_data = requests.get(img_url).content
          img_name = f"book_{count}.jpg" 
          img_path = os.path.join(IMAGE_FOLDER,img_name)     
          with open(img_path,"wb") as f:
            f.write(img_data)
    
          writer.writerow([title,price,rating,img_url])
        except Exception as e:
          print("Error:",e)

     try:
        nxt_btn = driver.find_element(By.CLASS_NAME,"next")
        nxt_btn.click()
        time.sleep(2)
     except:
        print("No more pages ")
        break
driver.quit()
 
print("\n Project completed Successfully!")
print(f"Images saved in:{IMAGE_FOLDER}")
print(f"Data saved in:{DATA_FILE}")
