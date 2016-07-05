#from CCWD.models import *
#from CCWD.views import *
from Tkinter import *
from managers import *
import os, random, ttk,tkSimpleDialog,shutil,tkMessageBox, tkFileDialog
import calendar, datetime, Tkinter,pyexiv2
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing,_DrawingEditorMixin,String
from reportlab.graphics.samples.excelcolors import color05,color06,color02,color01  ,color02,color03,color04,color05,color06,color07,color08,color09, color10
from reportlab.lib.units import cm, mm, inch
from reportlab.pdfgen.canvas import Canvas as rlCanvas
from reportlab.graphics.widgetbase import Widget,TypedPropertyCollection
from reportlab.lib import colors
import getpass
import time, random,tkColorChooser
import xlwt, xlrd
from Tables_adjusted import TableCanvas
from tkintertable.TableModels import TableModel
from shapefile import Reader, Writer


from PIL import Image, ImageTk
from PIL.ExifTags import TAGS

from shapely import wkt
from pyPdf import PdfFileWriter, PdfFileReader 

def generatePRJ(SRID= 26943):
    if SRID == 26943:
        prj =  'PROJCS["NAD83 / California zone 3",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Lambert_Conformal_Conic_2SP"],PARAMETER["standard_parallel_1",38.43333333333333],PARAMETER["standard_parallel_2",37.06666666666667],PARAMETER["latitude_of_origin",36.5],PARAMETER["central_meridian",-120.5],PARAMETER["false_easting",2000000],PARAMETER["false_northing",500000],AUTHORITY["EPSG","26943"],AXIS["X",EAST],AXIS["Y",NORTH]]'
    elif SRID == 26910:
        prj = 'PROJCS["NAD83 / UTM zone 10N",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-123],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],AUTHORITY["EPSG","26910"],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
    elif SRID == 4326:
        #prj = 'PROJCS["NAD83 / UTM zone 10N",GEOGCS["NAD83",DATUM["North_American_Datum_1983",SPHEROID["GRS 1980",6378137,298.257222101,AUTHORITY["EPSG","7019"]],AUTHORITY["EPSG","6269"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.01745329251994328,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4269"]],UNIT["metre",1,AUTHORITY["EPSG","9001"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",-123],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],AUTHORITY["EPSG","26910"],AXIS["Easting",EAST],AXIS["Northing",NORTH]]'
        pass
    return prj

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


def groups(glist, numPerGroup=2):
    result = []

    i = 0
    cur = []
    for item in glist:
        if not i < numPerGroup:
            result.append(cur)
            cur = []
            i = 0

        cur.append(item)
        i += 1

    if cur:
        result.append(cur)

    return result

def average(points):
    aver = [0,0]
    
    for point in points:
        aver[0] += point[0]
        aver[1] += point[1]
        
    return aver[0]/len(points), aver[1]/len(points)

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


def imagePDF2(path, ptext,  pdfname = 'PDF.pdf'):
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch  
    
    imageprocessor = ImageProcessorPDF(path)

    if imageprocessor.dim == 'width':
        dim2 = 5
        dim1 = dim2 * (float(imageprocessor.boundingBox[2])/imageprocessor.boundingBox[3])
    else:
        dim1 = 5
        dim2 = dim1 * (float(imageprocessor.boundingBox[3])/imageprocessor.boundingBox[2])        
    
    doc = SimpleDocTemplate(pdfname,pagesize=letter,
                        rightMargin=72,leftMargin=72,
                        topMargin=72,bottomMargin=18)      
    Story=[]
    
    im = Image(path, dim1*inch, dim2 *inch)
    Story.append(im)
    for text in ptext:
        Story.append(Paragraph(text, ParagraphStyle('body')))
    
    doc.build(Story)

def saveSHP(root):
        import tkFileDialog
        shp = tkFileDialog.asksaveasfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Save the Shapefile',initialfile='.shp',
                                                  filetypes=[('ESRI Shapefile', '*.shp')])
        
        return shp



def saveCSV(root):
        import tkFileDialog
        csv = tkFileDialog.asksaveasfilename(parent=root,
                                                  initialdir='C:/',
                                                  title='Save a Spreadsheet',defaultextension='.xls',
                                                  filetypes=[
                                                             ("Spreadsheets", ("*.xls")),
                                                             ])
        
        ##print csv    
        return csv

def savePDF():
        from Tkinter import Tk
    
        import tkFileDialog
        master = Tk()
        master.withdraw()
        pdf = tkFileDialog.asksaveasfilename(parent=master,
                                                  initialdir='C:/',
                                                  title='Save the PDF',initialfile='.pdf',
                                                  filetypes=[('PDF', '*.pdf')])
        master.destroy()
        return pdf.split('.')[0] + '.pdf'


def saveKML(master):

        kml = tkFileDialog.asksaveasfilename(parent=master,
                                                  initialdir='C:/',
                                                  title='Save the KML',defaultextension='.kml',
                                                  filetypes=[('Keyhole Markup Language', '*.kml')])
        master.destroy()
        return kml.split('.')[0] + '.kml'
    
def email(self):
    import win32com.client
    o = win32com.client.Dispatch("Outlook.Application")
    Msg = o.CreateItem(0)
    Msg.Subject = self.subject
    Msg.To = self.recipient 
    Msg.Body = self.body
    Msg.CC = 'CC'

    Msg.Send()

def get_exif(filepath):
    ret = {}
    from PIL import Image
    i = Image.open(filepath)
    #i = imageobject
    info = i._getexif()
    #try:
    for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    return i, ret
    #except:
    #    return i, {}

def moveImage(filepath, imagehome):
    import shutil,os
    date = dateStringYMD()
    folder = os.path.join(imagehome,date)
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    newfilepath =  os.path.join(folder,os.path.basename(filepath))
    shutil.copy2(filepath, newfilepath)
    return newfilepath

def geopics(a):
    try:
        
        if 'GPSInfo' in a.keys() :
            lat = [float(x)/float(y) for x, y in a['GPSInfo'][2]]
            latref = a['GPSInfo'][1]
            lon = [float(x)/float(y) for x, y in a['GPSInfo'][4]]
            lonref = a['GPSInfo'][3]

            
            lat = lat[0] + lat[1]/60 + lat[2]/3600
            lon = lon[0] + lon[1]/60 + lon[2]/3600
            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon
            picdata= lat,lon
            return picdata
        else:
            return (37.817525, -121.737361)
    except:
        return (37.817525, -121.737361)





def getOutputFolder(root):

            folder = tkFileDialog.askdirectory(parent=root,title='Choose an output folder',initialdir="C:\\")
            return folder

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



class ImageProcessor3(object):
    
                def __init__(self, filename,ScreenManager):
                        from PIL import Image, ImageTk
                        self.filename = filename
                        #self.tile = Image.open(filename)
                        
                        self.tile,self.exifdata = get_exif(filename)
                        self.boundingBox = self.tile.getbbox()
                        self.lat,self.long = geopics(self.exifdata)
                        self.date = self.exifdata['DateTime']

                        if self.boundingBox[2] > self.boundingBox[3]:
                            self.screenImageWidth = (ScreenManager.imagecanvasWidth -limiter)  * (self.boundingBox[2] / self.boundingBox[3])
                            self.screenImageHeight = (ScreenManager.imagecanvasWidth -limiter ) 

                        else:
                            self.screenImageWidth = ScreenManager.imagecanvasHeight - limiter
                            self.screenImageHeight = (ScreenManager.imagecanvasHeight -limiter)  * (float(self.boundingBox[3])/self.boundingBox[2])

                        self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
                        del self.tile
                        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 



class ImageProcessorPDF(object):
    
    def __init__(self, filename):
        from PIL import Image, ImageTk
        self.filename = filename
        self.tile = Image.open(filename)
        self.boundingBox = self.tile.getbbox()
        if self.boundingBox[2] > self.boundingBox[3]:
            self.dim = 'width'
        else:
            self.dim = 'height'
        
        



class ImageProcessorPreview(object):
    
    def __init__(self, filename,ScreenManager):
            from PIL import Image, ImageTk
            self.filename = filename
            self.tile = Image.open(filename)
            self.boundingBox = self.tile.getbbox()
            #self.exifdata = get_exif(filename)
            #self.lat,self.long = geopics(self.exifdata)
            limiter = (ScreenManager.imagecanvasWidth/5)
            if self.boundingBox[2] > self.boundingBox[3]:
                self.screenImageWidth = (ScreenManager.imagecanvasWidth -limiter) 
                self.screenImageHeight = (ScreenManager.imagecanvasWidth -limiter ) * (self.boundingBox[2] / self.boundingBox[3])

            else:
                self.screenImageWidth = ScreenManager.imagecanvasHeight - limiter
                self.screenImageHeight = (ScreenManager.imagecanvasHeight -limiter)  * (float(self.boundingBox[3])/self.boundingBox[2])

            self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
            del self.tile
            self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessorReview(object):
    
    def __init__(self, root, image, filename,exifdata, ScreenManager):
        from PIL import Image, ImageTk
        self.filename = filename
        self.tile = image
        self.boundingBox = self.tile.getbbox() 
        self.exifdata = exifdata  
        self.root = root
        sql = "SELECT Y(Geometry),X(Geometry) FROM CCWD_Photos WHERE Filepath = '{0}'".format(filename)

        self.root.cursorspatial.execute(sql)
        results = self.root.cursorspatial.fetchone()
        if results != None:
            if results == (37.817525, -121.737361):
                self.lat, self.long  = 37.817525, -121.737361    
            else:
                self.lat, self.long  = results
        else:
            self.lat, self.long  = 37.817525, -121.737361
        for key in self.exifdata:
            if type(key) == type('a') or type(key) == type(u'a'):
                if key.find('DateTime') != -1:
                    datekey = key
                    self.date = self.exifdata[key]
                    break


        limiter = (ScreenManager.imagecanvasWidth/5)
        if self.boundingBox[2] > self.boundingBox[3]:
            self.screenImageWidth = (ScreenManager.imagecanvasHeight -limiter) 
            self.screenImageHeight = (ScreenManager.imagecanvasHeight -limiter ) * (self.boundingBox[2] / self.boundingBox[3])

        else:
            self.screenImageWidth = ScreenManager.imagecanvasWidth - limiter
            self.screenImageHeight = (ScreenManager.imagecanvasWidth -limiter)  * (float(self.boundingBox[3])/self.boundingBox[2])

        self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 

class ImageProcessorPreviewSide(object):
    
    def __init__(self, filename,width):
        from PIL import Image, ImageTk
        self.filename = filename
        self.tile,self.exifdata = get_exif(filename)
        self.boundingBox = self.tile.getbbox()
        self.lat,self.long = geopics(self.exifdata)
        for key in self.exifdata:
            if type(key) == type('a') or type(key) == type(u'a'):
                if key.find('DateTime') != -1:
                    datekey = key
                    self.date = self.exifdata[key]
                    break

        if self.boundingBox[2] > self.boundingBox[3]:
            self.screenImageWidth = width * (self.boundingBox[2] / self.boundingBox[3])
            self.screenImageHeight = width 

        else:
            self.screenImageWidth = width 
            self.screenImageHeight = width  * (float(self.boundingBox[3])/self.boundingBox[2])

        self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
        del self.tile
        #self.tilescreen.save
        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 



