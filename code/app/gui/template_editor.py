
from app.gui.popup_window import PopupWindow
import tkinter as tk
import tkinter.messagebox

import app.backend.tag_templates as templates

class TemplateEditor(PopupWindow):
    def __init__(self, root):
        self._templateIndex = templates.TemplateIndex()
        PopupWindow.__init__(self, root)

    
    def _addWidgets(self):
        """ Called in superclass"""
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
        # Event needed for the click
        self.text.delete("1.0", tk.END)
        selection = self.listBox.curselection()[0] # bug here, returns a tup
        self.text.insert("1.0",
                str(self._templateIndex.getValues()[selection]))

    def editTag(self):
        selection = self.listBox.curselection()[0]
        
        tmp = AddTemplateEditor(self, self._templateIndex, selection)
        
        name = self._templateIndex.getNames()[selection]
        frontTag = self._templateIndex.getValues()[selection].getFront()
        endTag = self._templateIndex.getValues()[selection].getBack()

        
        tmp.setDefaults(name, frontTag, endTag)

    def updateTags(self):

        self.listBox.delete(0, tk.END)

        for tagName in self._templateIndex.getNames():
            self.listBox.insert(tk.END, tagName)

    def close(self):
        
        f = open("../META/custom_tags.txt", "w")
        f.write(self._templateIndex.getFileString())
        f.close()
        print("Successfully updated tags")

        # finalize stuff here
        self.grab_release()
        self.destroy()

    def deleteTag(self):
        
        # This actually can be undone if we add a cancel button - this is
        # probably a better solution.
        if tk.messagebox.askquestion("Delete Warning", "Are you sure you want\
        to delete this template? This cannot be undone.") == "no":
            return
        
        selection = self.listBox.curselection()[0]
        self._templateIndex.deleteTemplate(selection)
        self.updateTags()

    def addTag(self):
        AddTemplateEditor(self, self._templateIndex)


class AddTemplateEditor(PopupWindow):
    def __init__(self, root, templateIndex, selection = -1):
        self._templateIndex = templateIndex
        self._parent = root
        self._selection = selection
        PopupWindow.__init__(self, root)

    def _addWidgets(self):
        
        
        self.nameEntry = tk.Entry(self)
        self.frontTagEntry = tk.Entry(self)
        self.endTagEntry = tk.Entry(self)
        
        
        tk.Label(self, text="Template name:").pack()
        self.nameEntry.pack()
        tk.Label(self, text="Front Tag:").pack()
        self.frontTagEntry.pack()
        tk.Label(self, text="End Tag:").pack()
        self.endTagEntry.pack()
        tk.Button(self, text="ok", command=self.close).pack()

    def setDefaults(self, name, frontTag, endTag):
        self.nameEntry.insert(0, name)
        self.frontTagEntry.insert(0, frontTag)
        self.endTagEntry.insert(0, endTag)
    
    def close(self):

        if self._selection == -1:
            # Meaning that you are apppending
            self._templateIndex.addTemplate(self.nameEntry.get(), 
                self.frontTagEntry.get(), self.endTagEntry.get())
        else:
            # Meaning you are editing
            self._templateIndex.replaceTemplate(self._selection,
                self.nameEntry.get(), self.frontTagEntry.get(),
                self.endTagEntry.get())
        
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

