# coding=UTF-8

# Application.py

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""Our main application for the RMTP tagging project.  Application.py
holds all the widgets that are used to tag interviews in XML.  This was
made to replace manual tagging.  Exports to XML or TEI Standard depending
on preference.

This user interface program assigns tags to any keyword that is found in
the interview and that matches a keyword in the XML index created by 
Sasha and Elena Prokhorov.  The index includes various points of interest,
such as film titles, actor or director names, national cinemas, etc.  

The main goal of this project is to investigate the frequency of mentions
of certain people, places, and films by interviewees.  In Russian, this
is particularly difficult, given the various forms of declensions of 
words.  For example:  Саша, Саши, Саше, Сашу are all declined forms of 
the name Sasha.  In order to count all these as single instances of the 
same word, instead of four different words, we use XML to tag all as
<rs type="person" key="sasha">.  Our program automatically tags keywords
as the most common usage of the word.  However, many names or words 
could reference two or more different things.  An interviewee could say
the name "Smith" and be talking about Adam Smith or Maggie Smith.
Therefore, our program allows the user to choose the approrpriate tag
in cases of ambiguity, based on context clues.


LAST EDIT:

Margaret, 4/22/17
------------------------------------------------------------------------
(1) PEP-8 styles require code to be no longer than 79 characters. I have 
also implemented a new system for arguments:  If arguments all fit on 
one line, that's fine. If any would go over the break line, then we must 
move all to a new line, indented by 4 more spaces than the previous. 
Ending delimiters stay on the last line, ie ")" wouldn't get its own 
line.


(2) An exception to the above: function definitions have all arguments 
that can fit on one line, then remaining arguments go on the next line & 
lined up with the opening delimiter:

def this_is_a_long_function(argument_1, argument_2, argument_3,
                            argument_4)

If a single argument would still run over the breakline, then hanging 
indent is moved back four spaces until there is enough room to encompass 
the single longest argument.


(3) Spacing around operators: Should have one space around operators, no 
space around arguments or parameter values:
a = 5                      NOT    a=5
a.pack(side=left)     NOT    a.pack(side = left)


(4) The style guide says that comments or docstrings should be 72 
characters


(5) Imports should be grouped in the following order:

standard library imports
related third party imports
local application/library specific imports

and then in alphabetical order.

(6) Two spaces between classes, one between functions, two between 
groups of functions.


(7) Docstrings:
Should be commands, not descriptions, and should not have a blank line 
afterwards.  No space between quotes and characters. Keep end three 
quotes on same line if docstring is only one line (even if quotes would 
go over 72 characters), but if the docstring is multiline, put the 
quotes on their own line (ie, this docstring).  All docstrings and 
comments should be full sentences with punctuation and capitalization.


(8)

