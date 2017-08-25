# Sidebar.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""A sidebar for the main application.  This holds the current tags 
available for the selected word in a list box and allows the user to 
choose theappropriate tag, based on context.  It shows the current tag 
selected for the current word.


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""

import sys
sys.path.insert(0, '../')

import tkinter as tk
import app.gui.widgets as widgets

class Sidebar(tk.PanedWindow):
    """Container to hold all widgets that will appear on the right sidebar."""
    def __init__(self, parentFrame, fText, dim, app):
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)
        
        self.parent = parentFrame       
        self.fText = fText
        self.dimensions = dim
        self.exportTags = []
#        self.bg = self.styles.c_2
        
        self._app = app

        self._addWidgets()
#       self._styleWidgets()

    def _addWidgets(self):
        """Declare and pack all the widgets used in the sidebar."""
        self.currentTag = widgets.CurrentTagField(self, self._app)
        self.tagInfoField = widgets.TagInformationField(self, self._app)
        self.tagLabel = tk.Label(self, text="Tag Results")

        self.preview = widgets.TagPreviewField(self, self._app)
        
        # Frame is to keep scrollbar next to text.
        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame)
        self.tagResults = widgets.TagResults(frame, scrollbar,
                self._app)
        scrollbar.config(command=self.tagResults.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tagResults.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        screenHeight = self.dimensions[1]
        self.add(self.tagLabel)
        self.add(self.currentTag, sticky=tk.N)
        self.add(frame, height=screenHeight // 3)
        self.add(self.tagInfoField, height=screenHeight // 2)        
        self.add(self.preview, sticky=tk.N)

        
        # Initialize to empty fields.
        self.tagResults.populateTags([])

    def style(self, styles):
        self.config(bg=styles.c_2)
        self.tagLabel.config(font=styles.f_subtitle, bg=styles.c_2)

        
    #-----------------------------------------------
    # Styling.
    
#    def _styleWidgets(self):
#        """Apply the styles from styleSheet() to the 
#        widgets.
#        """
#        self.config(bg=self.bg)
#        self.tagLabel.config(font=self.styles.f_subtitle, bg=self.bg)
        
#        self.currentTag.config(
#            font=self.styles.f_button, bg=self.bg, 
#            highlightbackground=self.bg)

#        self.tagResults.config(font=self.styles.f_button, bg=self.bg)
#        self.tagInfoField.config(
#            font=self.styles.f_text, bg=self.bg, 
#            highlightbackground=self.bg)        

#        self.preview.config(
#                bg=self.bg,
#                highlightbackground=self.bg)

#    def configStyles(self, styles):
#        """Change the desired stylesheet."""
#        self.styles = styles
#        self._styleWidgets()
