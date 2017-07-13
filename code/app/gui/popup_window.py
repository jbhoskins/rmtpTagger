import tkinter as tk

class PopupWindow(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self)
        self.grab_set()

        self._addWidgets()

    def _addWidgets(self):
        raise NotImplementedError("Method _addWidgets must be implemented!")
