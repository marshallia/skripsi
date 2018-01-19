from pymongo import MongoClient
import json
client=MongoClient()
client=MongoClient('mongodb://adminSkripsi:adminSkripsi123@localhost:27017/skripsi')
db=client['skripsi']
#collections=db['schemaHierarchy']
with open('attributes1.json','r') as f:
	data=json.load(f)
#print len(data)
for datum in data:
	post=datum
	print post	
	posts=db.schemaAttribute
	print posts.insert_one(post)

