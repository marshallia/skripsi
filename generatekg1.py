import crawl, json
import string
from pymongo import MongoClient

client=MongoClient()
client=MongoClient('mongodb://adminSkripsi:adminSkripsi123@localhost:27017/skripsi')
db=client['skripsi']
post1=db.edge1
post=db.node1
files=crawl.listFile()
#print files
markup=crawl.crawlMarkup(files)

def main(data):
	data.pop('@context')
	if get_id(data.get('name'))==None:	post.insert_one({'type':data.get('@type'
),'name':str(data.get('name')).lower()})
	data.pop('@type')
	insert(data)

def get_id(name):
	return post.find_one({'name':str(name).lower()},{'_id':1})
	

def insert(data):
	depth=0
	a=get_id(data.get('name'))
	for key in data:
		if isinstance(data[key], dict)==False:
			if key !='name':
				if 'date' in key.lower():
					if get_id(data.get(key))==None:post.insert_one({'name':str(data.get(key)).lower(),'type': 'date'})
				else:
					if get_id(data.get(key))==None:post.insert_one({'name':str(data.get(key)).lower(),'type':'text'})
				b=get_id(data.get(key))
				post1.insert_one({'node1':str(data.get('name')).lower(),'node2':str(data.get(key)).lower(),'edge':key})
		else:
			print data[key]['@type'],data[key]['name']
			if get_id(data[key]['name'])==None:post.insert_one({'type':data[key]['@type'],'name':str(data[key]['name']).lower()})
			c=get_id(data[key]['name'])
			post1.insert_one({'node1':str(data.get('name')).lower(),'node2':data[key]['name'].lower(),'edge':key})
			d=data[key]
			d.pop('@type')
			insert(d)	
	return depth
for i in markup:
	print i
	main(json.loads(i))
	
