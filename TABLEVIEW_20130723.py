from Tkinter import *
from managers import *
import Tkinter
import os, random, csv, shutil, xlrd, xlwt, tkMessageBox, tkSimpleDialog
from shapely.wkt import loads
from pysqlite2 import dbapi2 as sqlconn
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import os
import sys
from sqlite3 import dbapi2 
#import shapefile

import tkFileDialog
import pyodbc as pdb
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import shutil, base64, time, datetime
import pyodbc




def generatePRJ(SRID= 26943):
    if SRID == 26943:
        prj =  'PROJCS["NAD83 / California zone 3",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",38.43333333333333],PARAMETER["standard_parallel_2",37.06666666666667],PARAMETER["latitude_of_origin",36.5],PARAMETER["central_meridian",-120.5],PARAMETER["false_easting",2000000],PARAMETER["false_northing",500000],AUTHORITY["EPSG","26943"],AXIS["X",EAST],AXIS["Y",NORTH]]'
    elif SRID == 26910:
        prj = 'PROJCS["NAD83 / UTM zone 10N",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-123],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],AUTHORITY["EPSG","26910"],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
    elif SRID == 4326:
        prj = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],METADATA["World",-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]'
    else:
        prj = ''
    return prj

def dateString(ymd=3):
    import time
    dates = time.localtime()
    
    timepiece = []
    for unit in dates[:ymd]:
        if unit < 10:
            unit = '0' + str(unit)
        timepiece.append(unit)
    date = str(timepiece[1]) + '/' + str(timepiece[2]) + '/' + str(timepiece[0])
    return date


def dateStringYMD(ymd=3):
    import time
    dates = time.localtime()
    
    timepiece = []
    for unit in dates[:ymd]:
        if unit < 10:
            unit = '0' + str(unit)
        timepiece.append(unit)
    date = ''
    for COUNT, times in enumerate(timepiece):
        if COUNT != len(timepiece)-1:
            date += str(times) + '_' 
        else:
            date += str(times)
    return date    

def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in dic.iteritems() if v == val][0]


def openCSV(root):
        import tkFileDialog
        csv = tkFileDialog.askopenfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Open a CSV',defaultextension='.csv',
                                                  filetypes=[('Comma Separated Value', '*.csv')])
        
        return csv
    
def openSS(root):
        import tkFileDialog
        csv = tkFileDialog.askopenfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Open a Spreadsheet',defaultextension='.xls',
                                                  filetypes = [ 
                                                    ('Text File','*.txt'),
                                                    ('Comma Separated Value', '*.csv'), 
                                                    ("Excel 2003",'*.xls'), 
                                                    ('Excel 2010','*.xlsx'),  
                                                    ("Spreadsheets", ("*.csv", "*.xls", "*.xlsx")), 

                                                  ])
        
        return csv

def openSHP(root):
        import tkFileDialog
        shp = tkFileDialog.askopenfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Open a Shapefile',defaultextension='.shp',
                                                  filetypes = [ 
                                                    ('ESRI Shapefile','*.shp'),
                                                  ])
        
        return shp

def saveKML(root):
        import tkFileDialog
        kml = tkFileDialog.asksaveasfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Save the KML',defaultextension='.kml',
                                                  filetypes=[('Keyhole Markup Language', '*.kml')])
        
        return kml.split('.')[0] + '.kml'



def saveDB(root):
        import tkFileDialog
        db = tkFileDialog.asksaveasfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Save a database',defaultextension='.sqlite',
                                                  filetypes=[('Spatialite Database', '*.sqlite')])
        
        return db.split('.')[0] + '.sqlite'



def createFolder(root):
        import tkFileDialog
        folder = tkFileDialog.askdirectory(parent=root,
                                                  initialdir='C:/',
                                                  title='Find the Parent Folder')
        
        return folder


def saveCSV(root):
        import tkFileDialog
        csv = tkFileDialog.asksaveasfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Save a Spreadsheet',defaultextension='.xls',
                                                  filetypes=[
                                                             ("Spreadsheets", ("*.csv", "*.xls")),
                                                             ])
        
        ##print csv    
        return csv


def saveSHP(root):
        import tkFileDialog
        shp = tkFileDialog.asksaveasfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Save the Shapefile',initialfile='.shp',
                                                  filetypes=[('ESRI Shapefile', '*.shp')])
        
        return shp


class calendarTk(Tkinter.Frame): # class calendarTk
    """ Calendar, the current date is exposed today, or transferred to date"""#http://stackoverflow.com/questions/7545315/tkinter-menu-for-chosing-a-date
    def __init__(self,master=None,date=None,dateformat="%d/%m/%Y",command=lambda i:None):
        Tkinter.Frame.__init__(self, master)
        self.dt=datetime.datetime.now() if date is None else datetime.datetime.strptime(date, dateformat) 
        self.showmonth()
        self.command=command
        self.dateformat=dateformat
    def showmonth(self): # Show the calendar for a month
        sc = calendar.month(self.dt.year, self.dt.month).split('\n')
        for t,c in [('<<',0),('<',1),('>',5),('>>',6)]: # The buttons to the left to the right year and month
            Tkinter.Button(self,text=t,relief='flat',command=lambda i=t:self.callback(i)).grid(row=0,column=c)
        Tkinter.Label(self,text=sc[0]).grid(row=0,column=2,columnspan=3) # year and month
        for line,lineT in [(i,sc[i+1]) for i in range(1,len(sc)-1)]: # The calendar
            for col,colT in [(i,lineT[i*3:(i+1)*3-1]) for i in range(7)]: # For each element
                obj=Tkinter.Button if colT.strip().isdigit() else Tkinter.Label # If this number is a button, or Label
                args={'command':lambda i=colT:self.callback(i)} if obj==Tkinter.Button else {} # If this button, then fasten it to the command
                bg='green' if colT.strip()==str(self.dt.day) else 'SystemButtonFace' # If the date coincides with the day of date - make him a green background
                fg='red' if col>=5 else 'SystemButtonText' # For the past two days, the color red
                obj(self,text="%s"% colT,relief='flat',bg=bg,fg=fg,**args).grid(row=line, column=col, ipadx=2, sticky='nwse') # Draw Button or Label
    def callback(self,but): # Event on the button
        if but.strip().isdigit():  self.dt=self.dt.replace(day=int(but)) # If you clicked on a date - the date change
        elif but in ['<','>','<<','>>']:
            day=self.dt.day
            if but in['<','>']: self.dt=self.dt+datetime.timedelta(days=30 if but=='>' else -30) # Move a month in advance / rewind
            if but in['<<','>>']: self.dt=self.dt+datetime.timedelta(days=365 if but=='>>' else -365) #  Year forward / backward
            try: self.dt=self.dt.replace(day=day) # We are trying to put the date on which stood
            except: pass                          # It is not always possible
        self.showmonth() # Then always show calendar again
        if but.strip().isdigit(): self.command(self.dt.strftime(self.dateformat)) # If it was a date, then call the command



class ToolTipManager:

    label = None
    window = None
    active = 0

    def __init__(self):
        "effbot's tool tips manager"
        self.tag = None

    def getcontroller(self, widget):
        if self.tag is None:

            self.tag = "ui_tooltip_%d" % id(self)
            widget.bind_class(self.tag, "<Enter>", self.enter)
            widget.bind_class(self.tag, "<Leave>", self.leave)

            # pick suitable colors for tooltips
            try:
                self.bg = "systeminfobackground"
                self.fg = "systeminfotext"
                widget.winfo_rgb(self.fg) # make sure system colors exist
                widget.winfo_rgb(self.bg)
            except:
                self.bg = "#ffffe0"
                self.fg = "black"

        return self.tag

    def register(self, widget, text):
        widget.ui_tooltip_text = text
        tags = list(widget.bindtags())
        tags.append(self.getcontroller(widget))
        widget.bindtags(tuple(tags))

    def unregister(self, widget):
        tags = list(widget.bindtags())
        tags.remove(self.getcontroller(widget))
        widget.bindtags(tuple(tags))

    # event handlers

    def enter(self, event):
        widget = event.widget
        if not self.label:
            # create and hide balloon help window
            self.popup = Toplevel(bg=self.fg, bd=1)
            self.popup.overrideredirect(1)
            self.popup.withdraw()
            self.label = Label(
                self.popup, fg=self.fg, bg=self.bg, bd=0, padx=2
                )
            self.label.pack()
            self.active = 0
        self.xy = event.x_root + 16, event.y_root + 10
        self.event_xy = event.x, event.y
        self.after_id = widget.after(200, self.display, widget)

    def display(self, widget):
        if not self.active:
            # display balloon help window
            text = widget.ui_tooltip_text
            if callable(text):
                text = text(widget, self.event_xy)
            self.label.config(text=text)
            self.popup.deiconify()
            self.popup.lift()
            self.popup.geometry("+%d+%d" % self.xy)
            self.active = 1
            self.after_id = None

    def leave(self, event):
        widget = event.widget
        if self.active:
            self.popup.withdraw()
            self.active = 0
        if self.after_id:
            widget.after_cancel(self.after_id)
            self.after_id = None


class MapInit(object):
    'Map Menu Class'
    def __init__(self, map, path):
        self.map =os.path.join(path,map)
    def execute(self):
        os.startfile(self.map)
                 
class ExportInit(object):
    'Export Menu Class'
    def __init__(self, export, desc):
        self.export = export
        self.description = desc
    def execute(self):
        self.export()

class AddInit(object):
    'Add Menu Class'
    def __init__(self, add, desc):
        self.add = add
        self.description = desc
    def execute(self):
        self.add()

class RectTracker:
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.item = None
        
    def draw(self, start, end, **opts):
        """Draw the rectangle"""
        return self.canvas.create_rectangle(*(list(start)+list(end)), **opts)
        
    def autodraw(self, **opts):
        """Setup automatic drawing; supports command option"""
        self.start = None
        self.canvas.bind("<Button-1>", self.__update, '+')
        self.canvas.bind("<B1-Motion>", self.__update, '+')
        self.canvas.bind("<ButtonRelease-1>", self.__stop, '+')
        
        self._command = opts.pop('command', lambda *args: None)
        self.rectopts = opts
        
    def __update(self, event):
        if not self.start:
            self.start = [event.x, event.y]
            return
        
        if self.item is not None:
            self.canvas.delete(self.item)
        self.item = self.draw(self.start, (event.x, event.y), **self.rectopts)
        self._command(self.start, (event.x, event.y))
        
    def __stop(self, event):
        self.start = None
        self.canvas.delete(self.item)
        self.item = None

    def stopRect(self):
        self.start = None
        self.canvas.delete(self.item)
        self.item = None
        
    def hit_test(self, start, end, tags=None, ignoretags=None, ignore=[]):
        """
        Check to see if there are items between the start and end
        """
        ignore = set(ignore)
        ignore.update([self.item])
        
        # first filter all of the items in the canvas
        if isinstance(tags, str):
            tags = [tags]
        
        if tags:
            tocheck = []
            for tag in tags:
                tocheck.extend(self.canvas.find_withtag(tag))
        else:
            tocheck = self.canvas.find_all()
        tocheck = [x for x in tocheck if x != self.item]
        if ignoretags:
            if not hasattr(ignoretags, '__iter__'):
                ignoretags = [ignoretags]
            tocheck = [x for x in tocheck if x not in self.canvas.find_withtag(it) for it in ignoretags]
        
        self.items = tocheck
        
        # then figure out the box
        xlow = min(start[0], end[0])
        xhigh = max(start[0], end[0])
        
        ylow = min(start[1], end[1])
        yhigh = max(start[1], end[1])
        
        items = []
        for item in tocheck:
            if item not in ignore:
                x, y = average(groups(self.canvas.coords(item)))
                if (xlow < x < xhigh) and (ylow < y < yhigh):
                    items.append(item)
    
        return items
    
def MatchButton( frame, text, command,bcolor='dark blue', fcolor= 'white',font = 'Times -12 bold', bdsize=9, width=12,height=2 ):

    return Button(frame,text=text,font =font ,bg = bcolor, fg = fcolor,bd = bdsize, width=width,height=height, command=command)

class PolygonManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor, fcolor, data, columns, bbox):
        
        self.map = MapCanvas.canvas
        self.toolTipManager = ToolTipManager()
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns
        self.coords = coords
        self.ocolor = ocolor
        self.fcolor = fcolor
        self.bbox = bbox
        self.polygon = self.map.create_polygon(self.coords, 
                                               outline=self.ocolor,
                                               fill=self.fcolor, 
                                               activeoutline="red",
                                               activefill="yellow",
                                               tags = ('polygon', self.data)
                                               )
        
        
class PointsManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor,  data, columns):
        
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns
        self.coords = coords
        self.ocolor = ocolor
        self.point = self.map.create_oval(self.coords[0]-2,self.coords[1]-2, self.coords[0]+2,self.coords[1]+2, 
                                               fill='orange',outline= 'red',
                                               activefill="yellow",
                                               tags = ('point', self.data)
                                               )
        
               
class LineManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor,  data, columns):
        
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns
        self.coords = coords
        self.ocolor = ocolor
        self.line = self.map.create_line(self.coords, 
                                               fill= self.ocolor,
                                               activefill="yellow",
                                               tags = ('line', self.data)
                                               )        

class MapImages(object):

    def __init__(self,frame,  width,height):
        self.frame = frame
        self.heightmap = height
        self.widthmap = width   
        #self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        #self.scrollbarX.pack(side=BOTTOM, fill=X)
        #self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        #self.scrollbarY.pack(side=RIGHT, fill=Y)    
        self.canvas = Canvas(self.frame,background='white',
                             width = self.widthmap, 
                             height = self.heightmap,
                             
                             borderwidth=3,
                             relief = SUNKEN,
                             selectborderwidth=3.0,
                             selectforeground='lime green',)
        self.canvas.pack(side=TOP)        
        
class CustomImport(object):
        'Dialogue to match data and tables together'
        def __init__(self,root, table, datadic, datalist ):
            
            self.masterselect = Toplevel(root)
            master = self.masterselect
            master.wm_attributes("-topmost", 1)
            master.title('Match Columns')
            self.previewMODE = 0
            self.geoTableIndicator = 0
            
            self.root = root
            self.table = table
            self.datadic = datadic
            self.dataList = datalist
            self.fieldTypes = { 'DOUBLE':'D',
                   'FLOAT':'F',
                   'INTEGER': 'N',
                   'BIGINT':'L',
                   'TEXT':'C',
                   'POLYGON':5,
                  'POINT':1,
                  'LINESTRING':3,
                   }

            self.curspatial()
            master.geometry('+100+100')
            master.iconbitmap(self.root.logoPath)
            self.sqlDialogue = Frame(master, relief=SUNKEN, bd=2, bg=self.root.backgroundcolor)
            self.sqlDialogue.grid(row=0, column=0,rowspan=9,columnspan=9, padx = 1)

            self.sqlMainFrame =  Frame(self.sqlDialogue, relief=SUNKEN, bd=2, bg=self.root.backgroundcolor)
            self.sqlMainFrame.grid(row=0, column=0, sticky = W+E+N+S)
            self.listboxFrame =  Frame(self.sqlMainFrame, bg=self.root.backgroundcolor)
            self.listboxFrame.grid(row=0, column=0,sticky = W+E+N+S, padx = 10,pady = 5)
            
            FRAME1 = Frame(self.listboxFrame, bg=self.root.backgroundcolor)
            FRAME1.grid(row=0,column=0,sticky=N+S,padx = 2,pady = 5, ipadx =5)
            
            
            self.scrollbarTable = Scrollbar(FRAME1, orient=VERTICAL)
            
            self.tableList = Listbox(FRAME1,selectmode=SINGLE,height=10)
            self.tableList.grid(row=0, column=0, )
            self.tableList.bind("<Double-Button-1>", self.addDataTypeInfo)
            self.tableList.bind("<Button-3>", self.calculateVal2)
    
            self.scrollbarTable.grid(row=0, column=1,sticky=N+S )
    
            self.scrollbarTable.config(command=self.tableList.yview)
            self.tableLabel = Label(FRAME1,font=('Times','11','bold'), text = '(A) Existing\nTable Fields')
            self.tableLabel.grid(row=1,column=0,columnspan=2)

            self.FRAME4 = Frame(FRAME1, bg=self.root.backgroundcolor)
            self.FRAME4.grid(row=2,column=0,sticky=N+S,padx = 2,pady = 5)
            
            self.typeDataList = Listbox(self.FRAME4,selectmode=SINGLE,height=10)
            self.typeDataList.grid(row=0, column=0, )        
            self.typeDataList.bind("<Double-Button-1>", self.removeFromTableList)
            self.typeDataList.bind("<Button-3>", self.calculateVal)
    
            self.typeDataLabel = Label(self.FRAME4,font=('Times','11','bold'), text = '(A) Selected')
            self.typeDataLabel.grid(row=1,column=0,columnspan=2)    
            
    
            columns = 'PRAGMA table_info(%s)' %  self.table
            self.cursorspatial.execute(columns)
            self.results = self.cursorspatial.fetchall()
            self.tableInfoDic = {}
            for result in self.results:
                colname = result[1]
                self.tableInfoDic[colname] = result[2]
                self.tableList.insert(END,colname)
            self.tableList.selection_set(0)
            
            FRAME2 = Frame(self.listboxFrame,  bg=self.root.backgroundcolor)
            FRAME2.grid(row=0,column=1,sticky=N+S,padx = 2,pady = 5, ipadx= 5)        
            self.scrollFieldbar = Scrollbar(FRAME2, orient=VERTICAL)
    
            self.fieldList = Listbox(FRAME2,height=10)
            self.fieldList.grid(row=0, column=0)
            self.fieldList.bind("<Double-Button-1>", self.addshpTypeInfo)
            self.scrollFieldbar.config(command=self.fieldList.yview)
            self.scrollFieldbar.grid(row=0,column=1, sticky=N+S)
            self.shapeLabel = Label(FRAME2,font=('Times','11','bold'), text = '(B) Incoming\nData Fields')
            self.shapeLabel.grid(row=1,column=0,columnspan=2)        
            self.fields = self.dataList
            for result in self.fields:
                    
                    self.fieldList.insert(END,result)    

            if 'Geometry' in self.tableInfoDic.keys() and 'Geometry' in self.fields:
                    self.geoTableIndicator = 1            
            FRAME5 = Frame(FRAME2, bg=self.root.backgroundcolor) 
            FRAME5.grid(row=2,column=0,sticky=N+S,padx = 2,pady = 5)
            
            self.shpDataList = Listbox(FRAME5,selectmode=SINGLE,height=10)
            self.shpDataList.grid(row=0, column=0, )        
            self.shpDataList.bind("<Double-Button-1>", self.removeFromShpList)
            self.shpDataLabel = Label(FRAME5,font=('Times','11','bold'), text = '(B) Selected')
            self.shpDataLabel.grid(row=1,column=0,columnspan=2)    
    
            self.FRAME3 = Frame(self.listboxFrame,  bg=self.root.backgroundcolor)
            self.FRAME3.grid(row=0,column=2,sticky=N+S,padx = 2,pady = 5)    
            self.matchCanvas = Canvas(self.FRAME3,bg='white', width=400, height=400)
            self.matchCanvas.grid(row=0, column=2)

            BUTTONFRAME = Frame(self.sqlMainFrame,  bg=self.root.backgroundcolor)
            BUTTONFRAME.grid(row=1,column=0,sticky=N+E+W+S,padx = 2,pady = 5)
            generateButton = MatchButton(BUTTONFRAME, 'Test\nMatches', self.generateMatches)
            generateButton.grid(row=0,column=0)
            sortButton = MatchButton(BUTTONFRAME,'Auto Sort\nFields', self.autoSort)
            sortButton.grid(row=0,column=1)
            ResetButton = MatchButton(BUTTONFRAME,'Reset\nFields',self.resets)
            ResetButton.grid(row=0,column=2) 
            previewButton = MatchButton(BUTTONFRAME,'Preview Data',self.previewTable)  
            previewButton.grid(row=0,column=3)       
