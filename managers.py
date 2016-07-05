from Tkinter import Canvas, PhotoImage, Button, SINGLE, Frame

#from CCWD.views import get_geoObjectsInRec, get_exif,geopics, check_pointWithinPoly, COLORS
from Tkinter import *
from PIL import Image, ImageTk

# MAP OBJECTS



COLORS  =['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']       
            

class Map(object):

    def __init__(self,frame,  width,height):
        self.frame = frame
        self.heightmap = height
        self.widthmap = width   
        self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollbarX.pack(side=BOTTOM, fill=X)
        self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbarY.pack(side=RIGHT, fill=Y)    
        self.canvas = Canvas(self.frame,background='light grey',
                             width = self.widthmap, 
                             height = self.heightmap,
                             
                             borderwidth=3,
                             relief = SUNKEN,
                             selectborderwidth=3.0,
                             selectforeground='lime green',)
        self.canvas.pack(side=TOP)
        
        #self.scrollbarX.config(command=self.canvas.xview)
        #self.scrollbarY.config(command=self.canvas.yview)

class MapImages(object):

    def __init__(self,frame,  width,height):
        self.frame = frame
        self.heightmap = height
        self.widthmap = width   
        #self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        #self.scrollbarX.pack(side=BOTTOM, fill=X)
        #self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        #self.scrollbarY.pack(side=RIGHT, fill=Y)    
        self.canvas = Canvas(self.frame,background='light grey',
                             width = self.widthmap, 
                             height = self.heightmap,
                             
                             borderwidth=3,
                             relief = SUNKEN,
                             selectborderwidth=3.0,
                             selectforeground='lime green',)
        self.canvas.pack(side=TOP)
        
        #self.scrollbarX.config(command=self.canvas.xview)
        #self.scrollbarY.config(command=self.canvas.yview)
                
class PictureWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        self.canvas = Canvas(self.frame,background='light grey',width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken')
        self.canvas.pack(side=TOP)
class ImageWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        self.canvas = Canvas(self.frame,background='light grey',width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken')


class ImageSideWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
  
        self.canvas = Canvas(self.frame,background='light grey',
                             width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken',
                             )

class CalendarSideWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
  
        self.canvas = Canvas(self.frame,background='white',
                             width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken',
                             )

class TableWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        
        

        self.canvas = Canvas(self.frame,background='white',width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken')


class TableWindowScroll(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        
        
        self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollbarX.pack(side=TOP, fill=X)
        self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbarY.pack(side=LEFT, fill=Y)   
        self.canvas = Canvas(self.frame,background='white',width = self.widthIMap, height = self.heightIMap,
                             borderwidth=3,relief='sunken')
        self.canvas.pack(side=TOP)
        self.scrollbarX.config(command=self.canvas.xview)
        self.scrollbarY.config(command=self.canvas.yview)
        #self.canvas.config(scrollregion=self.canvas.bbox(ALL))
class TableWindowScrollGrid(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        
        
        self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollbarX.grid(row=0,column=0, columnspan=3,sticky=W+E)
        self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbarY.grid(row=0, column=0,rowspan=3, sticky=N+S) 
        self.canvas = Canvas(self.frame,background='white',width = self.widthIMap, height = self.heightIMap,
                             relief='sunken')
        self.canvas.grid(sticky=W+E+N+S, row=1, column=1,rowspan=2,columnspan=2)
        self.scrollbarX.config(command=self.canvas.xview)
        self.scrollbarY.config(command=self.canvas.yview)

class CalendarWindowScroll(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        
        
        self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollbarX.pack(side=BOTTOM, fill=X)
        self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbarY.pack(side=RIGHT, fill=Y)   
        self.canvas = Canvas(self.frame,background='white',width = self.widthIMap, height = self.heightIMap,
                             borderwidth=3,relief='sunken')
        self.canvas.pack(side=TOP)
        self.scrollbarX.config(command=self.canvas.xview)
        self.scrollbarY.config(command=self.canvas.yview)


class LegendWindow(object):
    
    def __init__(self, frame, width,height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        self.canvas = Canvas(self.frame,background='#FFFFFF',width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken')


class Graph(object):
    
    def __init__(self, frame, width,height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        self.canvas = Canvas(self.frame,background='#FFFFFF',
                             width = self.widthIMap,
                             height = self.heightIMap,
                             borderwidth=3,relief='sunken')


class GraphWithScroll2(object):
    
    def __init__(self, frame, width,height):
        self.frame = Frame(frame)
        
        self.heightIMap = height
        self.widthIMap = width 
        scrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        scrollbar.pack(side=BOTTOM, fill=X)

        self.canvas = Canvas(self.frame,background='#FFFFFF',
                             width = self.widthIMap,
                             height = self.heightIMap,
                             borderwidth=3,relief='sunken',
                             )
        self.canvas.pack(side=TOP)
        scrollbar.config(command=self.canvas.xview)

class GraphWithScroll(object):
    
    def __init__(self, frame, width,height):
        self.frame = Frame(frame)
        
        self.heightIMap = height
        self.widthIMap = width 
        self.scrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollbar.pack(side=BOTTOM, fill=X)
        self.scrollbar2 = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar2.pack(side=RIGHT, fill=Y)
        self.canvas = Canvas(self.frame,background='#FFFFFF',
                             width = self.widthIMap,
                             height = self.heightIMap,
                             borderwidth=3,relief='sunken',
                             )
        self.canvas.pack(side=TOP)
        self.scrollbar.config(command=self.canvas.xview)
        self.scrollbar2.config(command=self.canvas.yview)
 

class DataScroll(object):
    
    def __init__(self, frame, width,height):
        self.frame = Frame(frame)
        
        self.heightIMap = height
        self.widthIMap = width 

        self.scrollbar2 = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar2.grid(row=0,column=3, rowspan=2, columnspan=3)
        self.canvas = Canvas(self.frame,background='#FFFFFF',
                             width = self.widthIMap,
                             height = self.heightIMap,
                             borderwidth=3,relief='sunken',
                             )
        self.canvas.grid(row=0,column=0, rowspan=2, columnspan=3)
        self.scrollbar2.config(command=self.canvas.yview)
               
        
class guiButton(object):

    def __init__(self, frame, name,width, height, filepath,  execute):
        self.frame = frame
        self.name = name
        self.width = width
        self.height = height
        self.filepath = filepath
        self.photo = PhotoImage(file = self.filepath)
        self.button = Button(self.frame,background='#FFFFFF',width = self.width, height = self.height, image = self.photo, bd=3,relief='raised', command = execute)
        self.button.image = self.photo

class guiButtonManager(object):

    def __init__(self,ZoomManager):
        self.buttons = { "Pan Up" : {'filepath': r'C:\district\png\Up.gif'},
                         "Pan Left" : {'filepath': r'C:\district\png\Left.gif'},
                         "Pan Right" : {'filepath': r'C:\district\png\Right.gif'},
                         "Pan Down" : {'filepath': r'C:\district\png\Down.gif'},
                         "Zoom In" : {'filepath': r'C:\district\png\MagnifyPlus.gif'},
                         "Zoom Out" : {'filepath': r'C:\district\png\MagnifyMinus.gif'},
                         "Raw Data" : {'filepath': r'C:\district\png\Row.gif'},
                         "Graph" : {'filepath': r'C:\district\png\BarGraph.gif'},
                         "Add Data" : {'filepath': r'C:\district\png\SaveDB.gif'},
                         "Home" : {'filepath': r'C:\district\png\Home.gif'},
                         "Load Pictures": {'filepath': r'C:\district\png\Camera.gif'},
                         "Map": {'filepath': r'C:\district\png\World2.gif'},
                         "Extract Data": {'filepath': r'C:\district\png\DataExtract.gif'},
                         "Big Picture": {'filepath': r'C:\district\png\Binocular.gif'},
                         "Print": {'filepath': r'C:\district\png\Print.gif'},
                         
                         }

       


class ScreenManager(object):

    def __init__(self, root):
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()

        self.windowWidth = root.winfo_screenwidth()
        self.windowHeight = root.winfo_screenheight()

        self.mapcanvasWidth = (self.windowWidth/5) * 2.7
        self.mapcanvasHeight = (self.windowHeight/7) * 5.4
        self.mapcanvaslegendWidth = (self.windowWidth/5) * .6
        self.mapcanvaslegendHeight = (self.windowHeight/7) * 3

        self.mapbuttonFrameWidth = (self.windowWidth/5) * .6
        self.mapbuttonFrameHeight = (self.windowHeight/7) * 2.3

        self.imagecanvasWidth = (self.windowWidth/5) * 3
        self.imagecanvasHeight = (self.windowHeight/7) * 5.4

        self.imagethumbcanvasWidth = (self.windowWidth/6) 
        self.imagethumbcanvasHeight = (self.windowHeight/7) * 1.1

        self.picCanvasWidth = (self.windowWidth/5) * .1
        self.picCanvasHeight = (self.windowHeight/7) * 3

        self.graphCanvasWidth = (self.windowWidth/5) * .1
        self.graphCanvasHeight = (self.windowHeight/7) * 2.3

        self.sideWidths = (self.windowWidth/5) * 1.3
        
        self.tableCanvasWidth = self.windowWidth * .95
        self.tableCanvasHeight = self.windowHeight * .8

        self.calendarCanvasWidth = (self.windowWidth/5) * 2.7
        self.calendarCanvasHeight = self.windowHeight * .85


        self.multiplier = 1
        self.buttonSize = (self.windowWidth/30) * self.multiplier

    

class ZoomManager(object):

    def __init__(self, upperLeft,lowerRight):
        self.zoomList = range(1,11)
        self.currentZoom = 8
        self.upperLeft = upperLeft
        self.lowerRight = lowerRight

        self.currentUpperLeft = self.upperLeft
        self.currentLowerRight = self.lowerRight
        self.centroid = self.upperLeft[0] + ((self.lowerRight[0] - self.upperLeft[0])/2), self.upperLeft[1] - ((self.upperLeft[1] - self.lowerRight[1])/2)
        self.currentWidth = self.currentLowerRight[0] - self.currentUpperLeft[0]  
        self.currentHeight = self.currentUpperLeft[1] - self.currentLowerRight[1]

        self.scale = 1000
        self.multiplier = 1
        self.updatePolyString()
        
    def updatePolyString(self):
        self.currentPolyString = 'POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))' % (self.currentUpperLeft[0],
                                                                                   self.currentUpperLeft[1], #Upper Left
                                                                                   self.currentUpperLeft[0],
                                                                                   self.currentLowerRight[1], #Lower Left Corner
                                                                                   self.currentLowerRight[0],                                                                                   
                                                                                   self.currentLowerRight[1], #Lower Right Corner
                                                                                   self.currentLowerRight[0],
                                                                                   self.currentUpperLeft[1],# Upper Right Corner
                                                                                   self.currentUpperLeft[0],
                                                                                   self.currentUpperLeft[1]) 
        
        self.currentWidth = self.currentLowerRight[0] - self.currentUpperLeft[0]
        self.currentHeight = self.currentUpperLeft[1] - self.currentLowerRight[1]
        self.centroid = self.currentUpperLeft[0] + ((self.currentLowerRight[0] - self.currentUpperLeft[0])/2), self.currentUpperLeft[1] - ((self.currentUpperLeft[1] - self.currentLowerRight[1])/2)
        
        
    def panUp(self):
        self.currentUpperLeft = self.currentUpperLeft[0] ,self.currentUpperLeft[1] + ((self.scale/self.currentHeight)* self.currentHeight) 
        self.currentLowerRight = self.currentLowerRight[0] ,self.currentLowerRight[1] + ((self.scale/self.currentHeight)* self.currentHeight)
        self.updatePolyString()
        print self.currentUpperLeft, self.currentLowerRight, 'buttonUp' 
        
    def panLeft(self):
        self.currentUpperLeft = self.currentUpperLeft[0] -  ((self.scale/self.currentWidth)* self.currentWidth) ,self.currentUpperLeft[1] 
        self.currentLowerRight = self.currentLowerRight[0]  - ((self.scale/self.currentWidth)* self.currentWidth) ,self.currentLowerRight[1]
        self.updatePolyString()        
        print self.currentUpperLeft, self.currentLowerRight,'buttonLeft' 

    def panDown(self):
        self.currentUpperLeft = self.currentUpperLeft[0] ,self.currentUpperLeft[1] - ((self.scale/self.currentHeight)* self.currentHeight)
        self.currentLowerRight = self.currentLowerRight[0],self.currentLowerRight[1]  - ((self.scale/self.currentHeight)* self.currentHeight)
        self.updatePolyString()        
        print self.currentUpperLeft, self.currentLowerRight, 'buttonDown' 
        
    def panRight(self):
        self.currentUpperLeft = self.currentUpperLeft[0]  + ((self.scale/self.currentWidth)* self.currentWidth) , self.currentUpperLeft[1]
        self.currentLowerRight = self.currentLowerRight[0] + ((self.scale/self.currentWidth)* self.currentWidth) , self.currentLowerRight[1] 
        
        self.updatePolyString()    
        print self.currentUpperLeft, self.currentLowerRight, 'buttonRight'   

    def zoomin(self, screenx, screeny):
        print screenx, screeny, 'points'
        

        diffWidth = self.currentWidth #abs(self.currentUpperLeft[0] -float(self.currentLowerRight[0]))
        diffHeight = self.currentHeight
        # (((diffX/diffWidth) * 2.0) * (diffWidth/2.0))/2
        diffX0 = (float(screenx) - self.currentUpperLeft[0]) 
        diffY0 = (self.currentUpperLeft[1] - float(screeny))
        #(self.currentUpperLeft[1] - float(self.currentLowerRight[1]))
        perX0 = diffX0/diffWidth
        perY0 = diffY0/diffHeight
        decDiffY0 = diffY0 * perX0 #/ 2.0  # (((diffY/float(diffHeight)) * 2.0) * (diffHeight/2.0))/2
        decDiffX0 = diffX0 * perY0  #/2.0
        print diffX0, diffY0,perX0, perY0 ,'diff'
        print decDiffX0, decDiffY0, 'In'


        diffX1 = (float(screenx) - self.currentUpperLeft[0]) 
        diffY1 = (self.currentUpperLeft[1] - float(screeny))
        #(self.currentUpperLeft[1] - float(self.currentLowerRight[1]))
        perX1 = 1- (diffX1/diffWidth)
        perY1 = 1-(diffY1/diffHeight)
        decDiffY1 = diffY1 * perX1 #/ 2.0  # (((diffY/float(diffHeight)) * 2.0) * (diffHeight/2.0))/2
        decDiffX1 = diffX1 * perY1  #/2.0
        print diffX1, diffY1,perX1, perY1 ,'diff'
        print decDiffX1, decDiffY1, 'In'


        currentUpperLeft0 = self.currentUpperLeft[0] + decDiffX0
        currentUpperLeft1 = self.currentUpperLeft[1] - decDiffY0
#
        currentLowerRight0 = self.currentLowerRight[0] - (diffWidth/2.0)  + decDiffX1
        currentLowerRight1 = self.currentLowerRight[1] + (diffHeight/2.0) - decDiffY1

        self.currentUpperLeft = currentUpperLeft0,currentUpperLeft1
        self.currentLowerRight = currentLowerRight0, currentLowerRight1
        
        self.updatePolyString()
        print self.currentUpperLeft, self.currentLowerRight, 'Zoom In ' ,self.scale
        print
        #self.scale =   self.scale/2.0

    def zoomout(self,screenx,screeny):
        diffX = (float(screenx) - self.currentUpperLeft[0]) 
        diffWidth = self.currentWidth #abs(self.currentUpperLeft[0] -float(self.currentLowerRight[0]))
        decDiffX = diffX #* 2.0# (((diffX/diffWidth) * 2.0) * (diffWidth/2.0))/2
        
        diffY = (self.currentUpperLeft[1] - float(screeny))
        diffHeight = self.currentHeight#(self.currentUpperLeft[1] - float(self.currentLowerRight[1]))
        decDiffY = diffY #* 2.0  # (((diffY/float(diffHeight)) * 2.0) * (diffHeight/2.0))/2
        print decDiffX, decDiffY, "Out"
        currentUpperLeft0 = self.currentUpperLeft[0]   - decDiffX
        currentUpperLeft1 = self.currentUpperLeft[1]    + decDiffY
#
        currentLowerRight0 = self.currentLowerRight[0] + (diffWidth)  - decDiffX
        currentLowerRight1 = self.currentLowerRight[1] - (diffHeight) + decDiffY

        self.currentUpperLeft = currentUpperLeft0,currentUpperLeft1
        self.currentLowerRight = currentLowerRight0, currentLowerRight1
                                  
        self.updatePolyString()
        print self.currentUpperLeft, self.currentLowerRight, 'Zoom Out ' ,self.scale  
        print
        #self.scale =   self.scale * 2.0


class ZoomManager2(object):

    def __init__(self, upperLeft,lowerRight):
        self.zoomList = range(1,18)
        self.currentZoom = 1
        self.upperLeft = upperLeft
        self.lowerRight = lowerRight

        self.currentUpperLeft = self.upperLeft
        self.currentLowerRight = self.lowerRight
        self.centroid = self.upperLeft[0] + ((self.lowerRight[0] - self.upperLeft[0])/2), self.upperLeft[1] - ((self.upperLeft[1] - self.lowerRight[1])/2)
        self.currentWidth = self.currentLowerRight[0] - self.currentUpperLeft[0]  

        self.scaleList = [250000,100000, 50000,25000,12000, 10000,
                      8000,6000,5000,4000,3000,2000,1500,1000,500,250,100]
        self.scale = self.scaleList[self.currentZoom]
        self.multiplier = 1000
        self.updatePolyString()
        
    def updatePolyString(self):
        self.currentPolyString = 'POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))' % (self.currentUpperLeft[0],
                                                                                   self.currentUpperLeft[1], #Upper Left
                                                                                   self.currentUpperLeft[0],
                                                                                   self.currentLowerRight[1], #Lower Left Corner
                                                                                   self.currentLowerRight[0],                                                                                   
                                                                                   self.currentLowerRight[1], #Lower Right Corner
                                                                                   self.currentLowerRight[0],
                                                                                   self.currentUpperLeft[1],# Upper Right Corner
                                                                                   self.currentUpperLeft[0],
                                                                                   self.currentUpperLeft[1]) 
        
        self.currentWidth = self.currentLowerRight[0] - self.currentUpperLeft[0]
        self.currentHeight = self.currentUpperLeft[1] - self.currentLowerRight[1]
        self.centroid = self.currentUpperLeft[0] + ((self.currentLowerRight[0] - self.currentUpperLeft[0])/2), self.currentUpperLeft[1] - ((self.currentUpperLeft[1] - self.currentLowerRight[1])/2)
        
        
    def panUp(self):
        self.currentUpperLeft = self.currentUpperLeft[0] ,self.currentUpperLeft[1] + (self.scale)
        self.currentLowerRight = self.currentLowerRight[0] ,self.currentLowerRight[1] + (self.scale )
        self.updatePolyString()
        #print self.currentUpperLeft, self.currentLowerRight, 'buttonUp' ,self.scale
        
    def panLeft(self):
        self.currentUpperLeft = self.currentUpperLeft[0] - self.scale ,self.currentUpperLeft[1] 
        self.currentLowerRight = self.currentLowerRight[0]  - self.scale,self.currentLowerRight[1]
        self.updatePolyString()        
        #print self.currentUpperLeft, self.currentLowerRight,'buttonLeft' ,self.scale

    def panDown(self):
        self.currentUpperLeft = self.currentUpperLeft[0] ,self.currentUpperLeft[1] - self.scale
        self.currentLowerRight = self.currentLowerRight[0],self.currentLowerRight[1]  - self.scale
        self.updatePolyString()        
        #print self.currentUpperLeft, self.currentLowerRight, 'buttonDown' ,self.scale
        
    def panRight(self):
        self.currentUpperLeft = self.currentUpperLeft[0]  + (self.scale ), self.currentUpperLeft[1]
        self.currentLowerRight = self.currentLowerRight[0] + (self.scale ), self.currentLowerRight[1] 
        
        self.updatePolyString()    
        #print self.currentUpperLeft, self.currentLowerRight, 'buttonRight' ,self.scale    

    def zoomin(self, screenx, screeny):
        diffX = (float(screenx) - self.currentUpperLeft[0]) 

        diffWidth = abs(self.currentUpperLeft[0] -float(self.currentLowerRight[0]))
        
        decDiffX = diffX/2.0# (((diffX/diffWidth) * 2.0) * (diffWidth/2.0))/2
        
        diffY = (self.currentUpperLeft[1] - float(screeny))
        diffHeight = (self.currentUpperLeft[1] - float(self.currentLowerRight[1]))
        
        decDiffY = diffY/2.0  # (((diffY/float(diffHeight)) * 2.0) * (diffHeight/2.0))/2
        #print decDiffX, decDiffY, 'In'

        currentUpperLeft0 = self.currentUpperLeft[0] + decDiffX
        currentUpperLeft1 = self.currentUpperLeft[1] - decDiffY
#
        currentLowerRight0 = self.currentLowerRight[0] - (diffWidth/2.0)  + decDiffX
        currentLowerRight1 = self.currentLowerRight[1] + (diffHeight/2.0) - decDiffY

        self.currentUpperLeft = currentUpperLeft0,currentUpperLeft1
        self.currentLowerRight = currentLowerRight0, currentLowerRight1
        
        self.updatePolyString()
        #print self.currentUpperLeft, self.currentLowerRight, 'Zoom In ' ,self.scale
        self.scale =   self.scale/2.0

    def zoomout(self,screenx,screeny):
        diffX = (float(screenx) - self.currentUpperLeft[0]) 
        diffWidth = abs(self.currentUpperLeft[0] -float(self.currentLowerRight[0]))
        decDiffX = diffX #* 2.0# (((diffX/diffWidth) * 2.0) * (diffWidth/2.0))/2
        
        diffY = (self.currentUpperLeft[1] - float(screeny))
        diffHeight = (self.currentUpperLeft[1] - float(self.currentLowerRight[1]))
        decDiffY = diffY #* 2.0  # (((diffY/float(diffHeight)) * 2.0) * (diffHeight/2.0))/2
        #print decDiffX, decDiffY, "Out"
        currentUpperLeft0 = self.currentUpperLeft[0]   - decDiffX
        currentUpperLeft1 = self.currentUpperLeft[1]    + decDiffY
#
        currentLowerRight0 = self.currentLowerRight[0] + (diffWidth)  - decDiffX
        currentLowerRight1 = self.currentLowerRight[1] - (diffHeight) + decDiffY

        self.currentUpperLeft = currentUpperLeft0,currentUpperLeft1
        self.currentLowerRight = currentLowerRight0, currentLowerRight1
                                  
        self.updatePolyString()
        #print self.currentUpperLeft, self.currentLowerRight, 'Zoom Out ' ,self.scale  
        self.scale =   self.scale * 2.0




class ScaleManager(object):

    def __init__(self, master, zoomManager, execute):
        from Tkinter import Scale, VERTICAL, HORIZONTAL
        self.max = 10
        self.min = 1
        self.scalevalues = [ 60, 120, 250, 500,1000, 2500, 5000, 10000, 20000, 40000 ]
        self.scale = Scale(master, from_=self.max, to=self.min, orient=HORIZONTAL, command=execute)
        self.scale.set(zoomManager.currentZoom) 


class ImageManager(object):

    def __init__(self):
        self.tileDic = {}
        self.tileCOORDIC = {}
        
    def update(self, geoObject, ZoomManager):
##        self.newImgs = get_geoObjectsInRec(geoObject,
##                                      ZoomManager.currentUpperLeft[1],
##                                      ZoomManager.currentLowerRight[0],
##                                      ZoomManager.currentUpperLeft[0],
##                                      ZoomManager.currentLowerRight[1], )  
        self.newImgs = get_geoObjectsInRec(geoObject,ZoomManager.currentPolyString)  
        for imageObject in self.newImgs:

            cornerUL =  imageObject.Geometry[0][0]
#            centroid = imageObject.Geometry[0].centroid
#            x = centroid.x
#            y = centroid.y
            x = cornerUL[0]
            y = cornerUL[1]
            
            self.tileDic[x,y] = imageObject.sheetName

        
        X = []
        Y = []
        
        for keys in self.tileDic.keys():
            if keys[0] not in X:
                X.append(keys[0])
            if keys[1] not in Y:
                Y.append(keys[1])
        

        X.sort()
        Y.sort()
        Y.reverse()
        
        
        for COUNTERX, x in enumerate(X):
            
            for COUNTERY, y in enumerate(Y):
                
                if (x,y) in self.tileDic.keys():
                    self.tileCOORDIC[COUNTERX + 1, COUNTERY + 1] = self.tileDic[x,y]

        self.COUNTERX = COUNTERX + 1
        self.COUNTERY = COUNTERY + 1

class ImageProcessor(object):
    
                def __init__(self, filename, divider, ScreenManager):
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenMapImageWidth = ScreenManager.mapcanvasWidth
                            self.screenMapImageHeight = ScreenManager.mapcanvasWidth * (self.boundingBox[2] / self.boundingBox[3])

                        else:
                            self.screenMapImageWidth = ScreenManager.mapcanvasHeight * (float(self.boundingBox[3])/self.boundingBox[2])

                            self.screenMapImageHeight = ScreenManager.mapcanvasHeight
                        
                        self.tilescreen = self.tile.resize((int(self.screenMapImageWidth/divider), int(self.screenMapImageHeight/divider)), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen)
                    
class ImageProcessor2(object):
    
                def __init__(self, filename, divider, ScreenManager):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        
                        self.boundingBox = self.tile.getbbox()

                        self.screenMapImageWidth = ScreenManager.sideWidths + 10  #* (float(self.boundingBox[2])/self.boundingBox[3])
                        self.screenMapImageHeight = ScreenManager.picCanvasHeight
    
                        self.tilescreen = self.tile.resize((int(self.screenMapImageWidth/divider), int(self.screenMapImageHeight/divider)), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen)                    

class ImageProcessor3(object):
    
                def __init__(self, filename,ScreenManager):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        self.exifdata = get_exif(filename)
                        self.lat,self.long = geopics(self.exifdata)
                       
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenImageWidth = ScreenManager.imagecanvasWidth * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenImageHeight = ScreenManager.imagecanvasWidth 

                        else:
                            self.screenImageWidth = ScreenManager.imagecanvasHeight

                            self.screenImageHeight = ScreenManager.imagecanvasHeight  * (float(self.boundingBox[3])/self.boundingBox[2])
                        
                        self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 


class ImageProcessorPreview(object):
    
                def __init__(self, filename,ScreenManager):
                        from PIL import Image, ImageTk
                        print filename
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        #self.exifdata = get_exif(filename)
                        #self.lat,self.long = geopics(self.exifdata)
                        limiter = (ScreenManager.imagecanvasWidth/5)
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenImageWidth = (ScreenManager.imagecanvasWidth -limiter) * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenImageHeight = ScreenManager.imagecanvasWidth -limiter 

                        else:
                            self.screenImageWidth = ScreenManager.imagecanvasHeight - limiter

                            self.screenImageHeight = (ScreenManager.imagecanvasHeight -limiter)  * (float(self.boundingBox[3])/self.boundingBox[2])
                        
                        self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessorPreviewSide(object):
    
                def __init__(self, filename,width):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        self.exifdata = get_exif(filename)
                        self.lat,self.long = geopics(self.exifdata)
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenMapImageWidth = width * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenMapImageHeight = width 
                        else:
                            self.screenMapImageWidth = width
                            self.screenMapImageHeight = width * (float(self.boundingBox[3])/self.boundingBox[2])
                            
                        self.tilescreen = self.tile.resize((int(self.screenMapImageWidth), int(self.screenMapImageHeight)), Image.ANTIALIAS)
                        del self.tile
                        #self.tilescreen.save
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessorResizeBig(object):
    
                def __init__(self, filename,ScreenManager):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        #self.exifdata = get_exif(filename)
                        #self.lat,self.long = geopics(self.exifdata)
                       
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenImageWidth = ScreenManager.imagecanvasWidth * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenImageHeight = ScreenManager.imagecanvasWidth 

                        else:
                            self.screenImageWidth = ScreenManager.imagecanvasHeight

                            self.screenImageHeight = ScreenManager.imagecanvasHeight  * (float(self.boundingBox[3])/self.boundingBox[2])
                        
                        self.tilescreen = self.tile.resize((int(self.screenImageWidth)*2, int(self.screenImageHeight)*2), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessorResizeSmall(object):
    
                def __init__(self, filename,ScreenManager):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        #self.exifdata = get_exif(filename)
                        #self.lat,self.long = geopics(self.exifdata)
                       
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenImageWidth = ScreenManager.imagecanvasWidth * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenImageHeight = ScreenManager.imagecanvasWidth 

                        else:
                            self.screenImageWidth = ScreenManager.imagecanvasHeight

                            self.screenImageHeight = ScreenManager.imagecanvasHeight  * (float(self.boundingBox[3])/self.boundingBox[2])
                        
                        self.tilescreen = self.tile.resize((int(self.screenImageWidth)/2, int(self.screenImageHeight)/2), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessor4(object):
    
                def __init__(self, filename,width):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        self.boundingBox = self.tile.getbbox()
                        self.exifdata = get_exif(filename)
                        self.lat,self.long = geopics(self.exifdata)
                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenMapImageWidth = width * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenMapImageHeight = width 
                        else:
                            self.screenMapImageWidth = width
                            self.screenMapImageHeight = width * (float(self.boundingBox[3])/self.boundingBox[2])
                            
                        self.tilescreen = self.tile.resize((int(self.screenMapImageWidth), int(self.screenMapImageHeight)), Image.ANTIALIAS)
                        del self.tile
                        #self.tilescreen.save
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessor5(object):
    
                def __init__(self, filename):
                        from PIL import Image, ImageTk

                        self.tile = Image.open(filename)
                        

    

                        self.jpgPI = ImageTk.PhotoImage(self.tile)   
class ImageProcessor6(object):
    
                def __init__(self, filename,ScreenManager):
                        "used for the extracting of detailed info about images"
                        from PIL import Image, ImageTk
                        self.filename = filename
                        self.tile = Image.open(filename)
                        #self.boundingBox = self.tile.getbbox()
                        #self.exifdata = get_exif(filename)
                        #self.lat,self.long = geopics(self.exifdata)
                       

                        self.jpgPI = ImageTk.PhotoImage(self.tile)                         

class Pictures(object):
    
    def __init__(self, ZoomManager):
        self.issuePics = get_geoObjectsInRec(IssuePhotos,ZoomManager.currentPolyString)  
        self.wetlandsPics = get_geoObjectsInRec(WetlandsPhotos,ZoomManager.currentPolyString)  
        

class PolygonManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor, fcolor):
        
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.coords = coords
        self.ocolor = ocolor
        self.fcolor = fcolor
        self.polygon = self.map.create_polygon(self.coords, outline=self.ocolor,fill=self.fcolor, activeoutline="yellow")


class PolygonManager2(object):
    
    def __init__(self, geoObject,ScreenManager, ZoomManager,MapCanvas,GraphCanvas, Legend):
        
        self.geoObject = geoObject
        self.name = geoObject.namestring
        self.graphable = geoObject.graph
        self.sManager = ScreenManager
        self.zManager = ZoomManager
        self.zManager.updatePolyString()
        self.legend = Legend
        self.graph = GraphCanvas.canvas
        self.graphMaster = GraphCanvas
        self.map = MapCanvas.canvas
        self.zManager.updatePolyString()
        self.originalUpperLeftX = self.zManager.currentUpperLeft[0]
        self.originalUpperLeftY = self.zManager.currentUpperLeft[1]
        self.originalLowerRightX = self.zManager.currentLowerRight[0]
        self.originalLowerRightY = self.zManager.currentLowerRight[1]
        self.originalCoordWidth = self.zManager.currentWidth
        self.originalCoordHeight = self.zManager.currentHeight
        self.originalmapcanvasWidth = self.zManager.scale#ScreenManager.mapcanvasWidth
        self.originalmapcanvasHeight = self.zManager.scale#ScreenManager.mapcanvasHeight
        self.dataset = {}
        
    def updatePolyData(self,graphcolor,mapcolor):
        self.zManager.updatePolyString()
        self.currentUpperLeftX = self.zManager.currentUpperLeft[0]
        self.currentUpperLeftY = self.zManager.currentUpperLeft[1]
        self.currentLowerRightX = self.zManager.currentLowerRight[0]
        self.currentLowerRightY = self.zManager.currentLowerRight[1]
        self.currentCoordWidth = self.zManager.currentWidth
        self.currentCoordHeight = self.zManager.currentHeight
        #self.mapcanvasWidth = self.sManager.mapcanvasWidth
        #self.mapcanvasHeight = self.sManager.mapcanvasHeight
        self.mapcanvasWidth = self.zManager.scale * self.zManager.multiplier
        self.mapcanvasHeight = self.zManager.scale * self.zManager.multiplier
        self.transformPolyData(graphcolor,mapcolor)



    def polysInWindowFunc(self):
        self.polysInWindow = []
        self.zManager.updatePolyString()
        self.polysInWindow = get_geoObjectsInRec(self.geoObject, self.zManager.currentPolyString)
        
            
    def transformPolyData(self, graphcolor,mapcolor ):

        self.mapcolor = mapcolor
        self.graphcolor = graphcolor
        
        def xposition(xval):
                xdist=  xval - self.currentUpperLeftX
                return int((xdist/self.currentCoordWidth) * self.mapcanvasWidth)
                
        def yposition(yval):
                ydist =  self.currentUpperLeftY -yval 
                return int((ydist/self.currentCoordHeight) * self.mapcanvasHeight)
            
        def bothpositions(geom):

#            if len(geom) < 4:
                xVal = xposition(geom[0])
                yVal = yposition(geom[1])
                screencoords.append(xVal)
                screencoords.append(yVal)
#                xdist = geom[0] - self.zManager.currentUpperLeft[0]
#                ydist = self.zManager.currentUpperLeft[1]  -geom[1]
#                xposition = int((xdist/self.currentCoordWidth) * self.sManager.mapcanvasWidth)
#                yposition = int((ydist/self.currentCoordHeight) *(self.sManager.mapcanvasWidth * (self.sManager.mapcanvasHeight/self.sManager.mapcanvasWidth)))
#                                      
#                screencoords.append(xposition)
#                screencoords.append(yposition)            


        self.polysInWindowFunc()
        for COUNTER, polyObject in enumerate(self.polysInWindow):
            geometry = polyObject.Geometry[0]
            area = polyObject.Geometry.area
            screencoords = []

            [bothpositions(geom) for geom in geometry ]


            screenObjectData = {"id": COUNTER,
                                "oid": polyObject.getid(),
                                "name" : polyObject.namefield(),
                                "type" : polyObject.namestring,
                                "geometry" : geometry,
                                "centroid" : polyObject.Geometry.centroid.coords,
                                "envelope" : polyObject.Geometry.envelope.coords,
                                "area" : area,
                                "boundary" : polyObject.Geometry.boundary,
                                "mapcolor" :mapcolor,
                                "screencoords": screencoords,
                                }

            
            legendObject = self.generateSmallLegendObject(COUNTER)

            screenObjectData["legendObject"] = legendObject
            self.dataset[polyObject] = screenObjectData       
        self.allarea = [self.dataset[datacount]["area"] for datacount in self.dataset]
        self.maxy = max(self.allarea)
        for polyObject in self.dataset:
            if polyObject.graph ==1:
                screenObjectData = self.dataset[polyObject]
                graphset = self.generateGraphRect(screenObjectData)
                screenObjectData["graphRect"] = graphset
    def reset(self):
        self.dataset = []
            
    def regeneratePolyData(self,ScreenManager, ZoomManager, graphcolor,mapcolor):
        self.currentUpperLeftX = self.originalUpperLeftX
        self.currentUpperLeftY = self.originalUpperLeftY
        self.currentLowerRightX = self.originalLowerRightX
        self.currentLowerRightY = self.originalLowerRightY
        self.currentCoordWidth = self.originalCoordWidth
        self.currentCoordHeight = self.originalCoordHeight

        self.transformPolyData(graphcolor,mapcolor)
        
    def generatePolygons(self):


            self.polygons = []
            
            for polyObject in self.dataset:
                screenObjectData = self.dataset[polyObject]
                screencoords = screenObjectData["screencoords"]
                fcolor = screenObjectData["mapcolor"]
                name = screenObjectData["name"]
                area = str(screenObjectData["area"])
                centroid = screenObjectData["centroid"]
                if len(screencoords) > 0:
                    polygon = self.map.create_polygon(screencoords, outline="grey",fill=fcolor, activeoutline="yellow")
                    self.map.itemconfig(polygon, tags=(self.name, name, area, centroid ))
                    self.polygons.append(polygon)
                    
                
                
    def regenerateGraphData(self):
        for polyObject in self.dataset:
            screenObjectData = self.dataset[polyObject]
            centroid = screenObjectData["centroid"]
            
            val = check_pointWithinPoly(centroid,self.zManager.currentPolyString)
            
            if val == 1:
                graphset = self.generateGraphRect(screenObjectData)
                screenObjectData["graphRect"] = graphset
            else:
                screenObjectData["graphRect"] = []
                
    def generateGraphRect(self,dataset):
            

            c_width = self.sManager.sideWidths
            c_height = self.sManager.graphCanvasHeight
    
            y_stretch = 15
            # gap between lower canvas edge and x axis
            y_gap = self.sManager.buttonSize *1.5
            # stretch enough to get all data items in
            x_stretch = 15
            x_width = 25
            # gap between left canvas edge and y axis
            x_gap = 20

            x = dataset["id"]
            y= dataset["area"]
            maxy = self.maxy
            yorig = y
            y  = (y/maxy) * (c_height - 100) 
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = int(c_height - (y  + y_gap) + 10)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = int(c_height - y_gap)
            # draw the bar
            databarcoords = [x0, y0, x1, y1]
            databarlabelcoords = [x0+10, y0]
            datalabelcoords = [x0+10, y1+5]
            databarlabel = str(int(yorig ))

            return databarcoords,databarlabelcoords, datalabelcoords, databarlabel
            
            
    def graphDataToScreen(self):
            c_width = self.sManager.sideWidths
            c_height = self.sManager.graphCanvasHeight
    
            y_stretch = 15
            # gap between lower canvas edge and x axis
            y_gap = self.sManager.buttonSize *1.5
            # stretch enough to get all data items in
            x_stretch = 15
            x_width = 25
            x_gap = 20
            ylinebottom = c_height- y_gap
            ylinetop = c_height - ((c_height - 130)   + y_gap)
            xlineleft = x_gap-5
            xlineright = self.sManager.sideWidths
            for polyObject in self.dataset:
                screenObjectData = self.dataset[polyObject]
                name = screenObjectData["name"]
                data = screenObjectData["graphRect"]
                color = screenObjectData["mapcolor"] 

                    
                rect = self.graph.create_rectangle(tuple(data[0]), fill=color, activefill="lime green")
                    
                barlabel = self.graph.create_text(data[1], anchor="s",font="Helvetica 7", justify="center", text=data[3])
                    #id = self.graph.canvas.create_text(x1+2, y1, anchor="sw", text=str(int(y)))
                datalabel = self.graph.create_text(data[2], anchor="n",font="Helvetica 6", justify="center", text=name)
                            
            self.graph.create_rectangle(xlineleft,ylinetop ,xlineleft,ylinebottom )
            self.graph.create_rectangle(xlineleft,ylinebottom ,xlineright,ylinebottom )
            title = self.graph.create_text(self.sManager.buttonSize * 2 + 10, 
                                           self.graphMaster.heightIMap-self.sManager.buttonSize + 5 , 
                                           anchor="nw", font="Helvetica 15", justify="center", text=str(self.name))



    def generateSmallLegendObject(self, id):    

           

            x1= 10 
            x2= x1 + 15
            y1= (id+1) * 20
            y2= y1+15
            screencoords = x1,y1,x2,y2
            return screencoords


    def generateLegendObject(self, id):    


            self.x1= 10 
            self.x2= self.x1 + 50
            self.y1= (id+1) * 50
            self.y2= self.y1+40
            screencoords = self.x1,self.y1,self.x2,self.y2
            return screencoords

            
    def legendDataToScreen(self, id):        
        
            
            legendrect = self.generateLegendObject(id)
            name = self.name.replace(' ','\n')
            self.mainLegend = self.legend.canvas.create_rectangle(legendrect,outline="black",fill=self.mapcolor, activeoutline="red", activewidth=2.0)
            
            self.mainLegendLabel = self.legend.canvas.create_text(legendrect[2]+5,legendrect[1]+5,text=name,anchor="nw")
                        

    def alllegendDataToScreen(self):  
        self.legend.canvas.delete("all")      
        for polyObject in self.dataset:
            screenObjectData = self.dataset[polyObject]
            legendrect = screenObjectData["legendObject"]
            name = screenObjectData["name"]
            color = screenObjectData["mapcolor"] 
            self.legend.canvas.create_rectangle(legendrect,outline="black",fill=color, activeoutline="red", activewidth=2.0)
            
            self.legend.canvas.create_text(legendrect[2]+5,legendrect[1]+5,font="Helvetica 6",text=name,anchor="nw")
             
    def randomizeColors(self):
        for polyObject in self.dataset:
            color =  COLORS[random.randint(0,len(COLORS)-1)]
            screenObjectData = self.dataset[polyObject] 
            screenObjectData["mapcolor"] = color  
            
            
            

class PolygonManager3(object):
    
    def __init__(self, geoObject,ScreenManager, ZoomManager,MapCanvas,GraphCanvas, Legend):
        
        self.geoObject = geoObject
        self.name = geoObject.namestring
        self.graphable = geoObject.graph
        self.sManager = ScreenManager
        self.zManager = ZoomManager
        self.zManager.updatePolyString()
        self.legend = Legend
        self.graph = GraphCanvas.canvas
        self.graphMaster = GraphCanvas
        self.map = MapCanvas.canvas
        self.zManager.updatePolyString()
        self.originalUpperLeftX = self.zManager.currentUpperLeft[0]
        self.originalUpperLeftY = self.zManager.currentUpperLeft[1]
        self.originalLowerRightX = self.zManager.currentLowerRight[0]
        self.originalLowerRightY = self.zManager.currentLowerRight[1]
        self.originalCoordWidth = self.zManager.currentWidth
        self.originalCoordHeight = self.zManager.currentHeight
        self.originalmapcanvasWidth = self.zManager.scale#ScreenManager.mapcanvasWidth
        self.originalmapcanvasHeight = self.zManager.scale#ScreenManager.mapcanvasHeight
        self.dataset = {}
        
    def updatePolyData(self,graphcolor,mapcolor):
        self.zManager.updatePolyString()
        self.currentUpperLeftX = self.zManager.currentUpperLeft[0]
        self.currentUpperLeftY = self.zManager.currentUpperLeft[1]
        self.currentLowerRightX = self.zManager.currentLowerRight[0]
        self.currentLowerRightY = self.zManager.currentLowerRight[1]
        self.currentCoordWidth = self.zManager.currentWidth
        self.currentCoordHeight = self.zManager.currentHeight
        #self.mapcanvasWidth = self.sManager.mapcanvasWidth
        #self.mapcanvasHeight = self.sManager.mapcanvasHeight
        self.mapcanvasWidth = self.zManager.scale * self.zManager.multiplier
        self.mapcanvasHeight = self.zManager.scale * self.zManager.multiplier
        self.transformPolyData(graphcolor,mapcolor)



    def polysInWindowFunc(self):
        self.polysInWindow = []
        self.zManager.updatePolyString()
        
        self.polysInWindow = get_geoObjectsInRec(self.geoObject, self.zManager.currentPolyString)
        
            
    def transformPolyData(self, graphcolor,mapcolor ):

        self.mapcolor = mapcolor
        self.graphcolor = graphcolor
        
        def xposition(xval):
                xdist=  xval - self.currentUpperLeftX
                self.currentCoordWidth = self.zManager.scale
                return int((xdist/self.currentCoordWidth) * 1000)
                
        def yposition(yval):
                ydist =  self.currentUpperLeftY -yval 
                self.currentCoordHeight = self.zManager.scale
                return int((ydist/self.currentCoordHeight) * 1000 )
        def bothpositions(geom):

                xVal = xposition(geom[0])
                yVal = yposition(geom[1])
                screencoords.append(xVal)
                screencoords.append(yVal)
            


        self.polysInWindowFunc()
        for COUNTER, polyObject in enumerate(self.polysInWindow):

            geometry = polyObject.Geometry[0]
            
            area = polyObject.Geometry.area
            
            screencoords = []

            [bothpositions(geom) for geom in geometry ]

            screenObjectData = {"id": COUNTER,
                                "oid": polyObject.getid(),
                                "name" : polyObject.namefield(),
                                "type" : polyObject.namestring,
                                "geometry" : geometry,
                                "centroid" : polyObject.Geometry.centroid.coords,
                                "envelope" : polyObject.Geometry.envelope.coords,
                                "area" : area,
                                "boundary" : polyObject.Geometry.boundary,
                                "mapcolor" :mapcolor,
                                "screencoords": screencoords,
                                }

            
            legendObject = self.generateSmallLegendObject(COUNTER)

            screenObjectData["legendObject"] = legendObject
            self.dataset[polyObject] = screenObjectData       
        self.allarea = [self.dataset[datacount]["area"] for datacount in self.dataset]
        #print self.allarea
        self.maxy = max(self.allarea)
        for polyObject in self.dataset:
            if polyObject.graph ==1:
                screenObjectData = self.dataset[polyObject]
                graphset = self.generateGraphRect(screenObjectData)
                screenObjectData["graphRect"] = graphset
    def reset(self):
        self.dataset = []
            
    def regeneratePolyData(self,ScreenManager, ZoomManager, graphcolor,mapcolor):
        self.currentUpperLeftX = self.originalUpperLeftX
        self.currentUpperLeftY = self.originalUpperLeftY
        self.currentLowerRightX = self.originalLowerRightX
        self.currentLowerRightY = self.originalLowerRightY
        self.currentCoordWidth = self.originalCoordWidth
        self.currentCoordHeight = self.originalCoordHeight

        self.transformPolyData(graphcolor,mapcolor)
        
    def generatePolygons(self):


            self.polygons = []
            
            for polyObject in self.dataset:
                screenObjectData = self.dataset[polyObject]
                screencoords = screenObjectData["screencoords"]
                fcolor = screenObjectData["mapcolor"]
                name = screenObjectData["name"]
                area = str(screenObjectData["area"])
                centroid = screenObjectData["centroid"]
                if len(screencoords) > 0:
                    polygon = self.map.create_polygon(screencoords, outline="grey",fill=fcolor, activeoutline="yellow")
                    self.map.itemconfig(polygon, tags=(self.name, name, area, centroid ))
                    self.polygons.append(polygon)
                    
                
                
    def regenerateGraphData(self):
        for polyObject in self.dataset:
            screenObjectData = self.dataset[polyObject]
            centroid = screenObjectData["centroid"]
            
            val = check_pointWithinPoly(centroid,self.zManager.currentPolyString)
            
            if val == 1:
                graphset = self.generateGraphRect(screenObjectData)
                screenObjectData["graphRect"] = graphset
            else:
                screenObjectData["graphRect"] = []
                
    def generateGraphRect(self,dataset):
            

            c_width = self.sManager.sideWidths
            c_height = self.sManager.graphCanvasHeight
    
            y_stretch = 15
            # gap between lower canvas edge and x axis
            y_gap = self.sManager.buttonSize *1.5
            # stretch enough to get all data items in
            x_stretch = 15
            x_width = 25
            # gap between left canvas edge and y axis
            x_gap = 20

            x = dataset["id"]
            y= dataset["area"]
            maxy = self.maxy
            yorig = y
            y  = (y/maxy) * (c_height - 100) 
            x0 = x * x_stretch + x * x_width + x_gap
            y0 = int(c_height - (y  + y_gap) + 10)
            x1 = x * x_stretch + x * x_width + x_width + x_gap
            y1 = int(c_height - y_gap)
            # draw the bar
            databarcoords = [x0, y0, x1, y1]
            databarlabelcoords = [x0+10, y0]
            datalabelcoords = [x0+10, y1+5]
            databarlabel = str(int(yorig ))

            return databarcoords,databarlabelcoords, datalabelcoords, databarlabel
            
            
    def graphDataToScreen(self):
            c_width = self.sManager.sideWidths
            c_height = self.sManager.graphCanvasHeight
    
            y_stretch = 15
            # gap between lower canvas edge and x axis
            y_gap = self.sManager.buttonSize *1.5
            # stretch enough to get all data items in
            x_stretch = 15
            x_width = 25
            x_gap = 20
            ylinebottom = c_height- y_gap
            ylinetop = c_height - ((c_height - 130)   + y_gap)
            xlineleft = x_gap-5
            xlineright = self.sManager.sideWidths
            for polyObject in self.dataset:
                screenObjectData = self.dataset[polyObject]
                name = screenObjectData["name"]
                data = screenObjectData["graphRect"]
                color = screenObjectData["mapcolor"] 

                    
                rect = self.graph.create_rectangle(tuple(data[0]), fill=color, activefill="lime green")
                    
                barlabel = self.graph.create_text(data[1], anchor="s",font="Helvetica 7", justify="center", text=data[3])
                    #id = self.graph.canvas.create_text(x1+2, y1, anchor="sw", text=str(int(y)))
                datalabel = self.graph.create_text(data[2], anchor="n",font="Helvetica 6", justify="center", text=name)
                            
            self.graph.create_rectangle(xlineleft,ylinetop ,xlineleft,ylinebottom )
            self.graph.create_rectangle(xlineleft,ylinebottom ,xlineright,ylinebottom )
            title = self.graph.create_text(self.sManager.buttonSize * 2 + 10, 
                                           self.graphMaster.heightIMap-self.sManager.buttonSize + 5 , 
                                           anchor="nw", font="Helvetica 15", justify="center", text=str(self.name))



    def generateSmallLegendObject(self, id):    

           

            x1= 10 
            x2= x1 + 15
            y1= (id+1) * 20
            y2= y1+15
            screencoords = x1,y1,x2,y2
            return screencoords


    def generateLegendObject(self, id):    


            self.x1= 10 
            self.x2= self.x1 + 50
            self.y1= (id+1) * 50
            self.y2= self.y1+40
            screencoords = self.x1,self.y1,self.x2,self.y2
            return screencoords

            
    def legendDataToScreen(self, id):        
        
            
            legendrect = self.generateLegendObject(id)
            name = self.name.replace(' ','\n')
            self.mainLegend = self.legend.canvas.create_rectangle(legendrect,outline="black",fill=self.mapcolor, activeoutline="red", activewidth=2.0)
            
            self.mainLegendLabel = self.legend.canvas.create_text(legendrect[2]+5,legendrect[1]+5,text=name,anchor="nw")
                        

    def alllegendDataToScreen(self):  
        self.legend.canvas.delete("all")      
        for polyObject in self.dataset:
            screenObjectData = self.dataset[polyObject]
            legendrect = screenObjectData["legendObject"]
            name = screenObjectData["name"]
            color = screenObjectData["mapcolor"] 
            self.legend.canvas.create_rectangle(legendrect,outline="black",fill=color, activeoutline="red", activewidth=2.0)
            
            self.legend.canvas.create_text(legendrect[2]+5,legendrect[1]+5,font="Helvetica 6",text=name,anchor="nw")
             
    def randomizeColors(self):
        for polyObject in self.dataset:
            color =  COLORS[random.randint(0,len(COLORS)-1)]
            screenObjectData = self.dataset[polyObject] 
            screenObjectData["mapcolor"] = color                  