class ImageProcessorGeo(object):
    
    def __init__(self, filename,image, exif, ScreenManager):
        'Class to hold info about open file with geo dimensions'
        from PIL import Image, ImageTk
        self.filename = filename
        self.tile, self.exifdata = image, exif
        self.boundingBox = self.tile.getbbox()
        for key in self.exifdata:
            if type(key) == type('a') or type(key) == type(u'a'):
                if key.find('DateTime') != -1:
                    datekey = key
                    self.date = self.exifdata[key]
                    break
        
        self.lat,self.long = geopics(self.exifdata)

        limiter = (ScreenManager.imagecanvasWidth/5)

        if self.boundingBox[2] > self.boundingBox[3]:
            self.screenImageWidth = (ScreenManager.imagecanvasHeight -limiter) * (self.boundingBox[2] / self.boundingBox[3])
            self.screenImageHeight = (ScreenManager.imagecanvasHeight -limiter ) 

        else:
            self.screenImageWidth = ScreenManager.imagecanvasWidth - limiter
            self.screenImageHeight = (ScreenManager.imagecanvasWidth -limiter)  * (float(self.boundingBox[3])/self.boundingBox[2])

        self.tilescreen = self.tile.resize((int(self.screenImageWidth), int(self.screenImageHeight)), Image.ANTIALIAS)
        del self.tile
        self.jpgPI = ImageTk.PhotoImage(self.tilescreen) 


class calendarTk(Tkinter.Frame): # class calendarTk
    """ Calendar, the current date is exposed today, or transferred to date"""
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

    
class DataScroll(object):
    
    def __init__(self, frame, width,height):
        self.frame = Frame(frame)
        
        self.heightIMap = height
        self.widthIMap = width 

        self.scrollbar2 = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar2.pack(side=RIGHT, fill=Y)
        self.canvas = Canvas(self.frame,background='#FFFFFF',
                             width = self.widthIMap,
                             height = self.heightIMap,
                             borderwidth=3,relief='sunken',
                             )
        self.canvas.pack(side=TOP)
        self.scrollbar2.config(command=self.canvas.yview)

class PhotoManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor, data, columns ):
        
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns

        self.coords = coords
        self.ocolor = ocolor
        self.point = self.map.create_oval(self.coords[0]-.2,self.coords[1]-.2, self.coords[0]+.2,self.coords[1]+.2, 
                                               fill=self.ocolor,outline= 'black',
                                               activefill="yellow",
                                               tags = ('photo', self.data)
                                               )
               
class PointsManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor, attributes, columns, data, pcolumns):
        
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns
        self.attributes = attributes
        self.pcolumns = pcolumns
        self.coords = coords
        self.ocolor = ocolor
        self.point = self.map.create_oval(self.coords[0]-1,self.coords[1]-1, self.coords[0]+1,self.coords[1]+1, 
                                               fill=self.ocolor,outline= 'black',
                                               activefill="yellow",
                                               tags = ('point','geo', self.data)
                                               )

               
class LineManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor,  attributes, columns, data, pcolumns):
    
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns
        self.attributes = attributes
        self.pcolumns = pcolumns
        self.coords = coords
        self.ocolor = ocolor
        self.line = self.map.create_line(self.coords, 
                                               fill= self.ocolor,
                                               activefill="yellow",
                                               tags = ('line','geo', self.data)
                                               )
                
                
class PolygonManager(object):
    
    def __init__(self, MapCanvas,coords,scoords, ocolor, fcolor, attributes, columns, data, pcolumns, bbox):
        
        self.map = MapCanvas.canvas
        self.spatialcoords = scoords
        self.data = data
        self.columns = columns
        self.attributes = attributes
        self.pcolumns = pcolumns
        self.coords = coords
        self.ocolor = ocolor
        self.fcolor = fcolor
        self.bbox = bbox
        self.polygon = self.map.create_polygon(self.coords, 
                                               outline=self.ocolor,
                                               fill=self.fcolor, 
                                               activeoutline="red",
                                               activefill="yellow",
                                               tags = ('polygon','geo', self.data)
                                               )
        self.textval = ''
        for CNTR,att in enumerate(self.attributes[1:-2]):
            if att == None or att =='None':
                att = 'unknown'
            self.textval += self.columns[CNTR+1][1] + ' = ' + str(att) + '\n'
            
    def draw_tooltip(self, event):
        """Draw a tooltip showing contents of cell"""
        self.map.delete('tooltip')
        x = event.x
        y = event.y

        


        self.text = self.map.create_text(x,y,text =self.textval,tag='tooltip',fill='black')
        
        
        box = self.map.bbox(self.text)
        x1=box[0]-1
        y1=box[1]-1
        x2=box[2]+1
        y2=box[3]+1

        rect = self.map.create_rectangle(x1+1,y1+1,x2+1,y2+1,tag='tooltip',fill='black')
        rect2 = self.map.create_rectangle(x1,y1,x2,y2,tag='tooltip',fill='lightyellow')
        self.map.lift(self.text)

        

    def remove_tooltip(self, event):
        """Draw a tooltip showing contents of cell"""

        self.map.delete('tooltip')
        return

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
        
        #self.scrollbarX.config(command=self.canvas.xview)
        #self.scrollbarY.config(command=self.canvas.yview)
                

class ScreenManager(object):

    def __init__(self, root):
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()

        self.windowWidth = root.winfo_screenwidth()
        self.windowHeight = root.winfo_screenheight()

        self.wdivider = self.windowWidth/10
        self.hdivider = self.windowHeight/10

        self.mapcanvasWidth = (self.wdivider) * 2.5
        self.mapcanvasHeight = self.mapcanvasWidth* 1.0


        self.imagecanvasWidth = (self.wdivider) * 5.5
        self.imagecanvasHeight = (self.hdivider) * 8.5

        self.imagethumbcanvasWidth = (self.wdivider) * 1.2 
        self.imagethumbcanvasHeight = (self.hdivider) * 8.5

        self.datacanvasWidth =  (self.wdivider) * 2.5
        self.datacanvasHeight =  (self.hdivider) * .5 

        self.tablecanvasWidth =  (self.wdivider) * 2.5
        self.tablecanvasHeight =  (self.hdivider) * 2.5

class ImageSideWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
  
        self.canvas = Canvas(self.frame,background='white',
                             width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken',
                             )
        

class ImageWindow(object):
    
    def __init__(self, frame, width, height):
        self.frame = frame
        
        self.heightIMap = height
        self.widthIMap = width 
        self.canvas = Canvas(self.frame,background='white',width = self.widthIMap, height = self.heightIMap, borderwidth=3,relief='sunken')

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
        self.listbox.selection_set(0)
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
                
