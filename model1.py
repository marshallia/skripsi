import MySQLdb
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs


class Mydb:
	connection=None
	cursor=None
	def __init__(self):
		self.connection=MySQLdb.connect('localhost','root','11November1995')
		self.cursor=self.connection.cursor()
	
	def execute(self,sql,*args):
		self.cursor.execute(sql,*args)
		self.rest=self.cursor.fetchall()
		return self.rest

	def execute1(self,sql,*args):
		self.cursor.execute(sql,*args)

	def query(self,sql,*args):
		try:
			self.execute(sql,*args)
			return self.rest
		except ( AttributeError, MySQLdb.OperationalError ):
			return self.execute (sql, *args)
	
	def query1(self,sql,*args):
		try:
			self.execute1(sql,*args)
			#return self.rest
		except ( AttributeError, MySQLdb.OperationalError ):
			return self.execute (sql, *args)

	def  disconnect (self):
		self.connection.close()

class preprop:

	def strip(self,data):
		self.result=[]
		for datum in data:
			self.result.append(str(datum).strip("(',')"))
		return self.result
	def get_databases(self):
		db=Mydb()			
		self.result=db.query('show databases;')
		self.result=self.strip(self.result)
		return self.result
	def get_tables(self,dbName,command):
		db=Mydb()
		db.query1('use '+dbName)
		result= db.query(command)	
		return result
	
	def get_att(self, dbname,tableName):
		db=Mydb()
		db.query1('use '+dbname)
		attributes = db.query("SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name='"+tableName+"'ORDER BY ordinal_position;")
		attributes=self.strip(attributes)
		return attributes
	
class mongo:
		
	def __init__(self):
		self.client=MongoClient('mongodb://adminSkripsi:adminSkripsi123@localhost:27017/skripsi')	
		self.db=self.client['skripsi']
	
	def get_related_schema(self,className):	
		post=self.db.schemaHierarchy	
		related= tuple(post.find({"className":className}))[0]['ancestors']
		related.append(className)
		return related

	def get_available_prop(self,schemas):
		post=self.db.schemaAttribute
		rest=[]	
		for i in schemas:	
			rest.append(post.find_one({"name":i},{"attributes.attribute":1,"attributes.expectedType":1})['attributes'])
		properties=[]

		for j in range(len(rest)):
			for k in range(len(rest[j])):
				b=[]
				for i in rest[j][k]['expectedType']:
					for l in i:
						b.append(str(l))
				properties.append((str(rest[j][k]['attribute']).strip("[','],(,),u',[,],'"),b))
		return properties
	
	
class wordnet1:
	def strip(self,data):
		return str(data).strip("[','],(,)")

	def genWebpage(self,att,dat,mark):
		g=open(str(dat[len(att)-1])+'.html','wb')
		with open ('index.html') as f:
			data=bs(f)
		ins=data.head
		markup=data.new_tag("script", type="application/ld+json")
		ins.append(markup)
		markup.string=mark		
		oriTag=data.table	
		
		if 'image' in att:
			image=att.index('image')-1
			#print 'image ',dat[image]
			if dat[image] !='':
				data.find('img')['src']=dat[image]
			print 'generate webpage ',dat[image]
		for i in range (len(att)):
			newTag=data.new_tag("tr",id=i)
			oriTag.append(newTag)
			dt1=data.new_tag("td")
			newTag.append(dt1)
			dt2=data.new_tag("td")
			newTag.append(dt2)
			dt1.string=str(att[i])
			dt2.string=str(dat[i-1])
		g.write(str(data))
		g.close()
		return str(data)

	def sudoMarkup(self,prop,types,classname,data):
		markup='{\n"@context": "http://schema.org",\n"@type": "'+classname+'",\n'
#		print len(prop)-1
		expProp=[pp[0] for pp in types]
#		print expProp
		if not data:		
			for i in range (len(prop)):
#				print 'property', i,prop[i]
				if i==(len(prop)-1):
#					print 'terakhir'
					if prop[i] not in expProp:
							markup=markup+'"'+prop[i]+'":"xxxxxx"\n'
					else:			
						for j in types:
							if prop[i]==j[0]:
#								print 'terakhir1'
								if 'Text' in j[1] or 'Date' in j[1] or 'URL' in j[1]:
									markup=markup+'"'+j[0]+'":"xxxxxx"\n'
#									print j[0],'terakhir2'
								else:
#									print 'terakhir3'
									markup=markup+'"'+j[0]+'":{\n"@type":"'+j[1][0]+'",\n\t"name":"xxxxxx"}\n'
#									print j[1][0]
				else:
					if prop[i] not in expProp:
							markup=markup+'"'+prop[i]+'":"xxxxxx",\n'
					else:			
						
						for j in types:
							if prop[i]==j[0]:
								if 'Text' in j[1] or 'Date' in j[1] or 'URL' in j[1]:
									markup=markup+'"'+j[0]+'":"xxxxxx",\n'
#									print j[0]
								else:
									markup=markup+'"'+j[0]+'":{\n"@type":"'+j[1][0]+'",\n\t"name":"xxxxxx"},\n'
#									print j[1][0]
		else:
			for i in range (len( prop)):
#				print 'property', i,prop[i]
				if i==(len(prop)-1):				
					if prop[i] not in expProp:
						markup=markup+'"'+prop[i]+'":"'+str(data[i])+'"\n'
					else:			
						for j in types:
							if prop[i]==j[0]:
								if 'Text' in j[1] or 'Date' in j[1] or 'URL' in j[1]:
									markup=markup+'"'+j[0]+'":"'+str(data[i])+'"\n'
								else:
									markup=markup+'"'+j[0]+'":{\n"@type":"'+j[1][0]+'",\n\t"name":"'+str(data[i])+'"}\n'
				else:
					if prop[i] not in expProp:
							markup=markup+'"'+prop[i]+'":"'+str(data[i])+'",\n'
					else:					
						for j in types:
							if prop[i]==j[0]:
								if 'Text' in j[1] or 'Date' in j[1] or 'URL' in j[1]:
									markup=markup+'"'+j[0]+'":"'+str(data[i])+'",\n'
								else:
									markup=markup+'"'+j[0]+'":{\n"@type":"'+j[1][0]+'",\n\t"name":"'+str(data[i])+'"},\n'
#									print str(data[i])
		markup=markup+'}'
#		print markup
		return markup
					
