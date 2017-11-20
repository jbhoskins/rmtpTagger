import tkinter as tk

class PopupWindow(tk.Toplevel):
    """Abstract class for popup windows."""
    def __init__(self, root):
        tk.Toplevel.__init__(self)

        # These two lines turn off interaction with other windows besides the
        # popup.
        self.wait_visibility()
        self.grab_set()

        self._addWidgets()

    def _addWidgets(self):
        raise NotImplementedError("Method __add_widgets must be implemented!")