class FieldImages(Frame):
    def __init__(self,mainImages,mainDB,icons,srid, Master=None,**kw):

        apply(Frame.__init__,(self,Master),kw)
        self.srid = srid
        self.searchBufferVal = '100'
        self.mainImageLibrary = mainImages
        self.logoPath = os.path.join(icons,'logo.ico')
        self.inputMain = mainDB
        #self.inputLocal = localDB
        #if os.path.exists(mainDB):
        self.mainDB = mainDB
        #else:
        #    self.mainDB = localDB
        #self.imageLibrary  = images
        Master.wm_iconbitmap(self.logoPath)
        self.buttonPicsPath = icons
        self.menubar = Menu(Master,tearoff=1)
        filemenu = Menu(self.menubar, tearoff=0)
        #filemenu.add_separator()
        #filemenu.add_command(label="Adjust Load Limit",command=self.adjustTableLimit)
        
        filemenu.add_command(label="Preview Images",command=self.previewPicSingleDialogue)
        filemenu.add_separator()
        filemenu.add_command(label="Exit",command=Master.destroy)
        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_separator()

        mapsmenu = Menu(self.menubar, tearoff=0)
        mapsmenu.add_command(label="As Shapefile",command = self.makeSHP)
        mapsmenu.add_command(label="As KML",command=self.outputPicKMLs)
        mapsmenu.add_command(label="As Spreadsheet", command=self.makeSpreadSheet)
        mapsmenu.add_command(label="As PDFs", command=self.printImageToPDFs)

        self.menubar.add_cascade(label="Export Images", menu=mapsmenu)
        self.setmenu = Menu(self.menubar, tearoff=0)
        self.setmenu.add_command(label="Base Layer = CCWD_Properties ", command=self.reviewPicsBaseLocation)
        
        self.setmenu.add_command(label="Set Search Table", command=self.reviewPicsSelectLocation)
        self.setmenu.add_command(label="Search Buffer = 100", command=self.setSearchBuffer)
        self.setmenu.add_command(label="Set Image Type", command=self.reviewPicsSelectType)

        self.setmenu.add_command(label= 'Set Start Date', command= self.setStartDate )
        self.setmenu.add_command(label= 'Set End Date', command= self.setEndDate )
        self.setmenu.add_command(label= 'Reset', command= self.resetAll )
        
        self.menubar.add_cascade(label="Review Images", menu=self.setmenu)

        self.menubar.add_command(label="Add Images", command=self.addPicsSelect)

        

        Master.config(menu=self.menubar)        
        
        self.toolTipManager = ToolTipManager()

        self.BaseFrame = Frame(self)
        self.BaseFrame.grid(row=0, column=0, padx = 1, pady=1,sticky=W+E+S+N)

        self.colors = COLORS #[   "red", "green", "blue", "cyan", "yellow",  'grey', 'light blue', 'dark red','dark green', 'dark blue', 'sky blue', 'tan' ]

        self.initialize()

    
    def randcolor(self):
        return random.randint(0,len(self.colors)-1)

    def initialize(self):
        self.wInfo = ScreenManager(self)
        #self.zoomer = ZoomManager
        self.addedPics = ''
        self.backgroundcolor = 'white'
        self.infrastructureSelected = ''
        self.progbar = ttk.Progressbar( orient=HORIZONTAL, length=200, mode='determinate')

        self.selectDateFrom = '1900:01:01'
        self.selectDateTo = '{0}:{1}:{2}'.format(*time.localtime()[0:3])
        self.setOfImages = []
        self.selectIndicator =0
        self.bigPicCOUNTER = 0
        self.sideY = 0
        self.bigPicMode = 0
        self.buttonWidth = self.wInfo.imagethumbcanvasWidth/3.0
        self.buttonHeight = self.buttonWidth/1.3
        self.mapBaseOutlineColor =  self.colors[self.randcolor()]
        self.mapBaseFillColor = self.colors[self.randcolor()]
        self.mapSearchOutlineColor = self.colors[self.randcolor()]
        self.mapSearchFillColor = self.colors[self.randcolor()]

        self.reviewMode = 0
        self.labelFont = font=("Arial", "9")
        self.labelTitleFont = font=("Arial", "10", 'italic')
        self.buttonTextSpacer = 50
        self.buttonSpacer = 40
        self.buttonColor = 'cadet blue'
        self.createFrames()
        self.allButtonsRefresh()
        self.bindings()
        self.curspatial()
        #self.setBase()
        self.imageSearchTable = ''
        self.imageSearchType = 'All'
        self.imageBaseTable = 'CCWD_Properties'
        self.imagePhotoTable = 'CCWD_Photos'
        self.imageFields = [(self.imagePhotoTable, 'Date'),(self.imagePhotoTable, 'Type'),(self.imagePhotoTable, 'Monitor'),(self.imagePhotoTable, 'Property'),(self.imagePhotoTable, 'Filepath'), ]
        self.ImageSQL = "SELECT Distinct {1}.Date, {1}.Type,{1}.Monitor,{1}.Property,{1}.Filepath,{1}.AsText(Transform(Geometry, {0})) FROM {1}".format(self.srid, self.imagePhotoTable)
        self.clickSearchVal = '0'
        self.pushbuttonIndicator = 0
        self.initiateMap()
        
        
    def setBase(self):
        from pysqlite2 import dbapi2 as sql
        db = 'initialphoto.sqlite'
           
        sql_connection = sql.Connection(db)
        cursor = sql.Cursor(sql_connection)
        
        try:
            createsql = "CREATE TABLE Settings ('baseTable' text,'photoTable' text)"
            cursor.execute(createsql)
            self.imageBaseTable = self.selectMetaGeoTables().keys()[0]
            self.imagePhotoTable = self.reviewPicsSelectPhoto()
            insertsql = "INSERT INTO INITIATION VALUES ('{0}','{1}')".format(self.imageBaseTable, self.imagePhotoTable)
            cursor.execute(insertsql)
            sql_connection.commit()
        except:        
                pass
        sql ='SELECT * FROM SETTINGS'
        cursor.execute(sql)
        results = cursor.fetchone()
        if results == None:
            pass
    def resetBase(self):
        from pysqlite2 import dbapi2 as sql
        db = 'initialphoto.sqlite'
           
        sql_connection = sql.Connection(db)

        cursor = sql.Cursor(sql_connection)        
        self.imageBaseTable = self.reviewPicsBaseLocation()
        self.imagePhotoTable = self.reviewPicsSelectPhoto()
        insertsql = "INSERT INTO INITIATION VALUES ('{0}','{1}')".format(self.imageBaseTable, self.imagePhotoTable)
        cursor.execute(insertsql)
        sql_connection.commit()
        
    def curspatial(self):
        from pysqlite2 import dbapi2 as sql
        self.sql_connection = sql.Connection(self.mainDB)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
        self.cursorspatial = sql.Cursor(self.sql_connection)
        self.sql_connection.enable_load_extension(1)
        self.sql_connection.load_extension('libspatialite-2.dll') 

        

        
    def initiateMap(self):
        self.turnoffClick = 0
        self.mapCoordMaxX =  0
        self.mapCoordMaxY =  0
        self.mapCoordMinX = 1000000000 
        self.mapCoordMinY = 1000000000 
        self.mapWidthSpacer = 100
        self.mapHeightSpacer = 100
        self.startcoords =[0,0]
        self.endcoords = [0,0]
        self.imageMapWindow.canvas.delete('all')
        #self.bigPicture.canvas.delete('pic')
        #self.sidePicture.canvas.delete('thumb')

        
        self.mapBaseGenerator()
        self.mapSearchGenerator()
        self.loadMap()        
        self.loadSearchLayer()
        self.mapPhotoGenerator()
        self.loadMapPhotos()
        self.bindings()


        

    def refreshMetaPhotos(self):
        metaSQL = "SELECT Type, Name from CCWD_Photos"
        self.cursorspatial.execute(metaSQL)
        results = self.cursorspatial.fetchall()
        
        phototablesDic = {}
        for row in results:
            if not row[0] in phototablesDic.keys():
                phototablesDic[row[0]] = [row[1]]
            else:
                phototablesDic[row[0]].append(row[1])
        return phototablesDic

    def bindings(self):
        #self.bigPicture.canvas.bind("<Button-1>", self.ZoomInMode)
        #self.bigPicture.canvas.bind("<Button-3>", self.ZoomOutMode)
        self.sidePicture.canvas.bind("<Button-1>", self.sideImageLoadFromClick)
        self.imageMapWindow.canvas.bind("<ButtonRelease-1>", self.onRelease)
        #self.imageMapWindow.canvas.bind("<Button-1>", self.orderImagesByDistance)

    def onDrag(self, start, end):

        self.startcoords = start#[start[0] - self.mapWidthSpacer/2.0,start[1] - self.mapHeightSpacer/2]
        self.endcoords= end #[end[0] - self.mapWidthSpacer/2,end[1] - self.mapHeightSpacer/2]

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
                yorigin = start[1] + (abs(start[1]-end[1])/2.0)  
    
            self.imageMapWindow.canvas.scale('all',xorigin ,yorigin, 
                                             xscale,yscale)
            self.startcoords =[0,0]
            self.endcoords = [0,0]
            
    def orderImagesByDistance(self, event):
        if self.turnoffClick == 0:
            mapx, mapy = self.screenToCoords(event)
            pointWKT = wkt.geom_from_wkt('''POINT({0} {1})'''.format(mapx, mapy))
            distanceList = []
            distControl = []
            for photo in self.photogeodata:
                photoWKT = wkt.geom_from_wkt(photo[-1])
                dist = pointWKT.distance(photoWKT)
                
                distanceInstance = (photo, dist)
                distanceList.append(distanceInstance)
                distControl.append(dist)
            
            distControl.sort()
            data = []
            for dist in distControl:
                for distvals in distanceList:
                    if distvals[1]== dist and distvals[0] not in data:
                        data.append(distvals[0])
            self.loadSelected(self, data, self.imageFields)
        
                
        
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
    def returnButton(self):
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Right.gif'))
        self.photoResetButton =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.imageDataButtons)
        self.photoResetButton.image = photo 

    def createFrames(self):
        self.imageModeFrame = Frame(self.BaseFrame,bg=self.backgroundcolor, relief='raised', bd=2)
                                     
                                     
        self.imageModeFrame.grid(row=0,column=0, sticky = W+E+N+S, padx= 15, pady= 15)

        self.imageModeFrameMain = Frame(self.imageModeFrame,bg=self.backgroundcolor)
        self.imageModeFrameMain.grid(row=0,column=0,  sticky = W+E+N+S)


        self.bigPicture = ImageWindow(self.imageModeFrameMain,self.wInfo.imagecanvasWidth , self.wInfo.imagecanvasHeight  )
        self.bigPicture.canvas.grid(row=0,column=1, sticky = W+E+N+S)


        self.mapmenubarImage = Menu(self.master,tearoff=0)
        self.mapmenubarImage.add_command(label="Adjust Image Location", command=self.updateLocation)
        self.mapmenubarImage.add_command(label="Adjust Image Type", command=self.updateType)





        self.sidePicture = ImageSideWindow(self.imageModeFrameMain,self.wInfo.imagethumbcanvasWidth , self.wInfo.imagethumbcanvasHeight  )
        self.sidePicture.canvas.grid(row=0,column=0, sticky = W+E+N+S)
        self.imageModeFrameBottom = Frame(self.imageModeFrame,bg=self.backgroundcolor)
                                     
                                      
        self.sideImageFrame = Frame(self.imageModeFrameMain,bg=self.backgroundcolor)
        self.sideImageFrame.grid( row=0,column=2,  sticky= E+W+N+S)

        self.imageMapFrame = Frame(self.sideImageFrame,bg=self.backgroundcolor)
        self.imageMapFrame.grid(row=0,column=0, sticky= E+W+N+S)        
        self.imageMapWindow = MapImages(self.imageMapFrame,self.wInfo.mapcanvasWidth, self.wInfo.mapcanvasWidth )
        self.imageMapWindow.canvas.grid(row=0,column=0,sticky= E+W+N+S )
 # 
        self.mapmenubar = Menu(self.master,tearoff=0)
        self.mapmenubar.add_command(label="Add Base Layer", command=self.reviewPicsBaseLocation)
        self.mapmenubar.add_command(label="Add Search Layer", command=self.reviewPicsSelectLocation)
        self.mapmenubar.add_command(label="Adjust Buffer Distance", command=self.setSearchBuffer)
        self.mapmenubar.add_command(label="Adjust Base Layer Colors", command=self.setBaseColor)
        self.mapmenubar.add_command(label="Adjust Search Layer Colors", command=self.setSearchColor)

        def popup(event):
            self.mapmenubar.post(event.x_root, event.y_root)
        self.imageMapWindow.canvas.bind("<Button-3>", popup)

        self.imageDataFrame = Frame(self.sideImageFrame,bg=self.backgroundcolor)
        self.imageDataFrame.grid(row=1,column=0, sticky= N+E+W+S)
        self.imageDataWindow = LegendWindow(self.imageDataFrame,self.wInfo.datacanvasWidth, self.wInfo.datacanvasHeight )
        self.imageDataWindow.canvas.grid(row=0,column=0, sticky= N+E+W+S)
        


        self.tableframe= Frame(self.sideImageFrame,width= self.wInfo.tablecanvasWidth,  bd=3,relief='sunken',height =self.wInfo.tablecanvasHeight)
        self.tableframe.grid(row=2,column=0, sticky= N+E+W+S)
        tableModel = TableModel(rows=10,columns=3)
        
        self.table = TableCanvas(self.tableframe, model = tableModel,  width= self.wInfo.tablecanvasHeight, height =self.wInfo.tablecanvasHeight  )
        self.table.createTableFrame()        
        self.imageMapWindowRect = RectTracker(self.imageMapWindow.canvas)
        self.imageMapWindowRect.autodraw(fill="", width=2, command=self.onDrag)
    
        self.imageExportFrame = Frame(self.sideImageFrame,bg=self.backgroundcolor)
        self.imageExportFrame.grid(row=3,column=0, sticky= N+E+W+S)
        self.imageExportWindow = LegendWindow(self.imageExportFrame,self.wInfo.datacanvasWidth, self.wInfo.datacanvasHeight )
        self.imageExportWindow.canvas.grid(row=0,column=0, sticky= N+E+W+S)    


    def adjustTableLimit(self):
        self.table.rowsperpage = tkSimpleDialog.askinteger('Adjust Load Limit', 'Adjust the number of images loaded at a time (default is 10)')
        if not self.table.rowsperpage >0:
            self.table.rowsperpage = 10
        self.refreshBoth()
        
    def openImageLibrary(self):
        os.startfile(self.mainImageLibrary)
        
    def exportToFolder(self):
        date = dateStringYMD(ymd=5)
        outfolder = getOutputFolder(self)
        if len(outfolder)>1:
            folderpath = os.path.join(outfolder, date)
            if not os.path.exists(folderpath):
                os.mkdir(folderpath)
                
            dataDic  = self.table.model.data
            keys = dataDic.keys()
            for key in keys:
                filepath = dataDic[key]['Filepath']
                newfilepath = os.path.join(folderpath, os.path.basename(filepath))
                shutil.copy2(filepath, newfilepath)
            os.startfile(folderpath)
    
    def setBaseColor(self):
        self.mapBaseOutlineColor =  tkColorChooser.askcolor(parent = self, title='Outline')[1]
        self.mapBaseFillColor = tkColorChooser.askcolor(parent = self, title='Fill')[1]
        self.initiateMap()


    def setSearchColor(self):
        self.mapSearchFillColor = tkColorChooser.askcolor(parent = self, title='Fill Color')[1]
        self.initiateMap()

    def allButtonsRefresh(self):
        self.imageBigPictureButtons()
        self.imageSidePicturesButtons()
        self.imageMapButtons()
        self.imageExportButtons()

    
    
    def imageExportButtons(self):
        width =self.buttonWidth 
        height= self.buttonHeight/2
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Camera.gif'))
        self.imageLoad =  Button(background=self.buttonColor,width = width, height = height,  image = photo, bd=3,relief='raised',command=self.addPicsToScreen)
        self.imageLoad.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'folder_open.gif'))
        self.imageExport =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.exportToFolder)
        self.imageExport.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'folder_1.gif'))
        self.imageImageLibrary =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.openImageLibrary)
        self.imageImageLibrary.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Print.gif'))
        self.imageButtonBatchPrint =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.printImageToPDFs)
        self.imageButtonBatchPrint.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'World2.gif'))
        self.imageButtonBatchKML =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.outputPicKMLs)
        self.imageButtonBatchKML.image = photo


        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Home.gif'))
        self.imageButtonBatchHome =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.refreshBoth) 
        self.imageButtonBatchHome.image = photo


        chooserbuttonsdic = {self.imageExport:'Export Selected Images', self.imageLoad:'Load Selected Images',self.imageImageLibrary:'Open Image Library',
                             self.imageButtonBatchPrint:'Create PDFs of Selected Images', 
                             self.imageButtonBatchKML:'Create KMLs of Selected Images',
                             self.imageButtonBatchHome:'Reset Map and Images' }
        chooserbuttons = [self.imageLoad,self.imageExport, self.imageImageLibrary,
                          self.imageButtonBatchKML,self.imageButtonBatchPrint,self.imageButtonBatchHome]
 
        for COUNTER, button in enumerate(chooserbuttons):
            
            self.imageExportWindow.canvas.create_window((width * COUNTER) + (10), 15 ,window=button,anchor="nw")
            self.toolTipManager.register(button, chooserbuttonsdic[button])
    
    
    
    def imageSidePicturesButtons(self):
        width =self.buttonWidth
        height= self.buttonHeight/2
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Up.gif'))
        self.imageButtonUp =  Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.imageThumbsDown)
        self.imageButtonUp.image = photo
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Down.gif'))
        self.imageButtonDown = Button(background=self.buttonColor,width = width, height = height, image = photo, bd=3,relief='raised',command=self.imageThumbsUp)
        self.imageButtonDown.image = photo
        chooserbuttonsdic = {self.imageButtonUp:'Move Up', 
                             self.imageButtonDown:'Move Down'}
        chooserbuttons = [self.imageButtonUp, self.imageButtonDown]
 
        for COUNTER, button in enumerate(chooserbuttons):
            self.sidePicture.canvas.create_window((width * COUNTER) + ((self.wInfo.imagecanvasWidth/5)/(len(chooserbuttons)*2)),self.wInfo.imagecanvasHeight - height ,window=button,anchor="nw", tags=('buttons'))
            self.toolTipManager.register(button, chooserbuttonsdic[button])
            
    def imageBigPictureButtons(self):        
        width1 = self.buttonWidth
        height1 = self.buttonHeight/2 
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Left.gif'))
        self.imageButtonBack =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.lastImage)
        self.imageButtonBack.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Right.gif'))
        self.imageButtonNext =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.nextImage)
        self.imageButtonNext.image = photo



        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Print.gif'))
        self.imageButtonPrint =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised', command=self.printImageToPDFMode)
        self.imageButtonPrint.image = photo
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'World2.gif'))
        self.imageButtonKML =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.outputPicKML)
        self.imageButtonKML.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'UpRight.gif'))
        self.imageButtonRotate =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.rotateImage)
        self.imageButtonRotate.image = photo               



        
        mainwindowbuttons = {self.imageButtonBack: 'Last Image', 
                             self.imageButtonNext: 'Next Image',
                             self.imageButtonKML: 'Make Image KML',
                             self.imageButtonPrint:  'Make Image PDF', 
                             self.imageButtonRotate: 'Rotate Image' ,
  
                             
                            }
        
        mainwindowbuttonsOrder= [self.imageButtonBack, self.imageButtonNext, self.imageButtonKML, self.imageButtonPrint,]#self.imageButtonDelete, self.imageButtonHome]
        for COUNTER, button in enumerate(mainwindowbuttonsOrder):
            self.bigPicture.canvas.create_window((width1 * COUNTER) + (self.wInfo.imagecanvasWidth/3)  ,self.wInfo.imagecanvasHeight - height1  ,window=button,anchor="nw")
            self.toolTipManager.register(button, mainwindowbuttons[button])
            
    def imageBigPicturePreviewButtons(self):        
        width1 = self.buttonWidth
        height1 = self.buttonHeight/2
        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Left.gif'))
        self.imageButtonPreviewBack =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.lastPreviewImage)
        self.imageButtonPreviewBack.image = photo


        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Right.gif'))
        self.imageButtonPreviewNext =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.nextPreviewImage)
        self.imageButtonPreviewNext.image = photo




        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Print.gif'))
        self.imageButtonPreviewPrint =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.printImageToPDFMode)
        self.imageButtonPreviewPrint.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'World2.gif'))
        self.imageButtonPreviewKML =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.outputPicKML)
        self.imageButtonPreviewKML.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'delete.gif'))
        self.imageButtonPreviewDelete =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.deletePic)
        self.imageButtonPreviewDelete.image = photo

        photo = PhotoImage(file = os.path.join(self.buttonPicsPath,'Home.gif'))
        self.imageButtonPreviewHome =  Button(background=self.buttonColor,width = width1, height = height1, image = photo, bd=3,relief='raised',command=self.refreshBoth) 
        self.imageButtonPreviewHome.image = photo
               
        mainwindowbuttons = {self.imageButtonPreviewBack:'Last Image', self.imageButtonPreviewNext:'Next Image',
                             self.imageButtonPreviewKML: 'Make Image KML',self.imageButtonPreviewPrint:'Make Image PDF', 
                             self.imageButtonPreviewHome:'Reset Mode',
                            }
        for COUNTER, button in enumerate(mainwindowbuttons):
            self.bigPicture.canvas.create_window((width1 * COUNTER) + (self.wInfo.imagecanvasWidth/3)  ,self.wInfo.imagecanvasHeight - height1  ,window=button,anchor="nw")
            self.toolTipManager.register(button, mainwindowbuttons[button])


    def imageMapButtons(self):
        width1 = self.buttonWidth
        height1 = self.buttonHeight/2 
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
            self.imageDataWindow.canvas.create_window((width1 * COUNTER) + (10), 15 ,window=button,anchor="nw")
            self.toolTipManager.register(button, mapwindowbuttonsdic[button])
             
    def selectProprerty(self, pointgeom):
        propsql =  "SELECT NAME FROM {2} WHERE INTERSECTS(Geometry, Transform(ST_GeomFromText({0},4326),{1}))".format(pointgeom,self.srid,self.imageBaseTable)
        self.cursorspatial.execute(propsql)
        prop = self.cursorspatial.fetchone()
        return prop
        
    def selectHMU(self, pointgeom):
        hmusql =  "SELECT NAME FROM CCWD_ManagementUnits WHERE INTERSECTS(Geometry, Transform(ST_GeomFromText({0},4326),{1}))".format(pointgeom,self.srid)
        self.cursorspatial.execute(hmusql)
        hmu = self.cursorspatial.fetchone()
        return hmu        

    def selectIntersectAny(self,table, pointgeom):
        anysql =  "SELECT * FROM {0} WHERE INTERSECTS(Geometry, Transform(ST_GeomFromText({1},4326),{2}))".format(table,pointgeom,self.srid)
        self.cursorspatial.execute(anysql)
        any = self.cursorspatial.fetchone()
        return any  
        
    def selectImageAll(self):
        self.cursorspatial.execute(self.ImageSQL)        
        results = self.cursorspatial.fetchall()
        return results
    
    def selectImageType(self):
        sql = "SELECT DISTINCT TYPE FROM CCWD_PHOTOS"
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()

        dic= {}
        for result in results:
            dic[result[0].title()] = result[0]
        return dic  
          
    def selectFilepathsWhere(self, fields, table, where):
        sql = "SELECT {0},AsText({3}.Geometry) FROM {3}{1} WHERE {2}".format(fields,table,where, self.imagePhotoTable)
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()
        return results
    
    def reviewSQLgenerator(self):
        
        buffer = self.searchBufferVal
        startdate = self.selectDateFrom
        enddate = self.selectDateTo
        table = self.imageSearchTable
        phototype = self.imageSearchType
        
        if table != '':
            tablesql = "{2}.ID IN (SELECT ROWID FROM SpatialIndex WHERE f_table_name = '{2}' AND search_frame = transform(buffer({0}.Geometry,{1}),4326)) ".format(table, buffer,self.imagePhotoTable)
        else:
            tablesql = ''
            
        datesql = "{2}.Date BETWEEN '{0}' AND '{1}' ".format(startdate, enddate, self.imagePhotoTable)
        
        if phototype != 'All':
            typesql = "{1}.Type = '{0}'".format(phototype, self.imagePhotoTable)
        else:
            typesql = ''


        if table =='':
            table = self.imageBaseTable
        
        fields = ''
        self.imageFields = [(self.imagePhotoTable, 'Date'),(self.imagePhotoTable, 'Type'),(self.imagePhotoTable, 'Monitor'),(self.imagePhotoTable, 'Property'),(self.imagePhotoTable, 'Filepath'), ]
        sql = "SELECT DISTINCT {2}.Date,{2}.Type,{2}.Monitor,{2}.Property, {2}.Filepath,AsText(Transform({2}.Geometry, {1})) FROM {2}{0} ".format( ','+table, self.srid, self.imagePhotoTable)
        
        self.wheresql = ' WHERE ' + datesql
        
        if tablesql != '':
            self.wheresql += ' AND ' + tablesql
            
        if typesql != '':
            self.wheresql += ' AND ' + typesql
            
        finalsql = sql + self.wheresql
        self.ImageSQL = finalsql
        
        

        
    def resetPhotos(self):
        #self.imageSideWindow.canvas.delete('photo')
        self.bigPicture.canvas.unbind("<Button-3>")
        self.imageMapWindow.canvas.delete('photo')
        

    def selectMetaGeoTables(self):

        sql = 'SELECT f_table_name FROM  geometry_columns'
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()

        dic= {}
        for result in results:
            dic[result[0].replace('CCWD_','').title()] = result[0]
