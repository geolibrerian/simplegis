from CCWD.AccessModels import * 
#from CCWD.models import *
from CCWD.views import *
from Tkinter import *
from workers import *
import os, random, datetime

from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.barcharts import VerticalBarChart#,VerticalBarChart3D
from reportlab.graphics.shapes import Drawing,_DrawingEditorMixin,String
from reportlab.graphics.charts.textlabels import Label as rlLabel, BarChartLabel
from reportlab.graphics.samples.excelcolors import color05,color06,color02,color01  ,color02,color03,color04,color05,color06,color07,color08,color09, color10
from reportlab.lib.units import cm, mm, inch
from reportlab.pdfgen.canvas import Canvas as rlCanvas
from reportlab.graphics.widgetbase import Widget,TypedPropertyCollection
from reportlab.lib import colors
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.linecharts import LineChart
from reportlab.lib.formatters import DecimalFormatter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas 

class Calendars(Frame):
    def __init__(self,Master=None,**kw):
        
        apply(Frame.__init__,(self,Master),kw)


        self.reportPath = r'C:\Projects1\ICFFieldOffice\reports'
        self.logoPath = r'C:\Projects1\ICFFieldOffice\icons\logo.ico'
        self.menubar = Menu(Master,tearoff=1)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open",)# command=self.ButtonAddData)
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=Master.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_separator()
    
        
        #self.SideFrame = Frame(self)
        #self.SideFrame.grid(row=0, column=1, padx = 1, pady=1)

        #self.ButtonFrame2 = Frame(self)
        #self.ButtonFrame2.grid(row=1, column=0, padx = 1, pady=1)
        self.colors = COLORS 
        self.months = ['January', 'February', 'March', 'April', 'May','June', 'July','August', 'September', 'October', 'November','December'
                  ]
        
        self.toolTipManager = ToolTipManager()
        self.backgroundcolor = 'white'
        self.fontcolor = 'dim gray'
        self.modeButtonWidth = 50
        self.modeButtonHeight = 50
        self.calendarModeSwitch = 1
        self.selectedCell = 'Properties'
        self.calendarCellDataDic = {}
        self.modeTitle = 'All'
        self.logoBigPath =   r'C:\Projects1\ICFFieldOffice\icons\logo.ico'

        self.selectedYear = dateStringYMD2(1)
        self.selectedMonth = 'January'
        self.wInfo = ScreenManager(self)
        self.BaseFrame = Frame(self)
        self.BaseFrame.grid(row=0, column=0, padx = 1, pady=1)
        self.calendarModeFrame = Frame(self.BaseFrame,bg=self.backgroundcolor, relief= SUNKEN, bd=5)
                                     
                                     
        
        self.calendarDetailModeFrame = Frame(self.BaseFrame,bg=self.backgroundcolor, relief= SUNKEN, bd=5)
                                     
                                         
        self.sqlGets()
        self.dataTemplates()  
        self.CalendarMode()
        #self.initiateGRID() 
        self.mainButtons()
        self.permButtons()
                       
        self.reportMode()
        
        
    def dataTemplates(self):
        self.parceltemplate = '''Property Details
Property = %s
Management Unit = %s
Acres = %s
'''                     
        self.modeTitleTemplate = '''%s Data Details for %s, %s'''
        self.dateTitleTemplate = ''
        self.imagesDataTemplate = '''Image Details
Images captured for the month = %s
Images captured for the year = %s
Total Images Captured = %s                  
'''
        self.studiesDataTemplate = '''Data Collection Details
Studies done this month = %s
Studies captured for the year = %s
Total Studies Performed = %s                  
'''                   
        self.issuesDataTemplate = '''Field Issues Recorded
Issues reported this month = %s
Issues reported for the year = %s
Total Issues Performed = %s                  
'''    


    def sqlGets(self):
        self.abcs = map(chr, range(65, 91))
        self.properties = self.abcs
        self.dataXlimit = 12
        self.dataYlimit = len(self.properties)
        self.modeButtonDic = {
                               'Grazing':self.grazingMode,
                               'Habitat':self.habitatMode, 
                               'Infrastruture':self.InfrastructureMode,
                                'Invasives':self.InvasivesMode, 
                                'Issues':self.IssuesMode,
                                 'Wetlands':self.WetlandsMode }
    
        self.permButtonDic = {'Calendar':[self.CalendarMode], 
                              'Details':[self.CalendarDetailMode], 
                              'Create Report': [self.CalendarDetailReport]
                              }
        self.previewPics = [ r'C:\Projects1\ICFFieldOffice\data\images\Copy of Los Vaqueros 001.jpg']

        self.selectedProperty = 'A'
        self.selectedPropertyMU = 'MU1' 
        self.selectedPropertyAcres = '100'
 

    def createLetters(self, num):
            num -=1
            times = int(num)/(int(len(self.abcs))) + 1
        
            remainder = int(num)%(int(len(self.abcs))) 

            letter = self.abcs[remainder]
            return letter * times

    def calendarBindings(self):
        self.Calendar.canvas.bind("<Button-1>", self.exploreCells)
        #self.Calendar.canvas.bind("<Button-3>", self.exploreCells2)

        #self.Calendar.canvas.bind('<Button-3>', lambda event: self.rollWheel(event))
        

    #def register(self, widget):
    #    self.toolTipManager.register(widget)
        
    #def unregister(self, widget):
    #    self.toolTipManager.unregister(widget)
 
    def CalendarMode(self):
        if self.calendarModeSwitch <> 0:
            self.calendarModeSwitch = 0
            self.calendarDetailModeFrame.grid_forget()
            self.calendarModeFrame.grid(row=0,column=0, sticky = W+E+N+S)
            self.calendarModeFrameMain = Frame(self.calendarModeFrame,bg=self.backgroundcolor)
            self.calendarModeFrameMain.grid(row=0,column=0,)
            
    
            self.calendarButtonFrame = CalendarSideWindow(self.calendarModeFrameMain,self.wInfo.imagecanvasWidth/6 , self.wInfo.imagecanvasHeight  )
            self.calendarButtonFrame.canvas.grid(row=0,column=0, sticky = W+E+N+S)
    
            self.calendarModeFrameMiddle = Frame(self.calendarModeFrameMain,bg=self.backgroundcolor)
            self.calendarModeFrameMiddle.grid(row=0,column=1, sticky = W+E+N+S)
            
    
            self.calendarHolderFrame= Frame(self.calendarModeFrameMiddle )
                    
            #self.Calendar = TableWindowScroll(self.calendarHolderFrame,self.wInfo.calendarCanvasWidth , self.wInfo.calendarCanvasHeight   )
            self.Calendar = CalendarWindowScroll(self.calendarHolderFrame,self.wInfo.calendarCanvasWidth , self.wInfo.calendarCanvasHeight  )
            self.calendarHolderFrame.grid(row=0,column=0)
    
            #self.calendarDataWindow = LegendWindow(self.sideCalendarFrame,self.wInfo.mapcanvasHeight* .5, self.wInfo.mapcanvasHeight *.5 )
    
    
            self.sideCalendarFrame = Frame(self.calendarModeFrameMain,bg=self.backgroundcolor)
            self.sideCalendarFrame.grid( row=0,column=2, sticky = W+E+N+S)
                     
            self.calendarImageWindow = MapImages(self.sideCalendarFrame,self.wInfo.mapcanvasHeight* .6, self.wInfo.mapcanvasHeight *.5 )
            self.calendarImageWindow.canvas.grid(row=0,column=0,sticky = W+E+N+S)
    
    
            self.calendarDataWindow = LegendWindow(self.sideCalendarFrame,self.wInfo.mapcanvasHeight *.6  , self.wInfo.mapcanvasHeight *.6  )
                                                   
    
            self.calendarDataWindow.canvas.grid(row=1,column=0, sticky = W+E+N+S)
            self.regenerateGRIDBig() 
            self.resetState()



        
    def CalendarDetailMode(self):
        if self.calendarModeSwitch <>  1:
            self.calendarModeSwitch =1
            self.calendarModeFrame.grid_forget()
            self.calendarDetailModeFrame.grid(row=0,column=0, sticky = W+E+N+S)
    
            self.calendarModeFrameMain = Frame(self.calendarDetailModeFrame,bg=self.backgroundcolor)
            self.calendarModeFrameMain.grid(row=0,column=0,)
            
    
            self.calendarButtonFrame = CalendarSideWindow(self.calendarModeFrameMain,self.wInfo.imagecanvasWidth/6 , self.wInfo.imagecanvasHeight  )
            self.calendarButtonFrame.canvas.grid(row=0,column=0, sticky = W+E+N+S)
    
            self.calendarModeFrameMiddle = Frame(self.calendarModeFrameMain,bg=self.backgroundcolor)
            self.calendarModeFrameMiddle.grid(row=0,column=1, sticky = W+E+N+S)
            
    
    
            #self.calendarDataWindow = LegendWindow(self.sideCalendarFrame,self.wInfo.mapcanvasHeight* .5, self.wInfo.mapcanvasHeight *.5 )
            self.calendarDataWindow = LegendWindow(self.calendarModeFrameMiddle,self.wInfo.calendarCanvasWidth , self.wInfo.calendarCanvasHeight  )
    
            self.calendarDataWindow.canvas.grid(row=0,column=0, sticky = W+E+N+S)
            
    
    
            self.sideCalendarFrame = Frame(self.calendarModeFrameMain,bg=self.backgroundcolor)
            self.sideCalendarFrame.grid( row=0,column=2, sticky = W+E+N+S)
                     
            self.calendarImageWindow = MapImages(self.sideCalendarFrame,self.wInfo.mapcanvasHeight* .6, self.wInfo.mapcanvasHeight *.5 )
            self.calendarImageWindow.canvas.grid(row=0,column=0,sticky = W+E+N+S)
    
            self.calendarHolderFrame= Frame(self.sideCalendarFrame )
                    
            #self.Calendar = TableWindowScroll(self.calendarHolderFrame,self.wInfo.calendarCanvasWidth , self.wInfo.calendarCanvasHeight   )
            self.Calendar = CalendarWindowScroll(self.calendarHolderFrame,self.wInfo.mapcanvasHeight *.6  , self.wInfo.mapcanvasHeight *.6  )
            
            self.calendarHolderFrame.grid(row=1,column=0)

            self.regenerateGRIDsmall() 
            self.resetState()
    def resetState(self):
            
            self.mainButtons()
            self.permButtons()
            self.calendarBindings()
            self.reportMode()
               
    def regenerateGRIDBig(self):
            self.Calendar.canvas.delete('all')
            x= 0
        
            COUNTER = 0
            width = 150
            length = 150
            
            while COUNTER <= len(self.months):
                x1 = x + width
                y = 0 
                z = 0
                COUNTERY = 0
                while COUNTERY <= self.dataYlimit:
                    y1 = y + length

                    corners = [x,y,x,y1,x1,y1,x1,y]
                    poly = self.generateTaggedPoly(COUNTER,COUNTERY,corners)
                    y +=length
                    z += 1
                    COUNTERY +=1
                x += width
                COUNTER += 1
                self.Calendar.canvas.config(scrollregion=(0, 0, x+1, y))
            self.labelMonths(width,length)
 
    def generateTaggedPoly(self, COUNTER,COUNTERY, corners):
            cell = "%d/%d" % (COUNTER, COUNTERY)
            print cell
            if COUNTER != 0 and COUNTERY !=0:
                type = 'data'
            elif COUNTER != 0 and COUNTERY ==0:
                type = 'header'
            elif COUNTERY != 0 and COUNTER ==0:
                type = 'header'
            else:
                
                type = 'year'
            
            poly = self.Calendar.canvas.create_polygon(corners,  activeoutline='red',fill='white', outline='black',activewidth= 2, tags= (type,cell ))
            return poly       
            
            
    def regenerateGRIDsmall(self):
            self.Calendar.canvas.delete('all')
            x= 0
        
            COUNTER = 0
            width = 75
            length = 75
            
            while COUNTER <= len(self.months):
                x1 = x + width
                y = 0 
                z = 0
                COUNTERY = 0
                while COUNTERY <= self.dataYlimit:
                    y1 = y + length

                    corners = [x,y,x,y1,x1,y1,x1,y]
                    poly = self.generateTaggedPoly(COUNTER,COUNTERY,corners)

                    y +=length
                    z += 1
                    COUNTERY +=1
                x += width
                COUNTER += 1
                self.Calendar.canvas.config(scrollregion=(0, 0, x+1, y))
            self.labelMonths(width,length)
 
    def labelMonths(self,width,length): 
            for COUNTER, month in enumerate(self.months):
                self.Calendar.canvas.create_text((width * (COUNTER +1)) + width/2, 25, text = str(self.months[COUNTER][:3]), tags =(self.months[COUNTER],'xHeader'))
 

            for COUNTER, property in enumerate(self.properties):

                    self.Calendar.canvas.create_text(width/2, ((COUNTER+1)* length) + length/2, text = str('Prop. ' + property), tags= (property,'yHeader') ) 
            
            self.Calendar.canvas.create_text(width/2, length/2, text = str(self.selectedYear), tags= (property,'yHeader') ) 


    def mainButtons(self):
        self.calendarButtonFrame.canvas.delete('mode')
        #self.calendarButtonFrame.canvas.delete('all')
        

        for COUNTER, mode in enumerate(self.modeButtonDic):
            execute = self.modeButtonDic[mode]
            photo = PhotoImage(file = r'C:\Projects1\ICFFieldOffice\icons\png\Left.gif')
            button = Button(background='#FFFFFF',width = self.modeButtonWidth , height = self.modeButtonHeight , image = photo, bd=3,relief='raised' ,command=execute)
            button.image = photo
            self.calendarButtonFrame.canvas.create_window(self.modeButtonWidth/4  ,self.modeButtonHeight * (COUNTER) + (self.modeButtonHeight * 1.7) ,window=button,anchor="w", tags=('mode'))
            self.calendarButtonFrame.canvas.create_text(self.modeButtonWidth/4 + (self.modeButtonWidth * 1.3)  ,self.modeButtonHeight * (COUNTER) + (self.modeButtonHeight * 1.7) ,text=mode,anchor="w", tags=('mode'))
            self.toolTipManager.register(button, mode)
    def permButtons(self): 
        self.calendarButtonFrame.canvas.delete('perm')       
        for COUNTER, perm in enumerate(self.permButtonDic):
            execute = self.permButtonDic[perm][0]
            photo = PhotoImage(file = r'C:\Projects1\ICFFieldOffice\icons\png\Right.gif')
            button = Button(background='#FFFFFF',width = self.modeButtonWidth , height = self.modeButtonHeight , image = photo, bd=3,relief='raised',command=execute)
            button.image = photo
            self.calendarButtonFrame.canvas.create_window( self.modeButtonWidth/4 ,self.calendarButtonFrame.heightIMap -  (self.modeButtonHeight * (COUNTER+1)) ,window=button,anchor="w", tags=('perm'))
            self.calendarButtonFrame.canvas.create_text(self.modeButtonWidth/4 + (self.modeButtonWidth * 1.3)  ,self.calendarButtonFrame.heightIMap -  (self.modeButtonHeight * (COUNTER+1)) ,text=perm,anchor="w",  tags=('perm'))
            self.toolTipManager.register(button, perm)
        
    def dateTemplateLoad(self):
        pass
        

    def loadImage(self):
        self.calendarImageWindow.canvas.delete('all')
        #self.imageBigPicturePreviewButtons()
        

        widSmall = (self.calendarImageWindow.widthmap)/5
        widBig = ((self.calendarImageWindow.widthmap)/5 ) * 4
        self.setOfPreviewImagesDic = {}
        
        self.imageCOUNTER = 0
        self.setOfPreviewImages = []
        for COUNTER,pic in enumerate(self.previewPics):
            
            picImageBig = ImageProcessorPreview(pic,self.wInfo)
            self.setOfPreviewImages.append(picImageBig)


  
        self.picImage = self.setOfPreviewImages[0]#ImageProcessor3(r'C:\CCWD\pics\Los Vaqueros 003.jpg', self.wInfo)    
        self.imageModeWidth  = self.calendarImageWindow.widthmap - self.picImage.screenImageWidth
        self.calendarImageWindow.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tag='pic')
    
    def loadLogo(self):
        self.calendarDataWindow.canvas.delete('pic')

        self.logoImageBig = ImageProcessor5(self.logoBigPath)


  
        self.dataModeLogoWidth  = self.calendarDataWindow.widthIMap
        self.calendarDataWindow.canvas.create_image(self.dataModeLogoWidth,0 , image= self.logoImageBig.jpgPI, anchor="ne",tag='logo')
            


    def selectSQL(self):
        sql = "SELECT * FROM %s" % self.selectedCell
        self.cursorspatial = curspatial()
        self.cursorspatial.execute(columns)
        cols = self.cursorspatial.fetchall()
        
        
        
        self.cursorspatial.execute(sql)
        self.loadvals = self.cursorspatial.fetchall()
        del self.cursorspatial
        self.loadVals()
        #sql = '''SELECT name FROM sqlite_master WHERE type='table'  ORDER BY name'''
        #sql = '''SELECT * FROM %s''' % self.selectedTable
        #self.cursorspatial = curspatial()
        #self.cursorspatial.execute(sql)
        #self.calendarsTableMode = self.cursorspatial.fetchall()
        


    def rollWheel(self,event):
        direction = 0
        if event.num == 5 or event.delta == -120:
            direction = 1
        if event.num == 4 or event.delta == 120:
            direction = -1
        event.widget.yview_scroll(direction, UNITS)


    def exploreCells(self, event):
        self.calendarDataWindow.canvas.delete('event')
 
        canvas = event.widget
        
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)

        closest = canvas.find_closest(x,y)
        coords =  canvas.coords(closest) #create_text(self.calendarDataWindow.widthIMap/2 - 10, 200, text = xy, tags= ('event'))
        tags =  canvas.gettags(closest)
        print tags, closest
        if 'data' in tags:
            splittag = tags[1].split('/')
            monthid = int(splittag[0])-1
            propid =int(splittag[1])-1
            self.selectedMonth = self.months[monthid]
            
            self.selectedProperty = self.properties[propid]
            
            
            #self.calendarDataWindow.canvas.create_text(self.calendarDataWindow.widthIMap/2 - 10, 200, text = month, tags= ('event'))
            self.reportMode()
            
    def exploreCells2(self, event):
        self.calendarDataWindow.canvas.delete('event')
 
        canvas = event.widget
        
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        xy  = '%d %d' % (x,y)
        canvas.itemconfig(CURRENT, fill="white")
        self.calendarDataWindow.canvas.create_text(self.calendarDataWindow.widthIMap/2 - 10, 200, text = xy, tags= ('event'))
        
    
    def grazingMode(self):
        self.modeTitle = 'Grazing'
        self.reportMode()
        
    def habitatMode(self):
        self.modeTitle = 'Habitat'
        self.reportMode()        
        
    def InfrastructureMode(self):
        self.modeTitle = 'Infrastructure'
        self.reportMode()

    def InvasivesMode(self):
        self.modeTitle = 'Invasives'
        self.reportMode()        

    def IssuesMode(self):
        self.modeTitle = 'Issues'
        self.reportMode() 

    def WetlandsMode(self):
        self.modeTitle = 'Wetlands'
        self.reportMode()        

    def CalendarDetailReport(self):
        import time
        from reportlab.lib.enums import TA_JUSTIFY
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
         
        doc = SimpleDocTemplate("Report.pdf",pagesize=letter,
                                rightMargin=72,leftMargin=72,
                                topMargin=72,bottomMargin=18)
        Story=[]
        logo = self.logoPath

         
        formatted_time = time.ctime()

         
        im = Image(logo, 2*inch, 2*inch)
        Story.append(im)
         
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>%s</font>' % formatted_time
         
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        
        title = self.modeTitleTemplate % (self.modeTitle, self.selectedMonth, self.selectedYear) 
        ptext = '<font size=12>%s</font>' % title
        Story.append(Paragraph(ptext, styles["Normal"]))       
   
         
        Story.append(Spacer(1, 12))
        
        propertyinfo = self.parceltemplate % (self.selectedProperty,self.selectedPropertyMU, self.selectedPropertyAcres )        

        ptext = '<font size=12>%s</font>' % propertyinfo
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
         
        imagesinfo = self.imagesDataTemplate % ('10','20','30')        
        ptext = '<font size=12>%s</font>' % imagesinfo
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))

        image = self.previewPics[0]
        im = Image(image, 2*inch, 2*inch)
        Story.append(im)
        doc.build(Story)
        os.startfile('Report.pdf')
        
    def reportMode(self):
        self.calendarDataWindow.canvas.delete('all')
        
        if self.calendarModeSwitch == 0:
            fontsize = '9'
            title = self.modeTitleTemplate % (self.modeTitle, self.selectedMonth, self.selectedYear)
            self.calendarDataWindow.canvas.create_text(10, 15, text = title, font = ('Helvetica', fontsize, 'bold'), anchor='nw')
    
            propertyinfo = self.parceltemplate % (self.selectedProperty,self.selectedPropertyMU, self.selectedPropertyAcres )        
            self.calendarDataWindow.canvas.create_text(10, 100, text = propertyinfo, font = ('Helvetica', fontsize, ), anchor='nw')
            
    
            imagesinfo = self.imagesDataTemplate % ('10','20','30')        
            self.calendarDataWindow.canvas.create_text(10, 200, text = imagesinfo, font = ('Helvetica', fontsize, ), anchor='nw')
            
        elif self.calendarModeSwitch == 1:
            fontsize = '12'
            title = self.modeTitleTemplate % (self.modeTitle, self.selectedMonth, self.selectedYear)
            self.calendarDataWindow.canvas.create_text(10, 15, text = title, font = ('Helvetica', fontsize, 'bold'), anchor='nw')
    
            propertyinfo = self.parceltemplate % (self.selectedProperty,self.selectedPropertyMU, self.selectedPropertyAcres )        
            self.calendarDataWindow.canvas.create_text(10, 100, text = propertyinfo, font = ('Helvetica', fontsize, ), anchor='nw')
            
    
            imagesinfo = self.imagesDataTemplate % ('10','20','30')        
            self.calendarDataWindow.canvas.create_text(10, 200, text = imagesinfo, font = ('Helvetica', fontsize, ), anchor='nw')
            
        
        
        self.loadImage()
        self.loadLogo()
        #self.calendarDataWindow.canvas.create_text(self.calendarDataWindow.widthIMap/2 - 10, 10, text = self.modeTitleTemplate % self.modeTitle)
        
           