# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Widgets that go in the sidebar

import tkinter as tk
from WordCache import *

class TagResults(tk.Listbox):
    """ The ListBox of results pulled from the index. """
    def __init__(self, sidebar):
        scrollbar = tk.Scrollbar(sidebar)
        tk.Listbox.__init__(self, sidebar, selectmode = tk.SINGLE, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def populateTags(self, listOfXmlIds):
        """ Populate the ListBox with every element in a list. """
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

    def xmlIdSelection(self):
        selection = self.curselection()
        if selection != (): # When empty, return ()
            return self.get(self.curselection()[0]) # Returned as a tuple, only want the 1st value.
        else:
            return ""
        

class TagInformationField(tk.Text):
    """ Displays information about the current selection in TagResults. """
    def __init__(self, sidebar):
        tk.Text.__init__(self, sidebar)        
        self.cache = Cache()
        
        self.config(state = tk.DISABLED)

    def updateCache(self, cache):
        """ Put a new list of entries in the cache. """
        self.cache = cache

    def updateInformation(self, selectionIndex):
        """ Display information about the item selected in TagResults. """
        
        self.config(state = tk.NORMAL)
        self.delete(0.0, tk.END)
        self.insert(tk.END, str(self.cache.entries()[selectionIndex]))
        self.config(state = tk.DISABLED)

class CurrentTagField(tk.Label):
    def __init__(self, sidebar):
        tk.Label.__init__(self, sidebar, text="Current:")


    def update(self, string):
        string = "Current:  " + string
        self.config(text=string)





