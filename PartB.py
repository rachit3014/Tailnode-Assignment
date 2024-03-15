import requests
import os
from bs4 import BeautifulSoup

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



from dotenv import load_dotenv
load_dotenv()
#uri connects you to  mongodb atlas
uri = os.environ['MONGODBURI']
client = MongoClient(uri, server_api=ServerApi('1'))
                          
#  successful connection
try:
    client.admin.command('ping')
    print("successfully connected to MongoDB!")
except Exception as e:
    print(e)

#creating a new database if does not already exists
mydb = client["Tailnodedatabase"]
#creating collections 
collection = mydb["test_collection"]


pagenumber=1
arr=[]
while (True):
    
    
    url=f'https://books.toscrape.com/catalogue/page-{1}.html'
    response=requests.get(url)

    soup=BeautifulSoup(response.text,'html.parser')
    books=soup.find_all('article',class_='product_pod')


    for book in books:
        Name=book.h3.a['title']
        Price=book.find('p',class_='price_color').text[1:]
        Availability = book.find('p', class_='instock availability').text.strip()
        Rating = book.find('p', class_='star-rating').get('class')[1]
        mybooks={
            "Name":Name,
            "Price":Price,
            "Rating":Rating,
            "Availability":Availability
        }
        arr.append(mybooks)
    next_button = soup.find("li", class_="next")
    if next_button:
        print(f"completed scraping of pageNo. {pagenumber}")
        pagenumber += 1
            
    else:
        print("completed scraping of pageNo. 50")
        print("All data of the Books added into the database")
        break  # No more pages to scrape, exit the loop

collection.insert_many(arr)