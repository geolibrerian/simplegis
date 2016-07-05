from LMS_DATA_MODELS.AccessModels import * 
from LMS_DATA_MODELS.models import *
from LMS_DATA_MODELS.views import *
from Tkinter import *
from workers import *
import os, random

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
import os
class LMS(Frame):
    def __init__(self,Master=None,**kw):
        
        apply(Frame.__init__,(self,Master),kw)


        self.reportPath = 'C:\\CCWD'
        self.logoPath = 'C:\\CCWD\\ogo.ico'
        self.menubar = Menu(Master,tearoff=1)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.ButtonAddData)
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=Master.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_separator()
        
        mapsmenu = Menu(self.menubar, tearoff=0)
        mapsmenu.add_command(label="Maps", command=self.ButtonMap)
        mapsmenu.add_command(label="Graphs",command=self.ButtonMakeGraph)
        mapsmenu.add_command(label="Pictures",command=self.ButtonImage )
        mapsmenu.add_command(label="SQL Queries",command=self.ButtonExtractData )
        mapsmenu.add_command(label="Data Tables",command=self.ButtonTables )

        self.menubar.add_cascade(label="Mode", menu=mapsmenu)        

        mapsmenu = Menu(self.menubar, tearoff=0)
        mapsmenu.add_command(label="Issues", command=self.issueReport)
        mapsmenu.add_command(label="Wetlands",command=self.wetlandsReport)
        mapsmenu.add_command(label="Grazing",command = self.grazingReport)
        mapsmenu.add_command(label="Habitat",command=self.habitatReport)
        mapsmenu.add_command(label="Invasive Species",command=self.iSpeciesReport)
        mapsmenu.add_command(label="Any Data",command=self.orderedDialogue )

        self.menubar.add_cascade(label="Queries", menu=mapsmenu)

        mapsmenu = Menu(self.menubar, tearoff=0)
        mapsmenu.add_command(label="Wetlands",)#command=self.grazedAreaMapEditing)
        mapsmenu.add_command(label="Grazing",)#command=self.habitatMapEditing)
        mapsmenu.add_command(label="Invasive Species",)#command=self.wetlandsMapEditing)
        mapsmenu.add_command(label="Species Habitat",)#command=self.invasiveSpeciesMapEditing)
        self.menubar.add_cascade(label="Studies", menu=mapsmenu)

        mapsmenu = Menu(self.menubar, tearoff=0)
        mapsmenu.add_command(label="Issues",command = self.getQuickReport)
        mapsmenu.add_command(label="Grazing",)#command=self.habitatMapEditing)
        mapsmenu.add_command(label="Close Issues",command=self.closeIssues)
        self.menubar.add_cascade(label="Report An Occurrence", menu=mapsmenu)

        mapsmenu = Menu(self.menubar, tearoff=0)
        mapsmenu.add_command(label="Pan Up", command=self.ButtonPanUp)
        mapsmenu.add_command(label="Pan Down",command=self.ButtonPanDown)
        mapsmenu.add_command(label="Pan Left",command=self.ButtonPanLeft)
        mapsmenu.add_command(label="Pan Right",command=self.ButtonPanRight)
        mapsmenu.add_command(label="Zoom In",command=self.ButtonZoomIn)
        mapsmenu.add_command(label="Zoom Out",command=self.ButtonZoomOut)

        self.menubar.add_cascade(label="Map Controls", menu=mapsmenu)
        mapsmenu = Menu(self.menubar, tearoff=0)


        mapsmenu.add_command(label="Shapefile",command = self.createSHP)
        mapsmenu.add_command(label="KML", command=self.outputPicKML)
        mapsmenu.add_command(label="Spreadsheet",command=self.selectSpreadSheet)
        mapsmenu.add_command(label="Images",command=self.pdfProxy)
        self.menubar.add_cascade(label="Export Data", menu=mapsmenu)


        self.master.config(menu=self.menubar)        
        

        self.BaseFrame = Frame(self)
        self.BaseFrame.grid(row=0, column=0, padx = 1, pady=1)
        #self.SideFrame = Frame(self)
        #self.SideFrame.grid(row=0, column=1, padx = 1, pady=1)
        self.ButtonFrame = Frame(self)
        self.ButtonFrame.grid(row=2, column=0, padx = 1, pady=1)
        #self.ButtonFrame2 = Frame(self)
        #self.ButtonFrame2.grid(row=1, column=0, padx = 1, pady=1)
        self.colors = COLORS #[   "red", "green", "blue", "cyan", "yellow",  'grey', 'light blue', 'dark red','dark green', 'dark blue', 'sky blue', 'tan' ]
        self.ModelMap = {Wetlands.namestring: Wetlands, 
                         LandCover.namestring:LandCover,
                         HabitatManagementObjectives.namestring:HabitatManagementObjectives,
                         InvasiveSpecies.namestring:InvasiveSpecies,
                         GrazedAreas.namestring: GrazedAreas
                         }
        self.initialize()

    
    def randcolor(self):
        return random.randint(0,len(self.colors)-1)

    def initialize(self):
        self.wInfo = ScreenManager(self)
        self.chartSwitch = 0
        self.mainMap()
        self.canvasList = []
        self.imageLibrary = r'C:\ParcelViewer\Images'
        self.upper = 568000.0, 4219459.0
        self.lower = 640000.0, 4168776.1428571427
        self.upper = 550000.0, 4220000.0
        
        self.lower = self.upper[0] + (100000.0 * (self.wInfo.mapcanvasWidth/self.wInfo.mapcanvasHeight))  , self.upper[1] - 100000.0 
        self.switches()
        
        self.home()
        self.iGrid = ImageGrid()
        self.iManager = ImageManager()
        self.Scale()

        self.GraphExplore()
        self.buttonHeight = self.wInfo.buttonSize
        self.buttonWidth = self.wInfo.buttonSize
        self.allButtons()
        self.grid_columnconfigure(0,weight=1)
        #self.imageArrange()
        self.dataconnect()
        self.regenerate()
        self.wInfo.mapcanvasHeight,self.wInfo.mapcanvasWidth
        
        
        self.mapModeLegendCheck()
        self.PictureExplore()
        
    def switches(self):
        self.graphset = 0
        self.mapSwitch  = 1
        
        self.chartmode = 0
        self.sqlSwitch = 0
        self.imageModeSwitch = 0
        self.tableModeSwitch = 0

        self.picCounter = 0
        self.backgroundcolor = 'dim gray'
        



    def mainMap(self):
        self.mainMapFrame =Frame(self.BaseFrame)
        self.mainMapFrame.grid(row=0,column=0)
        self.mapHolderFrame= Frame(self.mainMapFrame )
        self.mapHolderFrame.grid(row=0, column=1,columnspan=2,rowspan=2, padx = 1)
        self.mainMapWindow = Map(self.mapHolderFrame, self.wInfo.mapcanvasWidth, self.wInfo.mapcanvasHeight)
        self.picHolderFrame= Frame(self.mainMapFrame )
        self.picHolderFrame.grid(row=0, column=3, padx = 10,pady = 5)        
        self.mainpicWindow = PictureWindow(self.picHolderFrame,  self.wInfo.sideWidths,self.wInfo.picCanvasHeight)
        self.graphHolderFrame= Frame(self.mainMapFrame )
         
        self.maingraph = Graph(self.graphHolderFrame,  self.wInfo.sideWidths, self.wInfo.graphCanvasHeight)
        self.maingraph.canvas.grid(row=0,column=0)
        self.mapLegendFrame = Frame(self.mainMapFrame,width= self.wInfo.mapbuttonFrameWidth, height=self.wInfo.mapbuttonFrameHeight)
        self.mapLegendFrame.grid(row=0, column=0, padx = 1)
        self.mainLegend = LegendWindow(self.mapLegendFrame ,  self.wInfo.mapcanvaslegendWidth, self.wInfo.mapcanvaslegendHeight)
        self.mapButtons = Frame(self.mainMapFrame,width= self.wInfo.mapbuttonFrameWidth, height=self.wInfo.mapbuttonFrameHeight)
        self.Map(self.mainMapWindow,self.mainLegend,self.mapButtons, self.mainpicWindow, self.maingraph)

    def Map(self, mapObject,legendObject, buttonsObject, picWindowObject, graphObject):
        legendScrollbar = Scrollbar(self.mapLegendFrame)
        legendScrollbar.pack(side=LEFT, fill=Y)
        
        
        self.legend = legendObject
        self.legend.canvas.pack(side=RIGHT)#grid(row=0, column=1, padx = 1)
        self.legend.canvas.bind("<Double-Button-3>", self.ColorChoserProxy)
        #self.legend.canvas.bind("<Double-Button-1>", self.detailPolys)
        self.legend.canvas.bind("<Double-Button-1>", self.legendCoordCalc)
        legendScrollbar.config(command=self.legend.canvas.yview)
        
        
        self.mapButtonsFrame = buttonsObject
        self.mapButtonsFrame.grid(row=1, column=0,rowspan=1, padx = 1)
                
        self.map = mapObject
        #self.map.frame.grid(row=0, column=1,columnspan=2,rowspan=2, padx = 1)
        def xView(x,y,z):
            if int(y) ==1:
                    self.ButtonPanRight()
            elif int(y)==-1:
                self.ButtonPanLeft()
                
        def yView(x,y,z):
            if int(y) ==-1:
                    self.ButtonPanUp()
            elif int(y)==1:
                self.ButtonPanDown()

        self.map.scrollbarX.config(command=xView)
        self.map.scrollbarY.config(command=yView)
        
        self.map.canvas.bind("<Double-Button-1>", self.ZoomInMode)
        self.map.canvas.bind("<Double-Button-3>", self.ZoomOutMode)
        self.map.canvas.bind('Up',self.ButtonPanUp)
        self.map.canvas.bind('<Left>',self.ButtonPanLeft)
        self.map.canvas.bind('<Right>',self.ButtonPanRight)
        self.map.canvas.bind('<Down>',self.ButtonPanDown)  
        sidewindows = 3
        self.picWindow = picWindowObject
        #self.picWindow.canvas.grid(row=0, column=sidewindows, padx = 10,pady = 5)
        
        self.graph = graphObject
        self.graphHolderFrame.grid(row=1,column=3, padx=10,pady = 5)  

    def mapModeLegendCheck(self):
        self.legend.canvas.delete("all")
        
        self.canvasList.reverse()
        for COUNTER, legendObject in enumerate(self.canvasList):
            legendObject.legendDataToScreen(COUNTER)
    
    def legendCoordCalc(self, event):
        x = event.x
        y = event.y
        
        for COUNTER, legendObject in enumerate(self.canvasList):
            for dataset in legendObject.dataset:
                data = legendObject.dataset[dataset]
                rect = data["legendObject"]
                
                x1 = rect[0]
                y1 = rect[1]
                x2 = rect[2]+100
                y2 = rect[3]
                if x in range(x1,x2) and y in range(y1, y2):
                    legendObject.alllegendDataToScreen()             

    def detailPolys(self,event):
        y = event.y
        for COUNTER,legendval in enumerate(self.legendSet):
            if COUNTER != len(self.legendSet)-1:
                legendnext = self.legendSet
                if y >= legendval and y <= legendnext:
                    self.legend.canvas.delete("all")
                    color = self.colors[self.randcolor()]
                    geoObjectResults = self.geoList[COUNTER][0]
                    for polyObject in geoObjectResults:

                        x1= 10 
                        x2= x1 + 30
                        y1= (COUNTER+1) * 50
                        y2= y1+30
                        self.legend.canvas.create_rectangle(x1,y1,x2,y2,outline="black",fill=color, activeoutline="red", activewidth=2.0)
                        
                        self.legend.canvas.create_text(x1+35,y1+5,text=geoObjectResults[1].namestring,anchor="nw")
                    #self.legend.canvas.bind("<Double-Button-3>", self.ColorChoserProxy)
                    self.legend.canvas.bind("<Double-Button-1>", self.mapModeLegendCheck)

    def ImageMode(self):
        

        self.imageModeFrame = Frame(self.BaseFrame,bg=self.backgroundcolor, 
                                     
                                     relief=SUNKEN, bd=2)
        self.imageModeFrame.grid(row=0,column=0, sticky = W+E+N+S)

        self.imageModeFrameMain = Frame(self.imageModeFrame,bg=self.backgroundcolor)
        self.imageModeFrameMain.grid(row=0,column=1, rowspan=4,columnspan=6)

        self.imageModeFrameMid = Frame(self.imageModeFrameMain,bg=self.backgroundcolor, relief=SUNKEN, bd=2)
        self.imageModeFrameMid.grid(row=0,column=1)
        self.bigPicture = ImageWindow(self.imageModeFrameMid,self.wInfo.imagecanvasWidth , self.wInfo.imagecanvasHeight  )
        self.bigPicture.canvas.grid(row=0,column=0,rowspan=5,columnspan=6, sticky = W+E+N+S)

        self.bigPicture.canvas.bind("<Button-1>", self.imageModeZoomIn )
        self.bigPicture.canvas.bind("<Button-3>", self.imageModeZoomOut )

        self.imageModeFrameSide= Frame(self.imageModeFrameMain,bg=self.backgroundcolor)
        self.imageModeFrameSide.grid(row=0,column=0, rowspan=4)

        self.sidePicture = ImageWindow(self.imageModeFrameSide,self.wInfo.imagecanvasWidth/5 , self.wInfo.imagecanvasHeight  )
        self.sidePicture.canvas.grid(row=0,column=0,rowspan=4, sticky = W+E+N+S)
        self.sidePicture.canvas.bind("<Button-1>", self.imageLoadFromClick )
        self.imageModeFrameBottom = Frame(self.imageModeFrame,bg=self.backgroundcolor, 
                                     
                                     relief=RAISED, bd=2)
        self.imageModeFrameBottom.grid(row=4,column=0, rowspan=2,columnspan=7)


        picture_sql = "select * from Pictures"

        self.cursor.execute(picture_sql)
        self.picIDs = self.cursor.fetchall()



        self.picImage = ImageProcessor3(self.picIDs[self.picCounter][2], self.wInfo)    
        self.imageModeWidth  = self.wInfo.imagecanvasWidth - self.picImage.screenImageWidth
        placement = self.picImage.screenImageWidth +  20
        self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw")
        #self.imageModeImageGridObject = get_PointInPoly(ImageGrid, self.picImage.long, self.picImage.lat)

        

        self.imageModeGridSQL()
        width1 = 100
        height1= 50
        photo = PhotoImage(file = r'C:\district\png\Up.gif')
        self.imageButtonUp =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.imageThumbsDown)
        self.imageButtonUp.image = photo
        self.imageButtonUp.grid(row=0, column=0)
        photo = PhotoImage(file = r'C:\district\png\Down.gif')
        self.imageButtonDown = Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.imageThumbsUp)
        self.imageButtonDown.image = photo
        self.imageButtonDown.grid(row=0, column=1)
        #photo = PhotoImage(file = r'C:\district\png\Camera.gif')
        #self.sidePicture.canvas.create_window(1,1,window=self.imageButtonUp,anchor="nw")
        #self.sidePicture.canvas.create_window(1,101,window=self.imageButtonDown,anchor="nw")        
        
        photo = PhotoImage(file = r'C:\district\png\Left.gif')
        self.imageButtonBack =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.lastImage)
        self.imageButtonBack.image = photo
        self.imageButtonBack.grid(row=0, column=2)
        photo = PhotoImage(file = r'C:\district\png\Print.gif')
        self.imageButtonPrint =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.printImageToPDF)
        self.imageButtonPrint.image = photo
        self.imageButtonPrint.grid(row=0, column=3)
        photo = PhotoImage(file = r'C:\district\png\Binocular.gif')
        self.imageButtonPrint =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.outputPicKML)
        self.imageButtonPrint.image = photo
        self.imageButtonPrint.grid(row=0, column=4)
        photo = PhotoImage(file = r'C:\district\png\Right.gif')
        self.imageButtonNext =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.nextImage)
        self.imageButtonNext.image = photo
        self.imageButtonNext.grid(row=0, column=5)
        photo = PhotoImage(file = r'C:\district\png\MagnifyPlus.gif')
        self.imageButtonPrint =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.outputPicKML)
        self.imageButtonPrint.image = photo
        self.imageButtonPrint.grid(row=0, column=6)
        photo = PhotoImage(file = r'C:\district\png\MagnifyMinus.gif')
        self.imageButtonNext =  Button(self.imageModeFrameBottom,background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.nextImage)
        self.imageButtonNext.image = photo
        self.imageButtonNext.grid(row=0, column=7) 
               
        self.thumbImageList = []
        self.thumbImageList2 = []

        self.sidePicCoordList = []
        self.sideImagePathList = []
        self.imageModeDataList = [self.picImage.filename, "Latitude = %s" % self.picImage.lat, "Longitude = %s" % self.picImage.long,  ]
        self.thumbMoveVal = 100
        wid = self.sidePicture.widthIMap
        
