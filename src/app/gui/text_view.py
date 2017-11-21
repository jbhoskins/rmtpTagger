# FramedText.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""An extension of tk.Text, this class handles finding and tagging of 
keywords and displays the text to the user in real time.
"""

import math
import re
import tkinter as tk

# For the error message
import tkinter.messagebox

import app.gui.view_controller as view


class TextView(tk.Text, view.Viewer, view.Stylable):
    """Class to display text, and highlight appropiate words in the text based
    on a table of values (keywordTable)."""
    def __init__(self, Frame, app, scrollbar):
        tk.Text.__init__(self, Frame, yscrollcommand=scrollbar.set)
        view.Viewer.__init__(self)
        view.Stylable.__init__(self)
        
        self.__app = app

        # default settings
        self.insert("1.0", "Load some text from the menubar!")
        self.config(state=tk.DISABLED, wrap=tk.WORD)

    def load_string(self, string):
        """Parse string for keywords, and then insert the string into the text_view."""

        # Run the parsing algorithm
        keyword_table = self.__app.get_keyword_table()
        keyword_table.fill_table(string)
        string = string.replace("ё", "е")

        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert("1.0", string, "bigger")

        self.__tag_speakers()
        self.tag_all_elements_in_table()
        self.config(state=tk.DISABLED)

    def load_text(self, path, makeTable = True):
        """Insert text from desired file into the widget, then highlight 
        keywords upon initialization. 
        """

        f = open(path, encoding="UTF-8")
        string = f.read().strip()
        string = string.replace("ё", "е") # All keys in the index have e instead of ё
        f.close()

        # Validate the input format
        pattern = re.compile(r"^((.+)\n\n)+(.+)$", re.MULTILINE)
        if pattern.fullmatch(string) is None:
            # the input get_string is not in the right format of text\n\ntext
            # etc...
            tk.messagebox.showwarning("Parse Error", "It looks like the text"+\
                    " you are trying to load is not formatted correctly."+\
                    "\n\nBefore importing please make sure that everything an"+\
                    " individual says is on its own line, and each line is"+\
                    " seperated by a single blank line.")
            return

        self.load_string(string)

    def style(self, styles):
        self.config(
            background=styles.c_1, font=styles.f_text)
        self.__create_tags(styles) # need to remake them with new colors
    
    def __create_tags(self, styles):
        """Create the tags that will be applied to a word in the text. Tags
        have associated background colors - each tag has a different color
        associated with it."""
        self.tag_configure("clickableWord")
        self.tag_configure("multi", background=styles.h_multi)
        self.tag_configure("single", background=styles.h_single) 
        self.tag_configure("cur", background=styles.h_current)
        
        self.tag_configure("unambiguous", background="white")

        self.tag_configure("interviewer", foreground=styles.h_interviewer)
        self.tag_configure("interviewee")
        
    def __tag_speakers(self):
        """Mute the interviewer text to make it less obtrusive."""
        length = math.floor(float(self.index(tk.END)))
        para_range = range(1, length, 4)
        
        for i in para_range:       
            inx = float(i)
            self.tag_add("interviewer", inx, inx + 1)     
            self.tag_add("interviewee", inx + 2, inx + 3)    
            
    def __apply_tag(self, instance, results):
        """Apply tags to words that have been found, so that they can be 
        referenced later. 
        """            
        if not instance.is_ambiguous():
            tag = "unambiguous"
        elif len(results) > 1:
            tag = "multi"
        else:
            tag = "single"
            
        # Tag the relevant region of text.
        word_start = "1.0+%sc" % instance.get_start()
        word_end = "1.0+%sc" % instance.get_stop()
        self.tag_add(tag, word_start, word_end)
        
        if instance.is_ambiguous():
            self.tag_add("clickableWord", word_start, word_end)

    def tag_all_elements_in_table(self):
        """ Tags every keyword present in the keyword_table with its appropiate
        color. Only called once when first loading text from file. """
        
        keyword_table = self.__app.get_keyword_table()
        
        for instance in keyword_table:
            results = instance.get_entries()
            self.__apply_tag(instance, results)

    #-------------------------------------------------------------------
    # User interaction and graphical functions.
    
    def on_click(self, event):
        """Move the currently selected instance to the instance that has been clicked on."""
        keyword_table = self.__app.get_keyword_table()
        
        location = self.index("@%s,%s" % (event.x, event.y))

        char_count = self.count("1.0", location)[0] # O(n)?
        keyword_table.lookup(char_count)

        keyword_table.notify_viewers_redraw()
        
    def update(self):
        """ Moves the current coloring to the current instance as per the
        keyword_table. """
        keyword_table = self.__app.get_keyword_table()
        current_entry = keyword_table.get_current_entry()

        self.tag_remove("cur", "1.0", tk.END)        
        self.tag_add(
            "cur", "1.0+%sc" % current_entry.get_start(),
            "1.0+%sc" % current_entry.get_stop())

        self.see("1.0+%sc" % current_entry.get_start())
