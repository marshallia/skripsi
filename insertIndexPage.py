from pymongo import MongoClient
import json
client=MongoClient()
client=MongoClient('mongodb://adminSkripsi:adminSkripsi123@localhost:27017/skripsi')
db=client['skripsi']
#collections=db['schemaHierarchy']
with open('indexPage.json','r') as f:
	data=json.load(f)

for datum in data:
	post=datum
	#print post	
	posts=db.indexPage
	print posts.insert_one(post)


