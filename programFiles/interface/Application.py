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

import tkinter as tk

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
        self.fText.loadText("../../input/astaikina.txt")
        self.fText.pack(expand = True, fill = tk.BOTH)
        self.sidebar = Sidebar(self.sidebarFrame, self.fText, self.index, self.styles)
        self.legend = Legend(self.legendFrame, self.styles)
        
        self._makeMenu()
        self._makeTagMenu()

    def _bindKeys(self):
        """ Binds all clicks and key presses to commands. """
        self.fText.tag_bind("foundWord", "<Button-1>", self.fText.cacheWord)
        self.fText.tag_bind("foundWord", "<Button-1>", self.sidebar.showTagResults)
        self.sidebar.tagResults.bind("<ButtonRelease-1>", self.sidebar.showSelectionInfo)
        self.fText.tag_bind("interviewee", "<ButtonRelease-3>", self._showTagMenu)
        self.fText.tag_bind("interviewee", "<ButtonRelease-2>", self._showTagMenu)
            
        self.sidebar.tagResults.populateTags([])

    def export(self):
        """ Confirms, and exports the changes to a file. """
        savedString = self.fText.get("1.0", tk.END)
        
        # FIND A BETTER WAY TO DO THIS DO NOT USE FLOAT FOR THIS
        print("pre", [(x.string(), x.start()) for x in self.sidebar.exportTags])
        self.sidebar.exportTags.sort(key=lambda x: float(x.start()), reverse=True)
        print("post", [(x.string(), x.start()) for x in self.sidebar.exportTags])

        self.fText.config(state=tk.NORMAL)
        for item in self.sidebar.exportTags:
           
            if item.selected() >= 0:
                entry = item.entries()[item.selected()]
            
                self.fText.insert(self.fText.index(item.stop()), "</rs>")
                print("Start", item.start())
                print(item.start() < item.stop())
                print("Stop", item.stop())
                self.fText.insert(self.fText.index(item.start()), "<rs type=\"%s\" key=\"%s\">" % (entry.type(), entry.xmlId()))
        
        self.fText.config(state=tk.DISABLED)

        string = self.fText.get("1.0", tk.END)
        outputFile = open("../../output/OUTPUT.txt", 'w')
        outputFile.write(string)
        outputFile.close()

        self.fText.config(state=tk.NORMAL)
        # No need to read from disk again, should just copy back in from memory and retag
        self.fText.delete("1.0", tk.END)
        self.fText.loadText("../../input/astaikina.txt")
        self.fText.tag_add("cur", self.fText.wordCache.start(), self.fText.wordCache.stop())
        self.fText.config(state=tk.DISABLED)

    def _makeMenu(self):
        """ Defines the system menu. """
        menubar = tk.Menu(self.root)
        
        # File
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Export", command=self.export)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # Theme
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Bella", command=lambda: self._changeTheme(name = "bella"))
        editmenu.add_command(label="Sasha", command=lambda: self._changeTheme(name = "sasha"))
        editmenu.add_command(label="Elena", command=lambda: self._changeTheme(name = "elena"))
        editmenu.add_command(label="Maggie", command=lambda: self._changeTheme(name = "maggie"))
        editmenu.add_command(label="John", command=lambda: self._changeTheme(name = "john"))
        editmenu.add_command(label="Helena", command=lambda: self._changeTheme(name = "helena"))
        menubar.add_cascade(label="Theme", menu=editmenu)
        
        # Tools
        toolsmenu = tk.Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="Hide Greens")
        toolsmenu.add_command(label="Hide Interviewer Text")
        toolsmenu.add_command(label="Iterate")
        toolsmenu.add_separator()
        toolsmenu.add_command(label="Edit index...")
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        
        self.root.config(menu=menubar)
        
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