#            RestartSHPButton = MatchButton(BUTTONFRAME,'Find New\nShapefile',self.restartSHP)
#            RestartSHPButton.grid(row=1,column=1)   
#            RestartButton = MatchButton(BUTTONFRAME,'Find New\nTable',self.restartTable)
#            RestartButton.grid(row=1,column=0)    
#            PreviewButton = MatchButton(BUTTONFRAME,'Quit\nMatching',self.previewTable, color='dark red')
#            PreviewButton.grid(row=1,column=2)  
            ADDFRAME = Frame(BUTTONFRAME,  bg=self.root.backgroundcolor,relief=GROOVE,bd=4)
            ADDFRAME.grid(row=0,column=5, rowspan=2, columnspan=2,sticky=N+E+W+S,padx = 2,pady = 5)
            self.addButton = MatchButton(ADDFRAME,'Add\nData',self.addData, bcolor='dark red')        
            
        
            
            self.startPage()    
            if self.geoTableIndicator == 1:
                CHECKFRAME = Frame(BUTTONFRAME,  bg=self.root.backgroundcolor)
                CHECKFRAME.grid(row=0,column=3, rowspan=2, columnspan=2,sticky=N+E+W+S,padx = 2,pady = 5)
                
                SRIDFRAME  = Frame(CHECKFRAME,  bg=self.root.backgroundcolor,relief=GROOVE,bd=4)
                SRIDFRAME.grid(row=0,column=0,sticky=N+E+W+S,padx = 1,pady = 5)

                MODES = [
                    ("State Plane Meters", "26943"),
                    ("State Plane Feet", "2227"),
                    ("UTM Zone 10 Meters", "26910"),
                    ("Latitude/Longitude", "4326"),
                ]
                
                self.srid = StringVar()
                 # initialize
                COUNTER = 0
                for  text, mode in MODES:
                    b = Radiobutton(SRIDFRAME, text=text,  bg=self.root.backgroundcolor,
                                    variable=self.srid,indicatoron =0,
                                     value=mode, anchor='nw',
                                     relief=GROOVE,
                                     )
                    
                    b.grid(row=COUNTER,column=0,sticky=E+W)
                    
                    COUNTER +=1
                self.srid.set("26943")
        
                QUESTIONFRAME  = Frame(CHECKFRAME,  bg=self.root.backgroundcolor,relief=GROOVE,bd=4)
                QUESTIONFRAME.grid(row=0,column=1,sticky=N+E+W+S,padx = 1,pady = 5)
                
                self.GEO = IntVar()
                
                cGEO = Checkbutton(QUESTIONFRAME, text="Auto Geo Info", anchor='nw',variable=self.GEO)
                cGEO.grid(row=0,column=0,sticky=E+W)
                cGEO.select()
                self.SRID = IntVar()
                
                cSRID = Checkbutton(QUESTIONFRAME, text="Auto SRID",anchor='nw', variable=self.SRID)
                cSRID.grid(row=1,column=0,sticky=E+W)        
                
                self.FKEYS = IntVar()
                
                #cFKEYS = Checkbutton(QUESTIONFRAME, text="Save Input",anchor='nw', variable=self.FKEYS)
                #cFKEYS.grid(row=2,column=0,sticky=E+W)        
                
                cFKEYS = Checkbutton(QUESTIONFRAME, text="Send Notification",anchor='nw', variable=self.FKEYS)
                cFKEYS.grid(row=3,column=0,sticky=E+W)      
    
    

            
        def curspatial(self):
            from pysqlite2 import dbapi2 as sqlconn
            self.sql_connection = sqlconn.Connection(self.root.mainDB)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
            self.cursorspatial = sqlconn.Cursor(self.sql_connection)
            self.sql_connection.enable_load_extension(1)
            self.sql_connection.load_extension('libspatialite-2.dll') 
  
        def startPage(self):        
            self.matchCanvas.create_text(10,10,anchor = 'nw',font=('Times', '11','bold'), text='Match Fields From Data Table (A) to Current Data(B)')
    
            self.matchCanvas.create_line(10,30, 400, 30)
            
            self.matchCanvas.create_text(10,60, text = 'Double click on the field names to match them', anchor='w',tags=('generated', 'text', 'A'))
            self.matchCanvas.create_text(10,80, text = 'Double click matched fields to remove them', anchor='w',tags=('generated', 'text', 'A'))
            self.matchCanvas.create_text(10,100, text = 'Right click table fields to add a single value for the column', anchor='w',tags=('generated', 'text', 'A'))
            self.matchCanvas.create_text(10,120, text = 'Table = %s' % self.table, anchor='w',tags=('generated', 'text', 'A'))
        

    
        
        def checkTypes(self,tablefield,shapefield):
  
            tbFieldType = self.tableInfoDic[tablefield]
            shpFieldType = type(self.datadic['1'][shapefield])
            self.shapeDataDic = {type(1.0):'FLOAT',
                                 type(1):'INTEGER',
                                 type('a'): 'TEXT',
                                 type(u'a'): 'TEXT',
                                 }
            
            shpFieldTypeVal = self.shapeDataDic[shpFieldType]
            if tbFieldType != shpFieldType:
                val=1
                if tbFieldType == 'real' or tbFieldType == 'DOUBLE' or tbFieldType == 'FLOAT':
                    if shpFieldType == type(1.0):
                        
                        self.shapeDataInfo[shapefield] = shpFieldTypeVal
                        val= 1
                    elif shpFieldType == type(1):
                        self.shapeDataInfo[shapefield] = shpFieldTypeVal
                        val= 2
                    else:
                        shpFieldTypeVal = self.shapeDataDic[shpFieldType]
                        val = 0
                elif   tbFieldType.upper() == 'TEXT' or tbFieldType.find('varchar') != -1:
                    if shpFieldType == type('a') or shpFieldType == type(u'a'):
                        self.shapeDataInfo[shapefield] = shpFieldTypeVal
                        val= 1

                    else:
                        shpFieldTypeVal = self.shapeDataDic[shpFieldType]
                        val = 0                

                elif tbFieldType == 'INTEGER':
                    if shpFieldType == type(1.0):
                        self.shapeDataInfo[shapefield] = shpFieldTypeVal
                        val= 2
                    elif shpFieldType == type(1):
                        self.shapeDataInfo[shapefield] = shpFieldTypeVal
                        val= 1
                    else:
                        shpFieldTypeVal = self.shapeDataDic[shpFieldType]
                        val = 0
                elif tablefield == 'Geometry':

                    if shapefield == "Geometry":

                        shpFieldTypeVal = 'Geometry'
                        val=1
                    
                    else:
                        
                        shpFieldTypeVal = self.shapeDataDic[shpFieldType]
                        val = 0   
                else:
                    print 'ere', tbFieldType, shpFieldTypeVal
                    val= 2    
                    shpFieldTypeVal ='TEXT'     
                return val,tbFieldType, shpFieldTypeVal    
            return val,tbFieldType, shpFieldTypeVal
        
        def genColumnValueslist(self, column):
            keys = self.datadic.keys()
            keys.sort()
            columnValueList = []
            for key in keys:
                values = self.datadic[key]
                columnValueList.append(values[column])
            return columnValueList
        
        def addData(self):
            if self.geoTableIndicator ==1:
                WKTlist = self.genColumnValueslist('Geometry')
                for WKT in WKTlist:
                    if WKT == '':
                        self.geoTableIndicator = 0
                        break
            insertSQL = "INSERT INTO {0} ({1}) VALUES "
            tablefields = ''
            sFields = []
            
            for COUNTER, matches in enumerate(self.fieldMatchesList):
                if matches[0] != 'id' :
                    if matches[0] != 'Geometry':
                        
                        tablefields += "'" +matches[0] + "'," 
        
                    sFields.append(matches[1])
                    
            if self.geoTableIndicator == 1:
                if self.GEO.get() ==1:
                    if 'Acres' in self.tableInfoDic.keys():
                        unitval = 'Acres'
                        
                    elif 'Length' in  self.tableInfoDic.keys():
                        unitval = 'Length'     
                    tablefields += "'" +unitval + "',"
                    if 'Property' in self.tableInfoDic.keys():
                        tablefields += "'" +'Property' + "',"
                    if 'HMU'  in self.tableInfoDic.keys():
                        tablefields += "'" +'HMU' + "',"
                    
                    
                tablefields += 'Geometry'
                sFields.append('Geometry') 
            if tablefields[-1] == ',':
               tablefields = tablefields[:-1]                    
            insertSQLval = insertSQL.format(self.table, tablefields)
            keys = self.datadic.keys()
            for key in keys:
                    records = self.datadic[key]
                    valSQL = ''
                    for COUNTER, field in enumerate(sFields):
                        if field != 'Geometry' and field.find('Value =') == -1:
                            gtype = self.shapeDataInfo[str(field)]
                            
                            valSQL += str('"'+records[str(field)]+'"') + ','
                        elif field.find('Value =') != -1:
                            newval = field.replace('Value = ','')

                            if self.tableInfoDic[self.tablefields[COUNTER]] == 'TEXT':
                                valSQL += "'" + newval + "',"                           
                            else:
                                valSQL +=  newval + ","
                        else:
                            valSQL += str(records[str(field)]) + ','

                    if self.geoTableIndicator == 1:

                        if self.GEO.get() == 1:
                            geoWKTobject = loads(WKTlist[COUNTER]) 
                            if 'Acres' in  self.tableInfoDic.keys():
                                
                                acresVal = geoWKTobject.area * 0.000247105
                                valSQL +=  str(acresVal) + ','  
                                
                                
                            elif 'Length' in  self.tableInfoDic.keys():
                                lengthVal = geoWKTobject.length * 3.28084
                                valSQL +=  str(lengthVal) + ',' 
                                
                            if 'Property' in self.tableInfoDic.keys():
                                propsql =  "SELECT NAME FROM CCWD_PROPERTIES WHERE INTERSECTS(Geometry, ST_GeomFromText('%s'))" % WKTlist[COUNTER]
                                self.cursorspatial.execute(propsql)
                                prop = self.cursorspatial.fetchone()[0] 
                                
                                valSQL +=  '"'+prop +'"' + ','
                            if 'HMU'  in self.tableInfoDic.keys():
                                hmusql =  "SELECT NAME FROM CCWD_ManagementUnits WHERE INTERSECTS(Geometry, ST_GeomFromText('%s'))" % WKTlist[COUNTER]
                                self.cursorspatial.execute(hmusql)
                                #hmu = self.cursorspatial.fetchall()
                                
                                hmu = self.cursorspatial.fetchone()
                                v= ()
                                if type(hmu) == type(v):
                                    valSQL +=  '"'+hmu[0] +'"'+ ','
                                else:
                                    valSQL +=  '"",'           
                        if self.SRID.get()==1:
                            valSQL += "ST_GeomFromText(%s)" % (self.transformSRID(WKTlist[COUNTER], srid.get()))
                        else:
                            valSQL += "ST_GeomFromText('%s',%s)" % (WKTlist[COUNTER], srid.get())

                    if valSQL[-1] == ',':
                       valSQL = valSQL[:-1]  
                    
                    sql = insertSQLval + '(%s)' % valSQL
                     
                    self.cursorspatial.execute(sql)
                    
                        

            if not tkMessageBox.askyesno('Final Assurance', 'Add the data to the database?'):  

                    self.sql_connection.rollback()
                    tkMessageBox.showinfo('Data Rollback', 'Your data was not added to %s' % self.table)

            else:
                self.sql_connection.commit()
                    
                tkMessageBox.showinfo('Data Upload', 'Your data was successfully added to %s' % self.table)
        def generateMatches(self,):
            if self.previewMODE == 1:
                self.tablePreview.destroy()
                self.matchCanvas.grid(row=0, column=2)
                self.previewMODE = 0
            self.matchCanvas.delete('generated')
            self.fieldMatchesList =[]
            self.tablefields = self.typeDataList.get(0, END)
            self.shpfields = self.shpDataList.get(0, END)
            self.shapeDataInfo = {}
            if len(self.tablefields) == len(self.shpfields):
                self.fieldMatchesList = zip(self.tablefields, self.shpfields)

                self.matchCanvas.create_text(10,60, text = 'A', anchor='w',tags=('generated', 'text', 'DataTable Field  (Type)'))
                self.matchCanvas.create_text(200,60, text = 'B', anchor='w',tags=('generated', 'text','Shapefile Field  (Type)'))
                self.matchCanvas.create_line(10,70, 400,70,tags=('generated') )
                customCOUNTER = 0
                statusCOUNTER = 1
                for COUNTER, data in enumerate(self.fieldMatchesList):
                    tablefield = data[0]
                    shapefield = data[1]
                    if shapefield.find('Value =') == -1:
                        typestatus, tType, sType = self.checkTypes(tablefield, shapefield)
                        if typestatus ==1:
                            fontcolor = 'black'
                        elif typestatus ==0:
                            fontcolor = 'red'
                            statusCOUNTER = 0
                        elif typestatus==2:
                            fontcolor = 'orange'
                            statusCOUNTER = 2
                            
                      
                        tText = tablefield + '  (%s)' % tType    
                        sText = shapefield + '  (%s)' % sType    
                    else:
                            fontcolor = 'blue'
                            tText = tablefield + '  (%s)' % self.tableInfoDic[tablefield]    
                            sText = shapefield + '  (%s)' % self.tableInfoDic[tablefield]                           
                            customCOUNTER = 1
                    self.matchCanvas.create_text(10,(COUNTER+2) * 20 + 40,fill=fontcolor, text = tText, anchor='w', tags=('generated', 'text', tablefield))
                    self.matchCanvas.create_text(200,((COUNTER+2) * 20 + 40),fill=fontcolor, text = sText, anchor='w',tags=('generated', 'text', shapefield))
                    self.matchCanvas.create_line(10,(COUNTER+2) * 20 + 50, 400,(COUNTER+2)  * 20 +50,tags=('generated', 'line') )
                
                if statusCOUNTER == 1:
                    self.matchCanvas.create_text(10,385,fill='black', text = 'All Field Types Match', anchor='w',tags=('generated', 'text'))
                
                elif statusCOUNTER == 0:
                    self.matchCanvas.create_text(10,385,fill='black', text = 'Field Types Do Not Match', anchor='w',tags=('generated', 'text'))
                    return
                else :
                    self.matchCanvas.create_text(10,385,fill='black', text = 'We can let it slide this time', anchor='w',tags=('generated', 'text'))
                if customCOUNTER == 1:
                    self.matchCanvas.create_text(10,365,fill='black', text = 'Custom Import Accepted', anchor='w',tags=('generated', 'text'))
                                        
                if statusCOUNTER != 0:
                    self.addButton.grid(row=0,column=0)
                    #self.previewButton.grid(row=1,column=0)
                    
                    
                    
            else:
                self.matchCanvas.create_text(10,60, text = 'The fields must be matched', anchor='w',tags=('generated', 'text', 'A'))
                self.matchCanvas.create_line(10,70, 400,70 ,tags=('generated'))
                


        



        def resets(self,):
            
            self.addButton.grid_forget()
            #self.previewButton.grid_forget()

            self.matchCanvas.delete('generated')
            self.resetTableList()
            self.resetShpList()   
                 
        def autoSort(self,):
            self.addButton.grid_forget()
            self.resets()
            self.fieldMatchesList =[]
            tablefields = self.fieldList.get(0, END)
            shpfields = self.tableList.get(0, END)

            if len(tablefields) == len(shpfields):
                self.fieldMatchesList = zip(tablefields, shpfields)
                tFields = []
                sFields = []   
                for COUNTER, data in enumerate(self.fieldMatchesList):
                    tFields.append(data[0])
                    sFields.append(data[1]) 
                for field in tFields:
                    if field in sFields:
                                   
                        self.shpDataList.insert(END,field)
                        self.typeDataList.insert(END,field)
                generateMatches()
            else:
                self.matchCanvas.create_text(10,60, text = 'The fields do not match', anchor='w',tags=('generated', 'text', 'A'))
                self.matchCanvas.create_line(10,70, 400,70 )        
                    
        def resetShpList(self,):
            self.shpDataList.delete(0,END)

        def resetTableList(self,):
            self.typeDataList.delete(0,END)
                
        def removeFromShpList(self,event):
            self.addButton.grid_forget()
            #self.previewButton.grid_forget()

            self.shpDataList.delete('active', self.shpDataList.curselection())

        def removeFromTableList(self,event):
            self.addButton.grid_forget()
            #self.previewButton.grid_forget()

            self.typeDataList.delete('active', self.typeDataList.curselection())
            
        def addshpTypeInfo(self,event):
            try:
                self.addButton.grid_forget()
                #self.previewButton.grid_forget()

                field = self.fieldList.selection_get()
                if field not in self.shpDataList.get(0,END):
                    self.shpDataList.insert(END,field)
                
            except:
                pass        
        
        def addDataTypeInfo(self,event):
                self.addButton.grid_forget()
                #self.previewButton.grid_forget()

                table = self.tableList.selection_get()
                if table not in self.typeDataList.get(0,END):
                    self.typeDataList.insert(END,table)
                    
        def restartSHP(self,):
            self.addButton.grid_forget()
            #self.previewButton.grid_forget()
            self.takeout()
            self.masterselect = Frame()
            self.shpName = openSHP(self)
            self.root.addCustomSHP() 
        
        def restartTable(self,):
            self.addButton.grid_forget()
            #self.previewButton.grid_forget()
            self.shapeAddSelect()

        def previewTable(self,):
            self.previewMODE = 1
            self.matchCanvas.grid_forget()
            self.tablePreview = TableCanvas(self.FRAME3, newdict=self.datadic)
            self.tablePreview.createTableFrame()
        def getReader(self,shpName):
            shp = str(shpName.replace('.shp',''))
            shpReader =Reader(shp)
            return shpReader
        
        def calculateVal(self,event):

            self.masterselect.iconify()
            title = 'Supply Value'
            try:
                field = self.typeDataList.selection_get()
                #index = self.typeDataList.curselection()[0]
                fields = self.typeDataList.get(0,END)
            
                x =0 
                for f in fields:
                    if f == field:
                        index = 0
                    x+=1
                prompt = 'Please supply a value:'
                val = tkSimpleDialog.askstring(title, prompt)
                self.masterselect.deiconify()
                value = 'Value = ' + str(val)
                self.shpDataList.insert(index, value)
            except:
                pass
        def calculateVal2(self,event):

            self.masterselect.iconify()
            title = 'Supply Value'
            
            field = self.tableList.selection_get()
            #index = self.typeDataList.curselection()[0]
            fields = self.typeDataList.get(0,END)
            if field in fields:
                x =0 
                
                for f in fields:
                    if f == field:
                        index = x


                    x+=1
            else:
                index = END
            prompt = 'Please supply a value:'
            val = tkSimpleDialog.askstring(title, prompt)
            self.masterselect.deiconify()
            self.typeDataList.insert(END, field)
            value = 'Value = ' + str(val)
            self.shpDataList.insert(index, value)
     

