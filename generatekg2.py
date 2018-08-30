import networkx as nx
import matplotlib.pyplot as plt
from random import *
from graphviz import Graph
import crawl, json
from pymongo import MongoClient


def insertNode(a,b,db):
	post=db.node
	data={str('node'):a,str('type'):b}
	post.insert_one(data)
def insertEdge(a,b,lbl,db):
	post=db.kg
	data={'edge':[a,b],'label':lbl}
	print data
	post.insert_one(data)

def listNode():
	post=db.knowledegraph
	nodes=[]
	ax=post.find({})
	for a in ax:
		print a["node"]
	return nodes

def find_depth(data,db):
	depth = 0
#	insertNode(str(data.get('name')),str(data.get('@type')),db)
	#print 'name',data.get('name'),'\n'
	#data.pop('name')
	print 'tipe',data.get('@type'),'\n'
	#data.pop('@type')
	for key in data:
		if isinstance(data[key], dict)==False:
			if key !='name':
				#insertNode(str(data.get(key)),'text',db)
				#edge=getNodeID(data.get('name'),data.get(key))
				insertEdge(data.get('name'),data.get(key),str(key),db)
				#print 'edge',data.get('name'),data.get(key),str(key)
				
			
		else:
		       	depth += 1
			#print 'nested',data.get('name'),data[key]['name'],key
			insertEdge(data.get('name'),data[key]['name'], key,db)				
	        	find_depth(data[key],db)
			        	
	return depth

def getNodeID(a,b):
	post=db.knowledegraph
	node=[]
	a=post.find_one({"node":a},{"node":0,"type":0})
	b=post.find_one({"node":b},{"node":0,"type":0})
	return [a,b]
		

def main(data,db):
	data.pop('@context')
	find_depth(data,db)

def findMe(word,adj,s):
	for key in adj:
		s.edge(key,word,label=adj.get(key)['label'])

client=MongoClient()
client=MongoClient('mongodb://adminSkripsi:adminSkripsi123@localhost:27017/skripsi')
db=client['skripsi']

files=crawl.listFile()
markup=crawl.crawlMarkup(files)
#print listNode()

for i in markup:
	main(json.loads(i),db)


#f.render('ravik.gv', view=True) 
#print f.source

