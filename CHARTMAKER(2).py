'''
Created on Jan 25, 2013

@author: 25608
'''

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(selfparams):
        
        
        apply(Frame.__init__,(self,Master),kw)


        self.reportPath = 'C:\\CCWD'
        self.logoPath = 'C:\\CCWD\\ogo.ico'
        self.menubar = Menu(Master,tearoff=1)
        filemenu = Menu(self.menubar, tearoff=0)

        filemenu.add_command(label="Exit", command=Master.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_separator()
        self.master.config(menu=self.menubar)        
        
        self.BaseFrame = Frame(self)
        self.BaseFrame.grid(row=0, column=0, padx = 1, pady=1)
        #self.SideFrame = Frame(self)
        #self.SideFrame.grid(row=0, column=1, padx = 1, pady=1)
        self.ButtonFrame = Frame(self)
        self.ButtonFrame.grid(row=2, column=0, padx = 1, pady=1)
        #self.ButtonFrame2 = Frame(self)
        #self.ButtonFrame2.grid(row=1, column=0, padx = 1, pady=1)
        self.colors = COLORS 
 
 
 
    def TableMode(self):
        def regenerateGRID():
            x= 0
        
            COUNTER = 0
            abcs = map(chr, range(64, 91))
            
            while COUNTER < (len(abcs)-1):
                x1 = x + 100
                y = 0 
                z = 0
                if x != 0:
                    self.bigTable.canvas.create_text(x + 50, 25, text = str(abcs[COUNTER]))
                while y < self.wInfo.imagecanvasHeight:
                    y1 = y + 50
                    self.bigTable.canvas.create_rectangle(x,y, x1, y1, activefill='yellow')
                    if x == 0 and z>0:
                        self.bigTable.canvas.create_text(50, y + 25, text = str(z))
                    y += 50
                    z += 1
                x += 100
                COUNTER += 1
        def loadValsProxy(event):
            loadVals()
        def loadVals():
                self.tableSelected = "LMS_DATA_MODELS_" +self.tableModeTableList.selection_get().lower()

                columns = "PRAGMA table_info(%s)" %  self.tableSelected
                self.cursorspatial = curspatial()
                self.cursorspatial.execute(columns)
                cols = self.cursorspatial.fetchall()
                self.bigTable.canvas.delete("all")
                regenerateGRID()
                self.sqlAllFieldsList = []
                y = 75
                x = 150
                for COUNTER,col in enumerate(cols):
                    if col[1] == "Geometry":
                        geomval = COUNTER
                    text = Text()
                    self.bigTable.canvas.create_text(x, y, text = str(col[1]).replace(' ','\n')[:15])  
                    x+= 100  
                sql = "SELECT * FROM %s" % self.tableSelected
                
                self.cursorspatial.execute(sql)
                vals = self.cursorspatial.fetchall()
                del self.cursorspatial
                y = 125
                self.tableModeDataDic = {}
                for  valtup in vals:
                    x = 150
                    for COUNTER,rval in enumerate(valtup):
                        
                        if COUNTER == geomval:
                            data = "<Spatial Data>"
                        else:
                            data = rval
                        
                        self.bigTable.canvas.create_text(x, y, text = str(data).replace(' ','\n')[:15]) 
                        x100 = x + 50
                        y100 = y+ 25
                        rangetup = (x-50,x100,y-25,y100)
                        self.tableModeDataDic[rangetup] = str(data)
                        x += 100
                    y+=50
        def exploreVals(event):
            x = event.x
            y = event.y
            regenerateGRID()
            loadVals()
            for rangetup in  self.tableModeDataDic:
                if x in range(rangetup[0], rangetup[1]):
                    if y in range(rangetup[2], rangetup[3]):
                        self.tableTextInput.delete(0,END)
                        self.tableTextInput.insert(0, self.tableModeDataDic[rangetup])
                        valentry = Entry(width=10)
                        text = self.tableModeDataDic[rangetup]
                        valentry.insert(0,text)
                        self.bigTable.canvas.create_window(x,y,window=valentry,anchor="nw")
                        self.bigTable.canvas.create_rectangle(rangetup[0],rangetup[2], rangetup[1], rangetup[3],outline="red" ,width=2.0)
                        
        self.tableModeFrame = Frame(self.BaseFrame,bg=self.backgroundcolor, 
                                     
                                     relief=SUNKEN, bd=2)
        self.tableModeFrame.grid(row=0,column=0, rowspan=7,columnspan=10, ipadx=10, ipady=5,sticky = W+E+N+S)


        self.tableModeFrameMain = Frame(self.tableModeFrame,bg=self.backgroundcolor, relief=SUNKEN, bd=2)
        self.tableModeFrameMain.grid(row=0,column=4, rowspan=4,columnspan=6)
        self.tableTextLabel = Label(self.tableModeFrameMain, text= "Data Value:", fg="white", bg = 'dim grey')
        self.tableTextLabel.grid(row=3,column=0)
        self.tableTextInput = Entry(self.tableModeFrameMain,width=100)
        self.tableTextInput.grid(row=3,column=1,columnspan=6)
        self.bigTable = TableWindow(self.tableModeFrameMain,self.wInfo.imagecanvasWidth , self.wInfo.imagecanvasHeight   )
        self.bigTable.canvas.grid(row=0,column=0,rowspan=3,columnspan=6)
        self.bigTable.canvas.bind("<Double-Button-1>", exploreVals)
        regenerateGRID()

        self.sideSliverTableFrame = Frame(self.tableModeFrame,bg=self.backgroundcolor)
        self.sideSliverTableFrame.grid( row=0,column=0, rowspan=7)
        self.sideTableFrame = Frame(self.tableModeFrame,bg=self.backgroundcolor)
        self.sideTableFrame.grid( row=0,column=1, rowspan=6, columnspan=3)
        self.tableTextTablesLabel = Label(self.sideTableFrame, text= "Double Click on a Table", fg="white", bg = 'dim grey')
        self.tableTextTablesLabel.grid(row=0,column=0,columnspan=3)
            

        sql = '''SELECT name FROM sqlite_master WHERE type='table'  ORDER BY name'''
        self.cursorspatial = curspatial()
        self.cursorspatial.execute(sql)
        self.tablesTableMode = self.cursorspatial.fetchall()



        
        self.scrollbarTableMode = Scrollbar(self.sideSliverTableFrame, orient=VERTICAL)
        
        self.tableModeTableList = Listbox(self.sideTableFrame,selectmode=SINGLE,height=15,width=55,yscrollcommand=self.scrollbarTableMode.set)
        self.tableModeTableList.grid(row=1, column=0, rowspan=2)
        self.tableModeTableList.bind("<Double-Button-1>", loadValsProxy)
        self.scrollbarTableMode.config(command=self.tableModeTableList.yview)
        self.scrollbarTableMode.grid(row=0,column=0)
        for table in self.tablesTableMode:
            
            if table[0].find('LMS') != -1 and table[0].find('idx') == -1 :
                
                self.tableModeTableList.insert(END, table[0].replace('LMS_DATA_MODELS_','').title())

        



        self.tableMapWindow = Map(self.sideTableFrame,self.wInfo.mapcanvasHeight* .47, self.wInfo.mapcanvasHeight *.4  )
        self.tableMapWindow.canvas.grid(row=3,column=0, rowspan=3, columnspan=3)
        
        
        self.imageModeGridSQL()
        self.tableMapWindow.canvas.delete("all")
        filename  = self.imageLibrary + '\\' +  self.imageModeImageGridName[0] + '.jpg'
        self.tableMapWindowAerial = ImageProcessor4(filename, self.wInfo.mapcanvasHeight *.6)  
        self.tableMapWindow.canvas.create_image(1,1, image= self.tableMapWindowAerial.jpgPI, anchor="nw")
        #self.tableModeLegendWindow = LegendWindow(self.sideTableFrame,self.wInfo.mapcanvasHeight* .5, self.wInfo.mapcanvasHeight *.2  )
        self.tableModeLegendWindow = Text(self.sideTableFrame,width=55, height=3  )

        #self.tableModeLegendWindow.canvas.grid(row=2,column=0,columnspan=3)
        self.tableModeLegendWindow.grid(row=6,column=0,columnspan=3)
        self.tableTextFormulaLabel = Label(self.sideTableFrame, text= "Enter Formula", fg="white", bg = 'dim grey')
        self.tableTextFormulaLabel.grid(row=7,column=0,columnspan=3)

           