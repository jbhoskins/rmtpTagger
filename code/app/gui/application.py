# coding=UTF-8

# Application.py

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""Our main application for the RMTP tagging project.  Application.py
holds all the widgets that are used to tag interviews in XML.  This was
made to replace manual tagging.  Exports to XML or TEI Standard depending
on preference.

This user interface program assigns tags to any keyword that is found in
the interview and that matches a keyword in the XML index created by 
Sasha and Elena Prokhorov.  The index includes various points of interest,
such as film titles, actor or director names, national cinemas, etc.  

The main goal of this project is to investigate the frequency of mentions
of certain people, places, and films by interviewees.  In Russian, this
is particularly difficult, given the various forms of declensions of 
words.  For example:  Саша, Саши, Саше, Сашу are all declined forms of 
the name Sasha.  In order to count all these as single instances of the 
same word, instead of four different words, we use XML to tag all as
<rs type="person" key="sasha">.  Our program automatically tags keywords
as the most common usage of the word.  However, many names or words 
could reference two or more different things.  An interviewee could say
the name "Smith" and be talking about Adam Smith or Maggie Smith.
Therefore, our program allows the user to choose the approrpriate tag
in cases of ambiguity, based on context clues.

"""


import sys
#sys.path.insert(0, '../')

import tkinter as tk
from tkinter import filedialog # do we need this?

from app.backend.keyword_instance_table import KeywordInstanceTable
from app.gui.entry_window import EntryWindow
from app.gui.text_view import TextView
from app.gui.left_sidebar import LeftSidebar
from app.gui.menubar import Menubar
from app.gui.sidebar import Sidebar
from app.gui.stylesheet import StyleSheet
from app.gui.splash_screen import SplashScreen

from app.backend.keyword_instance_table import KeywordInstanceTable


class Application:
    def __init__(self):
        """Initialize and style root; set styles, widgets, and frames, 
        make sure app opens properly.
        """
        # Withdraw hides all graphical elements, so that nothing is shown
        # partially loaded until everything is in place.
        self.__root = tk.Tk()
        self.__root.withdraw()
        self.__splash = SplashScreen(self.__root)
        
        # Pull window to the top, but not permanently.
        self.__root.lift()
        self.__root.call('wm', 'attributes', '.', '-topmost', True)
        self.__root.after_idle(
            self.__root.call, 'wm', 'attributes', '.', '-topmost', False)
        self.__root.focus_set()
        
        # Set title
        self.__root.wm_title("William & Mary Index Tagger")
        
        # Set the window icon. This has some cross platform issues.
#        icon =\
#        tk.PhotoImage(file=r"../META/cypher_alpha_32x32.png")
#        self._root.tk.call("wm", "iconphoto", self._root._w, "-default", icon)
        
        # Set dim, index, & paned window.
        self.__dim = (self.__root.winfo_screenwidth(),
                      self.__root.winfo_screenheight())
        self.__mainFrame = tk.PanedWindow(
            self.__root, orient=tk.HORIZONTAL, sashrelief=tk.GROOVE,
            height=self.__dim[1], opaqueresize=False)

        # Initialize the table used by the program
        self.__keyword_table = KeywordInstanceTable()
        
        # Declare the stylesheet
        self.__styler = StyleSheet(self.__dim)
        
        # Set styles, widgets, frame, and bind keys.
        self.__define_widgets()
        self.__register_viewers()
        self.__style_widgets()
        self.__add_widgets()
        self.__mainFrame.pack_propagate(0)
        self.__mainFrame.pack(fill=tk.BOTH, expand=True)
        self.bind_keys()

    def get_keyword_table(self):
        return self.__keyword_table

    def set_keyword_table(self, keyword_table):
        self.__keyword_table = keyword_table

    def get_text_view(self):
        return self.__text_view

    def get_styler(self):
        return self.__styler
    #-------------------------------------------------------------------
    # Styling.

    def get_root(self):
        return self.__root

    def __get_dim(self):
        """Return dimensions of the screen."""

    def __define_widgets(self):

        self.__left_sidebar = LeftSidebar(self.__mainFrame, self)
        
        self.__text_frame = tk.Frame(self.__mainFrame)
        scrollbar = tk.Scrollbar(self.__text_frame)
        self.__text_view = TextView(self.__text_frame, self, scrollbar)
        scrollbar.config(command=self.__text_view.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__text_view.pack(side = tk.LEFT, fill=tk.BOTH, expand=1)
        
        self.__right_sidebar = Sidebar(
            self.__mainFrame, self.__text_view, self.__dim, self)
 
        self.__menubar = Menubar(self)

    def __style_widgets(self):
        """Style the application."""
        self.__styler.changeTheme("bella")
        
#        self._legend.configStyles(styles=self._styles)
#        self._legend.config(bg=self._styles.c_2)
        
        
#        self._sidebar.configStyles(styles=self._styles)    
        #self.sidebarFrame.config(bg=self.styles.c_2)
        
    #-------------------------------------------------------------------
    # Create and place frames, widgets, and menus
        
    def __add_widgets(self):
        """Create and fill the text box, sidebar and menu."""
        screen_width = self.__dim[0]
        self.__mainFrame.add(
            self.__left_sidebar, width=(screen_width // 8), stretch="never")

        self.__mainFrame.add(self.__text_frame, width=(screen_width // 2), stretch="always")

        self.__mainFrame.add(
            self.__right_sidebar, width=(screen_width // 4), stretch="never")

    def bind_keys(self):
        """Bind all clicks and key presses to commands."""
        self.__text_view.tag_bind(
            "clickableWord", "<Button-1>", self.__text_view.on_click)
        self.__right_sidebar.tagResults.bind(
            "<ButtonRelease-1>", self.__right_sidebar.tagResults.on_click)
        self.__left_sidebar.tree.bind("<ButtonRelease-1>", self.__left_sidebar.tree.on_click)
        
        self.__root.bind("<Right>", self.__keyword_table.next_valid_entry)
        self.__root.bind("<Left>", self.__keyword_table.previous_valid_entry)
        self.__root.bind("<Up>", self.__keyword_table.prev_tag)
        self.__root.bind("<Down>", self.__keyword_table.next_tag)
        self.__root.bind("<Return>",
                         self.__keyword_table.toggle_confirm_current)

 #       self.fText.tag_bind(
 #           "interviewee", "<ButtonRelease-3>", self.__show_tag_menu)
 #       self.fText.tag_bind(
 #           "interviewee", "<ButtonRelease-2>", self.__show_tag_menu)

    def __register_viewers(self):
        """Attaches view objects to the keyword table, so that they will be
        updated when keywordTable is told up update its viewers."""
        
        # Register the viewers
        self.__keyword_table.register_viewer(self.__text_view)
        self.__keyword_table.register_viewer(self.__right_sidebar.tagResults)
        self.__keyword_table.register_viewer(self.__right_sidebar.currentTag)
        self.__keyword_table.register_viewer(self.__right_sidebar.tagInfoField)

        self.__keyword_table.register_viewer(self.__right_sidebar.preview)
        self.__keyword_table.register_viewer(self.__left_sidebar.tree)

        # Styling Viewers
        self.__styler.register_viewer(self.__text_view)
        self.__styler.register_viewer(self.__right_sidebar)
        self.__styler.register_viewer(self.__right_sidebar.tagResults)
        self.__styler.register_viewer(self.__right_sidebar.currentTag)
        self.__styler.register_viewer(self.__right_sidebar.tagInfoField)
        self.__styler.register_viewer(self.__right_sidebar.preview)

        # Left sidebar
        self.__styler.register_viewer(self.__left_sidebar)
        self.__styler.register_viewer(self.__left_sidebar._legend)
        self.__styler.register_viewer(self.__left_sidebar.tree)


    #-------------------------------------------------------------------
    # Hover (in progress)

#    def on_enter(self, event):
#        self.textView.tag_add("cur", self.cur_line, self.cur_line + 1) 

    def on_leave(self, enter):
        self.textView.tag_add("reg", self.cur_line, self.cur_line + 1)

    #-------------------------------------------------------------------
    # The right click menu.

    def __make_tag_menu(self):
        """Define the menu that will show when
        right-clicked.
        """
        self.__menu_frame = tk.Frame(self.__root)
        self.__tag_menu = tk.Menu(self.__menu_frame, tearoff=0)
        self.__tag_menu.add_command(label="tag here", command=print("tag"))
        self.__tag_menu.add_command(label="Add Tag", command=self.__show_tag_screen)

    def __show_tag_menu(self, event):
        """Show the Menu pop up when right-clicked."""
        self.__tag_menu.post(event.x_root, event.y_root)
    
    def __show_tag_screen(self):
        """Display the New Tag Window."""
        word = self.__text_view.getString()
        self.__add_tag = EntryWindow(self.root, word, self.styles)


    #-------------------------------------------------------------------
    # Launch app

    def launch(self):
        """Launch the program."""

        # deiconify shows the window again. It is hidden at the beginning of
        # initialization, so that you don't get that weird grey box when it
        # starts to load.
        self.__splash.destroy()
        self.__root.deiconify()
        self.__root.mainloop()
        

#-----------------------------------------------------------------------
# Main section.

if __name__ == "__main__":
    app = Application()
    app.launch()

