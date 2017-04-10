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

    def __init__(self, parentFrame, text, index, styles):
        self.parent = parentFrame
        self.index = index
        self.fText = text
        self.styles = styles

        self.styleSheet()
        self.createWidgets()
        self.styleWidgets()

    def styleSheet(self):
        self.font1 = self.styles[0]
        self.font2 = self.styles[1]
        self.color1 = self.styles[2]
        self.color2 = self.styles[3]

    def createWidgets(self):
        self.tagResults = TagResults(self.parent)
        self.confirmButton = tk.Button(self.parent, text="Confirm", command=lambda: self.fText.insertAroundCache(self.tagResults.curSelection()))
        self.tagInfoField = TagInformationField(self.parent)
        
        tk.Label(self.parent, text="Tag Results", font=self.font1, bg=self.color2).pack()
        self.tagResults.pack()
        self.confirmButton.pack()
        self.tagInfoField.pack()
        
        self.tagResults.populateTags([])

    def styleWidgets(self):
        self.confirmButton.config(font = self.font2, bg = self.color2)
        self.tagResults.config(font = self.font2, bg = self.color2)
        self.tagInfoField.config(font = self.font2, bg = self.color2)

    def showTagResults(self, event):
        self.fText.cacheWord(event)
        cache = self.fText.getCache()
        self.tagInfoField.updateCache(cache)
                    
        self.tagResults.populateTags([entry.xmlId() for entry in cache.entries()])
        self.showSelectionInfo(0) # Zero passes as event
        
    def showSelectionInfo(self, event):
        selectionIndex = self.tagResults.curSelection()
        
        self.tagInfoField.updateInformation(selectionIndex)
        


