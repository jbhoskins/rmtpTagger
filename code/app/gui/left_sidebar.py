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
    def __init__(self, parentFrame, app):
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)

        self._app = app
        self._addWidgets()
#        self._styleLegend()
#        self._packLegend()
        
        
    def _addWidgets(self):
        """Declare and pack all the widgets used in the sidebar."""

        self._legend = Legend(self)
        self.add(self._legend)


        self.tree = widgets.AllTaggedResultsTable(self, self._app)
        self.tree.pack(fill=tk.BOTH, expand=True)

#        self.tree.pack()
        self.add(self.tree)

    def style(self, styles):
        self.config(bg=styles.c_2)
#        self.title.config(
#            text="Legend", font=self.styles.f_title, bg=self.styles.c_2, 
#            pady=10)        
        

class Legend(tk.Frame):
    def __init__(self, parent): 
        tk.Frame.__init__(self, parent)
        self.l1 = ttk.Label(self, text = "Interviewer text")
        self.l2 = ttk.Label(self, text = "Interviewee text")
        self.l3 = ttk.Label(self, text = "Single key")
        self.l4 = ttk.Label(self, text = "Multiple Keys")

        self.l1.pack()
        self.l2.pack()
        self.l3.pack()
        self.l4.pack()

    def style(self, styles):
        self.config(bg=styles.c_2)

        self.l1.config(
            font=styles.f_text, background=styles.c_1, 
            foreground=styles.h_interviewer)
        self.l2.config(
            font=styles.f_text, background=styles.c_1, foreground="black")
        self.l3.config(
            font=styles.f_text, background=styles.h_single)
        self.l4.config(
            font=styles.f_text, background=styles.h_multi)

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

