# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

from FramedText import *
from Sidebar import *
from EntryWindow import *
import tkinter as tk


class Application:
    """ Main program """
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-topmost', 1)
        self.root.wm_title("William and Mary Index Tagger")
        
        self.dim = self._getDim()
        self.index = Index("../../META/index.xml")
        
        self._setStyles()
        self._placeFrames()
        self._createWidgets()
        self._bindKeys()
        self._style()

    def _getDim(self):
        """ Gets the dimensions of the screen. """
        print(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        return (self.root.winfo_screenwidth(), self.root.winfo_screenheight())

    def _setStyles(self):
        """ Set the formatting of the application. """
        self.font1 = "Verdana", 24
        self.font2 = "Verdana", 18
        self.color1 = "#D5CDFF"
        self.color2 = "#AFC0AA"
        self.styles = [self.font1, self.font2, self.color1, self.color2]

    def _placeFrames(self):
        """ Places the sext and sidebar frames within the application. """

        self.textFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 2)
        self.textFrame.pack_propagate(0) # Stops frames from shrinking to fit contents.    
        self.textFrame.pack(expand = True, side = tk.LEFT)
        
        self.sidebarFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 4)
        self.sidebarFrame.pack_propagate(0) 
        self.sidebarFrame.pack(side = tk.LEFT)

    def _createWidgets(self):
        """ Fills text box, creates sidebar and menu. """
        self.fText = FramedText(self.textFrame, self.index)
        self.fText.loadText("../../input/astaikina.txt")
        self.fText.pack(expand = True, fill = tk.BOTH)
        self.sidebar = Sidebar(self.sidebarFrame, self.fText, self.index, self.styles)
        self._makeMenu()
        self._makeTagMenu()

    def _bindKeys(self):
        """ Binds all clicks and key presses to commands. """
        self.fText.tag_bind("foundWord", "<Button-1>", self.fText.cacheWord)
        self.fText.tag_bind("foundWord", "<Button-1>", self.sidebar.showTagResults)
        self.sidebar.tagResults.bind("<ButtonRelease-1>", self.sidebar.showSelectionInfo)
        self.fText.bind("<ButtonRelease-3>", self._showTagMenu)
        self.fText.bind("<ButtonRelease-2>", self._showTagMenu)
        self.sidebar.tagResults.populateTags([])

    def _style(self):
        """ Styles the application """
        self.root.config(bg = self.color1)
        self.fText.config(bg = self.color1, highlightbackground = self.color1, font = self.font2)
        self.sidebarFrame.config(bg = self.color2)

    def _makeMenu(self):
        """ Defines the system menu. """
        menubar = tk.Menu(self.root)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Export")
        menubar.add_cascade(label="File", menu=filemenu)
        
        toolsmenu = tk.Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="Hide Greens")
        toolsmenu.add_command(label="Hide Interviewer Text")
        toolsmenu.add_command(label="Iterate")
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Edit index...")
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        
        self.root.config(menu=menubar)
        

#--------------------------------------------------------------------
# Right clock stuff

    def _makeTagMenu(self):
        """ Defines the menu that will show when you right-click. """
        self.menuFrame = tk.Frame(self.root)
        self.tagMenu = tk.Menu(self.menuFrame, tearoff = 0)
        self.tagMenu.add_command(label="Add Tag", command = self._showTagScreen)

    def _showTagMenu(self, event):
        """ Shows the Menu pop up when you right click. """
        self.tagMenu.post(event.x_root, event.y_root)


    def _showTagScreen(self):
        """ Displays the New Tag Window. """
        word = self.fText.getCache()
        self.root.attributes('-topmost', 0)
        self.add_tag = EntryWindow(self.root, word, self.color1, self.font1, self.font2)

    def launch(self):
        """ Launched the program. """
        self.root.mainloop()


        
# make root, 
app = Application()
app.launch()

