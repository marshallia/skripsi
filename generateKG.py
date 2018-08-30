import networkx as nx
import matplotlib.pyplot as plt
from random import *
from graphviz import Graph
import crawl, json
from pymongo import MongoClient

def start():
	client=MongoClient('mongodb://adminSkripsi:adminSkripsi123@localhost:27017/skripsi')	
	db=client['skripsi']
	return db

def insertNode(a,db):
	#print 'new node',a
	db.kg.insert({str("node"):a})

def insertEdge(a,b,lbl,db):
	#print 'edge',a,b,'labeled',lbl
	db.kg.insert({str("edge"):[a,b],str("label"):lbl})


def find_depth(data,db):
	depth = 0
	G.add_node(data.get('name'),type=data.get('@type'))
	f.node(data.get('name'))
	insertNode(str(data.get('name')),db)
	print 'node',data.get('name')
	for key in data:
		if isinstance(data[key], dict)==False:
			if key !='name':
				G.add_node(data.get(key))
				G.add_edge(data.get('name'),data.get(key),label=key)
				f.node(str(data.get(key)))
				f.edge(data.get('name'),data.get(key),label=str(key))
				insertNode(str(data.get(key)),db)
				insertEdge(data.get('name'),data.get(key),str(key),db)
				print 'node',str(data.get(key))
				print 'edge',data.get('name'),data.get(key),str(key)
		else:
		       	depth += 1
			G.add_edge(data.get('name'),data[key]['name'], label=key)
			f.edge(data.get('name'),data[key]['name'], label=key)
			print 'nested',data.get('name'),data[key]['name'],key
			insertEdge(data.get('name'),data[key]['name'], key,db)				
	        	find_depth(data[key],db)
			        	
	return depth

def main(data,db):
	data.pop('@context')
	find_depth(data,db)

def findMe(word,adj,s):
	for key in adj:
		s.edge(key,word,label=adj.get(key)['label'])
		
def search(word):
	adj=G[word]
	print 'adj',adj
	s=Graph('searchKG', filename='search.gv')
	s.attr(rankdir='LR', size='8,5')
	s.attr('node', shape='circle',fillcolor='crimson')
	s.node(word)
	findMe(word,adj,s)
	s.render('search.gv',view=True)


#print list(G.edges)
if __name__=="__main__":
	db=start()
	f=Graph('KG', filename='ravik.gv')
	f.attr(rankdir='LR', size='8,5')
	f.attr('node', shape='circle')

	files=crawl.listFile()
	markup=crawl.crawlMarkup(files)

	G=nx.Graph()
	for i in markup:
		main(json.loads(i),db)
	search("Wakil Rektor")
	#print list(G.nodes)


#f.render('ravik.gv', view=True) 
#print f.source

