 # A popup window that allows the user to add entries to a local, "mini index"
 # that can be sent out to merge with a universal copy.

import tkinter as tk
from lxml import etree as ET

class IndexEditor(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.grab_set()

        self.root = ET.Element("Person")
        self.root.attrib["xmlid"] = "sashaprokhorov"

        self._addWidgets()
        self.update()

    def _addWidgets(self):
        self.txt = tk.Text(self, state=tk.DISABLED)
        self.attributeName = tk.Entry(self)
        self.attributeContent = tk.Entry(self)


        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side=tk.BOTTOM)
        
        # Pack everything
        self.txt.pack()
        tk.Label(self, text="Enter a tag name:").pack(side=tk.LEFT)
        self.attributeName.pack(side=tk.LEFT)
        tk.Label(self, text="Enter the tag content:").pack(side=tk.LEFT)
        self.attributeContent.pack(side=tk.LEFT, fill=tk.X)
        
        
        tk.Button(bottom_frame, text="submit", command=self.submit).pack(side=tk.BOTTOM)
        tk.Button(bottom_frame, text="update", command=self.update).pack(side=tk.BOTTOM)

    
    def addElement(self):
       pass
    
    
    def update(self):
        # Note: numbers cannot be tags
        
        # This block catches if the fields are empty.
        try:
            new = ET.SubElement(self.root, self.attributeName.get())
            new.text = self.attributeContent.get()
        except:
            pass

        pretty_string = ET.tostring(self.root, pretty_print=True)

        # Needs to be reencoded for some reason - not working yet tho
        # pretty_string = pretty_string.encode(encoding='UTF-8')

        self.txt.config(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.txt.insert("1.0", pretty_string)
        self.txt.config(state=tk.DISABLED)

    def submit(self):
        # finalize stuff here
        self.grab_release()
        self.destroy()



def __pop():
    top = IndexEditor(root)

if __name__ == "__main__":

    root = tk.Tk()

    tk.Button(root, text="Pop", command=__pop).pack()

    root.mainloop()

