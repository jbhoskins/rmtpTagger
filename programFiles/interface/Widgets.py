# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Widgets that go in the sidebar

from tkinter import *


class TitledListBox:
    """A list box with an attached title. Has specific methods to interact with the Index."""
    def __init__(self, sidebar, color="green", padX = 20, font = "Verdana 20", text= "<Title Here>"):
        self.title = Label(sidebar, text = text, font = font, bg = color)
        self.title.pack(fill = Y, pady = 20)
        self.results = Listbox(sidebar, selectmode = SINGLE)
        self.results.pack(fill = X, padx = padX)

        self.entries = None

    def config(self, title_font = "Helvetica", text_font = "Helvetica", bg = "white", fg = "white"):
        """Set the fonts and colors."""
        self.title.config(bg = bg, font = title_font)
        self.results.config(bg = fg, font = text_font)

    def bind(self, button, command):
        """Passes along bind through to the tk.Listbox element."""
        self.results.bind(button, command)
 
    def populateTags(self, key, index):
        """Using the index and a key, fill the Listbox with each element returned from the index."""
        self.results.delete(0, END)
        
        try:
            self.entries = index.lookup(key)
        except KeyError:
            self.entries = []

        for item in self.entries:
            print(item.xmlID())
            self.results.insert(END, item.xmlID())

        self.results.selection_set(0)

    def getXmlId(self):
        """Returns the string that is selected in the listbox."""
        return self.results.get(self.results.curselection())
    
    def getSelection(self):
        """Returns a string of information about the current selection, pulled from the index."""
        selection = self.results.curselection()
        if selection is not ():
            return self.entries[selection[0]]
        else:
            return ""

class TitledTextBox:
    def __init__(self, sidebar, text = "<Title Here>"):
        self.title = Label(sidebar, text = text)
        self.title.pack(pady = 20)
        self.results = Text(sidebar, height = 10)
        self.results.pack(fill = X, padx = 20)
        self.results.config(state = DISABLED)

    def config(self, title_font = "Helvetica", text_font = "Helvetica", fg = "white", bg = "white"):
        """Set font and colors of the title, and text."""
        self.title.config(bg = bg, font = title_font)
        self.results.config(bg = fg, font = text_font, highlightbackground = fg)

    def updateInformation(self, string):
        """Insert the given string into the textbox."""
        self.results.config(state = NORMAL)
        self.results.delete(0.0, END)
        self.results.insert(END, string)
        self.results.config(state = DISABLED)

class Button_:
    def __init__(self, sidebar, textString, command):
        self.button = Button(sidebar, text = textString, command = command)
        self.button.pack(pady = 10)

    def config(self, font="Helvetica", bg="white"):
        """Set the font, and color of the button."""
        self.button.config(font = font, bg = bg, highlightbackground = bg)