class TableWindowScrollGrid(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        
        
        self.scrollbarX = Scrollbar(self.frame, orient=HORIZONTAL)
        self.scrollbarX.grid(row=0,column=0, columnspan=3,sticky=W+E)
        self.scrollbarY = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbarY.grid(row=0, column=3,rowspan=3, sticky=N+S) 
        self.canvas = Canvas(self.frame,background='white',width = self.widthIMap, height = self.heightIMap,
                             borderwidth=3,relief='sunken')
        self.canvas.grid(sticky=W+E+N+S, row=1, column=0,rowspan=2,columnspan=2)
        self.scrollbarX.config(command=self.canvas.xview)
        self.scrollbarY.config(command=self.canvas.yview)
class ScreenManager(object):

    def __init__(self, root):
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()

        self.windowWidth = root.winfo_screenwidth()
        self.windowHeight = root.winfo_screenheight()

        self.wdivider = self.windowWidth/10
        self.hdivider = self.windowHeight/10

        self.mapcanvasWidth = (self.wdivider) * 2.5
        self.mapcanvasHeight = self.mapcanvasWidth* 1

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
        self.matchCanvasWidth = (self.windowWidth/5) * 1
        self.matchCanvasWidth = self.windowHeight * .85


        self.multiplier = 1
        self.buttonSize = (self.windowWidth/30) * self.multiplier


class SelectMenu(object):
    
    def __init__(self, root,dic,execute, title, mode=SINGLE):
        self.masterselect = Toplevel(root)
        self.exe = execute
        self.dic = dic
        master = self.masterselect
        master.wm_attributes("-topmost", 1)
        master.title(title)
        master.maxsize(500,500)
        master.geometry('+100+100')
        master.iconbitmap(root.logoPath)
    
    
        frame2 = Frame(master, height=6, bd=7, relief=SUNKEN)
        frame2.pack(fill=X, padx= 2, pady=2)
    
        frame5 = Frame(frame2, bd=7)
        frame5.pack()
        
        scrollbar = Scrollbar(frame5)
        scrollbar.pack(side=RIGHT, fill= Y)
        
        self.listbox = Listbox(frame5,height = 20, width= 400,
                          selectmode=mode)
        self.listbox.bind("<Double-Button-1>",  lambda x: self.execute() )
        sortTable = self.dic.keys()
        sortTable.sort()
        for keys in sortTable:
            self.listbox.insert(END, keys) 
        
        self.listbox.pack()
        scrollbar.config(command=self.listbox.yview)
        stepButton = Button(frame5, text= 'Next Step',
                             font = 'Gill_Sans_MT -12 bold' ,
                             bg = 'dark blue', fg = 'white',
                             bd = 10, width=12,
                             command = self.execute)
        
        stepButton.pack(side=TOP, pady =5,padx=4)   
        
        
    def execute(self):
        selected = self.listbox.selection_get()
        selSplit = selected.split('\n')
        if len(selSplit)==1:
            tables = self.dic[selSplit[0]]
            self.masterselect.destroy() 
            self.exe(tables) 
        elif len(selSplit) > 1:
            newtables = []
            [newtables.append(self.dic[select]) for select in selSplit]
            self.masterselect.destroy()
            self.exe(newtables)

class SelectMenuBar(object):
    
    def __init__(self, root, title,dataname, listval,count, execute, mode=SINGLE):
        self.root = root
        self.title = title
        self.dataname = dataname
        self.listval = listval
        self.count = count
        
        self.mode = mode
        self.exe = execute
        
    def start(self):
        self.masterselect = Toplevel(self.root)
        master = self.masterselect
        master.wm_attributes("-topmost", 1)
        master.title(self.title)
        master.maxsize(500,500)
        master.geometry('+100+100')
        master.iconbitmap(self.root.logoPath)
    
    
        frame2 = Frame(master, height=6, bd=7, relief=SUNKEN)
        frame2.pack(fill=X, padx= 2, pady=2)
    
        frame5 = Frame(frame2, bd=7)
        frame5.pack()
        
        scrollbar = Scrollbar(frame5)
        scrollbar.pack(side=RIGHT, fill= Y)
        
        self.listbox = Listbox(frame5,height = 20, width= 400,
                          selectmode=self.mode)
        self.listbox.bind("<Double-Button-1>",  lambda x: self.execute() )

        for vals in self.listval:
            self.listbox.insert(END, vals) 
        self.listbox.insert(END, 'Reset') 
        self.listbox.pack()
        scrollbar.config(command=self.listbox.yview)
        stepButton = Button(frame5, text= 'Select Data',
                             font = 'Gill_Sans_MT -12 bold' ,
                             bg = 'dark blue', fg = 'white',
                             bd = 10, width=12,
                             command = self.execute)
        
        stepButton.pack(side=TOP, pady =5,padx=4)   
        
        
    def execute(self):
        selected = self.listbox.selection_get()
        if selected == 'Reset':
            self.reset()
        else:
            self.exe(self.dataname,self.count, selected)
        
        self.masterselect.destroy()
        
    def reset(self):
        self.root.resetSQLMenuItem(self.dataname,self.count)
        
        
class TABLES(Frame):
    def __init__(self,mainImages,  mainDB, maps,reports,srid, icons,shps, spreadsheets, Master=None,**kw):
        
        apply(Frame.__init__,(self,Master),kw)

        self.mapRepository = maps
        self.reportPath = reports
        self.logoPath = os.path.join(icons,'logo.ico')
        self.TEMPLATEdb = 'template.sqlite'
        self.mainDB =  mainDB
        self.buttonPicsPath = icons
        self.shpRepo = shps

        self.ssRepo = spreadsheets
          
        self.sysSRID = srid
        self.menubar = Menu(Master,tearoff=1)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open a Database Table", command=self.tableSelect)
        filemenu.add_command(label="Open a Database GeoTable", command=self.geotableSelect)

        filemenu.add_command(label="Review a Spreadsheet", command=self.spreadsheetPreview)
        filemenu.add_command(label="Review a Shapefile", command=self.shapefilePreview)
        filemenu.add_separator()
        filemenu.add_command(label="Create Template Shapefile", command= lambda : self.tableTemplate('shapefile') )
        filemenu.add_command(label="Create Template Spreadsheet", command=lambda :self.tableTemplate('spreadsheet'))
        filemenu.add_separator()         
        filemenu.add_command(label="Add Shapefile To Database", command=self.addShpToTable)
        filemenu.add_command(label="Add Spreadsheet To Database", command=self.addSSToTable)
        filemenu.add_separator() 
        filemenu.add_command(label='Reset Table', command=self.reset)
        filemenu.add_command(label="Exit", command=Master.destroy)
        self.menubar.add_cascade(label="Main", menu=filemenu)
        self.menubar.add_separator()
        
        editmenu = Menu(self.menubar, tearoff=0)
        self.editMode = BooleanVar()
        #editmenu.add_checkbutton(label="Turn On Full Edit Mode", onvalue=True, offvalue=False, variable=self.editMode, command=self.startEditMode)
        editmenu.add_separator()  
        editmenu.add_command(label="Drop a Table", command= self.dropTableSelect )
        editmenu.add_command(label="Drop All Data From a Table", command=self.dropTableDataSelect)
        editmenu.add_separator()          
        editmenu.add_command(label="Find and Replace Data", command=self.findAndReplaceSelect)
        self.menubar.add_cascade(label="Edit Data", menu=editmenu)
        self.menubar.add_separator()


        tableSideButtonDicOrder= ["Add Current Data to Database",
                                  "Add Shapefile To Database",
                                        "Add Spreadsheet To Database",
                                        "Add Current Data as New Table"
                                   ]

        tableSideButtonDic = {tableSideButtonDicOrder[0]:self.addCurrentData,
                               tableSideButtonDicOrder[1]:self.addShpToTable,
                               tableSideButtonDicOrder[2]:self.addSSToTable,
                               tableSideButtonDicOrder[3]:self.createTables,

                               }
        addmenu = Menu(self.menubar, tearoff=0)
        
        for desc in tableSideButtonDicOrder:
            add = tableSideButtonDic[desc]
            func = AddInit(add, desc)
            addmenu.add_command(label=func.description, command=func.execute)     
        self.menubar.add_cascade(label="Add Data To Database", menu=addmenu)  
                        
      
        
        currentSaveList = ["Save Current Data as Shapefile","Save Current Data as Spreadsheet",
                                       "Save Current Data as Database","Save Current Data as KML",
                                       ]        
        
        currentSaveListButtonDic = {currentSaveList[0]:self.exportSHPCurrent,
                               currentSaveList[1]:self.exportCSVCurrent,
                               currentSaveList[2]:self.exportDBCurrent,
                               currentSaveList[3]:self.exportKMLCurrent,
                               }
        
        tableSideExportButtonDicOrder= ["Save a Shapefile","Save a Spreadsheet",
                                       "Save a Database","Save a KML",
                                       ]

        tableSideExportButtonDic = {tableSideExportButtonDicOrder[0]:self.exportSHP,
                               tableSideExportButtonDicOrder[1]:self.exportCSV,
                               tableSideExportButtonDicOrder[2]:self.exportDB,
                               tableSideExportButtonDicOrder[3]:self.exportKML,
                               }

        exportmenu = Menu(self.menubar, tearoff=0)
        for desc in currentSaveList:
            export = currentSaveListButtonDic[desc]
            func = ExportInit(export, desc)
            exportmenu.add_command(label=func.description, command=func.execute)  
        exportmenu.add_separator()            
        for desc in tableSideExportButtonDicOrder:
            export = tableSideExportButtonDic[desc]
            func = ExportInit(export, desc)
            exportmenu.add_command(label=func.description, command=func.execute)     
        self.menubar.add_cascade(label="Save Data", menu=exportmenu)   


        mapsmenu = Menu(self.menubar, tearoff=0)
        maps = os.listdir(self.mapRepository)
        for map in maps:
            func = MapInit(map, self.mapRepository)
            mapsmenu.add_command(label=map, command=func.execute)

        self.menubar.add_cascade(label="Open Maps", menu=mapsmenu)
        self.menubar.add_separator()
        
        batchmenu = Menu(self.menubar, tearoff=0)
        batchmenu.add_command(label="Tables to Spreadsheet", command=self.batchSpreadsheetSelect)
        batchmenu.add_command(label="Tables to Shapefiles", command=self.batchShapefileSelect)
        batchmenu.add_command(label="Tables to New Database", command=self.exportDB)
        
        batchmenu.add_command(label="Copy Entire Database", command=self.exportWholeDB)

        self.menubar.add_cascade(label="Batch Processing", menu=batchmenu)
        self.menubar.add_separator()  
        
        self.menubar.add_command(label='Save Edits', command=self.saveEdits)
        #self.master.config(menu=self.menubar)        
                
        self.menubar.add_separator()  
        
        self.sqlmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Select Data',menu=self.sqlmenu)
        self.master.config(menu=self.menubar)        

        self.setmenu = Menu(self.menubar, tearoff=0)
        self.setmenu.add_command(label="Select Base Table", command=self.geotableSelect)
        
        self.setmenu.add_command(label="Select Search Table",command=self.searchTableSelect )
        self.setmenu.add_command(label="Search Buffer = 100", command=self.setSearchBuffer)

        self.menubar.add_cascade(label="Spatial Search", menu=self.setmenu)

        self.joinmenu = Menu(self.menubar, tearoff=0)
        self.joinmenu.add_command(label="Select Join From Table", command=self.tableSelect)
        
        self.joinmenu.add_command(label="Select Join To Table",command=self.tableSelect )
        self.joinmenu.add_command(label="Select Conditions", command=self.setSearchBuffer)

        self.menubar.add_cascade(label="Join Tables", menu=self.joinmenu)



        self.BaseFrame = Frame(self)
        self.BaseFrame.grid(row=0, column=0, padx = 1, pady=1)
        #self.SideFrame = Frame(self)
        #self.SideFrame.grid(row=0, column=1, padx = 1, pady=1)

        #self.ButtonFrame2 = Frame(self)
        #self.ButtonFrame2.grid(row=1, column=0, padx = 1, pady=1)
        self.initiate()
        
    def initiate(self):
        self.toolTipManager = ToolTipManager()
        
        self.tableModeDataDic = {}
        self.sqlconditionals = []
        self.colors = COLORS 
        self.backgroundcolor = 'light gray'
        self.buttonColor = 'cadet blue'
        self.batchIndicator = 0
        self.searchIndicator = 0
        self.searchBufferVal = '100'
        
        self.loadMode = 1
        self.font = "Times"
        self.fontSize = 9
        self.tableSelected = 0
        self.testMode = 0
        self.wInfo = ScreenManager(self)
        self.dataXlimit = 50
        self.dataYlimit = 50
        self.abcs = map(chr, range(65, 91))
        self.mapHeightSpacer = 100
        self.mapWidthSpacer = 100
        self.findAndReplaceMode = 0
        self.curspatial()   
        self.TableMode()
        self.bindings()
        #self.generateGRID()  
        self.searchBaseTable = ''
        self.searchSearchTable = ''
        self.fieldTypes = { 'DOUBLE':'D',
                           'FLOAT':'F',
                           'INTEGER': 'N',
                           'BIGINT':'L',
                           'TEXT':'C',
                           'POLYGON':5,
                          'POINT':1,
                          'LINESTRING':3,
        
        
                           }

        
        self.allTypesDic = {'BOOL':'TEXT', "DATE":"DOUBLE",  'REAL':"FLOAT", 'DOUBLE':'FLOAT'}
        for key in self.fieldTypes:
            self.allTypesDic[key] = key
        

    def bindings(self):
        'bind the map to clicks and motion'
        
        self.imageMapWindow.canvas.bind("<ButtonRelease-1>", self.onRelease)

    def onDrag(self, start, end):

        self.startcoords = start
        self.endcoords= end

    def onRelease(self,event):

        self.imageMapWindowRect.stopRect()

        start = self.startcoords
        end = self.endcoords
        if start != [0,0] and end != [0,0]:
            self.turnoffClick = 1
            xscale = abs(self.imageMapWindow.widthmap/(start[0] - end[0]))
            
            if self.imageMapWindow.widthmap>self.imageMapWindow.heightmap:
                yscale = xscale * (self.imageMapWindow.heightmap/float(self.imageMapWindow.widthmap))
            else:
                yscale = xscale * (self.imageMapWindow.widthmap/float(self.imageMapWindow.heightmap))
    
            if start[0]< end[0]:
                xorigin = start[0] + (abs(start[0]-end[0])/2.0)
            else:
                xorigin = end[0] + (abs(start[0]-end[0])/2.0)
            if start[1] > end[1]:
                yorigin = end[1] + (abs(start[1]-end[1])/2.0)
            else:
                yorigin = start[1] + (abs(start[1]-end[1])/2)
    
            self.imageMapWindow.canvas.scale('all',xorigin ,yorigin, 
                                             xscale,yscale)
            self.startcoords =[0,0]
            self.endcoords = [0,0]
                    

    
    def mapReset(self): 
        self.mapBaseOutlineColor =  'dark blue' #self.colors[self.randcolor()]
        self.mapBaseFillColor = 'tan' #self.colors[self.randcolor()]   
        self.mapSearchOutlineColor = 'black'
        self.mapSearchFillColor = 'dark green'
        self.mapCoordMaxX =  0
        self.mapCoordMaxY =  0
        self.mapCoordMinX = 1000000000 
        self.mapCoordMinY = 1000000000 
        self.mapWidthSpacer = 100
        self.mapHeightSpacer = 100
        #self.mapBaseGenerator()
        #self.loadMap() 
        #self.mapSearchGenerator( ['CCWD_Fences'])
        
        #self.loadMap() 
        
    def curspatial(self):
        from pysqlite2 import dbapi2 as sql
        self.sql_connection = sql.Connection(self.mainDB)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
        self.cursorspatial = sql.Cursor(self.sql_connection)
        self.sql_connection.enable_load_extension(1)
        self.sql_connection.load_extension('libspatialite-2.dll') 
        self.resourceGeoDic = self.selectMetaGeoTables()
        self.resourceDic = self.selectMetaTables()
 
    def TableMode(self):
        self.tableModeFrameMain = Frame(self.BaseFrame,bg=self.backgroundcolor, relief=SUNKEN, bd=2)
        self.tableModeFrameMain.grid(row=0,column=0)


        self.buttonWidth = self.wInfo.imagethumbcanvasWidth/4.4
        self.buttonHeight = self.buttonWidth/1.3

        self.tableHolderFrame= Frame(self.tableModeFrameMain )
        self.tableHolderFrame.grid(row=0,column=1, sticky=W+E+N+S)        

        self.sideImageFrame = Frame(self.tableModeFrameMain,bg=self.backgroundcolor)
        self.sideImageFrame.grid( row=0,column=2,  sticky= E+W+N+S)

        self.imageMapFrame = Frame(self.sideImageFrame,bg=self.backgroundcolor)
        self.imageMapFrame.grid(row=0,column=0, sticky= E+W+N+S)        
        self.imageMapWindow = MapImages(self.imageMapFrame,self.wInfo.mapcanvasWidth, self.wInfo.mapcanvasWidth )
        self.imageMapWindow.canvas.grid(row=0,column=0,sticky= E+W+N+S )
 #         

        self.imageDataFrame = Frame(self.sideImageFrame,bg=self.backgroundcolor)
        self.imageDataFrame.grid(row=1,column=0, sticky= E+W+N+S)        
        self.imageDataWindow = MapImages(self.imageDataFrame,self.wInfo.mapcanvasWidth, self.wInfo.mapcanvasWidth/8.0 )
        self.imageDataWindow.canvas.grid(row=0,column=0,sticky= E+W+N+S )

        self.imageGraphFrame = Frame(self.sideImageFrame,bg=self.backgroundcolor)
        self.imageGraphFrame.grid(row=2,column=0, sticky= E+W+N+S)        
        self.imageGraphWindow = MapImages(self.imageGraphFrame,self.wInfo.mapcanvasWidth, self.wInfo.mapcanvasWidth )
        self.imageGraphWindow.canvas.grid(row=0,column=0,sticky= E+W+N+S )
 #         
        self.imageMapWindowRect = RectTracker(self.imageMapWindow.canvas)
        self.imageMapWindowRect.autodraw(fill="", width=2, command=self.onDrag)
        
        
        tableModel = TableModel(rows=self.dataYlimit,columns=self.dataXlimit)
        self.table = TableCanvas(self.tableHolderFrame, model = tableModel, width=self.wInfo.tableCanvasWidth/1.5, height =self.wInfo.tableCanvasHeight  )
        self.table.createTableFrame()
        
        
        width1 = self.buttonWidth
        height1 = self.buttonHeight 
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'MagnifyPlus.gif'))
        self.mapButtonPlus =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.ButtonZoomIn)
        self.mapButtonPlus.image = photo
        #self.imageButtonPrint.grid(row=0, column=6)
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'MagnifyMinus.gif'))
        self.mapButtonMinus =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.ButtonZoomOut)
        self.mapButtonMinus.image = photo       

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Right.gif'))
        self.mapButtonNext =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.ButtonPanRight)
        self.mapButtonNext.image = photo
        
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Left.gif'))
        self.mapButtonBack =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.ButtonPanLeft)
        self.mapButtonBack.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Up.gif'))
        self.mapButtonUp =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.ButtonPanUp)
        self.mapButtonUp.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Down.gif'))
        self.mapButtonDown = Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.ButtonPanDown)
        self.mapButtonDown.image = photo

        
        mapwindowbuttonsdic = {self.mapButtonPlus:'Zoom In',
                            self.mapButtonMinus:'Zoom Out',
                            self.mapButtonBack:'Move Left',
                            self.mapButtonNext:'Move Right', 
                            self.mapButtonDown:'Move Down',
                            self.mapButtonUp:'Move Up'} 
        mapwindowbuttons = [self.mapButtonPlus, self.mapButtonMinus, self.mapButtonBack,self.mapButtonNext,self.mapButtonDown, self.mapButtonUp  ]
        for COUNTER, button in enumerate(mapwindowbuttons):
            self.imageDataWindow.canvas.create_window((width1 * COUNTER) + (15), 5 ,window=button,anchor="nw")
 


        
    def ButtonZoomIn(self):
        xscale = 2
        
        if self.imageMapWindow.widthmap>self.imageMapWindow.heightmap:
            yscale = xscale * (self.imageMapWindow.heightmap/float(self.imageMapWindow.widthmap))
        else:
            yscale = xscale * (self.imageMapWindow.widthmap/float(self.imageMapWindow.heightmap))
            
        self.imageMapWindow.canvas.scale('all',self.imageMapWindow.widthmap/2,self.imageMapWindow.heightmap/2, 
                                         xscale,yscale
                                        )        
        
    def ButtonZoomOut(self):
        xscale = .5
        
        if self.imageMapWindow.widthmap>self.imageMapWindow.heightmap:
            yscale = xscale * (self.imageMapWindow.heightmap/float(self.imageMapWindow.widthmap))
        else:
            yscale = xscale * (self.imageMapWindow.widthmap/float(self.imageMapWindow.heightmap))
            
        self.imageMapWindow.canvas.scale('all',self.imageMapWindow.widthmap/2,self.imageMapWindow.heightmap/2, 
                                         xscale,yscale
                                        )           

    def ButtonPanUp(self):

                self.imageMapWindow.canvas.move('all',0, self.mapHeightSpacer/5 )

    def ButtonPanDown(self):

                self.imageMapWindow.canvas.move('all',0, -self.mapHeightSpacer/5 )

             
    def ButtonPanLeft(self):

            self.imageMapWindow.canvas.move('all', self.mapWidthSpacer/5,0 )
        

    def ButtonPanRight(self):

            self.imageMapWindow.canvas.move('all', -self.mapWidthSpacer/5,0 )

    def setSearchBuffer(self):
        self.searchBufferVal = tkSimpleDialog.askstring('Set Buffer Distance', 'Enter Buffer Distance In Meters: ')
        self.setmenu.entryconfig(2, label= 'Search Buffer = {0}'.format(self.searchBufferVal))
    
    def searchTableSelect(self):
        self.geoTablesMenu = SelectMenu(self,self.selectMetaGeoTables(), self.loadSearchTable, 'Select a Geo Table')
        
            
    
    def reviewSQLgenerator(self):
        self.searchIndicator = 1
        buffer = self.searchBufferVal

        basetable = self.searchBaseTable
        table = self.searchSearchTable
        
        if table != '':
            tablesql = "{0}.ID IN (SELECT DISTINCT ROWID FROM SpatialIndex WHERE f_table_name = '{0}' AND search_frame = buffer({1}.Geometry,{2})) ".format(basetable,table, buffer)
        else:
            tablesql = ''
        self.searchSQL = tablesql

    def reset(self):
        self.dataXlimit = 50
        self.dataYlimit = 50
        self.generateSS()
        self.mapReset()
            
    def switchMainDBs(self):
        pass

    def generateSS(self):
        self.tableSelected = 0
        self.selectedTable = ''
        self.table.destroy()
      
        tableModel = TableModel(rows=self.dataYlimit,columns=self.dataXlimit)
        self.table = TableCanvas(self.tableHolderFrame, model = tableModel, width=self.wInfo.tableCanvasWidth/1.5, height =self.wInfo.tableCanvasHeight  )
        self.table.createTableFrame()
 
    def tableTemplate(self,type):
        if type == 'shapefile':
            table = self.selectMetaGeoTables()
            
        elif type == 'spreadsheet':
            table = self.selectMetaTables()
        self.templateType = type
        execute  = self.loadTemplate
        title = 'Select a Table to Template' 
        templateSelectMenu = SelectMenu(self,table, execute,title)
        
 
    def loadTemplate(self,table):
        'load the column headers of the selected table and save a template file'
        self.selectedTable = table

        self.columns = self.tableInfo(table)
        self.dataXlimit = len(self.columns)

        self.loadedTableDic = {}
        
        for COUNTER,column in enumerate(self.columns):
            self.loadedTableDic[column] = []

        if self.batchIndicator == 0:
            self.loadValsNew()

        if tkMessageBox.askyesno('Save Template', 'Would you like to save this template?'):
            if self.templateType == 'shapefile':
                shp = saveSHP(self)
                if len(shp)> 0:
                    shpWriter = Writer()
                    shpWriter.autoBalance = 1        
                    for COUNTER, column in enumerate(self.columns):
                        headerval = str(column[1])
                        typeval = self.fieldTypes[self.allTypesDic[column[2].upper()]]
                        
                        if headerval == 'Geometry':
    
                            geomtype = self.fieldTypes[column[2]]
                        else:
                            if typeval == 'M' or typeval== 'C':
                                shpWriter.field(headerval, typeval, '255')
                            elif typeval == 'N' or typeval == 'L':
                                shpWriter.field(headerval, typeval)
                            else:
                                shpWriter.field(headerval, typeval)
                    shpWriter.shapeType = geomtype
                    shpWriter.null()
                    shpWriter.save(target=shp)
                    #
                    #shpWriter.saveDbf(shp)
                    #shpWriter.saveShx(shp)
                    #shpWriter.saveShp(shp)
                    tkMessageBox.showinfo('File Save', 'Your shapefile was saved at: %s' % shp)
            else:
                spst = saveCSV(self)
                self.retrievedData = []
                self.makeSpreadSheet(spst)
        return
    #def spreadsheetSelect(self):
        #selectMenu = SelectMenu(self,self.selectMetaTables,self.exportSpreadsheet, 'Select a Table')


    def tableSelect(self):
        self.TablesMenu = SelectMenu(self,self.selectMetaTables(), self.loadTable, 'Select a Table')


    def geotableSelect(self):
        'create select menu with geo tables'
        self.geoTablesMenu = SelectMenu(self,self.selectMetaGeoTables(), self.loadTable, 'Select a Geo Table')


    def geoTabletableSelect(self):
        'create select menu with geo tables'
        self.geoTablesMenu = SelectMenu(self,self.selectMetaGeoTables(), self.loadGeoTable, 'Select a Geo Table')



    def selectMetaGeoTables(self):

        sql = 'SELECT f_table_name FROM  geometry_columns'
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()

        dic= {}
        for result in results:
            dic[result[0].replace('CCWD_','').title()] = result[0]
