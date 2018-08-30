from Tkinter import *
from ttk import *
import Tkinter as tk
import model1 as md 
import MySQLdb
import savepoint_wordnet as wn
import test1 as withd
from nltk import word_tokenize, pos_tag

LARGE_FONT= ("Verdana", 12)
SLARGE_FONT= ("Verdana", 25)

attributes=[]
properties=[]
translatedAttributes=[]
attributeMatch=[]
matchingScore=[]
classname=''
tablename=''
databaseName=''
Mydb=md.Mydb()
preprop=md.preprop()
mongo=md.mongo()
wordnet1=md.wordnet1()
expectedType=[]
class MyApp(Tk):

    def __init__(self, *args, **kwargs):
        
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
	container.pack( expand = YES, fill = BOTH )
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,PageTwo,PageThree,PageFour,PageFive,PageSix):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
	    
        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
	return self.frames[page_class]
        
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self,parent)
        label = Label(self, text="WELCOME", font=SLARGE_FONT)
        label.pack(side=TOP,expand=YES,fill=Y)

        button = Button(self, text="Visit Page 1",command=lambda: controller.show_frame(PageTwo))
        button.pack(side=TOP,expand=YES)

class PageTwo(Frame):
    	
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
	self.con=controller
	self.grid()
	for i in range(3):
		self.grid_columnconfigure(i,weight=1)
	for j in range(9):
		self.grid_rowconfigure(j,weight=1)
	self.create_widget(self.con)
    def create_widget(self,controller):
	global preprop
	
        label = Label(self, text="Select Table Reference", font=LARGE_FONT)
        label.grid(row=0,column=0, padx=5,pady=5,columnspan=3)

	label1 = Label(self, text="Select Database")
        label1.grid(row=1,column=0, padx=5,pady=5)

	self.databases=StringVar(self)
	choices = preprop.get_databases()

	self.database=OptionMenu(self,self.databases, *choices, command=self.get_table)
	self.database.bind()
	self.database.grid(row=1,column=1,columnspan=2,rowspan=1, padx=5,pady=5,sticky='WE')
		
	label2 = Label(self, text="Select table")
        label2.grid(row=2,column=0,padx=5,pady=5)
	
	self.tables=Treeview(self)
	self.tables.grid(row=2,column=1,padx=5,pady=5,columnspan=2, rowspan=1,sticky='NSWE')
	self.tables.bind("<Double-Button-1>",self.get_att)
	
	label3 = Label(self, text="Display Attribute")
        label3.grid(row=3,column=0,padx=5,pady=5)
	
	self.treeTable=Treeview(self,selectmode='extended')
	self.treeTable.grid(row=4, column=0,columnspan=1,rowspan=4,padx=5,pady=5,sticky='NSWE')
	self.treeTable.heading("#0", text='attribute')
	self.treeTable.column("#0", anchor='w')
	
	self.remove=Button(self,text='remove', command=self.removeatt)
	self.remove.grid(row=5, column=1,padx=5,pady=5,sticky='WE')	
	self.match=Button(self,text='translate', command=self.match)
	self.match.grid(row=6, column=1,padx=5,pady=5,sticky='WE')
	
	label4 = Label(self, text="Display Matching value")
        label4.grid(row=3,column=2,padx=5,pady=5)
	
	self.treeTranslate=Treeview(self)
	self.treeTranslate['column']=()
	self.treeTranslate.grid(row=4, column=2,columnspan=1,rowspan=4,padx=5,pady=5,sticky='NSWE')
	self.treeTranslate.heading("#0", text='attribute')
	self.treeTranslate.column("#0", anchor='w')
	
	self.button1 = Button(self, text="Prev",command=lambda: controller.show_frame(PageOne))
        self.button1.grid(row=8,column=1, sticky='WE')

        self.button2 = Button(self, text="Next",command=lambda: self.next(controller))
        self.button2.grid(row=8,column=2, sticky='WE')

    def next(self,controller):
	global translatedAttributes
	global attributes

	attributes=self.treeTable.get_children()
	translatedAttributes=self.treeTranslate.get_children()
	controller.show_frame(PageThree)
	
    def removeatt(self):
	selected=self.treeTable.selection()
	for i in selected:
		self.treeTable.delete(i)

    def get_table(self,*args):
	global databaseName
	global preprop

	self.tables.delete(*self.tables.get_children())
	self.clearTV()
	databaseName=self.databases.get()
	self.b=preprop.get_tables(databaseName,'show tables;')
	for i in self.b:
		self.tables.insert('','end',i,text=i)

    def get_att(self,*args):
	global tablename
	global databaseName
	global preprop

	currItem=self.tables.focus()
	tablename=self.tables.item(currItem)['text']
	
	self.clearTV()
	attributes=preprop.get_att(databaseName,tablename)
	
	self.insertTV(attributes)

    def clearTV(self,*args):
	self.treeTable.delete(*self.treeTable.get_children())

    def insertTV(self,att):
	for at in att:
		self.treeTable.insert('','end',at,text=at)

    def match(self):
	self.treeTranslate.delete(*self.treeTranslate.get_children())
	help=wn.translate(wn.addSpace(list(self.treeTable.get_children())))
	for at in help:
		self.treeTranslate.insert('','end',at,text=at)
	
	