#        for COUNTER,pic in enumerate(self.picIDs):
#            
#            #val = 'thumb%d' % COUNTER
#            #print val
#            #self.val = ImageProcessor4(pic[2],wid)
#            #print self.val.screenMapImageWidth,self.val.screenMapImageHeight
#            #print dir(self.val)
#            exec "self.thumb%d = ImageProcessor4(pic[2],wid)" % COUNTER
#            exec 'val = self.thumb%d ' % COUNTER
#            
#            #self.add_property( "thumb%d" % COUNTER, lambda self: ImageProcessor4(pic[2],wid))
#            #exec 'val = self.thumb%d ' % COUNTER
#            #val = 'thumb%d' % COUNTER
#            #exec 'val = iProcess.thumb%d ' % COUNTER
##            yvalue = int(COUNTER * self.val.screenMapImageHeight + 10 )
##            nextyvalue = int((COUNTER +1) * self.val.screenMapImageHeight + 10 )
##            rangeval = (yvalue, nextyvalue)
##            self.sidePicCoordList.append(rangeval)
##            self.sideImagePathList.append(pic[2])
##            thumb = self.sidePicture.canvas.create_image( 10,yvalue, image= self.val.jpgPI, anchor="nw", tags=self.picIDs[COUNTER][2])
#            yvalue = int(COUNTER * val.screenMapImageHeight + 10 )
#            nextyvalue = int((COUNTER +1) * val.screenMapImageHeight + 10 )
#            rangeval = (yvalue, nextyvalue)
#            self.sidePicCoordList.append(rangeval)
#            self.sideImagePathList.append(pic[2])
#            thumb = self.sidePicture.canvas.create_image( 10,yvalue, image= val.jpgPI, anchor="nw", tags=self.picIDs[COUNTER][2])
#                        
#            self.thumbImageList.append(thumb)
        for COUNTER,pic in enumerate(self.picIDs):

            thumb = ImageProcessor4(pic[2],wid)
            self.thumbImageList2.append(thumb)
            
        for COUNTER,val in enumerate(self.thumbImageList2):
            yvalue = int(COUNTER * val.screenMapImageHeight + 10 )
            nextyvalue = int((COUNTER +1) * val.screenMapImageHeight + 10 )
            rangeval = (yvalue, nextyvalue)
            self.sidePicCoordList.append(rangeval)
            self.sideImagePathList.append(pic[2])
            thumb = self.sidePicture.canvas.create_image( 10,yvalue, image= val.jpgPI, anchor="nw", tags=self.picIDs[COUNTER][2])
                        
            self.thumbImageList.append(thumb)
        self.sideImageFrame = Frame(self.imageModeFrameMain,bg=self.backgroundcolor)
        self.sideImageFrame.grid( row=0,column=7, rowspan=6, columnspan=3)
        
        self.imageMapWindow = Map(self.sideImageFrame,self.wInfo.mapcanvasHeight* .5, self.wInfo.mapcanvasHeight *.5  )
        self.imageMapWindow.canvas.grid(row=0,column=0, rowspan=2, columnspan=3)
        filename  = self.imageLibrary + '\\' +  self.imageModeImageGridName[0] + '.jpg'
        self.imageModeMap = ImageProcessor2(filename, 1, self.wInfo)  
                    
        self.imageModeMap = ImageProcessor2(filename, 1, self.wInfo)  
        self.imageMapWindow.canvas.create_image(1,1, image= self.imageModeMap.jpgPI, anchor="nw")
        
        self.imageDataWindow = LegendWindow(self.sideImageFrame,self.wInfo.mapcanvasHeight* .5, self.wInfo.mapcanvasHeight *.5  )
        self.imageDataWindow.canvas.grid(row=2,column=0, rowspan=2, columnspan=3)
        self.imageDataWindowLoad()
        
    def imageModeZoomIn(self,event):
        x= event.x
        y = event.y


        scaleX = 1.0 
        scaleY = scaleX
        self.bigPicture.canvas.scale("all",x, y, scaleX, scaleY)            

    def imageModeZoomOut(self, event):
        x= event.x
        y = event.y


        scaleX = .5 # 1.0/self.zoomer.currentZoom
        scaleY = scaleX #* (self.wInfo.mapcanvasHeight/self.wInfo.mapcanvasWidth)
        self.bigPicture.canvas.scale("all",x, y, scaleX, scaleY)


    def add_property(self, name, func):
        setattr(self.__class__, name, property(func))    
            
    def printImageToPDF(self):

        imagePDF2([self.picImage.filename])
        pdf = savePDF()
        imagePDF3(os.path.dirname(self.picImage.filename), pdf)
        os.startfile(pdf)
        
    def imageDataWindowLoad(self):
        self.imageDataWindow.canvas.delete("all")
        for COUNTER, textval in enumerate(self.imageModeDataList):
            
            self.imageDataWindow.canvas.create_text(10,COUNTER * 15 + 25, text= textval,anchor="nw")
            
    def imageLoadFromClick(self, event):
            y = event.y

            for COUNTER, ranges in enumerate(self.sidePicCoordList):
                
                min1, max1 = min(ranges) + self.thumbMoveVal, max(ranges) + self.thumbMoveVal
                
                if y in range(min1, max1):
                    
                    self.bigPicture.canvas.delete("all")
                    self.picImage = ImageProcessor3(self.thumbImageList2[COUNTER].filename , self.wInfo)
                    #self.imageModeImageGridObject = get_PointInPoly(ImageGrid, self.picImage.long, self.picImage.lat)
                    self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw")
                    
                    self.imageModeDataList = [self.picImage.filename, "Latitude = %s" % self.picImage.lat, "Longitude = %s" % self.picImage.long,  ]

                    self.imageModeGridSQL()
                    self.imageMapWindow.canvas.delete("all")
                    filename  = self.imageLibrary + '\\' +  self.imageModeImageGridName[0] + '.jpg'
                    self.imageModeMap = ImageProcessor2(filename, 1, self.wInfo)  
                    
                    self.imageMapWindow.canvas.create_image(1,1, image= self.imageModeMap.jpgPI, anchor="nw")                    
                    self.imageDataWindowLoad()
                    
    def imageModeGridSQL(self):
        self.cursorspatial = curspatial()
        #sql = "SELECT sheetName FROM LMS_DATA_MODELS_imagegrid WHERE Within(Transform(GeomFromText('POINT(%s %s)', 4326),2227),LMS_DATA_MODELS_imagegrid.Geometry)" % (self.picImage.long, self.picImage.lat)
        sql = "SELECT sheetName FROM LMS_DATA_MODELS_imagegrid WHERE Within(GeomFromText('POINT(%s %s)', 2227),LMS_DATA_MODELS_imagegrid.Geometry)" % (self.zoomer.centroid[0],self.zoomer.centroid[1]) #(self.picImage.long, self.picImage.lat)
        #sql = "SELECT sheetName FROM LMS_DATA_MODELS_imagegrid WHERE Within(GeomFromText('%s',2227),LMS_DATA_MODELS_imagegrid.Geometry)" 
        
        
        #transql = "select AsText(Transform(GeomFromText('POINT(%s %s)',4326),2227))" % (self.picImage.long, self.picImage.lat)
        
        #self.cursorspatial.execute(transql)
        #XY =  self.cursorspatial.fetchone()[0] 
  
        self.cursorspatial.execute(sql)
        self.imageModeImageGridName = self.cursorspatial.fetchone()
        
        del self.cursorspatial  
    
    def imageThumbsUp(self):
        if self.thumbMoveVal > -(self.sidePicCoordList[-1][1] -100):
            for thumb in self.thumbImageList:
                
                self.sidePicture.canvas.move(thumb,0, -100 )
            
            self.thumbMoveVal -= 100
            
            
    def imageThumbsDown(self):

        if  self.thumbMoveVal <=0: # (self.sidePicCoordList[-1][1] +100) :
            #if self.thumbMoveVal <=100:
                for thumb in self.thumbImageList:
                
                    self.sidePicture.canvas.move(thumb,0, 100 )
                self.thumbMoveVal += 100

            

    def nextImage(self):
        
        if self.picCounter < (len(self.picIDs)-1):
            self.picCounter += 1
            self.picImage = ImageProcessor3(self.picIDs[self.picCounter][2], self.wInfo)    
        else:
            self.picCounter = 0
            self.picImage = ImageProcessor3(self.picIDs[self.picCounter][2], self.wInfo)
        self.bigPicture.canvas.delete("all")  
        self.imageModeDataList = [self.picImage.filename, "Latitude = %s" % self.picImage.lat, "Longitude = %s" % self.picImage.long,  ]

        #self.imageModeImageGridObject = get_PointInPoly(ImageGrid, self.picImage.long, self.picImage.lat) 
        self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw")
        self.imageModeGridSQL() 
        self.imageDataWindowLoad()
        
    def lastImage(self):
        if self.picCounter > 0:
            self.picCounter -= 1
            self.picImage = ImageProcessor3(self.picIDs[self.picCounter][2], self.wInfo)    
        else:
            self.picCounter = 0
            self.picImage = ImageProcessor3(self.picIDs[self.picCounter][2], self.wInfo)
        self.bigPicture.canvas.delete("all")
        self.imageModeDataList = [self.picImage.filename, "Latitude = %s" % self.picImage.lat, "Longitude = %s" % self.picImage.long,  ]

        #self.imageModeImageGridObject = get_PointInPoly(ImageGrid, self.picImage.long, self.picImage.lat)
        self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw")
        self.imageModeGridSQL()    
        self.imageDataWindowLoad()

    def DashboardMode(self):
        self.dashModeFrame = Frame(self.BaseFrame,bg="white", 
                                     
                                     relief=SUNKEN, bd=2)
        self.dashModeFrame.grid(row=0,column=0, rowspan=7,columnspan=10, ipadx=10, ipady=5,sticky = W+E+N+S)



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

    
    
    def dataconnect(self):    
        import pyodbc
        self.driver = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' 
        self.dbq = 'DBQ=C:/CCWD/backend.accdb;' 
        connection_string = self.driver + self.dbq 
        conn = pyodbc.connect(connection_string, autocommit = True)
        self.cursor = conn.cursor()

        #self.cursorspatial = curspatial()


    def home(self):
        
        self.zoomer =  ZoomManager(self.upper, self.lower)

    def Scale(self):
        self.scaleManager = ScaleManager(self.ButtonFrame, self.zoomer, self.zoomSet)
        self.scale = self.scaleManager.scale
        
    def ColorChoserProxy(self,event):
        self.ColorChoser()
    def ColorChoser(self):
        import tkColorChooser as co
        import Tkinter
        
        root = Tkinter.Tk()
        
        root.withdraw()
        
        
        # [(R,G,B,),'#FFFFFF']
        colortuple = co.askcolor()
        
        
        #root.mainloop()
        root.destroy()
        return colortuple
    
    def PictureExplore(self):
        width1 = self.wInfo.buttonSize - 10
        height1 = self.wInfo.buttonSize - 10
        self.picWindow.canvas.delete("all")
        photo = PhotoImage(file = r'C:\district\png\Right.gif')
        self.picButton =  Button(background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.nextPic)
        self.picButton.image = photo
        photo = PhotoImage(file = r'C:\district\png\Binocular.gif')
        self.picButton2 = Button(background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.ButtonImage)#command=self.outputPicKML
        self.picButton2.image = photo
        photo = PhotoImage(file = r'C:\district\png\Camera.gif')

        buttons = [self.picButton,self.picButton2]
        for COUNTER,button in enumerate(buttons):
            self.mainpicWindow.canvas.create_window(self.wInfo.buttonSize * COUNTER + 10,self.mainpicWindow.heightIMap-self.wInfo.buttonSize,window=button,anchor="nw")
    
        self.pictureGet()
                                   
    def getQuickReport(self):
        quickReport()                                      
                                          
        
    def nextPic(self):
        
        if self.picCounter != len(self.picIDs) -1:
            self.picCounter +=1
        else:
            self.picCounter = 0
        self.picImage = ImageProcessor2(self.picIDs[self.picCounter][2], 1, self.wInfo)
        self.picWindow.canvas.create_image(1,1, image= self.picImage.jpgPI,anchor="nw")



    def pictureGet(self):
        
        picture_sql = "select * from Pictures"

        self.cursor.execute(picture_sql)
        self.picIDs = self.cursor.fetchall()

        self.picImage = ImageProcessor2(self.picIDs[self.picCounter][2], 1, self.wInfo)
        self.picWindow.canvas.create_image(1,1, image= self.picImage.jpgPI, anchor="nw")

    def geoPictureGet(self):
        
        
        self.geoPics = Pictures()
        
        self.picImage = ImageProcessor2(self.picIDs[self.picCounter][2], 1, self.wInfo)
        self.picWindow.canvas.create_image(1,1, image= self.picImage.jpgPI, anchor="nw")
           
            

    def GraphExplore(self):
        width1 = self.wInfo.buttonSize - 10
        height1 = self.wInfo.buttonSize - 10        #self.graphButton = Button( width= 4, height= 2,text= 'Next', command = self.graphView)
        photo = PhotoImage(file = r'C:\district\png\Right.gif')
        self.graph.graphButton =  Button(background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.graphCheck)
        self.graph.graphButton.image = photo
        photo = PhotoImage(file = r'C:\district\png\BarGraph.gif')
        self.graph.graphButton2 =  Button(background='#FFFFFF',width = width1, height = height1, image = photo, bd=3,relief='raised',cursor = 'boat', command=self.ButtonMakeGraph) #command=self.makeGraph)
        self.graph.graphButton2.image = photo
       
                               
    def makeGraph(self):
        geoObject = self.geoList[self.graphset]
        data = []
        for poly in geoObject[0]:
            a =  str(poly.id)
            b = poly.Geometry.area * 0.000247105381
            ab = a,b
            data.append(ab)

        BarChartArea(data, geoObject[1])   
                                               
          
    def graphCheck(self):
        
        #from django.db import models
        #self.graphGeoObjects = models.get_models()


        self.graph.canvas.delete("all")
        graphable =[]
        for currentgraph in self.canvasList:
            
            if currentgraph.graphable == 1:
                currentgraph.regenerateGraphData()
                graphable.append(currentgraph)
        limit = len(graphable)-1
        if self.graphset != limit:
            self.graphset +=1
        else:
            self.graphset = 0
            
        currentgraph = graphable[self.graphset]
        
        currentgraph.graphDataToScreen()
        buttons = [self.graph.graphButton,self.graph.graphButton2 ]
        for COUNTER,button in enumerate(buttons):
            self.graph.canvas.create_window(self.wInfo.buttonSize * COUNTER + 10,
                                            self.graph.heightIMap-self.wInfo.buttonSize, 
                                            window=button,
                                            anchor="nw")
        
        
    def GraphGen(self, geoObjectResults, title):
        data = []
        for polyObject in geoObjectResults:
            data.append(polyObject.Geometry.area)
        #data.sort()
        c_width = self.wInfo.sideWidths
        c_height = self.wInfo.graphCanvasHeight

        y_stretch = 15
        # gap between lower canvas edge and x axis
        y_gap = self.wInfo.buttonSize *1.5
        # stretch enough to get all data items in
        x_stretch = 15
        x_width = 25
        # gap between left canvas edge and y axis
        x_gap = 20
         
        maxy = max(data)
        color = self.colors[self.randcolor()]
        for x, y in enumerate(data):
            yorig = y
            y  = (y/maxy) * (c_height - 100) 
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y  + y_gap) + 10
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # draw the bar
            rect = self.graph.canvas.create_rectangle(x0, y0, x1, y1, fill="dark green")
            
            label = self.graph.canvas.create_text(x0+2, y0, anchor="sw", text=str(int(yorig * 0.000247105381)))
            #id = self.graph.canvas.create_text(x1+2, y1, anchor="sw", text=str(int(y)))
        
        ylinebottom = c_height- y_gap + 5
        ylinetop = c_height - ((c_height - 100)   + y_gap)
        xlineleft = x_gap-5
        xlineright = x1+5
        self.graph.canvas.create_rectangle(xlineleft,ylinetop ,xlineleft,ylinebottom )
        self.graph.canvas.create_rectangle(xlineleft,ylinebottom ,xlineright,ylinebottom )
        title = self.graph.canvas.create_text((xlineright)/2, ylinebottom + 5, anchor="nw", text=str(title))
        buttons = [self.graphButton,self.graphButton2 ]
        for COUNTER,button in enumerate(buttons):
            self.graph.canvas.create_window(self.wInfo.buttonSize * COUNTER + 10,
                                            self.graph.heightIMap-self.wInfo.buttonSize, 
                                            window=button,
                                            anchor="nw")
           
    def chartSwitchFunction(self):
        if self.chartSwitch != 1:
            self.ChartBarFunction()


    def reMap(self):

        
        
        self.ButtonsMap()

        self.mainMapFrame.grid(row=0, column=0,)

        self.pictureGet()
        self.GraphExplore()

    def regenerate(self):
        self.currentCoordWidth = self.zoomer.currentLowerRight[0]- self.zoomer.currentUpperLeft[0] 
        self.currentCoordHeight = self.zoomer.currentUpperLeft[1]- self.zoomer.currentLowerRight[1]
        self.geoList = []
        if self.canvasList == []:
            self.geoPolys(EastBay, 'white')
            self.geoPolys(WaterDistrictProperties, 'brown')
            self.geoPolys(AcquisitionProperties, "sandy brown")
            self.geoPolys(GrazedAreas, 'yellow')
            self.geoPolys(Wetlands, 'dark blue' )
            self.geoPolys(InvasiveSpecies,  'red')
        else:
            self.map.canvas.delete('all')
            self.graph.canvas.delete('all')
            self.picWindow.canvas.delete('all')

            for polyDisplay in self.canvasList:
                
                polyDisplay.generatePolygons()     
        self.mapModeLegendCheck()
        self.graphCheck()
        self.pictureGet()  



    
    def geoPolys(self, geoObject, fcolor):

        ocolor = self.colors[self.randcolor()]
        #fcolor = self.colors[self.randcolor()]
        if fcolor == ocolor:
            ocolor = self.colors[self.randcolor()]

        polyDisplay = PolygonManager2(geoObject,self.wInfo, self.zoomer,self.map, self.graph, self.legend)
        polyDisplay.updatePolyData( fcolor, fcolor)
        polyDisplay.generatePolygons()

        self.canvasList.append(polyDisplay)    
            
    def screenToCoords(self,event):
            screenx = event.x
            screeny = event.y
            mapx, mapy = self.screenToCoordsEngine(screenx,screeny)
            return mapx, mapy
        
    def screenToCoordsEngine(self, screenx, screeny):
            mapx = self.zoomer.currentUpperLeft[0] + ((float(screenx)/self.wInfo.mapcanvasWidth) * self.zoomer.currentWidth)
            mapy = self.zoomer.currentUpperLeft[1] - ((float(screeny)/self.wInfo.mapcanvasHeight ) * self.zoomer.currentHeight)
            return mapx, mapy

    def coordsToScreen(self,geoObject):
            
            mapx = geoObject.Geometry.x
            mapy = geoObject.Geometry.y

            screenx =   int(((mapx - self.zoomer.currentUpperLeft[0])/ self.wInfo.mapcanvasWidth) * self.wInfo.mapcanvasWidth) 
            screeny = int((( self.zoomer.currentUpperLeft[1] - mapy )/ self.wInfo.mapcanvasHeight) * self.wInfo.mapcanvasHeight)
            return screenx, screeny


     
    def currentCoords(self, event):
            sX, sY = self.screenToCoordsEngine(event.x, event.y)
            txt  =str(sX) + ' ' + str(sY)
            #self.graph.canvas.delete('all') 
            #self.graph.canvas.create_text(20,10, text=  txt, anchor = "nw")      
    
    

    def deleteScreenObjects(self):
        for poly in self.canvasList[2:]:
            del poly
        self.map.canvas.delete('all')
        self.graph.canvas.delete('all')
        self.picWindow.canvas.delete('all')
        self.GraphExplore()
        self.PictureExplore()

    def allButtons(self):

        self.ButtonList = []
        self.ButtonList2 = []

        self.guiButtonMgmt = guiButtonManager(self.zoomer)
        self.buttonDic = {"Add Data" :self.ButtonAddData,"Raw Data" : self.ButtonTables, "Graph" : self.ButtonMakeGraph,
                     "Pan Left": self.ButtonPanLeft, "Pan Up":self.ButtonPanUp, "Pan Down": self.ButtonPanDown,
                     "Pan Right": self.ButtonPanRight, "Zoom In":self.ButtonZoomIn, "Zoom Out":self.ButtonZoomOut, 
                     "Home" : self.ButtonHome, "Load Pictures":self.ButtonPictures, 'Map':self.ButtonMap, "Extract Data":self.ButtonExtractData,
                     "Big Picture": self.ButtonImage, "Print":self.ButtonPrint }
        orderKeys = ["Add Data","Load Pictures","Extract Data" ,
                     "Pan Left", "Pan Up", "Pan Down",
                     "Pan Right","Zoom In", "Zoom Out", "Home", "Raw Data","Graph",'Map']
        orderKeys = [
                     "Pan Left","Pan Right", "Pan Up", "Pan Down",
                     "Zoom In", "Zoom Out", "Home", "Print"
                     ]
        mainKeys = ["Add Data","Load Pictures","Extract Data" ,"Raw Data","Big Picture","Graph",'Map']
        for keys in orderKeys:
            x = guiButton(self.mapButtonsFrame, keys, self.buttonWidth, self.buttonHeight, self.guiButtonMgmt.buttons[keys]['filepath'],self.buttonDic[keys])
            self.ButtonList.append(x)

        self.ButtonsMap()

        for keys in mainKeys:
            x = guiButton(self.ButtonFrame, keys, self.buttonWidth, self.buttonHeight, self.guiButtonMgmt.buttons[keys]['filepath'],self.buttonDic[keys])
            self.ButtonList2.append(x)

        self.ButtonsMain()

    def ButtonsMap(self):

            x= 0
            COUNTER = 0
            for buttons in self.ButtonList:
                buttons.button.grid(row =COUNTER, column=x,padx = 3, pady=1)

                if COUNTER == 3:
                    COUNTER=0
                    x=1
                else:
                    COUNTER+=1
                

    def ButtonsMain(self):
        for COUNTER,buttons in enumerate(self.ButtonList2):
            buttons.button.grid(row =0, column=(14-COUNTER),padx = 3, pady=1)



    def ButtonForget(self):
        for buttons in self.ButtonList:
            buttons.button.grid_forget()

    def ButtonMap(self):

            self.ModeSwitch("Map")
        
    def ButtonAddData(self):
        self.importSHP()

    def ButtonPictures(self):
        self.PicModels = [WetlandsPhotos, 
                            IssuePhotos,
                            HabitatPhotos,
                            InvasiveSpeciesPhotos,
                            GrazedAreasPhotos
                            ]
        self.selectType2(self.loadPic, self.PicModels)

    def ButtonImage(self):
        self.ModeSwitch("Image")

    def ButtonExtractData(self):
        #self.orderedDialogue()
        self.ModeSwitch('SQL')
        
    def ButtonTables(self):
        self.ModeSwitch('Table')
        #self.orderedDialogue()
        
    def ButtonMakeGraph(self):
        self.ModeSwitch('Graph')
        

    def ButtonPrint(self):
        self.printMap()

    def ButtonPanUp(self):
        moveval =((self.zoomer.scale/self.currentCoordHeight) * self.wInfo.mapcanvasHeight)
        print moveval, 'moveval', self.wInfo.mapcanvasHeight

        for polyDisplay in self.canvasList:
            for poly in polyDisplay.polygons:
                self.map.canvas.move(poly,0, moveval )
        self.zoomer.panUp()
        self.setStatus()
        self.buttonsCheck()
        
    def ButtonPanDown(self):
        moveval = 0 - ((self.zoomer.scale/self.currentCoordHeight) * self.wInfo.mapcanvasHeight)
        print moveval, 'moveval'
        for polyDisplay in self.canvasList:
            for poly in polyDisplay.polygons:
                self.map.canvas.move(poly,0, moveval )
        self.zoomer.panDown()
        
        self.buttonsCheck()   
             
    def ButtonPanLeft(self):
       
        moveval = ((self.zoomer.scale/self.currentCoordWidth) * self.wInfo.mapcanvasWidth)
        print moveval, 'moveval',self.wInfo.mapcanvasWidth

        for polyDisplay in self.canvasList:
            for poly in polyDisplay.polygons:
                self.map.canvas.move(poly, moveval,0 )
        
        self.zoomer.panLeft()
        self.setStatus()
        self.buttonsCheck()
        
    def ButtonPanRight(self):
         
       
        moveval = 0 -(self.zoomer.scale/self.currentCoordWidth) * self.wInfo.mapcanvasWidth
        
        print moveval, 'moveval'

        for polyDisplay in self.canvasList:
            for poly in polyDisplay.polygons:
                self.map.canvas.move(poly, moveval,0 )
        self.zoomer.panRight()
        
        self.buttonsCheck()

        
    def ButtonZoomIn(self):


        if self.zoomer.currentZoom != 1:
            widthhalf,heighthalf = self.wInfo.mapcanvasWidth/2.0, self.wInfo.mapcanvasHeight/2.0

            scale = 2 #10.0 /(self.zoomer.currentZoom )* 2.0
            self.map.canvas.scale("all",widthhalf,heighthalf , scale, scale)
            self.zoomer.currentZoom = self.zoomer.currentZoom - 1
            #self.adjustCurrentRecIn(0,0)
            screenx, screeny  =self.screenToCoordsEngine(widthhalf,heighthalf )
            self.zoomer.zoomin(screenx,screeny)
            
            self.buttonsCheck()    
                    
    def ZoomInMode(self, event):
        canvas = event.widget
        x = event.x
        y = event.y


        if self.zoomer.currentZoom != 1:
            scaleX = 2.0 #(10.0 /(self.zoomer.currentZoom ))* 2.0
            scaleY = scaleX #* (self.wInfo.mapcanvasHeight/self.wInfo.mapcanvasWidth)
            self.map.canvas.scale("all",x, y, scaleX, scaleY)            
            self.zoomer.currentZoom = self.zoomer.currentZoom - 1
            self.zoomer.multiplier = self.zoomer.multiplier * scaleX

            screenx, screeny  =self.screenToCoordsEngine(x, y)
            self.zoomer.zoomin(screenx,screeny)
            

            self.buttonsCheck()

            self.currentCoordWidth = self.zoomer.currentWidth
            self.currentCoordHeight = self.zoomer.currentHeight
            print self.zoomer.currentPolyString

            
    def ButtonZoomOut(self):
        
        if self.zoomer.currentZoom != 11:
            widthhalf,heighthalf = self.wInfo.mapcanvasWidth/2.0, self.wInfo.mapcanvasHeight/2.0
            scale = .5 # 1.0/self.zoomer.currentZoom
            self.map.canvas.scale("all",widthhalf,heighthalf, scale, scale)
            self.zoomer.currentZoom = self.zoomer.currentZoom + 1
            screenx, screeny = self.screenToCoordsEngine(widthhalf,heighthalf)
            self.zoomer.zoomout(screenx,screeny)

            #self.adjustCurrentRecOut(0,0,scale)
            
            self.buttonsCheck()

    def buttonsCheck(self):
        try:
            self.graphCheck()
            self.mapModeLegendCheck()
        except Exception, e:
            print e


            
    def ZoomOutMode(self, event):
        x= event.x
        y = event.y


        if self.zoomer.currentZoom != 11:
            scaleX = .5 # 1.0/self.zoomer.currentZoom
            scaleY = scaleX #* (self.wInfo.mapcanvasHeight/self.wInfo.mapcanvasWidth)
            self.map.canvas.scale("all",x, y, scaleX, scaleY)
            #self.map.canvas.scale("all",1.0/scale, 1.0/scale, x, y )

            self.zoomer.currentZoom = self.zoomer.currentZoom + 1
            self.zoomer.multiplier = self.zoomer.multiplier * scaleX
            screenx, screeny = self.screenToCoordsEngine(x, y)
            self.zoomer.zoomout(screenx,screeny)
            #self.adjustCurrentRecOut(x,y, scaleX)
            self.buttonsCheck()
            self.currentCoordWidth = self.zoomer.currentWidth
            self.currentCoordHeight = self.zoomer.currentHeight
            print self.zoomer.currentPolyString



    
    
    def ButtonHome(self):
        self.home()
        #self.deleteScreenObjects()
        self.regenerate()    
        
        
    def zoomSet(self,event):
        if self.scale.get() < self.zoomer.currentZoom:
            self.zoomer.currentZoom = self.scale.get()
            self.zoomer.zoomOut(self.scaleManager.scalevalues[self.zoomer.currentZoom +1])
        elif self.scale.get() > self.zoomer.currentZoom:
            self.zoomer.currentZoom = self.scale.get()
            self.zoomer.zoomIn(self.scaleManager.scalevalues[self.zoomer.currentZoom-1])
        self.textvar.set(self.scaleManager.scalevalues[self.zoomer.currentZoom-1])


    def printMap(self):
        pass

    def adjustButtons(self):
        'controls adjustments to button sizes'
        self.buttonHeight = self.wInfo.buttonSize -10
        self.buttonWidth = self.wInfo.buttonSize - 10
        
        for COUNTER,buttonObject in enumerate(self.ButtonList):
            buttonObject.button.grid_forget()
            del buttonObject
        self.allButtons()



    def status(self):
        self.statusWindow = Toplevel()
        self.statusWindow.title("status")
        self.statusWindow.wm_attributes("-topmost", 1)
        self.statusWindow.wm_maxsize(1200, 600)
        self.statustext = StringVar()
        self.statusscreen = Label(self.statusWindow, textvariable = self.statustext)
        self.statusscreen.pack(padx = 10, pady = 50)
        self.statustext.set(self.zoomer.currentPolyString)

        self.screentext = StringVar()
        self.screenCoordstatus = Label(self.statusWindow, textvariable = self.screentext)
        self.screenCoordstatus.pack()
        self.xy = ''

    
    def setStatus(self):
        #data = self.zoomer.currentPolyString + '\n' + self.xy +'\n' + str(self.zoomer.currentHeight) + '\n' + str(self.zoomer.currentWidth) + '\n' + str(self.zoomer.currentUpperLeft) + '\n' +str(self.zoomer.currentLowerRight) 
        pass
        #self.statustext.set(data)


        
    def closeIssues(self):
        
        self.root2 = Toplevel() #self.masterswitch  
        #self.root2.wm_iconbitmap(self.logoPath)  

        self.background2 = createFrame(self.root2)
        self.background2.pack(side=TOP, padx=10)

        
        
        self.reportLabel2  = createLabel(self.background2, "CLOSE AN ISSUE")
        self.reportLabel2.pack(side =TOP)
        
        
        self.closeFrame = createFrame(self.background2)
        self.closeFrame.pack(side=TOP, padx=10)

        self.closeList = createListBox(self.closeFrame,x=6,y=30)
        self.closeList.pack(side=LEFT, pady=7)

        sql = "select * from Issues WHERE ISNULL(DayClosed)"
        self.cursor.execute(sql)
        
        self.issues2 = self.cursor.fetchall()
        self.closeList.delete(0,END)
        max = 0
        for COUNTER, issue in enumerate(self.issues2):
            data = ''
            if max < issue[0]:
                max = issue[0]
            date = issue[3].date()
            importantData = [issue[1], date]

            for details in importantData:
                if details != None:
                    
                    data = data + ' ' + str(details)
            self.closeList.insert(END, data)
            self.closeList.itemconfig(COUNTER, fg='red')



        self.NumberFrame = createFrame(self.background2)
        self.NumberFrame.pack(side=TOP)
        self.closeNumberLabel = Label(self.NumberFrame, text= 'Number\nOf\nPersonnel\nUsed', bg='white')
        self.closeNumberLabel.pack(side=LEFT)
        self.closeNumber = Entry(self.NumberFrame, bg='white')
        self.closeNumber.pack(side=RIGHT)
 
        self.DaysFrame = createFrame(self.background2)
        self.DaysFrame.pack(side=TOP)        
        self.closeDaysLabel = Label(self.DaysFrame, text= 'Number\nOf\nDays\nSpent', bg='white')
        self.closeDaysLabel.pack(side=LEFT)
        self.closeDays = Entry(self.DaysFrame, bg='white')
        self.closeDays.pack(side=RIGHT)
        
        
        self.closeButtonFrame = createFrame(self.background2)
        self.closeButtonFrame.pack(side=BOTTOM)
        self.buttonClose = Button(self.closeButtonFrame,bg= 'dark green',fg= 'white',bd=8, text = 'CLOSE ISSUE') #command = self.issueClosed)
        self.buttonClose.pack()        
        
    def writeSHP(self):
        # Constants for shape types (from shapefile.py)
    
        for geom in geoObject.Geometry:
            coord.append(geom)
            
        shapedic = {
                    0: 1,
                    1: 3,
                    3: 5,
                    4 :8}    
        shape = shapdic[geoObject.Geometry.geom_typeid]
        shp = Writer(shapeType=shape) #shapedic[shape])
        shp.poly(parts=[coords])
    
    
        from Tkinter import Tk
    
        import tkFileDialog
        master = Tk()
        master.withdraw()
        shpath = tkFileDialog.asksaveasfilename(parent=master,
                                                  initialdir='C:/',
                                                  title='Save the Shapefile',
                                                  filetypes=[('SHP', '*.shp')])
        master.destroy()
        shp.save(shpath.split('.')[0])

    def report(self,):
        self.root = Toplevel()
        self.master.iconify()
        logoPath = 'C:\\CCWD\\ogo.ico' #self.masterswitch  
        self.root.wm_iconbitmap(logoPath)  
        self.background = Frame(self.root,width =50, height=50, bd=5,  relief=RAISED)
        self.background.pack(side=LEFT)
        self.column1 =createFrame(self.background)
        self.column1.pack(side=LEFT, padx=10)
        
        self.reportLabel  = createLabel(self.column1, "REPORT AN ISSUE")
        self.reportLabel.pack(side =TOP)

        self.emailFrame = createFrame(self.column1)
        self.emailFrame.pack(side=TOP, padx=10)

        self.emailIssueFrame = createFrame(self.emailFrame)
        self.emailIssueFrame.pack(side=TOP)
        self.issueLabel = createLabel(self.emailIssueFrame,"Select\nIssue\nType")
        self.issueLabel.pack(side=LEFT)       
        self.emailIssueType = createListBox(self.emailIssueFrame, x=6,y=30)
        self.emailIssueType.pack(side=LEFT, pady=7)

        self.emailRecipientsFrame = createFrame(self.emailFrame)
        self.emailRecipientsFrame.pack(side=TOP)
        
        
              
        self.emailRecipients = createListBox(self.emailIssueFrame,selmo = MULTIPLE, x=6,y=30)
        self.emailRecipients.pack(side=LEFT, pady=7)
        #self.emailRecipients.bind("<Double Button-1>", self.selectEmailRecipients)
        self.recipientLabel = createLabel(self.emailIssueFrame,"Select\nRecipients")
        self.recipientLabel.pack(side=LEFT) 
        
        #self.selectedEmailRecipients = createListBox(self.emailRecipientsFrame, x=6,y=30)
        #self.selectedEmailRecipients.pack(side=LEFT, pady=7)
        #self.selectedEmailRecipients.bind("<Double Button-1>", self.clearEmailRecipients)
        
        #self.recipientLabel = createLabel(self.emailRecipientsFrame,"Selected\nRecipients")
        #self.recipientLabel.pack(side=RIGHT)    


        self.propTrailFrame = createFrame(self.emailFrame)
        self.propTrailFrame.pack(side=TOP)
        self.propertyLabel = createLabel(self.propTrailFrame,"Property\nAffected")
        self.propertyLabel.pack(side=LEFT) 
              
        self.propertiesList = createListBox(self.propTrailFrame, x=6,y=30)
        self.propertiesList.pack(side=LEFT, pady=7)
        self.propertiesList.bind("<Double Button-1>", self.selectProperty)
        
        self.trailsList = createListBox(self.propTrailFrame, x=6,y=30)
        self.trailsList.pack(side=LEFT, pady=7)
        self.trailsList.bind("<Double Button-1>", self.selectTrail)
        
        self.trailsLabel = createLabel(self.propTrailFrame,"Trails\nAffected")
        self.trailsLabel.pack(side=RIGHT)  

        
        self.issueTextFrame = createFrame(self.emailFrame)
        self.issueTextFrame.pack(side=TOP)
        self.issueTextLabel = createLabel(self.issueTextFrame,"Short  \nIssue  \nDescription")
        self.issueTextLabel.pack(side=LEFT)
        self.issueText = Text(self.issueTextFrame, height= 1, width=50, bd=3)
        self.issueText.pack(side=RIGHT)
        

        
        self.emailTextFrame = createFrame(self.emailFrame)
        self.emailTextFrame.pack(side=TOP)
        self.emailLabel = createLabel(self.emailTextFrame,"Body Of\nEmail")  
        self.emailLabel.pack(side=LEFT)    
        self.emailText  =Text(self.emailTextFrame, height= 10, width=50,relief=SUNKEN, bd=5)
        self.emailText.pack(side=RIGHT)

        

        self.buttonEmail = Button(self.column1,bg= 'dark green',fg= 'white',bd=8, text = 'SEND EMAIL', command = self.sendEmail)
        self.buttonEmail.pack(side=RIGHT)
        self.buttonAttachPics = Button(self.column1,bg= 'dark red',fg= 'white', bd=8,text = 'Attach Pictures', command = self.AttachPicsEmail)
        self.buttonAttachPics.pack(side=RIGHT) 
        self.buttonAttachPics = Button(self.column1,bg= 'dark red',fg= 'white', bd=8,text = 'Attach KML ', command = self.makeMarkerProxy)
        self.buttonAttachPics.pack(side=RIGHT)         
    
    def issueReport(self):
        self.createQuery("ISSUE",self.issueGet)
 
    def grazingReport(self):
        self.createQuery("GRAZING",self.grazingGet)

    def wetlandsReport(self):
        self.createQuery("WETLANDS",self.wetlandsGet)

    def iSpeciesReport(self):
        self.createQuery("INVASIVE SPECIES",self.iSpeciesGet)
        
    def habitatReport(self):
        self.createQuery("HABITAT",self.habitatGet)
                                                 
        
    def createQuery(self, type, execute):
        self.root3 = Toplevel()
        logoPath = 'C:\\CCWD\\ogo.ico'
        self.root3.wm_iconbitmap(logoPath)  
        
        self.background3 = createFrame(self.root3)
        self.background3.pack()
        
        self.createReportLabel = createLabel(self.background3, "%s REPORT" % type )
        self.createReportLabel.pack()
        
        self.showMeLabel = createLabel(self.background3, "Show Me All %s" % type.title() )
        self.showMeLabel.pack()
       
        self.showMeLabel = createLabel(self.background3, "FROM" )
        self.showMeLabel.pack()
        
        self.dateFromFrame = createFrame(self.root3)
        self.dateFromFrame.pack()
        
        months = ['January', 'February', 'March', 'April', 'May','June', 'July','August', 'September', 'October', 'November','December'
                  ]
        self.month = StringVar(self.root3)
        self.month.set(months[0])
        
        self.monthSelect = apply(OptionMenu,(self.dateFromFrame, self.month) + tuple(months))
        self.monthSelect.pack(side= LEFT)
        
        date = time.localtime()
        
        years = []
        
        self.year = StringVar(self.root3)
        self.year.set('2000')
        
        origYear = 2000
        yearrange = int(date[0]) - origYear
        for hist in range(yearrange):
            inYear = hist + origYear
            years.append(str(inYear))
            
        
        self.yearSelect = apply(OptionMenu,(self.dateFromFrame, self.year) + tuple(years))
        self.yearSelect.pack(side= RIGHT)

        self.dateToFrame = createFrame(self.root3)
        self.dateToFrame.pack()
        

        self.showMeLabel = createLabel(self.dateToFrame, "UP TO" )
        self.showMeLabel.pack()


        self.month2 = StringVar(self.root3)
        self.month2.set(months[-1])
        
        self.monthSelectTo = apply(OptionMenu,(self.dateToFrame, self.month2) + tuple(months))
        self.monthSelectTo.pack(side= LEFT)
        
        date = time.localtime()
        
        years = []
        
        self.year2 = StringVar(self.root3)
        self.year2.set(date[0])
        
        origYear = 2000
        yearrange = int(date[0]) - origYear + 1
        for hist in range(yearrange):
            inYear = hist + origYear
            years.insert(0,str(inYear))
    
        self.yearSelectTo = apply(OptionMenu,(self.dateToFrame, self.year2) + tuple(years))
        self.yearSelectTo.pack(side= RIGHT)

        self.getButtonFrame = createFrame(self.root3)
        self.getButtonFrame.pack(side=BOTTOM)
        self.buttonGet = Button(self.getButtonFrame,bg= 'dark green',fg= 'white',bd=8, text = 'CREATE REPORT', command = execute)
        self.buttonGet.pack()


    def grazingGet(self):
        name = "GrazingReport_%s.csv" % dateString().replace('/','_')