#            dic[result[0]]= result[0].replace('CCWD_','').title()
        return dic

    def selectMetaTables(self):
        sql = "SELECT Name FROM  sqlite_master WHERE type='table' and name LIKE 'CCWD%'"
        
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()
        dic= {}
        for result in results:
            dic[result[0].replace('CCWD_','').title()] = result[0]
            #dic[result[0]]= result[0].replace('CCWD_','').title()
        return dic    
    
    def selectMetaPhotoTables(self):
        sql = "SELECT Name FROM  sqlite_master WHERE type='table' and name LIKE '%photos'"
        
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()
        dic= {}
        for result in results:
            dic[result[0].replace('CCWD_','').title()] = result[0]
            #dic[result[0]]= result[0].replace('CCWD_','').title()
        return dic    
        
    def loadTable(self, table):
        
        self.searchIndicator = 0
        self.selectedTable =  table
        self.tableSelected = 1
        self.selectSQL()
        self.mapReset()
        if table in self.selectMetaGeoTables().values():
            self.setmenu.entryconfig(0, label= 'Base Table = ' + table)
            self.setmenu.entryconfig(1, label= 'Set Search Table')
            self.searchBaseTable  = table
            self.mapBaseGenerator()
            self.loadMap()
            
    def loadSearchTable(self, table):
        
        
        #self.selectedTable =  table
        #self.tableSelected = 1
        #self.selectSQL()
        
        self.mapReset()
        self.searchSearchTable  = table 
        self.reviewSQLgenerator()
        if table in self.selectMetaGeoTables().values():
            self.setmenu.entryconfig(1, label= 'Search Table = ' + table)
            self.sqlSelectGenerator()
            self.mapBaseGenerator()
            self.loadMap()            

                       
            self.mapSearchGenerator()
            self.loadSearchLayer()
            
            
            
    def exportSpreadsheet(self, table):
        'select spreadsheet to load to table selected'
        
        self.selectedTable = table
        self.tableSelected = 1
        #self.masterselect.destroy()
        csvname = saveCSV(self)
        self.selectSQL()
        if csvname.find('csv') != -1:
            self.makeCSV(csvname)
        elif  csvname.find('xls') != -1:
            self.makeSpreadSheet(csvname)
        tkMessageBox.showinfo('File Save', 'Your file has saved at: %s' % csvname)
        return


    def loadGeoTable(self, table):
        'export a geo table to shape or KML'
        
        self.selectedTable = table
        #self.masterselect.destroy()
        
        if self.exportType == 'SHP':
            self.makeSHP()
        elif self.exportType == 'KML':
            self.makeKML()
        elif self.exportType == 'KMLcurrent':
            self.makeKMLcurrent()        
        elif self.exportType == 'SHPcurrent':
            self.makeSHPcurrent()
            
    def selectSQL(self):
            'select row data and header data for the selected table'
            
            self.columns = self.tableInfo(self.selectedTable)
            self.dataXlimit = len(self.columns)

            if self.selectedTable in self.selectMetaGeoTables().values():
                fields = ''
                for COUNTER,column in enumerate(self.columns):
                    field = column[1]
                    if field == 'Geometry':
                        field = 'AsText(Geometry)'
                    if COUNTER != (len(self.columns)-1):
                        
                        fields += field + ','
                    else:
                        fields += field 
                sql = "SELECT {0} FROM {1}".format(fields,self.selectedTable)
            else:
                sql = "SELECT * FROM {0}".format(self.selectedTable)    
            self.currentSQL = sql       
            self.cursorspatial.execute(self.currentSQL)
            self.retrievedData = self.cursorspatial.fetchall()

            self.loadedTableDic = {}
            
            for COUNTER,column in enumerate(self.columns):
                self.loadedTableDic[column] = []
                for values in self.retrievedData:
                    for COUNT, value in enumerate(values):
                        if COUNTER == COUNT:
                            self.loadedTableDic[column].append(value)
            if self.batchIndicator == 0:
                self.loadValsNew()
                #self.mapBaseGenerator()
                self.sqlMenuGenerate(self.table.data)
            return
        
    def sqlSelectGenerator(self):
    
        if self.selectedTable in self.selectMetaGeoTables().values():
            fields = ''
            for COUNTER,column in enumerate(self.columns):
                field = self.selectedTable+ '.'+column[1]
                if column[1] == 'Geometry':
                    field = 'AsText('+self.selectedTable+ '.'+'Geometry)'
                if COUNTER != (len(self.columns)-1):
                    
                    fields +=  field + ','
                else:
                    fields += field 
            sql = "SELECT {0} FROM {1}".format(fields,self.selectedTable)
        else:
            sql = "SELECT * FROM {0}".format(self.selectedTable)   
        
        if self.searchIndicator !=0:
            sql += ','+ self.searchSearchTable  
        wheresql = " WHERE "      
        
        for COUNT, condition in enumerate(self.sqlconditionals):
            if COUNT != len(self.sqlconditionals)-1:
                wheresql += condition + ' AND '
            else:
                wheresql += condition
        
        if wheresql != " WHERE ":
            sql += wheresql
        if self.searchIndicator != 0:
            if wheresql != " WHERE ":
                sql += " AND " + self.searchSQL
            else:
                sql += " WHERE " + self.searchSQL
        self.currentSQL = sql
        self.cursorspatial.execute(self.currentSQL)
        self.retrievedData = self.cursorspatial.fetchall()

        self.loadedTableDic = {}
        
        for COUNTER,column in enumerate(self.columns):
            self.loadedTableDic[column] = []
            for values in self.retrievedData:
                for COUNT, value in enumerate(values):
                    if COUNTER == COUNT:
                        self.loadedTableDic[column].append(value)
        if self.batchIndicator ==0:
            self.loadValsNew()
            #self.mapBaseGenerator()        

    def getDistinctValues(self,column):
        values = self.loadedTableDic[column]
        valist = []
        for value in values:
            if value not in valist:
                valist.append(value)
        return valist

    def resetSQLMenuItem(self,dataname,count):
        newvalue = dataname 
        self.sqlmenu.entryconfig(count,label= newvalue)
        for COUNT, sql in enumerate(self.sqlconditionals):
            splitsql = sql.split(' = ')
            if newvalue in splitsql:
                self.sqlconditionals.pop(COUNT)
        self.sqlSelectGenerator()

    def adjustSQLMenuItem(self,dataname,count, selected):
        newvalue = dataname + ' = ' + selected
        #selector = SelectMenuBar(self,'Select Data Value From {0}'.format(dataname), dataname, data,count,self.adjustSQLMenuItem)
        self.sqlmenu.entryconfig(count,label= newvalue)
        sqlvalue = dataname+" = "+ '"'+selected+'" '
        if sqlvalue not in self.sqlconditionals:
            self.sqlconditionals.append(sqlvalue)
        self.sqlSelectGenerator()
        
    def sqlMenuGenerate(self,data):
        #if self.menuRegenerate == 0:
            self.menuRegenerate = 1
            self.sqlmenu.delete(0, END)
            self.sqlconditionals = []
            self.columns = self.tableInfo(self.selectedTable)

            for COUNTER,column in enumerate(self.columns):
                data = self.getDistinctValues(column)
                dataname = column[1]
                if dataname != 'Date':
                    selector = SelectMenuBar(self,'Select Data Value From {0}'.format(dataname), dataname, data,COUNTER,self.adjustSQLMenuItem)
                    self.sqlmenu.add_command(label=dataname,command = selector.start)
                else:
                    self.dateMenuEntry = COUNTER
                    self.sqlmenu.add_command(label=dataname ,command = self.setDates)
                    
    def setDates(self):
        'select dates for SQL search'
        self.setStartDate()
        self.setEndDate()
        datebetween = ' Date Between {0} AND {1} '.format(self.selectDateFrom, self.selectDateTo)
        self.sqlmenu.entryconfig(self.dateMenuEntry, label=datebetween)
        for COUNT,cons in enumerate(self.sqlconditionals):
            if cons.find('Date') != -1:
                self.sqlconditionals.pop(COUNT)
        self.sqlconditionals.append(datebetween)
        
    def setStartDate(self):
        'select calendar date'
        frame = Toplevel()
        frame.wm_iconbitmap(self.logoPath)
        def setFrom(f):
            self.selectDateFrom = f

            frame.destroy()

        c = calendarTk(master=frame, date="2008/01/01",dateformat="%Y/%m/%d",command=setFrom)
        c.grid(row=0,column=0)
        
            
    def setEndDate(self):
        frame = Toplevel()
        frame.wm_iconbitmap(self.logoPath)

        def setFrom(f):
            self.selectDateTo = f
            
            frame.destroy()

        c = calendarTk(master=frame, date=self.selectDateTo,dateformat="%Y/%m/%d",command=setFrom)
        c.grid(row=0,column=0)

 
    def parseData(self):
        'convert datatable data into table matrix data'
        dataDic = {}
        if len(self.loadedTableDic[self.columns[0]]) > 0:
            self.valueRange = len(self.loadedTableDic[self.columns[0]])
        else:
            self.valueRange =0
        for i in range(1,self.valueRange+1):
            dataDic[str(i)] = {}
        for COUNTERX, columns in enumerate(self.columns):
            if type(columns) == type('a') or type(columns) == type(u'a'):
                header = columns
            else: 
                header = columns[1]
            values = self.loadedTableDic[columns]
            if len(values)> 0:
                for COUNTERY, value in enumerate(values):
                    dataDic[str(COUNTERY+1)][header] = value 
            else:
                if dataDic == {}:
                    dataDic[str(0)] = {}
                dataDic[str(0)][header] = '' 
        return dataDic
    
    def loadValsNew(self):
        'parse into a dictionary that is loaded into a TableCanvas'
        
        self.table.paging_OffAlways()
        data = self.parseData()
        if self.selectedTable not in self.selectMetaGeoTables().values():
            totaldatalen = 0
            for val in data[data.keys()[0]].values():
                if val != None:
                    totaldatalen+=len(str(val)) 
    
            if len(data.keys()) > 0 and  totaldatalen != 0:
                maxval = int(max(data.keys()))+1
                keys = data[data.keys()[0]].keys()
                data[str(maxval)] = {}
                [data[str(maxval)].update({key: ''})for key in keys]
            
        self.tableSelected = 1
        if self.findAndReplaceMode ==0:
            self.preEditsCopyDataDic = data
        from tkintertable.Tables import TableCanvas
        from tkintertable.TableModels import TableModel
        self.table.destroy()
        self.table = TableCanvas(self.tableHolderFrame, newdict=data)
        self.table.createTableFrame()
        try:
            self.table.sortTable( self.table.model.getColumnIndex( 'id'), )
        except:
            pass

        self.table.redrawTable()
        
        return

    
    def reloadVals(self,data):
        'parse into a dictionary that is loaded into a TableCanvas'
        from tkintertable.Tables import TableCanvas
        from tkintertable.TableModels import TableModel
        self.table.destroy()
        if self.findAndReplaceMode == 0:
            self.preEditsCopyDataDic = data
        self.table = TableCanvas(self.tableHolderFrame, newdict=data)
        self.table.createTableFrame()
        try:
            self.table.sortTable( self.table.model.getColumnIndex( 'id'), )
        except:
            pass

        self.table.redrawTable()
        return
    
    def exportCSV(self):
        
        selectMenu = SelectMenu(self,self.selectMetaTables(),self.exportSpreadsheet, 'Select a Table')
        

    def exportCSVCurrent(self):
        
        try:
            self.exportSpreadsheet(self.selectedTable)
        except AttributeError:
            tkMessageBox.showwarning('Data Issue', 'No Data Loaded')
    
    
    def makeCSV(self,csvname):        
        csvsplit = csvname.split('.')
        csvname = csvsplit[0] + '.csv'
        header = ''
        geomval = -1
        for COUNTER, column in enumerate(self.columns):
            headerval = column[1]
            if COUNTER != len(self.columns)-1:
                header += headerval + ','
            else:
                header += headerval +'\n'
                
            if headerval == 'Geometry':
                geomval = COUNTER
       
        csv = open(csvname,'w')
        csv.write(header)
        for data in self.retrievedData:
            datarow = ''
            for COUNTER, val in enumerate(data):
                if COUNTER != geomval:
                    dataval = str(val).replace(',',' ')
                else:
                    dataval = '<Spatial Data>'
                if COUNTER != len(data)-1:
                    datarow += dataval + ','
                else:
                    datarow += dataval +'\n'
            csv.write(datarow)
        csv.close()
        
    def batchSpreadsheetSelect(self):
        'select a table to export to '
        batchSelectMenu = SelectMenu(self,self.selectMetaTables(),self.batchXLS,'Select Tables To Export',mode=EXTENDED) 


        
    def batchXLS(self, selected):
        'export selected tables to spreadsheet in batch mode'
        self.batchIndicator = 1

        datestring = dateStringYMD(4)
        foldername = os.path.join(createFolder(self), datestring)
        if not os.path.exists(foldername): os.mkdir(foldername)
        
        for COUNTER, table in enumerate(selected):
            self.selectedTable = table
            self.tableSelected = 1
            csvname = os.path.join(foldername, table+ '.xls')
            self.selectSQL()
            if csvname.find('csv') != -1:
                self.makeCSV(csvname)
            elif  csvname.find('xls') != -1:
                self.makeSpreadSheet(csvname)
        self.batchIndicator = 0
        tkMessageBox.showinfo('File Save', 'Your batch files have been saved at: %s' % foldername)
        
    def batchShapefileSelect(self):
        'select a table to export to shapefile'
        batchSelectMenu = SelectMenu(self,self.selectMetaTables(),self.batchSHP,'Select Tables To Export',mode=EXTENDED) 

                        
    def batchSHP(self, selected):
        'batch export of shapefiles from tables'
        self.batchIndicator = 1

        datestring = dateStringYMD(4)
        foldername = os.path.join(createFolder(self), datestring + '_shps')
        if not os.path.exists(foldername): os.mkdir(foldername)

        for COUNTER, table in enumerate(selected):
            self.selectedTable = table
            self.tableSelected = 1
            shpname = os.path.join(foldername, table.replace(' ','_')+ '.shp')
            self.makeSHP(shpname)

        self.batchIndicator = 0
        tkMessageBox.showinfo('File Save', 'Your batch files have been saved at: %s' % foldername)
        
    def makeSpreadSheet(self,ssname):        
        'convert a table into a spreadsheet'
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet1')
        headerFont = xlwt.Font() # Create the Font
        headerFont.name = 'Times New Roman'
        headerFont.bold = True
        headerFont.italic = True  
        headerStyle = xlwt.XFStyle()
        headerStyle.font = headerFont


        dataFont = xlwt.Font() 
        dataFont.name = 'Times New Roman'
        dataStyle = xlwt.XFStyle()
        dataStyle.font = dataFont
                        
        
        for COUNTER, header in enumerate(self.columns):
            worksheet.write(0, COUNTER, label = header[1], style = headerStyle)

        for COUNTER, data in enumerate(self.retrievedData):
            for ROWCOUNT, value in enumerate(data):
                
                worksheet.write( COUNTER+1, ROWCOUNT, label = value, style =dataStyle)
        workbook.save(ssname)
        if self.batchIndicator ==0:
            tkMessageBox.showinfo('File Save', 'Your spreadsheet has been saved at: %s' % ssname)



    def exportSHP(self):
        self.insertLB('export shapefile')
        self.exportType = 'SHP'
        self.geoTabletableSelect()

    def exportSHPCurrent(self):
        self.insertLB('export shapefile')
        self.exportType = 'SHPcurrent'
        self.loadGeoTable(self.selectedTable)        

    def exportKMLCurrent(self):
        self.insertLB('export shapefile')
        self.exportType = 'KMLcurrent'
        self.loadGeoTable(self.selectedTable)        

    def insertLB(self, msg):
        pass

    def startEditMode(self):
        if self.tableSelected == 1:
            val = self.editMode.get()
            if val == 1:
                self.editBind = self.table.bind('<Enter>', self.saveEditsProxy)
            else:
                self.table.unbind('<Enter>', self.editBind ) 
        else:
            tkMessageBox.showwarning('No Data Selected', 'You have not selected a table yet')    
            
    def saveEditsProxy(self,event):
        self.saveEdits()
        
    def saveEdits(self):

        alterSQL = "ALTER TABLE {0} ADD COLUMN {1} {2}"
        updateSQL = "UPDATE {0} SET {1}='{2}' WHERE {3}={4}"
        insertSQL = "INSERT INTO {0}({1}) VALUES ({2})"
        headers = self.tableInfo(self.selectedTable)

        data = self.table.model.data

        updates = []
        keys = data.keys()
        keys.sort()
        insertdatacollector = []
        if int(keys[0]) != 0:
            for i in range(int(keys[0]),len(self.preEditsCopyDataDic)+1):
                i= str(i)
                rowI = self.preEditsCopyDataDic[i]
                insertdata = []
                for key in rowI:
                    value = self.preEditsCopyDataDic[i][key]
                    if value != '' and data[i][key] != '':
                        for newkey in data[i].keys():
                            if key == newkey:
                                
                                if value != data[i][key] and str(value) != data[i][key]:
                                    sql = updateSQL.format(self.selectedTable, key, data[i][key], 'id', data[i]['id'])
                                    updates.append(sql)
                    elif value == '' and data[i][key] != '':
                        keyvalpair = (key,data[i][key] )
                        insertdata.append(keyvalpair)
                if insertdata != []:
                    insertdatacollector.append(insertdata)
        else:
            values = data[keys[0]].values()
            headstring =''
            valheads = []
            for count, header in enumerate(headers):
                if header[1].lower() != 'id': 
                    headstring+="'"+ header[1]+"'"
                    if count != len(headers)-1:
                        headstring+=','
                    valheads.append(header[1])
            valstring = ''
            for count, head in enumerate(valheads):
                value = data[keys[0]][head]
                if type(value) == type('a') or value == type(u'a'):
                    valstring+="'"+ value+"'"
                else:
                    valstring+= value
                if count != len(valheads)-1:
                    valstring+=','  
            insertstring = insertSQL.format(self.selectedTable, headstring, valstring)
            updates.append(insertstring) 
        
        for insertdata in insertdatacollector:
                
            insertheader =''
            insertvals = ''
            for count,keyvalpairs in enumerate(insertdata):
                insertheader+=keyvalpairs[0]
                value = keyvalpairs[1]
                if type(value) == type('a') or value == type(u'a'):
                    insertvals+="'"+ value+"'"
                else:
                    insertvals+= value
                if count != len(insertdata)-1:
                    insertheader+=','
                    insertvals+=','
            sql = insertSQL.format(self.selectedTable, insertheader, insertvals)
            updates.append(sql)
                     
        if self.editMode.get() == 0:
            if tkMessageBox.askyesno('Final Assurance', 'Are you sure you want to save your edits?'):
                for sql in updates:
                    self.cursorspatial.execute(sql)
                self.sql_connection.commit()
                tkMessageBox.showinfo('Data Updated', 'The data in {0} has been updated'.format(self.selectedTable))
        else:
                for sql in updates:
                    self.cursorspatial.execute(sql)
                self.sql_connection.commit() 
        self.selectSQL() 
                        
    def findAndReplaceSelect(self):
        'find and replace menu list button'
        try:
            self.findAndReplaceTable(self.selectedTable)
        except:
            tkMessageBox.showwarning('No Table Selected', 'Please select a table first')
            
    def findAndReplaceTable(self, table):
        'find and replace supplied values for supplied datatable'
        self.preEditsCopyDataDic = self.table.model.data
        column = self.table.get_currentColName()
        findval = tkSimpleDialog.askstring('Find Value', 'Which value to look for?')
        replaceval = tkSimpleDialog.askstring('Replacement Value', 'Which value to replace it?')
        datadic = self.findAndReplace(self.preEditsCopyDataDic , column, findval, replaceval)
        self.saveEdits()
        self.findAndReplaceMode = 1
        self.reloadVals(datadic)
        self.findAndReplaceMode = 0
        
        #self.reloadVals(datadic)
        
    def findAndReplace(self,datadic, column, findval,replaceval):
        'search through data dictionary to find and replace values'
        #self.preEditsCopyDataDic = datadic

        for i in range(len(datadic)):
            for keys in datadic[str(i+1)]:
                if keys == column:
                        value = datadic[str(i+1)][keys]
                        if value.find(findval) != -1:
                            newval = value.replace(findval,replaceval)

                            
                            datadic[str(i+1)][keys] = newval
        return datadic
                        

    def tableInfo(self,table):
        'get table info (names and types of columns) for supplied table'
        columns = "PRAGMA table_info({0})".format(table)
        self.cursorspatial.execute(columns)
        recolumns = self.cursorspatial.fetchall()                
        return recolumns
    
    def makeSHP(self, shpname= None):
        'make a shapefile from selected geo data'
        self.geocolumns = self.tableInfo(self.selectedTable)
        self.dataXlimit = len(self.geocolumns)
 

        self.batchIndicator = 1
        self.sqlSelect()
        self.batchIndicator = 0
        sql = self.currentSQL
        self.cursorspatial.execute(sql)
        self.retrievedGeoData = self.cursorspatial.fetchall()
        header = ''
        geomval = -1
        if shpname == None:
            shpname = saveSHP(self)
        shpWriter = Writer()
        shpWriter.autoBalance = 1        
        for COUNTER, column in enumerate(self.geocolumns):
            headerval = str(column[1])
            typeval = self.fieldTypes[self.allTypesDic[column[2].upper()]]
            
            if headerval == 'Geometry':
                geomval = column[2]
                geomtype = self.fieldTypes[column[2]]
            else:
                if typeval == 'M' or typeval== 'C':
                    shpWriter.field(headerval, typeval, '255')
                elif typeval == 'N' or typeval == 'L':
                    shpWriter.field(headerval, typeval)
                else:
                    shpWriter.field(headerval, typeval)
        shpWriter.shapeType = geomtype
        parsedGeometryList = []
        [parsedGeometryList.append(self.parseGeo(data[-1])) for data in self.retrievedGeoData]
        if geomtype == 5or geomtype == 3:
            [shpWriter.poly(shapeType= geomtype,parts=parsedGeometry) for parsedGeometry in parsedGeometryList]
        elif geomtype == 1:
            [shpWriter.point(*parsedGeometry) for parsedGeometry in parsedGeometryList]
        dataLists = []
        for  data in self.retrievedGeoData:
            dList = list(data[:-1])
            for COUNTER,val in enumerate(dList):
                typeval = self.fieldTypes[self.allTypesDic[self.geocolumns[COUNTER][2].upper()]]
                if typeval == 'M' or typeval== 'C':
                    dList[COUNTER] = str(val)
                elif typeval == 'F':
                    dList[COUNTER] = float(val)
                elif typeval == 'N':
                    dList[COUNTER] = int(val)
                elif typeval =='D':
                    dList[COUNTER] = float(val)
            dataLists.append(dList)
        [shpWriter.record(*dList) for dList in dataLists]

        shpWriter.save(shpname) 
        prj = generatePRJ()
        prjfile = shpname.replace('.shp','') + '.prj' 
        prjfileOpen = open(prjfile, 'w')
        prjfileOpen.write(prj)
        prjfileOpen.close()
        self.insertLB('shapefile saved')
        self.insertLB(shpname)
        if self.batchIndicator ==0:
            tkMessageBox.showinfo('File Save', 'Your file has been saved at: %s' % shpname)
        
    def makeSHPcurrent(self, shpname= None):
        'make a shapefile from selected geo data'
        self.geocolumns = self.tableInfo(self.selectedTable)
        self.dataXlimit = len(self.geocolumns)
 

        sql = self.currentSQL

        self.cursorspatial.execute(sql)
        self.retrievedGeoData = self.cursorspatial.fetchall()
        header = ''
        geomval = -1
        if shpname == None:
            shpname = saveSHP(self)
        shpWriter = Writer()
        shpWriter.autoBalance = 1        
        for COUNTER, column in enumerate(self.geocolumns):
            headerval = str(column[1])
            typeval = self.fieldTypes[self.allTypesDic[column[2].upper()]]
            
            if headerval == 'Geometry':
                geomval = column[2]
                geomtype = self.fieldTypes[column[2]]
            else:
                if typeval == 'M' or typeval== 'C':
                    shpWriter.field(headerval, typeval, '255')
                elif typeval == 'N' or typeval == 'L':
                    shpWriter.field(headerval, typeval)
                else:
                    shpWriter.field(headerval, typeval)
        shpWriter.shapeType = geomtype
        parsedGeometryList = []
        [parsedGeometryList.append(self.parseGeo(data[-1])) for data in self.retrievedGeoData]
        if geomtype == 5 or geomtype == 3:
            [shpWriter.poly(shapeType= geomtype,parts=parsedGeometry) for parsedGeometry in parsedGeometryList]
        elif geomtype == 1:
            [shpWriter.point(*parsedGeometry) for parsedGeometry in parsedGeometryList]
        dataLists = []
        for  data in self.retrievedGeoData:
            dList = list(data[:-1])
            for COUNTER,val in enumerate(dList):
                typeval = self.fieldTypes[self.allTypesDic[self.geocolumns[COUNTER][2].upper()]]
                if typeval == 'M' or typeval== 'C':
                    dList[COUNTER] = str(val)
                elif typeval == 'F':
                    dList[COUNTER] = float(val)
                elif typeval == 'N':
                    dList[COUNTER] = int(val)
                elif typeval =='D':
                    dList[COUNTER] = float(val)
            dataLists.append(dList)
        [shpWriter.record(*dList) for dList in dataLists]

        shpWriter.save(shpname) 
        prj = generatePRJ()
        prjfile = shpname.replace('.shp','') + '.prj' 
        prjfileOpen = open(prjfile, 'w')
        prjfileOpen.write(prj)
        prjfileOpen.close()
        self.insertLB('shapefile saved')
        self.insertLB(shpname)
        if self.batchIndicator ==0:
            tkMessageBox.showinfo('File Save', 'Your file has been saved at: %s' % shpname)
                
    def sridScrape(self, tablename):
        sql = "SELECT SRID FROM geom_cols_ref_sys WHERE f_table_name = '%s'" % tablename
        self.cursorspatial.execute(sql)
        srid = self.cursorspatial.fetchone()[0]
        return srid
        
    def parseGeo(self, geometry):
        partsList = []
        if geometry.find('POINT')!= -1 :
            geom = geometry.split('(')[1].replace(')','')
            geomlist = map(float,geom.split())
            partsList = geomlist
        elif geometry.find('LINESTRING')!= -1:
            geom = geometry.split('(')[1].replace(')','')
            geomsplit = geom.split(', ')
            
            geomlist = []
            for COUNTER,geoms in enumerate(geomsplit):
                       
                xy = map(float,geoms.split())
                        
                geomlist.append(xy)
                
            partsList.append( geomlist)
        else:
            
            geom = geometry.split('((')[1].replace('))','')
            partSplit = geom.split('), (')
            for part in partSplit:
                geomlist = []
                geomsplit = part.split(', ')
                for COUNTER,geoms in enumerate(geomsplit):
                       
                        xy = map(float,geoms.split())
                        
                        geomlist.append(xy)
                partsList.append(geomlist)
                
        return partsList

    def reverseParseGeo(self, shpReader):
        geomtype = find_key(self.fieldTypes, shpReader.shapeType )
        if geomtype == 'POINT':
            WKTlist = []
            WKTtemplate = 'POINT(%f %f)'
            shapes = shpReader.shapes()
            for shape in shapes:
                pnt = shape.points[0]
                WKT = WKTtemplate % (pnt[0], pnt[1])
                WKTlist.append(WKT)
        elif geomtype == 'POLYGON':
            WKTtemplate = 'POLYGON(('
            WKTlist = []
            shapes = shpReader.shapes()
            for shape in shapes:
                WKT = WKTtemplate
                points =shape.points
                firstCoords = points[0] 
                countVal = 0
                for COUNTER,coords in enumerate(points):
                    if COUNTER != len(shape.points)-1:
                        if coords == firstCoords and COUNTER != countVal:
                            WKT += str(coords[0]) + ' '+ str(coords[1])+ '), ('
                            firstCoords = points[COUNTER+1]
                            countVal = COUNTER +1                            
                        else:
                            WKT += str(coords[0]) + ' '+ str(coords[1])+ ', '

                    else:
                        WKT += str(coords[0]) + ' '+ str(coords[1])+ '))'
                WKTlist.append(WKT)
        elif geomtype == 'LINESTRING':
            WKTtemplate = 'LINESTRING('
            WKTlist = []
            shapes = shpReader.shapes()
            for shape in shapes:
                WKT = WKTtemplate
                for COUNTER,coords in enumerate(shape.points):
                    if COUNTER != len(shape.points)-1:
                        WKT += str(coords[0]) + ' '+ str(coords[1])+ ', '
                    else:
                        WKT += str(coords[0]) + ' '+ str(coords[1])+ ')'
                WKTlist.append(WKT)                   
        return WKTlist
    
    def shapefilePreview(self):
        'generate a preview of the selected shapefile'
        if self.testMode == 0:
            self.shpName = openSHP(self)
        shpReader = self.getReader(self.shpName)
        shpfields = shpReader.fields[1:]
        records =  shpReader.records()
        WKTlist = self.reverseParseGeo(shpReader)
        self.loadedTableDic = {}
        headers = []
        [headers.append(field[0]) for field in shpfields]
        headers.append('Geometry')
        #headers.append('id')

        self.columns = headers
        for COUNTER,values in enumerate(records):
            values.append(WKTlist[COUNTER])
            #values.append(COUNTER+1)
            for COUNT, value in enumerate(values):
                column = self.columns[COUNT]
                if column not in self.loadedTableDic:
                    self.loadedTableDic[column] = [value]
                else:
                    self.loadedTableDic[column].append(value)

        self.loadValsNew()    
            
    def spreadsheetPreview(self):
        'get a spreadsheet to preview'
        ssName = openSS(self)
        directory = os.path.dirname(ssName)
        if len(ssName.split('.')) <2: 
            tkMessageBox.showwarning('Missing File Type', 'The file extension is missing')
        name, extension =  os.path.splitext(ssName) #basename(ssName).split('.')
        
        if tkMessageBox.askyesno('Data Import', 'Are the field headers on the first row?'):
            rowval = 0
        else:
            rowval = tkSimpleDialog.askinteger('Field Names', 'On what row are the field headers located?')
            rowval = rowval-1
        if extension == "csv":

            
            csvbinary = open(ssName,'rb')
            
            csvreader = csv.reader(csvbinary, delimiter=',', quotechar='|')
            dataList = []
            [dataList.append(row) for row in csvreader[rowval:]]
            headers = []
            for header in dataList[row]:
                if header != '':
                    headers.append(header)
            self.columns = headers
            self.retrievedData = dataList[rowval+1:]
            self.loadedTableDic = {}
            
            for COUNTER,column in enumerate(self.columns):
                self.loadedTableDic[column] = []
                for values in self.retrievedData:
                    for COUNT, value in enumerate(values):
                        if COUNTER == COUNT:
                            self.loadedTableDic[column].append(value)
            if self.dataXlimit < len(self.columns):
                self.dataXlimit = len(self.columns)
            if self.dataYlimit < len(self.loadedTableDic[column]):
                self.dataYlimit = len(self.loadedTableDic[column]) +1
            x= 100
            y = 25
            COUNTER = 0
            
        
        elif extension == 'xls' or  extension == 'xlsx':
            #import xlrd 
            from xlrd import open_workbook
        
            wb = open_workbook(ssName)
            for s in wb.sheets()[:1]:
                data = []
                for row in range(rowval, s.nrows):
                    values = []
                    for col in range(s.ncols):
                        #print dir(s.cell)
                        values.append(s.cell(row,col).value)
                    data.append(values)
            self.columns = data[row]
            self.retrievedData = data[row+1:]
            self.loadedTableDic = {}
            #print self.columns 
            for COUNTER,column in enumerate(self.columns):
                #print column
                self.loadedTableDic[column] = []
                for values in self.retrievedData:
                    for COUNT, value in enumerate(values):
                        if COUNTER == COUNT:
                            self.loadedTableDic[column].append(value)            
            
        #elif extension == 'xlsx':
            #pass
        self.insertLB( extension + ' spreadsheet loaded')   
        if self.loadMode == 1:     
            self.loadValsNew()

    def dropTableSelect(self):
        dropSelect = SelectMenu(self, self.selectMetaTables(), self.dropTable, 'Select Table to Drop')
        
    def dropTable(self,table):
        dropSQL = "DROP Table {0}".format(table)
        if tkMessageBox.askyesno('Final Assurance', 'Are you sure you want to drop table {0}?\nIt cannot be undone.'.format(table)):
            self.cursorspatial.execute(dropSQL)   
             
    def dropTableDataSelect(self):
        dropSelect = SelectMenu(self, self.selectMetaTables(), self.dropDataTable, 'Select Table for Data Drop')
        
    def dropDataTable(self,table):
        dropSQL = "DELETE FROM  '{0}'".format(table)
        print dropSQL
        if tkMessageBox.askyesno('Final Assurance', 'Are you sure you want to drop all data from table {0}?\nIt cannot be undone.'.format(table)):
            self.cursorspatial.execute(dropSQL)
            tkMessageBox.showinfo('Data Dropped', 'Your data has been dropped')
        
    def exportDB(self):
        self.insertLB('export database tables')
      
        selectTables = SelectMenu(self,self.selectMetaTables(), self.exportTables, 'Select Tables to Export',  mode = EXTENDED )

    def exportTables(self,tables):
        'Export selected tables to Spatialite table'
        dbname = saveDB(self)
        shutil.copy(self.TEMPLATEdb, dbname)
        
        v = []
        if type(tables) == type(v):
            for table in tables:
                self.sqlWrite(table, dbname)
        else:
            self.sqlWrite(tables, dbname)
        tkMessageBox.showinfo('Database  Created', 'Your database was created here: {0}'.format(dbname))
        
    def exportDBCurrent(self):
        'export database tables'
        self.insertLB('export database tables')
        dbname = saveDB(self)
        shutil.copy(self.TEMPLATEdb, dbname)       
        self.sqlWrite(self.selectedTable, dbname)
        tkMessageBox.showinfo('Database  Created', 'Your database was created here: {0}'.format(dbname))
        
    def sqlWrite(self, table, dbname):
        'create new connection and write table data to new database'

        sql_connection = sqlconn.Connection(dbname)     
        cursorspatial = sqlconn.Cursor(sql_connection)
        sql_connection.enable_load_extension(1)
        sql_connection.load_extension('libspatialite-2.dll')   
        createSQL,  insertSQList = self.exportDBTables(table)
        cursorspatial.execute(createSQL) 
        for sql in insertSQList:
            cursorspatial.execute(sql)
        sql_connection.commit()
        del sql_connection, cursorspatial  


    def createTables(self ):
        'create Table from raw sheet'
        
        data =  self.table.model.getData()
        createSQL = 'CREATE TABLE {0} ( {1} )'
        table = tkSimpleDialog.askstring('New Table', "What is the name of the new table?")
        if table == '':
            tables = self.selectMetaTables().values()
            table = 'newtable'
            if table in tables:
                table = table + str(random.randint(1, 10000))
        
        inVal = ''   
        colVals = ''     
        for COUNTER,coVal in  enumerate(self.columns):

            if coVal != 'Geometry':
                colVals += coVal
            else:
                colVals += 'AsText('+coVal +')'
                insertSQL = 'INSERT INTO {0} VALUES ({1}GeomFromText({2},{3}))'
            inVal += '"'+coVal+'" ' +  coVal[2]

            if COUNTER != len(columnVals)-1:
                inVal += ','
                colVals += ','
            
        createSQL = createSQL.format(table, inVal) 
        self.cursorspatial.execute(createSQL)
        
        
        
    def exportDBTables(self, table  ):
        'create SQL, insert SQL, select SQL generator'
        
        createSQL = 'CREATE TABLE {0} ( {1} )'
        insertSQL = 'INSERT INTO {0} VALUES '
        recoverSQL = "SELECT RecoverGeometryColumn('{0}', 'Geometry', {1}, '{2}', 'XY')"
        dataSQL = "SELECT srid, type FROM  'geometry_columns' where f_table_name = '{0}'"
        columnVals = self.tableInfo(table)
        inVal = ''        
        colVals = ''
        switch =0
        for COUNTER,coVal in  enumerate(columnVals):

            if coVal[1] != 'Geometry':
                colVals += coVal[1]
            else:
                colVals += 'AsText('+coVal[1] +')'
                switch =1
                insertSQL = 'INSERT INTO {0} VALUES ({1}GeomFromText({2},{3}))'
            inVal += '"'+coVal[1] +'" ' +  coVal[2]
            if coVal[3] == 1:
                inVal += ' NOT NULL '
            if coVal[5] == 1:
                inVal += ' PRIMARY KEY '
            if coVal[4] != None:
                inVal += " DEFAULT \'\'"
            if COUNTER != len(columnVals)-1:
                inVal += ','
                colVals += ','
            

        createSQL = createSQL.format(table, inVal) 
        insertSQList = []
        if switch == 1:
            self.cursorspatial.execute(dataSQL.format(table))
            typedata = self.cursorspatial.fetchone()  
            rsql = recoverSQL.format(table,typedata[0], typedata[1])
            insertSQList = [rsql]
            
        selectSQL = 'SELECT {0} FROM {1}'.format(colVals,table)
        self.cursorspatial.execute(selectSQL)
        rows = self.cursorspatial.fetchall()        
        
        for row in rows:
            newrow = []
            for val in row:
                if type(val) == type(u'a') :
                    val = str(val)
                elif val == None:
                    val = ''
                newrow.append(val)
            row = tuple(newrow)
            if switch == 0:
                sql = insertSQL.format(table) + str(row)
            else:
                valStr = ''
                for val in row[:-1]:
                    if type(val) == type('a') :
                        valStr += "'" + val + "',"
                    else:
                        valStr+=str(val)+','
                geom = "'"+row[-1]+ "'"
                sql = insertSQL.format(table,valStr, geom, typedata[0])
            insertSQList.append(sql)
        return createSQL,  insertSQList

    def exportWholeDB(self):
        'export entire database'
        self.insertLB('export entire database')
        dbname = saveDB(self)
        
        shutil.copy(self.mainDB, dbname)

    def openGUI(self):
        os.startfile('spatialite_gui.exe')
 
 
    def readKML(self, kmlfile):
        kml = open(kmlfile)
        line = kml.readline()
        while line:
            if line.find('<Polygon>') != -1:
                shape = 5
            if line.find('<Point>') != -1:
                shape = 1
            if line.find('<coordinates>') != -1 and line.find('</coordinates>') == -1:
                line = kml.readline()
                coords = line
            if line.find('<coordinates>') != -1 and line.find('</coordinates>') != -1:
                coords = line.replace('<coordinates>','')
                coords = coords.replace('</coordinates>','')
            line = kml.readline()
        kml.close()
        coords = coords.replace('\t','')
        coords = coords.replace('\n','')
        coords= coords.split()
        newcoords = []
        for coord in coords:
            split= coord.split(',')
            coord = [float(split[0]),float(split[1])]
            newcoords.append(coord)
        return newcoords, shape 
 
 
    def exportKML(self):
        'export KML table select'
        self.insertLB('export KML')
        self.exportType = 'KML'
        self.geoTabletableSelect()
        
        
    def makeKML(self):
        'export a table to a KML'
        kmlname = saveKML(self)
        self.geocolumns = self.tableInfo(self.selectedTable) 
        self.dataXlimit = len(self.geocolumns)
        #fields = 'AsKML(Geometry)'
 


        self.batchIndicator = 1
        self.selectSQL()
        self.batchIndicator = 0
        sql = self.currentSQL.replace('AsText','AsKML')
        self.cursorspatial.execute(sql)
        self.retrievedGeoData = self.cursorspatial.fetchall() 
        kml = open(kmlname,'w')
        kmlval = ''
        for geoms in self.retrievedGeoData:
            valstring = '<description>\n'
            for COUNT, val in enumerate(geoms[:-1]):
                
                valstring+= self.geocolumns[COUNT][1] + ' = ' + unicode(val) + '\n'
            valstring += '</description>\n' +'<styleUrl>#default</styleUrl>\n'

            kmlval += '<Placemark>\n'+ valstring + geoms[-1].replace('><','>\n<')+ '</Placemark>\n'
            
            
        finalkml = polykml % (kmlname, kmlval)
        kml.write(finalkml)
        kml.close()
        self.insertLB('KMl exported')
        self.insertLB(kmlname)
        tkMessageBox.showinfo('KML Saved', 'Your KML was saved here:\n {0}'.format(kmlname))

    def makeKMLcurrent(self):
        'export the current data table to a KML'
        kmlname = saveKML(self)

        self.geocolumns = self.tableInfo(self.selectedTable) 
        sql = self.currentSQL.replace('AsText','AsKML')

        self.cursorspatial.execute(sql)
        self.retrievedGeoData = self.cursorspatial.fetchall() 
        kml = open(kmlname,'w')
        kmlval = ''
        for geoms in self.retrievedGeoData:
            valstring = '<description>\n'
            for COUNT, val in enumerate(geoms[:-1]):
                valstring+= self.geocolumns[COUNT][1] + ' = ' + str(val) + '\n'
            valstring += '</description>\n' +'<styleUrl>#default</styleUrl>\n'
            kmlval += '<Placemark>\n'+ valstring + geoms[-1].replace('><','>\n<')+ '</Placemark>\n'
        finalkml = polykml % (kmlname, kmlval)
        kml.write(finalkml)
        kml.close()
        self.insertLB('KMl exported')
        self.insertLB(kmlname)
        tkMessageBox.showinfo('KML Saved', 'Your KML was saved here:\n {0}'.format(kmlname))


    def addCurrentData(self):
        'add currently displayed data to table'
        self.insertLB('add data to table')
        currentSelectMenu = SelectMenu(self, self.selectMetaTables(), self.addCurrentToTable, 'Select a Table to Append')
        
    def addCurrentToTable(self, table):
        'append current loaded data to a selected datatable'
        data =  self.table.model.data 
        
        tHeaders = self.table.model.columnNames
        insertSQL = "INSERT INTO {0} ({1}) VALUES ({2}) "

        tableheaders = self.tableInfo(table)     
        
        
        def dicadd(key,value, dic):
            
            dic[key] =value
            return
        tablefields = {}
        [dicadd(field[1], field[2], tablefields) for field in tableheaders]
        
        
        tablenameStr = ''
        for field in tableheaders:
            tablenameStr +=field[1]+','
        tablenameStr = tablenameStr.replace('id,', '')
        tablenameStr = tablenameStr[:-1]
        fieldNames = tablefields.keys()
        fieldNames.sort()
        
        tHeaders.sort()
        if  fieldNames == tHeaders:
            for count in range( len(data)):
                valdic = data[str(count+1)]
                valstr = ''
                for COUNTER, field in enumerate(tablefields):
                    if field != 'id':
                        if COUNTER != len(tablefields)-1:
                            if tablefields[field] != 'text' and tablefields[field].find('varchar') == -1:
                                valstr += str(valdic[field]) + ','
                            elif tablefields[field] == 'text' or tablefields[field].find('varchar') != -1:
                                valstr += "'" + str(valdic[field]) + "',"
                            else:
                                valstr += str(valdic[field]) + ','
                        else:    
                            if tablefields[field] != 'text' and tablefields[field].find('varchar') == -1:
                                valstr += str(valdic[field]) 
                            elif tablefields[field] == 'text' or tablefields[field].find('varchar') != -1:
                                valstr += "'" + str(valdic[field]) + "',"
                            else:
                                valstr += str(valdic[field]) 
                sql = insertSQL.format(*(table, tablenameStr, valstr))
                self.cursorspatial.execute(sql)
            if not tkMessageBox.askyesno('Final Assurance', 'Add the shapefile to the database?'):  

                    self.sql_connection.rollback()
                    tkMessageBox.showinfo('Data Rollback', 'Your data was not added to %s' % self.selectedTable)

            else:
                self.sql_connection.commit()
                    
                tkMessageBox.showinfo('Data Upload', 'Your data was successfully added to %s' % self.selectedTable)    
        else:
            if tkMessageBox.askyesno('Data Mismatch', 'The columns do not match.\nWould you like to perform a custom import?'):
                self.addCustomTables = CustomImport(self,table, data, tHeaders)
                        
                  
    def addShpToTable(self):
        #import shapefile
        self.insertLB('add data to table')

        shapeSelectMenu = SelectMenu(self, self.selectMetaGeoTables(), self.addShapefile, 'Select a Table to Append')
 


    def transformSRID(self,WKT,SRID):
        self.sysSRID = '26943'
        if not SRID == self.sysSRID:
            transformSQL = "Transform('%s', %s)" % (WKT,self.sysSRID)
            WKT=transformSQL
        else:
            WKT = "'%s',%s" % (WKT,SRID)
        return WKT
    
    def idGen(self, table):

        sqlarea = 'SELECT MAX(ID) FROM %s'
        self.cursorspatial.execute(sqlarea)
        max = self.cursorspatial.fetchone()
        return max
    
    def getReader(self,shpName):
        shp = str(shpName.replace('.shp',''))
        shpReader =Reader(shp)
        return shpReader 
           
    def addSSToTable(self):
        #import shapefile
        self.insertLB('add data to table')
        
        spreadSelectMenu = SelectMenu(self, self.selectMetaTables(), self.addSpreadsheet, 'Select a Table to Append')

    def addSpreadsheet(self, table):
        self.loadMode = 0
        self.spreadsheetPreview()
        data = self.parseData()
        self.loadMode = 1
        
        insertSQL = "INSERT INTO {0} ({1}) VALUES ({2}) "

        tableheaders = self.tableInfo(table)    
        
        
        def dicadd(key,value, dic):
            
            dic[key] =value
            return
        tablefields = {}
        #[dicadd(field[1], field[2], tablefields) for field in tableheaders]
        [ tablefields.update({field[1]: field[2]}) for field in tableheaders]

        fieldNames = tablefields.keys()
        fieldNames.sort()
        tablenameStr = ''
        for field in fieldNames:
            tablenameStr +=field+','
        tablenameStr = tablenameStr.replace('id,', '')
        tablenameStr = tablenameStr[:-1]
        tHeaders = self.columns
        tHeaders.sort()
        if  fieldNames == tHeaders:
            for count in range( len(data)):
                valdic = data[str(count+1)]
                valstr = ''
                for COUNTER, field in enumerate(fieldNames):
                    if field != 'id':
                        if COUNTER != len(tablefields)-1:
                            if tablefields[field] != 'text' and tablefields[field].find('varchar') == -1:
                                valstr += str(valdic[field]) + ','
                            elif tablefields[field] == 'text' or tablefields[field].find('varchar') != -1:
                                valstr += "'" + str(valdic[field]) + "',"
                            else:
                                valstr += str(valdic[field]) + ','
                        else:    
                            if tablefields[field] != 'text' and tablefields[field].find('varchar') == -1:
                                valstr += str(valdic[field]) 
                            elif tablefields[field] == 'text' or tablefields[field].find('varchar') != -1:
                                valstr += "'" + str(valdic[field]) + "',"
                            else:
                                valstr += str(valdic[field]) 
                if valstr[-1] == ',':valstr= valstr[:-1]
                sql = insertSQL.format(*(table, tablenameStr, valstr))
                
                self.cursorspatial.execute(sql)
            if not tkMessageBox.askyesno('Final Assurance', 'Add the spreadsheet to the database?'):  

                    self.sql_connection.rollback()
                    tkMessageBox.showinfo('Data Rollback', 'Your data was not added to %s' % table)

            else:
                self.sql_connection.commit()
                    
                tkMessageBox.showinfo('Data Upload', 'Your data was successfully added to %s' % table)
        else:
            if tkMessageBox.askyesno('Data Mismatch', 'The columns do not match.\nWould you like to perform a custom import?'):
                self.addCustomTables = CustomImport(self,table, data, self.columns)
        

    def addShapefile(self, table):
        self.selectedTable = table
        self.batchIndicator = 1
        self.shapefilePreview()
        self.batchIndicator = 0
        data = self.parseData()
        self.loadMode = 1
        insertSQL = "INSERT INTO {0} ({1}) VALUES ({2}) "

        tableheaders = self.tableInfo(table)   
        
        
        def dicadd(key,value, dic):
            
            dic[key] =value
            return
        tablefields = {}
        [dicadd(field[1], field[2], tablefields) for field in tableheaders]

        fieldNames = tablefields.keys()
        fieldNames.sort()
        tablenameStr = ''
        for field in fieldNames:
            tablenameStr +=field+','
        tablenameStr = tablenameStr.replace('id,', '')
        tablenameStr = tablenameStr[:-1]
        tHeaders = self.columns
        tHeaders.sort()
        if  fieldNames == tHeaders:
            for count in range( len(data)):
                valdic = data[str(count+1)]
                valstr = ''
                for COUNTER, field in enumerate(fieldNames):
                    if field != 'id':
                        if COUNTER != len(tablefields)-1:
                            if tablefields[field] != 'text' and tablefields[field].find('varchar') == -1:
                                valstr += str(valdic[field]) + ','
                            elif tablefields[field] == 'text' or tablefields[field].find('varchar') != -1:
                                valstr += "'" + str(valdic[field]) + "',"
                            else:
                                valstr += str(valdic[field]) + ','
                        else:    
                            if tablefields[field] != 'text' and tablefields[field].find('varchar') == -1:
                                valstr += str(valdic[field]) 
                            elif tablefields[field] == 'text' or tablefields[field].find('varchar') != -1:
                                valstr += "'" + str(valdic[field]) + "',"
                            else:
                                valstr += str(valdic[field]) 
                if valstr[-1] == ',':valstr= valstr[:-1]
                sql = insertSQL.format(*(table, tablenameStr, valstr))
                
                self.cursorspatial.execute(sql)
            if not tkMessageBox.askyesno('Final Assurance', 'Add the shapefile to the database?'):  

                    self.sql_connection.rollback()
                    tkMessageBox.showinfo('Data Rollback', 'Your data was not added to %s' % table)

            else:
                self.sql_connection.commit()
                files = os.listdir(os.path.basename(self.shpName))
                for file in files:
                    if file.find(self.shpName.replace('.shp',''))!=-1:
                        shutil.copy(os.path.join(os.path.dirname(self.shpName),file), os.path.join(self.shpRepo, file))    
                tkMessageBox.showinfo('Data Upload', 'Your data was successfully added to %s' % table)
        else:
            if tkMessageBox.askyesno('Data Mismatch', 'The columns do not match.\nWould you like to perform a custom import?'):
                
                self.addCustomSHP()
        
    def addCustomSHP(self):
        'Dialogue to match shapefiles and tables together'
        
        def checkTypes(tablefield,shapefield):
  
            tbFieldType = self.tableInfoDic[tablefield]
            shpFieldType = self.shapeInfoDic[shapefield]
            if tbFieldType != shpFieldType:
                val=1
                if tbFieldType == 'DOUBLE':
                    if shpFieldType == "TEXT":
                        val = 0
                    elif shpFieldType == "INTEGER":
                        val=2
                    elif shapefield == "Geometry":
                        val=0
                    elif shpFieldType== 'FLOAT':
                        val= 1
                    else:
                        val = 1
                elif tbFieldType == 'real':
                    if shpFieldType == "TEXT":
                        val = 0
                    elif shpFieldType == "INTEGER":
                        val=2
                    elif shapefield == "Geometry":
                        val=0
                    elif shpFieldType== 'FLOAT':
                        val= 1
                    else:
                        val = 1
                
                elif  tbFieldType == 'TEXT':
                    if shpFieldType == "INTEGER":
                        val=2
                    elif  shpFieldType == 'DOUBLE':
                        val=2
                    elif shapefield == "Geometry":
                        val=0
                    elif shpFieldType== 'FLOAT':
                        val= 2
                    else:
                        val=1
                elif  tbFieldType.find('varchar') != -1:
                    if shpFieldType == "INTEGER":
                        val=2
                    elif  shpFieldType == 'DOUBLE':
                        val=2
                    elif shapefield == "Geometry":
                        val=0
                    elif shpFieldType== 'FLOAT':
                        val= 2
                    else:
                        val=1
                elif tbFieldType == 'INTEGER':
                    if shpFieldType == "TEXT":
                        val=0
                    elif  shpFieldType == 'DOUBLE':
                        val=2
                    elif shapefield == "Geometry":
                        val=0
                    elif shpFieldType== 'FLOAT':
                        val= 2
                    else:
                        val=1

                elif tablefield == 'Geometry':

                    if shapefield == "Geometry":
                        if tbFieldType == 'LINESTRING':
                            if shpFieldType == "POLYGON":
                                val=0
                            elif  shpFieldType == 'POINT':

                                val=0

                            else:
                                val=1
                        
                        elif tbFieldType == 'POLYGON':
                            if shpFieldType == "LINESTRING":
                                val=0
                            elif  shpFieldType == 'POINT':

                                val=0

                            else:
                                val=1

                        elif tbFieldType == 'POINT':
                            if shpFieldType == "LINESTRING":
                                val=0
                            elif  shpFieldType == 'POLYGON':

                                val=0

                            else:
                                val=1
                    
                    else:
                        val=0
            else:
                return 1,tbFieldType, shpFieldType    
            return val,tbFieldType, shpFieldType
            
        def addData():
            WKTlist = self.reverseParseGeo(shpReader)
            
            insertSQL = "INSERT INTO %s (%s) VALUES "
            tablefields = ''
            sFields = []
            IDFIELD =''
            for COUNTER, matches in enumerate(self.fieldMatchesList):
                if matches[1].find('GEOID') != -1:
                    IDFIELD = matches[0]
                    
                elif matches[0] != 'id' and matches[1].find('GEOID') == -1:
                    if matches[0] != 'Geometry':
                        
                        tablefields += "'" +matches[0] + "'," 
