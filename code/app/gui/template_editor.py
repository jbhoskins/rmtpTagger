
from app.gui.popup_window import PopupWindow
import tkinter as tk

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
        tk.Button(self, text="add").pack(side=tk.LEFT)
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

    def close(self):
        
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