#        
        csv = open(os.path.join(self.reportPath,name ),'w')
        header = "Lease,AUM,MonthCode,Year,GrazingYear,Month,AUM Value,Grazing Fee,AD, ADA\n"
        csv.write(header)
        monthFrom = self.month.get()
        monthTo = self.month2.get()
        yearFrom = self.year.get()
        yearTo = self.year2.get()
        grazing_sql = 'SELECT * FROM GRAZING'
        #grazing_sql = "SELECT * from Grazing where GrazingYear > format(#%s/%s#,'mm/yyyy') AND GrazingYear < format(#%s/%s#,'mm/yyyy') ORDER BY GrazingYear DESC" % (monthFrom, yearFrom, monthTo, yearTo)
        self.cursor.execute(grazing_sql)
        datas = self.cursor.fetchall()
        for data in datas:
                    
            csvinfo = str(data[1]) +',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4]) + ',' + str(data[5]) + ',' + str(data[6]) + ',' + str(data[7]) + ',' + str(data[8]) + ',' + str(data[9]) + ',' + str(data[10]) +  '\n'
            csv.write(csvinfo)
        csv.close()
        os.startfile(os.path.join(self.reportPath,name ))  

    def wetlandsGet(self):
        name = "Wetlands_%s.csv" % self.dateString().replace('/','_')
#        
        csv = open(os.path.join(self.reportPath,name ),'w')
        header = "Lease,AUM,MonthCode,Year,GrazingYear,Month,AUM Value,Grazing Fee,AD, ADA\n"
        csv.write(header)
        monthFrom = self.month.get()
        monthTo = self.month2.get()
        yearFrom = self.year.get()
        yearTo = self.year2.get()
        grazing_sql = 'SELECT * FROM GRAZING'
        #grazing_sql = "SELECT * from Grazing where GrazingYear > format(#%s/%s#,'mm/yyyy') AND GrazingYear < format(#%s/%s#,'mm/yyyy') ORDER BY GrazingYear DESC" % (monthFrom, yearFrom, monthTo, yearTo)
        self.cursor.execute(grazing_sql)
        datas = self.cursor.fetchall()
        for data in datas:
                    
            csvinfo = str(data[1]) +',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4]) + ',' + str(data[5]) + ',' + str(data[6]) + ',' + str(data[7]) + ',' + str(data[8]) + ',' + str(data[9]) + ',' + str(data[10]) +  '\n'
            csv.write(csvinfo)
        csv.close()
        os.startfile(os.path.join(self.reportPath,name ))

    def iSpeciesGet(self):
        name = "Invasive_Species_%s.csv" % self.dateString().replace('/','_')
#        
        csv = open(os.path.join(self.reportPath,name ),'w')
        header = "Lease,AUM,MonthCode,Year,GrazingYear,Month,AUM Value,Grazing Fee,AD, ADA\n"
        csv.write(header)
        monthFrom = self.month.get()
        monthTo = self.month2.get()
        yearFrom = self.year.get()
        yearTo = self.year2.get()
        grazing_sql = 'SELECT * FROM GRAZING'
        #grazing_sql = "SELECT * from Grazing where GrazingYear > format(#%s/%s#,'mm/yyyy') AND GrazingYear < format(#%s/%s#,'mm/yyyy') ORDER BY GrazingYear DESC" % (monthFrom, yearFrom, monthTo, yearTo)
        self.cursor.execute(grazing_sql)
        datas = self.cursor.fetchall()
        for data in datas:
                    
            csvinfo = str(data[1]) +',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4]) + ',' + str(data[5]) + ',' + str(data[6]) + ',' + str(data[7]) + ',' + str(data[8]) + ',' + str(data[9]) + ',' + str(data[10]) +  '\n'
            csv.write(csvinfo)
        csv.close()
        os.startfile(os.path.join(self.reportPath,name ))

    def habitatGet(self):
        name = "Habitat_Monitoring_%s.csv" % self.dateString().replace('/','_')
#        
        csv = open(os.path.join(self.reportPath,name ),'w')
        header = "Lease,AUM,MonthCode,Year,GrazingYear,Month,AUM Value,Grazing Fee,AD, ADA\n"
        csv.write(header)
        monthFrom = self.month.get()
        monthTo = self.month2.get()
        yearFrom = self.year.get()
        yearTo = self.year2.get()
        grazing_sql = 'SELECT * FROM GRAZING'
        #grazing_sql = "SELECT * from Grazing where GrazingYear > format(#%s/%s#,'mm/yyyy') AND GrazingYear < format(#%s/%s#,'mm/yyyy') ORDER BY GrazingYear DESC" % (monthFrom, yearFrom, monthTo, yearTo)
        self.cursor.execute(grazing_sql)
        datas = self.cursor.fetchall()
        for data in datas:
                    
            csvinfo = str(data[1]) +',' + str(data[2]) + ',' + str(data[3]) + ',' + str(data[4]) + ',' + str(data[5]) + ',' + str(data[6]) + ',' + str(data[7]) + ',' + str(data[8]) + ',' + str(data[9]) + ',' + str(data[10]) +  '\n'
            csv.write(csvinfo)
        csv.close()
        os.startfile(os.path.join(self.reportPath,name ))

    def issueGet(self):
        name = "IssueReport_%s.csv" % dateString().replace('/','_')
        
        csv = open(os.path.join(self.reportPath,name ),'w')
        header = "Issue,Type,Property,Trail,NumberPersonnel,DaysSpent,DateReported,DateClosed,ReportedBy\n"
        csv.write(header)
        monthFrom = self.month.get()
        monthTo = self.month2.get()
        yearFrom = self.year.get()
        yearTo = self.year2.get()
        between_sql = "SELECT * from Issues where DayReported > format(#%s/%s#,'mm/yyyy') AND DayReported < format(#%s/%s#,'mm/yyyy') ORDER BY DayReported DESC" % (monthFrom, yearFrom, monthTo, yearTo)
        self.cursor.execute(between_sql)
        datas = self.cursor.fetchall()
        for data in datas:
            
            type_select_sql = "SELECT TypeName FROM IssueType WHERE TypeID = ? " 
            self.cursor.execute(type_select_sql,int(data[2]))
            type = self.cursor.fetchone()[0]
            property_sql =  "SELECT PropertyName FROM Properties WHERE PropertyID = ? " 
            self.cursor.execute(property_sql, int(2))
            property = self.cursor.fetchone()[0]
            if data[8] != None:
                
                trail_sql =  "SELECT TrailName FROM Trails WHERE TrailID = ? " 
                self.cursor.execute(trail_sql, int(data[8]))
                trail = self.cursor.fetchone()[0]                   
            else:
                trail = ''
            
            if data[4] != None:
                dateClosed = str(data[4].date())
                issue_sql =  "SELECT NumPersonnel,NumDays FROM IssueClose WHERE IssueID = ? "  
                
                self.cursor.execute(issue_sql,int(data[0]))
                returned = self.cursor.fetchone()
                
                numper = returned[0]
                numdays = returned[1]                 
            else:
                dateClosed = 'Still Open'
                numper = ''
                numdays = ''
            csvinfo = data[1] +',' + type + ',' + property + ',' + trail + ',' + numper + ',' + numdays + ',' + str(data[3].date()) + ',' + dateClosed + ',' + data[5] + '\n'
            csv.write(csvinfo)
        csv.close()
        os.startfile(os.path.join(self.reportPath,name ))    


    def sendEmail(self):
        
        self.emailissue(issue)
        self.root.destroy()
        self.master.wm_state("normal")  
        
    def emailissue(self, issue):
        self.subject = "Issue Reported: %s" % issue
        self.recipient = self.emailstring
        self.body = self.emailText.get(1.0,END)
        self.CC = ""
        import win32com.client
        o = win32com.client.Dispatch("Outlook.Application")
        Msg = o.CreateItem(0)
        Msg.Subject = self.subject
        Msg.To = self.recipient 
        Msg.Body = self.body
        Msg.CC = self.CC
        size = 0
        for COUNTER,pic in enumerate(self.sizedic.keys()):
            
                size = size + os.stat(pic.replace('/','\\'))[6]
                if size < 6000000:
                    Msg.Attachments.Add(pic.replace('/','\\'))
        if self.attachmarker == 1:
            print 'here'
            print self.attachKMLPath
            Msg.Attachments.Add(self.attachKMLPath)
            self.attachmarker = 0 
        Msg.Send()
    
    def AttachPicsEmail(self):
        select_sql = "SELECT MAX(ID) from Pictures"
        
        self.cursor.execute(select_sql)
        picMax = self.cursor.fetchone()[0] +1
        
        self.paths = choosePics(self)
        self.sizedic = {}
        for path in self.paths.split(';'):
            
            self.sizedic[path] = os.stat(path)[6]
            destination = os.path.join(self.picFolder, os.path.basename(path))
            shutil.copy2(path.replace('/','\\'), destination)
            insert_pic_sql = "INSERT INTO Pictures VALUES(%d,%d,'%s')" % (picMax,self.IssueID,destination )
            
            self.cursor.execute(insert_pic_sql)
            picMax += 1

    def loadPic(self):
        listnumber = int(self.typeListbox.curselection()[0])
        type_ = self.PicModels[listnumber]
        self.masterselect.destroy()
        
        wellknowntext, filepath = loadPic()
        newfilepath = moveImage(filepath, self.imageLibrary )
        newrow = type_(filepath = newfilepath, Geometry = wellknowntext)
        newrow.save()
        
    