#            IDFIELD ='GeoID'
#            for COUNTER, matches in enumerate(self.fieldMatchesList):
#                if matches[0].find('GeoID') != -1:
#                    IDFIELD = matches[0]
#                    tablefields += "'GeoID'," 
#                #elif matches[0] != 'id' and matches[1].find('GEOID') == -1:
#                #    if matches[0] != 'Geometry':
#                        
#                        

                                 
                    sFields.append(matches[1])
            if GEO.get() ==1:
                if 'Acres' in self.tableInfoDic.keys():
                    unitval = 'Acres'
                    tablefields += "'" +unitval + "',"
                elif 'Length' in  self.tableInfoDic.keys():
                    unitval = 'Length'     
                    tablefields += "'" +unitval + "',"
            if PROPS.get() == 1: 
                if 'Property' in self.tableInfoDic.keys():
                    tablefields += "'" +'Property' + "',"
            if HMUS.get() == 1: 
                if 'HMU'  in self.tableInfoDic.keys():
                    tablefields += "'" +'HMU' + "',"
            
            #if GEOID.get() == 1: 
            if IDFIELD != '':
                     tablefields += "'" +IDFIELD + "',"
                                        
                    
            tablefields += 'Geometry'
            sFields.append('Geometry')                    
            insertSQLval = insertSQL % (self.selectedTable, tablefields)
            allfields = shpReader.fields
            
            fieldIndexDic = {}
            for COUNTER, field in enumerate(allfields):
                if field[0] in sFields and field[0] != 'Geometry':
                    fieldIndexDic[field[0]] = (COUNTER-1, field[1])
            records = shpReader.records()
            for COUNTER, record in enumerate(records):
                    valSQL = ''
                    for fieldCOUNT, field in enumerate(sFields):

                        if field != 'Geometry' and field.find('Value =') == -1:
                            index, gtype = fieldIndexDic[field]
                            if gtype == 'C' or gtype == 'Text' or gtype.find('varchar') !=-1:
                                strVal = record[index]
                                checkStrVal = ''
                                if len(strVal.split()) == len(checkStrVal.split()): #check for extraneous spaces 
                                    strVal = ''
                                valSQL += str('"'+strVal+'"') + ','
                                
                            else:
                                valSQL += str(record[index]) + ','
                        elif field.find('Value =') != -1:
                            newval = field.replace('Value = ','')

                            if self.tableInfoDic[self.typeDataList.get(0,END)[fieldCOUNT]] == 'TEXT':
                                valSQL += "'" + newval + "',"                           
                            else:
                                valSQL +=  newval + ","

                    if GEO.get() == 1:
                        sridVal = srid.get()
                        geoWKTobject = loads(WKTlist[COUNTER]) 
                        if sridVal == '26943':
                            acresMultiplier = 0.000247105
                            lengthMultiplier = (1/3.28084)
                        elif sridVal == '2227':
                            acresMultiplier = (1/43560)
                            lengthMultiplier = 1
                        elif sridVal == '26910':
                            acresMultiplier = 0.000247105
                            lengthMultiplier = (1/3.28084)                            
                           
                        if 'Acres' in  self.tableInfoDic.keys():
                            
                            acresVal = geoWKTobject.area * acresMultiplier
                            valSQL +=  str(acresVal) + ','  
                            
                            
                        elif 'Length' in  self.tableInfoDic.keys():
                            lengthVal = geoWKTobject.length * lengthMultiplier
                            valSQL +=  str(lengthVal) + ',' 
                    if PROPS.get() == 1:        
                        if 'Property' in self.tableInfoDic.keys():
                            propsql =  "SELECT NAME FROM CCWD_PROPERTIES WHERE INTERSECTS(Geometry, ST_GeomFromText('{0}'))".format(WKTlist[COUNTER])
                            self.cursorspatial.execute(propsql)
                            prop = self.cursorspatial.fetchone()
                            v = ()
                            if type(prop) == type(v):
                            
                                valSQL +=  '"'+prop[0] +'"' + ','
                            else:
                                valSQL +=  '"",'
                    if HMUS.get() == 1: 
                        if 'HMU'  in self.tableInfoDic.keys():
                            hmusql =  "SELECT NAME FROM CCWD_ManagementUnits WHERE INTERSECTS(Geometry, ST_GeomFromText('{0}'))".format(WKTlist[COUNTER])
                            self.cursorspatial.execute(hmusql)
                           
                            hmu = self.cursorspatial.fetchone()
                            v= ()
                            if type(hmu) == type(v):
                                valSQL +=  '"'+hmu[0] +'"'+ ','
                            else:
                                valSQL +=  '"",'           
                    if IDFIELD != '': 
                        geoSQL = "SELECT AsText(Centroid(Transform(ST_GeomFromText('{0}',{1}),4326)))".format(WKTlist[COUNTER], srid.get())
                        self.cursorspatial.execute(geoSQL)
                        results = self.cursorspatial.fetchone()
                        geom = results[0]
                        parsedGeom = self.parseGeo(geom) 
                        geoid = 'W'+ str(abs(parsedGeom[0]))[:7].replace('.','')  + 'N'+ str(abs(parsedGeom[1]))[:7].replace('.','')
                        valSQL +=  '"'+geoid +'"'+ ','
                           
                    if srid.get()!=self.sysSRID:
                        valSQL += "Transfrom(ST_GeomFromText('{0}',{1}),{2})".format(WKTlist[COUNTER], srid.get(), self.sysSRID)
                    else:
                        valSQL += "ST_GeomFromText('%s',%s)" % (WKTlist[COUNTER], srid.get())

                    sql = insertSQLval + '(%s)' % valSQL
                    print sql
                    self.cursorspatial.execute(sql)

            if not tkMessageBox.askyesno('Final Assurance', 'Add the shapefile to the database?'):  

                    self.sql_connection.rollback()
                    tkMessageBox.showinfo('Data Rollback', 'Your data was not added to %s' % self.selectedTable)

            else:
                self.sql_connection.commit()
                    
                tkMessageBox.showinfo('Data Upload', 'Your data was successfully added to %s' % self.selectedTable)
        
        def restoreMatchCanvas():
            self.tablePreview.grid_forget()
            
            self.matchCanvas.grid(row=0,column=0)
            addButton.grid_forget()
            restoreButton.grid_forget()  
            matchText()      
            
        def previewData():
            undoButton.grid_forget()
            #restoreButton.grid(row=1,column=0)
            self.matchCanvas.delete('all')
            self.matchCanvas.grid_forget()

            records =  shpReader.records()
            
            self.previewTableDic = {}
            headers = []
            shpfields = self.shpDataList.get(0,END)
            tablefields = self.typeDataList.get(0,END)
            [headers.append(field) for field in shpfields ]
            fieldsSHP = []
            [fieldsSHP.append(field[0]) for field in shpReader.fields[1:]]
            
            for COUNTER, column in enumerate(headers):
                self.previewTableDic[column] = []
                if column in fieldsSHP:
                    
                    for values in records:
                        
                        for COUNT, value in enumerate(values):

                                if fieldsSHP[COUNT] == column:
                                    self.previewTableDic[column].append(value)
                                    
                elif column.find('Value =') !=-1:
                    columnVal = tablefields[COUNTER]
                    for values in records:
                        self.previewTableDic[columnVal].append(column.replace('Value = ',''))                 
                                
            dataDic = {}
            if len(self.previewTableDic[headers[0]]) > 0:
                valueRange = len(self.previewTableDic[headers[0]])
            else:
                valueRange =0
            for i in range(1,valueRange+1):
                dataDic[str(i)] = {}
            for COUNTERX, columns in enumerate(headers):
                if type(columns) == type('a') or type(columns) == type(u'a'):
                    header = columns
                else: 
                    header = columns[1]
                values = self.previewTableDic[columns]
                if len(values)> 0:
                    for COUNTERY, value in enumerate(values):
                        dataDic[str(COUNTERY+1)][header] = value 
                else:
                    if dataDic == {}:
                        dataDic[str(0)] = {}
                    dataDic[str(0)][header] = '' 
            self.tablePreview = TableCanvas(FRAME3, newdict=dataDic)
            self.tablePreview.createTableFrame()
                
        def generateMatches():
            self.matchCanvas.delete('generated')
            self.fieldMatchesList =[]
            tablefields = self.typeDataList.get(0, END)
            shpfields = self.shpDataList.get(0, END)

            if len(tablefields) == len(shpfields):
                self.fieldMatchesList = zip(tablefields, shpfields)

                self.matchCanvas.create_text(10,60, text = 'A', anchor='w',tags=('generated', 'text', 'DataTable Field  (Type)'))
                self.matchCanvas.create_text(200,60, text = 'B', anchor='w',tags=('generated', 'text','Shapefile Field  (Type)'))
                self.matchCanvas.create_line(10,70, 400,70,tags=('generated') )
    
                statusCOUNTER = 1
                customCOUNTER = 0
                for COUNTER, data in enumerate(self.fieldMatchesList):
                    tablefield = data[0]
                    shapefield = data[1]
                    if shapefield.find('Value =') == -1:
                        typestatus, tType, sType = checkTypes(tablefield, shapefield)
                        if typestatus ==1:
                            fontcolor = 'black'
                        elif typestatus ==0:
                            fontcolor = 'red'
                            statusCOUNTER = 0
                        elif typestatus==2:
                            fontcolor = 'orange'
                            statusCOUNTER = 2
                            
                      
                        tText = tablefield + '  (%s)' % tType    
                        sText = shapefield + '  (%s)' % sType    
                    else:
                            fontcolor = 'blue'
                            tText = tablefield + '  (%s)' % self.tableInfoDic[tablefield]    
                            sText = shapefield + '  (%s)' % self.tableInfoDic[tablefield]                           
                            customCOUNTER = 1 

                    self.matchCanvas.create_text(10,(COUNTER+2) * 20 + 40,fill=fontcolor, text = tText, anchor='w', tags=('generated', 'text', tablefield))
                    self.matchCanvas.create_text(200,((COUNTER+2) * 20 + 40),fill=fontcolor, text = sText, anchor='w',tags=('generated', 'text', shapefield))
                    self.matchCanvas.create_line(10,(COUNTER+2) * 20 + 50, 400,(COUNTER+2)  * 20 +50,tags=('generated', 'line') )
                
                if statusCOUNTER == 1:
                    self.matchCanvas.create_text(10,385,fill='black', text = 'All Field Types Match', anchor='w',tags=('generated', 'text'))
                
                elif statusCOUNTER == 0:
                    self.matchCanvas.create_text(10,385,fill='black', text = 'Field Types Do Not Match', anchor='w',tags=('generated', 'text'))
                    return
                else:
                    self.matchCanvas.create_text(10,385,fill='black', text = 'We can let it slide this time', anchor='w',tags=('generated', 'text'))
                if customCOUNTER == 1:
                    self.matchCanvas.create_text(10,365,fill='black', text = 'Custom Import Accepted', anchor='w',tags=('generated', 'text'))
                                
                if statusCOUNTER != 0:


                    addButton.grid(row=0,column=0)
                    undoButton.grid(row=1,column=0)
                    
                    
                    
            else:
                self.matchCanvas.create_text(10,60, text = 'The fields must be matched', anchor='w',tags=('generated', 'text', 'A'))
                self.matchCanvas.create_line(10,70, 400,70 ,tags=('generated'))
                

        def resets():
            addButton.grid_forget()
            undoButton.grid_forget()

            self.matchCanvas.delete('generated')
            resetTableList()
            resetShpList()   
                 
        def autoSort():
            addButton.grid_forget()
            resets()
            self.fieldMatchesList =[]
            tablefields = self.fieldList.get(0, END)
            shpfields = self.tableList.get(0, END)

            if len(tablefields) == len(shpfields):
                self.fieldMatchesList = zip(tablefields, shpfields)
                tFields = []
                sFields = []   
                for COUNTER, data in enumerate(self.fieldMatchesList):
                    tFields.append(data[0])
                    sFields.append(data[1]) 
                for field in tFields:
                    if field in sFields:
                                   
                        self.shpDataList.insert(END,field)
                        self.typeDataList.insert(END,field)
                generateMatches()
            else:
                self.matchCanvas.create_text(10,60, text = 'The fields do not match', anchor='w',tags=('generated', 'text', 'A'))
                self.matchCanvas.create_line(10,70, 400,70 )        
                    
        def resetShpList():
            self.shpDataList.delete(0,END)

        def resetTableList():
            self.typeDataList.delete(0,END)
                
        def removeFromShpList(event):
            addButton.grid_forget()
            undoButton.grid_forget()

            self.shpDataList.delete('active', self.shpDataList.curselection())

        def removeFromTableList(event):
            addButton.grid_forget()
            undoButton.grid_forget()

            self.typeDataList.delete('active', self.typeDataList.curselection())
            
        def addshpTypeInfo(event):
            try:
                addButton.grid_forget()
                undoButton.grid_forget()

                field = self.fieldList.selection_get()
                if field not in self.shpDataList.get(0,END):
                    self.shpDataList.insert(END,field)
                
            except:
                pass        
        
        def addDataTypeInfo(event):

                table = self.tableList.selection_get()
                if table not in self.typeDataList.get(0,END):
                    self.typeDataList.insert(END,table)
                    
        def restartSHP():
            addButton.grid_forget()
            undoButton.grid_forget()
            takeout()
            self.masterselect = Frame()
            self.shpName = openSHP(self)
            self.addCustomSHP() 
        
        def restartTable():
            addButton.grid_forget()
            undoButton.grid_forget()
            self.addShpToTable()

        def takeout():
            self.masterselect.destroy()
            
        def getReader(shpName):
            shp = str(shpName.replace('.shp',''))
            shpReader =Reader(shp)
            return shpReader
        
        def calculateVal(event):
            title = 'Supply Value'
            
            field = self.typeDataList.selection_get()
            #index = self.typeDataList.curselection()[0]
            fields = self.typeDataList.get(0,END)
            x =0 
            for f in fields:
                if f == field:
                    index = x
                x+=1
            self.masterselect.iconify()
            prompt = 'Please supply a value:'
            val = tkSimpleDialog.askstring(title, prompt)
            if type(val) == type(''):
                value = 'Value = ' + val
                self.shpDataList.insert(index, value)
            self.masterselect.deiconify()

        def matchText():
            self.matchCanvas.create_text(10,10,anchor = 'nw',font=('Times', '11','bold'), text='Match Fields From Data Table (A) to Shapefile(B)')

            self.matchCanvas.create_line(10,30, 400, 30)
            
            self.matchCanvas.create_text(10,60, text = 'Double click on the field names to match them', anchor='w',tags=('generated', 'text', 'A'))
            self.matchCanvas.create_text(10,80, text = 'Double click matched fields to remove them', anchor='w',tags=('generated', 'text', 'A'))
            self.matchCanvas.create_text(10,100, text = 'Right click on a selected table field to suppy a value', anchor='w',tags=('generated', 'text', 'A'))
            
            self.matchCanvas.create_text(10,130, text = 'Table = {0}'.format(self.selectedTable), anchor='w',tags=('generated', 'text', 'A'))
            self.matchCanvas.create_text(10,150, text = 'Shapefile = {0}'.format(self.shpName), anchor='w',tags=('generated', 'text', 'A'))
    


            
        shpReader = getReader(self.shpName)
        self.masterselect = Toplevel()
        master = self.masterselect
        master.wm_attributes("-topmost", 1)
        master.title('Match Columns')
        #master.maxsize(1000,700)
        master.geometry('+100+100')
        master.iconbitmap(self.logoPath)
        self.sqlDialogue = Frame(master, relief=SUNKEN, bd=2, bg=self.backgroundcolor)
        self.sqlDialogue.grid(row=0, column=0,rowspan=9,columnspan=9, padx = 1)


        self.tables = self.resourceDic.keys()

        self.sqlMainFrame =  Frame(self.sqlDialogue, relief=SUNKEN, bd=2, bg=self.backgroundcolor)
        self.sqlMainFrame.grid(row=0, column=0, sticky = W+E+N+S)
        self.listboxFrame =  Frame(self.sqlMainFrame, bg=self.backgroundcolor)
        self.listboxFrame.grid(row=0, column=0,sticky = W+E+N+S, padx = 10,pady = 5)
        
        FRAME1 = Frame(self.listboxFrame,  bg=self.backgroundcolor)
        FRAME1.grid(row=0,column=0,sticky=N+S,padx = 2,pady = 5, ipadx =5)
        
        
        self.scrollbarTable = Scrollbar(FRAME1, orient=VERTICAL)
        
        self.tableList = Listbox(FRAME1,selectmode=SINGLE,height=10)
        self.tableList.grid(row=0, column=0, )
        self.tableList.bind("<Double-Button-1>", addDataTypeInfo)

        self.scrollbarTable.grid(row=0, column=1,sticky=N+S )

        self.scrollbarTable.config(command=self.tableList.yview)
        self.tableLabel = Label(FRAME1,font=('Times','11','bold'), text = '(A) Table Fields')
        self.tableLabel.grid(row=1,column=0,columnspan=2)

        
        FRAME4 = Frame(FRAME1,  bg=self.backgroundcolor)
        FRAME4.grid(row=2,column=0,sticky=N+S,padx = 2,pady = 5)
        
        self.typeDataList = Listbox(FRAME4,selectmode=SINGLE,height=10)
        self.typeDataList.grid(row=0, column=0, )        
        self.typeDataList.bind("<Double-Button-1>", removeFromTableList)
        self.typeDataList.bind("<Button-3>", calculateVal)

        self.typeDataLabel = Label(FRAME4,font=('Times','11','bold'), text = '(A) Selected')
        self.typeDataLabel.grid(row=1,column=0,columnspan=2)    
        

        columns = 'PRAGMA table_info(%s)' %  self.selectedTable
        self.cursorspatial.execute(columns)
        results = self.cursorspatial.fetchall()
        self.tableListOrder = []

        self.tableInfoDic = {}
        for result in results:
            colname = result[1]
            self.tableInfoDic[colname] = result[2]
            self.tableList.insert(END,colname)
            self.tableListOrder.append(result[1])

        self.tableList.selection_set(0)
        
        FRAME2 = Frame(self.listboxFrame,  bg=self.backgroundcolor)
        FRAME2.grid(row=0,column=1,sticky=N+S,padx = 2,pady = 5, ipadx= 5)        
        self.scrollFieldbar = Scrollbar(FRAME2, orient=VERTICAL)

        self.fieldList = Listbox(FRAME2,height=10)
        self.fieldList.grid(row=0, column=0)
        self.fieldList.bind("<Double-Button-1>", addshpTypeInfo)
        self.scrollFieldbar.config(command=self.fieldList.yview)
        self.scrollFieldbar.grid(row=0,column=1, sticky=N+S)
        self.shapeLabel = Label(FRAME2,font=('Times','11','bold'), text = '(B) Shape Fields')
        self.shapeLabel.grid(row=1,column=0,columnspan=2)        
        fields = shpReader.fields
        self.shapeInfoDic = {}
        for result in fields:
            colname = result[0]
            if not colname =='DeletionFlag':
                self.shapeInfoDic[colname] = find_key(self.fieldTypes, result[1])
                self.fieldList.insert(END,colname)    
        self.fieldList.insert(END,'Geometry') 
        self.shapeInfoDic['Geometry'] = find_key(self.fieldTypes, shpReader.shapeType)
        
        FRAME5 = Frame(FRAME2,  bg=self.backgroundcolor) 
        FRAME5.grid(row=2,column=0,sticky=N+S,padx = 2,pady = 5)
        
        self.shpDataList = Listbox(FRAME5,selectmode=SINGLE,height=10)
        self.shpDataList.grid(row=0, column=0, )        
        self.shpDataList.bind("<Double-Button-1>", removeFromShpList)
        self.shpDataLabel = Label(FRAME5,font=('Times','11','bold'), text = '(B) Selected')
        self.shpDataLabel.grid(row=1,column=0,columnspan=2)    

        FRAME3 = Frame(self.listboxFrame,  bg=self.backgroundcolor)
        FRAME3.grid(row=0,column=2,sticky=N+S,padx = 2,pady = 5)    
        self.matchCanvas = Canvas(FRAME3,bg='white', width=400, height=400)
        self.matchCanvas.grid(row=0, column=0)
        matchText()

        BUTTONFRAME = Frame(self.sqlMainFrame,  bg=self.backgroundcolor)
        BUTTONFRAME.grid(row=1,column=0,sticky=N+E+W+S,padx = 2,pady = 5)
        generateButton = MatchButton(BUTTONFRAME,'Test\nMatches',generateMatches)
        generateButton.grid(row=0,column=0)
        sortButton = MatchButton(BUTTONFRAME,'Auto Sort\nFields',autoSort)
        sortButton.grid(row=0,column=1)
        ResetButton = MatchButton(BUTTONFRAME,'Reset\nFields',resets)
        ResetButton.grid(row=0,column=2)        
        RestartSHPButton = MatchButton(BUTTONFRAME,'Find New\nShapefile',restartSHP)
        RestartSHPButton.grid(row=1,column=1)   
        RestartButton = MatchButton(BUTTONFRAME,'Find New\nTable',restartTable)
        RestartButton.grid(row=1,column=0)    
        QuitButton = MatchButton(BUTTONFRAME,'Quit\nMatching',takeout)
        QuitButton.grid(row=1,column=2)  

        CHECKFRAME = Frame(BUTTONFRAME,  bg=self.backgroundcolor)
        CHECKFRAME.grid(row=0,column=3, rowspan=2, columnspan=2,sticky=N+E+W+S,padx = 2,pady = 5)
        
        SRIDFRAME  = Frame(CHECKFRAME,  bg=self.backgroundcolor,relief=GROOVE,bd=4)
        SRIDFRAME.grid(row=0,column=0,sticky=N+E+W+S,padx = 1,pady = 5)
        


        MODES = [
            ("State Plane Meters", "26943"),
            ("State Plane Feet", "2227"),
            ("UTM Zone 10 Meters", "26910"),
            ("Latitude/Longitude", "4326"),
        ]
    
        srid = StringVar()
         # initialize
        COUNTER = 0
        for  text, mode in MODES:
            b = Radiobutton(SRIDFRAME, text=text,  bg=self.backgroundcolor,
                            variable=srid,indicatoron =0,
                             value=mode, anchor='nw',
                             relief=GROOVE,
                             )
            
            b.grid(row=COUNTER,column=0,sticky=E+W)
            
            COUNTER +=1
        srid.set("26943")

        QUESTIONFRAME  = Frame(CHECKFRAME,  bg=self.backgroundcolor,relief=GROOVE,bd=4)
        QUESTIONFRAME.grid(row=0,column=1,sticky=N+E+W+S,padx = 1,pady = 5)
        
        GEO = IntVar()
        cGEO = Checkbutton(QUESTIONFRAME, text="Auto Acres/Feet", anchor='nw',variable=GEO)
        cGEO.grid(row=0,column=0,sticky=E+W)
        cGEO.select()

        PROPS = IntVar()
        cPROPS = Checkbutton(QUESTIONFRAME, text="Auto Add Property",anchor='nw', variable=PROPS)
        cPROPS.grid(row=1,column=0,sticky=E+W)        
        cPROPS.select()
        
        HMUS  = IntVar()
        cFKEYS = Checkbutton(QUESTIONFRAME, text="Add Mgmt. Unit",anchor='nw', variable=HMUS)
        cFKEYS.grid(row=2,column=0,sticky=E+W)      
        cFKEYS.select()
        
        GEOID = IntVar()
        
        cSRID = Checkbutton(QUESTIONFRAME, text="Auto ID",anchor='nw', variable=GEOID)
        cSRID.grid(row=3,column=0,sticky=E+W)        
        cSRID.select()
        ADDFRAME = Frame(BUTTONFRAME,  bg=self.backgroundcolor,relief=GROOVE,bd=4)
        ADDFRAME.grid(row=0,column=5, rowspan=2, columnspan=2,sticky=N+E+W+S,padx = 2,pady = 5)
        addButton = MatchButton(ADDFRAME,'Add\nData',addData)        
        undoButton = MatchButton(ADDFRAME,'Preview\nAdded Data',previewData)        
                
        
       
    
    def mapBaseGenerator(self ):
        self.imageMapWindow.canvas.delete('all')
        self.mapObjects = []
        table = self.searchBaseTable
        columns = "PRAGMA table_info(%s)" %  table
        self.cursorspatial.execute(columns)
        self.columns = self.cursorspatial.fetchall()
        fields  = ''

        if self.selectedTable in self.selectMetaGeoTables().values():
            fields = ''
            for COUNTER,column in enumerate(self.columns):
                field = self.searchBaseTable + '.'+column[1]
                if field == self.searchBaseTable + '.'+'Geometry':
                    field = 'AsText(Envelope(' +self.searchBaseTable + '.Geometry)),AsText('+ self.searchBaseTable + '.Geometry)'
                if COUNTER != (len(self.columns)-1):
                    
                    fields += field + ','
                else:
                    fields += field 
            sql = "SELECT DISTINCT {0} FROM {1}".format(fields,self.selectedTable)
        
        if self.searchIndicator !=0:
            sql += ','+ self.searchSearchTable  
        wheresql = " WHERE "      
        
        for COUNT, condition in enumerate(self.sqlconditionals):
            if COUNT != len(self.sqlconditionals)-1:
                wheresql += condition + ' AND '
            else:
                wheresql += condition
        
        if wheresql != " WHERE ":
            sql += wheresql
        if self.searchIndicator != 0:
            if wheresql != " WHERE ":
                sql += " AND " + self.searchSQL
            else:
                sql += " WHERE " + self.searchSQL
