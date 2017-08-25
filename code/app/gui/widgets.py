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
import tkinter.ttk as ttk
import app.gui.view_controller as view

from app.backend.keyword_instance import KeywordInstance
import app.backend.tag_templates as templates

class TagResults(tk.Listbox, view.Viewer, view.Stylable):
    """A ListBox of results pulled from the index."""
    
    def __init__(self, sidebar, scrollbar, app):
        tk.Listbox.__init__(self, sidebar, selectmode=tk.SINGLE, 
                            yscrollcommand=scrollbar.set)
        self._app = app

        # Used to determine which kind of update to do.
        self._oldEntry = None
        
    def populateTags(self, listOfXmlIds):
        """Populate the ListBox with every element in a list."""
        self.delete(0, tk.END)

        # Don't display anything if an empty list is passed.
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
        """Returns the string in the listbox corrosponding to the current
        selection."""
        selection = self.curselection()
        if selection != ():
            # Returned as tuple, only want 1st value.
            return self.get(self.curselection()[0])
        else:
            return ""

    def onClick(self, event):
        """Update the selected entry when an entry is clicked."""
        
        keywordTable = self._app.getKeywordTable()
        
        keywordTable.getCurrentEntry()["selectedEntry"] =\
            self.curSelection() - 1

        keywordTable.notifyViewersRedraw()
    
    def update(self):
        """Redraw the widget based on the state of the program."""
       
        keywordTable = self._app.getKeywordTable()

        currentEntry = keywordTable.getCurrentEntry()
        print("IN DUDE, CURRENT ENTRY IS:", currentEntry.selectionIndex())
       
        # Makes sure not to repopulate everything unless the current entry has
        # been changed.
        if self._oldEntry != currentEntry:
            print("Ignoring update...")
            self.populateTags([entry.getValue("__xml:id__") for entry in currentEntry.entries()])
            self._oldEntry = currentEntry

        self.selection_clear(0, tk.END)
        print("SEL:", currentEntry.selectionIndex())
        if currentEntry.selectionIndex() is not None:
            self.selection_set(currentEntry.selectionIndex() + 1)
        else:
            self.selection_set(0)

        self.see(currentEntry.selectionIndex() + 1)

    def style(self, styles):
        self.config(font=styles.f_subtitle, bg=styles.c_2)
        

class TagInformationField(tk.Text, view.Viewer, view.Stylable):
    """ Display information about the current selection in TagResults."""
    
    def __init__(self, sidebar, app):
        tk.Text.__init__(self, sidebar)
        self.config(state=tk.DISABLED)
        self._app = app

    def _updateInformation(self, string):
        """ Display information about the item selected in TagResults."""
        self.config(state = tk.NORMAL)
        self.delete(0.0, tk.END)
        self.insert(tk.END, string)
        self.config(state = tk.DISABLED)
    
    def update(self):
        """Redraw the widget based on the state of the program."""

        keywordTable = self._app.getKeywordTable()

        currentEntry = keywordTable.getCurrentEntry()
        currentSelection = currentEntry["selectedEntry"]
       
        print("Current sel:", currentSelection)
        if currentSelection == -1:
            string = ""
        else:
            string = str(currentEntry.selection())
        
        self._updateInformation(string)

    def style(self, styles):
        self.config(font=styles.f_text, bg=styles.c_2,
                highlightbackground=styles.c_2)

class CurrentTagField(tk.Label, view.Viewer, view.Stylable):
    """A label that shows the xml:id of the current selection of the possible
    tags."""
    def __init__(self, sidebar, app):
        tk.Label.__init__(self, sidebar, text="Current:")
        self._app = app

    def update(self):
        """Redraw the widget based on the state of the program."""

        keywordTable = self._app.getKeywordTable()

        selectionIndex = keywordTable.getCurrentEntry().selectionIndex()
        
        if selectionIndex == -1:
            string = "NO TAG"
        else:
            string =\
            str(keywordTable.getCurrentEntry().selection().getValue("__xml:id__"))
        
        string = "Current:  " + string
#        string += u" \u2713" # Testing confirmed check mark
        self.config(text=string)

    def style(self, styles):
        self.config(font=styles.f_button, bg=styles.c_2,
                highlightbackground=styles.c_2)

class TagPreviewField(tk.Label, view.Viewer, view.Stylable):
    """Shows a preview of how the xml tags around the current selecion will
    look."""
    def __init__(self, sidebar, app):
        tk.Label.__init__(self, sidebar, text="Preview:")
        self._app = app

        # Will need updating after changes to templates.
        self._templates = templates.TemplateIndex()

    def update(self):
        """Redraw the widget based on the current state of the program."""

        keywordTable = self._app.getKeywordTable()
        
        selectionIndex = keywordTable.getCurrentEntry().selectionIndex()
        
        if selectionIndex == -1:
            string = ""
        else:

            currentEntry = keywordTable.getCurrentEntry()

            template = currentEntry.selection().getValue("template")
            if template is "":
                tag = self._templates.lookup("default")
            else:
                tag = self._templates.lookup(template.lower())

            frontTag = tag.getFront() % tuple([currentEntry.selection().getValue(x)\
                for x in tag.getArguments()])
            backTag = tag.getBack()
        
            string = "Preview:  " + frontTag + currentEntry.string() + backTag
        self.config(text=string)

    def style(self, styles):
        self.config(bg=styles.c_2, highlightbackground=styles.c_2)

class AllTaggedResultsTable(ttk.Treeview, view.Viewer, view.Stylable):
    def __init__(self, parent, app):
        headings = ("#", "word", u"\u2713")
        ttk.Treeview.__init__(self, parent, columns=headings, show="headings")

        self._app = app

        for col in headings:
            self.heading(col, text=col.title())

        self.column("#", width=35, stretch=False)
        self.column("word", width=0, stretch=True)
        self.column(u"\u2713", width=20, stretch=False)

        self.unbind("<Up>")
        self.unbind("<Down>")

    def onClick(self, event):
        
        index = int(self.focus()) - 1

        self._app.getKeywordTable().jumpTo(index)

    def update(self):
        keywordTable = self._app.getKeywordTable()

        for row in self.get_children():
            self.delete(row)

        keywordTableIndex = 0
        rowIndex = 1
        for entry in keywordTable:
            keywordTableIndex += 1
            if entry["unambiguous"]: continue

            confirmedCheck = ""
            if entry["confirmed"]: confirmedCheck = u"\u2713"

            self.insert("", tk.END, str(keywordTableIndex), values=("%d" %
                rowIndex, entry.string(), confirmedCheck))
            rowIndex += 1

        self.selection_add(str(keywordTable.getCurrentIndex() + 1))