#    


    def createSHP(self):
        pass
    def importSHP(self):
        self.selectType(self.nextStep)
        
    def nextStep(self):
        
        from Tkinter import Tk
        from django.contrib.gis.geos import GEOSGeometry
        #TODO: make a sorter for different types of shapefile
        import tkFileDialog
        import time
        date = time.localtime()

        self.masterselect.destroy()
        master = Tk()
        master.withdraw()
        shp = tkFileDialog.askopenfilename(parent=master,initialdir='C:/',
                                                  title='Import a Shapefile',
                                                  filetypes=[('SHP', '*.shp')])
        master.destroy()

        if len(shp) != 0:
            shape = Reader(shp.split('.')[0])
            fields = shape.fields
            try:
                records = shape.records()
            except:
                pass
            attributes = {}
    
            polys = shape.shapes()
            
            
            for poly in  polys:
                polystring = 'POLYGON(('
                for point in poly.points[:-1]:
                    polystring += '%s %s,' % (point[0], point[1])
                polystring += "%s %s))" % (poly.points[-1][0], poly.points[-1][1])
                data = GEOSGeometry(polystring)
                newWetlands = Wetlands(Geometry = data)
                newWetlands.save()
            #sql_string = "INSERT INTO wetlands (Geometry) VALUES (%s) " % polystring
    
    def selectSpreadSheet(self):
        self.selectType(self.createQueryProxy)
        
    def createQueryProxy(self):
        title = self.typeListbox.selection_get()
        self.masterselect.destroy()
        self.createQuery(title.split()[0], self.grazingGet)
        
    def selectType(self, execute):
    
        
        self.masterselect = Tk()
        master = self.masterselect
        master.wm_attributes("-topmost", 1)
        master.title('Select Study Type')
        master.maxsize(500,500)
        master.geometry('+100+100')
        master.iconbitmap(self.logoPath)
    
    
        frame2 = Frame(master, height=6, bd=7, relief=SUNKEN)
        frame2.pack(fill=X, padx= 2, pady=2)
    
        frame5 = Frame(frame2, bd=7)
        frame5.pack()
        
        scrollbar = Scrollbar(frame5)
        scrollbar.pack(side=RIGHT, fill= Y)
        
        listbox = Listbox(frame5,height = 20, width= 400,
                          yscrollcommand=scrollbar.set,
                          xscrollcommand=scrollbar.set)

        listbox.insert(END, 'Wetland Study') 
        listbox.insert(END,"Resource Study")
        listbox.insert(END,"Habitat Study")
        listbox.insert(END,"Invasive Species Report")
        listbox.insert(END,"Grazing Report")
        
        
        listbox.pack()
        self.typeListbox = listbox
        scrollbar.config(command=listbox.yview)
        stepButton = Button(frame5, text= 'Next Step',
                             font = 'Gill_Sans_MT -12 bold' ,
                             bg = 'dark green', fg = 'white',
                             bd = 10, width=12,
                             command=execute)
        stepButton.pack(side=TOP, pady =5,padx=4)
        master.mainloop()

    def selectType2(self, execute, keys):
    
        
        self.masterselect = Tk()
        master = self.masterselect
        master.wm_attributes("-topmost", 1)
        master.title('Select Photo Type')
        master.maxsize(500,500)
        master.geometry('+100+100')
        master.iconbitmap(self.logoPath)
    
    
        frame2 = Frame(master, height=6, bd=7, relief=SUNKEN)
        frame2.pack(fill=X, padx= 2, pady=2)
    
        frame5 = Frame(frame2, bd=7)
        frame5.pack()
        
        scrollbar = Scrollbar(frame5)
        scrollbar.pack(side=RIGHT, fill= Y)
        
        listbox = Listbox(frame5,height = 20, width= 400,
                          yscrollcommand=scrollbar.set,
                          xscrollcommand=scrollbar.set)
        for key in keys:
            listbox.insert(END, key.namestring) 

        
        
        listbox.pack()
        self.typeListbox = listbox
        scrollbar.config(command=listbox.yview)
        stepButton = Button(frame5, text= 'Next Step',
                             font = 'Gill_Sans_MT -12 bold' ,
                             bg = 'dark green', fg = 'white',
                             bd = 10, width=12,
                             command=execute)
        stepButton.pack(side=TOP, pady =5,padx=4)
        master.mainloop()

        

    def geoNotes(self):
        from Tkinter import Tk, Text, Button, END, Entry, Label
        self.second_window = Toplevel()
        self.second_window.wm_iconbitmap(self.logoPath)
        self.second_window.title('Record Location')
        self.second_window.wm_attributes("-topmost", 1) 
        self.map.canvas.bind("Button-2", self.adjustLocCapture)
        self.pdf_title_label = Label(self.second_window, text='PDF TITLE')
        self.pdf_title_label.pack()
        self.pdf_title = Entry(self.second_window, width=20)
        self.pdf_title.pack()

        self.pdf_title_label = Label(self.second_window, text='Description')
        self.pdf_title_label.pack()       
        self.note_text = Text(self.second_window, width=20, height=10)
        self.note_text.pack(padx = 10)
        
        self.locCapture = StringVar()
        self.pdf_title_label = Label(self.second_window, textvariable=self.locCapture)
        self.locCapture.set("Click on Map")
        
        self.pdf_title_label.pack() 
        self.buttonNotesGO = Button(self.second_window ,width = 15, height=2, bg='dark green', fg='white',text = 'Record Note', command = self.recordNotes)
        self.buttonNotesGO.pack()
        self.second_window.mainloop()

    def adjustLocCapture(self, event):
        self.locCapture.set("Location Captured")
        mapx, mapy = self.screenToCoordsEngine(event.x, event.y)
        self.noteX  = mapx
        self.noteY = mapy
    
    def outputPicKML(self):
        filepath = self.picIDs[self.picCounter][2]
        tags = get_exif(filepath)
        picloc = geopics(tags)
        longitude = picloc[1]
        latitude = picloc[0]
        kmlname= "OutputKML"
        
        kmlname2= kmlname.replace(' ','')
         
        shutil.copy(filepath,"C:/CCWD/pics/KMLS/%s" % os.path.basename(filepath))
        kmltext = kml % (kmlname2, kmlname,
                         os.path.basename(filepath),
                         '',
                         longitude, 
                         latitude, 
                         longitude, 
                         latitude )
        
        kmlfile = open(os.path.join("C:/CCWD/pics/KMLS",'%s.kml' % kmlname), 'w')        
        kmlfile.write(kmltext)
        kmlfile.close()        
        os.startfile(os.path.join("C:/CCWD/pics/KMLS",'%s.kml' % kmlname))
                
    def recordNotes(self):
        if self.locCapture != "Click on Map":
            self.second_window.destroy()
            points = get_geoObjectInRec(GeoNotes, self.zoomer.currentPolyString)

    def chartMake4(self,datalist, titlestring,descriptionstring):
        from reportlab.graphics.charts.legends import Legend
        from reportlab.graphics.charts.barcharts import VerticalBarChart#,VerticalBarChart3D
        from reportlab.graphics.shapes import Drawing,_DrawingEditorMixin,String
        from reportlab.graphics.charts.textlabels import Label, BarChartLabel
        from reportlab.graphics.samples.excelcolors import color05,color06,color02,color01  ,color02,color03,color04,color05,color06,color07,color08,color09, color10
        from reportlab.lib.units import cm, mm, inch
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.graphics.widgetbase import Widget,TypedPropertyCollection
        from reportlab.lib import colors
        from reportlab.graphics.charts.linecharts import HorizontalLineChart
        from reportlab.graphics.charts.linecharts import LineChart
        from reportlab.lib.formatters import DecimalFormatter
    
        from reportlab.graphics.widgets.markers import makeMarker
        import string
        drawing = Drawing(width=11 * inch, height= 8 * inch) #(width=len(columns)* inch + 1 * inch, height=5*inch)
    
              #(0,1010, 2020, 3030, 4040, 5050, 6060, 7070, 8080, 9090, 10100, 11110, 12120, 13130, 14140, 15150, 16160, 17170, 18180, 19190, 20200, 21210, 22220, 23230, 24240, 25250, 26260, 27270, 28280, 29290, 30300),
       
    ##    data = [
    ##        (0,  2020,  4040,  6060,  8080,  10100,  12120,
    ##         14140,  16160,  18180,  20200,
    ##          22220,  24240,  26260, 28280,  30300),
    ##        datalist
    ##    ]
        data = [
            (0,1010, 2020, 3030, 4040, 5050, 6060, 7070, 8080, 9090, 10100, 11110, 12120, 13130,
             14140, 15150, 16160, 17170, 18180, 19190, 20200,
             21210, 22220, 23230, 24240, 25250, 26260, 27270, 28280, 29290, 30300),
            datalist
        ]
    ##    data2 = [
    ##        (0,1010, 2020, 3030, 4040, 5050, 6060, 7070, 8080, 9090, 10100, 11110, 12120, 13130,
    ##         14140, 15150, 16160, 17170, 18180, 19190, 20200,
    ##         21210, 22220, 23230, 24240, 25250, 26260, 27270, 28280, 29290, 30300),
    ##        datalist
    ##    ]
        lc = HorizontalLineChart()
        lc.x = 1* inch
        lc.y = 1.5 * inch
        lc.height = 5 * inch
        lc.width = 9 * inch
        lc.data = data
        
        lc.joinedLines = 1
        lc.categoryAxis.categoryNames = ['2007','',
                                         '2009','','2011','', '2013','',
                                         '2015','', '2017', '',
                                         '2019','', '2021','', '2023','',
                                         '2025','', '2027','', '2029','', '2031','',
                                         '2033','', '2035','', '2037'] 
    
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.categoryAxis.labels.angle = 0#30
        lc.categoryAxis.tickDown = 2
        lc.categoryAxis.joinAxisMode = 'bottom'
        lc.categoryAxis.labels.fontName = "Helvetica"
        lc.categoryAxis.labels.fontSize = 10
        
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = 35000
        lc.valueAxis.valueStep = 5000
        lc.valueAxis.visibleGrid =1
        lc.valueAxis.labels.fontName = 'Helvetica'
        lc.valueAxis.labels.fontSize = 10
        lc.valueAxis.labels.maxWidth = 2
        lc.valueAxis.labelTextFormat = DecimalFormatter(places=0,
                                                    decimalSep='.',
                                                    thousandSep=',',
                                                    prefix=None,
                                                    suffix=None) 
        lc.lines[1].symbol = makeMarker('FilledSquare')
        lc.lines[0].strokeWidth = 2
        lc.lines[1].strokeWidth = 2
        lc.lines[0].strokeColor = colors.lightgreen
        lc.lines[1].strokeColor = colors.green
        #lc.lineLabelFormat = '%d'
        lc.lineLabels.dx = 0
        lc.lineLabels.dy = 0
        #vb.barLabels.boxAnchor = 'w'
        #vb.barLabels.fontName = "Helvetica"
        lc.lineLabels.fontSize = 6
        #lc.lineLabels.nudge = 5
        #lc.lineLabels.color = colors.white
    
    
    ##    lc1 = HorizontalLineChart()
    ##    lc1.x = 1* inch
    ##    lc1.y = 1.5 * inch
    ##    lc1.height = 5 * inch
    ##    lc1.width = 9 * inch
    ##    lc1.data = data2
    ##    lc1.categoryAxis.categoryNames = ['2007','',
    ##                                     '2009','','2011','', '2013','',
    ##                                     '2015','', '2017', '',
    ##                                     '2019','', '2021','', '2023','',
    ##                                     '2025','', '2027','', '2029','', '2031','',
    ##                                     '2033','', '2035','', '2037'] 
    ##
    ##    lc1.categoryAxis.labels.boxAnchor = 'n'
    ##    lc1.categoryAxis.labels.angle = 0#30
    ##    lc1.categoryAxis.tickDown = 2
    ##    lc1.categoryAxis.joinAxisMode = 'bottom'
    ##    lc1.valueAxis.valueMin = 0
    ##    lc1.valueAxis.valueMax = 35000
    ##    lc1.valueAxis.valueStep = 5000
    ##    lc1.valueAxis.visibleGrid =1
    ##    lc1.lines[1].symbol = makeMarker('FilledSquare')
    ##    lc1.lines[0].strokeWidth = 2
    ##    lc1.lines[1].strokeWidth = 2
    ##    #lc1.lines[0].strokeColor = colors.lightgreen
    ##    #lc1.lines[1].strokeColor = colors.green
    ##    lc1.lines[0].strokeColor = colors.green
    ##    lc1.lineLabelFormat = '%d'
    ##    lc1.lineLabels.dx = 0
    ##    lc1.lineLabels.dy = 0
    ##    #vb.barLabels.boxAnchor = 'w'
    ##    #vb.barLabels.fontName = "Helvetica"
    ##    lc1.lineLabels.fontSize = 6
    ##    #lc.lineLabels.nudge = 5
    
    
        legendColorList = [(colors.green, 'Acquisitions to date'),(colors.lightgreen, 'Progress toward estimated Preserve System')]
    
        for set in legendColorList:
            legend = Legend()
            legend.colorNamePairs = [set]#legendColorList
            legend.fontName       = 'Helvetica'
            legend.fontSize       = 11
            legend.x              = (2 * inch) + (2.5* inch *  legendColorList.index(set))
            legend.y              = .8* inch 
    
            
            legend.deltay         = 10
            legend.alignment      ='right'
            drawing.add(legend)
        #legend.fontName       = 'Helvetica'
    
        title = Label()
        title.fontName   = 'Helvetica'
        title.fontSize   = 12
        title.x          = drawing.width/2 
        title.y          = drawing.height - 1 * cm
        title._text      = titlestring 
        title.textAnchor = 'middle'
    
        description = Label()
        description.fontName   = 'Helvetica'
        description.fontSize   = 10
        description.x          = drawing.width/2 
        description.y          = drawing.height - 1.8 * cm
        description._text      = descriptionstring 
        description.textAnchor = 'start'
        note = Label()
        note.fontName   = 'Helvetica'
        note.fontSize   = 10
        note.x          = lc.width  + 1 * inch
        note.y          = lc.height + 2.7 * cm
        note._text      = "Year: 30\nGoal: 30,300 acres" 
        note.textAnchor = 'start'
        
        yLabel = Label()    
        yLabel.fontName       = 'Helvetica'
        yLabel.fontSize       = 11
        yLabel.x              = .3 * inch
        yLabel.y              = lc.height - 1 * inch
        yLabel.angle          = 0
        yLabel.textAnchor     ='middle'
        yLabel.maxWidth       = 100
        yLabel.height         = 20
        yLabel._text          = "Acres" #yText #"Acres"
        yLabel.angle = 90
    
        xLabel = Label()    
        xLabel.fontName       = 'Helvetica'
        xLabel.fontSize       = 11
        xLabel.x              = 5.5 * inch
        xLabel.y              = 1 * inch
        xLabel.angle          = 0
        xLabel.textAnchor     ='middle'
        xLabel.maxWidth       = 100
        xLabel.height         = 20
        xLabel._text          = "Year" #yText #"Acres"
        
       
        drawing.add(note)
        drawing.add(yLabel)
        drawing.add(xLabel)
        drawing.add(description)
        drawing.add(title)
        drawing.add(lc)
        #drawing.add(lc1)
        drawing.save(formats= ['pdf'],outDir=None,fnRoot='C:/Chart4.pdf' )
        return 'C:/Chart4.pdf'
    
    
    
    def savePDF(self):
            from Tkinter import Tk
        
            import tkFileDialog
            master = Tk()
            master.withdraw()
            pdf = tkFileDialog.asksaveasfilename(parent=master,
                                                      initialdir='C:/',
                                                      title='Save the PDF',initialfile='Chart_04.pdf',
                                                      filetypes=[('PDF', '*.pdf')])
            master.destroy()
            return pdf

    
    
    
    
    def watermark(pdflist, fileout):
    
        from pyPdf import PdfFileWriter, PdfFileReader
        output = PdfFileWriter()
        for pdf in pdflist:
    
    
            input1 = PdfFileReader(file(pdf, "rb"))
            page = input1.getPage(0)
            output.addPage(page)
            
            watermark = PdfFileReader(file("C:/HCPDatabase/watermark2011.pdf", "rb"))
            page.mergePage(watermark.getPage(0))
    
    
        
        fileout = fileout.replace('.pdf','')        
        fileout = fileout +'.pdf'
        outputStream = file(fileout  , "wb")
        output.write(outputStream)
        outputStream.close()
        import os
        os.startfile(fileout) 

    def chartCheck(self):
        self.geoChartList = []
        from django.db import models
        self.graphGeoObjects = models.get_models()
        for object in self.graphGeoObjects:

            try:
                if object.namestring:
                    if object.graph ==1:   
    
    
                        Polys = get_geoObjectsInRec(object, self.zoomer.currentPolyString)
                        geodata = Polys, object
                        if len(Polys) != 0:

                            self.geoChartList.append(geodata)
            except:
                pass
        self.chartView()
                                      
    def chartView(self):
        if self.graphset != len(self.geoList)-1 :
            self.graphset += 1

        else:
            self.graphset = 0
        
        self.chartMiddle()
        
    def chartMiddle(self):
            


        self.demoCanvas.canvas.delete('all')
        
        try:

            geoObject = self.geoChartList[self.graphset][0]
            title = self.geoChartList[self.graphset][1].namestring
            
        except Exception, e:

            self.demoCanvas.canvas.delete("all")
            self.graphset = self.graphset+1
            geoObject = self.geoChartList[self.graphset][0]
            title = self.geoChartList[self.graphset][1].namestring
        data = []
        for polyObject in geoObject:
            data.append(polyObject.Geometry.area)            
        self.ChartGen(data, title)
        
        ylong=100

        #geoList = [InvasiveSpecies,Wetlands,GrazedAreas,]
        #for model in geoList:
        self.currentGraphModel = self.geoList[self.graphset][1]
        model = self.currentGraphModel    
        self.chartFunctionDicAll = {'Type':self.ByTypeAllProxy,
                                    'Property':self.ByPropertyAllProxy,
                                    'Management Unit':self.ByManagementUnitAllProxy,
                                    'Date':self.ByDateAllProxy,
                                    'Treatment Used':self.ByTreatmentAllProxy,
                                    'Percent Change':self.ByChangeAllProxy,
                                    'Land Cover':self.ByLandCoverAllProxy,
                                    'Animal Used':self.ByAnimalAllProxy,
                                    'Owner':self.ByOwnerAllProxy
                                
                                 }
        self.chartFunctionDicCurrent = {'Type':self.ByTypeCurrentProxy,
                                    'Property':self.ByPropertyCurrentProxy,
                                    'Management Unit':self.ByManagementUnitCurrentProxy,
                                    'Date':self.ByDateCurrentProxy,
                                    'Treatment Used':self.ByTreatmentCurrentProxy,
                                    'Percent Change':self.ByChangeCurrentProxy,
                                    'Land Cover':self.ByLandCoverCurrentProxy,
                                    'Animal Used':self.ByAnimalCurrentProxy,
                                    'Owner':self.ByOwnerCurrentProxy

                                 }
        
        for type in model.graphtypes:
                    
                    if self.chartmode == 1:

                            func = self.chartFunctionDicAll[type]
                            
                    elif self.chartmode == 0:
                        func = self.chartFunctionDicCurrent[type]
                                                                
                    button = Button(self.chartButtonCanvas,background='tan',foreground='SlateBlue4',width = 10, height = 1, text=str(type), bd=3,relief='raised', command=func)
                    self.chartButtonCanvas.create_window(0,ylong,window=button, anchor="nw")
                    ylong += 30

        
    def dataGrouping(self):
        pass
    
                            
    def ChartGen(self, data, title):
        
        
        
        c_width = self.wInfo.mapcanvasWidth
        c_height = self.wInfo.graphCanvasHeight *2

        y_stretch = 25
        # gap between lower canvas edge and x axis
        y_gap = 50
        # stretch enough to get Current data items in
        x_stretch = 25
        x_width = 100
        # gap between left canvas edge and y axis
        x_gap = 100
        maxy = max(data)
        color = self.colors[self.randcolor()]
        self.chartBarGroups = []
        
        createRect = self.demoCanvas.canvas.create_rectangle
        createText = self.demoCanvas.canvas.create_text
        for x, y in enumerate(data):
            yorig = y
            y  = (y/maxy) * (c_height - 120) 
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = c_height - (y  + y_gap)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = c_height - y_gap
            # draw the bar
            rect = createRect(x0, y0, x1, y1, fill=color,activeoutline="red", activewidth=3.0)
            
            vallabel = createText(x0+ x_width/2, y0,anchor="s", justify=CENTER, text=str(int(yorig * 0.000247105381)))
            label = createText(x0+ x_width/2, y1+2,anchor="n", justify=CENTER, text=(title +" Item").replace(' ','\n'),tags="xValue")
            #id = self.graph.canvas.create_text(x1+2, y1, anchor="sw", text=str(int(y)))
            bargroup = rect,vallabel, label
            self.chartBarGroups.append(bargroup)
        ylinebottom = c_height- y_gap
        ylinetop = c_height - ((c_height - 100)   + y_gap)
        xlineleft = x_gap-5
        xlineright = x1+5
        createRect(xlineleft,ylinetop ,xlineleft,ylinebottom )
        createRect(xlineleft,ylinebottom ,xlineright,ylinebottom )
        title = createText(int(xlineright/2), 20, anchor="nw",justify=CENTER, text=str(title),tags="title",activefill="red")

        #xvalue = self.demoCanvas.canvas.create_text((xlineright)/2, ylinebottom + 5, anchor="nw", text=str(title))
        yvalue = createText(x_gap-70, ylinebottom/2, anchor="n",justify=CENTER,activefill="red",  text=str("Acres"),width=1, tags="yValue")
        for y in range(0,maxy,int(maxy/4) ):
            y  = (y/maxy) * (c_height - 120)
            y0 = c_height - (y  + y_gap) 
            createRect(xlineleft,y0 ,xlineleft-20,y0 )
            createText(xlineleft-24, y0, anchor="e", text=str(int(y)))
    
    def chartmodeswitch(self):
        
        if self.chartmode == 1:
            self.chartmode  = 0
            
        elif self.chartmode == 0:
            self.chartmode  = 1
        self.chartButtonCanvas.delete("all")
        self.chartMiddle()  

    def ModeSwitch(self, type):

        if type == "Graph":
            if self.mapSwitch  == 1:
                self.mapSwitch = 0
                #self.map.canvas.grid_forget()
                #self.graph.canvas.grid_forget()
                
                #self.picWindow.canvas.grid_forget()
                self.mainMapFrame.grid_forget()
                #self.graphButton.destroy()
                #self.graphButton2.destroy()
                
            if self.imageModeSwitch  ==1:
                self.imageModeSwitch = 0

                self.imageModeFrame.destroy()
            if self.sqlSwitch  ==1:
                self.sqlSwitch = 0

                self.sqlDialogue.destroy()
            elif self.tableModeSwitch  == 1:
                self.tableModeSwitch = 0
                self.tableModeFrame.destroy()
                
            if self.chartmode == 1:
                self.chartmode  = 0
                
            elif self.chartmode == 0:
                self.chartmode  = 1
            self.ButtonForget()
            self.ButtonsMain()
            self.chartSwitch  = 1
            self.ChartBarFunction()

        elif type == "Map":

            if self.chartSwitch  == 1:
                self.chartSwitch = 0
                self.chartDialogue.destroy()

            elif self.imageModeSwitch  ==1:
                self.imageModeSwitch = 0
                self.imageModeFrame.destroy()
            elif self.tableModeSwitch  == 1:
                self.tableModeSwitch = 0
                self.tableModeFrame.destroy()
                
            elif self.sqlSwitch  ==1:
                self.sqlSwitch = 0
                self.sqlDialogue.destroy()
            self.mapSwitch  = 1
            self.reMap()


        elif type == "SQL":
   
   
            if self.mapSwitch  == 1:
                self.mapSwitch = 0
                #self.map.canvas.grid_forget()
                #self.graph.canvas.grid_forget()
                
                #self.picWindow.canvas.grid_forget()
                self.mainMapFrame.grid_forget()

                #self.graphButton.destroy()
                #self.graphButton2.destroy()
                
            elif self.chartSwitch  == 1:
                self.chartSwitch = 0
                self.chartDialogue.destroy()
            elif self.imageModeSwitch  ==1:
                self.imageModeSwitch = 0
                self.imageModeFrame.destroy()
            elif self.tableModeSwitch  == 1:
                self.tableModeSwitch = 0
                self.tableModeFrame.destroy()
                
            self.ButtonForget()
            self.ButtonsMain()
            self.sqlSwitch  = 1
            self.orderedDialogue()
            
        elif type == "Image":
   
            if self.mapSwitch  == 1:
                self.mapSwitch = 0
                
                #self.map.canvas.grid_forget()
                #self.graph.canvas.grid_forget()
                #self.picWindow.canvas.grid_forget()
                self.mainMapFrame.grid_forget()
                #self.graphButton.destroy()
                #self.graphButton2.destroy()
                
            elif self.sqlSwitch  ==1:
                self.sqlSwitch = 0
                self.sqlDialogue.destroy()
            
            elif self.chartSwitch  == 1:
                self.chartSwitch = 0
                self.chartDialogue.destroy()
            elif self.tableModeSwitch  == 1:
                self.tableModeSwitch = 0
                self.tableModeFrame.destroy()
                
            self.ButtonForget()
            self.ButtonsMain()
            self.imageModeSwitch =1
            self.ImageMode()
            
        elif type == "Table":
   
            if self.mapSwitch  == 1:
                self.mapSwitch = 0
                
                #self.map.canvas.grid_forget()
                #self.graph.canvas.grid_forget()
                #self.picWindow.canvas.grid_forget()
                self.mainMapFrame.grid_forget()

                #self.graphButton.destroy()
                #self.graphButton2.destroy()
                
            elif self.sqlSwitch  ==1:
                self.sqlSwitch = 0
                self.sqlDialogue.destroy()
            
            elif self.chartSwitch  == 1:
                self.chartSwitch = 0
                self.chartDialogue.destroy()
                
            elif self.imageModeSwitch  ==1:
                self.imageModeSwitch = 0
                self.imageModeFrame.destroy()
                                
            self.ButtonForget()
            self.ButtonsMain()
            self.tableModeSwitch =1
            self.TableMode()
