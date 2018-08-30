from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from googletrans import Translator
import nltk
import re
import itertools
from itertools import groupby
import string
import numpy as np
import MySQLdb
from nltk.corpus import brown
from operator import itemgetter
#attributes=['name','gender','place of birth','date of birth','religion','educational requirement','job title','faculty','department','classroom','have a job','role name']
#attributes=['id','name','nip','gender','place of birth','date of birth','religion','the highest education','staff type','unit','rank','space class','functional','image','structural positions']
attributes=['name','nim','force','faculty','unit','place of birth','date of birth','image']
properties=['additional Type', 'alternate Name', 'description', 'disambiguating Description', 'identifier', 'image', 'main Entity Of Page', 'name', 'potential Action', 'same As', 'subject Of', 'rl', 'additional Name', 'address', 'affiliation', 'alumni Of', 'award', 'birth Date', 'birth Place', 'brand', 'children', 'colleague', 'contact Point', 'death Date', 'death Place', 'duns', 'email', 'family Name', 'fax Number', 'follows', 'funder', 'gender', 'given Name', 'global Location Number', 'has Occupation', 'has Offer Catalog', 'has POS', 'height', 'home Location', 'honorific Prefix', 'honorific Suffix', 'isic V4', 'job Title', 'knows', 'makes Offer', 'member Of', 'naics', 'nationality', 'net Worth', 'owns', 'parent', 'performer In', 'publishing Principles', 'related To', 'seeks', 'sibling', 'sponsor', 'spouse', 'tax ID', 'telephone', 'vat ID', 'weight', 'work Location', 'works For']
stop_words=list(stopwords.words('english'))
brown_tagged_sents=brown.tagged_sents()
brown_sents=brown.sents()
tagger=nltk.UnigramTagger(brown_tagged_sents)

#stop_words=list(stop_words)

for i in range(len(stop_words)):
	stop_words[i]=str(stop_words[i])

def addSpace(x):	
	return ' '.join(re.findall('[A-Za-z][a-z]*',x))

def removeStopWords(x):
	for i in range(len(x)):
		x[i]=x[i].lower()	
	return [w for w in x if not w in stop_words]

def generalisasi(word,tag):
	if tag.startswith('N'):
		return (word,'n')
	if tag.startswith('V'):
		return (word,'v')
	if tag.startswith('J'):
		return (word,'a')
	if tag.startswith('R'):
		return (word,'r')
	else:
		return (word,None)

def disambiguitas(word,tag):
	if tag is None:
		return None
	else:
		try:	
			for i in wn.synsets(word,pos=tag):
				print i, i.definition()
			return wn.synsets(word,pos=tag)[0]
		except:
			return None

def helper(listx):
	for i in range(len(listx)):
		listx[i]=generalisasi(*listx[i])
		print 'generalisasi=',listx
		listx[i]=disambiguitas(*listx[i])
		print 'disambiguitas=',listx
	return listx	
def similarity(att,prop):
	try:
#		print att,prop
		att=removeStopWords(word_tokenize(att))
		prop=removeStopWords(word_tokenize(prop))
#		print 'att ',att,'prop ',prop
		att=looping(att)
		prop=looping(prop)
#		print 'att1 ',att,'prop1 ',prop
	
		vector_length=max(len(att),len(prop))
#		print 'vector length',vector_length
		Vx=np.zeros(vector_length,dtype=np.float)
		Vy=np.zeros(vector_length,dtype=np.float)
		S=0
		C=0
		threshold=0.8025
		Vx=wup(att,prop,Vx)
		Vy=wup(prop,att,Vy)
#		print 'v1=',Vx,',V2=',Vy
		for i in range(vector_length):
			S+=Vx[i]*Vy[i]
#		print 'S=',S
		Cx=sorting(Vx)
		Cy=sorting(Vy)
#		print 'C1=',Cx,',C2=',Cy
		if (Cx+Cy)> 0:		
			C+=(Cx+Cy)/1.8
		else:
			C+=vector_length/float(2)
		sim=S/C
#		print 'sim=',sim,'C=',C
	except:
		sim=0
	return sim
	
def sorting(listx):
	return len([i for i in listx if i>0])	

def wup(listx,listy,V1):
#	print 'WUP similarity'
	for i in range(len(listx)):

		helper=[]
		xLemmas= [str(lemma) for lemma in listx[i].lemma_names()]
#		print listx[i]
		for j in range(len(listy)):
			y=listy[j].name()[0:-5]
#			print listy[j]
			if y in xLemmas:
#				print 'synonym'
				d=1
			else:
#				print 'not synonym'
				d=0
			if listx[i].wup_similarity(listy[j]) is not None:
				score=(listx[i].wup_similarity(listy[j])+d)/2					
#				print 'score',score
				helper.append(score)
			else:
				helper.append(0.0)
		#print helper
		V1[i]=max(helper)
#		print 'V1',V1
	return V1

def looping(listx):
	global tagger
	listx=tagger.tag(listx)
	print 'tagging listx=',listx
	listx=helper(listx)
	return listx

def removeSpace(prop):	
	words=re.findall('[A-Za-z][a-z]*',prop)
	#print words		
	return ''.join(words)	

def duplicate(listx):
	global hasil
	dups=dup(listx)
#	print 'dups',dups	
	for i in range(len(listx)):
		if listx[i][1] in dups:
			for j in saved:
				if j[0][1] is listx[i][1]:
#					print 'same ', j[0][1], listx[i][1],listx[i],j[1]
					listx[i]=j[1]
					del saved[saved.index(j)][1]
					
	dups=dup(listx)
#	print len(dups)
	if len(dups)==0:
		hasil=listx
	else:
		duplicate(listx)

def dup(listx):
	d=dict()
	dups=[]
	result=[]
	for s,a,p in listx:
		d[p]=d.get(p,[])+[(s,a)]
#		print p,d[p]
	for k,v in d.items():
 		if len(v)>1:
			sort=sorted(d[k], key=lambda x:x[0], reverse=True)
			del sort[0]
			for s,a in sort:
				dups.append(a)
				
	return dups

def matching_property(attributes,properties):
	global saved	
	max_matching_score=[]
	for att in attributes:
		max_score=[]
		for prop in properties:
			scoreMatching=similarity(att,prop)
			max_score.append((scoreMatching,att,prop))
		saved.append(sorted(max_score, key=lambda x:x[0], reverse=True))
		if max(max_score, key=lambda x: x[0])[0] < 0.001:
			max_matching_score.append((0,removeSpace(string.capwords(att)),removeSpace(string.capwords(att))))
		else:
			max_matching_score.append(max(max_score, key=lambda x: x[0]))
	return max_matching_score
saved=[]
hasil=[]

def lastStep(attributes,properties):
	result= matching_property(attributes,properties)
	duplicate(result)
# if mau return only greater than 0.5
	print result
	print [x for x in hasil if x[0]>0.5]
	return [x for x in hasil if x[0]>0.5]
#	return hasil
lastStep(['place of birth'],['birth place'])
