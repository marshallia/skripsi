import pandas as pd
import MySQLdb as mys
import numpy as np

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
def mainMarkUp(data,i):
	isi='<script type="application/ld+json">\n{\n"@context": "http://schema.org",\n"@type": "person",\n"name":"'+str(data.loc[i,'name'])+'",\n"gender":"'+str(data.loc[i,'gender'])+'",\n"birthPlace":{\n"@type":"Place",\n"name":"'+str(data.loc[i,'birthPlace'])+'"\n},\n"identifier":"'+str(data.loc[i,'identifier'])+'",\n"worksFor":{\n"@type":"CollegeOrUniversity",\n"name":"Sebelas Maret University"},\n"jobTitle":"'+str(data.loc[i,'jobTitle'])+'",\n"hasOccupation":\n[{\n"@type":"OrganizationRole",\n"numberedPosition":"1",\n"roleName":"'+str(data.loc[i,'roleName'])+'",\n"startDate":"",\n"endDate":""},\n{"@type":"Occupation",\n"name":"'+str(data.loc[i,'hasOccupation'])+' '+str(data.loc[i,'GolonganRuang'])+'",\n"educationRequirements":"'+str(data.loc[i,'educationalRequirement'])+'",\n"estimatedSalary":{"@type":"MonetaryAmount","value":"1000000","currency":"IDR"}\n}\n]\n}\n</script>'
	return isi

database=mys.connect('localhost','root','11November1995','uns')
cursor=database.cursor()
cursor.execute('select name from pegawai')
names=cursor.fetchall()
data=pd.DataFrame()
data=getColumnsName()
head=list(data)
data1=np.array(data.iloc[0:9])
i=0	
for li in names:
	name=str(li).strip("(',')")
	#print name	
	sql="select * from pegawai where name ='"+name+"';"	
	cursor.execute(sql)
	isi=cursor.fetchall()
	filename=name+'.html'
	markUp=mainMarkUp(data,i)
	f=open(filename,'wb')
	f.write('<! DOCTYPE html><html><head><title>'+name+'</title>'+markUp+'</head><body>')
	for j in range(len(isi[0])):
		f.write('<p>'+str(isi[0][j])+'</p><br>')
	f.write('</body></html>')
	f.close()
	i+=1