#          
#    def ChartBarFunction(self):        
#            
#            self.chartbar = ChartBar()
#            self.fonts = ['Helvetica','Arial']
#            self.font = self.fonts[0]
#            self.fontsizes = range(4,30)
#            descsize = 8
#            self.labelsize = 11
#            self.optionsize = 9
#            self.textAnchorOptions = ['start','middle','end']
#
#
#            self.chartDialogue = Frame(self.BaseFrame, relief=SUNKEN, bd=2,bg=self.backgroundcolor ) #Toplevel() #Tk()
#            self.chartDialogue.grid(row=0, column=0,rowspan=3,columnspan=4, padx = 1, sticky = W+E+N+S)
#
# 
#            
#            self.chartHolder = Frame(self.chartDialogue)
#            self.chartHolder.grid(row=0,column=0, columnspan = 5, rowspan=4)
#            self.demoCanvas = GraphWithScroll(self.chartHolder, self.wInfo.mapcanvasWidth/1.7, self.wInfo.graphCanvasHeight)
#            #self.demoCanvas.canvas.grid(row=0,column=0, columnspan = 3, rowspan=3)
#            self.demoCanvas.frame.grid(row=0,column=0, columnspan = 3, rowspan=3)
#            self.legendCanvas = Graph(self.chartHolder, 
#                                      self.wInfo.mapcanvasWidth-(self.wInfo.mapcanvasWidth/1.7), 
#                                      self.wInfo.graphCanvasHeight)
#            self.legendCanvas.canvas.grid(row=0,column=3, columnspan = 3, rowspan=3)
#                        
#            self.chartButtonCanvas = Canvas(self.chartDialogue)
#            self.chartButtonCanvas.grid(row=4,column=2)
#    
#            #self.chart_button_frame = Frame(self.chartHolder)
#            #self.chart_button_frame.grid(row= 3,column=0)
# 
#    
#            #self.chartDescriptionFrame = Frame(self.chartDialogue) #, width = 400,height = 25)
#            #self.chartDescriptionFrame.grid(row=1,column=2,pady=5)
# 
#            self.titleFrame = Frame(self.chartDialogue, width = 400,height = 25)
#            self.titleFrame.grid(row=4,column=0,pady=5) 
#            
#            self.bottom_frame = Frame(self.chartDialogue)
#            self.bottom_frame.grid(row= 4,column=3)
#
#            self.chartAdjustButtonsFrame = Frame(self.chartHolder)
#            self.chartAdjustButtonsFrame.grid(row=3,column=0)            
#
#
#            self.nextChartButton = Button(self.chartAdjustButtonsFrame,background="dark blue" ,foreground='white',width = 10, height = 3, text='Next', bd=3,relief='raised', command=self.chartView)
#            self.nextChartButton.grid(row=0,column=0) 
#
#            
#            self.acresButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Acres', bd=3,relief='raised', command=self.publish)
#            self.acresButton.grid(row=0,column=1)
#            self.hectaresButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Hectares', bd=3,relief='raised', command=self.publish)
#            self.hectaresButton.grid(row=0,column=2)
#          
#            self.metersButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Square\nMeters', bd=3,relief='raised', command=self.publish)
#            self.metersButton.grid(row=0,column=3)
#            
#            self.feetButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Square\nFeet', bd=3,relief='raised', command=self.publish)
#            self.feetButton.grid(row=0,column=4)            
#
#
#            self.modeButton = Button(self.chartAdjustButtonsFrame,background='dark green',foreground='white',width = 10, height = 3, text='Chart\nMode', bd=3,relief='raised', command=self.chartmodeswitch)
#            self.modeButton.grid(row=0,column=5) 
#            
#
#
#            #self.scrollbar = Scrollbar(self.chartDialogue)
#            #self.scrollbar.grid(row=0,column=5,rowspan=3)
#
#            #self.scrollbar.config(command=self.chartButtonCanvas.yview)
#
#            ylong=10
#            xlat=200
#
#
#
#
#            titlerow =1
#            self.titleLabel = Label(self.titleFrame, text = 'TITLE OF CHART'.title(), font =(self.font, self.labelsize))
#            self.titleLabel.grid(row=titlerow,column=0,pady=5,padx=5)
#            self.titletext = Text(self.titleFrame, width=50,height=2)
#            self.titletext.grid(row=titlerow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustTitleOptions )
#            self.OptionsButton.grid(row=titlerow,column=2,pady=5,padx=5)
#    
#            subrow = 2
#            self.subLabel = Label(self.titleFrame, text = 'SUBTITLE'.title(), font =(self.font, self.labelsize))
#            self.subLabel.grid(row=subrow,column=0,pady=5,padx=5)
#            self.subtext = Text(self.titleFrame, width=50,height=4)
#            self.subtext.grid(row=subrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustSubOptions)
#            self.OptionsButton.grid(row=subrow,column=2,pady=5,padx=5)
#            noterow = 6
#            self.noteLabel = Label(self.titleFrame, text = 'NOTES'.title(), font =(self.font, self.labelsize))
#            self.noteLabel.grid(row=noterow,column=0,pady=5,padx=5)
#            self.notetext = Text(self.titleFrame, width=50,height=4)
#            self.notetext.grid(row=noterow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustNoteOptions)
#            self.OptionsButton.grid(row=noterow,column=2,pady=5,padx=5)
#            yLabelrow =3
#            self.yLabelLabel = Label(self.titleFrame, text = 'Y AXIS LABEL'.title(), font =(self.font, self.labelsize))
#            self.yLabelLabel.grid(row=yLabelrow,column=0,pady=5,padx=5)
#            self.yLabelEntry = Entry(self.titleFrame, width=50)
#            self.yLabelEntry.grid(row=yLabelrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustYLabelOptions)
#            self.OptionsButton.grid(row=yLabelrow,column=2,pady=5,padx=5)
#            xLabelrow = 4
#            self.xLabelLabel = Label(self.titleFrame, text = 'X AXIS LABEL'.title(), font =(self.font, self.labelsize))
#            self.xLabelLabel.grid(row=xLabelrow,column=0,pady=5,padx=5)
#            self.xLabelEntry = Entry(self.titleFrame, width=50)
#            self.xLabelEntry.grid(row=xLabelrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustXLabelOptions)
#            self.OptionsButton.grid(row=xLabelrow,column=2,pady=5,padx=5)
#            legendRow = 5
##            self.legendLabel = Label(self.titleFrame, text = 'LEGEND'.title(), font =(self.font, self.labelsize))
##            self.legendLabel.grid(row=legendRow,column=0,pady=5,padx=5)
##            self.legendEntry = Entry(self.titleFrame, width=50)
##            self.legendEntry.grid(row=legendRow,column=1,pady=5,padx=5)
##            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustLegendOptions)
##            self.OptionsButton.grid(row=legendRow,column=2,pady=5,padx=5)
#            
#            self.titletext.insert(0.0,self.geoList[self.graphset][1].namestring)
#
#            
#                        
#            self.publishButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
#                                        text='PUBLISH\nKML', bd=3,relief='raised', command=self.publish)
#            self.publishButton.grid(row=0,column=0)
#            self.graphKMLButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
#                                        text='PUBLISH\nSHP', bd=3,relief='raised', command=self.publish)
#            self.graphKMLButton.grid(row=1,column=0)
#            self.graphSHPButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
#                                        text='PUBLISH\nCHART', bd=3,relief='raised', command=self.publish)
#            self.graphSHPButton.grid(row=2,column=0)
#            
##            self.backToMapButton = guiButton(self.bottom_frame, 'Map', self.buttonWidth, self.buttonHeight,  
##                                             self.guiButtonMgmt.buttons['Map']['filepath'],  self.ButtonMap)
##            self.backToMapButton.button.grid(row=0, column=5)    
##            
##            
#            self.chartCheck()  
#                
#            
#    def ChartBarFunction(self):        
#            
#            self.chartbar = ChartBar()
#            self.fonts = ['Helvetica','Arial']
#            self.font = self.fonts[0]
#            self.fontsizes = range(4,30)
#            descsize = 8
#            self.labelsize = 11
#            self.optionsize = 9
#            self.textAnchorOptions = ['start','middle','end']
#            self.chartfg = "white"
#            
#            self.chartDialogue = Frame(self.BaseFrame, relief=SUNKEN, bd=2,bg=self.backgroundcolor ) #Toplevel() #Tk()
#            self.chartDialogue.grid(row=0, column=0,rowspan=4,columnspan=6, padx = 1, sticky = W+E+N+S)
#
# 
#            
#            self.chartTitleTopFrame = Frame(self.chartDialogue,bg=self.backgroundcolor)
#            self.chartTitleTopFrame.grid(row=0,column=0,columnspan=6)
#            
#            titlerow =1
#            self.titleLabel = Label(self.chartTitleTopFrame, text = 'TITLE OF CHART'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
#            self.titleLabel.grid(row=titlerow,column=0,pady=5,padx=5)
#            self.titletext = Text(self.chartTitleTopFrame, width=50,height=2)
#            self.titletext.grid(row=titlerow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.chartTitleTopFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustTitleOptions )
#            self.OptionsButton.grid(row=titlerow,column=2,pady=5,padx=5)
#            subrow = 2
#            self.subLabel = Label(self.chartTitleTopFrame, text = 'SUBTITLE'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
#            self.subLabel.grid(row=subrow,column=0,pady=5,padx=5)
#            self.subtext = Text(self.chartTitleTopFrame, width=50,height=2)
#            self.subtext.grid(row=subrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.chartTitleTopFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustSubOptions)
#            self.OptionsButton.grid(row=subrow,column=2,pady=5,padx=5)
#     
#
#            
#            self.chartHolder = Frame(self.chartDialogue,bg=self.backgroundcolor)
#            self.chartHolder.grid(row=1,column=1, columnspan = 6, rowspan=4)
#            self.demoCanvas = GraphWithScroll(self.chartHolder, self.wInfo.mapcanvasWidth/1.4, self.wInfo.graphCanvasHeight* 1.5)
#            #self.demoCanvas.canvas.grid(row=0,column=0, columnspan = 3, rowspan=3)
#            self.demoCanvas.frame.grid(row=0,column=0, columnspan = 3, rowspan=3)
##            self.legendCanvas = Graph(self.chartHolder, 
##                                      self.wInfo.mapcanvasWidth-(self.wInfo.mapcanvasWidth/1.7), 
##                                      self.wInfo.graphCanvasHeight)
##            self.legendCanvas.canvas.grid(row=0,column=3, columnspan = 3, rowspan=3)
##                        
#
#
#            self.chartYValueFrame = Frame(self.chartDialogue,bg=self.backgroundcolor)
#            self.chartYValueFrame.grid(row=1,column=0, rowspan=3)
#
#            yLabelrow =3
#            self.yLabelLabel = Label(self.chartYValueFrame, text = 'Y AXIS LABEL'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
#            self.yLabelLabel.grid(row=0,column=0,pady=5,padx=5)
#            self.yLabelEntry = Entry(self.chartYValueFrame, width=10)
#            self.yLabelEntry.grid(row=1,column=0,pady=5,padx=5)
#            self.yLabelEntry.insert(0,"Acres")
#            self.OptionsButton = Button(self.chartYValueFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustYLabelOptions)
#            self.OptionsButton.grid(row=2,column=0,pady=5,padx=5)
#
#            self.chartXValueFrame = Frame(self.chartDialogue,bg=self.backgroundcolor)
#            self.chartXValueFrame.grid(row=1,column=7, rowspan=3)
#
#
#
#            #self.chart_button_frame = Frame(self.chartHolder)
#            #self.chart_button_frame.grid(row= 3,column=0)
# 
#            self.chartButtonCanvas = Canvas(self.chartDialogue,width=50,bg=self.backgroundcolor)
#            self.chartButtonCanvas.grid(row=1,column=8)    
#            #self.chartDescriptionFrame = Frame(self.chartDialogue) #, width = 400,height = 25)
#            #self.chartDescriptionFrame.grid(row=1,column=2,pady=5)
# 
#  
#            self.bottom_frame = Frame(self.chartDialogue,bg=self.backgroundcolor)
#            self.bottom_frame.grid(row= 4,column=8)
#            self.chartHolderBottom = Frame(self.chartHolder,bg=self.backgroundcolor)
#            self.chartHolderBottom.grid(row=3,column=0)
#            self.chartAdjustButtonsFrame = Frame(self.chartHolderBottom)
#            self.chartAdjustButtonsFrame.grid(row=1,column=0 ,columnspan=6)            
#
#
#            self.nextChartButton = Button(self.chartAdjustButtonsFrame,background="dark blue" ,foreground='white',width = 10, height = 3, text='Next', bd=3,relief='raised', command=self.chartView)
#            self.nextChartButton.grid(row=0,column=0) 
#
#            
#            self.acresButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Acres', bd=3,relief='raised', command=self.publish)
#            self.acresButton.grid(row=0,column=1)
#            self.hectaresButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Hectares', bd=3,relief='raised', command=self.publish)
#            self.hectaresButton.grid(row=0,column=2)
#          
#            self.metersButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Square\nMeters', bd=3,relief='raised', command=self.publish)
#            self.metersButton.grid(row=0,column=3)
#            
#            self.feetButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Square\nFeet', bd=3,relief='raised', command=self.publish)
#            self.feetButton.grid(row=0,column=4)            
#
#
#            self.modeButton = Button(self.chartAdjustButtonsFrame,background='dark green',foreground='white',width = 10, height = 3, text='Chart\nMode', bd=3,relief='raised', command=self.chartmodeswitch)
#            self.modeButton.grid(row=0,column=5) 
#            
#            self.chartFrameBottom = Frame(self.chartHolderBottom,bg=self.backgroundcolor)
#            self.chartFrameBottom.grid(row=0,column=0 ,columnspan=6)            
#            xLabelrow = 4
#            self.xLabelLabel = Label(self.chartFrameBottom, text = 'X AXIS LABEL'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
#            self.xLabelLabel.grid(row=0,column=0,pady=5,padx=5)
#            self.xLabelEntry = Entry(self.chartFrameBottom, width=50)
#            self.xLabelEntry.grid(row=0,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.chartFrameBottom, text='Options',font =(self.font, self.optionsize), command=self.adjustXLabelOptions)
#            self.OptionsButton.grid(row=0,column=2,pady=5,padx=5)
#
#            noterow = 1
#            self.noteLabel = Label(self.chartFrameBottom, text = 'NOTES'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
#            self.noteLabel.grid(row=noterow,column=0,pady=5,padx=5)
#            self.notetext = Text(self.chartFrameBottom, width=50,height=2)
#            self.notetext.grid(row=noterow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.chartFrameBottom, text='Options',font =(self.font, self.optionsize), command=self.adjustNoteOptions)
#            self.OptionsButton.grid(row=noterow,column=2,pady=5,padx=5)
#
#
#            ylong=10
#            xlat=200
#
#
#
#
#
#
#
#
#            legendRow = 5
##            self.legendLabel = Label(self.titleFrame, text = 'LEGEND'.title(), font =(self.font, self.labelsize))
##            self.legendLabel.grid(row=legendRow,column=0,pady=5,padx=5)
##            self.legendEntry = Entry(self.titleFrame, width=50)
##            self.legendEntry.grid(row=legendRow,column=1,pady=5,padx=5)
##            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustLegendOptions)
##            self.OptionsButton.grid(row=legendRow,column=2,pady=5,padx=5)
#            
#            self.titletext.insert(0.0,self.geoList[self.graphset][1].namestring)
#
#            
#                        
#            self.publishButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
#                                        text='PUBLISH\nKML', bd=3,relief='raised', command=self.publish)
#            self.publishButton.grid(row=0,column=0)
#            self.graphKMLButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
#                                        text='PUBLISH\nSHP', bd=3,relief='raised', command=self.publish)
#            self.graphKMLButton.grid(row=1,column=0)
#            self.graphSHPButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
#                                        text='PUBLISH\nCHART', bd=3,relief='raised', command=self.publish)
#            self.graphSHPButton.grid(row=2,column=0)
#            
##            self.backToMapButton = guiButton(self.bottom_frame, 'Map', self.buttonWidth, self.buttonHeight,  
##                                             self.guiButtonMgmt.buttons['Map']['filepath'],  self.ButtonMap)
##            self.backToMapButton.button.grid(row=0, column=5)    
##            
##            
#            self.chartCheck()  



    def ChartBarFunction(self):        
            
            self.chartbar = ChartBar()
            self.fonts = ['Helvetica','Arial']
            self.font = self.fonts[0]
            self.fontsizes = range(4,30)
            descsize = 8
            self.labelsize = 11
            self.optionsize = 9
            self.textAnchorOptions = ['start','middle','end']
            self.chartfg = "white"
            
            self.chartDialogue = Frame(self.BaseFrame, relief=SUNKEN, bd=2,bg=self.backgroundcolor ) #Toplevel() #Tk()
            self.chartDialogue.grid(row=0, column=0,rowspan=4,columnspan=6, padx = 1, sticky = W+E+N+S)

 
            
            self.chartTitleTopFrame = Frame(self.chartDialogue,bg=self.backgroundcolor)
            self.chartTitleTopFrame.grid(row=0,column=0,columnspan=6)
            

            self.chartHolder = Frame(self.chartDialogue,bg=self.backgroundcolor)
            self.chartHolder.grid(row=1,column=1, columnspan = 6, rowspan=4)
            self.demoCanvas = GraphWithScroll(self.chartHolder, self.wInfo.mapcanvasWidth, self.wInfo.graphCanvasHeight* 2)
            self.demoCanvas.frame.grid(row=0,column=0, columnspan = 3, rowspan=3)
            
            self.demoCanvas.canvas.tag_bind("title", '<ButtonPress-1>', self.adjustTitleOptionsProxy)  
            self.demoCanvas.canvas.tag_bind("yValue", '<ButtonPress-1>', self.adjustYLabelOptionsProxy)  
            self.demoCanvas.canvas.tag_bind("xValue", '<ButtonPress-1>', self.adjustXLabelOptionsProxy)  
            
            
            self.chartButtonCanvas = Canvas(self.chartDialogue,width=50,bg=self.backgroundcolor)
            self.chartButtonCanvas.grid(row=1,column=8)    

  
            self.bottom_frame = Frame(self.chartDialogue,bg=self.backgroundcolor)
            self.bottom_frame.grid(row= 4,column=8)
            self.chartHolderBottom = Frame(self.chartHolder,bg=self.backgroundcolor)
            self.chartHolderBottom.grid(row=3,column=0)
            self.chartAdjustButtonsFrame = Frame(self.chartHolderBottom)
            self.chartAdjustButtonsFrame.grid(row=0,column=0 ,columnspan=6)            


            self.nextChartButton = Button(self.chartAdjustButtonsFrame,background="dark blue" ,foreground='white',width = 10, height = 3, text='Next', bd=3,relief='raised', command=self.chartView)
            self.nextChartButton.grid(row=0,column=0) 

            
            self.acresButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Acres', bd=3,relief='raised', command=self.publish)
            self.acresButton.grid(row=0,column=1)
            self.hectaresButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Hectares', bd=3,relief='raised', command=self.publish)
            self.hectaresButton.grid(row=0,column=2)
          
            self.metersButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Square\nMeters', bd=3,relief='raised', command=self.publish)
            self.metersButton.grid(row=0,column=3)
            
            self.feetButton = Button(self.chartAdjustButtonsFrame,background='dark red',foreground='white',width = 10, height = 3, text='Square\nFeet', bd=3,relief='raised', command=self.publish)
            self.feetButton.grid(row=0,column=4)            


            self.modeButton = Button(self.chartAdjustButtonsFrame,background='dark green',foreground='white',width = 10, height = 3, text='Chart\nMode', bd=3,relief='raised', command=self.chartmodeswitch)
            self.modeButton.grid(row=0,column=5) 
            
            self.chartFrameBottom = Frame(self.chartHolderBottom,bg=self.backgroundcolor)
            self.chartFrameBottom.grid(row=0,column=0 ,columnspan=6)            

            ylong=10
            xlat=200
                        
            self.publishButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
                                        text='PUBLISH\nKML', bd=3,relief='raised', command=self.publish)
            self.publishButton.grid(row=0,column=0)
            self.graphKMLButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
                                        text='PUBLISH\nSHP', bd=3,relief='raised', command=self.publish)
            self.graphKMLButton.grid(row=1,column=0)
            self.graphSHPButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 10, height = 3, 
                                        text='PUBLISH\nCHART', bd=3,relief='raised', command=self.publish)
            self.graphSHPButton.grid(row=2,column=0)
            
        
            self.chartCheck()  




 

 
                            
    def ByTypeAllProxy(self):
        model = self.currentGraphModel
        func = self.ByTypeAll(model)

    def ByTypeAll(self,geoObject):
        data = get_geoObjectType(geoObject)
        return data
    

    def ByPropertyAllProxy(self):
        model = self.currentGraphModel
        data = self.ByPropertyAll(model)
        datalist = []
        print data
        for property in data:
            print property
            for datavalues in data[property]:
                for datavalue in datavalues:
                    
                    
                    
                    area = datavalue.Geometry.area
                    print area
                    datalist.append(area) 
        self.ChartGen(datalist, "%s By Property" % model.namestring)
        
    def ByPropertyAll(self, geoObject):
        data = get_OrderedGeoObjectsWithin( AcquisitionProperties,geoObject)
        return data
       
        
    def ByManagementUnitAllProxy(self):
        model = self.currentGraphModel
        func = self.ByManagementUnitAll(model)

    def ByManagementUnitAll(self, geoObject):
        data = get_OrderedGeoObjectsWithin( ManagementUnit,geoObject)
        return data

    
    def ByAnimalAllProxy(self):
        model = self.currentGraphModel        
        func = self.ByAnimalAll(model)  
                            
    def ByAnimalAll(self,geoObject):
        data = get_geoObjectType(geoObject)
        return data


    def ByLandCoverAllProxy(self):
        model = self.currentGraphModel
        func = self.ByLandCoverAll(model)

    def ByLandCoverAll(self,geoObject):
        data = get_geoObjectLandCover(geoObject)
        return data  
    
    
    def ByChangeAllProxy(self):
        model = self.currentGraphModel
        func = self.ByChangeAll(model) 
        
    
    def ByTreatmentAllProxy(self):
        model = self.currentGraphModel
        func = self.ByTreatmentAll(model)        


    def ByOwnerAllProxy(self):
        model = self.currentGraphModel        
        func = self.ByOwnerAll(model)  

    def ByOwnerAll(self,geoObject):
        data = get_geoObjectType(geoObject)
        return data


    def ByDateAllProxy(self):
        model = self.currentGraphModel
        func = self.ByDateAll(model)


    def ByDateAll(self,geoObject):
        data = get_geoObjectType(geoObject)
        return data
                         
    def ByDateCurrentProxy(self):
        model = self.currentGraphModel
        func = self.ByDateCurrent(model)

    def ByManagementUnitCurrentProxy(self):
        model = self.currentGraphModel
        func = self.ByManagementUnitCurrent(model)  

    def ByTypeCurrentProxy(self):
        model = self.currentGraphModel
        func = self.ByTypeCurrent(model)
        
    def ByPropertyCurrentProxy(self):
        model = self.currentGraphModel
        data = self.ByPropertyCurrent(model)
        datalist = []
        for property in data:
            for datavalue in data[property]:
                datalist.append(datavalue.Geometry.area) 
        self.ChartGen(datalist, "%s By Property" % model.namestring)
        
    def ByPropertyCurrent(self, geoObject):
        data = get_OrderedGeoObjectsWithinSort(AcquisitionProperties,geoObject, self.zoomer.currentPolyString )
        return data


       
    def ByLandCoverCurrentProxy(self):
        model = self.currentGraphModel
        self.ByLandCoverCurrent(model)

    def ByOwnerCurrentProxy(self):
        model = self.currentGraphModel
        self.ByOwnerCurrent(model)  

    def ByAnimalCurrentProxy(self):
        model = self.currentGraphModel
        self.ByAnimalCurrent(model) 
        
    def ByChangeCurrentProxy(self):
        model = self.currentGraphModel
        self.ByChangeCurrent(model)

    def ByTreatmentCurrentProxy(self):
        model = self.currentGraphModel        
        self.ByTreatmentCurrent(model)
        
        

            




    











    def ByManagementUnitCurrent(self, geoObject):
        data = get_OrderedGeoObjectsWithinSort(geoObject, self.zoomer.currentPolyString )
        return data
    
    def ByTypeCurrent(self,geoObject):
        data = get_OrderedGeoObjectsWithinSort(geoObject, self.zoomer.currentPolyString )
        return data

    def ByDateCurrent(self,geoObject):
        data = get_OrderedGeoObjectsWithinSort(geoObject, self.zoomer.currentPolyString )
        return data

    def ByAnimalCurrent(self,geoObject):
        data = get_OrderedGeoObjectsWithinSort(geoObject, self.zoomer.currentPolyString )
        return data

    def ByOwnerCurrent(self,geoObject):
        data = get_OrderedGeoObjectsWithinSort(geoObject, self.zoomer.currentPolyString )
        return data    

    def ByLandCoverCurrent(self,geoObject):
        data = get_OrderedGeoObjectsWithinSort(geoObject, self.zoomer.currentPolyString )
        return data  

    def insert(self, title,modelist):
        self.subtext.delete(0.0,END)
        self.subtext.insert(END, 'By ' + title)
        #self.chartDescriptionStringVar.set(title) 
        self.tablesToProcess = modelist
    
#    def ChartBarFunction(self):        
#            self.chartSwitch = 1
#            self.chartbar = ChartBar()
#            self.fonts = ['Helvetica','Arial']
#            self.font = self.fonts[0]
#            self.fontsizes = range(4,22)
#            descsize = 8
#


#
#            datarow =0
#
#
#            self.PropertyButton = Button(self.data_adjust_frame, text='Organize\nBy\nProperty',font =(self.font, self.optionsize))
#            self.PropertyButton.grid(row=datarow,column=2,pady=5,padx=5)
#            
#            datarow =1
#
#
#            self.ManagementButton = Button(self.data_adjust_frame, text='Organize\nBy\nManagement\nUnit',font =(self.font, self.optionsize))
#            self.ManagementButton.grid(row=datarow,column=2,pady=5,padx=5)            
#            
#            datarow = 2
#
#
#            self.AreaButton = Button(self.data_adjust_frame, text='Organize\nBy\nTotal\nArea',font =(self.font, self.optionsize))
#            self.AreaButton.grid(row=datarow,column=2,pady=5,padx=5)          
#            
#            datarow = 0
#
#
#            self.DateOlderButton = Button(self.data_adjust_frame, text='Organize\nBy\nDate\n(Oldest)',font =(self.font, self.optionsize))
#            self.DateOlderButton.grid(row=datarow,column=3,pady=5,padx=5) 
#            
#            datarow = 1
#
#
#            self.DateNewerButton = Button(self.data_adjust_frame, text='Organize\nBy\nDate\n(Newest)',font =(self.font, self.optionsize))
#            self.DateNewerButton.grid(row=datarow,column=3,pady=5,padx=5)             
#
#            datarow = 0
#
#
#            self.DataMetersButton = Button(self.data_adjust_frame, text='Show\nIn\nSquare\nMeters',font =(self.font, self.optionsize))
#            self.DataMetersButton.grid(row=datarow,column=4,pady=5,padx=5)             
#
#            datarow = 1
#
#
#            self.DataMetersButton = Button(self.data_adjust_frame, text='Show\nIn\nAcres',font =(self.font, self.optionsize))
#            self.DataMetersButton.grid(row=datarow,column=4,pady=5,padx=5)             
#
#            datarow = 2
#
#
#            self.DataMetersButton = Button(self.data_adjust_frame, text='Show\nIn\nSquare\nFeet',font =(self.font, self.optionsize))
#            self.DataMetersButton.grid(row=datarow,column=4,pady=5,padx=5)     
#    
 
    
#            fontrow = 0
#            self.fontvariable = StringVar(self.titleFrame)
#            self.fontLabel = Label(self.titleFrame, text = 'FONT OF CHART', font =(self.font, 13))
#            self.fontLabel.grid(row=fontrow,column=0,pady=5,padx=5)
#    
#    
#            self.fontOptions =  apply(OptionMenu, (self.titleFrame,self.fontvariable) + tuple(self.fonts))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
#            self.fontvariable.set(self.fonts[0])
#            self.fontOptions.grid(row=fontrow,column=1,pady=5,padx=5)

