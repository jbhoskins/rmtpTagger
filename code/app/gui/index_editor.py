 # A popup window that allows the user to add entries to a local, "mini index"
 # that can be sent out to merge with a universal copy.

import tkinter as tk

class IndexEditor(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.grab_set()

        self._addWidgets()

    def _addWidgets(self):
        self.txt = tk.Text(self)
        self.txt.insert("1.0", "Sample Index entry:\n\n\n<person xml:id=\"aronofsky\">\n\t<role>director</role>\n\t<surname>Aronofsky</surname>\n\t<forename>Darren</forename>\n\t<gender>m</gender>\n\t<nationality>USA</nationality>\n\t<keys>\n\t\t<key>аронофски</key>\n\t</keys>\n</person>\n\nNO CHANGES ACTUALLY MADE ON SUBMIT")
        self.txt.pack()
        tk.Button(self, text="submit", command=self.submit).pack()

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

