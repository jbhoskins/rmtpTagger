
from app.gui.popup_window import PopupWindow
import tkinter as tk
import tkinter.messagebox

import app.backend.tag_templates as templates

class TemplateEditor(PopupWindow):
    """A popup window that gives access to the template configuration file. """
    def __init__(self, root):
        # This widget might benefit from the observer pattern as well.
        self._templateIndex = templates.TemplateIndex()
        PopupWindow.__init__(self, root)

    
    def _addWidgets(self):
        """ Called in superclass, adds all widgets to itself."""
        self.text = tk.Text(self)
        self.listBox = tk.Listbox(self)
        self.listBox.bind("<ButtonRelease-1>", self.update)
        
        self.listBox.pack(side=tk.LEFT)
        self.text.pack(side=tk.LEFT)
        tk.Button(self, text="add", command=self.addTag).pack(side=tk.LEFT)
        tk.Button(self, text="edit", command=self.editTag).pack(side=tk.LEFT)
        tk.Button(self, text="delete", command=self.deleteTag).pack(side=tk.LEFT)
        tk.Button(self, text="ok", command=self.close).pack(side=tk.LEFT)

        for tagName in self._templateIndex.getNames():
            self.listBox.insert(tk.END, tagName)

        self.listBox.selection_set(0)
        self.update()

    def update(self, event=None):
        """Update the text widget based on the user's selection in the
        listbox."""
        # Event needed for the click
        self.text.delete("1.0", tk.END)
        selection = self.listBox.curselection()[0] # bug here, returns a tup
        self.text.insert("1.0",
                str(self._templateIndex.getValues()[selection]))

    def editTag(self):
        """Opens another popup window that allows the user to edit the selected
        template."""
        selection = self.listBox.curselection()[0]
        
        tmp = AddTemplateEditor(self, self._templateIndex, selection)
        
        # get the values of the selected template to fill the defaults of the
        # new popup window
        name = self._templateIndex.getNames()[selection]
        frontTag = self._templateIndex.getValues()[selection].getFront()
        endTag = self._templateIndex.getValues()[selection].getBack()
        arguments = self._templateIndex.getValues()[selection].getArguments()

        
        tmp.setDefaults(name, frontTag, endTag, arguments)

    def updateTags(self):
        """populate the listbox with the names of the templates in the
        template index."""

        self.listBox.delete(0, tk.END)

        for tagName in self._templateIndex.getNames():
            self.listBox.insert(tk.END, tagName)

    def close(self):
        """Write the current index to file, and close the popup window."""
        
        f = open("../META/custom_tags.txt", "w")
        f.write(self._templateIndex.getFileString())
        f.close()
        print("Successfully updated tags")

        # grab_release allows the user to iteract with other windows again.
        self.grab_release()
        self.destroy()

    def deleteTag(self):
        """Delete the currently selected template."""
        
        # This actually can be undone if we add a cancel button - this is
        # probably a better solution.
        if tk.messagebox.askquestion("Delete Warning", "Are you sure you want\
        to delete this template? This cannot be undone.") == "no":
            return
        
        selection = self.listBox.curselection()[0]
        self._templateIndex.deleteTemplate(selection)
        self.updateTags()

    def addTag(self):
        """Open a popup window that allows the user to insert values for a new
        template."""
        AddTemplateEditor(self, self._templateIndex)


class AddTemplateEditor(PopupWindow):
    """Popup window that allows the user to edit or create a new template."""
    def __init__(self, root, templateIndex, selection = None):
        self._templateIndex = templateIndex
        self._parent = root
        self._selection = selection
        PopupWindow.__init__(self, root)

    def _addWidgets(self):
        """Populate the popup window with widgets."""
        
        # Called in the superclass
        self.nameEntry = tk.Entry(self)
        self.frontTagEntry = tk.Entry(self)
        self.endTagEntry = tk.Entry(self)
        self.argumentsEntry = tk.Entry(self)
        
        tk.Label(self, text="Template name:").pack()
        self.nameEntry.pack()
        tk.Label(self, text="Front Tag:").pack()
        self.frontTagEntry.pack()
        tk.Label(self, text="End Tag:").pack()
        self.endTagEntry.pack()
        tk.Label(self, text="Arguments:").pack()
        self.argumentsEntry.pack()
        tk.Button(self, text="ok", command=self.close).pack()

    def setDefaults(self, name, frontTag, endTag, arguments):
        """Populate the fields of the popup window with the values of the
        currently selected values, for the case that you are editing a
        currently existing template."""
        self.nameEntry.insert(0, name)
        self.frontTagEntry.insert(0, frontTag)
        self.endTagEntry.insert(0, endTag)
        self.argumentsEntry.insert(0, " ".join(arguments))
    
    def close(self):
        """Commit the changes made by the user to the data structure, and close
        the window."""

        if self._selection == None:
            # Meaning that you are appending
            self._templateIndex.addTemplate(self.nameEntry.get(), 
                self.frontTagEntry.get(), self.endTagEntry.get(),
                self.argumentsEntry.get().split())
        else:
            # Meaning you are editing
            self._templateIndex.replaceTemplate(self._selection,
                self.nameEntry.get(), self.frontTagEntry.get(),
                self.endTagEntry.get(), self.argumentsEntry.get().split())
        
        self._parent.updateTags()
        
        # finalize stuff here
        self.grab_release()
        self.destroy()

# ------------------ for debugging ---------------------
def __pop():
    top = TemplateEditor(root)

if __name__ == "__main__":

    root = tk.Tk()

    tk.Button(root, text="Pop", command=__pop).pack()

    root.mainloop()