#            dic[result[0]]= result[0].replace('CCWD_','').title()
        return dic
    
        
    def reviewPicsSelectType(self):
        dic = self.selectImageType()
        dic['All']= 'All'
               
        selectType = SelectMenu(self,dic,self.setImageType, 'Select Image Type')


    def setClickSearchLimit(self):
        self.clickSearchVal = tkSimpleDialog.askstring('Set Search Distance', 'Enter Search Distance In Meters: ')
        self.setmenu.entryconfig(6, label= 'Click Search Limit = {0}'.format(self.clickSearchVal))
        self.reviewSQLgenerator()
        self.initiateMap()
    
    def setSearchBuffer(self):
        self.searchBufferVal = tkSimpleDialog.askstring('Set Buffer Distance', 'Enter Buffer Distance In Meters: ')
        self.setmenu.entryconfig(2, label= 'Search Buffer = {0}'.format(self.searchBufferVal))
        self.reviewSQLgenerator()
        self.initiateMap()

    def reviewPicsSelectPhoto(self):
        dic = self.selectMetaGeoTables()
        selectType = SelectMenu(self,dic,self.setPhotoTable, 'Select Geo Photo Table')
        return selectType

    def setPhotoTable(self, table):
        self.imagePhotoTable = table
        
    def reviewPicsSelectLocation(self):
        dic = self.selectMetaGeoTables()
        dic['None'] = ''
        selectType = SelectMenu(self,dic,self.setImageLocation, 'Select Geo Table to Add to Map')

    def reviewPicsBaseLocation(self):
        
        dic = self.selectMetaGeoTables()
        selectType = SelectMenu(self,dic,self.setBaseLocation, 'Select Base Table to Add to Map')
        return selectType

    def setBaseLocation(self,table):
        self.setmenu.entryconfig(0, label= 'Base Table = {0}'.format(table))
        self.imageBaseTable = table
        self.reviewSQLgenerator()
        self.initiateMap()
        
    def setImageLocation(self,table):
        self.setmenu.entryconfig(1, label= 'Search Table = {0}'.format(table))
        self.imageSearchTable = table

        self.reviewSQLgenerator()
        
        self.initiateMap()     
        

        
    def updateLocation(self):
        if tkMessageBox.askyesno('Adjust Location', 'Do You Want To Adjust The Location of This Image?'):
            self.initiateMap()
            tkMessageBox.showinfo('Adjust Location', 'Click On The Map To Adjust Location')
            
            
            
            self.imageMapWindow.canvas.unbind(  "<Button-1>")
            #self.imageMapWindow.canvas.unbind(  self.orderImagesByDistance)
            self.imageMapWindow.canvas.bind("<Button-1>", self.getClickedLocation)
    
    def getClickedLocation(self, event):

        mapx, mapy = self.screenToCoords(event)


        pointWKT = "'POINT({0} {1})'".format(mapx, mapy)
    
        transql = "SELECT AsText(Transform(GeomFromText({0},{1}),4326))".format(pointWKT,self.srid)
        geom4326 = str(self.curspatialExe(transql)[0][0])
        sql = "UPDATE CCWD_Photos SET Geometry = GeomFromText('{0}',4326) WHERE Filepath = '{1}'".format(geom4326, self.picImage.filename)    
        
        if tkMessageBox.askyesno('Adjust Location', 'Are You Satisfied With The New Location of This Image?'):
            self.cursorspatial.execute(sql)
            self.sql_connection.commit()  
            geoparts = self.parseGeo(geom4326)
            self.picImage.lat = geoparts[1]
            self.picImage.long = geoparts[0]
            
            tkMessageBox.showinfo('Adjust Location', 'The Location Has Been Adjusted')
            self.imageMapWindow.canvas.unbind( '<Button-1>')
            self.initiateMap()
            self.bindings()
            
    def updateType(self):
        dic = self.selectImageType()
        dic['Other'] = 'Other'
        selectType = SelectMenu(self,dic,self.resetImageType, 'Select Image Type')    
    
    def resetImageType(self, type):
        if type == 'Other':
            type = tkSimpleDialog.askstring('Supply a Type', 'What Type Of Image Is This?')
        
        sql = "UPDATE CCWD_Photos SET Type = '{0}' WHERE Filepath='{1}'".format(type,self.picImage.filename )
        self.cursorspatial.execute(sql)
        self.sql_connection.commit()
        tkMessageBox.showinfo('Type Update', 'The Image Type Has Been Updated')
        self.initialize()
        
        
    def setImageType(self, type):
        self.imageSearchType = type
        self.setmenu.entryconfig(3, label= 'Search Type = {0}'.format(self.imageSearchType ))
        self.reviewSQLgenerator()
        self.initiateMap()
        


    def addImageTypeLoad(self,type):
        if len(type)<1:
            type == 'Other'
        if type == 'Other':
            type = tkSimpleDialog.askstring('Supply a Type', 'What Type Of Images Are Being Added?')
        if len(type)!=0:
            self.imageAddType = type
            self.addPhotosToDatabase()
        else:
            if tkMessageBox.askyesno('No Type Supplied', 'Do you want to load this image?'):
                self.addPicsClassify()
            else:
                tkMessageBox.showwarning('Image Not Loaded', 'This image will not be loaded to the database')
                
    
    def addPicsSelect(self):
        self.addedPics = self.addPicsFolderDialogue()
        if len(self.addedPics) > 1:
            self.addPicsReview()
            self.addPicsClassify()

        else:
            tkMessageBox.showwarning('No File Selected', 'You have not selected any images')
            
    def addPicsClassify(self):
        dic = self.selectImageType()
        dic['Other'] = 'Other'
        selectType = SelectMenu(self,dic,self.addImageTypeLoad, 'Select Image Type')
        


    def nextImage(self):
        
        if (self.bigPicCOUNTER + 1) == len(self.setOfImages):
            self.bigPicCOUNTER = 0
        else:
            self.bigPicCOUNTER += 1
            
        self.bigPicture.canvas.delete('pic')
        self.picImage = self.setOfImages[self.bigPicCOUNTER] 
        self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
        self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')
        
    def rotateImage(self):
        filename = self.picImage.filename
        metadata = pyexiv2.ImageMetadata(filename)

        
        image = Image.open(filename)
        image.rotate(90)
        image.save(filename)
        image, exifdata = get_exif(filename)
        if 'GPSInfo' in exifdata.keys() :
            picImageBig = ImageProcessorGeo(filename, image, exifdata, self.wInfo)
        else:
            picImageBig = ImageProcessorReview(image,filename,  exifdata, self.wInfo)
        picImageBig.notes = ''         
        self.bigPicture.canvas.delete('pic')
        self.setOfImages[self.bigPicCOUNTER] = picImageBig
        self.picImage = self.setOfImages[self.bigPicCOUNTER] 
        self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
        self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')
        metadata.write()       
        
    def lastImage(self):
        if (self.bigPicCOUNTER - 1) <0 :
            self.bigPicCOUNTER = (len(self.setOfImages)-1)
        else:
            self.bigPicCOUNTER -= 1        
            
        self.bigPicture.canvas.delete('pic')
        self.picImage = self.setOfImages[self.bigPicCOUNTER] 
        self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
        self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')

    def nextPreviewImage(self):
        if len(self.setOfPreviewImages) > 0:
            if (self.bigPicCOUNTER + 1) == len(self.setOfPreviewImages):
                self.bigPicCOUNTER = 0
            else:
                self.bigPicCOUNTER += 1
                
            self.bigPicture.canvas.delete('pic')
            self.picImage = self.setOfPreviewImages[self.bigPicCOUNTER] 
            self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
            self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')


        
    def lastPreviewImage(self):
        if len(self.setOfPreviewImages) > 0:
            if (self.bigPicCOUNTER - 1) <0 :
                self.bigPicCOUNTER = (len(self.setOfPreviewImages)-1)
            else:
                self.bigPicCOUNTER -= 1        
                
            self.bigPicture.canvas.delete('pic')
            self.picImage = self.setOfPreviewImages[self.bigPicCOUNTER] 
            self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
            self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')






    def addPicsFolderDialogue(self):

        pics = tkFileDialog.askopenfilenames(parent=self,initialdir='C:/',
                                                  title='Import Images or Set of Images',defaultextension='.jpg',
                                                  filetypes=[('JPEG', '*.jpg')])
        
        return pics
            
        
    def previewPicSingleDialogue(self):

        self.previewPics = tkFileDialog.askopenfilenames(parent=self,initialdir='C:/',
                                                  title='Import an Image',defaultextension='.jpg',
                                                  filetypes=[('JPEG', '*.jpg')])
        self.generatePreviewPics()
    
    def generatePreviewPics(self):
        self.reviewMode =1
        if len(self.previewPics) != 0:
            self.bigPicMode = 0
            self.sidePicture.canvas.delete('thumb')
            self.sidePicture.canvas.delete('data')

            self.bigPicture.canvas.delete('all')
            self.imageBigPicturePreviewButtons()
    
            wid = self.sidePicture.widthIMap
            self.setOfPreviewImagesDic = {}
            
            self.bigPicCOUNTER = 0
            self.setOfPreviewImages = []
            

            splitList = self.previewPics.split('} {')
            for COUNTER,pic in enumerate(splitList):
                pic = pic.replace('{','')
                pic = pic.replace('}','')
                image, exifdata = get_exif(pic)
                picImageBig = ImageProcessorReview( image,pic, exifdata, self.wInfo)
                self.setOfPreviewImages.append(picImageBig)    

                picImage = ImageProcessorPreviewSide(pic,wid)            
                yvalue = int(COUNTER * picImage.screenImageHeight + 10 )
                nextyvalue = int((COUNTER +1) * picImage.screenImageHeight + 10 )
                rangeval = (yvalue, nextyvalue)
                self.setOfPreviewImagesDic[picImageBig] = [picImage, rangeval]
                thumbImage = self.sidePicture.canvas.create_image( 10,yvalue, image= picImage.jpgPI, anchor="nw", tags='thumb')
            self.sideMax = nextyvalue      
            self.picImage = self.setOfPreviewImages[0]#ImageProcessor3(r'C:\CCWD\pics\Los Vaqueros 003.jpg', self.wInfo)    
            self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
            self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')


    def setStartDate(self):
        self.selectIndicator =1
        frame = Toplevel()
        frame.wm_iconbitmap(self.logoPath)
        def setFrom(f):
            self.selectDateFrom = f
            self.setmenu.entryconfig(4, label='Start Date = {0}'.format(f))

            frame.destroy()
            self.reviewSQLgenerator()
            self.initiateMap()
        c = calendarTk(master=frame, date="2008:01:01",dateformat="%Y:%m:%d",command=setFrom)
        c.grid(row=0,column=0)
        
            
    def setEndDate(self):
        self.selectIndicator =1
        frame = Toplevel()
        frame.wm_iconbitmap(self.logoPath)

        def setFrom(f):
            self.selectDateTo = f
            self.setmenu.entryconfig(5, label='End Date = {0}'.format(f))
            frame.destroy()
            self.reviewSQLgenerator()
            self.initiateMap()
        c = calendarTk(master=frame, date=self.selectDateTo,dateformat="%Y:%m:%d",command=setFrom)
        c.grid(row=0,column=0)


    def addPicsReview(self):
        'bring the selected images to the screen to review them'
        self.reviewMode= 1
        self.bigPicture.canvas.delete('pic')
        self.bigPicMode = 1

        wid = self.sidePicture.widthIMap
        self.setOfAddedImagesDic = {}
        
        self.bigPicCOUNTER = 0
        self.setOfAddedImages = []
        self.addedPics = self.addedPics.replace('JPG','jpg')
        splitList = self.addedPics.split('jpg') 
        self.newList = []
        self.missingList = []
        for COUNTER,split in enumerate(splitList):
            pic = ''
            if len(split) != 0:
                if split.find('{')!=-1 or split.find('}')!=-1:
                    pic = split.replace('{','')
                    pic = pic.replace('} ','')
                    pic = pic.replace('}','')
                    pic = pic.replace('JPG','') 

                elif split[0]==' ':
                    pic = split.replace(' ','',1)
                    pic = pic.replace('JPG','')     
                else:
                    pic = split
                path = pic + 'jpg'
                if os.path.exists(path) and path not in self.newList:
                    self.newList.append(pic + 'jpg')
                elif not os.path.exists(path) and path not in self.missingList:
                    self.missingList.append(path)
                    tkMessageBox.showinfo('Image Missing', os.path.basename(path) + ' Does Not Exist' )
        nextyvalue =0
        for COUNTER,pic in enumerate(self.newList):
            image, exifdata = get_exif(pic)
            if 'GPSInfo' in exifdata.keys() :
                picImageBig = ImageProcessorGeo(pic, image, exifdata, self.wInfo)
            else:
                picImageBig = ImageProcessorReview(self, image,pic,  exifdata, self.wInfo)
            picImageBig.notes = ''  
            self.setOfAddedImages.append(picImageBig)
            
            picImage = ImageProcessorPreviewSide(pic,wid)   

            if picImage.screenImageHeight > picImage.screenImageWidth:
                spacer  = picImage.screenImageHeight
            else:
                spacer = picImage.screenImageWidth
            yvalue = int(nextyvalue + 10 )
            nextyvalue = yvalue + int(spacer+ 10 )

            rangeval = (yvalue, nextyvalue)
            self.setOfAddedImagesDic[picImageBig] = [picImage, rangeval]
            thumbImage = self.sidePicture.canvas.create_image( 10,yvalue, image= picImage.jpgPI, anchor="nw", tags='thumb')


        self.bigPicture.canvas.bind("<Button-3>", self.popupImage)
        
        if nextyvalue != 0:
            self.sideMax = nextyvalue                        
            self.picImage = self.setOfAddedImages[0]#ImageProcessor3(r'C:\CCWD\pics\Los Vaqueros 003.jpg', self.wInfo)    
            self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
            self.bigPicture.canvas.create_image(self.imageModeWidth/2,10, image= self.picImage.jpgPI, anchor="nw",tags ='pic')
            self.setOfImages = self.setOfAddedImages


    def popupImage(self,event):
            self.mapmenubarImage.post(event.x_root, event.y_root)
            

    def addPhotosToDatabase(self):
        insertSQL = "INSERT INTO {0}(Date,Monitor,Type,Property,HMU,Notes,Filepath,Geometry) VALUES ({1})"
        imagefolder = self.createDatedFolder()
        sqlcollection = []
        for image in self.setOfImages:
            shutil.copy(image.filename, os.path.join(imagefolder,os.path.basename(image.filename)))
            filepath = os.path.join(imagefolder,os.path.basename(image.filename))
            date = image.date
            pointgeom = "'POINT({0} {1})'".format(image.long, image.lat)

            hmu = self.selectHMU(pointgeom)
            v= ()
            hmuSQL = ''
            if type(hmu) == type(v):
                hmuSQL +=  '"'+hmu[0] +'"'+ ','
            else:
                hmuSQL +=  '"",'    

            prop = self.selectProprerty(pointgeom)
            v = ()
            propSQL = ''
            if type(prop) == type(v):
            
                propSQL +=  '"'+prop[0] +'"' + ','
            else:
                propSQL +=  '"",'                
            monitor = getpass.getuser()     
            notes = image.notes   
            try:
                values = '"'+date + '","' + monitor  +'","' +self.imageAddType +'",' + propSQL + hmuSQL + '"'+notes+'"' + ',"'+ filepath+'",' + "ST_GeomFromText({0},4326)".format(pointgeom)
                sql= insertSQL.format(self.imagePhotoTable, values)
                sqlcollection.append(sql)

            except Exception as e:
                tkMessageBox.showwarning('Image(s) Not Added',image.filename + ' was not added because \n'+ str(e))
        if tkMessageBox.askyesno('Final Assurance', 'Are you sure you want to add these to the database?'):
            for sql in sqlcollection:
                self.cursorspatial.execute(sql)
                self.sql_connection.commit()
            tkMessageBox.showinfo('Images Loaded', 'The image data added to the database.\nThe images were copied here: {0}'.format(imagefolder))
            #self.menubar.delete(4)
        else:
            tkMessageBox.showinfo('Image Loading Stopped', 'The images were not added to the database')
        #self.menubar.delete(5)
        #self.pushbuttonIndicator = 0
        
    def addDataToLocalDB(self,sql):
        from pysqlite2 import dbapi2 as sql
        sql_connectionLocal = sql.Connection(self.inputLocal)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
        cursorspatialLocal = sql.Cursor(sql_connectionLocal)
        sql_connectionLocal.enable_load_extension(1)
        sql_connectionLocal.load_extension('libspatialite-2.dll')         
        curspatialLocal.execute(sql)
        sql_connectionLocal.commit()


    def syncDBs(self):
        sqlstatement = "PRAGMA table_info(CCWD_PHOTOS)"
        self.cursorspatial.execute(sqlstatement)
        columns = self.cursorspatial.fetchall()
        fields  = ''
        for COUNTER,column in enumerate(columns):
            field = column[1]
            if field == 'Geometry':
                field = ' AsText(Geometry)'
                geomval = COUNTER
            if COUNTER != (len(columns)-1):
                
                fields += field + ','
            else:
                fields += field 
        sqlsel = "Select {0} FROM CCWD_PHOTOS".format(fields)
        self.cursorspatial.execute(sqlsel)
        mainresults = self.cursorspatial.fetchall()
    
    
    
        lsql_connection = sql.Connection(self.inputLocal)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
        lcursor = sql.Cursor(lsql_connection)
        lsql_connection.enable_load_extension(1)
        lsql_connection.load_extension('libspatialite-2.dll') 
        sqlstatement = "PRAGMA table_info(CCWD_PHOTOS)"
        lcursor.execute(sqlstatement)
        columns = lcursor.fetchall()
        fields  = ''
        for COUNTER,column in enumerate(columns):
            field = column[1]
            if field == 'Geometry':
                field = ' AsText(Geometry)'
                geomval = COUNTER
            if COUNTER != (len(columns)-1):
                
                fields += field + ','
            else:
                fields += field 
        sqlsel = "Select {0} FROM CCWD_PHOTOS".format(fields)
        lcursor.execute(sqlsel)
        localresults = lcursor.fetchall()
    
        x= 0
        for results in mainresults:
            if results not in localresults:
                x = 1
                date = "'"+str(results[1])+"'"
                monitor = "'"+str(results[2])+"'"
                type = "'"+str(results[3])+"'"
                property = "'"+str(results[4])+"'"
                hmu = "'"+str(results[5])+"'"
                notes = "'"+str(results[6])+"'"
                
                #newfilepath = results[7]
                
                filepath = "'"+str(results[7])+"'"
                geometry =  'GeomFromText(' + "'" + results[-1] + "'" +',4326)'  
                insertSQL = "INSERT INTO CCWD_PHOTOS(Date,Monitor,Type,Property,HMU,Notes,Filepath,Geometry) VALUES ({0},{1},{2},{3},{4},{5},{6},{7})".format(date,monitor,type,property,hmu,notes,filepath,geometry )
                lcursor.execute(insertSQL)
                lsql_connection.commit()




    def deleteChosenPics(self):
        #self.imageDataWindow.canvas.delete('all')
        self.sidePicture.canvas.delete('thumb')
        self.bigPicture.canvas.delete('all')
        self.imageBigPictureButtons()
        self.imageDataButtons()
        self.addedPics = ''
        self.setOfAddedImages = []
        

 
    def sideImageLoadFromClick(self,event):
        y = event.y
        if self.reviewMode == 1:
            if self.bigPicMode == 0:
                dic = self.setOfPreviewImagesDic
                set = self.setOfPreviewImages
            elif self.bigPicMode == 1:
                dic = self.setOfAddedImagesDic
                set = self.setOfImages
            
    
            for COUNTER,picObject in enumerate(dic): 
                rangeval = dic[picObject][1]
                if y in range(rangeval[0]+ self.sideY,rangeval[1]+self.sideY):
                    self.bigPicture.canvas.delete('pic')
                    self.picImage = set[COUNTER] 
                    self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
                    self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= picObject.jpgPI, anchor="nw",tags ='pic')
                    
  

    
    def imageThumbsUp(self):
        if self.sideY < 0:
            self.sidePicture.canvas.move('thumb',0, 100 )
            self.sideY += 100
    
    def imageThumbsDown(self):
        if self.sideY + self.sideMax > self.sidePicture.heightIMap:
            self.sidePicture.canvas.move('thumb',0, -100 )
            self.sideY -= 100



    def ZoomInMode(self,event):
        x = event.x
        y = event.y
        self.bigPicture.canvas.delete('pic')
        self.picFilePath = self.pics[self.bigPicCOUNTER]
        self.picImageBig = ImageProcessorResizeBig(self.picFilePath,self.wInfo)
        self.imageModeWidth  = self.bigPicture.widthIMap - self.picImageBig.screenImageWidth
        self.bigPicture.canvas.create_image(self.imageModeWidth/2 - x,3 - y, image= self.picImage.jpgPI, anchor="nw",tags ='pic')
        

    def ZoomOutMode(self,event):
        x = event.x
        y = event.y
        self.bigPicture.canvas.delete('pic')
        self.picFilePath = self.pics[self.bigPicCOUNTER]
        self.picImageSmall = ImageProcessorResizeSmall(self.picFilePath,self.wInfo)
        self.imageModeWidth  = self.bigPicture.widthIMap - self.picImageSmall.screenImageWidth
        self.bigPicture.canvas.create_image(self.imageModeWidth/2 - x,3 - y, image= self.picImage.jpgPI, anchor="nw",tags ='pic')
        
    def BigPicHome(self):
        self.imageModeFrameMain.destroy()
        self.initialize()
    def refreshBoth(self):
        self.bigPicture.canvas.delete('all')
        self.sidePicture.canvas.delete('thumb')
        self.imageBigPictureButtons()
        #self.imageExportButtons()
        self.initiateMap()
        
    def deletePic(self):
        if len(self.setOfImages) != 0: 
            self.bigPicture.canvas.delete('pic')
            self.setOfImages.pop(self.bigPicCOUNTER)
            if self.bigPicCOUNTER != 0:
                self.bigPicCOUNTER -=1
            else:
                self.bigPicCOUNTER = 0
            try:
                self.picImage = self.setOfImages[self.bigPicCOUNTER]    
                self.imageModeWidth  = self.bigPicture.widthIMap - self.picImage.screenImageWidth
                self.bigPicture.canvas.create_image(self.imageModeWidth/2,3, image= self.picImage.jpgPI, anchor="nw",tags ='pic')
            except:
                self.BigPicHome()    
                
    def printImageToPDFMode(self):
        self.printImageToPDF() 
        
    def printImageToPDF(self):
        
        
        filename = savePDF()
        ptext = self.picImage.date
        if len(filename) > 1:
            imagePDF2(self.picImage.filename, [ptext],filename )
            os.startfile(filename)
        else:
            tkMessageBox.showwarning('File not Selected', 'No file name was selected')
        
    def printImageToPDFs(self):
        
        dataDic = self.table.model.data
        pdfs = []
        lendex = len(dataDic) +1 
        
        for index in range(1,lendex):
            row = dataDic[str(index)]
            filepath = row['Filepath']
            monitor = row['Monitor']
            date = row['Date']
            prop = row['Property']
            type = row['Type']
            ptext = [date , type ,monitor, prop]
            imagePDF2(filepath, ptext, 'pdf_{0}.pdf'.format(str(index)) )
            
            pdfs.append('pdf_{0}.pdf'.format(str(index)))
        output = PdfFileWriter()
        openfiles = []
        for pdf in pdfs:
            openpdf = file(pdf, 'rb')
            inpdf = PdfFileReader(openpdf)
            output.addPage(inpdf.getPage(0))
            openfiles.append(openpdf)
        filename = savePDF()
        outputStream = file(filename, "wb")
        output.write(outputStream)
        outputStream.close()    
        
        for COUNTER, pdf in enumerate(pdfs):
            opdf = openfiles[COUNTER]
            opdf.close()
            os.remove(pdf)
        os.startfile(filename)
        
    def outputPicKMLs(self):
        #if self.setOfImages == []:
        #    self.addPicsReview()
        date = dateStringYMD(ymd=5)
        outfolder = getOutputFolder(self)
        if len(outfolder)>1:
            folderpath = os.path.join(outfolder, date)
            if not os.path.exists(folderpath):
                os.mkdir(folderpath)
        
        dic =  self.table.model.data
        files = []
        for i in range(1,10):
            
            if self.table.currentpage> 0:
                val= str(self.table.currentpage) + str(i)
            else:
                val = str(i)
            if val in dic.keys():
                filepath = dic[val]['Filepath']
                if filepath  not in files:
                    files.append(filepath)

        
        
        for COUNTER, pic in enumerate(files):
            filepath = pic.filename

            longitude = pic.long
            latitude = pic.lat
            kmlname= os.path.basename(filepath).replace('jpg','')
            
            kmlname2= kmlname.replace(' ','')
             
            shutil.copy(filepath,os.path.join(folderpath,os.path.basename(filepath)))
            kmltext = kml % (kmlname2, kmlname,
                             os.path.basename(filepath),
                             '',
                             longitude, 
                             latitude, 
                             longitude, 
                             latitude )
            outkml = os.path.join(folderpath, '{0}.kml'.format(kmlname))
            if os.path.exists(outkml):
                outkml = os.path.join(folderpath, '{0}_{1}.kml'.format(kmlname,COUNTER))
                              
            kmlfile = open(outkml, 'w')        
            kmlfile.write(kmltext)
            kmlfile.close()        
        os.startfile(folderpath)
        os.chdir(folderpath)
        os.system('zip -r C:\Temp\%s.kmz *' % 'test')
        
        
    def outputPicKML(self):
        if self.setOfAddedImages != []:
            filepath = self.picImage.filename
            longitude = self.picImage.long
            latitude = self.picImage.lat
            date = dateStringYMD()
            outfolder = getOutputFolder(self)
            if len(outfolder)>1:
                folderpath = os.path.join(outfolder, date)
                if not os.path.exists(folderpath):
                    os.mkdir(folderpath)
            
            
            kmlname = os.path.basename(filepath).replace('.jpg','')
            kmlname2 = kmlname2= kmlname.replace(' ','')
            shutil.copy(filepath,os.path.join(folderpath, os.path.basename(filepath)))
            kmltext = kml % (kmlname2, kmlname,
                             os.path.basename(filepath),
                             '',
                             longitude, 
                             latitude, 
                             longitude, 
                             latitude )
            
            kmlfile = open(os.path.join(folderpath,'%s.kml' % kmlname), 'w')        
            kmlfile.write(kmltext)
            kmlfile.close()        
            os.startfile(folderpath)

    def makeSpreadSheet(self):        
        'convert a table into a spreadsheet'
        ssname = saveCSV(self)
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Images')
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
                        
        fields = self.imageFields
        newfield = (self.imagePhotoTable,'Transformed Geometry As Text') 
        fields.append(newfield)
        for COUNTER, header in enumerate(fields):
            worksheet.write(0, COUNTER, label = header[1], style = headerStyle)

        for COUNTER, data in enumerate(self.photogeodata):
            for ROWCOUNT, value in enumerate(data):
                
                worksheet.write( COUNTER+1, ROWCOUNT, label = value, style =dataStyle)
        workbook.save(ssname)
        
        tkMessageBox.showinfo('File Save', 'Your spreadsheet has been saved at: %s' % ssname)

    
    def makeSHP(self):
        'make a shapefile from selected geo data'



        self.cursorspatial.execute(self.ImageSQL)
        self.retrievedGeoData = self.cursorspatial.fetchall()
        header = ''


        shpname = saveSHP(self)
        shpWriter = Writer()
        shpWriter.autoBalance = 1        
        for COUNTER, column in enumerate(self.imageFields):
            headerval = str(column[1])
            shpWriter.field(headerval, 'C', '255')
        
        geomtype =1
        shpWriter.shapeType = geomtype
        parsedGeometryList = []
        [parsedGeometryList.append(self.parseGeo(data[-1])) for data in self.retrievedGeoData]

        [shpWriter.point(*parsedGeometry) for parsedGeometry in parsedGeometryList]
        
        dataLists = []
        for  data in self.retrievedGeoData:
            dList = list(data[:-1])
            for COUNTER,val in enumerate(dList):
                dList[COUNTER] = str(val)

            dataLists.append(dList)
        [shpWriter.record(*dList) for dList in dataLists]

        shpWriter.save(shpname) 
        prj = generatePRJ()
        prjfile = shpname.replace('.shp','') + '.prj' 
        prjfileOpen = open(prjfile, 'w')
        prjfileOpen.write(prj)
        prjfileOpen.close()
        tkMessageBox.showinfo('File Save', 'Your file has been saved at: {0}'.format(shpname))
        




    def parseGeo(self, geometry):
        partsList = []
        if geometry.find('POINT')!= -1 :
            geom = geometry.split('(')[1].replace(')','')
            geomlist = map(float,geom.split())
            partsList = geomlist
        return partsList
            
    def screenToCoords(self,event):
            screenx = event.x
            screeny = event.y
            mapx, mapy = self.screenToCoordsEngine(screenx,screeny)
            return mapx, mapy
        
    def screenToCoordsEngine(self, screenx, screeny):

            mapx = self.mapCoordMinX + ((float(screenx - (self.mapWidthSpacer/2) )/self.mapWidth) * self.currentCoordWidth)
            mapy = self.mapCoordMaxY - ((float(screeny - (self.mapWidthSpacer/2) )/self.mapHeight )* self.currentCoordHeight)
            return mapx, mapy

    def coordsToScreen(self,points):
            
            mapx = points[0]
            mapy = points[1]

            screenx =   int(((mapx - self.mapCoordMinX)/ self.mapWidth) * self.mapWidth) 
            screeny = int((( self.mapCoordMaxY - mapy )/ self.mapHeight) * self.mapHeight)
            return screenx, screeny
    
    
        
    
    def mapBaseGenerator(self ):
        
        self.mapObjects = []
        table = self.imageBaseTable
        columns = "PRAGMA table_info(%s)" %  table
        self.cursorspatial.execute(columns)
        self.columns = self.cursorspatial.fetchall()
        fields  = ''
        for COUNTER,column in enumerate(self.columns):
                field = column[1]
                if field == 'Geometry':
                    field = 'AsText(Envelope(Geometry)),AsText(Geometry)'
                    geomval = COUNTER
                if COUNTER != (len(self.columns)-1):
                    
                    fields += field + ','
                else:
                    fields += field 
        sql = "Select {0} FROM {1}".format(fields, table)
        self.cursorspatial.execute(sql)
        results = self.cursorspatial.fetchall()


        
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
        if self.mapWidth >= self.mapHeight:
            self.stabilizer = self.mapHeight/float(self.mapWidth)
            self.currentCoordWidth = self.mapCoordMaxX - self.mapCoordMinX
            self.currentCoordHeight = (self.mapCoordMaxY - self.mapCoordMinY) * self.stabilizer
            self.mapCoordMinY = self.mapCoordMaxY - self.currentCoordHeight
        else:
            self.stabilizer = self.mapWidth/float(self.mapHeight)
            self.currentCoordWidth = (self.mapCoordMaxX - self.mapCoordMinX)* self.stabilizer
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
        self.tag = 'base'
        self.loadLayerToScreen(self.mapObjects)
        
    def loadSearchLayer(self):
        
        self.tag = 'search'
        self.loadLayerToScreen(self.mapSearchObjects)  
              
    def loadMapPhotos(self):
        'convert spatial coords to screen coords'
        self.getMBRdata()
        self.mapPhotos= []
        self.loadMapPhotoToScreen()
    
    

    def mapPhotoGenerator(self):
        
        self.mapPhotoObjects = []
        photos = self.imagePhotoTable
        columns = "PRAGMA table_info({0})".format(photos)
        self.cursorspatial.execute(columns)
        self.columns = self.cursorspatial.fetchall()
        results = self.selectImageAll()
        columns = self.columns
        infodic = {photos:[columns,results]}
        self.mapPhotoObjects.append(infodic)
        for COUNTER, dic in enumerate(self.mapPhotoObjects):
            values = dic.values()[0][1]
            transList = []
            for value in values:
                WKT = value[-1]
                transVals = self.polyTransform(WKT)
                transList.append(transVals)
            dic[dic.keys()[0]].append(transList)
        return        

    def mapSearchGenerator(self):
        
        self.mapSearchObjects = []
        if self.imageSearchTable !='':
            table = self.imageSearchTable
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

            columns = self.searchcolumns
            infodic = {table:[columns,results]}
            self.mapSearchObjects.append(infodic)
            
                
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
       
        return  
                 

    def loadLayerToScreen(self, dic):
        self.reviewSQLgenerator()
        photosql = self.ImageSQL 
        self.cursorspatial.execute(photosql)
        self.photogeodata = self.cursorspatial.fetchall()
        pColumns = self.imageFields 
        
        self.loadSelected(self, self.photogeodata, pColumns)
        datavals = ''
        for data in self.photogeodata:
            datavals += data[-2]
        self.addedPics = datavals
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
                        wktgeom = atts[-1]
                        
                        geomWKT = wkt.geom_from_wkt(wktgeom).buffer(int(self.searchBufferVal))
                        photolist = []
                        for photo in self.photogeodata:
                            
                            photoWKT = wkt.geom_from_wkt(photo[-1])
                            if geomWKT.intersects(photoWKT):
                                photolist.append(photo)
                        
                        if geomcol[2] == "LINESTRING":
                                    mapDisplay = self.geoLines(transgeom, geometry,atts,columns, photolist, pColumns, eGeoms)
                        elif geomcol[2] == "POLYGON":
                                    mapDisplay = self.geoPolys(transgeom, geometry,atts,columns, photolist, pColumns, eGeoms)

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
                        wktgeom = atts[-1]
                        
                        geomWKT = wkt.geom_from_wkt(wktgeom).buffer(int(self.searchBufferVal))
                        photolist = []
                        for photo in self.photogeodata:
                            
                            photoWKT = wkt.geom_from_wkt(photo[-1])
                            if geomWKT.intersects(photoWKT):
                                photolist.append(photo)    
                        pointDisplay = self.geoPoints(transgeom, geom, atts,columns, photolist, pColumns)
                        
        return  
    
    def loadMapPhotoToScreen(self):

        for data in self.mapPhotoObjects:
            table = data.keys()[0]
            dVals = data.values()
            attributes = dVals[0][1]
            columns = dVals[0][0]
            gvalues = dVals[0][2]
            
            for COUNTER, geom in enumerate(gvalues):
                    transgeom = []
                    xdist = geom[0] - self.mapCoordMinX
                    ydist = self.mapCoordMaxY - geom[1]
                    xposition = float((xdist/self.currentCoordWidth) * self.mapWidth) + (self.mapWidthSpacer/2)
                    yposition = float((ydist/self.currentCoordHeight) * self.mapHeight) + (self.mapHeightSpacer/2)
                    transgeom.append(xposition)
                    transgeom.append(yposition)    

                    pointDisplay = self.geoPhotos(transgeom, geom, attributes[COUNTER], columns)
                    self.mapPhotos.append(pointDisplay)
        return    
    
    def loadSelected(self, root, data, columns):
        dataDic = self.parseData(data, columns)
        self.table.destroy()
        if dataDic != {}:
            self.tableframe= Frame(self.sideImageFrame,width= self.wInfo.tablecanvasWidth,  bd=3,relief='sunken',height =self.wInfo.tablecanvasHeight)
            self.tableframe.grid(row=2,column=0, sticky= N+E+W+S)
            self.table = TableCanvas(self.tableframe, newdict=dataDic, width= self.wInfo.imagecanvasWidth* .4, height =self.wInfo.imagecanvasWidth *.25  )
            self.table.createTableFrame()  
            self.table.bind('<Button-1>', self.loadClickedRow)

    def addPicsToScreen(self):
        dic =  self.table.model.data
        files = []
        for i in range(1,10):
            
            if self.table.currentpage> 0:
                val= str(self.table.currentpage) + str(i)
            else:
                val = str(i)
            if val in dic.keys():
                filepath = dic[val]['Filepath']
                if filepath  not in files:
                    files.append(filepath)
        
        self.addedPics = ''
        for file in files:
            self.addedPics+=file
        self.addPicsReview()
            
    def loadClickedRow(self,event):
        dataModel = self.table.model
        dic = dataModel.data
        rowIndex = self.table.get_row_clicked(event)
        page = self.table.currentpage

        if page > 0:
            index = str(page)+ str(rowIndex+1)
        else:
            index = str(rowIndex+1)

        #photo = dataModel.getCellRecord(rowIndex, -1)
        photo = dic[index]['Filepath']
        self.addedPics = photo#+self.addedPics.replace(photo,'')
        self.addPicsReview()
        
        
    def geoPoints(self, coords,scoords, attributes, columns, data, pcolumns,):
        if self.tag == 'base':
            ocolor = self.mapBaseOutlineColor 
            fcolor = self.mapBaseFillColor  
        else:
            ocolor = self.mapSearchOutlineColor 
            fcolor = self.mapSearchFillColor   

        if fcolor == ocolor:
            ocolor = self.colors[self.randcolor()]

        pointDisplay = PointsManager(self.imageMapWindow,coords, scoords, ocolor, attributes, columns, data, pcolumns,)
        #self.toolTipManager.register(pointDisplay, 'test')
        class reportPoint(object):
            def __init__(self,root, poly, function):
                self.root= root
                #self.root.toolTipManager.register(poly, 'test')
                self.poly= poly
                self.function = function
                self.data = poly.data
                self.columns = poly.pcolumns
            def execute(self, event):
                if self.root.turnoffClick == 1:
                    self.function(self,self.data, self.columns)
        self.imageMapWindow.canvas.itemconfig(pointDisplay.point, tags = ( self.tag))
        function = reportPoint(self, pointDisplay,self.loadSelected)
        self.imageMapWindow.canvas.tag_bind(pointDisplay.point, '<Double-Button-1>', function.execute)
        return pointDisplay

    def geoLines(self, coords,scoords, attributes, columns, data, pcolumns, bbox):
        if self.tag == 'base':
            ocolor = self.mapBaseOutlineColor 
            fcolor = self.mapBaseFillColor  
        else:
            ocolor = self.mapSearchOutlineColor 
            fcolor = self.mapSearchFillColor   


        lineDisplay = LineManager(self.imageMapWindow,coords, scoords, ocolor, attributes, columns, data, pcolumns, )
        #self.toolTipManager.register(lineDisplay, 'test')
        class reportLines(object):
            def __init__(self,root, poly, function):
                self.root= root
                #self.root.toolTipManager.register(poly, 'test')
                self.poly= poly
                self.function = function
                self.data = poly.data
                self.columns = poly.pcolumns
            def execute(self, event):
                if self.root.turnoffClick == 1:
                    self.function(self,self.data, self.columns)
        self.imageMapWindow.canvas.itemconfig(lineDisplay, tags = ( self.tag))
        function = reportLines(self, lineDisplay,self.loadSelected)
        self.imageMapWindow.canvas.tag_bind(lineDisplay.line, '<Button-1>', function.execute)
        return lineDisplay



    
    def geoPolys(self, coords,scoords, attributes, columns, data, pcolumns, bbox):
        if self.tag == 'base':
            ocolor = self.mapBaseOutlineColor 
            fcolor = self.mapBaseFillColor  
        else:
            ocolor = self.mapSearchOutlineColor 
            fcolor = self.mapSearchFillColor              
            
        if fcolor == ocolor:
            ocolor = self.colors[self.randcolor()]

        polyDisplay = PolygonManager(self.imageMapWindow,coords, scoords, ocolor, fcolor,attributes, columns, data, pcolumns, bbox)
        #self.toolTipManager.register(polyDisplay,'test')
        
        class reportPoly(object):
            def __init__(self,root, poly, function):
                self.root= root
                #self.root.toolTipManager.register(poly, 'test')
                self.poly= poly
                self.function = function
                self.data = poly.data
                self.columns = poly.pcolumns
            def execute(self, event):
                if self.root.turnoffClick == 1:
                    self.function(self,self.data, self.columns)
        self.imageMapWindow.canvas.itemconfig(polyDisplay, tags = ( self.tag))
        function = reportPoly(self, polyDisplay,self.loadSelected)
        self.imageMapWindow.canvas.tag_bind(polyDisplay.polygon, '<Button-1>', function.execute)
        #function2 = reportPoly(self, polyDisplay,polyDisplay.remove_tooltip)#self.loadSelected)
        #self.imageMapWindow.canvas.tag_bind(polyDisplay.polygon, '<B1-Motion>', function2.execute)
        
        return polyDisplay

    def geoPhotos(self, coords,scoords, data, columns):
        
        ocolor = self.mapBaseOutlineColor 
        fcolor = self.mapBaseFillColor  
        if fcolor == ocolor:
            ocolor = self.colors[self.randcolor()]
            
        pointsDisplay = PhotoManager(self.imageMapWindow,coords, scoords, 'red',  data, columns )
        class reportPoint(object):
            def __init__(self,points, function):
                self.function = function
                self.point = points
                self.data = points.data
                self.columns = points.columns
            def execute(self, event):
                self.function(self.point)

        function = reportPoint(pointsDisplay,self.addImage)
        self.imageMapWindow.canvas.tag_bind(pointsDisplay.point, '<Button-1>', function.execute)
        return pointsDisplay
    
    def addImage(self,point):
        coords = point.coords
        datavals = point.data[-2]

        for pointx in self.mapPhotos:
            if pointx.coords == coords:
                datavals +=  pointx.data[-2]
        if self.addedPics != datavals:    
            self.addedPics = datavals
            self.addPicsReview()
        
        
    def ButtonPanUp(self):

                self.imageMapWindow.canvas.move('all',0, self.mapHeightSpacer/5 )

    def ButtonPanDown(self):

                self.imageMapWindow.canvas.move('all',0, -self.mapHeightSpacer/5 )

             
    def ButtonPanLeft(self):

            self.imageMapWindow.canvas.move('all', self.mapWidthSpacer/5,0 )
        

    def ButtonPanRight(self):

            self.imageMapWindow.canvas.move('all', -self.mapWidthSpacer/5,0 )

    def parseData(self,  features, columns):
        dataDic = {}
        valueRange = len(features)
        for i in range(1,valueRange+1):
            dataDic[str(i)] = {}
        for COUNTERX, column in enumerate(columns):
            header = column[1]
            for COUNTERY, value in enumerate(features):
                dataDic[str(COUNTERY+1)][header] = value[COUNTERX] 
        return dataDic
                
        
    def createDatedFolder(self):
        imageLibrary = self.mainImageLibrary
        date = dateStringYMD()
        folderpath = os.path.join(imageLibrary, date)
        if not os.path.exists(folderpath):
            os.mkdir(folderpath)
        return folderpath
    

    def resetAll(self):
        
        self.imageBaseTable = self.reviewPicsBaseLocation()
        self.setmenu.entryconfig(0, label= 'Base Layer = CCWD_Properties ')
        self.imageSearchTable = ''
        self.setmenu.entryconfig(1, label= 'Set Search Layer')
        self.searchBufferVal = '100'
        self.setmenu.entryconfig(2, label= 'Search Buffer = 100')
        self.imageSearchType = 'All'
        self.setmenu.entryconfig(3, label= 'Set Image Type')
        self.selectDateFrom = '1900:01:01'
        self.setmenu.entryconfig(4, label= 'Set Start Date')
        self.selectDateTo = '{0}:{1}:{2}'.format(*time.localtime()[0:3])
        self.setmenu.entryconfig(5, label= 'Set End Date')
        self.setOfAddedImages = []
        self.setOfImages = []
        
        
        
        
        
        
        
        
        
kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>%s</name>
    <Style id="sh_camera_copy:0_copy291">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/camera.png</href>
            </Icon>
        </IconStyle>
    </Style>
    <StyleMap id="msn_camera_copy:0_copy292">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_camera_copy:0_copy290</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_camera_copy:0_copy291</styleUrl>
        </Pair>
    </StyleMap>
    <Style id="sn_camera_copy:0_copy290">
        <IconStyle>
            <scale>0.8</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/camera.png</href>
            </Icon>
        </IconStyle>
    </Style>




    <Placemark>
        <name>%s</name>
        <Snippet maxLines="0" id="khSnippet1041_copy2">Empty</Snippet>



        <description><![CDATA[<table width=200><tr><td>

<center>

<br><img src="%s">
</center>
<br>

<center>

<font size="8" color="black">%s\n</font>
<br>
<font size="8" color="black">Location is Approximate</font>
</center>


</td></tr></table><font color="white">]]></description>



        <LookAt>
            <longitude>%s</longitude>
            <latitude>%s</latitude>
            <altitude>0</altitude>
            <heading>-12.52280530623806</heading>
            <tilt>30</tilt>
            <range>8802.184358802457</range>
        </LookAt>
        <styleUrl>#msn_camera_copy:0_copy292</styleUrl>
        <Point>
            <coordinates>%s,%s,0</coordinates>
        </Point>
    </Placemark>
