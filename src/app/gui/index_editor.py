""" A popup window that allows the user to add entries to a local, 'mini index'
    that can be sent out to merge with a universal copy. Incomplete."""

from app.gui.popup_window import PopupWindow
import tkinter as tk
from lxml import etree as ET


class IndexEditor(PopupWindow):
    """Popup window to facilitate editing the index."""
    def __init__(self, root):
        PopupWindow.__init__(self, root)

        self.root = ET.Element("Person")
        self.root.attrib["xmlid"] = "sashaprokhorov"

        self.update()

    def _add_widgets(self):
        """ Called in the superclass. Adds all widgets to the window."""
        self.txt = tk.Text(self, state=tk.DISABLED)
        self.attributeName = tk.Entry(self)
        self.attributeContent = tk.Entry(self)

        # Needed to stack buttons below other widgets.
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
        """Fill the text based on the xml tree made by the user as they add
        elements."""

        # Note: tags cannot be numbers.
        
        # This block catches if the fields are empty.
        try:
            new = ET.SubElement(self.root, self.attributeName.get())
            new.text = self.attributeContent.get()
        except:
            pass

        pretty_string = ET.tostring(self.root, pretty_print=True)

        # Needs to be reencoded for some reason - not working yet though
        # pretty_string = pretty_string.encode(encoding='UTF-8')

        self.txt.config(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.txt.insert("1.0", pretty_string)
        self.txt.config(state=tk.DISABLED)

    def submit(self):
        """Close the window."""
        # finalize stuff here
        self.grab_release()
        self.destroy()


def __pop():
    top = IndexEditor(root)

if __name__ == "__main__":

    root = tk.Tk()
    tk.Button(root, text="Pop", command=__pop).pack()
    root.mainloop()

