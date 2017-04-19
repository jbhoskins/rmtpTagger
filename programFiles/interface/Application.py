# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

from FramedText import *
from Sidebar import *
from EntryWindow import *
from StyleSheet import *
from Legend import *
from Menubar import *

import tkinter as tk
from tkinter import filedialog

#---------------------------------------------------------------------------
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
        self._styleApp()

#---------------------------------------------------------------------------
# Styling

    def _getDim(self):
        """ Gets the dimensions of the screen. """
        print(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        return (self.root.winfo_screenwidth(), self.root.winfo_screenheight())

    def _setStyles(self, name = "bella"):
        """ Set the formatting of the application. """
        self.styles = StyleSheet(name, dim=self.dim)
        
    def _styleApp(self):
        """ Styles the application """
        self.root.config(bg = self.styles.c_1)
        
        self.legend.configStyles(styles = self.styles)
        self.legendFrame.config(bg = self.styles.c_2)
        
        self.fText.configStyles(styles = self.styles)
        
        self.sidebar.configStyles(styles = self.styles)    
        self.sidebarFrame.config(bg = self.styles.c_2)
        
    def _changeTheme(self, name):
        """ Changes the theme of the app. """
        self._setStyles(name)
        self._styleApp()    

#----------------------------------------------------------------
# Creating and placing frames, widgets, and menus
        
    def _placeFrames(self):
        """ Places the sext and sidebar frames within the application. """

        self.legendFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 8)
        self.legendFrame.pack_propagate(0) 
        self.legendFrame.pack(side = tk.LEFT)
        
        self.textFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 2)
        self.textFrame.pack_propagate(0) # Stops frames from shrinking to fit contents.    
        self.textFrame.pack(expand = True, side = tk.LEFT)
        
        self.sidebarFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 4)
        self.sidebarFrame.pack_propagate(0) 
        self.sidebarFrame.pack(side = tk.LEFT)

    def _createWidgets(self):
        """ Fills text box, creates sidebar and menu. """
        self.fText = FramedText(self.textFrame, self.index, self.styles)
        self.fText.pack(expand = True, fill = tk.BOTH)
        self.sidebar = Sidebar(self.sidebarFrame, self.fText, self.index, self.styles)
        self.legend = Legend(self.legendFrame, self.styles)
        self.menubar = Menubar(self)

        self._makeTagMenu()

    def _bindKeys(self):
        """ Binds all clicks and key presses to commands. """
        self.fText.tag_bind("foundWord", "<Button-1>", self.sidebar.showTagResultsOnClick)
        self.sidebar.tagResults.bind("<ButtonRelease-1>", self.sidebar.showSelectionInfo)
        
        self.root.bind("<Right>", self.moveRight)
        self.root.bind("<Left>", self.moveLeft)

        self.fText.tag_bind("interviewee", "<ButtonRelease-3>", self._showTagMenu)
        self.fText.tag_bind("interviewee", "<ButtonRelease-2>", self._showTagMenu)
            
        self.sidebar.tagResults.populateTags([])

#-------------------------------------------------------------------------
# Functions bound to keypresses

    def moveRight(self, event):
        # Should be in framed text, but here for testing purposes.
        self.fText.move(1)
        self.fText.see("1.0+%sc" % self.fText.getCache().start())
        self.sidebar.showTagResults()
        self.sidebar.showSelectionInfo(0)

    def moveLeft(self, event):
        # Should be in framed text, but here for testing purposes.
        self.fText.move(-1)
        self.fText.see("1.0+%sc" % self.fText.getCache().start())
        self.sidebar.showTagResults()
        self.sidebar.showSelectionInfo(0)

#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hover stuff (in progress)

    def on_enter(self, event):
        self.fText.tag_add("cur", self.cur_line, self.cur_line+1) 

    def on_leave(self, enter):
        self.fText.tag_add("reg", self.cur_line, self.cur_line+1)


#--------------------------------------------------------------------
# Right click menu

    def _makeTagMenu(self):
        """ Defines the menu that will show when you right-click. """
        self.menuFrame = tk.Frame(self.root)
        self.tagMenu = tk.Menu(self.menuFrame, tearoff = 0)
        self.tagMenu.add_command(label = "tag here", command = print("tag"))
        self.tagMenu.add_command(label="Add Tag", command = self._showTagScreen)

    def _showTagMenu(self, event):
        """ Shows the Menu pop up when you right click. """
        self.tagMenu.post(event.x_root, event.y_root)
    
    def _showTagScreen(self):
        """ Displays the New Tag Window. """
        word = self.fText.getString()
        self.root.attributes('-topmost', 0)
        self.add_tag = EntryWindow(self.root, word, self.styles)

#---------------------------------------------------------------------------        
# Are you sure you want to leave prompt



#---------------------------------------------------------------------------        
# make root, launch app

    def launch(self):
        """ Launches the program. """
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.launch()

