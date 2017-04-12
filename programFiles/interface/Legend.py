# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

import tkinter as tk

#---------------------------------------------------------------------------
class Legend:
    """ Container to hold the legend """

    def __init__(self, parentFrame, styles):
        self.parent = parentFrame
        self.styles = styles

        self._setFrame()
        self._createLegend()
        self._styleLegend()
        self._packLegend()
        
        
    def _setFrame(self):
        self.title = tk.Label(self.parent, text = "Legend", pady = 10)        
        self.legendFrame = tk.Frame(self.parent, height = 500)
        
    def _createLegend(self):
        """ Declare and pack all the widgets used in the sidebar. """
        
        self.l1 = tk.Label(self.legendFrame, text = "Interviewer text")
        self.l2 = tk.Label(self.legendFrame, text = "Interviewee text")
        self.l3 = tk.Label(self.legendFrame, text = "Single key")
        self.l4 = tk.Label(self.legendFrame, text = "Multiple Keys")       

    #------------------------------------------------------------------
    # Styling
    
    def _styleLegend(self):
        """ Apply the styles from styleSheet() to the widgets. """        
        self.title.config(font = self.styles.f_title, bg = self.styles.c_2, pady = 10)
        self.legendFrame.config(bg = self.styles.c_1, highlightbackground = self.styles.h_single, pady = 10)
        
        self.l1.config(font = self.styles.f_text, bg = self.styles.c_1, fg = self.styles.h_interviewer, pady = 5)
        self.l2.config(font = self.styles.f_text, bg = self.styles.c_1, fg = "black", pady = 5)
        self.l3.config(font = self.styles.f_text, bg = self.styles.h_single, pady = 5)
        self.l4.config(font = self.styles.f_text, bg = self.styles.h_multi, pady = 5)
                

    def configStyles(self, styles):
        self.styles = styles
        self._styleLegend()
        self._packLegend()

    def _packLegend(self):        
        self.title.pack()        
        self.legendFrame.pack()
        
        self.l1.pack()
        self.l2.pack()
        self.l3.pack()
        self.l4.pack()        
        
        
    #-------------------------------------------------------------------
        