
from app.gui.popup_window import PopupWindow
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox

import app.backend.tag_templates as templates

class TemplateEditor(PopupWindow):
    """A popup window that gives access to the template configuration file. """
    def __init__(self, root):
        # This widget might benefit from the observer pattern as well.
        self._templateIndex = templates.TemplateIndex()
        PopupWindow.__init__(self, root)
    
        self.bind("<Double-Button-1>", self.editTag)

    def _addWidgets(self):
        """ Called in superclass, adds all widgets to itself."""

        headings = ("name", "front tag", "back tag", "arguments")
        self.tree = ttk.Treeview(self, columns=headings, show="headings")

        for col in headings:
            self.tree.heading(col, text=col.title())
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Need this frame to pack the buttons neatly centered below the table.
        buttonFrame = tk.Frame(self)

        tk.Button(buttonFrame, text="add",
                command=self.addTag).pack(side=tk.LEFT)
        tk.Button(buttonFrame, text="edit", command=self.editTag).pack(side=tk.LEFT)
        tk.Button(buttonFrame, text="delete",
                command=self.deleteTag).pack(side=tk.LEFT)
        tk.Button(buttonFrame, text="ok", command=self.closeAndCommit).pack(side=tk.LEFT)
        tk.Button(buttonFrame, text="cancel", command=self.close).pack(side=tk.LEFT)

        buttonFrame.pack(expand=True)
        self.updateTags()

    def editTag(self, event=None):
        """Opens another popup window that allows the user to edit the selected
        template."""
        # Note: event passed as it is needed for the binding to mouseclick. 
        selection = self.tree.focus()
        index = self.tree.index(selection)
        print("SELECTION IS>>>>>>>>>>>>>>>>>>>>>>", index)
        
        tmp = AddTemplateEditor(self, self._templateIndex, index)
        
        # get the values of the selected template to fill the defaults of the
        # new popup window
        name = self._templateIndex.get_names()[index]
        frontTag = self._templateIndex.get_values()[index].get_front()
        endTag = self._templateIndex.get_values()[index].get_back()
        arguments = self._templateIndex.get_values()[index].get_arguments()

        
        tmp.setDefaults(name, frontTag, endTag, arguments)

    def updateTags(self):
        """populate the listbox with the names of the templates in the
        template index."""

        # Delete all the templates in the view.
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Populate the tree view with templates.
        for template in self._templateIndex.get_templates():
            self.tree.insert("", tk.END, text=template[0],
                             values=(template[0],) + template[1].get_tuple())


    def closeAndCommit(self):
        """Write the current index to file, and close the popup window."""
        
        f = open("../META/tagTemplatesBackup.txt", "w")
        f.write(self._templateIndex.get_file_string())
        f.close()
        print("Successfully updated tags")

        # grab_release allows the user to iteract with other windows again.
        self.grab_release()
        self.destroy()

    def close(self):
        """Closes the window."""
        # grab_release allows the user to iteract with other windows again.
        self.grab_release()
        self.destroy()

    def deleteTag(self):
        """Delete the currently selected template."""
        
        # This actually can be undone if we add a cancel button - this is
        # probably a better solution.
        if tk.messagebox.askquestion("Delete Warning", "Are you sure you"+\
            "want to delete this template? This cannot be undone.") == "no":
            return
        
        selection = self.tree.focus()
        index = self.tree.index(selection)
        self._templateIndex.delete_template(index)
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
       
        topFrame = tk.Frame(self)
        bottomFrame = tk.Frame(self)

        # Called in the superclass
        leftFrame = tk.Frame(topFrame)
        rightFrame = tk.Frame(topFrame)

        tk.Label(leftFrame, text="Template name:").pack()
        tk.Label(leftFrame, text="Front Tag:").pack()
        tk.Label(leftFrame, text="End Tag:").pack()
        tk.Label(leftFrame, text="Arguments:").pack()
        
        self.nameEntry = tk.Entry(rightFrame, width=30)
        self.frontTagEntry = tk.Entry(rightFrame, width=30)
        self.endTagEntry = tk.Entry(rightFrame, width=30)
        self.argumentsEntry = tk.Entry(rightFrame, width=30)
       
        self.nameEntry.pack(fill=tk.X, expand=True)
        self.frontTagEntry.pack(fill=tk.X, expand=True)
        self.endTagEntry.pack(fill=tk.X, expand=True)
        self.argumentsEntry.pack(fill=tk.X, expand=True)
       
        topFrame.pack(fill= tk.X, expand=True)
        bottomFrame.pack()

        leftFrame.pack(side=tk.LEFT)
        rightFrame.pack(side=tk.LEFT, fill=tk.X, expand=True)
         
        tk.Button(bottomFrame, text="ok",
                command=self.close).pack()

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

        # Make sure that there are the right amount of arguments to fit the
        # number of '%s' get_string formatting spots in the front tag.
        if len(self.argumentsEntry.get().split()) !=\
                self.frontTagEntry.get().count(r"%s"):
            tk.messagebox.showwarning("Argument Error", "The number of"+\
                    " arguments you supplied was not equal to the number of"+\
                    r" '%s' symbols in the front tag.")
            return


        if self._selection == None:
            # Meaning that you are appending
            self._templateIndex.add_template(self.nameEntry.get(),
                                             self.frontTagEntry.get(), self.endTagEntry.get(),
                                             self.argumentsEntry.get().split())
        else:
            # Meaning you are editing
            self._templateIndex.replace_template(self._selection,
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

