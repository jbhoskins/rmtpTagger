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

from index import Index
from entry_window import EntryWindow
from text_view import TextView
from left_sidebar import LeftSidebar
from menubar import Menubar
from sidebar import Sidebar
from stylesheet import StyleSheet


class Application:
    def __init__(self):
        """Initialize and style root; set styles, widgets, and frames, 
        make sure app opens properly.
        """
        self.root = tk.Tk()
        
        # Pull window to the top, but not permanently.
        self.root.lift()
        self.root.call('wm', 'attributes', '.', '-topmost', True)
        self.root.after_idle(
            self.root.call, 'wm', 'attributes', '.', '-topmost', False)
        self.root.focus_set()
        
        # Set title, dim, index, & paned window.
        self.root.wm_title("William & Mary Index Tagger")
        self.dim = ( self.root.winfo_screenwidth(), 
                     self.root.winfo_screenheight() )
        self.mainFrame = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL, sashrelief=tk.GROOVE, 
            height=self.dim[1], opaqueresize=False)
        self.index = Index("../../META/index.xml")
        
        # Set styles, widgets, frame, and bind keys.
        self._setStyles()
        self._addWidgets()
        self.mainFrame.pack_propagate(0)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        self._bindKeys()
        self._styleApp()


    #-------------------------------------------------------------------
    # Styling.

    def _getDim(self):
        """Return dimensions of the screen."""

    def _setStyles(self, name="bella"):
        """Set the formatting of the application."""
        self.styles = StyleSheet(name, dim=self.dim)
        
    def _styleApp(self):
        """Style the application."""
        self.root.config(bg=self.styles.c_1)
        
        self.legend.configStyles(styles=self.styles)
        self.legend.config(bg=self.styles.c_2)
        
        self.fText.configStyles(styles=self.styles)
        
        self.sidebar.configStyles(styles=self.styles)    
        #self.sidebarFrame.config(bg=self.styles.c_2)
        
    def _changeTheme(self, name):
        """Change the theme of the app."""
        self._setStyles(name)
        self._styleApp()    


    #-------------------------------------------------------------------
    # Create and place frames, widgets, and menus
        
    def _addWidgets(self):
        """Create and fill the text box, sidebar and menu."""
        screenWidth = self.styles.dimensions[0]
        self.legend = LeftSidebar(self.mainFrame, self.styles)
        self.mainFrame.add(
            self.legend, width=(screenWidth // 8), stretch="never")

        tframe = tk.Frame(self.mainFrame)
        scrollbar = tk.Scrollbar(tframe)
        self.fText = TextView(tframe, self.index, self.styles, scrollbar)
        scrollbar.config(command=self.fText.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.fText.pack(side = tk.LEFT, fill=tk.BOTH, expand=1)
        self.mainFrame.add(tframe, width=(screenWidth // 2), stretch="always")

        self.sidebar = Sidebar(
            self.mainFrame, self.fText, self.index, self.styles)
        self.mainFrame.add(
            self.sidebar, width=(screenWidth // 4), stretch="never")
        
        self.menubar = Menubar(self)
        self._makeTagMenu()

    def _bindKeys(self):
        """Bind all clicks and key presses to commands."""
        self.fText.tag_bind(
            "foundWord", "<Button-1>", self.sidebar.showTagResultsOnClick)
        self.sidebar.tagResults.bind(
            "<ButtonRelease-1>", self.sidebar.showSelectionInfo)
        
        self.root.bind("<Right>", self.moveRight)
        self.root.bind("<Left>", self.moveLeft)
        self.root.bind("<Up>", self.prevTag)
        self.root.bind("<Down>", self.nextTag)

        self.fText.tag_bind(
            "interviewee", "<ButtonRelease-3>", self._showTagMenu)
        self.fText.tag_bind(
            "interviewee", "<ButtonRelease-2>", self._showTagMenu)
            
        self.sidebar.tagResults.populateTags([])

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

    #-------------------------------------------------------------------
    # Hover (in progress)

    def on_enter(self, event):
        self.fText.tag_add("cur", self.cur_line, self.cur_line + 1) 

    def on_leave(self, enter):
        self.fText.tag_add("reg", self.cur_line, self.cur_line + 1)


    #-------------------------------------------------------------------
    # The right click menu.

    def _makeTagMenu(self):
        """Define the menu that will show when
        right-clicked.
        """
        self.menuFrame = tk.Frame(self.root)
        self.tagMenu = tk.Menu(self.menuFrame, tearoff=0)
        self.tagMenu.add_command(label="tag here", command=print("tag"))
        self.tagMenu.add_command(label="Add Tag", command=self._showTagScreen)

    def _showTagMenu(self, event):
        """Show the Menu pop up when right-clicked."""
        self.tagMenu.post(event.x_root, event.y_root)
    
    def _showTagScreen(self):
        """Display the New Tag Window."""
        word = self.fText.getString()
        self.add_tag = EntryWindow(self.root, word, self.styles)


    #-------------------------------------------------------------------
    # Launch app

    def launch(self):
        """Launch the program."""
        self.root.mainloop()
        

#-----------------------------------------------------------------------
# Main section.

if __name__ == "__main__":
    app = Application()
    app.launch()

