# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

from Index import *
from FramedText import *
from Widgets import *
import tkinter as tk

class Sidebar:
    """ Container to hold all the widgets that are active in the sidebar. """
    def __init__(self, parentFrame, fText, index, styles):
        self.parent = parentFrame
        self.index = index
        self.fText = fText
        self.styles = styles

        # Not super slever implementation, but gets the job done
        self.exportTags = []
        
        self._setFrames()
        self._createWidgets()
        self._styleWidgets()

    def _setFrames(self):
        """ Set the frames to be the right size, based on the screen height."""
        # Should be a part of the stylesheet

        
        screenHeight = self.styles.dimensions[1]
        print(screenHeight)

        tagResultsHeight = screenHeight // 3 + 20
        infoHeight = screenHeight // 3

        self.tagFrame = tk.Frame(self.parent, height=tagResultsHeight)
        self.infoFrame = tk.Frame(self.parent, height=infoHeight)

        self.currentTagFrame = tk.Frame(self.parent)


    def _createWidgets(self):
        """ Declare and pack all the widgets used in the sidebar. """
        self.tagResults = TagResults(self.tagFrame)
        self.currentTag = CurrentTagField(self.currentTagFrame)
#        self.confirmButton = tk.Button(self.parent, text="Confirm", command=lambda: self.fText.insertAroundCache(self.tagResults.curSelection()))
#        self.confirmButton = tk.Button(self.parent, text="Confirm", command=lambda: self.currentTag.update(self.tagResults.xmlIdSelection()))
#        self.confirmButton = tk.Button(self.parent, text="Confirm", command=self.fText.keywordTable.printTable)
        self.tagInfoField = TagInformationField(self.infoFrame)
        self.tagLabel = tk.Label(self.parent, text="Tag Results")
        
        self.tagLabel.pack()
        
        self.tagFrame.pack_propagate(0) 
        self.tagFrame.pack(side=tk.TOP, fill = tk.X)
        self.tagResults.pack(fill = tk.BOTH, expand=True)
        
#        self.confirmButton.pack()
        
        self.infoFrame.pack_propagate(0) 
        self.infoFrame.pack(side=tk.TOP, fill = tk.X)
        self.tagInfoField.pack(fill = tk.BOTH, expand=True)
        
        self.currentTagFrame.pack(fill = tk.X)
        self.currentTag.pack(side=tk.LEFT, padx = 30)
        
        # Initialize to empty fields
        self.tagResults.populateTags([])

    def showTagResults(self, event):
        """ Update the tagResults widget (inherits from ListBox) with the word in the
            FramedText cache. Automatically fills the tagInfoField with first tag. """
        
        # Update the cache
        self.fText.cacheWord(event)

        cache = self.fText.getCache()                    
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
        self.parent.config(bg = self.styles.c_2, highlightbackground = self.styles.c_2)
        self.tagLabel.config(font=self.styles.f_subtitle, bg=self.styles.c_2)
        
        self.currentTagFrame.config(bg = self.styles.c_2, highlightbackground = self.styles.c_2)
        self.currentTag.config(font = self.styles.f_button, bg = self.styles.c_2, highlightbackground = self.styles.c_2)
#        self.confirmButton.config(font = self.styles.f_button, bg = self.styles.c_2, highlightbackground = self.styles.c_2)
        
        self.tagResults.config(font = self.styles.f_button, bg = self.styles.c_2)
        self.tagInfoField.config(font = self.styles.f_text, bg = self.styles.c_2, highlightbackground = self.styles.c_2)        

    def configStyles(self, styles):
        self.styles = styles
        self._styleWidgets()

    #-------------------------------------------------------------------
