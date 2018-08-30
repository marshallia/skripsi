from bs4 import BeautifulSoup as bs
import os, sys

def crawlMarkup(files):
	markup=[]
	for fl in files:
		with open ('webpagethreshold/'+fl) as f:
			data=bs(f,'lxml')
			a=data.find('script', type='application/ld+json')
			markup.append(str(a.string))
#			print data.script.string
	return markup
def listFile():
	path='/home/shiro/python2/graph/webpagethreshold/'
	dirs=os.listdir(path)
	files=[]
	for f in dirs:
		files.append(f)
	return files


