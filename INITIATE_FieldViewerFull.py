import sys
if '.' not in sys.path:
        sys.path.append('.')
        


from TK_GUI.FieldImageViewer_20130618 import FieldImages

from Tkinter import *
from TK_GUI import  managers


import string, shutil
from pysqlite2 import dbapi2 as sql

from PIL import Image, ImageTk
from Tkinter import  Frame, Canvas, SUNKEN, LEFT,RIGHT, Label
import os, tkSimpleDialog, tkFileDialog, tkMessageBox

def selectMetaGeoTables(cursor):

        sql = 'SELECT f_table_name FROM  geometry_columns'
        cursor.execute(sql)
        results = cursor.fetchall()

        dic= {}
        for result in results:
            dic[result[0].title()] = result[0]
#            dic[result[0]]= result[0].replace('CCWD_','').title()
        return dic


class SelectMenu(object):
    
    def __init__(self, dic,execute, title, mode=SINGLE):
        self.masterselect = Tk()
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
                


def openFile(titlestring, desc,ext):
        import tkFileDialog
        filename = tkFileDialog.askopenfilename(  initialdir='C:/',
                                                  title=titlestring,defaultextension= '.{0}'.format(ext),
                                                  filetypes=[(desc, '*.{0}'.format(ext))])
        
        return filename.split('.')[0]+'.{0}'.format(ext)

def openFolder(titlestring):
        import tkFileDialog
        folder = tkFileDialog.askdirectory(title=titlestring)
        
        return folder

def genInitialInfo():
    db = 'initialphoto.sqlite'
    sql_connection = sql.Connection(db)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    cursor = sql.Cursor(sql_connection)
    mainDB = openFile('Locate Main Database File', 'Spatialite SQL Database', 'sqlite')




    mainImages = openFolder('Find Main Images Library Folder')
           

    icons = openFolder('Find Icons Folder')
    srid = tkSimpleDialog.askstring('Spatial Reference System', 'Please provide a spatial reference ID (SRID).\nRefer to spatialreference.org for more instructions')

    sql_connection = sql.Connection(db)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    cursor = sql.Cursor(sql_connection)    
    try:
        createsql = "CREATE TABLE INITIATION ('mainImages' text,'maindb' text,'icons' text, 'srid' text)"
        cursor.execute(createsql)
    except:
        pass
    insertsql = "INSERT INTO INITIATION VALUES ('{0}','{1}','{2}','{3}')".format(mainImages, mainDB,icons, srid)
    cursor.execute(insertsql)
    sql_connection.commit()
    tkMessageBox.showinfo('Database Initialized', 'Your settings have been recorded')
    standards = mainImages,  mainDB, icons,srid 
    return standards


db = 'initialphoto.sqlite'
if os.path.exists(db):
    sql_connection = sql.Connection(db)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    cursor = sql.Cursor(sql_connection)
    sqlstatement = 'SELECT * FROM INITIATION'
    cursor.execute(sqlstatement)
    standards = cursor.fetchone()

if not os.path.exists(db) or standards == None:
    standards = genInitialInfo()

    
mainImages,  mainDB, icons,srid = standards




    
if __name__ == '__main__':
    #try:
        Root = Tk()
        Root.tk_strictMotif()
        App = FieldImages(mainImages,  mainDB, icons,srid,   Root)
        App.pack(expand='yes',fill='both')

        Root.state('zoomed')
        Root.title('ICF Field Office Image View')


                
                
        Root.mainloop()

    #except Exception as e:
    #    print e