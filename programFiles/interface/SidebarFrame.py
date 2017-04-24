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

LAST EDIT:

Margaret, 4/23/17

Created this template so that we can use it on both sides of the main
application.
"""

import sys
sys.path.insert(0, '../')

import tkinter as tk


class SidebarFrame(tk.PanedWindow):
    
    class Blank():
        def __init__(self, parentFrame):
            tk.Label.__init__(self, parentFrame)
            
    
    
    def __init__(self, parentFrame=None, title='TITLE', styles=None):
        
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)
        self.title = tk.Label(title)
        self.parent = parentFrame
        self.widget1 = None
        self.widget2 = None
        self.widget3 = None
        self.widget4 = None
        
        self.styles = styles
        self.bg = self.styles.c_2
        
        self._createBlanks()
        self._packWidgets()
        self._styleWidgets()
        
    
    def _createBlanks(self):
        """Create blank spaces to stand for empty widgets."""
        
        

    def _packWidgets(self):
        """Pack all the widgets used in the sidebar."""
        self.title.pack()
        self.widget1.pack()
        self.widget2.pack()
        self.widget3.pack()
    
    def _styleWidgets(self):
        """Apply the styles from stylesheet to the widgets."""
        self.parent.config(bg=self.bg)
        self.title.config(
            font=self.f_title, bg=self.bg, highlightbackground=self.bg)
        
        self.widget1.config(
            font=self.f_text, bg=self.bg, highlightbackground=self.bg)
        self.widget2.config(
            font=self.f_text, bg=self.bg, highlightbackground=self.bg)        
        self.widget3.config(
            font=self.f_text, bg=self.bg, highlightbackground=self.bg)    
        self.widget4.config(
            font=self.f_text, bg=self.bg, highlightbackground=self.bg)
        
        
    # ------------------------------------------------------------------
    # Public methods
    
    def addWidget(self, widget):
        """Add widgets to the sidebar publicly."""
        if self.widget1 == None:
            self.widget1 = widget
        elif self.widget2 == None:
            self.widget2 = widget   
        elif self.widget3 == None:
            self.widget3 = widget 
        else:
            # Will this work? If so, change this public method so that
            # this is the only bit.
            widget.pack() 

    def configStyles(self, styles):
        """Change the desired stylesheet publicly."""
        self.styles = styles
        self._styleWidgets()