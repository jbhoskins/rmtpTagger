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

        self.styleSheet()
        self.createWidgets()
        self.styleWidgets()

    def styleSheet(self):
        """ Assigns the style variables that will be used in the sidebar. Will be replaced
            by a style class in the future. """
        self.font1 = self.styles[0]
        self.font2 = self.styles[1]
        self.color1 = self.styles[2]
        self.color2 = self.styles[3]

    def createWidgets(self):
        """ Declare and pack all the widgets used in the sidebar. """
        self.tagResults = TagResults(self.parent)
        self.confirmButton = tk.Button(self.parent, text="Confirm", command=lambda: self.fText.insertAroundCache(self.tagResults.curSelection()))
        self.tagInfoField = TagInformationField(self.parent)
        
        tk.Label(self.parent, text="Tag Results", font=self.font1, bg=self.color2).pack()
        self.tagResults.pack()
        self.confirmButton.pack()
        self.tagInfoField.pack()
        
        # Initialize to empty fields
        self.tagResults.populateTags([])

    def styleWidgets(self):
        """ Apply the styles from styleSheet() to the widgets. """
        self.confirmButton.config(font = self.font2, bg = self.color2)
        self.tagResults.config(font = self.font2, bg = self.color2)
        self.tagInfoField.config(font = self.font2, bg = self.color2)

    def showTagResults(self, event):
        """ Update the tagResults widget (inherits from ListBox) with the word in the
            FramedText cache. Automatically fills the tagInfoField with first tag. """
        self.fText.cacheWord(event)
        cache = self.fText.getCache()
        self.tagInfoField.updateCache(cache)
                    
        self.tagResults.populateTags([entry.xmlId() for entry in cache.entries()])
        self.showSelectionInfo(0) # Zero passes as event
        
    def showSelectionInfo(self, event):
        """ Get the selection from the tagResults box and display its information in
            tagInfoField. """
        selectionIndex = self.tagResults.curSelection()
        
        self.tagInfoField.updateInformation(selectionIndex)
        