#
#        for COUNTER,column in enumerate(self.columns):
#                field = column[1]
#                if field == 'Geometry':
#                    field = 'AsText(Envelope(Geometry)),AsText(Geometry)'
#                    geomval = COUNTER
#                if COUNTER != (len(self.columns)-1):
#                    
#                    fields += field + ','
#                else:
#                    fields += field 
#        sql = "Select {0} FROM {1}".format(fields, table)
#        wheresql = " WHERE "
#        for COUNT, condition in enumerate(self.sqlconditionals):
#            if COUNT != len(self.sqlconditionals)-1:
#                wheresql += condition + ' AND '
#            else:
#                wheresql += condition
#        
#        if wheresql != " WHERE ":
#            sql += wheresql
#        if self.searchIndicator != 0:
#            sql += " AND " +self.searchSQL
        self.currentSQL = sql
        self.cursorspatial.execute(self.currentSQL)
        #self.retrievedData = self.cursorspatial.fetchall()
        #sql = self.sqlSelectGenerator()
        #self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()

        #selectSQL = 'SELECT  CCWD_PHOTOS.Property, CCWD_PHOTOS.Date, CCWD_PHOTOS.Filepath,AsText(Transform(CCWD_PHOTOS.Geometry, {0})) FROM CCWD_PHOTOS, {1} WHERE Intersects(Buffer({1}.Geometry, {2}), Transform(CCWD_PHOTOS.Geometry, {0}))'.format(self.srid, table, self.searchBufferVal)
        #self.cursorspatial.execute(selectSQL)
        #photoInfo = self.cursorspatial.fetchall()
        #pColumns = [ ('CCWD_PHOTOS','Date'), ('CCWD_PHOTOS','Filepath')]
        
        columns = self.columns
        infodic = {table:[columns,results]}
        self.mapObjects.append(infodic)
        
        #for COUNTER, dic in enumerate(self.mapObjects):
            
        values = infodic.values()[0][1]
        transList = []
        envelopeList = []
        for value in values:
            WKT = value[-1]
            transVals = self.polyTransform(WKT)
            transList.append(transVals)
            envelope = value[-2]
            envVals = self.polyTransform(envelope)
            envelopeList.append(envVals)
        infodic[table].append(transList)
        infodic[table].append(envelopeList)
        #infodic[table].append(pColumns)
        #infodic[table].append(photoInfo)
        return
    
    
    def curspatialExe(self,sql):
            self.cursorspatial.execute(sql)
            results = self.cursorspatial.fetchall()
            return results
        
    def polyTransform(self, geometry):
        'Transform well known text string into a list of coord pair float tuples'
        partsList = []
        if geometry.find('POINT')!= -1 :
            geom = geometry.split('(')[1].replace(')','')
            geomlist = map(float,geom.split())
            partsList = geomlist
        elif geometry.find('LINESTRING')!= -1:
            geom = geometry.split('(')[1].replace(')','')
            geomsplit = geom.split(', ')
            
            geomlist = []
            for COUNTER,geoms in enumerate(geomsplit):
                       
                xy = map(float,geoms.split())
                        
                geomlist.append(xy)
                
            partsList.append( geomlist)
        
        elif geometry.find('POLYGON')!= -1:   
            geom = geometry.split('((')[1].replace('))','')
            partSplit = geom.split('), (')
            for part in partSplit:
                geomlist = []
                geomsplit = part.split(', ')
                for COUNTER,geoms in enumerate(geomsplit):
                       
                        xy = map(float,geoms.split())
                        
                        geomlist.append(xy)
                partsList.append(geomlist)


        elif geometry.find('MULTIPOLYGON')!= -1:   
            geom = geometry.split('(((')[1].replace(')))','')
            partSplit = geom.split(')), ((')
            for part in partSplit:
                geomlist = []
                geomsplit = part.split('), (')
                for COUNTER,geoms in enumerate(geomsplit):
                    geolist = []
                    geoms.split(', ')
                    for geo in geoms:
                        xy = map(float,geoms.split())
                        
                        geomlist.append(xy)
                partsList.append(geomlist)

                
