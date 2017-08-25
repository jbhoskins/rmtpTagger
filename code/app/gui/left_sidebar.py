# LeftSidebar.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""A legend for the main application.  This holds the key for colors 
used in the text tagging application.


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""


import sys
sys.path.insert(0, '../')

import tkinter as tk
import tkinter.ttk as ttk
import app.gui.widgets as widgets


class LeftSidebar(tk.PanedWindow):
    def __init__(self, parentFrame, styles, app):
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)

        self._app = app
        self._addWidgets()
#        self._styleLegend()
#        self._packLegend()
        
        
    def _addWidgets(self):
        """Declare and pack all the widgets used in the sidebar."""
        self.l1 = ttk.Label(self, text = "Interviewer text")
        self.l2 = ttk.Label(self, text = "Interviewee text")
        self.l3 = ttk.Label(self, text = "Single key")
        self.l4 = ttk.Label(self, text = "Multiple Keys")

        self.add(self.l1)
        self.add(self.l2)
        self.add(self.l3)
        self.add(self.l4)


        self.tree = widgets.AllTaggedResultsTable(self, self._app)
        self.tree.pack(fill=tk.BOTH, expand=True)

#        self.tree.pack()
        self.add(self.tree)


    #--------------------------------------
    # Styling.
    
#    def _styleLegend(self):
#        """Apply the styles from styleSheet() to the widgets."""        
#        self.config(
#            bg=self.styles.c_1, highlightbackground=self.styles.h_single, 
#            pady=10)
#        self.title.config(
#            text="Legend", font=self.styles.f_title, bg=self.styles.c_2, 
#            pady=10)        
        
#        self.l1.config(
#            font=self.styles.f_text, bg=self.styles.c_1, 
#            fg=self.styles.h_interviewer, pady=5)
#        self.l2.config(
#            font=self.styles.f_text, bg=self.styles.c_1, fg="black", pady=5)
#        self.l3.config(
#            font=self.styles.f_text, bg=self.styles.h_single, pady=5)
#        self.l4.config(
#            font=self.styles.f_text, bg=self.styles.h_multi, pady=5)

#    def configStyles(self, styles):
#        """Change the desired stylesheet."""
#        self.styles = styles
#        self._styleLegend()
#        self._packLegend()

