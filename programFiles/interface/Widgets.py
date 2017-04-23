# Widgets.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""Widgets that go in the sidebar of the main application:  
     TagResults (tk.Listbox)
     TagInformationField (tk.Text)
     CurrentTagField (tk.Label)
     Table (tk.Text)


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""

import tkinter as tk

from WordCache import *


class TagResults(tk.Listbox):
    """Create a ListBox of results pulled from the index."""
    
    def __init__(self, sidebar, scrollbar):
        tk.Listbox.__init__(self, sidebar, selectmode=tk.SINGLE, 
                            yscrollcommand=scrollbar.set)
        
    def populateTags(self, listOfXmlIds):
        """Populate the ListBox with every element in a list."""
        self.delete(0, tk.END)
        if listOfXmlIds != []:
            self.insert(tk.END, "NO TAG")
        for item in listOfXmlIds:
            self.insert(tk.END, item)

    def curSelection(self):
        """ Return an integer corrosponding to the value currently 
        selected in the listbox.
        """
        userSelection = self.curselection()
        if userSelection != ():
            # Returned as tuple, only want 1st value.
            return self.curselection()[0] 
        else:
            return 0

    def xmlIdSelection(self):
        selection = self.curselection()
        if selection != ():
            # Returned as tuple, only want 1st value.
            return self.get(self.curselection()[0])
        else:
            return ""
        

class TagInformationField(tk.Text):
    """ Display information about the current selection in TagResults."""
    
    def __init__(self, sidebar):
        tk.Text.__init__(self, sidebar)        
        self.cache = Cache()
        self.config(state=tk.DISABLED)

    def updateInformation(self, string):
        """ Display information about the item selected in TagResults."""
        self.config(state = tk.NORMAL)
        self.delete(0.0, tk.END)
        self.insert(tk.END, string)
        self.config(state = tk.DISABLED)


class CurrentTagField(tk.Label):
    def __init__(self, sidebar):
        tk.Label.__init__(self, sidebar, text="Current:")

    def update(self, string):
        string = "Current:  " + string
        self.config(text=string)


class Table(tk.Text):
    def __init__(self, frame):
        tk.Text.__init__(self, frame)



