</Document>
</kml>
'''
           
            
youkml =  '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name></name>
    <Style id="sh_ylw-pushpin">
        <IconStyle>
            <scale>1.3</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
    </Style>
    <Style id="sn_ylw-pushpin">
        <IconStyle>
            <scale>1.1</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <LabelStyle>
            <scale>0.7</scale>
        </LabelStyle>
    </Style>
    <StyleMap id="msn_ylw-pushpin">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_ylw-pushpin</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_ylw-pushpin</styleUrl>
        </Pair>
    </StyleMap>
    <Placemark>
        <name>%s</name>
        <description>%s</description>
        <LookAt>
            <longitude>%s</longitude>
            <latitude>%s</latitude>
            <altitude>0</altitude>
            <range>610.58999413005</range>
            <tilt>21.9744109732249</tilt>
            <heading>-7.271491860164984</heading>
            <altitudeMode>relativeToGround</altitudeMode>
        </LookAt>
        <styleUrl>#msn_ylw-pushpin</styleUrl>
        <Point>
            <coordinates>%s,%s,0</coordinates>      
        </Point>
    </Placemark>
</Document>
</kml>
'''

#This string is a KML script called to produce polygons representing the selected parcels. 
polykml= '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">
<Document>
    <name>%s</name>
    <Style id="sn_ylw-pushpin">
        <IconStyle>
            <scale>1.1</scale>
            <Icon>
                <href>pushpin.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
    </Style>
    <Style id="sn_ylw-pushpin0">
        <IconStyle>
            <scale>1.1</scale>
            <Icon>
                <href>pushpin.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
        <LineStyle>
            <color>#ff0000ff</color>
            <width>6</width>
        </LineStyle>
        <PolyStyle>
            <fill>0</fill>
        </PolyStyle>
    </Style>
    <StyleMap id="msn_ylw-pushpin">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_ylw-pushpin</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_ylw-pushpin0</styleUrl>
        </Pair>
    </StyleMap>
    <StyleMap id="msn_ylw-pushpin0">
        <Pair>
            <key>normal</key>
            <styleUrl>#sn_ylw-pushpin0</styleUrl>
        </Pair>
        <Pair>
            <key>highlight</key>
            <styleUrl>#sh_ylw-pushpin</styleUrl>
        </Pair>
    </StyleMap>
    <Style id="sh_ylw-pushpin">
        <IconStyle>
            <scale>1.3</scale>
            <Icon>
                <href>pushpin.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>

        <PolyStyle>
            <fill>0</fill>
        </PolyStyle>
    </Style>
    <Style id="sh_ylw-pushpin0">
        <IconStyle>
            <scale>1.3</scale>
            <Icon>
                <href>http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png</href>
            </Icon>
            <hotSpot x="20" y="2" xunits="pixels" yunits="pixels"/>
        </IconStyle>
    </Style>
    %s
</Document>
</kml>
'''
placemarKML='''
    <Placemark>
        <name>%s</name>
        <description>%s</description>
        <styleUrl>#msn_ylw-pushpin0</styleUrl>
        <Polygon>
            <tessellate>1</tessellate>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>%s      
                    </coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
    '''


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
            

    