#            self.map.canvas.grid_forget()
#            self.graph.canvas.grid_forget()
#            
#            self.picWindow.canvas.grid_forget()
#            
#            self.chartDialogue = Frame(self.BaseFrame) #Toplevel() #Tk()
#            self.chartDialogue.grid(row=0, column=0,rowspan=5,columnspan=4, padx = 1, sticky = W+E+N+S)
#
#            self.ButtonForget()
#            self.graphButton.grid_forget()
#            self.graphButton2.grid_forget()
#            
#            self.demoCanvas = Graph(self.chartDialogue, self.wInfo.mapcanvasWidth/2, self.wInfo.graphCanvasHeight)
#            self.demoCanvas.canvas.grid(row=0,column=0, columnspan = 3)
#            self.graph = self.demoCanvas
#            self.graphCheck()
#            self.textAnchorOptions = ['start','middle','end']
#    
#    
#            self.titleFrame = Frame(self.chartDialogue, width = 400,height = 25)
#            self.titleFrame.grid(row=1,column=0,pady=5)
#    
#            self.chart_button_frame = Frame(self.chartDialogue)
#            self.chart_button_frame.grid(row= 1,column=1, columnspan=4,rowspan=2)
#    
#            self.chartDescriptionFrame = Frame(self.chartDialogue) #, width = 400,height = 25)
#            self.chartDescriptionFrame.grid(row=1,column=2,pady=5)
#
#            self.bottom_frame = Frame(self.chartDialogue)
#            self.bottom_frame.grid(row= 2,column=1, columnspan=4)
#
#
#            #self.data_adjust_frame = Frame(self.chartDialogue)
#            #self.data_adjust_frame.grid(row= 0,column=4, rowspan=3)
#
#
#            self.labelsize = 11
#            self.optionsize = 9
#
#            def makeFunc(title, masterfunc,modelist):
#                class tableInfo(object):
#                    def __init__(self, title,masterfunc):
#                        self.title = title
#                        self.masterfunc = masterfunc
#                        self.modelist = modelist
#                    def backfunc(self):
#                        self.masterfunc(self.title,self.modelist)
#                        
#                instatiation = tableInfo(title, masterfunc)
#                return instatiation
#
#            self.scrollbar = Scrollbar(self.chartDialogue)
#            self.scrollbar.grid(row=0,column=5)
#            self.chartButtonCanvas = Canvas(self.chartDialogue, width=300,height=500,relief=SUNKEN)
#            self.chartButtonCanvas.grid(row=0,column=4, rowspan=3)
#            self.scrollbar.config(command=self.chartButtonCanvas.yview)
#
#            
#            for model in self.geoList:
#                title = model.name
#                func = makeFunc(title, self.insert,[model])
#                button = Button(self.chartButtonCanvas,background='tan',foreground='SlateBlue4',width = 30, height = 2, text=title, bd=3,relief='raised', command=func.backfunc)
#                self.chartButtonCanvas.create_window(20,ylong,window=button, anchor="nw")
#                ylong += 50
#
#
#
#
#
##
##            datarow =0
##
##
##            self.PropertyButton = Button(self.data_adjust_frame, text='Organize\nBy\nProperty',font =(self.font, self.optionsize))
##            self.PropertyButton.grid(row=datarow,column=2,pady=5,padx=5)
##            
##            datarow =1
##
##
##            self.ManagementButton = Button(self.data_adjust_frame, text='Organize\nBy\nManagement\nUnit',font =(self.font, self.optionsize))
##            self.ManagementButton.grid(row=datarow,column=2,pady=5,padx=5)            
##            
##            datarow = 2
##
##
##            self.AreaButton = Button(self.data_adjust_frame, text='Organize\nBy\nTotal\nArea',font =(self.font, self.optionsize))
##            self.AreaButton.grid(row=datarow,column=2,pady=5,padx=5)          
##            
##            datarow = 0
##
##
##            self.DateOlderButton = Button(self.data_adjust_frame, text='Organize\nBy\nDate\n(Oldest)',font =(self.font, self.optionsize))
##            self.DateOlderButton.grid(row=datarow,column=3,pady=5,padx=5) 
##            
##            datarow = 1
##
##
##            self.DateNewerButton = Button(self.data_adjust_frame, text='Organize\nBy\nDate\n(Newest)',font =(self.font, self.optionsize))
##            self.DateNewerButton.grid(row=datarow,column=3,pady=5,padx=5)             
##
##            datarow = 0
##
##
##            self.DataMetersButton = Button(self.data_adjust_frame, text='Show\nIn\nSquare\nMeters',font =(self.font, self.optionsize))
##            self.DataMetersButton.grid(row=datarow,column=4,pady=5,padx=5)             
##
##            datarow = 1
##
##
##            self.DataMetersButton = Button(self.data_adjust_frame, text='Show\nIn\nAcres',font =(self.font, self.optionsize))
##            self.DataMetersButton.grid(row=datarow,column=4,pady=5,padx=5)             
##
##            datarow = 2
##
##
##            self.DataMetersButton = Button(self.data_adjust_frame, text='Show\nIn\nSquare\nFeet',font =(self.font, self.optionsize))
##            self.DataMetersButton.grid(row=datarow,column=4,pady=5,padx=5)     
##    
#    
#    
#            fontrow = 0
#            self.fontvariable = StringVar(self.titleFrame)
#            self.fontLabel = Label(self.titleFrame, text = 'FONT OF CHART', font =(self.font, 13))
#            self.fontLabel.grid(row=fontrow,column=0,pady=5,padx=5)
#    
#    
#            self.fontOptions =  apply(OptionMenu, (self.titleFrame,self.fontvariable) + tuple(self.fonts))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
#            self.fontvariable.set(self.fonts[0])
#            self.fontOptions.grid(row=fontrow,column=1,pady=5,padx=5)
#
#    
#            titlerow =1
#            self.titleLabel = Label(self.titleFrame, text = 'TITLE OF CHART'.title(), font =(self.font, self.labelsize))
#            self.titleLabel.grid(row=titlerow,column=0,pady=5,padx=5)
#            self.titletext = Text(self.titleFrame, width=50,height=2)
#            self.titletext.grid(row=titlerow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustTitleOptions )
#            self.OptionsButton.grid(row=titlerow,column=2,pady=5,padx=5)
#    
#            subrow = 2
#            self.subLabel = Label(self.titleFrame, text = 'SUBTITLE'.title(), font =(self.font, self.labelsize))
#            self.subLabel.grid(row=subrow,column=0,pady=5,padx=5)
#            self.subtext = Text(self.titleFrame, width=50,height=4)
#            self.subtext.grid(row=subrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustSubOptions)
#            self.OptionsButton.grid(row=subrow,column=2,pady=5,padx=5)
#            noterow = 6
#            self.noteLabel = Label(self.titleFrame, text = 'NOTES'.title(), font =(self.font, self.labelsize))
#            self.noteLabel.grid(row=noterow,column=0,pady=5,padx=5)
#            self.notetext = Text(self.titleFrame, width=50,height=4)
#            self.notetext.grid(row=noterow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustNoteOptions)
#            self.OptionsButton.grid(row=noterow,column=2,pady=5,padx=5)
#            yLabelrow =3
#            self.yLabelLabel = Label(self.titleFrame, text = 'Y AXIS LABEL'.title(), font =(self.font, self.labelsize))
#            self.yLabelLabel.grid(row=yLabelrow,column=0,pady=5,padx=5)
#            self.yLabelEntry = Entry(self.titleFrame, width=50)
#            self.yLabelEntry.grid(row=yLabelrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustYLabelOptions)
#            self.OptionsButton.grid(row=yLabelrow,column=2,pady=5,padx=5)
#            xLabelrow = 4
#            self.xLabelLabel = Label(self.titleFrame, text = 'X AXIS LABEL'.title(), font =(self.font, self.labelsize))
#            self.xLabelLabel.grid(row=xLabelrow,column=0,pady=5,padx=5)
#            self.xLabelEntry = Entry(self.titleFrame, width=50)
#            self.xLabelEntry.grid(row=xLabelrow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustXLabelOptions)
#            self.OptionsButton.grid(row=xLabelrow,column=2,pady=5,padx=5)
#            legendRow = 5
#            self.legendLabel = Label(self.titleFrame, text = 'LEGEND'.title(), font =(self.font, self.labelsize))
#            self.legendLabel.grid(row=legendRow,column=0,pady=5,padx=5)
#            self.legendEntry = Entry(self.titleFrame, width=50)
#            self.legendEntry.grid(row=legendRow,column=1,pady=5,padx=5)
#            self.OptionsButton = Button(self.titleFrame, text='Options',font =(self.font, self.optionsize), command=self.adjustLegendOptions)
#            self.OptionsButton.grid(row=legendRow,column=2,pady=5,padx=5)
#            
#            
#            geoList = [GrazedAreas, Wetlands, InvasiveSpecies, Issues]
#            #self.grazedic = get_OrderedGeoObjectsWithin(AcquisitionProperties, GrazedAreas)
#            #self.wetlandic = get_OrderedGeoObjectsWithin(AcquisitionProperties, Wetlands)
#            #self.invasivedic = get_OrderedGeoObjectsWithin(AcquisitionProperties, InvasiveSpecies)
#            #self.issuedic = get_OrderedGeoObjectsWithin(AcquisitionProperties, Issues)
#            
#            
#            self.types_dic = {'Point in Polygon':[[AcquisitionProperties, Issues]],
#                             'Line in Polygon':[],
#                             'Polygon in Polygon': [[AcquisitionProperties, GrazedAreas], [AcquisitionProperties, Wetlands], [AcquisitionProperties, InvasiveSpecies],],
#                             'Point': [Issues],
#                             'Polygon':[GrazedAreas,Wetlands, InvasiveSpecies ]
#                             }
#            #self.scrollbar = Scrollbar(self.chartDialogue)
#            #self.scrollbar.grid(row=4)
#            #self.chartButtonCanvas = Canvas(self.chartDialogue, width=300,height=500,relief=SUNKEN)
#            #self.chartButtonCanvas.grid(row=1,column=0)
#            #self.scrollbar.config(command=self.chartButtonCanvas.yview)
#            ylong=10
#            xlat=200
#
#
#
#
##            geomtypes = ['Point','Linestring','Polygon']
##            for types in self.types_dic:
##                if types in geomtypes:
##                    for model in self.types_dic[types]:
##                                title = model.__name__
##                                func = makeFunc(title, self.insert,[model])
##                                button = Button(self.chartDialogue,background='tan',foreground='SlateBlue4',width = 30, height = 2, text=title, bd=3,relief='raised', command=func.backfunc)
##                                self.chartButtonCanvas.create_window(20,ylong,window=button, anchor="nw")
##                                ylong += 50
##                else:
##                    for modelist in self.types_dic[types]:
##
##                        base = modelist[0]
##                        layer= modelist[1]
##                        title = layer.__name__  + ' by ' + base.__name__
##                        func = makeFunc(title, self.insert,modelist)
##                        button = Button(self.chartDialogue,background='SlateBlue4',foreground='white',width = 30, height = 2, text=title, bd=3,relief='raised', command=func.backfunc)
##                        self.chartButtonCanvas.create_window(20,ylong,window=button, anchor="nw")
##                        ylong += 50                    
#            self.publishButton = Button(self.bottom_frame,background='dark green',foreground='white',width = 30, height = 3, text='PUBLISH', bd=3,relief='raised', command=self.publish)
#            self.publishButton.grid(row=0,column=4)
    def adjustTitleOptionsProxy(self,event):
            self.adjustTitleOptions()

    def adjustTitleOptions(self):
            titlerow = 0
            self.titleOptionDialogue = Toplevel()
            self.titleOptionDialogue.title('Adjust Options')
            
            self.titleLabel = Label(self.titleOptionDialogue, text = 'TITLE OF CHART'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
            self.titleLabel.grid(row=titlerow,column=0,pady=5,padx=5)
            
            self.titletext = Text(self.titleOptionDialogue, width=50,height=2)
            self.titletext.grid(row=titlerow,column=1,pady=5,padx=5)
            fontsizerow = 2
            self.titlefontsizeval = StringVar(self.titleOptionDialogue)
            self.titleFontSizeLabel = Label(self.titleOptionDialogue, text = 'Font Size', font =(self.font, self.optionsize))
            self.titleFontSizeLabel.grid(row=fontsizerow,column=2,pady=5,padx=5)
            self.titlesizeOptions =  apply(OptionMenu, (self.titleOptionDialogue,self.titlefontsizeval) + tuple(self.fontsizes))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
            self.titlefontsizeval.set(11)
            self.titlesizeOptions.grid(row=fontsizerow,column=3,pady=5,padx=5)
            #self.title.x          = self.drawing.width/2 
            #self.title.y          = self.drawing.height - 1 * cm
            anchorrow = 3
            self.titleAnchorLabel = Label(self.titleOptionDialogue, text = 'Font Anchor', font =(self.font, self.optionsize))
            self.titleAnchorLabel.grid(row=anchorrow,column=2,pady=5,padx=5)        
            self.titleTextAnchorStringVar = StringVar()
            self.titleTextAnchorOptions =  apply(OptionMenu, (self.titleOptionDialogue,self.titleTextAnchorStringVar) + tuple(self.textAnchorOptions))
            self.titleTextAnchorOptions.grid(row=anchorrow,column=3,pady=5,padx=5)
            self.titleTextAnchorStringVar.set(self.textAnchorOptions[1])
    
            setrow = 10
            self.setTitleOptionsButton = Button(self.titleOptionDialogue, text = 'Set Options',font =(self.font, self.optionsize),command=self.chartbarTitleSetFunction)
            self.setTitleOptionsButton.grid(row=setrow,column=2,columnspan=2)
    
    def chartbarTitleSetFunction(self):
        self.chartbar.titleSetFunction(self.titlefont.get(),
                                       self.titlefontsizeval.get(),
                                       
                                       500,
                                       50,
                                       self.titleTextAnchorStringVar.get(),
                                       )
        
    def adjustSubOptionsProxy(self,event):
            self.adjustSubOptions()    
    def adjustSubOptions(self):        
            
            self.subOptionDialogue = Toplevel()
            self.subOptionDialogue.title('Adjust Options')
            subrow = 0
            self.subLabel = Label(self.subOptionDialogue, text = 'SUBTITLE'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
            self.subLabel.grid(row=subrow,column=0,pady=5,padx=5)
            self.subtext = Text(self.subOptionDialogue, width=50,height=2)
            self.subtext.grid(row=subrow,column=1,pady=5,padx=5)
            self.subfontsizeval = StringVar(self.subOptionDialogue)
            fontsizerow = 2
            self.subFontSizeLabel = Label(self.subOptionDialogue, text = 'Font Size', font =(self.font, self.optionsize))
            self.subFontSizeLabel.grid(row=fontsizerow,column=2,pady=5,padx=5)
            self.subsizeOptions =  apply(OptionMenu, (self.subOptionDialogue,self.subfontsizeval) + tuple(self.fontsizes))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
            self.subfontsizeval.set(11)
            self.subsizeOptions.grid(row=fontsizerow,column=3,pady=5,padx=5)
            anchorrow = 3
            self.subAnchorLabel = Label(self.subOptionDialogue, text = 'Font Anchor', font =(self.font, self.optionsize))
            self.subAnchorLabel.grid(row=anchorrow,column=2,pady=5,padx=5)        
            self.subTextAnchorStringVar = StringVar()
            self.subTextAnchorOptions =  apply(OptionMenu, (self.subOptionDialogue,self.subTextAnchorStringVar) + tuple(self.textAnchorOptions))
            self.subTextAnchorOptions.grid(row=anchorrow,column=3,pady=5,padx=5)
            self.subTextAnchorStringVar.set(self.textAnchorOptions[1])
    
            setrow = 10
            self.setTitleOptionsButton = Button(self.titleOptionDialogue, text = 'Set Options',font =(self.font, self.optionsize), command= self.chartbar.subtitleSetFunction )
            self.setTitleOptionsButton.grid(row=setrow,column=2,columnspan=2)
    
    
    def chartbarSubSetFunction(self):
        self.chartbar.subtitleSetFunction(self.subfont.get(),
                                          self.subfontsizeval.get(),
                                       
                                          500,
                                          100,
                                          self.subTextAnchorStringVar.get(),
                                          )    
    def adjustNoteOptionsProxy(self,event):
            self.adjustNoteOptions()       
    def adjustNoteOptions(self):        
            
            self.noteOptionDialogue = Toplevel()
            self.noteOptionDialogue.title('Adjust Options')
            
            noterow = 0
            self.noteLabel = Label(self.chartFrameBottom, text = 'NOTES'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
            self.noteLabel.grid(row=noterow,column=0,pady=5,padx=5)
            self.notetext = Text(self.chartFrameBottom, width=50,height=2)
            self.notetext.grid(row=noterow,column=1,pady=5,padx=5)
            fontsizerow = 2
            self.notefontsizeval = StringVar(self.noteOptionDialogue)
            self.noteFontSizeLabel = Label(self.noteOptionDialogue, text = 'Font Size', font =(self.font, self.optionsize))
            self.noteFontSizeLabel.grid(row=fontsizerow,column=2,pady=5,padx=5)
            self.notesizeOptions =  apply(OptionMenu, (self.noteOptionDialogue,self.notefontsizeval) + tuple(self.fontsizes))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
            self.notefontsizeval.set(11)
            self.notesizeOptions.grid(row=fontsizerow,column=3,pady=5,padx=5)
            anchorrow = 3
            self.noteAnchorLabel = Label(self.noteOptionDialogue, text = 'Font Anchor', font =(self.font, self.optionsize))
            self.noteAnchorLabel.grid(row=anchorrow,column=2,pady=5,padx=5)        
            self.noteTextAnchorStringVar = StringVar()
            self.noteTextAnchorOptions =  apply(OptionMenu, (self.noteOptionDialogue,self.noteTextAnchorStringVar) + tuple(self.textAnchorOptions))
            self.noteTextAnchorOptions.grid(row=anchorrow,column=3,pady=5,padx=5)
            self.noteTextAnchorStringVar.set(self.textAnchorOptions[1])
    
            setrow = 10
            self.setnoteOptionsButton = Button(self.noteOptionDialogue, text = 'Set Options',font =(self.font, self.optionsize), command=self.chartbar.noteSetFunction)
            self.setnoteOptionsButton.grid(row=setrow,column=2,columnspan=2)
    
    
    
    def adjustYLabelOptionsProxy(self,event):
            self.adjustYLabelOptions()         
    def adjustYLabelOptions(self):        
            
            self.yLabelOptionDialogue = Toplevel()
            self.yLabelOptionDialogue.title('Adjust Options')
            
            
            yLabelrow =0
            self.yLabelLabel = Label(self.yLabelOptionDialogue, text = 'Y AXIS LABEL'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
            self.yLabelLabel.grid(row=0,column=0,pady=5,padx=5)
            self.yLabelEntry = Entry(self.yLabelOptionDialogue, width=10)
            self.yLabelEntry.grid(row=1,column=0,pady=5,padx=5)
            self.yLabelEntry.insert(0,"Acres")
            fontsizerow = 2
            self.yLabelfontsizeval = StringVar(self.yLabelOptionDialogue)
            self.yLabelFontSizeLabel = Label(self.yLabelOptionDialogue, text = 'Font Size', font =(self.font, self.optionsize))
            self.yLabelFontSizeLabel.grid(row=fontsizerow,column=2,pady=5,padx=5)
            self.yLabelsizeOptions =  apply(OptionMenu, (self.yLabelOptionDialogue,self.yLabelfontsizeval) + tuple(self.fontsizes))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
            self.yLabelfontsizeval.set(11)
            self.yLabelsizeOptions.grid(row=fontsizerow,column=3,pady=5,padx=5)
    
            anchorrow = 1
            self.yLabelAnchorLabel = Label(self.yLabelOptionDialogue, text = 'Font Anchor', font =(self.font, self.optionsize))
            self.yLabelAnchorLabel.grid(row=anchorrow,column=2,pady=5,padx=5)        
            self.yLabelTextAnchorStringVar = StringVar()
            self.yLabelTextAnchorOptions =  apply(OptionMenu, (self.yLabelOptionDialogue,self.yLabelTextAnchorStringVar) + tuple(self.textAnchorOptions))
            self.yLabelTextAnchorOptions.grid(row=anchorrow,column=3,pady=5,padx=5)
            self.yLabelTextAnchorStringVar.set(self.textAnchorOptions[1])
    
            setrow = 10
            self.setyLabelOptionsButton = Button(self.yLabelOptionDialogue, text = 'Set Options',font =(self.font, self.optionsize), command=self.chartbar.YlabelSetFunction)
            self.setyLabelOptionsButton.grid(row=setrow,column=2,columnspan=2)
    
    
    def adjustXLabelOptionsProxy(self,event):
            self.adjustXLabelOptions()         

    def adjustXLabelOptions(self):        
            
            self.xLabelOptionDialogue = Toplevel()
            self.xLabelOptionDialogue.title('Adjust Options')
            
            xLabelrow = 0
            self.xLabelLabel = Label(self.xLabelOptionDialogue, text = 'X AXIS LABEL'.title(), font =(self.font, self.labelsize),fg = self.chartfg,bg=self.backgroundcolor)
            self.xLabelLabel.grid(row=0,column=0,pady=5,padx=5)
            self.xLabelEntry = Entry(self.xLabelOptionDialogue, width=50)
            self.xLabelEntry.grid(row=0,column=1,pady=5,padx=5)
            fontsizerow = 2
            self.xLabelfontsizeval = StringVar(self.xLabelOptionDialogue)
            self.xLabelFontSizeLabel = Label(self.xLabelOptionDialogue, text = 'Font Size', font =(self.font, self.optionsize))
            self.xLabelFontSizeLabel.grid(row=fontsizerow,column=2,pady=5,padx=5)
            self.xLabelsizeOptions =  apply(OptionMenu, (self.xLabelOptionDialogue,self.xLabelfontsizeval) + tuple(self.fontsizes))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
            self.xLabelfontsizeval.set(11)
            self.xLabelsizeOptions.grid(row=fontsizerow,column=3,pady=5,padx=5)
    
            anchorrow = 1
            self.xLabelAnchorLabel = Label(self.xLabelOptionDialogue, text = 'Font Anchor', font =(self.font, self.optionsize))
            self.xLabelAnchorLabel.grid(row=anchorrow,column=2,pady=5,padx=5)        
            self.xLabelTextAnchorStringVar = StringVar()
            self.xLabelTextAnchorOptions =  apply(OptionMenu, (self.xLabelOptionDialogue,self.xLabelTextAnchorStringVar) + tuple(self.textAnchorOptions))
            self.xLabelTextAnchorOptions.grid(row=anchorrow,column=3,pady=5,padx=5)
            self.xLabelTextAnchorStringVar.set(self.textAnchorOptions[1])
    
    
            setrow = 10
            self.setxLabelOptionsButton = Button(self.xLabelOptionDialogue, text = 'Set Options',font =(self.font, self.optionsize), command=self.chartbar.XcategoryaxisSetFunction)
            self.setxLabelOptionsButton.grid(row=setrow,column=2,columnspan=2)
    
    def adjustLegendOptionsProxy(self,event):
            self.adjustLegendOptions()         
    def adjustLegendOptions(self):        
            fontsizerow = 0
            self.legendOptionDialogue = Toplevel()
            self.legendOptionDialogue.title('Adjust Options')
            self.legendfontsizeval = StringVar(self.legendOptionDialogue)
            self.legendFontSizeLabel = Label(self.legendOptionDialogue, text = 'Font Size', font =(self.font, self.optionsize))
            self.legendFontSizeLabel.grid(row=fontsizerow,column=2,pady=5,padx=5)
            self.legendsizeOptions =  apply(OptionMenu, (self.legendOptionDialogue,self.legendfontsizeval) + tuple(self.fontsizes))  #OptionMenu(self.chartDialogue,self.fontvariable,self.fonts)
            self.legendfontsizeval.set(11)
            self.legendsizeOptions.grid(row=fontsizerow,column=3,pady=5,padx=5)
    

                                  
                

        
        ##
    def publish(self):
                
                if  self.notetext.get(0.0,END) !='':
                    self.chartbar.note._text  = self.notetext.get(0.0,END)
        
                    self.chartbar.drawing.add(self.chartbar.note)
                if self.yLabelEntry.get() !='':
                    self.chartbar.yLabel._text = self.yLabelEntry.get() 
        
                    self.chartbar.drawing.add(self.chartbar.yLabel)
                if self.xLabelEntry.get() !='':
                    self.chartbar.xLabel._text          = self.xLabelEntry.get()
                    self.chartbar.drawing.add(self.chartbar.xLabel)
                if self.subtext.get(0.0,END) !='':
                    self.chartbar.description._text = self.subtext.get(0.0,END)
        
                    self.chartbar.drawing.add(self.chartbar.description)
                if self.titletext.get(0.0,END) !='':
                    self.chartbar.title._text = self.titletext.get(0.0,END) 
                    self.chartbar.drawing.add(self.chartbar.title)
                    
        #        self.legendColorList = [(colors.green, 'Acquisitions to date'),(colors.lightgreen, 'Progress toward estimated Preserve System')]
        #        
        #        for set in self.legendColorList:
        #            
        #            self.legend.colorNamePairs = self.legendColorList
        #            self.legend.fontName       = self.font
        #            self.legend.fontSize       = 12#self.legendfontsizeval.get()
        #            
        #            self.legend.x              = (2 * inch) + (2.5* inch *  self.legendColorList.index(set))
        #            self.legend.y              = .8* inch 
        #    
        #            
        #            self.legend.deltay         = 10
        #            self.legend.alignment      ='right'
                    
                #data = self.dataPrep()
#                maxval=0
#                for COUNTER, vals in enumerate(data):
#                    if max(vals) > maxval:
#                        maxval = max(vals) 
#                print maxval, 'maxval'
#                print COUNTER, 'counter'
#                minval = 0
                datadic = {0: [[[4224, 2112, 2640], [1219.40000000000001, 2408.700000000001, 1338.3], [2112, 2112, 2640], [560.310000000000002, 650.0, 760.0]], 1338.3, ['Perennial stream', 'Intermittent stream', 'Ephemeral stream']]}
                self.chartbar.vb.data = datadic[0][0]
                maxval = max(datadic[0][0][0])
                minval = 0
                stepval = int(float(maxval)/len(datadic[0][0][0]))
                self.chartbar.vb.valueAxis.labels.maxWidth = 10#self.labelsmaxwidth #.get()
        
                self.chartbar.vb.valueAxis.valueMin = minval
                self.chartbar.vb.valueAxis.valueMax = maxval
                self.chartbar.vb.valueAxis.valueStep = stepval
                self.chartbar.vb.valueAxis.visibleGrid = 1 #self.gridvisible.get()
                self.chartbar.drawing.add(self.chartbar.vb)
                self.chartbar.drawing.add(self.chartbar.vb.valueAxis)
                
                names = datadic[0][2] #data[1]
                self.chartbar.vb.categoryAxis.categoryNames = names     
                self.chartbar.drawing.add(self.chartbar.vb.categoryAxis)
        
                self.chartbar.drawing.add(self.chartbar.legend)
                
                pdfname = savePDF()
                self.chartbar.drawing.save(formats= ['pdf'],outDir=None,fnRoot=pdfname)
                
                os.startfile(pdfname)
    def dataPrep(self):
        if len(self.tablesToProcess) == 1:
            data = []
            datavals = []
            datanames = []
            geomreturned = get_geoObjectArea(self.tablesToProcess[0]) 
            for geom in geomreturned:
                datavals.append(geom.Geometry.area * 0.000247105381)
                try:
                    datanames.append(geom.name)
                except:
                    datanames.append('')
            data.append(datavals)
            data.append(datanames)
            print data
            return data
        else:
            data = []
            self.dataReturn = get_OrderedGeoObjectsWithin(self.tablesToProcess[0],self.tablesToProcess[1]) 
            dataname = []
            datacontainer = []
            for outer in self.dataReturn:
                dataname.append(outer.name)
                dataval = []
                for inners in self.dataReturn[outer]:
                    dataval.append(inners.Geometry.area * 0.000247105381)
                datacontainer.append(dataval)
            data.append(datacontainer)
            data.append(dataname)
            
            return data
        
        
    def orderedDialogue(self):
        
            x = 6
            y = 3
            self.sqlFieldsList = []
            self.sqlTableList = []
            self.sqlAllFieldsList = []
            def addFieldProxy(event):
                addField()
                
            def addField():
                table = self.tableSelected
                val = self.fieldList.selection_get()
                val = self.sqlStringVar.get() + ' ' +  val  + " "  
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get()) 
                
            def addVals(event):
    
                val = self.valueList.selection_get()
                val = self.sqlStringVar.get() + ' ' +  val +" "  
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
                 
            def insertAll():
                table = self.tableSelected
                val = self.fieldList.selection_get()
                val = self.sqlStringVar.get() 
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get()) 

                table = self.tableSelected
                
                for field in self.sqlAllFieldsList:
                    fieldval = "%s.%s" % (field, table)
                    if not fieldval in self.sqlFieldsList:
                        self.sqlFieldsList.append(fieldval)
                
                #selectString = self.sqlStringVar.get() 
                selectString = self.sqlStringVar.get()
                if len(self.sqlFieldsList) > 1:
                    for fieldval in self.sqlFieldsList[:-1]:
                        selectString += fieldval.split('.')[0]  + ', '
                    selectString += self.sqlFieldsList[-1].split('.')[0] 
                    selectString += ' FROM '
                    tablecheck = []
                    for fieldval in self.sqlFieldsList[:-1]:
                        table = fieldval.split('.')[1]
                        if table not in tablecheck:

                            selectString += table + ', '
                            tablecheck.append(table)
                    table = self.sqlFieldsList[-1].split('.')[1] 
                    if table not in tablecheck:
                        selectString += table 
                    else:
                        selectString= selectString[:-2] + ' '
                else:
                    selectString += fieldval.split('.')[0]
                    selectString += ' FROM '
                    table = fieldval.split('.')[1]
                    selectString += table 

                self.sqlStringVar.set(selectString)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get()) 

            def getVals():
                
                field = self.fieldList.selection_get()
                valuesql = "SELECT DISTINCT " + field + " FROM " + self.tableSelected 
                
                self.cursorspatial.execute(valuesql)
                
                vals = self.cursorspatial.fetchall()
                self.valueList.delete(0,END)
                
                for val in vals:
                        self.valueList.insert(END, val[0])
            
            def addAtts(event):
                table = self.tableSelected
                field = self.fieldList.selection_get()
                
                if not field in self.sqlFieldsList:
                    fieldval = "%s.%s" % (field, table)
                    self.sqlFieldsList.append(fieldval)
                
                #selectString = self.sqlStringVar.get() 
                selectString = self.sqlStringVar.get() + ' '
                if len(self.sqlFieldsList) > 1:
                    for fieldval in self.sqlFieldsList[:-1]:
                        selectString += fieldval.split('.')[0]  + ', '
                    selectString += self.sqlFieldsList[-1].split('.')[0] 
                    selectString += ' FROM '
                    for fieldval in self.sqlFieldsList[:-1]:
                        table = fieldval.split('.')[1]
                        selectString += table + ', '
                        self.sqlTableList.append(table)
                    table = self.sqlFieldsList[-1].split('.')[1] 
                    self.sqlTableList.append(table)
                    selectString += table 
                else:
                    selectString += fieldval.split('.')[0]
                    selectString += ' FROM '
                    table = fieldval.split('.')[1]
                    selectString += table 

                self.sqlStringVar.set(selectString)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())   
            
            def getAttsProxy(event):
                getAtts() 
            
            def getAtts():
                self.tableSelected = "LMS_DATA_MODELS_" +self.tableList.selection_get()
                if self.tableSelected not in self.sqlTableList:
                    self.sqlTableList.append(self.tableSelected)
                columns = "PRAGMA table_info(%s)" %  self.tableSelected
                self.cursorspatial.execute(columns)
                cols = self.cursorspatial.fetchall()
                self.fieldList.delete(0,END)
                self.sqlAllFieldsList = []
                for col in cols:
                        print cols
                        self.fieldList.insert(END, col[1])
                        self.sqlAllFieldsList.append(col[1])
            def insertReset():
                val = "SELECT "
    
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlFieldsList = []
                self.sqlTableList = []
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            
            def transformationText(coords):
                'input: string of WKT coordinates; output:a tuple containing tuples with coordinate pairs'
            
            
                # get rid of extra strings within the string
                replaceList = ['POLYGON', 'MULTIPOLYGON', 'MULTI', '((', '))','(', ')', 'POINT', 'LINESTRING', 'MULTILINESTRING']
                for string2replace in replaceList:
                    coords = coords.replace(string2replace, '')
            
            
                #split the resulting string into a list
                coordsplit = coords.split(',')
            
                #convert the list into a paired list with tuples    
                polycoords = []
                for value in coordsplit:
                    coords = value.split()
            
                    polycoords.append(tuple(coords))
            
                del coordsplit
                return polycoords
            def transformationSVG(coords):
                'input: string of SVG coordinates; output:a tuple containing tuples with coordinate pairs'
            
            
                # get rid of extra strings
                replaceList = ['M', 'z', 'cx=', 'cy=','=']
                for string2replace in replaceList:
                    coords = coords.replace(string2replace, '')
            
            
                #split the resulting string into a list
                coordsplit = coords.split()
            
                # this gets rid of excess double quotes and coverts the values into absolute value floating numbers
                coordsplit = [abs(float(value.replace('"',''))) for value in coordsplit]
            
                listLength = len(coordsplit)
                
                #make the coords into a true poly by appending the first coord pair onto the end of the list, unless the coords describe a point
                if listLength > 2:   
                    zeroValue = float(coordsplit[0])
                    oneValue = float(coordsplit[1])
                    coordsplit.append(zeroValue)
                    coordsplit.append(oneValue)
            
            
                #convert numbers in a list into paired tuples inside a list        
                polycoords = []
                for xy in range(0,listLength-1,2):
                    x = coordsplit[xy]
                    y = coordsplit[xy+1]
                    xytup = (float(x),float(y))
                    polycoords.append(xytup)
                    
                return polycoords

            def executeSHP():
                pass
            
            def executeKML():
                headers = self.sqlFieldsList
                sp = self.sqlWindow.get(0.0,END).replace("Geometry", "AsSVG(Transform(Geometry,4326))")
                
                self.cursorspatial.execute(sp)
                vals = self.cursorspatial.fetchall()
                places = ''
                
                    
                for valtup in vals:
                    data = ''
                    for COUNTER, header in enumerate(headers):
                        
                        rval =  valtup[COUNTER]
                        if header.split('.')[0] == "Geometry":
                            geodata = transformationSVG(rval)
                        else:
                            data += str(rval) + ' '
                    places += placemarKML % (data,data, geodata) + '\n'
                
                kml = polykml % ("KML", places)  
                kmlname = saveKML() 
                kmlwrite = open(kmlname,'w')
                kmlwrite.write(kml)
                kmlwrite.close() 
                os.startfile(kmlname)      
            def executeSS():
                headers = self.sqlFieldsList
                sp = self.sqlWindow.get(0.0,END).replace("Geometry", "AsText(Geometry)")
                
                self.cursorspatial.execute(sp)
                vals = self.cursorspatial.fetchall()   
                csvname = saveCSV()
                csv = open(csvname,'w')
                data = ''
                for header in headers:
                    headerval = header.split('.')[0]

                    data += headerval + ','
                
                data += '\n'
                csv.write(data)
                for valtup in vals:
                    data = ''
                    for rval in valtup:
                        data += str(rval) + ','
                    data += '\n'
                    csv.write(data)
                csv.close()
                os.startfile(csvname)
                                 
                
            def save():
                pass
            self.sqlDialogue = Frame(self.BaseFrame, relief=SUNKEN, bd=2, bg=self.backgroundcolor)
            self.sqlDialogue.grid(row=0, column=0,rowspan=9,columnspan=9, padx = 1)

            self.ButtonForget()

            sql = '''SELECT name FROM sqlite_master WHERE type='table'  ORDER BY name'''
            self.cursorspatial = curspatial()
            self.cursorspatial.execute(sql)
            self.tables = self.cursorspatial.fetchall()
    
            self.sqlMainFrame =  Frame(self.sqlDialogue, relief=SUNKEN, bd=2, bg=self.backgroundcolor)
            self.sqlMainFrame.grid(row=0, column=0, sticky = W+E+N+S)
            self.listboxFrame =  Frame(self.sqlMainFrame, bg=self.backgroundcolor)
            self.listboxFrame.grid(row=0, column=0, padx = 10,pady = 5)
            
            self.scrollbar = Scrollbar(self.listboxFrame, orient=VERTICAL)
            
            self.tableList = Listbox(self.listboxFrame,selectmode=SINGLE,height=15,yscrollcommand=self.scrollbar.set)
            self.tableList.grid(row=0, column=1, padx = 2,pady = 5)
            self.tableList.bind("<Double-Button-1>", getAttsProxy)
            self.scrollbar.config(command=self.tableList.yview)
            self.scrollbar.grid(row=0,column=2)

            
            self.scrollFieldbar = Scrollbar(self.listboxFrame, orient=VERTICAL)

            self.fieldList = Listbox(self.listboxFrame,height=15,yscrollcommand=self.scrollFieldbar.set)
            self.fieldList.grid(row=0, column=3, padx = 2,pady = 5)
            self.fieldList.bind("<Double-Button-1>", addAtts)
            self.scrollFieldbar.config(command=self.fieldList.yview)
            self.scrollFieldbar.grid(row=0,column=4)

            self.scrollValuebar = Scrollbar(self.listboxFrame, orient=VERTICAL)

            self.valueList = Listbox(self.listboxFrame,height=15,yscrollcommand=self.scrollValuebar.set)
            self.valueList.grid(row=0, column=5, padx = 2,pady = 5)
            self.valueList.bind("<Double-Button-1>", addVals)
            self.scrollValuebar.config(command=self.valueList.yview)
            self.scrollValuebar.grid(row=0,column=6)



            self.sqlStringVar = StringVar()
            self.sqlStringVar.set('SELECT ')
            for table in self.tables:
                
                if table[0].find('LMS') != -1 and table[0].find('idx') == -1 :
                    
                    self.tableList.insert(END, table[0].replace('LMS_DATA_MODELS_',''))
            self.buttonAddFields = Button(self.listboxFrame,
                                        fg= 'dark blue',
                                        bd=3,
                                        height=y,width=x*2,
                                        bg='tan',
                                        text = 'Add Fields',
                                        command = getAtts)
            self.buttonAddFields.grid(row=1, column=1, padx = 2,pady = 1)
            self.buttonAddValues = Button(self.listboxFrame,
                                        fg= 'dark blue',
                                        bd=3,
                                        height=y,width=x*2,
                                        bg='tan',
                                        text = 'Get All\nFields',
                                        command = insertAll)
            self.buttonAddValues.grid(row=1, column=3, padx = 2,pady = 1)
            
            self.buttonAddValues = Button(self.listboxFrame,
                                        fg= 'dark blue',
                                        bd=3,
                                        height=y,width=x*2,
                                        bg='tan',
                                        text = 'Add Unique\nValues',
                                        command = getVals)
            self.buttonAddValues.grid(row=1, column=5, padx = 2,pady = 1)

   
            self.sqlSQLFrame =  Frame(self.sqlMainFrame,  bg=self.backgroundcolor)
            self.sqlSQLFrame.grid(row=0, column=1, padx = 10,pady = 5)
            
    
            self.sqlWindow= Text(self.sqlSQLFrame, width=50, height=15, wrap=WORD)
            self.sqlWindow.grid(row=0,column=0, columnspan=3, rowspan=2)
            self.sqlWindow.delete(0.0, END)
            self.sqlWindow.insert(END, self.sqlStringVar.get())

            self.buttonAddFieldSQL = Button(self.sqlSQLFrame,
                                        fg= 'dark blue',
                                        bd=3,
                                        height=y,width=x*2,
                                        bg='tan',
                                        text = 'Add Field\nName',
                                        command = addField)
            self.buttonAddFieldSQL.grid(row=2, column=0, pady = 2)
            self.buttoninsertReset2= Button(self.sqlSQLFrame,
                                        fg= 'dark blue',
                                        bd=2,
                                        height=y,width=x* 2,
                                        bg='tan',
                                        text = 'Reset\nStatement',
                                        command = insertReset)
            self.buttoninsertReset2.grid(row=2, column=1,pady = 2)
    
            self.buttonSaveSQL = Button(self.sqlSQLFrame,
                                        fg= 'dark blue',
                                        bd=3,
                                        height=y,width=x*2,
                                        bg='tan',
                                        text = 'Save\nStatement',
                                        command = save)
            self.buttonSaveSQL.grid(row=2, column=2,pady = 2)




            self.sqlBottomFrame =  Frame(self.sqlDialogue, bg=self.backgroundcolor)
            self.sqlBottomFrame.grid(row=1, column=0)


            self.buttonFrame = Frame(self.sqlBottomFrame)
            self.buttonFrame.grid(row=0,column=0,rowspan=3)

            self.sqlModelFrame = Frame(self.sqlBottomFrame)
            self.sqlModelFrame.grid(row=0,column=1,columnspan=6, rowspan=3)

            self.sqlModelFrameHolder = Frame(self.sqlBottomFrame)
            self.sqlModelFrameHolder.grid(row=0,column=1,columnspan=6, rowspan=3)
            #self.sqlModelFrameScrollbar = Scrollbar(self.sqlModelFrameHolder, orient=HORIZONTAL)
            #self.sqlModelFrameScrollbar.pack(side=BOTTOM, fill=X)

            self.sqlModelCanvas = GraphWithScroll(self.sqlModelFrameHolder,
                                                  self.wInfo.mapcanvasWidth/3, 
                                                  self.wInfo.graphCanvasHeight )
            #self.sqlModelCanvas.canvas.pack(side=TOP)
            #self.sqlModelFrameScrollbar.config(command=self.sqlModelCanvas.canvas.xview)
            self.sqlModelCanvas.frame.grid(row=0,column=0)

            
            self.buttonFrameRight = Frame(self.sqlBottomFrame)
            self.buttonFrameRight.grid(row=0,column=7,columnspan=3, rowspan=3, padx=10)

            rexe = 0
            self.buttonExecute = Button(self.buttonFrameRight,
                                        fg= 'white',
                                        bd=2,
                                        height=y,width=x+4,
                                        bg='dark red',
                                        text = 'Create\nShapefile',
                                        command = executeSHP)
            self.buttonExecute.grid(row=rexe, column=0, padx = 2,pady = 1)
            self.buttonExecuteSS = Button(self.buttonFrameRight,
                                        fg= 'white',
                                        bd=2,
                                        height=y,width=x+4,
                                        bg='dark green',
                                        text = 'Create\nSpreadsheet',
                                        command = executeSS)
            self.buttonExecuteSS.grid(row=rexe+1, column=0, padx = 2,pady = 1)    
            self.buttonExecuteKML = Button(self.buttonFrameRight,
                                        fg= 'white',
                                        bd=2,
                                        height=y,width=x+4,
                                        bg='dark blue',
                                        text = 'Create\nKML',
                                        command = executeKML)
            self.buttonExecuteKML.grid(row=rexe+2, column=0, padx = 2,pady = 1)       
    
    
    
            equals = ' = '
            notEqual = ' <> '
            and_ = ' AND '
            all = ' * '
            or_ = ' OR '
            not_ = ' NOT '                      
            is_ = ' IS '
            greater = ' > '
            lesser = ' < '
            lesserEQ = ' <= '
            greaterEQ = ' >= '
            like = ' LIKE ' 
            within = ' WITHIN ' 
            where = ' WHERE '
            near = ' NEAR '
            order = ' ORDER BY '
            from_ = ' FROM '


            def insertIs():
                val = self.sqlStringVar.get()
                val = val + is_
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonIs = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'Is',
                                        command = insertIs)
            self.buttonIs.grid(row=0, column=0, padx = 1,pady = 1) 
            def insertOr():
                val = self.sqlStringVar.get()
                val = val + or_
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonOr = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'Or',
                                        command = insertOr)
            self.buttonOr.grid(row=1, column=0, padx = 1,pady = 1) 
            def insertWhere():
                val = self.sqlStringVar.get()
                val = val + where
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonWhere = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'Where',
                                        command = insertWhere)
            self.buttonWhere.grid(row=2, column=0, padx = 1,pady = 1)  
    
            
            def insertAll():
                val = self.sqlStringVar.get()
                val = val + all
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonAll = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'All',
                                        command = insertAll)
            self.buttonAll.grid(row=0, column=1, padx = 1,pady = 1)

    
            
            def insertNotEquals():
                val = self.sqlStringVar.get()
                val = val + notEqual
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonNotEquals = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Does\nNot\nEqual',
                                        command = insertNotEquals)
            self.buttonNotEquals.grid(row=1, column=1, padx = 1,pady = 1)
            
            def insertEquals():
                val = self.sqlStringVar.get()
                val = val + equals
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonEquals = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Equals',
                                        command = insertEquals)
            self.buttonEquals.grid(row=2, column=1, padx = 1,pady = 1)

    
            def insertWithin():
                val = self.sqlStringVar.get()
                val = val + within
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonIs = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'Within',
                                        command = insertWithin)
            self.buttonIs.grid(row=0, column=3, padx = 1,pady = 1)
            
            def insertOrder():
                val = self.sqlStringVar.get()
                val = val + order
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonIs = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'Order\nBy',
                                        command = insertOrder)
            self.buttonIs.grid(row=1, column=3, padx = 1,pady = 1)     
    
            def insertNear():
                val = self.sqlStringVar.get()
                val = val + near
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonIs = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'Near',
                                        command = insertNear)
            self.buttonIs.grid(row=2, column=3, padx = 1,pady = 1)     
    
            def insertFrom():
                val = self.sqlStringVar.get()
                val = val + from_
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonIs = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
                                        text = 'From',
                                        command = insertFrom)
            self.buttonIs.grid(row=0, column=4, padx = 1,pady = 1)   
    

            def insertGreaterEQ():
                val = self.sqlStringVar.get()
                val = val + greaterEQ
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonGreaterEQ = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Greater\nOr Equal',
                                        command = insertGreaterEQ)
            self.buttonGreaterEQ.grid(row=1, column=4, padx = 1,pady = 1) 
 
            def insertLesserEQ():
                val = self.sqlStringVar.get()
                val = val + lesserEQ
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonLesserEQ = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Lesser\nOr Equal',
                                        command = insertLesserEQ)
            self.buttonLesserEQ.grid(row=2, column=4, padx = 1,pady = 1)
    
            
    
            def insertNot():
                val = self.sqlStringVar.get()
                val = val + not_
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())    
            self.buttonNot = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Not',
                                        command = insertNot)
            self.buttonNot.grid(row=0, column=5, padx = 1,pady = 1)
            
            def insertAnd():
                val = self.sqlStringVar.get()
                val = val + and_
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonAnd = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'And',
                                        command = insertAnd)
            self.buttonAnd.grid(row=1, column=5, padx = 1,pady = 1)
            def insertLike():
                val = self.sqlStringVar.get()
                val = val + like
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonLike = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Like',
                                        command = insertLike)
            self.buttonLike.grid(row=2, column=5, padx = 1,pady = 1)
            
            def insertGreater():
                val = self.sqlStringVar.get()
                val = val + greater
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonGreater = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Greater',
                                        command = insertGreater)
            self.buttonGreater.grid(row=0, column=6, padx = 1,pady = 1)
            
            def insertLesser():
                val = self.sqlStringVar.get()
                val = val + lesser
                self.sqlStringVar.set(val)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())
            self.buttonLesser = Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Lesser',
                                        command = insertLesser)
            self.buttonLesser.grid(row=1, column=6, padx = 1,pady = 1) 
    
    
            
            def distinctProxy():

                    insertDISTINCTCURRENT()


                             
            def insertDISTINCTCURRENT():
                val = self.sqlStringVar.get()
                
                statement_ = val[:6] + ' DISTINCT ' +  val[6:]
                self.sqlStringVar.set(statement_)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, statement_) 
            self.buttoninsertDistinct= Button(self.buttonFrame,bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x,
    
                                        text = 'Distinct',
                                        command = distinctProxy)
            self.buttoninsertDistinct.grid(row=2, column=6, padx = 2,pady = 1)
    
    
            def insertRemove():
                val = self.sqlStringVar.get()
                valist = val.split()
                statement_ = 'SELECT '
                for pieces in valist[1:-1]:
                    statement_ += pieces + ' '
                
                
                self.sqlStringVar.set(statement_)
                self.sqlWindow.delete(0.0, END)
                self.sqlWindow.insert(END, self.sqlStringVar.get())  
            self.buttonRemove = Button(self.buttonFrame,
                                        bg= 'dark grey',
                                        fg= 'black',
                                        bd=2,
                                        height=y,width=x*8,
    
                                        text = 'Remove\nLast',
                                        command = insertRemove)
            self.buttonRemove.grid(row=3, column=0,columnspan=8,pady = 2)
    

    
    
    
 
        
            #self.sqlFrame = Frame(self.sqlDialogue)
            #self.sqlFrame.grid(row=4,column=0,columnspan=3)
    
            #self.sqlStatement = Label(self.sqlFrame, textvariable = self.sqlStringVar)
            #self.sqlStatement.grid(row = 0,column=0)
            
            
            self.sqlDialogue.mainloop()
        
        
        



            
    def chartMake2(self, datadic, titlestring, COUNTER):
        from reportlab.graphics.charts.legends import Legend
        from reportlab.graphics.charts.barcharts import VerticalBarChart#,VerticalBarChart3D
        from reportlab.graphics.shapes import Drawing,_DrawingEditorMixin,String
        from reportlab.graphics.charts.textlabels import Label, BarChartLabel
        from reportlab.graphics.samples.excelcolors import color05,color06,color02,color01  ,color02,color03,color04,color05,color06,color07,color08,color09, color10
        from reportlab.lib.units import cm, mm, inch
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.graphics.widgetbase import Widget,TypedPropertyCollection
        from reportlab.lib import colors
        from reportlab.lib.colors  import PCMYKColor, HexColor
        from reportlab.lib.formatters import DecimalFormatter

        d = Drawing(width=11 * inch, height= 8 * inch) #(width=len(columns)* inch + 1 * inch, height=5*inch)

        vb = VerticalBarChart()
        vb.x = 1.5 * inch
        vb.y = 1.7 * inch
     
        vb.width = 8 * inch #len(columns) * inch - 1 * inch
        vb.height = 5 * inch

        vb.bars[0].fillColor = HexColor('#66cc00') #colors.peru
        vb.bars[1].fillColor = HexColor('#669933') #colors.darkkhaki
        vb.bars[2].fillColor = colors.goldenrod
        vb.bars[3].fillColor = colors.darkred

        vb.barLabels.boxAnchor = 'c'
        #vb.barLabels.textAnchor = 'middle'
        vb.barLabelFormat = '%0.1f'  #'%0.2f' '%d'
        vb.barLabelFormat = DecimalFormatter(places=1,
                                                    decimalSep='.',
                                                    thousandSep=',',
                                                    prefix=None,
                                                    suffix=None) 
        vb.barLabels.dx = 0
        vb.barLabels.dy = 2
        #vb.barLabels.boxAnchor = 'w'
        vb.barLabels.fontName = 'Helvetica'
        vb.barLabels.fontSize = 9
        vb.barLabels.nudge = 5
        
        vb.data = datadic[0][0] #dataList a list of data

        vb.categoryAxis.categoryNames = datadic[0][2]  # ['All\nGrassland', 'chaparral', 'oak\nsavanna', 'oak\nwoodland', 'riparian', 'permanent\nwetland', 'seasonal\nwetland', 'alkali\nwetland', 'pond', 'ephemeral', 'intermittent', 'perennial'] #columnList -list of column names goes here
        vb.categoryAxis.labels 
        vb.categoryAxis.labels.angle = 0#30
        vb.categoryAxis.labels.bottomPadding = 50
        vb.categoryAxis.labels.boxAnchor = 'n'
        #vb.categoryAxis.labels.boxFillColor = None
        #vb.categoryAxis.labels.boxStrokeColor = None
        vb.categoryAxis.labels.boxStrokeWidth = 0.5
        vb.categoryAxis.labels.boxTarget = 'normal'
        vb.categoryAxis.labels.dx = 0
        #vb.categoryAxis.labels.dy = -5
        #vb.categoryAxis.labels.fillColor = color05
        vb.categoryAxis.labels.fontName = 'Helvetica'
        vb.categoryAxis.labels.fontSize = 10
        #vb.categoryAxis.labels.height = None
        vb.categoryAxis.labels.labelPosFrac = 0.5
        #vb.categoryAxis.labels.leading = None
        vb.categoryAxis.labels.leftPadding = 0
        #vb.categoryAxis.labels.maxWidth = None
        vb.categoryAxis.labels.rightPadding = 0
        #vb.categoryAxis.labels.strokeColor = None
        vb.categoryAxis.labels.strokeWidth = 0.1
        vb.categoryAxis.labels.textAnchor = 'middle'
        vb.categoryAxis.labels.topPadding = 0
        vb.categoryAxis.labels.visible = 1
        #vb.categoryAxis.labels.width = None
        #vb.categoryAxis.labels.x = 200
        #vb.categoryAxis.labels.y = 200
        #vb.categoryAxis.style='stacked'


        vb.valueAxis.valueMin = 0
        vb.valueAxis.valueMax = datadic[0][1]#valueMax #max(vb.data[0])
        #vb.valueAxis.valueStep = int(max(data[0])/3)
        #vb.valueAxis.gridEnd = vb.width + 25
        vb.valueAxis.labels.fontName = 'Helvetica'
        vb.valueAxis.labels.fontSize = 10
        vb.valueAxis.labels.maxWidth = 2
        vb.valueAxis.labelTextFormat = DecimalFormatter(places=0,
                                                    decimalSep='.',
                                                    thousandSep=',',
                                                    prefix=None,
                                                    suffix=None) 
        vb.valueAxis.tickLeft  = 1
        vb.valueAxis.visibleGrid  = 1





        #vb.bars.fillColor = PCMYKColor(0,100,0,59,alpha=100)
        #vb.bars.strokeColor = PCMYKColor(0,66,33,39,alpha=100)
        #vb.bars.strokeDashArray = None
        vb.bars.strokeWidth = .1
        #vb.bars.symbol = None



        title = Label()
        title.fontName   = 'Helvetica'
        title.fontSize   = 12
        title.x          = d.width/2 
        title.y          = d.height - .5* inch
        title._text      = titlestring 
        title.textAnchor = 'middle'

    ##    pages = Label()
    ##    pages.fontName   = 'Helvetica'
    ##    pages.fontSize   = 11
    ##    pages.x          = d.width - 1 * inch
    ##    pages.y          = d.height - 1 * cm
    ##    pages._text      = 'Page %d of 2' % COUNTER 
    ##    pages.textAnchor = 'middle'
    ##    d.add(pages)
    ##
    ##    title.angle = 0
    ##    title.bottomPadding = 0
    ##    title.boxAnchor = 'c'
    ##    #title.boxFillColor = None
    ##    #title.boxStrokeColor = None
    ##    title.boxStrokeWidth = 0.5
    ##    title.boxTarget = 'normal'
    ##    title.dx = 0
    ##    title.dy = 0
    ##    #title.fillColor = color02
    ##
    ##    title.fontName = 'Helvetica'
    ##    title.fontSize = 13
    ##    #title.height = None
    ##    #title.leading = None
    ##    title.leftPadding = 0
    ##
    ##    #title.maxWidth = None
    ##
    ##    title.rightPadding = 0
    ##    #title.strokeColor = None
    ##    title.strokeWidth = 0.1
    ##    title.textAnchor = 'middle'
    ##    title.topPadding = 0
    ##    title.visible = 1
    ##    title.width = None
    ##    #title.x = 100
    ##    #title.y = 100

        legendColorList = []
        legend_entry =  HexColor('#66CC00'), 'Protection\nRequired'
        legendColorList.append(legend_entry)
        legend_entry =  HexColor('#669933'),'Protection\nTo Date'
        legendColorList.append(legend_entry)
        legend_entry =  colors.goldenrod,'Impact\nCap'
        legendColorList.append(legend_entry)
        legend_entry =  colors.darkred,'Impacts\nTo Date'
        legendColorList.append(legend_entry)
       
        for set in legendColorList:
            legend = Legend()
            legend.colorNamePairs = [set]#legendColorList
            legend.fontName       = 'Helvetica'
            legend.fontSize       = 10
            legend.x              = (3 * inch) + (1.5* inch *  legendColorList.index(set))
            legend.y              = .7* inch 
        ##    legend.dxTextSpace    = 15
        ##    legend.dy             = 5 
        ##    legend.dx             = 5
            
            legend.deltay         = 10
            legend.alignment      ='right'
            d.add(legend)


        xLabel = Label()
        xLabel.fontName       = 'Helvetica'
        xLabel.fontSize       = 11
        xLabel.x              = vb.width - 200
        xLabel.y              = 1.1 * inch
        xLabel.textAnchor     ='middle'
        xLabel.maxWidth       = 100
        xLabel.height         = .5 * inch
        xLabel._text          = "Terrestrial Land Cover Type"



    ##    xLabel.angle = 0
    ##    xLabel.bottomPadding = 0
    ##    xLabel.boxAnchor = 'c'
    ##    xLabel.boxFillColor = None
    ##    xLabel.boxStrokeColor = None
    ##    xLabel.boxStrokeWidth = 0.5
    ##    xLabel.boxTarget = 'normal'
    ##    xLabel.dx = 0
    ##    xLabel.dy = 0
    ##    #xLabel.fillColor = color02
    ##    xLabel.fontName = 'Helvetica'
    ##    xLabel.fontSize = 11
    ##    xLabel.height = None
    ##    xLabel.leading = None
    ##    xLabel.leftPadding = 0
    ##    xLabel.maxWidth = None
    ##    xLabel.rightPadding = 0
    ##    xLabel.strokeColor = None
    ##    xLabel.strokeWidth = 0.1
    ##    xLabel.textAnchor = 'start'
    ##    xLabel.topPadding = 0
    ##    xLabel.visible = 1
    ##    xLabel.width = None
    ##    #xLabel.x = 20
        #xLabel.y = 400
        d.add(xLabel)

        yLabel = Label()    
        yLabel.fontName       = 'Helvetica'
        yLabel.fontSize       = 11
        yLabel.x              = .5 * inch
        yLabel.y              = vb.height - 1 * inch
        yLabel.angle          = 0
        yLabel.textAnchor     ='middle'
        yLabel.maxWidth       = 100
        yLabel.height         = 20
        yLabel._text          = "Acres" #yText #"Acres"


        yLabel.angle = 90
        yLabel.bottomPadding = 0
        yLabel.boxAnchor = 'c'
        #yLabel.boxFillColor = None
        #yLabel.boxStrokeColor = None
        yLabel.boxStrokeWidth = 0.5
        yLabel.boxTarget = 'normal'
        yLabel.dx = 0
        yLabel.dy = 0
        #yLabel.fillColor = color02
        yLabel.fontName = 'Helvetica'
        yLabel.fontSize = 11
        yLabel.height = None
        yLabel.leading = None
        yLabel.leftPadding = 0
        yLabel.maxWidth = None
        yLabel.rightPadding = 0
        yLabel.strokeColor = None
        yLabel.strokeWidth = 0.1
        yLabel.textAnchor = 'start'
        yLabel.topPadding = 0
        yLabel.visible = 1
        yLabel.width = None
        #yLabel.x = 200
        #yLabel.y = 20

        d.add(vb)
        d.add(title)
        #d.add(legend)
        #d.add(xLabel)
        d.add(yLabel)

        
        d.save(formats= ['pdf'],outDir=None,fnRoot='C:/Chart2_%s.pdf' % datadic[0][2][0])
        return 'C:/Chart2_%s.pdf' % datadic[0][2][0]

    ##def watermark(pdflist, fileout):
    ##
    ##    from pyPdf import PdfFileWriter, PdfFileReader
    ##    output = PdfFileWriter()
    ##    for pdf in pdflist:
    ##
    ##
    ##        input1 = PdfFileReader(file(pdf, "rb"))
    ##        page = input1.getPage(0)
    ##        output.addPage(page)
    ##        
    ##        watermark = PdfFileReader(file("C:/HCPDatabase/watermark2011.pdf", "rb"))
    ##        page.mergePage(watermark.getPage(0))
    ##
    ##
    ##    
    ##    fileout = fileout.replace('.pdf','')        
    ##    fileout = fileout +'.pdf'
    ##    outputStream = file(fileout  , "wb")
    ##    output.write(outputStream)
    ##    outputStream.close()
    ##    import os
    ##    os.startfile(fileout) 
    
    

    def pdfProxy(self):
        filepath = r'C:\ParcelViewer\Images\N18D3_4.jpg'
        self.pdf(filepath)

    def pdf(self, filepath):
        from win32com.shell import shell, shellcon
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import cm, mm, inch       
        import os        

      
