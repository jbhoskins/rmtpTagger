# LeftSidebar.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""A legend for the main application.  This holds the key for colors 
used in the text tagging application.
"""

import tkinter as tk
import app.gui.widgets as widgets


class LeftSidebar(tk.PanedWindow):
    def __init__(self, parent_frame, app):
        tk.PanedWindow.__init__(self, parent_frame, orient=tk.VERTICAL)

        self.__app = app
        self.__add_widgets()

    def __add_widgets(self):
        """Declare and pack all the widgets used in the sidebar."""

        self._legend = widgets.Legend(self)
        self.add(self._legend)

        self.tree = widgets.AllTaggedResultsTable(self, self.__app)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.add(self.tree)

    def style(self, styles):
        self.config(bg=styles.c_2)