#        else: 
#            geom = geometry.split('((')[1].replace('))','')
#            partSplit = geom.split('), (')
#            for part in partSplit:
#                geomlist = []
#                geomsplit = part.split(', ')
#                for COUNTER,geoms in enumerate(geomsplit):
#                       
#                        xy = map(float,geoms.split())
#                        
#                        geomlist.append(xy)
#                partsList.append(geomlist)
                
        return partsList
     
    def mapMaxGenerator(self, MBRs):
        'determines maximum boundary of set of polygons'
        for mbrs in MBRs:
            if mbrs[0]> self.mapCoordMaxX:
                self.mapCoordMaxX =  mbrs[0]
            if mbrs[1]> self.mapCoordMaxY:     
                self.mapCoordMaxY =  mbrs[1]
            if mbrs[2]< self.mapCoordMinX:
                    self.mapCoordMinX = mbrs[2] 
            if mbrs[3]< self.mapCoordMinY:
                    self.mapCoordMinY = mbrs[3] 
                    
    def mapWidthGenerator(self):
        'determines maximum boundary of set of polygons'
        self.mapWidth = self.wInfo.mapcanvasWidth - self.mapWidthSpacer
        self.mapHeight = self.wInfo.mapcanvasHeight - self.mapHeightSpacer
        if self.mapWidth >= self.wInfo.mapcanvasHeight:
            stabilizer = self.mapHeight/float(self.mapWidth)
            self.currentCoordWidth = self.mapCoordMaxX - self.mapCoordMinX
            self.currentCoordHeight = (self.mapCoordMaxY - self.mapCoordMinY) * stabilizer
            self.mapCoordMinY = self.mapCoordMaxY - self.currentCoordHeight
        else:
            stabilizer = self.mapWidth/float(self.mapHeight)
            self.currentCoordWidth = (self.mapCoordMaxX - self.mapCoordMinX)* stabilizer
            self.currentCoordHeight = self.mapCoordMaxY - self.mapCoordMinY 
            self.mapCoordMaxX = self.mapCoordMinX +  - self.currentCoordWidth


        return

    def getMBRdata(self):
        minmaxSQl = 'SELECT MbrMinX(Geometry),MbrMinY(Geometry),MbrMaxX(Geometry),MbrMaxY(Geometry) FROM {0}'
        for data in self.mapObjects:
            sql = minmaxSQl.format(data.keys()[0])
            MBRlist = self.curspatialExe(sql)
            self.mapMaxGenerator(MBRlist)
        self.mapWidthGenerator()   

    def loadMap(self):
        'convert spatial coords to screen coords'
        self.getMBRdata()
        self.mapPolys = []
        #self.loadBaseLayerToScreen()
        self.tag = 'base'
        self.loadLayerToScreen(self.mapObjects)
        
    def loadSearchLayer(self):
        
        #self.loadSearchLayerToScreen()
        self.tag = 'search'
        self.loadLayerToScreen(self.mapSearchObjects)  
              

    
    
    def mapSearchGenerator(self):
        
        self.mapSearchObjects = []
        if self.searchSearchTable !='':
            table = self.searchSearchTable
            columns = "PRAGMA table_info(%s)" %  table
            self.cursorspatial.execute(columns)
            self.searchcolumns = self.cursorspatial.fetchall()
            fields  = ''
            for COUNTER,column in enumerate(self.searchcolumns):
                    field = column[1]
                    if field == 'Geometry':
                        field = 'AsText(Envelope(Geometry)),AsText(Geometry)'
                        geomval = COUNTER
                    if COUNTER != (len(self.searchcolumns)-1):
                        
                        fields += field + ','
                    else:
                        fields += field 
            sql = "Select {0} FROM {1}".format(fields, table)
            self.cursorspatial.execute(sql)
            results = self.cursorspatial.fetchall()
            #self.reviewSQLgenerator()
            #selectSQL = self.ImageSQL #'SELECT DISTINCT CCWD_PHOTOS.Date, CCWD_PHOTOS.Filepath,AsText(Transform(CCWD_PHOTOS.Geometry, {0})) FROM CCWD_PHOTOS, {1} WHERE Intersects(Buffer({1}.Geometry, {2}), Transform(CCWD_PHOTOS.Geometry, {0}))'.format(self.srid, table, self.searchBufferVal)
            #self.cursorspatial.execute(selectSQL)
            #photoInfo = self.cursorspatial.fetchall()
            
            #pColumns = [('CCWD_PHOTOS', 'Type'),('CCWD_PHOTOS', 'Monitor'),('CCWD_PHOTOS','Property'), ('CCWD_PHOTOS','Date'), ('CCWD_PHOTOS','Filepath')]
            
            columns = self.searchcolumns
            infodic = {table:[columns,results]}
            
            
            #for COUNTER, dic in enumerate(self.mapObjects):
                
            values = infodic.values()[0][1]
            transList = []
            envelopeList = []
            for value in values:
                WKT = value[-1]
                transVals = self.polyTransform(WKT)
                transList.append(transVals)
                envelope = value[-2]
                envVals = self.polyTransform(envelope)
                envelopeList.append(envVals)
            infodic[table].append(transList)
            infodic[table].append(envelopeList)
            #infodic[table].append(pColumns)
            #infodic[table].append(photoInfo)     
            self.mapSearchObjects.append(infodic)
        return  
                 

    def loadLayerToScreen(self, dic):


        for data in dic:
            table = data.keys()[0]
            dVals = data.values()
            attributes = dVals[0][1]
            columns = dVals[0][0]

            for column in columns:
                if column[1] == 'Geometry':
                    geomcol = column 
            if geomcol[2] == "LINESTRING" or geomcol[2] == "POLYGON":
                gvalues = dVals[0][2]
                eValues = dVals[0][3]
                #photos = dVals[0][-1]
                for COUNTER, value in enumerate(gvalues):
                    edata = eValues[COUNTER]
                    eGeoms = []
                    for geom in edata[0]:
                        exdist = geom[0]
                        eydist = geom[1]       
                        exposition = int((exdist/self.currentCoordWidth) * self.mapWidth) + (self.mapWidthSpacer/2)
                        eyposition = int((eydist/self.currentCoordHeight) * self.mapHeight) + (self.mapHeightSpacer/2)
                        eGeoms.append(exposition)
                        eGeoms.append(eyposition)  
                    for valCOUNT, geometry in enumerate(value):
                        transgeom = []
    
                        for geom in geometry:
                            xdist = geom[0] - self.mapCoordMinX
                            ydist = self.mapCoordMaxY - geom[1]
                            xposition = float((xdist/self.currentCoordWidth) * self.mapWidth) + (self.mapWidthSpacer/2)
                            yposition = float((ydist/self.currentCoordHeight) * self.mapHeight) + (self.mapHeightSpacer/2)
                            transgeom.append(xposition)
                            transgeom.append(yposition)    
                        

                        atts = attributes[COUNTER]
                        
                        if geomcol[2] == "LINESTRING":
                                    mapDisplay = self.geoLines(transgeom, geometry,atts,columns,   eGeoms)
                        elif geomcol[2] == "POLYGON":
                                    mapDisplay = self.geoPolys(transgeom, geometry,atts,columns,   eGeoms)

            elif geomcol[2] == "POINT":
                gvalues = dVals[0][2]
                for COUNTER, geom in enumerate(gvalues):
                        transgeom = []
                        xdist = geom[0] - self.mapCoordMinX
                        ydist = self.mapCoordMaxY - geom[1]
                        xposition = float((xdist/self.currentCoordWidth) * self.mapWidth) + (self.mapWidthSpacer/2)
                        yposition = float((ydist/self.currentCoordHeight) * self.mapHeight) + (self.mapHeightSpacer/2)
                        transgeom.append(xposition)
                        transgeom.append(yposition)  
                          
                        atts = attributes[COUNTER]
 
                        pointDisplay = self.geoPoints(transgeom, geom, atts,columns, )
                        
        return  


            

        
    def geoPoints(self, coords,scoords, attributes, columns,  ):
        if self.tag == 'base':
            ocolor = self.mapBaseOutlineColor 
            fcolor = self.mapBaseFillColor  
        else:
            ocolor = self.mapSearchOutlineColor 
            fcolor = self.mapSearchFillColor   

        if fcolor == ocolor:
            ocolor = self.colors[self.randcolor()]

        pointDisplay = PointsManager(self.imageMapWindow,coords, scoords, ocolor, attributes, columns,  )
        #self.toolTipManager.register(pointDisplay, 'test')
        class reportPoint(object):
            def __init__(self,root, poly, function):
                self.root= root
                #self.root.toolTipManager.register(poly, 'test')
                self.poly= poly
                self.function = function
                self.data = poly.attributes
            def execute(self, event):
                    self.function(self,self.attributes)
        self.imageMapWindow.canvas.itemconfig(pointDisplay.point, tags = ( self.tag))
        function = reportPoint(self, pointDisplay,self.loadSelected)
        self.imageMapWindow.canvas.tag_bind(pointDisplay.point, '<Enter>', function.execute)
        return pointDisplay

    def geoLines(self, coords,scoords, attributes, columns,  bbox):
        if self.tag == 'base':
            ocolor = self.mapBaseOutlineColor 
            fcolor = self.mapBaseFillColor  
        else:
            ocolor = self.mapSearchOutlineColor 
            fcolor = self.mapSearchFillColor   


        lineDisplay = LineManager(self.imageMapWindow,coords, scoords, ocolor, attributes, columns,  )
        #self.toolTipManager.register(lineDisplay, 'test')
        class reportLines(object):
            def __init__(self,root, poly, function):
                self.root= root
                #self.root.toolTipManager.register(poly, 'test')
                self.poly= poly
                self.function = function
                self.data = poly.data
            def execute(self, event):
                    self.function(self,self.data)
        self.imageMapWindow.canvas.itemconfig(lineDisplay, tags = ( self.tag))
        function = reportLines(self, lineDisplay,self.loadSelected)
        self.imageMapWindow.canvas.tag_bind(lineDisplay.line, '<Enter>', function.execute)
        return lineDisplay



    
    def geoPolys(self, coords,scoords, attributes, columns,  bbox):
        if self.tag == 'base':
            ocolor = self.mapBaseOutlineColor 
            fcolor = self.mapBaseFillColor  
        else:
            ocolor = self.mapSearchOutlineColor 
            fcolor = self.mapSearchFillColor              
            
        if fcolor == ocolor:
            ocolor = self.colors[self.randcolor()]

        polyDisplay = PolygonManager(self.imageMapWindow,coords, scoords, ocolor, fcolor,attributes, columns,  bbox)
        #self.toolTipManager.register(polyDisplay,'test')
        
        class reportPoly(object):
            def __init__(self,root, poly, function):
                self.root= root
                #self.root.toolTipManager.register(poly, 'test')
                self.poly= poly
                self.function = function
                self.data = poly.data
            def execute(self, event):

                    self.function(self,self.data)
        self.imageMapWindow.canvas.itemconfig(polyDisplay, tags = ( self.tag))
        function = reportPoly(self, polyDisplay,self.loadSelected)
        self.imageMapWindow.canvas.tag_bind(polyDisplay.polygon, '<Enter>', function.execute)
        #function2 = reportPoly(self, polyDisplay,polyDisplay.remove_tooltip)#self.loadSelected)
        #self.imageMapWindow.canvas.tag_bind(polyDisplay.polygon, '<B1-Motion>', function2.execute)
        
        return polyDisplay


    def loadSelected(self, root, data):
        oid =  data[0]
        self.table.setSelectedRow(oid)
        self.table.drawSelectedRow() 
        self.table.movetoSelectedRow(oid)
        
        #self.table.select_All()
#        dataDic = self.parseData(data, columns)
#        self.table.destroy()
#        if dataDic != {}:
#            self.tableframe= Frame(self.sideImageFrame,width= self.wInfo.tablecanvasWidth,  bd=3,relief='sunken',height =self.wInfo.tablecanvasHeight)
#            self.tableframe.grid(row=2,column=0, sticky= N+E+W+S)
#            self.table = TableCanvas(self.tableframe, newdict=dataDic, width= self.wInfo.imagecanvasWidth* .4, height =self.wInfo.imagecanvasWidth *.25  )
#            self.table.createTableFrame()  
#            self.table.bind('<Button-1>', self.loadClickedRow)


            

        
        

    def parseDataToTable(self,  features, columns):
        dataDic = {}
        valueRange = len(features)
        for i in range(1,valueRange+1):
            dataDic[str(i)] = {}
        for COUNTERX, column in enumerate(columns):
            header = column[1]
            for COUNTERY, value in enumerate(features):
                dataDic[str(COUNTERY+1)][header] = value[COUNTERX] 
        return dataDic    


    def randcolor(self):
        return random.randint(0,len(self.colors)-1)

    def graphGen(self, data):
        print data
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
            rect = self.imageGraphWindow.canvas.create_rectangle(x0, y0, x1, y1, fill="dark green")
            
            label = self.imageGraphWindow.canvas.create_text(x0+2, y0, anchor="sw", text=str(int(yorig * 0.000247105381)))
            #id = self.graph.canvas.create_text(x1+2, y1, anchor="sw", text=str(int(y)))
        
#        ylinebottom = c_height- y_gap + 5
#        ylinetop = c_height - ((c_height - 100)   + y_gap)
#        xlineleft = x_gap-5
#        xlineright = x1+5
#        self.graph.canvas.create_rectangle(xlineleft,ylinetop ,xlineleft,ylinebottom )
#        self.graph.canvas.create_rectangle(xlineleft,ylinebottom ,xlineright,ylinebottom )
#        title = self.graph.canvas.create_text((xlineright)/2, ylinebottom + 5, anchor="nw", text=str(title))
#        buttons = [self.graphButton,self.graphButton2 ]
#        for COUNTER,button in enumerate(buttons):
#            self.imageGraphWindow.canvas.create_window(self.wInfo.buttonSize * COUNTER + 10,
#                                            self.graph.heightIMap-self.wInfo.buttonSize, 
#                                            window=button,
#                                            anchor="nw")


        
"""
shapefile.py
Provides read and write support for ESRI Shapefiles.
author: jlawhead<at>geospatialpython.com
date: 20110921
version: 1.1.0
"""

from struct import pack, unpack, calcsize, error
import os
import time
import array
#
# Constants for shape types
NULL = 0
POINT = 1
POLYLINE = 3
POLYGON = 5
MULTIPOINT = 8
POINTZ = 11
POLYLINEZ = 13
POLYGONZ = 15
MULTIPOINTZ = 18
POINTM = 21
POLYLINEM = 23
POLYGONM = 25
MULTIPOINTM = 28
MULTIPATCH = 31

class _Array(array.array):
    """Converts python tuples to lists of the appropritate type.
    Used to unpack different shapefile header parts."""
    def __repr__(self):
        return str(self.tolist())

class _Shape:
    def __init__(self, shapeType=None):
        """Stores the geometry of the different shape types
        specified in the Shapefile spec. Shape types are
        usually point, polyline, or polygons. Every shape type
        except the "Null" type contains points at some level for
        example verticies in a polygon. If a shape type has
        multiple shapes containing points within a single
        geometry record then those shapes are called parts. Parts
        are designated by their starting index in geometry record's
        list of shapes."""
        self.shapeType = shapeType
        self.points = []

class _ShapeRecord:
    """A shape object of any type."""
    def __init__(self, shape=None, record=None):
        self.shape = shape
        self.record = record

class ShapefileException(Exception):
    """An exception to handle shapefile specific problems."""
    pass

class Reader:
    """Reads the three files of a shapefile as a unit or
    separately.  If one of the three files (.shp, .shx,
    .dbf) is missing no exception is thrown until you try
    to call a method that depends on that particular file.
    The .shx index file is used if available for efficiency
    but is not required to read the geometry from the .shp
    file. The "shapefile" argument in the constructor is the
    name of the file you want to open.

    You can instantiate a Reader without specifying a shapefile
    and then specify one later with the load() method.

    Only the shapefile headers are read upon loading. Content
    within each file is only accessed when required and as
    efficiently as possible. Shapefiles are usually not large
    but they can be.
    """
    def __init__(self, *args, **kwargs):
        self.shp = None
        self.shx = None
        self.dbf = None
        self.shapeName = "Not specified"
        self._offsets = []
        self.shpLength = None
        self.numRecords = None
        self.fields = []
        self.__dbfHdrLength = 0
        # See if a shapefile name was passed as an argument
        if len(args) > 0:
            if type(args[0]) is type("stringTest"):
                self.load(args[0])
                return
        if "shp" in kwargs.keys():
            if hasattr(kwargs["shp"], "read"):
                self.shp = kwargs["shp"]
                if hasattr(self.shp, "seek"):
                    self.shp.seek(0)
            if "shx" in kwargs.keys():
                if hasattr(kwargs["shx"], "read"):
                    self.shx = kwargs["shx"]
                    if hasattr(self.shx, "seek"):
                        self.shx.seek(0)
        if "dbf" in kwargs.keys():
            if hasattr(kwargs["dbf"], "read"):
                self.dbf = kwargs["dbf"]
                if hasattr(self.dbf, "seek"):
                    self.dbf.seek(0)
        if self.shp or self.dbf:        
            self.load()
        else:
            raise ShapefileException("Shapefile Reader requires a shapefile or file-like object.")

    def load(self, shapefile=None):
        """Opens a shapefile from a filename or file-like
        object. Normally this method would be called by the
        constructor with the file object or file name as an
        argument."""
        if shapefile:
            (shapeName, ext) = os.path.splitext(shapefile)
            self.shapeName = shapeName
            try:
                self.shp = file("%s.shp" % shapeName, "rb")
            except IOError:
                raise ShapefileException("Unable to open %s.shp" % shapeName)
            try:
                self.shx = file("%s.shx" % shapeName, "rb")
            except IOError:
                raise ShapefileException("Unable to open %s.shx" % shapeName)
            try:
                self.dbf = file("%s.dbf" % shapeName, "rb")
            except IOError:
                raise ShapefileException("Unable to open %s.dbf" % shapeName)
        if self.shp:
            self.__shpHeader()
        if self.dbf:
            self.__dbfHeader()

    def __getFileObj(self, f):
        """Checks to see if the requested shapefile file object is
        available. If not a ShapefileException is raised."""
        if not f:
            raise ShapefileException("Shapefile Reader requires a shapefile or file-like object.")
        if self.shp and self.shpLength is None:
            self.load()
        if self.dbf and len(self.fields) == 0:
            self.load()
        return f

    def __restrictIndex(self, i):
        """Provides list-like handling of a record index with a clearer
        error message if the index is out of bounds."""
        if self.numRecords:
            rmax = self.numRecords - 1
            if abs(i) > rmax:
                raise IndexError("Shape or Record index out of range.")
            if i < 0: i = range(self.numRecords)[i]
        return i

    def __shpHeader(self):
        """Reads the header information from a .shp or .shx file."""
        if not self.shp:
            raise ShapefileException("Shapefile Reader requires a shapefile or file-like object. (no shp file found")
        shp = self.shp
        # File length (16-bit word * 2 = bytes)
        shp.seek(24)
        self.shpLength = unpack(">i", shp.read(4))[0] * 2
        # Shape type
        shp.seek(32)
        self.shapeType= unpack("<i", shp.read(4))[0]
        # The shapefile's bounding box (lower left, upper right)
        self.bbox = _Array('d', unpack("<4d", shp.read(32)))
        # Elevation
        self.elevation = _Array('d', unpack("<2d", shp.read(16)))
        # Measure
        self.measure = _Array('d', unpack("<2d", shp.read(16)))

    def __shape(self):
        """Returns the header info and geometry for a single shape."""
        f = self.__getFileObj(self.shp)
        record = _Shape()
        nParts = nPoints = zmin = zmax = mmin = mmax = None
        (recNum, recLength) = unpack(">2i", f.read(8))
        shapeType = unpack("<i", f.read(4))[0]
        record.shapeType = shapeType
        # For Null shapes create an empty points list for consistency
        if shapeType == 0:
            record.points = []
        # All shape types capable of having a bounding box
        elif shapeType in (3,5,8,13,15,18,23,25,28,31):
            record.bbox = _Array('d', unpack("<4d", f.read(32)))
        # Shape types with parts
        if shapeType in (3,5,13,15,23,25,31):
            nParts = unpack("<i", f.read(4))[0]
        # Shape types with points
        if shapeType in (3,5,8,13,15,23,25,31):
            nPoints = unpack("<i", f.read(4))[0]
        # Read parts
        if nParts:
            record.parts = _Array('i', unpack("<%si" % nParts, f.read(nParts * 4)))
        # Read part types for Multipatch - 31
        if shapeType == 31:
            record.partTypes = _Array('i', unpack("<%si" % nParts, f.read(nParts * 4)))
        # Read points - produces a list of [x,y] values
        if nPoints:
            record.points = [_Array('d', unpack("<2d", f.read(16))) for p in range(nPoints)]
        # Read z extremes and values
        if shapeType in (13,15,18,31):
            (zmin, zmax) = unpack("<2d", f.read(16))
            record.z = _Array('d', unpack("<%sd" % nPoints, f.read(nPoints * 8)))
        # Read m extremes and values
        if shapeType in (13,15,18,23,25,28,31):
            (mmin, mmax) = unpack("<2d", f.read(16))
            # Measure values less than -10e38 are nodata values according to the spec
            record.m = [m if m > -10e38 else None for m in _Array('d', unpack("%sd" % nPoints, f.read(nPoints * 8)))]
        # Read a single point
        if shapeType in (1,11,21):
            record.points = [_Array('d', unpack("<2d", f.read(16)))]
        # Read a single Z value
        if shapeType == 11:
            record.z = unpack("<d", f.read(8))
        # Read a single M value
        if shapeType in (11,21):
            record.m = unpack("<d", f.read(8))
        return record

    def __shapeIndex(self, i=None):
        """Returns the offset in a .shp file for a shape based on information
        in the .shx index file."""
        shx = self.shx
        if not shx:
            return None
        if not self._offsets:
            # File length (16-bit word * 2 = bytes) - header length
            shx.seek(24)
            shxRecordLength = (unpack(">i", shx.read(4))[0] * 2) - 100
            numRecords = shxRecordLength / 8
            # Jump to the first record.
            shx.seek(100)
            for r in range(numRecords):
                # Offsets are 16-bit words just like the file length
                self._offsets.append(unpack(">i", shx.read(4))[0] * 2)
                shx.seek(shx.tell() + 4)
        if not i == None:
            return self._offsets[i]

    def shape(self, i=0):
        """Returns a shape object for a shape in the the geometry
        record file."""
        shp = self.__getFileObj(self.shp)
        i = self.__restrictIndex(i)
        offset = self.__shapeIndex(i)
        if not offset:
            # Shx index not available so use the full list.
            shapes = self.shapes()
            return shapes[i]
        shp.seek(offset)
        return self.__shape()

    def shapes(self):
        """Returns all shapes in a shapefile."""
        shp = self.__getFileObj(self.shp)
        shp.seek(100)
        shapes = []
        while shp.tell() < self.shpLength:
            shapes.append(self.__shape())
        return shapes

    def __dbfHeaderLength(self):
        """Retrieves the header length of a dbf file header."""
        if not self.__dbfHdrLength:
            if not self.dbf:
                raise ShapefileException("Shapefile Reader requires a shapefile or file-like object. (no dbf file found)")
            dbf = self.dbf
            (self.numRecords, self.__dbfHdrLength) = \
                    unpack("<xxxxLH22x", dbf.read(32))
        return self.__dbfHdrLength

    def __dbfHeader(self):
        """Reads a dbf header. Xbase-related code borrows heavily from ActiveState Python Cookbook Recipe 362715 by Raymond Hettinger"""
        if not self.dbf:
            raise ShapefileException("Shapefile Reader requires a shapefile or file-like object. (no dbf file found)")
        dbf = self.dbf
        headerLength = self.__dbfHeaderLength()
        numFields = (headerLength - 33) // 32
        for field in range(numFields):
            fieldDesc = list(unpack("<11sc4xBB14x", dbf.read(32)))
            name = 0
            idx = 0
            if "\x00" in fieldDesc[name]:
                idx = fieldDesc[name].index("\x00")
            else:
                idx = len(fieldDesc[name]) - 1
            fieldDesc[name] = fieldDesc[name][:idx]
            fieldDesc[name] = fieldDesc[name].lstrip()
            self.fields.append(fieldDesc)
        terminator = dbf.read(1)
        assert terminator == "\r"
        self.fields.insert(0, ('DeletionFlag', 'C', 1, 0))

    def __recordFmt(self):
        """Calculates the size of a .shp geometry record."""
        if not self.numRecords:
            self.__dbfHeader()
        fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in self.fields])
        fmtSize = calcsize(fmt)
        return (fmt, fmtSize)

    def __record(self):
        """Reads and returns a dbf record row as a list of values."""
        f = self.__getFileObj(self.dbf)
        recFmt = self.__recordFmt()
        recordContents = unpack(recFmt[0], f.read(recFmt[1]))
        if recordContents[0] != ' ':
            # deleted record
            return None
        record = []
        for (name, typ, size, deci), value in zip(self.fields,
                                                                                                recordContents):
            if name == 'DeletionFlag':
                continue
            elif not value.strip():
                record.append(value)
                continue
            elif typ == "N":
                value = value.replace('\0', '').strip()
                if value == '':
                    value = 0
                elif deci:
                    value = float(value)
                else:
                    value = int(value)
            elif typ == 'D':
                try:
                    y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                    value = [y, m, d]
                except:
                    value = value.strip()
            elif typ == 'L':
                value = (value in 'YyTt' and 'T') or \
                                        (value in 'NnFf' and 'F') or '?'
            else:
                value = value.strip()
            record.append(value)
        return record

    def record(self, i=0):
        """Returns a specific dbf record based on the supplied index."""
        f = self.__getFileObj(self.dbf)
        if not self.numRecords:
            self.__dbfHeader()
        i = self.__restrictIndex(i)
        recSize = self.__recordFmt()[1]
        f.seek(0)
        f.seek(self.__dbfHeaderLength() + (i * recSize))
        return self.__record()

    def records(self):
        """Returns all records in a dbf file."""
        if not self.numRecords:
            self.__dbfHeader()
        records = []
        f = self.__getFileObj(self.dbf)
        f.seek(self.__dbfHeaderLength())
        for i in xrange(self.numRecords):
            r = self.__record()
            if r:
                records.append(r)
        return records

    def shapeRecord(self, i=0):
        """Returns a combination geometry and attribute record for the
        supplied record index."""
        i = self.__restrictIndex(i)
        return _ShapeRecord(shape=self.shape(i),
                                                        record=self.record(i))

    def shapeRecords(self):
        """Returns a list of combination geometry/attribute records for
        all records in a shapefile."""
        shapeRecords = []
        return [_ShapeRecord(shape=rec[0], record=rec[1]) \
                                for rec in zip(self.shapes(), self.records())]

