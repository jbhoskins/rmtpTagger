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
import app.gui.view_controller as view

from app.backend.keyword_instance import KeywordInstance


class TagResults(tk.Listbox, view.Viewer):
    """Create a ListBox of results pulled from the index."""
    
    def __init__(self, sidebar, scrollbar, keywordTable):
        tk.Listbox.__init__(self, sidebar, selectmode=tk.SINGLE, 
                            yscrollcommand=scrollbar.set)
        self._keywordTable = keywordTable

        # Used to determine which kind of update to do.
        self._oldEntry = None
        
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

    def onClick(self, event):
        self._keywordTable.getCurrentEntry()["selectedEntry"] =\
            self.curSelection() - 1

        self._keywordTable.notifyViewersRedraw()
    
    def update(self):
        """Update the tagResults widget (inherits from ListBox) with the 
        word in the FramedText cache. Automatically fills the 
        tagInfoField with first tag.
        """
        
        # confusing terminology here - fix it. One entry is an entry in the
        # keywordTable, the other is each possible tag per entry.
        currentEntry = self._keywordTable.getCurrentEntry()
       
        # Makes sure not to repopulate everything unless the current entry has
        # been changed.
        if self._oldEntry != currentEntry:
            self.populateTags([entry.getValue("__xml:id__") for entry in currentEntry.entries()])
            self._oldEntry = currentEntry

        self.selection_clear(0, tk.END)
        print("SEL:", currentEntry.selectionIndex())
        if currentEntry.selectionIndex() is not None:
            self.selection_set(currentEntry.selectionIndex() + 1)
        else:
            self.selection_set(0)

        self.see(currentEntry.selectionIndex() + 1)
        

class TagInformationField(tk.Text, view.Viewer):
    """ Display information about the current selection in TagResults."""
    
    def __init__(self, sidebar, keywordTable):
        tk.Text.__init__(self, sidebar)
        self.config(state=tk.DISABLED)
        self._keywordTable = keywordTable

    def _updateInformation(self, string):
        """ Display information about the item selected in TagResults."""
        self.config(state = tk.NORMAL)
        self.delete(0.0, tk.END)
        self.insert(tk.END, string)
        self.config(state = tk.DISABLED)
    
    def update(self):
        """Get the selection from the tagResults box and display its 
        information in tagInfoField.
        """

        currentEntry = self._keywordTable.getCurrentEntry()
        currentSelection = currentEntry["selectedEntry"]
       
        print("Current sel:", currentSelection)
        if currentSelection == -1:
            string = ""
        else:
            string = str(currentEntry.selection())
        
        self._updateInformation(string)

class CurrentTagField(tk.Label, view.Viewer):
    def __init__(self, sidebar, keywordTable):
        tk.Label.__init__(self, sidebar, text="Current:")
        self._keywordTable = keywordTable

    def update(self):
        
        selectionIndex = self._keywordTable.getCurrentEntry().selectionIndex()
        
        if selectionIndex == -1:
            string = "NO TAG"
        else:
            string =\
            str(self._keywordTable.getCurrentEntry().selection().getValue("__xml:id__"))
        
        string = "Current:  " + string
        self.config(text=string)