"""


import sys
sys.path.insert(0, '../')

import tkinter as tk
from tkinter import filedialog # do we need this?

from app.backend.keyword_instance_table import KeywordInstanceTable
from app.gui.entry_window import EntryWindow
from app.gui.text_view import TextView
from app.gui.left_sidebar import LeftSidebar
from app.gui.menubar import Menubar
from app.gui.sidebar import Sidebar
from app.gui.stylesheet import StyleSheet

from app.backend.keyword_instance_table import KeywordInstanceTable

class Application:
    def __init__(self):
        """Initialize and style root; set styles, widgets, and frames, 
        make sure app opens properly.
        """
        self._root = tk.Tk()
        
        # Pull window to the top, but not permanently.
        self._root.lift()
        self._root.call('wm', 'attributes', '.', '-topmost', True)
        self._root.after_idle(
            self._root.call, 'wm', 'attributes', '.', '-topmost', False)
        self._root.focus_set()
        
        # Set title, dim, index, & paned window.
        self._root.wm_title("William & Mary Index Tagger")
        self._dim = ( self._root.winfo_screenwidth(), 
                     self._root.winfo_screenheight() )
        self._mainFrame = tk.PanedWindow(
            self._root, orient=tk.HORIZONTAL, sashrelief=tk.GROOVE, 
            height=self._dim[1], opaqueresize=False)

        # Initialize the table used by the program
        self._keywordTable = KeywordInstanceTable()
        
        # Set styles, widgets, frame, and bind keys.
        self._setStyles()
        self._addWidgets()
        self._registerViewers()
        self._mainFrame.pack_propagate(0)
        self._mainFrame.pack(fill=tk.BOTH, expand=True)
        self._bindKeys()
        self._styleApp()

    #-------------------------------------------------------------------
    # Styling.

    def _getDim(self):
        """Return dimensions of the screen."""

    def _setStyles(self, name="bella"):
        """Set the formatting of the application."""
        self._styles = StyleSheet(name, dim=self._dim)
        
    def _styleApp(self):
        """Style the application."""
        self._root.config(bg=self._styles.c_1)
        
        self._legend.configStyles(styles=self._styles)
        self._legend.config(bg=self._styles.c_2)
        
        self._textView.configStyles(styles=self._styles)
        
        self._sidebar.configStyles(styles=self._styles)    
        #self.sidebarFrame.config(bg=self.styles.c_2)
        
    def _changeTheme(self, name):
        """Change the theme of the app."""
        self._setStyles(name)
        self._styleApp()    


    #-------------------------------------------------------------------
    # Create and place frames, widgets, and menus
        
    def _addWidgets(self):
        """Create and fill the text box, sidebar and menu."""
        screenWidth = self._styles.dimensions[0]
        self._legend = LeftSidebar(self._mainFrame, self._styles)
        self._mainFrame.add(
            self._legend, width=(screenWidth // 8), stretch="never")

        tframe = tk.Frame(self._mainFrame)
        scrollbar = tk.Scrollbar(tframe)
        self._textView = TextView(tframe, self._keywordTable, self._styles, scrollbar)
        scrollbar.config(command=self._textView.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._textView.pack(side = tk.LEFT, fill=tk.BOTH, expand=1)
        self._mainFrame.add(tframe, width=(screenWidth // 2), stretch="always")

        self._sidebar = Sidebar(
            self._mainFrame, self._textView, self._styles, self._keywordTable)
        self._mainFrame.add(
            self._sidebar, width=(screenWidth // 4), stretch="never")
        
        self._menubar = Menubar(self)
        self._makeTagMenu()

    def _bindKeys(self):
        """Bind all clicks and key presses to commands."""
        self._textView.tag_bind(
            "foundWord", "<Button-1>", self._textView.onClick)
        self._sidebar.tagResults.bind(
            "<ButtonRelease-1>", self._sidebar.tagResults.onClick)
        
        self._root.bind("<Right>", self.moveRight)
        self._root.bind("<Left>", self.moveLeft)
        self._root.bind("<Up>", self.prevTag)
        self._root.bind("<Down>", self.nextTag)

 #       self.fText.tag_bind(
 #           "interviewee", "<ButtonRelease-3>", self._showTagMenu)
 #       self.fText.tag_bind(
 #           "interviewee", "<ButtonRelease-2>", self._showTagMenu)
            
#        self.sidebar.tagResults.populateTags([])

# ------------------- Methods bound to keys ----------------------
    def moveRight(self, event):
        self._keywordTable.nextValidEntry()
        self._keywordTable.notifyViewersRedraw() # These redraw methods could
                                                 # arguably be called within kt
    def moveLeft(self, event):
        self._keywordTable.previousValidEntry()
        self._keywordTable.notifyViewersRedraw()

    def prevTag(self, event):
        self._keywordTable.prevTag()
        self._keywordTable.notifyViewersRedraw()
        
    def nextTag(self, event):
        self._keywordTable.nextTag()
        self._keywordTable.notifyViewersRedraw()
    
    def _registerViewers(self):
        
        # Register the viewers
        self._keywordTable.registerViewer(self._textView)
        self._keywordTable.registerViewer(self._sidebar.tagResults)
        self._keywordTable.registerViewer(self._sidebar.currentTag)
        self._keywordTable.registerViewer(self._sidebar.tagInfoField)

    #-------------------------------------------------------------------
    # Hover (in progress)

    def on_enter(self, event):
        self.textView.tag_add("cur", self.cur_line, self.cur_line + 1) 

    def on_leave(self, enter):
        self.textView.tag_add("reg", self.cur_line, self.cur_line + 1)

    #-------------------------------------------------------------------
    # The right click menu.

    def _makeTagMenu(self):
        """Define the menu that will show when
        right-clicked.
        """
        self._menuFrame = tk.Frame(self._root)
        self._tagMenu = tk.Menu(self._menuFrame, tearoff=0)
        self._tagMenu.add_command(label="tag here", command=print("tag"))
        self._tagMenu.add_command(label="Add Tag", command=self._showTagScreen)

    def _showTagMenu(self, event):
        """Show the Menu pop up when right-clicked."""
        self._tagMenu.post(event.x_root, event.y_root)
    
    def _showTagScreen(self):
        """Display the New Tag Window."""
        word = self._textView.getString()
        self._add_tag = EntryWindow(self.root, word, self.styles)


    #-------------------------------------------------------------------
    # Launch app

    def launch(self):
        """Launch the program."""
        self._root.mainloop()
        

#-----------------------------------------------------------------------
# Main section.

if __name__ == "__main__":
    app = Application()
    app.launch()