class PageThree(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
	self.con=controller
	self.grid()
	for i in range(3):
		self.grid_columnconfigure(i,weight=1)
	for j in range(9):
		self.grid_rowconfigure(j,weight=1)
	self.create_widget(self.con)	
         
    def create_widget(self,controller):
	global preprop
	

	label = Label(self, text='Select Class Reference', font=LARGE_FONT)
	label.grid(row=0,column=0,padx=5,pady=5,columnspan=3)
	
	label2=Label(self,text='Select Class :')
	label2.grid(row=1,column=0,padx=5,pady=5,sticky='W')
	
	self.clasess=StringVar(self)
	self.choices = preprop.get_tables('uns','show tables;')

	self.classList=Listbox(self,height=5,selectmode=BROWSE)
	self.classList.bind("<Double-Button-1>",self.printed)
	self.classList.grid(row=1,column=1,rowspan=1,sticky='WE')
	self.scroll=Scrollbar(self,command=self.classList.yview)
	self.scroll.grid(column=2,row=1,padx=5,pady=5,sticky='SN',rowspan=1)

	label3=Label(self, text='Properties ')
	label3.grid(row=2,column=0,padx=5,pady=5,sticky='WE',columnspan=3)	
	
	self.classList.configure(yscrollcommand=self.scroll.set)
	
	for i in self.choices:
		self.classList.insert(END,i)
	
	self.propTree=Treeview(self)
	self.propTree.grid(row=3, column=0,columnspan=3,rowspan=5,sticky='NEWS')
	self.propTree['column']=('expected')
	self.propTree.heading("#0", text='Property')
	self.propTree.column("#0", anchor='center')
	self.propTree.heading('#1',text='Expected Type')
	self.propTree.column('#1',anchor='center')
	
	self.button1 = Button(self, text="Prev",command=lambda: controller.show_frame(PageTwo))
        self.button1.grid(row=8,column=1,padx=5,pady=5,sticky='WE')

        self.button2 = Button(self, text="Next",command=lambda: self.next(controller))
        self.button2.grid(row=8,column=2,padx=5,pady=5,sticky='WE')
   
    def printed(self,*args):
	global wordnet1
	global properties
	global classname
	items= self.classList.curselection()
	self.propTree.delete(*self.propTree.get_children())
	
	classname=wordnet1.strip(str([self.choices[int(item)] for item in items]))
	self.helpProp=self.get_schemaClass(classname)
	for at in self.helpProp:
		value=''
		for i in range(len(at[1])):
			value+=str(at[1][i])+','
#		print value
		self.propTree.insert('','end',at[0],text=at[0],value=(value))
	properties=self.propTree.get_children()	

    def get_schemaClass(self,name):
	global mongo
	global expectedType
		
	self.classes= mongo.get_related_schema(name)
	expectedType= mongo.get_available_prop(self.classes)
	return expectedType
	
    def next(self,controller):
	global properties
	global translatedAttributes
	global wordnet1
	global classname
	global scoreMatching
	global expectedType
	global attributeMatch
		
	att= wn.addSpace(translatedAttributes)
	prop=wn.addSpace(properties)
#	print 'property 1', properties
	scoreMatching=withd.lastStep(att,prop)
	properties=[prop[2] for prop in scoreMatching]
	for i in range(len(properties)):
		properties[i]=wn.removeSpace(properties[i])
#	print 'property 2', properties
		
	help=[]
	psudomarkup=wordnet1.sudoMarkup(properties,expectedType,classname,help)
#	print 'pseudomarkup',psudomarkup
	items= self.classList.curselection()
	classname=wordnet1.strip(str([self.choices[int(item)] for item in items]))	
#	print 'classname',classname
	self.page4=controller.get_page(PageFour)
	self.page4.treeMatch.delete(*self.page4.treeMatch.get_children())
	
	#self.page4.markup.insert(END,'<script type="application/ld+json">\n{\n"@context": "http://schema.org",\n"@type": "'+classname+'",\n')
	for sc in scoreMatching:
		self.page4.treeMatch.insert('','end',sc[1],text=sc[1],value=(sc[2],sc[0]))
		#self.page4.markup.insert(END,'"'+sc[2]+'":"#####",\n')
	self.page4.markup.insert(END,psudomarkup)
	controller.show_frame(PageFour)

class PageFour(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
	self.con=controller
	self.grid()
	for i in range(3):
		self.grid_columnconfigure(i,weight=1)
	for j in range(9):
		self.grid_rowconfigure(j,weight=1)
	self.create_widget(self.con)
         
    def create_widget(self,controller):

	label = Label(self, text="Schema.org Matching", font=LARGE_FONT)
	label.grid(row=0,column=0,columnspan=3,padx=5,pady=5,sticky='WE')

	label1=Label(self,text='Matching Result')
	label1.grid(row=1,column=0,padx=5,pady=5,sticky='W')	

	self.treeMatch=Treeview(self)
	self.treeMatch['column']=('property','score')
	self.treeMatch.grid(row=2, column=0,columnspan=3,rowspan=2,sticky='NEWS')
	self.treeMatch.heading("#0", text='attribute')
	self.treeMatch.column("#0", anchor='w')
	self.treeMatch.heading('#1', text='property')
	self.treeMatch.column('#1',anchor='w')
	self.treeMatch.heading('#2',text='score')
	self.treeMatch.column('#2', anchor='w')
	
	label1=Label(self,text='Markup :')	
	label1.grid(column=0,row=4, padx=5,pady=5, sticky='W')
	
	self.sbar=Scrollbar(self)
	self.markup=Text(self, relief=SUNKEN)
	self.sbar.config(command=self.markup.yview)
	self.markup.config(yscrollcommand=self.sbar.set)
	self.markup.grid(row=5,column=0,padx=5,pady=5,columnspan=2,sticky='WE',rowspan=3)	
	self.sbar.grid(row=5,column=2,sticky='NS',rowspan=3)	

	self.button1 = Button(self, text="Prev",command=lambda: controller.show_frame(PageThree))
        self.button1.grid(row=8,column=1,padx=5,pady=5,sticky='WE')

        self.button2 = Button(self, text="Next",command=lambda: self.setData(controller))
        self.button2.grid(row=8,column=2,padx=5,pady=5,sticky='WE')

    def setData(self,controller):
	global attributes
	global preprop
	global tablename
	
	page5=controller.get_page(PageFive)                                                                
	page5.treeData['column']=tuple(attributes)[1:]
	print 'att now ',tuple(attributes)[1:]
	print 'att result ',attributeMatch
	for i in range(len(attributes)):
		page5.treeData.heading('#'+str(i),text=attributes[i])
		page5.treeData.column('#'+str(i),anchor='center')	
	
	kolumn= str(attributes).strip("(',')")       
	kolumn=kolumn.replace("'", "")
#	kolumn= str(attributeMatch).strip("[,]")
	data=list(preprop.get_tables('uns','select '+kolumn+' from '+tablename+';'))
	print data
	page5.treeData.delete(*page5.treeData.get_children())
	for i in data:	
		print i[0],i[1:]
		page5.treeData.insert('','end',i[0],text=i[0],value=(i[1:]))
	controller.show_frame(PageFive)	


class PageFive(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
	self.con=controller
	self.grid()
	#self.grid_columnconfigure(2,weight=1)
	#self.grid_columnconfigure(1,weight=1)
	for i in range(3):
		self.grid_columnconfigure(i,weight=1)
	for j in range(9):
		self.grid_rowconfigure(j,weight=1)
	self.create_widget(self.con)
	 
    def create_widget(self,controller):
	label=Label(self,text='Data Selection',font=SLARGE_FONT,anchor='center')
	label.grid(row=0,column=0,columnspan=3,padx=5,pady=5, sticky='WE')
	
	
	self.treeData=Treeview(self,selectmode='extended')
	ysb = Scrollbar(self, orient='vertical', command=self.treeData.yview)
        xsb = Scrollbar(self,orient='horizontal',command=self.treeData.xview)

	self.treeData.config(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
	self.treeData.grid(row=1,column=0,columnspan=3,rowspan=2,padx=5,pady=5,sticky='NEWS')
	#ysb.grid(row=1,column=2,sticky='SN')
	xsb.grid(row=3,column=0,sticky='WE')	

	label1=Label(self,text='Result :')
	label1.grid(row=4,column=0,padx=5,pady=5,sticky='W')
 
	button3=Button(self,text="Generate",command=lambda: self.generate(controller))
	button3.grid(row=4,column=1,padx=5,pady=5,sticky='WE')

	self.sbar=Scrollbar(self)
	self.markup=Text(self, relief=SUNKEN)
	self.sbar.config(command=self.markup.yview)
	self.markup.config(yscrollcommand=self.sbar.set)
	self.markup.grid(row=5,column=0,padx=5,pady=5,columnspan=3,sticky='WE',rowspan=3)	
	#self.sbar.grid(row=5,column=2,sticky='NS',rowspan=3)
	
	self.button1 = Button(self, text="Prev",command=lambda: controller.show_frame(PageFour))
        self.button1.grid(row=8,column=1,padx=5,pady=5,sticky='WE')

        self.button2 = Button(self, text="Next",command=lambda: self.webgen(controller))
        self.button2.grid(row=8,column=2,padx=5,pady=5,sticky='WE')

    def generate(self,controller):
	global expectedType
	global classname
	global scoreMatching
	global wordnet1
	global properties

	help=[]

	if not(self.markup.get('1.0',END)is None) :
		self.markup.delete('1.0', END)	

	page2=controller.get_page(PageTwo)
	selected=self.treeData.focus()

	help.append(self.treeData.item(selected)['text'])
	help+= self.treeData.item(selected)['values']
	#help.pop(len(help)-1)
	self.markup.insert(END,wordnet1.sudoMarkup(properties,expectedType,classname,help))

    def webgen(self,controller):
	global wordnet1
	global attributes

	mark=str(self.markup.get('1.0',END))
	#print mark
	selected=self.treeData.focus()
	data=self.treeData.item(selected)['values']
	data.append(self.treeData.item(selected)['text'])
	att=wn.addSpace(attributes)
	page6=controller.get_page(PageSix)
	page6.webpage.insert(END,wordnet1.genWebpage(att,data,mark))
	controller.show_frame(PageSix)

class PageSix(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
	self.con=controller
	self.grid()
	for i in range(3):
		self.grid_columnconfigure(i,weight=1)
	for j in range(9):
		self.grid_rowconfigure(j,weight=1)
	self.create_widget(self.con)
         
    def create_widget(self,controller):
	label=Label(self, text='Hasil Webpage')
	label.grid(row=0,column=0)
	self.sbar=Scrollbar(self)
	self.webpage=Text(self, relief=SUNKEN)
	self.sbar.config(command=self.webpage.yview)
	self.webpage.config(yscrollcommand=self.sbar.set)
	self.webpage.grid(row=1,column=0,padx=5,pady=5,columnspan=3,sticky='NEWS',rowspan=6)	
	#self.sbar.grid(row=5,column=2,sticky='NS',rowspan=3)
	
	self.button1 = Button(self, text="Prev",command=lambda: controller.show_frame(PageFive))
        self.button1.grid(row=8,column=1,padx=5,pady=5,sticky='WE')

        self.button2 = Button(self, text="Next",command=lambda: controller.show_frame(PageSix))
        self.button2.grid(row=8,column=2,padx=5,pady=5,sticky='WE')	

app = MyApp()
#app.geometry('500x600')
app.title('schema markup')
app.mainloop()


