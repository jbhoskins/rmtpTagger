# Sidebar.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""A sidebar for the main application.  This holds the current tags 
available for the selected word in a list box and allows the user to 
choose theappropriate tag, based on context.  It shows the current tag 
selected for the current word.


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""

import sys
sys.path.insert(0, '../')

import tkinter as tk
import widgets

class Sidebar(tk.PanedWindow):
    def __init__(self, parentFrame, fText, index, styles):
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)
        
        self.parent = parentFrame       
        self.index = index
        self.fText = fText
        self.styles = styles
        self.exportTags = []
        self.bg = self.styles.c_2
        
        self._addWidgets()
        self._styleWidgets()

    def _addWidgets(self):
        """Declare and pack all the widgets used in the sidebar."""
        self.currentTag = widgets.CurrentTagField(self)
        self.tagInfoField = widgets.TagInformationField(self)
        self.tagLabel = tk.Label(self, text="Tag Results")
        
        # Frame is to keep scrollbar next to text.
        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame)
        self.tagResults = widgets.TagResults(frame, scrollbar)
        scrollbar.config(command=self.tagResults.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tagResults.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        screenHeight = self.styles.dimensions[1]
        self.add(self.tagLabel)
        self.add(self.currentTag, sticky=tk.N)
        self.add(frame, height=screenHeight // 3)
        self.add(self.tagInfoField, height=screenHeight // 3)        
        
        # Initialize to empty fields.
        self.tagResults.populateTags([])

    def showTagResultsOnClick(self, event):
        # Update the cache.
        self.fText.cacheWord(event)
        # Zero passes as event.
        self.showTagResults()

    def showTagResults(self):
        """Update the tagResults widget (inherits from ListBox) with the 
        word in the FramedText cache. Automatically fills the 
        tagInfoField with first tag.
        """
        cache = self.fText.getCache()
        print("cce", cache)
        self.tagResults.populateTags(
            [entry.xmlId() for entry in cache.entries()])

        if cache.selectionIndex() is not None:
            self.tagResults.selection_set(cache.selectionIndex() + 1)
            self.currentTag.update(cache.selection().xmlId())
        else:
            self.currentTag.update("NO TAG")
            self.tagResults.selection_set(0)
   
    def showSelectionInfo(self, event):
        """Get the selection from the tagResults box and display its 
        information in tagInfoField.
        """
        selectionIndex = self.tagResults.curSelection()
        cache = self.fText.keywordTable.currentVal()
        
        if selectionIndex == 0:
            cache["selectedEntry"] = None
            ndx = 0
            string = ""
        else:
            cache["selectedEntry"] = selectionIndex - 1
            ndx = cache.selectionIndex() + 1
            string = cache.selection()
        
        self.tagInfoField.updateInformation(string)
        self.tagResults.selection_set(ndx)

        # Catches when cache.selectedEntry is None
        try:
            string = cache.selection().xmlId()
        except TypeError:
            string = "NO TAG"

        self.currentTag.update(string)
        
        
    #-----------------------------------------------
    # Styling.
    
    def _styleWidgets(self):
        """Apply the styles from styleSheet() to the 
        widgets.
        """
        self.config(bg=self.bg)
        self.tagLabel.config(font=self.styles.f_subtitle, bg=self.bg)
        
        self.currentTag.config(
            font=self.styles.f_button, bg=self.bg, 
            highlightbackground=self.bg)

        self.tagResults.config(font=self.styles.f_button, bg=self.bg)
        self.tagInfoField.config(
            font=self.styles.f_text, bg=self.bg, 
            highlightbackground=self.bg)        

    def configStyles(self, styles):
        """Change the desired stylesheet."""
        self.styles = styles
        self._styleWidgets()
