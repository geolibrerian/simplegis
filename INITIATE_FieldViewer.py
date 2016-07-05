import sys
if '.' not in sys.path:
        sys.path.append('.')
        
import settings

#from CCWD.models import *

from TK_GUI.FieldImageViewer_20130102 import FieldImages

from Tkinter import *
from TK_GUI import  managers


import string

from PIL import Image, ImageTk
from Tkinter import  Frame, Canvas, SUNKEN, LEFT,RIGHT, Label
import os

  
if __name__ == '__main__':
    #try:
        Root = Tk()
        Root.tk_strictMotif()
        App = FieldImages(Root)
        App.pack(expand='yes',fill='both')

        Root.state('zoomed')
        Root.title('ICF Field Office Image View')


        #logoPath = r'C:\Projects1\ICFFieldOffice\icons\logo.ico'

        #Root.wm_iconbitmap(logoPath)
        #Root.winfo_toplevel().wm_geometry("")
                
                
        Root.mainloop()

    #except Exception as e:
    #    print e