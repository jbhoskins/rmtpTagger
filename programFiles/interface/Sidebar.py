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
        self.text = text
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
        self.tagButton = Button_(self.parent, "Tag Document", lambda: self.text.findAndFlag(self.index))
        self.tagResults = TitledListBox(self.parent, text="Tag Results")
        self.confirmButton = Button_(self.parent, "Confirm", lambda: self.text.insertAround(self.tagResults.getXmlId()))
        self.indexResults = TitledTextBox(self.parent, text = "Tag Information")
        self.tagResults.populateTags("", self.index)

    def styleWidgets(self):
        self.tagButton.config(font = self.font2, bg = self.color2)
        self.confirmButton.config(font = self.font2, bg = self.color2)
        self.tagResults.config(title_font = self.font1, text_font = self.font2, fg = self.color1, bg = self.color2)
        self.indexResults.config(title_font = self.font1, text_font = self.font2, fg = self.color1, bg = self.color2)

    def updateTags(self, event):
        self.text.cacheWord(event)
        word = self.text.getCache()[0]
        print(word)
        self.tagResults.populateTags(str(word).lower(), self.index)
        self.updateInfo(0) # Zero passes as event
        
    def updateInfo(self, event):
        entry = self.tagResults.getSelection()
        self.indexResults.updateInformation(str(entry))
        