#        coordsplit = self.transformation2(self.geom2227)

        # Retrieve the attributes (including Geometry) and process them below  


        import time
        c = time.localtime()
        from PIL import Image, ImageTk
        self.tile = Image.open(filepath)
        self.boundingBox = self.tile.getbbox()       

        #desktop = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, None, 0)
        path = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, None, 0)
        try:
            pdfname = path + "/"+self.pdf_title.get() + '.pdf'
        except:
            date =   str(c[1]) + '_'+ str(c[2]) + '_' + str(c[0]) +'_' + str(c[3]) + '_' + str(c[4])
            pdfname = path + "/"+ date +'.pdf'
        #pdfname = desktop + '\\' +projectForMap +str(random.Random().randint(1,10000)) + '.pdf'                                         

        pdf= canvas.Canvas(pdfname, pagesize=letter)          #Create the PDF Canvas object, to be drawn on below
        #pdf.setFont("Courier", 20)
        #pdf.setStrokeColorRGB(1, 0, 0)
        #pdf.drawString(inch ,21 * cm, str(self.longitude) + ', ' + str(self.latitude))
        #pdf.drawString(inch, 20 * cm, 'You are on Parcel:')
        #pdf.drawString(inch, 19 * cm, self.ownername + ", APN: "+ str(self.apnvalue))
        #pdf.drawString(inch, 18 * cm, self.note)
        self.pdfPicWidth = ((14 *cm) * (float(self.boundingBox[2])/self.boundingBox[3]) )
        self.pdfPicHeight = (float(14 * cm))
        pdf.drawImage(filepath, .3* cm, 1 *cm, width=self.pdfPicWidth, height=self.pdfPicHeight )
        

        pdf.showPage()
        pdf.save()

        os.startfile(pdfname)              

    def imageArrange(self):
        #'controls image placement and associated image grid objects'
        if self.zoomer.currentZoom <= 4:
            
            self.iManager.update(ImageGrid,self.zoomer)
            divider = 2 #(len(self.iManager.tileCOORDIC.keys()))/2
            dickeys = self.iManager.tileCOORDIC.keys()
            for keys in dickeys:
                    X = keys[0]
                    Y = keys[1]
                    coords = [coords for coords in self.iManager.tileDic if self.iManager.tileDic[coords]  == self.iManager.tileCOORDIC[X,Y]][0]

                    xposition = ((coords[0] - self.zoomer.upperLeft[0])/((self.zoomer.currentLowerRight[0])- self.zoomer.upperLeft[0])) * (self.wInfo.mapcanvasWidth) 
                    yposition =  ((self.zoomer.upperLeft[1]-coords[1])/(self.zoomer.upperLeft[1]-self.zoomer.currentLowerRight[1])) * (self.wInfo.mapcanvasHeight) 

                    filename = os.path.join(self.imageLibrary, self.iManager.tileCOORDIC[X,Y] + '.jpg')
