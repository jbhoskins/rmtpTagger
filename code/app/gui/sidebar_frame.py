# SidebarFrame.py

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Created on April 23, 2017.
# Authored by Margaret Swift: meswift@email.wm.edu
# Co-authored by John Hoskins: jbhoskins@email.wm.edu


"""A sidebar frame for the main application, used to hold sidebar
widgets for the app.

"""

import tkinter as tk


class SidebarFrame(tk.PanedWindow):

    def __init__(self, parentFrame=None, title='TITLE', styles=None):
        
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)
        self.title = tk.Label(title)
        self.parent = parentFrame
        self.styles = styles
        self.bg = self.styles.c_2
        self._styleWidgets()
    
    def _styleWidgets(self):
        """Apply the styles from stylesheet to the widgets."""
        self.parent.config(bg=self.bg)
        self.title.config(
            font=self.f_title, bg=self.bg, highlightbackground=self.bg)
        
        for widget in self.panes():
            widget.config(bg=self.bg)
            
    # ------------------------------------------------------------------
    # Public methods
    
    def add(self, widget):
        """Add widgets to the sidebar publicly."""
        self.add(widget)
        widget.config(
            bg=self.bg, highlightbackground=self.bg, 
            font=self.styles.f_text)
        
    def configStyles(self, styles):
        """Change the desired stylesheet publicly."""
        self.styles = styles
        self._styleWidgets()