import sys
if '.' not in sys.path:
        sys.path.append('.')
        
import settings

#from CCWD.models import *

from TK_GUI.TABLEVIEW_20130723 import TABLES

from Tkinter import *
from TK_GUI import  managers


import string

from PIL import Image, ImageTk
from Tkinter import  Frame, Canvas, SUNKEN, LEFT,RIGHT, Label
import os

import string
from pysqlite2 import dbapi2 as sql

from PIL import Image, ImageTk
from Tkinter import  Frame, Canvas, SUNKEN, LEFT,RIGHT, Label
import os, tkSimpleDialog, tkFileDialog, tkMessageBox, shutil



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


def selectMetaTables(cursorspatial):
    sql = "SELECT Name FROM  sqlite_master WHERE type='table' and name LIKE 'CCWD%'"
    
    cursorspatial.execute(sql)
    results = cursorspatial.fetchall()

    return results    


def genInitialInfo():
    db = 'initialtable.sqlite'
    sql_connection = sql.Connection(db)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    cursor = sql.Cursor(sql_connection)
    mainDB = openFile('Locate Main Database File', 'Spatialite SQL Database', 'sqlite')
    if not os.path.exists(os.path.basename(mainDB)):
        shutil.copy(mainDB, os.path.basename(mainDB))

    localDB = os.path.basename(mainDB)



    mainImages = openFolder('Find Main Images Library Folder')

    maps = openFolder('Find Maps Folder')
 
    icons = openFolder('Find Icons Folder')

    reports = openFolder('Find Reports Folder')      
 


    shps = openFolder('Find Main Shapefile Folder')      
 
    spreadsheets = openFolder('Find Spreadsheets Folder')      


    srid = tkSimpleDialog.askstring('Spatial Reference System', 'Please provide a spatial reference ID (SRID).\nRefer to spatialreference.org for more instructions')

    sql_connection = sql.Connection(db)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    cursor = sql.Cursor(sql_connection)    
    try:
        createsql = "CREATE TABLE INITIATION ('mainImages' text,'maindb' text,'maps' text,'reports' text,'srid' text,'icons' text,'shps' text,'spreadsheets' text)"
        cursor.execute(createsql)
    except:
        pass
    insertsql = "INSERT INTO INITIATION VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(mainImages,  mainDB, maps,reports,srid, icons,shps, spreadsheets)
    cursor.execute(insertsql)
    sql_connection.commit()
    tkMessageBox.showinfo('Database Initialized', 'Your settings have been recorded')
    standards = mainImages,  mainDB, maps,reports,srid, icons,shps, spreadsheets
    return standards


db = 'initialtable.sqlite'
if os.path.exists(db):
    sql_connection = sql.Connection(db)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
    cursor = sql.Cursor(sql_connection)
    sqlstatement = 'SELECT * FROM INITIATION'
    cursor.execute(sqlstatement)
    standards = cursor.fetchone()

if not os.path.exists(db) or standards == None:
    standards = genInitialInfo()

    
#
#
#if not os.path.exists(localDB):
#    shutil.copy(mainDB, localDB)
#
#if os.path.exists(mainDB):
#    msql_connection = sql.Connection(mainDB)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
#    mcursor = sql.Cursor(msql_connection)
#    msql_connection.enable_load_extension(1)
#    msql_connection.load_extension('libspatialite-2.dll') 
#    lsql_connection = sql.Connection(localDB)     # This is the path to the database. If it doesn't exist, it will be created, though, of course, without the require tables
#    lcursor = sql.Cursor(lsql_connection)
#    lsql_connection.enable_load_extension(1)
#    lsql_connection.load_extension('libspatialite-2.dll') 
#    tables = selectMetaTables(mcursor)
#    for table in tables:
#        table = table[0]
#        sqlstatement = "PRAGMA table_info({0})".format(table)
#        mcursor.execute(sqlstatement)
#        columns = mcursor.fetchall()
#        fields  = ''
#        for COUNTER,column in enumerate(columns):
#            field = column[1]
#            if field == 'Geometry':
#                field = 'AsText(Geometry)'
#                geomval = COUNTER
#            if COUNTER != (len(columns)-1):
#                
#                fields += field + ','
#            else:
#                fields += field 
#        sqlsel = "Select {0} FROM {1}".format(fields, table)
#        mcursor.execute(sqlsel)
#        mainresults = mcursor.fetchall()
#        lcursor.execute(sqlsel)
#        localresults = lcursor.fetchall()
#        ids = []
#        for results in mainresults:
#            ids.append(results[0])
#        
#        for results in localresults:
#            if results not in mainresults:
#                valstring = ''
#                if results[0] not in ids:
#                    for COUNT,result in enumerate(results[1:]):
#                        
#                        if columns[COUNT+1][2]=='text':
#                            val = "'"+ result+ "'"
#                        elif columns[COUNT+1][2]!='text' and columns[COUNT+1][1]!='Geometry':
#                            val = str(result)
#                        elif columns[COUNT+1][1]=='Geometry':
#                            val = 'GeomFromText(' + "'" + result + "'" +',4326)'  
#                        if COUNT != len(result)-1:
#                            valstring += val + ','
#                        else:
#                            valsting += val
#                    insertSQL = "INSERT INTO {0}({1}) VALUES ({2})".format(table,fields.replace('AsText(Geometry)', 'Geometry'),valstring )
#                    mcursor.execute(insertSQL)
#                    msql_connection.commit()
#                else:
#                    for COUNT,result in enumerate(results[1:]):
#                        
#                        if columns[COUNT+1][2]=='text':
#                            
#                            val = columns[COUNT+1][1] +"= '"+ result+ "'"
#                        elif columns[COUNT+1][2]!='text' and columns[COUNT+1][1]!='Geometry':
#                            val = columns[COUNT][1] +"= '"+ str(result)
#     
#                        if COUNT != len(result)-2:
#                            valstring += val + ','
#                        else:
#                            valsting += val   
#                    where = "ID = '{0}'".format(results[0])             
#                    updateSQL = 'UPDATE {0} SET {1} WHERE {2}'.format(table,valstring,where)
#                    mcursor.execute(insertSQL)
#                    msql_connection.commit()
#    
#
#    shutil.copy(mainDB, localDB)




        


#if x ==1:
#    tkMessageBox.showinfo('Data Sync Complete', 'Data has been synced between the two databases')

    

    
if __name__ == '__main__':
    #try:
        Root = Tk()
        #Root.tk_strictMotif()
        listandards = list(standards)
        listandards.append(Root)
        App = TABLES(*listandards)
        App.pack(expand='yes',fill='both')

        Root.state('zoomed')
        Root.title('ICF Field Office Table View')


        #logoPath = r'logo.ico'
        
        #Root.wm_iconbitmap(logoPath)
                
                
        Root.mainloop()