class Writer:
    """Provides write support for ESRI Shapefiles."""
    def __init__(self, shapeType=None):
        self._shapes = []
        self.fields = []
        self.records = []
        self.shapeType = shapeType
        self.shp = None
        self.shx = None
        self.dbf = None
        # Geometry record offsets and lengths for writing shx file.
        self._offsets = []
        self._lengths = []
        # Use deletion flags in dbf? Default is false (0).
        self.deletionFlag = 0

    def __getFileObj(self, f):
        """Safety handler to verify file-like objects"""
        if not f:
            raise ShapefileException("No file-like object available.")
        elif hasattr(f, "write"):
            return f
        else:
            pth = os.path.split(f)[0]
            if pth and not os.path.exists(pth):
                os.makedirs(pth)
            return file(f, "wb")

    def __shpFileLength(self):
        """Calculates the file length of the shp file."""
        # Start with header length
        size = 100
        # Calculate size of all shapes
        for s in self._shapes:
            # Add in record header and shape type fields
            size += 12
            # nParts and nPoints do not apply to all shapes
            #if self.shapeType not in (0,1):
            #       nParts = len(s.parts)
            #       nPoints = len(s.points)
            if hasattr(s,'parts'):
                nParts = len(s.parts)
            if hasattr(s,'points'):
                nPoints = len(s.points)
            # All shape types capable of having a bounding box
            if self.shapeType in (3,5,8,13,15,18,23,25,28,31):
                size += 32
            # Shape types with parts
            if self.shapeType in (3,5,13,15,23,25,31):
                # Parts count
                size += 4
                # Parts index array
                size += nParts * 4
            # Shape types with points
            if self.shapeType in (3,5,8,13,15,23,25,31):
                # Points count
                size += 4
                # Points array
                size += 16 * nPoints
            # Calc size of part types for Multipatch (31)
            if self.shapeType == 31:
                size += nParts * 4
            # Calc z extremes and values
            if self.shapeType in (13,15,18,31):
                # z extremes
                size += 16
                # z array
                size += 8 * nPoints
            # Calc m extremes and values
            if self.shapeType in (23,25,31):
                # m extremes
                size += 16
                # m array
                size += 8 * nPoints
            # Calc a single point
            if self.shapeType in (1,11,21):
                size += 16
            # Calc a single Z value
            if self.shapeType == 11:
                size += 8
            # Calc a single M value
            if self.shapeType in (11,21):
                size += 8
        # Calculate size as 16-bit words
        size /= 2
        return size

    def __bbox(self, shapes, shapeTypes=[]):
        x = []
        y = []
        for s in shapes:
            shapeType = self.shapeType
            if shapeTypes:
                shapeType = shapeTypes[shapes.index(s)]
            px, py = zip(*s.points)[:2]
            x.extend(px)
            y.extend(py)
        return [min(x), min(y), max(x), max(y)]

    def __zbox(self, shapes, shapeTypes=[]):
        z = []
        for s in shapes:
            try:
                for p in s.points:
                    z.append(p[2])
            except IndexError:
                pass
        if not z: z.append(0)
        return [min(z), max(z)]

    def __mbox(self, shapes, shapeTypes=[]):
        m = [0]
        for s in shapes:
            try:
                for p in s.points:
                    m.append(p[3])
            except IndexError:
                pass
        return [min(m), max(m)]

    def bbox(self):
        """Returns the current bounding box for the shapefile which is
        the lower-left and upper-right corners. It does not contain the
        elevation or measure extremes."""
        return self.__bbox(self._shapes)

    def zbox(self):
        """Returns the current z extremes for the shapefile."""
        return self.__zbox(self._shapes)

    def mbox(self):
        """Returns the current m extremes for the shapefile."""
        return self.__mbox(self._shapes)

    def __shapefileHeader(self, fileObj, headerType='shp'):
        """Writes the specified header type to the specified file-like object.
        Several of the shapefile formats are so similar that a single generic
        method to read or write them is warranted."""
        f = self.__getFileObj(fileObj)
        f.seek(0)
        # File code, Unused bytes
        f.write(pack(">6i", 9994,0,0,0,0,0))
        # File length (Bytes / 2 = 16-bit words)
        if headerType == 'shp':
            f.write(pack(">i", self.__shpFileLength()))
        elif headerType == 'shx':
            f.write(pack('>i', ((100 + (len(self._shapes) * 8)) / 2)))
        # Version, Shape type
        f.write(pack("<2i", 1000, self.shapeType))
        # The shapefile's bounding box (lower left, upper right)
        if self.shapeType != 0:
            try:
                f.write(pack("<4d", *self.bbox()))
            except error:
                raise ShapefileException("Failed to write shapefile bounding box. Floats required.")
        else:
            f.write(pack("<4d", 0,0,0,0))
        # Elevation
        z = self.zbox()
        # Measure
        m = self.mbox()
        try:
            f.write(pack("<4d", z[0], z[1], m[0], m[1]))
        except error:
            raise ShapefileException("Failed to write shapefile elevation and measure values. Floats required.")

    def __dbfHeader(self):
        """Writes the dbf header and field descriptors."""
        f = self.__getFileObj(self.dbf)
        f.seek(0)
        version = 3
        year, month, day = time.localtime()[:3]
        year -= 1900
        # Remove deletion flag placeholder from fields
        for field in self.fields:
            if field[0].startswith("Deletion"):
                self.fields.remove(field)
        numRecs = len(self.records)
        numFields = len(self.fields)
        headerLength = numFields * 32 + 33
        recordLength = sum([int(field[2]) for field in self.fields]) + 1
        header = pack('<BBBBLHH20x', version, year, month, day, numRecs,
                headerLength, recordLength)
        f.write(header)
        # Field descriptors
        for field in self.fields:
            name, fieldType, size, decimal = field
            name = name.replace(' ', '_')
            name = name.ljust(11).replace(' ', '\x00')
            size = int(size)
            fld = pack('<11sc4xBB14x', name, fieldType, size, decimal)
            f.write(fld)
        # Terminator
        f.write('\r')

    def __shpRecords(self):
        """Write the shp records"""
        f = self.__getFileObj(self.shp)
        f.seek(100)
        recNum = 1
        for s in self._shapes:
            self._offsets.append(f.tell())
            # Record number, Content length place holder
            f.write(pack(">2i", recNum, 0))
            recNum += 1
            start = f.tell()
            # Shape Type
            f.write(pack("<i", s.shapeType))
            # All shape types capable of having a bounding box
            if s.shapeType in (3,5,8,13,15,18,23,25,28,31):
                try:
                    f.write(pack("<4d", *self.__bbox([s])))
                except error:
                    raise ShapefileException("Falied to write bounding box for record %s. Expected floats." % recNum)
            # Shape types with parts
            if s.shapeType in (3,5,13,15,23,25,31):
                # Number of parts
                f.write(pack("<i", len(s.parts)))
            # Shape types with multiple points per record
            if s.shapeType in (3,5,8,13,15,23,25,31):
                # Number of points
                f.write(pack("<i", len(s.points)))
            # Write part indexes
            if s.shapeType in (3,5,13,15,23,25,31):
                for p in s.parts:
                    f.write(pack("<i", p))
            # Part types for Multipatch (31)
            if s.shapeType == 31:
                for pt in s.partTypes:
                    f.write(pack("<i", pt))
            # Write points for multiple-point records
            if s.shapeType in (3,5,8,13,15,23,25,31):
                try:
                    [f.write(pack("<2d", *p[:2])) for p in s.points]
                except error:
                    raise ShapefileException("Failed to write points for record %s. Expected floats." % recNum)
            # Write z extremes and values
            if s.shapeType in (13,15,18,31):
                try:
                    f.write(pack("<2d", *self.__zbox([s])))
                except error:
                    raise ShapefileException("Failed to write elevation extremes for record %s. Expected floats." % recNum)
                try:
                    [f.write(pack("<d", p[2])) for p in s.points]
                except error:
                    raise ShapefileException("Failed to write elevation values for record %s. Expected floats." % recNum)
            # Write m extremes and values
            if s.shapeType in (23,25,31):
                try:
                    f.write(pack("<2d", *self.__mbox([s])))
                except error:
                    raise ShapefileException("Failed to write measure extremes for record %s. Expected floats" % recNum)
                try:
                    [f.write(pack("<d", p[3])) for p in s.points]
                except error:
                    raise ShapefileException("Failed to write measure values for record %s. Expected floats" % recNum)
            # Write a single point
            if s.shapeType in (1,11,21):
                try:
                    f.write(pack("<2d", s.points[0][0], s.points[0][1]))
                except error:
                    raise ShapefileException("Failed to write point for record %s. Expected floats." % recNum)
            # Write a single Z value
            if s.shapeType == 11:
                try:
                    f.write(pack("<1d", s.points[0][2]))
                except error:
                    raise ShapefileException("Failed to write elevation value for record %s. Expected floats." % recNum)
            # Write a single M value
            if s.shapeType in (11,21):
                try:
                    f.write(pack("<1d", s.points[0][3]))
                except error:
                    raise ShapefileException("Failed to write measure value for record %s. Expected floats." % recNum)
            # Finalize record length as 16-bit words
            finish = f.tell()
            length = (finish - start) / 2
            self._lengths.append(length)
            # start - 4 bytes is the content length field
            f.seek(start-4)
            f.write(pack(">i", length))
            f.seek(finish)

    def __shxRecords(self):
        """Writes the shx records."""
        f = self.__getFileObj(self.shx)
        f.seek(100)
        for i in range(len(self._shapes)):
            f.write(pack(">i", self._offsets[i]/2))
            f.write(pack(">i", self._lengths[i]))

    def __dbfRecords(self):
        """Writes the dbf records."""
        f = self.__getFileObj(self.dbf)
        for record in self.records:
            if not self.fields[0][0].startswith("Deletion"):
                f.write(' ') # deletion flag
            for (fieldName, fieldType, size, dec), value in zip(self.fields, record):
                fieldType = fieldType.upper()
                size = int(size)
                if fieldType.upper() == "N":
                    value = str(value).rjust(size)
                elif fieldType == 'L':
                    value = str(value)[0].upper()
                else:
                    value = str(value)[:size].ljust(size)
                assert len(value) == size
                f.write(value)

    def null(self):
        """Creates a null shape."""
        self._shapes.append(_Shape(NULL))

    def point(self, x, y, z=0, m=0):
        """Creates a point shape."""
        pointShape = _Shape(self.shapeType)
        pointShape.points.append([x, y, z, m])
        self._shapes.append(pointShape)

    def line(self, parts=[], shapeType=POLYLINE):
        """Creates a line shape. This method is just a convienience method
        which wraps 'poly()'.
        """
        self.poly(parts, shapeType, [])

    def poly(self, parts=[], shapeType=POLYGON, partTypes=[]):
        """Creates a shape that has multiple collections of points (parts)
        including lines, polygons, and even multipoint shapes. If no shape type
        is specified it defaults to 'polygon'. If no part types are specified
        (which they normally won't be) then all parts default to the shape type.
        """
        polyShape = _Shape(shapeType)
        polyShape.parts = []
        polyShape.points = []
        for part in parts:
            polyShape.parts.append(len(polyShape.points))
            for point in part:
                # Ensure point is list
                if not isinstance(point, list):
                    point = list(point)
                # Make sure point has z and m values
                while len(point) < 4:
                    point.append(0)
                polyShape.points.append(point)
            
        if polyShape.shapeType == 31:
            if not partTypes:
                for part in parts:
                    partTypes.append(polyShape.shapeType)
            polyShape.partTypes = partTypes
        self._shapes.append(polyShape)

    def field(self, name, fieldType="C", size="50", decimal=0):
        """Adds a dbf field descriptor to the shapefile."""
        self.fields.append((name, fieldType, size, decimal))

    def record(self, *recordList, **recordDict):
        """Creates a dbf attribute record. You can submit either a sequence of
        field values or keyword arguments of field names and values. Before
        adding records you must add fields for the record values using the
        fields() method. If the record values exceed the number of fields the
        extra ones won't be added. In the case of using keyword arguments to specify
        field/value pairs only fields matching the already registered fields
        will be added."""
        record = []
        fieldCount = len(self.fields)
        # Compensate for deletion flag
        if self.fields[0][0].startswith("Deletion"): fieldCount -= 1
        if recordList:
            [record.append(recordList[i]) for i in range(fieldCount)]
        elif recordDict:
            for field in self.fields:
                if recordDict.has_key(field[0]):
                    val = recordDict[field[0]]
                    if val:
                        record.append(val)
                    else:
                        record.append("")
        if record:
            self.records.append(record)

    def shape(self, i):
        return self._shapes[i]

    def shapes(self):
        """Return the current list of shapes."""
        return self._shapes

    def saveShp(self, target):
        """Save an shp file."""
        if not hasattr(target, "write"):
            target = os.path.splitext(target)[0] + '.shp'
        if not self.shapeType:
            self.shapeType = self._shapes[0].shapeType
        self.shp = self.__getFileObj(target)
        self.__shapefileHeader(self.shp, headerType='shp')
        self.__shpRecords()

    def saveShx(self, target):
        """Save an shx file."""
        if not hasattr(target, "write"):
            target = os.path.splitext(target)[0] + '.shx'
        if not self.shapeType:
            self.shapeType = self._shapes[0].shapeType
        self.shx = self.__getFileObj(target)
        self.__shapefileHeader(self.shx, headerType='shx')
        self.__shxRecords()

    def saveDbf(self, target):
        """Save a dbf file."""
        if not hasattr(target, "write"):
            target = os.path.splitext(target)[0] + '.dbf'
        self.dbf = self.__getFileObj(target)
        self.__dbfHeader()
        self.__dbfRecords()

    def save(self, target=None, shp=None, shx=None, dbf=None):
        """Save the shapefile data to three files or
        three file-like objects. SHP and DBF files can also
        be written exclusively using saveShp, saveShx, and saveDbf respectively."""
        # TODO: Create a unique filename for target if None.
        if shp:
            self.saveShp(shp)
        if shx:
            self.saveShx(shx)
        if dbf:
            self.saveDbf(dbf)
        elif target:
            self.saveShp(target)
            self.shp.close()
            self.saveShx(target)
            self.shx.close()
            self.saveDbf(target)
            self.dbf.close()

class Editor(Writer):
    def __init__(self, shapefile=None, shapeType=POINT, autoBalance=1):
        self.autoBalance = autoBalance
        if not shapefile:
            Writer.__init__(self, shapeType)
        elif isinstance(shapefile, basestring):
            base = os.path.splitext(shapefile)[0]
            if os.path.isfile("%s.shp" % base):
                r = Reader(base)
                Writer.__init__(self, r.shapeType)
                self._shapes = r.shapes()
                self.fields = r.fields
                self.records = r.records()

    def select(self, expr):
        """Select one or more shapes (to be implemented)"""
        # TODO: Implement expressions to select shapes.
        pass

    def delete(self, shape=None, part=None, point=None):
        """Deletes the specified part of any shape by specifying a shape
        number, part number, or point number."""
        # shape, part, point
        if shape and part and point:
            del self._shapes[shape][part][point]
        # shape, part
        elif shape and part and not point:
            del self._shapes[shape][part]
        # shape
        elif shape and not part and not point:
            del self._shapes[shape]
        # point
        elif not shape and not part and point:
            for s in self._shapes:
                if s.shapeType == 1:
                    del self._shapes[point]
                else:
                    for part in s.parts:
                        del s[part][point]
        # part, point
        elif not shape and part and point:
            for s in self._shapes:
                del s[part][point]
        # part
        elif not shape and part and not point:
            for s in self._shapes:
                del s[part]

    def point(self, x=None, y=None, z=None, m=None, shape=None, part=None, point=None, addr=None):
        """Creates/updates a point shape. The arguments allows
        you to update a specific point by shape, part, point of any
        shape type."""
        # shape, part, point
        if shape and part and point:
            try: self._shapes[shape]
            except IndexError: self._shapes.append([])
            try: self._shapes[shape][part]
            except IndexError: self._shapes[shape].append([])
            try: self._shapes[shape][part][point]
            except IndexError: self._shapes[shape][part].append([])
            p = self._shapes[shape][part][point]
            if x: p[0] = x
            if y: p[1] = y
            if z: p[2] = z
            if m: p[3] = m
            self._shapes[shape][part][point] = p
        # shape, part
        elif shape and part and not point:
            try: self._shapes[shape]
            except IndexError: self._shapes.append([])
            try: self._shapes[shape][part]
            except IndexError: self._shapes[shape].append([])
            points = self._shapes[shape][part]
            for i in range(len(points)):
                p = points[i]
                if x: p[0] = x
                if y: p[1] = y
                if z: p[2] = z
                if m: p[3] = m
                self._shapes[shape][part][i] = p
        # shape
        elif shape and not part and not point:
            try: self._shapes[shape]
            except IndexError: self._shapes.append([])

        # point
        # part
        if addr:
            shape, part, point = addr
            self._shapes[shape][part][point] = [x, y, z, m]
        else:
            Writer.point(self, x, y, z, m)
        if self.autoBalance:
            self.balance()

    def validate(self):
        """An optional method to try and validate the shapefile
        as much as possible before writing it (not implemented)."""
        #TODO: Implement validation method
        pass

    def balance(self):
        """Adds a corresponding empty attribute or null geometry record depending
        on which type of record was created to make sure all three files
        are in synch."""
        if len(self.records) > len(self._shapes):
            self.null()
        elif len(self.records) < len(self._shapes):
            self.record()

    def __fieldNorm(self, fieldName):
        """Normalizes a dbf field name to fit within the spec and the
        expectations of certain ESRI software."""
        if len(fieldName) > 11: fieldName = fieldName[:11]
        fieldName = fieldName.upper()
        fieldName.replace(' ', '_')

#This string is a KML script called to produce polygons representing the selected parcels. 
#polykml= '''<?xml version="1.0" encoding="UTF-8"?>
#<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
#<Document>
#<name>%s</name>
#<Style id="sn_ylw-pushpin">
#    <IconStyle>
#        <scale>1.1</scale>
#        <Icon>
#            <href>pushpin.png</href>
#        </Icon>
#        <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
#    </IconStyle>
#</Style>
#<Style id="sn_ylw-pushpin0">
#    <IconStyle>
#        <scale>1.1</scale>
#        <Icon>
#            <href>pushpin.png</href>
#        </Icon>
#        <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
#    </IconStyle>
#    <LineStyle>
#        <color>#ff0000ff</color>
#        <width>6</width>
#    </LineStyle>
#    <PolyStyle>
#        <fill>0</fill>
#    </PolyStyle>
#</Style>
#<StyleMap id="msn_ylw-pushpin">
#    <Pair>
#        <key>normal</key>
#        <styleUrl>#sn_ylw-pushpin</styleUrl>
#    </Pair>
#    <Pair>
#        <key>highlight</key>
#        <styleUrl>#sh_ylw-pushpin0</styleUrl>
#    </Pair>
#</StyleMap>
#<StyleMap id="msn_ylw-pushpin0">
#    <Pair>
#        <key>normal</key>
#        <styleUrl>#sn_ylw-pushpin0</styleUrl>
#    </Pair>
#    <Pair>
#        <key>highlight</key>
#        <styleUrl>#sh_ylw-pushpin</styleUrl>
#    </Pair>
#</StyleMap>
#<Style id="sh_ylw-pushpin">
#    <IconStyle>
#        <scale>1.3</scale>
#        <Icon>
#            <href>pushpin.png</href>
#        </Icon>
#        <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
#    </IconStyle>
#
#    <PolyStyle>
#        <fill>0</fill>
#    </PolyStyle>
#</Style>
#<Style id="sh_ylw-pushpin0">
#    <IconStyle>
#        <scale>1.3</scale>
#        <Icon>
#            <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
#        </Icon>
#        <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
#    </IconStyle>
#</Style>
#
#%s
#
#</Document>
#</kml>
#'''
polykml =  '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>%s</name>
        <Style id="hl">
        <IconStyle>
            <scale>1.2</scale>
        </IconStyle>
        <LineStyle>
            <color>ffffffff</color>
            <colorMode>random</colorMode>
        </LineStyle>
        <PolyStyle>
            <color>ffffffff</color>
            <colorMode>random</colorMode>
        </PolyStyle>
    </Style>
    <Style id="default">
        <LineStyle>
            <color>ffffffff</color>
            <colorMode>random</colorMode>
        </LineStyle>
        <PolyStyle>
            <color>ffffffff</color>
            <colorMode>random</colorMode>
        </PolyStyle>
    </Style>
    %s
</Document>
</kml>
'''


           