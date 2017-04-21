# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

from Index import *
from FramedText import *
from Widgets import *
import tkinter as tk

class Sidebar(tk.PanedWindow):
    """ Container to hold all the widgets that are active in the sidebar. """
    def __init__(self, parentFrame, fText, index, styles):
        tk.PanedWindow.__init__(self, parentFrame, orient = tk.VERTICAL)
        self.parent = self        
        self.index = index
        self.fText = fText
        self.styles = styles

        # Not super slever implementation, but gets the job done
        self.exportTags = []
        
        self.addWidgets()
        self._styleWidgets()

    def addWidgets(self):
        """ Declare and pack all the widgets used in the sidebar. """
        self.currentTag = CurrentTagField(self)
        self.tagInfoField = TagInformationField(self)
        self.tagLabel = tk.Label(self, text="Tag Results")

        
        # Frame needed to keep scrollbar next to text, that's why tagResults treated spcl
        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame)
        self.tagResults = TagResults(frame, scrollbar)
        scrollbar.config(command=self.tagResults.yview)
        scrollbar.pack(side = tk.RIGHT, fill=tk.Y)
        self.tagResults.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        screenHeight = self.styles.dimensions[1]
        self.add(self.tagLabel)
        self.add(frame, height = screenHeight // 3)
        self.add(self.tagInfoField, height = screenHeight // 3)
        self.add(self.currentTag, sticky=tk.N)
        

        # Initialize to empty fields
        self.tagResults.populateTags([])

    def showTagResultsOnClick(self, event):
        # Update the cache
        self.fText.cacheWord(event)
        # zero passes as event
        self.showTagResults()

    def showTagResults(self):
        """ Update the tagResults widget (inherits from ListBox) with the word in the
            FramedText cache. Automatically fills the tagInfoField with first tag. """
        
        cache = self.fText.getCache()
        print("cce", cache)
        self.tagResults.populateTags([entry.xmlId() for entry in cache.entries()])

        if cache.selectionIndex() is not None:
            self.tagResults.selection_set(cache.selectionIndex() + 1)
            self.currentTag.update(cache.selection().xmlId())
        else:
            self.currentTag.update("NO TAG")
            self.tagResults.selection_set(0)

                            
    def showSelectionInfo(self, event):
        """ Get the selection from the tagResults box and display its information in
            tagInfoField. """
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
    #------------------------------------------------------------------
    # Styling
    
    def _styleWidgets(self):
        """ Apply the styles from styleSheet() to the widgets. """
        self.parent.config(bg = self.styles.c_2)
        self.tagLabel.config(font=self.styles.f_subtitle, bg=self.styles.c_2)
        
        self.currentTag.config(font = self.styles.f_button, bg = self.styles.c_2, highlightbackground = self.styles.c_2)
#        self.confirmButton.config(font = self.styles.f_button, bg = self.styles.c_2, highlightbackground = self.styles.c_2)
        
        self.tagResults.config(font = self.styles.f_button, bg = self.styles.c_2)
        self.tagInfoField.config(font = self.styles.f_text, bg = self.styles.c_2, highlightbackground = self.styles.c_2)        

    def configStyles(self, styles):
        self.styles = styles
        self._styleWidgets()

    #-------------------------------------------------------------------
