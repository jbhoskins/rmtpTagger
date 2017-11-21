# Sidebar.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu

"""A sidebar for the main application.  This holds the current tags 
available for the selected word in a list box and allows the user to 
choose theappropriate tag, based on context.  It shows the current tag 
selected for the current word.


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""

import tkinter as tk
import app.gui.widgets as widgets


class RightSidebar(tk.PanedWindow):
    """Container to hold all widgets that will appear on the right sidebar."""
    def __init__(self, parentFrame, fText, dim, app):
        tk.PanedWindow.__init__(self, parentFrame, orient=tk.VERTICAL)

        self.__dimensions = dim
        self.__app = app

        self.__add_widgets()

    def __add_widgets(self):
        """Declare and pack all the widgets used in the sidebar."""
        # Public to better facilitate MVC pattern, be careful with them.
        self.current_tag = widgets.CurrentTagField(self, self.__app)
        self.tag_info_field = widgets.TagInformationField(self, self.__app)
        self.tag_label = tk.Label(self, text="Tag Results")

        self.preview = widgets.TagPreviewField(self, self.__app)
        
        # Frame is to keep scrollbar next to text.
        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame)
        self.tag_results = widgets.TagResults(frame, scrollbar, self.__app)
        scrollbar.config(command=self.tag_results.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tag_results.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        screen_height = self.__dimensions[1]
        self.add(self.tag_label)
        self.add(self.current_tag, sticky=tk.N)
        self.add(frame, height=screen_height // 3)
        self.add(self.tag_info_field, height=screen_height // 2)
        self.add(self.preview, sticky=tk.N)

        # Initialize to empty fields.
        self.tag_results.populate_tags([])

    def style(self, styles):
        self.config(bg=styles.c_2)
        self.tag_label.config(font=styles.f_subtitle, bg=styles.c_2)