#  
                    #xposition  = ((X -1) * (self.wInfo.mapcanvasWidth/2 + 30)) + 5
                    #yposition =  (Y-1) * self.wInfo.mapcanvasHeight/2 + 1
                    
        
                    print xposition, yposition
                    exec "self.tile%d%d = ImageProcessor(filename, divider, self.wInfo)" % (X,Y)
                    
                    exec "self.mapAerial%d%d = self.mainMap.canvas.create_image(xposition,yposition, image = self.tile%d%d.jpgPI, anchor= 'nw') " % (X,Y,X,Y)
                    #self.ImageList.append(self.mapAerial)
                    

#                    self.tile = ImageProcessor(filename, divider, self.wInfo)
#                    try:
#                        self.mapAerial = self.mainMap.canvas.create_image(xposition,yposition, image = self.tile.jpgPI, anchor= 'nw', tags = self.iManager.tileCOORDIC[X,Y]) 
#                        self.mainMap.canvas.itemconfig(self.mapAerial, tags=(self.iManager.tileCOORDIC[X,Y]))
#                    except:
#                        pass
                
                
#                    exec "self.tile%d%d = Image.open(os.path.join(self.imageLibrary, %s + '.jpg'))" % (X,Y, self.iManager.tileCOORDIC[X,Y])
#                    exec "self.boundingBox = self.tile%d%d.getbbox()" % X,Y
#                    self.screenMapImageWidth = self.wInfo.mapcanvasHeight * (float(self.boundingBox[2])/self.boundingBox[3])
#                    exec "self.tile%d%dscreen = self.tile%d%d.resize((int(self.screenMapImageWidth/%d), int(self.screenMapImageHeight/%d)), Image.ANTIALIAS)" % (X, Y, X,Y,divider, divider)
#                    exec "del self.tile%d%d" % X,Y
#                    
#                                      
#                    
#                    exec "self.widthOnScreen%d = (self.screenMapImageWidth/center_point_finder) *3 " % COUNTER
#                    exec "self.heightOnScreeen%d = (self.screenMapImageHeight/center_point_finder)" % COUNTER
#                    exec "self.mapAerial%d = self.mainMap.canvas.create_image(self.widthOnScreen%d,self.heightOnScreeen%d, image = self.jpgPI%d)" % (COUNTER,COUNTER,COUNTER,COUNTER)
#                    exec "self.ImageList.append(self.mapAerial%d)" % COUNTER
#                    exec "print self.widthOnScreen%d,self.heightOnScreeen%d" % (COUNTER, COUNTER)
#                                  

    def imageProcess(self,filename):
        self.tile = Image.open(os.path.join(self.imageLibrary, filename + '.jpg'))
        self.boundingBox = self.tile.getbbox() 
        self.screenMapImageWidth = self.wInfo.mapcanvasHeight * (float(self.boundingBox[2])/self.boundingBox[3])
        self.tilescreen = self.tile.resize((int(self.screenMapImageWidth/2), int(self.screenMapImageHeight/2)), Image.ANTIALIAS)
        del self.tile
#        center_point_finder = 4
#        self.widthOnScreen = (self.screenMapImageWidth/center_point_finder)
#        self.heightOnScreeen = (self.screenMapImageHeight/center_point_finder) * 3
#        self.mapAerial = self.mainMap.canvas.create_image(self.widthOnScreen,self.heightOnScreeen, image = self.jpgPI)
#                     
        return self.tilescreen 
                    
                    


#
#            
#            for COUNTER,imageObject in enumerate(self.iManager.newImgs):
#                print self.zoomer.currentUpperLeft
#                print imageObject.sheetName
#                print imageObject.Geometry[0][0]
#            print dir(imageObject.Geometry[0] )
#
#
#
#
#            for COUNTER,imageObject in enumerate(self.iManager.newImgs):
#                    
#
#                    
#                    
#
#                    self.screenMapImageWidth = self.wInfo.mapcanvasHeight * (float(self.boundingBox[2])/self.boundingBox[3])
#                    self.screenMapImageHeight = self.wInfo.mapcanvasHeight
#
#                    exec "self.tile%d = self.tile%d.resize((int(self.screenMapImageWidth/2), int(self.screenMapImageHeight/2)), Image.ANTIALIAS)" % (COUNTER, COUNTER)
#                    exec "self.jpgPI%d = ImageTk.PhotoImage(self.tile%d)" % (COUNTER, COUNTER)
#                    center_point_finder = 4
#
#                    if COUNTER == 0:
#                        exec "self.widthOnScreen%d = (self.screenMapImageWidth/center_point_finder) *3 " % COUNTER
#                        exec "self.heightOnScreeen%d = (self.screenMapImageHeight/center_point_finder)" % COUNTER
#                        exec "self.mapAerial%d = self.mainMap.canvas.create_image(self.widthOnScreen%d,self.heightOnScreeen%d, image = self.jpgPI%d)" % (COUNTER,COUNTER,COUNTER,COUNTER)
#                        exec "self.ImageList.append(self.mapAerial%d)" % COUNTER
#                        exec "print self.widthOnScreen%d,self.heightOnScreeen%d" % (COUNTER, COUNTER)
#
#
#
#                    if COUNTER == 1: 
#                        exec "self.widthOnScreen%d = (self.screenMapImageWidth/center_point_finder) * 1 " % COUNTER
#                        exec "self.heightOnScreeen%d = (self.screenMapImageHeight/center_point_finder)" % COUNTER
#                        exec "self.mapAerial%d = self.mainMap.canvas.create_image(self.widthOnScreen%d,self.heightOnScreeen%d, image = self.jpgPI%d)" % (COUNTER,COUNTER,COUNTER,COUNTER)
#                        exec "self.ImageList.append(self.mapAerial%d)" % COUNTER
#                        exec "print self.widthOnScreen%d,self.heightOnScreeen%d" % (COUNTER, COUNTER)
#
#                    elif COUNTER == 2:
#                        exec "self.widthOnScreen%d = (self.screenMapImageWidth/center_point_finder)  " % COUNTER
#                        exec "self.heightOnScreeen%d = (self.screenMapImageHeight/center_point_finder) * 3" % COUNTER
#                        exec "self.mapAerial%d = self.mainMap.canvas.create_image(self.widthOnScreen%d,self.heightOnScreeen%d, image = self.jpgPI%d)" % (COUNTER,COUNTER,COUNTER,COUNTER)
#                        exec "self.ImageList.append(self.mapAerial%d)" % COUNTER
#                        exec "print self.widthOnScreen%d,self.heightOnScreeen%d" % (COUNTER, COUNTER)
#
#                    elif COUNTER == 3:
#                        exec "self.widthOnScreen%d = (self.screenMapImageWidth/center_point_finder) *3  " % COUNTER
#                        exec "self.heightOnScreeen%d = (self.screenMapImageHeight/center_point_finder) * 3" % COUNTER
#                        exec "self.mapAerial%d = self.mainMap.canvas.create_image(self.widthOnScreen%d,self.heightOnScreeen%d, image = self.jpgPI%d)" % (COUNTER,COUNTER,COUNTER,COUNTER)
#                        exec "self.ImageList.append(self.mapAerial%d)" % COUNTER
#                        exec "print self.widthOnScreen%d,self.heightOnScreeen%d" % (COUNTER, COUNTER)
#
#
#
#















##
##
##
##                if COUNTER == 1:
##                    self.tile = Image.open(os.path.join(self.imageLibrary, imageObject.sheetName + '.jpg'))
##                    print imageObject.sheetName, COUNTER
##                    self.boundingBox = self.tile.getbbox()
##                    
##                    self.screenMapImageWidth = self.wInfo.mapcanvasHeight * (float(self.boundingBox[2])/self.boundingBox[3])
##                    self.screenMapImageHeight = self.wInfo.mapcanvasHeight
##
##                    self.tile = self.tile.resize((int(self.screenMapImageWidth/2), int(self.screenMapImageHeight/2)), Image.ANTIALIAS)
##                    self.jpgPI = ImageTk.PhotoImage(self.tile)
##                    center_point_finder = 4
##
##                    self.widthOnScreen = 300.0#(self.screenMapImageWidth/center_point_finder) 
##                    self.heightOnScreeen = 300 * (1334.0/2000) #(self.screenMapImageHeight/center_point_finder)
##
##                    self.widthOnScreen = self.widthOnScreen 
##                    print self.widthOnScreen, self.heightOnScreeen
##                    
##                    self.mapAerial = self.mainMap.canvas.create_image(self.widthOnScreen,self.heightOnScreeen, image = self.jpgPI)
##                    self.ImageList.append(self.mapAerial)
##
##
##                if COUNTER == 2:
##                    self.tile3 = Image.open(os.path.join(self.imageLibrary, imageObject.sheetName + '.jpg'))
##                    print imageObject.sheetName, COUNTER
##                    self.boundingBox = self.tile.getbbox()
##                    
##                    self.screenMapImageWidth = self.wInfo.mapcanvasHeight * (float(self.boundingBox[2])/self.boundingBox[3])
##                    self.screenMapImageHeight = self.wInfo.mapcanvasHeight
##
##                    self.tile = self.tile.resize((int(self.screenMapImageWidth/2), int(self.screenMapImageHeight/2)), Image.ANTIALIAS)
##                    self.jpgPI = ImageTk.PhotoImage(self.tile)
##                    center_point_finder = 4
##
##                    self.widthOnScreen = 300.0#(self.screenMapImageWidth/center_point_finder) 
##                    self.heightOnScreeen = 300 * (1334.0/2000) #(self.screenMapImageHeight/center_point_finder)
##
##                    self.widthOnScreen = self.widthOnScreen 
##                    print self.widthOnScreen, self.heightOnScreeen
##                    
##                    self.mapAerial = self.mainMap.canvas.create_image(self.widthOnScreen,self.heightOnScreeen, image = self.jpgPI)
##                    self.ImageList.append(self.mapAerial)
##
##

##                for geometry in imageObject.Geometry[0]:
##                    print geometry
