# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Widgets that go in the sidebar

import tkinter as tk
from WordCache import *

class TagResults(tk.Listbox):
    """ The box of results pulled from the index"""
    def __init__(self, sidebar):
        tk.Listbox.__init__(self, sidebar, selectmode = tk.SINGLE)        

    def populateTags(self, listOfXmlIds):
        """ Populate the ListBox with every element in a list."""
        self.delete(0, tk.END)
        
        for item in listOfXmlIds:
            self.insert(tk.END, item)

        self.selection_set(0)

    def curSelection(self):
        """ Returns an integer corrosponding to the value is selected in the listbox. """
        selection = self.curselection()
        if selection != (): # When empty, return ()
            return self.curselection()[0] # Returned as a tuple, only want the 1st value.
        else:
            return 0

class TagInformationField(tk.Text):
    def __init__(self, sidebar):
        tk.Text.__init__(self, sidebar)        
        self.cache = Cache()
        
        self.config(state = tk.DISABLED)

    def updateCache(self, cache):
        self.cache = cache

    def updateInformation(self, selectionIndex):
        """Insert the given string into the textbox."""
        
        self.config(state = tk.NORMAL)
        self.delete(0.0, tk.END)
        self.insert(tk.END, str(self.cache.entries()[selectionIndex]))
        self.config(state = tk.DISABLED)

