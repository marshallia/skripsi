from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from googletrans import Translator

import re
import string

translator=Translator()

def convToWn(tag):
	if tag.startswith('N'):
		return 'n'
	if tag.startswith('V'):
		return 'v'
	if tag.startswith('J'):
		return 'a'
	if tag.startswith('R'):
		return 'r'
	return None

def tagToSynset(word,tag):
	wordnet_tag=convToWn(tag)
	#print wordnet_tag
	if wordnet_tag is None:
		return None
	else:
		try:	
			return wn.synsets(word,wordnet_tag)[0]
		except:
			return None

def similarity(sentence1, sentence2):
	sentence1=pos_tag(word_tokenize(sentence1))
	sentence2=pos_tag(word_tokenize(sentence2))
	synset1=[tagToSynset(*tagged_word) for tagged_word in sentence1]	
	synset2=[tagToSynset(*tagged_word) for tagged_word in sentence2]
	#print synset1, synset2
	synset1=[ss for ss in synset1 if ss]
	synset2=[ss for ss in synset2 if ss]
	score, count=0.0,0
	for syn in synset1:
		scoce=[]
		for ss in synset2:
			scoce.append(syn.wup_similarity(ss))
			best_score=max(scoce)
			if best_score is not None:
				score+=best_score
				count+=1
	if count==0:
		return 0
	else:
		score/=count
		return score

def addSpace(attributes):	
	result=[]
	for attribute in attributes:		
		words=re.findall('[A-Za-z][a-z]*',attribute)
		#print words		
		result.append(' '.join(words))
	return result	

def removeSpace(prop):	
	words=re.findall('[A-Za-z][a-z]*',prop)
	#print words		
	return ''.join(words)	

def matching_property(attributes,properties):
	max_matching_score=[]	
	for att in attributes:
		#print att
		max_score=[]
		for prop in properties:
		#	print prop
			scoreMatching=similarity(att,prop)
			#print scoreMatching
			max_score.append((scoreMatching,removeSpace(string.capwords(att)),removeSpace(prop)))
		if max(max_score, key=lambda x: x[0])[0] < 0.5:#threshold matching
			max_matching_score.append((0,removeSpace(string.capwords(att)),removeSpace(string.capwords(att))))
		else:
			max_matching_score.append(max(max_score, key=lambda x: x[0]))			
	print 'hasil akhir matching'
	print max_matching_score
	return max_matching_score

def translate(x):
	h1=[]
	#translation=translator.translate(x,dest='en')
	for i in x:
		a=re.sub(r'[\W_]',' ',i)
		att=translator.translate(a,dest='en').text
		#print att
		h1.append(str(att))
	return h1

