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
#        self.root.attributes('-topmost', 1)
        self.root.wm_title("William and Mary Index Tagger")
        
        self.dim = self._getDim()
        self.mainFrame = tk.PanedWindow(self.root, orient = tk.HORIZONTAL, sashrelief=tk.GROOVE, height = self.dim[1])
        
        self.index = Index("../../META/index.xml")
        
        self._setStyles()
        self.addWidgets()
        self.mainFrame.pack_propagate(0)
        self.mainFrame.pack(fill = tk.BOTH, expand = True)
        self._bindKeys()

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
        self.legend.config(bg = self.styles.c_2)
        
        self.fText.configStyles(styles = self.styles)
        
        self.sidebar.configStyles(styles = self.styles)    
        self.sidebarFrame.config(bg = self.styles.c_2)
        
    def _changeTheme(self, name):
        """ Changes the theme of the app. """
        self._setStyles(name)
        self._styleApp()    

#----------------------------------------------------------------
# Creating and placing frames, widgets, and menus
        
    def addWidgets(self):
        """ Fills text box, creates sidebar and menu. """
        screenWidth = self.styles.dimensions[0]

        self.legend = Legend(self.mainFrame, self.styles)
        self.mainFrame.add(self.legend, width=screenWidth//8, stretch="never")

        # Frame needed to keep scrollbar next to text
        frame = tk.Frame(self.mainFrame)
        scrollbar = tk.Scrollbar(frame)
        self.fText = FramedText(frame, self.index, self.styles, scrollbar)
        scrollbar.config(command=self.fText.yview)
        scrollbar.pack(side = tk.RIGHT, fill=tk.Y)
        self.fText.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.mainFrame.add(frame, width=screenWidth//2, stretch="always")

        self.sidebar = Sidebar(self.mainFrame, self.fText, self.index, self.styles)
        self.mainFrame.add(self.sidebar, width = screenWidth// 4, stretch="never")
        self.menubar = Menubar(self)

        self._makeTagMenu()

    def _bindKeys(self):
        """ Binds all clicks and key presses to commands. """
        self.fText.tag_bind("foundWord", "<Button-1>", self.sidebar.showTagResultsOnClick)
        self.sidebar.tagResults.bind("<ButtonRelease-1>", self.sidebar.showSelectionInfo)
        
        self.root.bind("<Right>", self.moveRight)
        self.root.bind("<Left>", self.moveLeft)
        self.root.bind("<Up>", self.prevTag)
        self.root.bind("<Down>", self.nextTag)

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

    def nextTag(self, event):
        newSel = self.sidebar.tagResults.move(1)
        self.sidebar.tagResults.see(newSel)
        self.sidebar.showSelectionInfo(0)

    def prevTag(self, event):
        newSel = self.sidebar.tagResults.move(-1)
        self.sidebar.tagResults.see(newSel)
        self.sidebar.showSelectionInfo(0)

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
# make root, launch app

    def launch(self):
        """ Launches the program. """
        self.root.mainloop()

if __name__ == "__main__":
    app = Application()
    app.launch()

