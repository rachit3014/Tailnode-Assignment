#importing for data scraping
import requests
import os

from dotenv import load_dotenv
#importing for mongo db
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

#uri connects you to  mongodb atlas
uri = os.environ['MONGODBURI']



# Set API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
                          
# successful connection
try:
    client.admin.command('ping')
    print("successfully connected to MongoDB!")
except Exception as e:
    print(e)


#creating a new database if does not already exists
mydb = client["Tailnodedatabase"]

#creating collections 
collection = mydb["userdeatil"]
userpost = mydb["userpostdata"]




# fetch all the user 
def fetchData():
    url=f'https://dummyapi.io/data/v1/user'
    headers={'app-id': "65f1b82c18b46085b5e5ee45"}
    response=requests.get(url,headers=headers)
    userdata=response.json().get('data')
    print(userdata)
    return userdata
#  inserting the user post data in database
def postdata(userid):
    url='https://dummyapi.io/data/v1/user/{}/post'
    headers={'app-id': "65f1b82c18b46085b5e5ee45"}
    response=requests.get(url.format(userid),headers=headers)
    data=response.json().get('data')
    userpost.insert_many(data)

# insert user data in database
def insertData():
    list=fetchData()
    collection.insert_many(list)

# finding the user id from databases
def uplaodpost():
    for j in collection.find({}):
        postdata(j['id'])
    

# Min Program Starts
while True:
    print('''
    Enter you choice:-
    -> Press 1 to Insert users
    -> Press 2 to Upload Posts
    ''')
    option=int(input("What would you like to do?  "))

    if(option==1):
        insertData()
    elif(option==2):
        uplaodpost()