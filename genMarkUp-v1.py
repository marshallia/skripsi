import pandas as pd
import MySQLdb as mys
import numpy as np
'''
belum kepake karena belum pake matching
def getSchemaAttribute:
	db=mys.connect('localhost','root','11November1995','schemaTerm')
	cursor=db.cursor()
	sql='select attribute, expectedType from Person;' 
	cursor.execute(sql)
	avClass= cursor.fetchall()
	schemaTerm=pd.DataFrame([[ij for ij in i] for i in avClass])
	schemaTerm.rename(columns={0:'attribute',1:'expectedType'},inplace=True)
	return schemaTerm
'''
def getColumnsName():
	database=mys.connect('localhost','root','11November1995','uns')
	cursor1=database.cursor()
	sql="SELECT column_name FROM information_schema.columns WHERE table_schema = DATABASE() AND table_name='pegawai'ORDER BY ordinal_position;"
	sql1="SELECT * from pegawai;"	
	cursor1.execute(sql)
	attributes = cursor1.fetchall()
	cursor1.execute(sql1)
	datas=cursor1.fetchall()
	data=pd.DataFrame([[ij for ij in i] for i in datas])
	data.rename(columns={0:str(attributes[0]).strip("(',')"),1:str(attributes[1]).strip("(',')"),2:str(attributes[2]).strip("(',')"),3:str(attributes[3]).strip("(',')"),4:str(attributes[4]).strip("(',')"),5:str(attributes[5]).strip("(',')"),6:str(attributes[6]).strip("(',')"),7:str(attributes[7]).strip("(',')"),8:str(attributes[8]).strip("(',')"),9:str(attributes[9]).strip("(',')"),10:str(attributes[10]).strip("(',')"),11:str(attributes[11]).strip("(',')"),12:str(attributes[12]).strip("(',')")},inplace=True)
	return data
	
#main
data=pd.DataFrame()
data=getColumnsName()
head=list(data)
data1=np.array(data.iloc[0:9])
print(data1)
print(data)
print(head)
for i in range(len(data)):
	#print data.loc[0,'name']
	isi='<script type="application/ld+json">\n{\n"@context": "http://schema.org",\n"@type": "person",\n"name":"'+str(data.loc[i,'name'])+'",\n"gender":"'+str(data.loc[i,'gender'])+'",\n"birthPlace":{\n"@type":"Place",\n"name":"'+str(data.loc[i,'birthPlace'])+'"\n},\n"identifier":"'+str(data.loc[i,'identifier'])+'",\n"worksFor":{\n"@type":"CollegeOrUniversity",\n"name":"Sebelas Maret University"},\n"jobTitle":"'+str(data.loc[i,'jobTitle'])+'",\n"hasOccupation":\n{\n"@type":"OrganizationRole",\n"numberedPosition":"1",\n"roleName":"'+str(data.loc[i,'roleName'])+'",\n"startDate":"",\n"endDate":""}\n}\n</script>'
	filename=str(data.loc[i,'name'])+'.json'
	f=open(filename,'wb')
	f.write(isi)
	f.close()	
	
	
