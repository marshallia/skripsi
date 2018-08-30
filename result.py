from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from googletrans import Translator
import nltk
import re
import string
from nltk.corpus import brown

attributes=['Identifier', 'name','Gender','PlaceOfBirth','DateOfBirth','Religion','EducationRequirement','jobTitle','Faculty','Department','Classroom','HaveAJob','RoleName']
properties=['additionalType', 'alternateName', 'description', 'disambiguatingDescription', 'identifier', 'image', 'mainEntityOfPage', 'name', 'potentialAction', 'sameAs', 'subjectOf', 'rl', 'additionalName', 'address', 'affiliation', 'alumniOf', 'award', 'birthDate', 'birthPlace', 'brand', 'children', 'colleague', 'contactPoint', 'deathDate', 'deathPlace', 'duns', 'email', 'familyName', 'faxNumber', 'follows', 'funder', 'gender', 'givenName', 'globalLocationNumber', 'hasOccupation', 'hasOfferCatalog', 'hasPOS', 'height', 'homeLocation', 'honorificPrefix', 'honorificSuffix', 'isicV4', 'jobTitle', 'knows', 'makesOffer', 'memberOf', 'naics', 'nationality', 'netWorth', 'owns', 'parent', 'performerIn', 'publishingPrinciples', 'relatedTo', 'seeks', 'sibling', 'sponsor', 'spouse', 'taxID', 'telephone', 'vatID', 'weight', 'workLocation', 'worksFor']

stop_words=set(stopwords.words('english'))

freqs = nltk.FreqDist(w.lower() for w in brown.words())
freq2 = nltk.ConditionalFreqDist((tag, wrd.lower()) for wrd, tag in brown.tagged_words(tagset="universal"))
def addSpace(listx):	
	result=[]
	for x in listx:		
		result.append(' '.join(re.findall('[A-Za-z][a-z]*',x)))
	return result	

def removeStopWords(listx):
	result=[]
	for x in listx:	
		for i in range(len(x)):
			x[i]=x[i].lower()	
		result.append([w for w in x if not w in stop_words])
	return result
		
def tagging(listx):
	result=[]
	for x in listx:
		print [tagToSynset(*tag) for tag in pos_tag(x)]
		result.append([tagToSynset(*tag) for tag in pos_tag(x)])	
	return result

def convertToWn(tag):
	if tag.startswith('N'):
		return 'n'
	if tag.startswith('V'):
		return 'v'
	if tag.startswith('J'):
		return 'a'
	if tag.startswith('R'):
		return 'r'
	else:
		return None

def tagToSynset(word,tag):
	wordnet_tag=convertToWn(tag)
	#print word,wordnet_tag
	if wordnet_tag is None:
		return None
	else:
		try:	
			x=[str(i) for i in wn.synsets(word,wordnet_tag)]
			return wn.synsets(word,wordnet_tag)[0]
		except:
			return None

def similarity(sentence1, sentence2):
	sentence1=pos_tag(word_tokenize(sentence1))
	sentence2=pos_tag(word_tokenize(sentence2))
	synset1=[tagToSynset(*tagged_word) for tagged_word in sentence1]	
	synset2=[tagToSynset(*tagged_word) for tagged_word in sentence2]
	synset1=[ss for ss in synset1 if ss]
	synset2=[ss for ss in synset2 if ss]
	#print 'attribute',synset1,'\nproperti', synset2
	
	score, count=0.0,0
	for syn in synset1:
		scoce=[]
		for ss in synset2:
			scoce.append(syn.wup_similarity(ss))
			print syn,ss,scoce
			#print 'lemma att',[str(j) for j in syn.lemma_names()]
			#print 'lemma prop',[str(j) for j in ss.lemma_names()]
			
			best_score=max(scoce)
			#print syn,ss,'best score ',best_score
			if best_score is not None:
				score+=best_score
				count+=1
	if count==0:
		return 0
	else:
		score/=count
		#print score
		return score

def removeSpace(prop):	
	words=re.findall('[A-Za-z][a-z]*',prop)
	#print words		
	return ''.join(words)	

def matching_property(attributes,properties):
	max_matching_score=[]	
	for att in attributes:
		max_score=[]
		for prop in properties:
			scoreMatching=similarity(att,prop)
			#print 'attribute ',att,'property ',prop,'score ',scoreMatching
			max_score.append((scoreMatching,removeSpace(string.capwords(att)),removeSpace(prop)))
		#if max(max_score, key=lambda x: x[0])[0] < 0.5:#threshold matching
		#	max_matching_score.append((0,removeSpace(string.capwords(att)),removeSpace(string.capwords(att))))
		#else:
		max_matching_score.append(max(max_score, key=lambda x: x[0]))
		print max_matching_score			
	return max_matching_score

def common(listx):
	h=[wn.synset(i[8:-2]) for i in listx]
	print [i[8:-7] for i in listx]
	for j in h:
		
		k=j.lemma_names()
		print 'word ',j,'lemma ',k
		for x in k:
			print str(x)
matching_property(attributes,properties)

'''
attributes=[word_tokenize(x) for x in addSpace(attributes)]
properties=[word_tokenize(x) for x in addSpace(properties)]

attributes=removeStopWords(attributes)
properties=removeStopWords(properties)
tagging(attributes)
print properties 
print attributes
print freq2['NOUN']['tax']
#a=[Synset('function.n.03'), Synset('character.n.04'), Synset('function.n.02'), Synset('role.n.04')]
#common(a)
x=["Synset('name.n.01')", "Synset('name.n.02')", "Synset('name.n.03')", "Synset('name.n.04')", "Synset('name.n.05')", "Synset('name.n.06')"]


			

h={"Synset('have.v.01')", "Synset('occupation.n.01')"}
'''

