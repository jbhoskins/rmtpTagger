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

LAST EDIT:

Margaret, 4/22/17

Changed style of code to be more like the PEP8 styleguide.  Rearranged 
things so that like functions would be in same block of code.  Rewrote 
some comments and code to make it more readable.
"""

## We need to distinguish between our tags and
## Python's tags, like self.tag_configure, to help
## improve readability.


import sys
sys.path.insert(0, '../')

import math
import re
import tkinter as tk

from app.backend.keyword_instance_table import KeywordInstanceTable
from app.backend.keyword_instance import KeywordInstance
import app.gui.view_controller as view


class TextView(tk.Text, view.Viewer):
    def __init__(self, Frame, keywordInstanceTable, styles, scrollbar):
        """Initialize the text, keyword table, index, styles, variable 
        tags, and widgets.
        """
        tk.Text.__init__(self, Frame, yscrollcommand=scrollbar.set)
        
        # The following needs "object" name so as not to overwrite the 
        # Text method Text.index()
        self._keywordTable = keywordInstanceTable
        self.styles = styles
        
        self._styleFrame()
        self._styleWidget()
        self._createTags()        
    
        
    #-------------------------------------------------------------------
    # Styling.    
    
    def loadText(self, path, makeTable = True):
        """Insert text from desired file into the widget, then highlight 
        keywords upon initialization. 
        """
        f = open(path, encoding="UTF-8")
        string = f.read()
        string = string.replace("ё", "е")
        f.close()

        self._keywordTable.fillTable(string)
        
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert("1.0", string, "bigger")
            
        self._tagPersons()
        self.tagAllElementsInTable()
        self.config(state=tk.DISABLED) 
    
    def _styleFrame(self):
        """Style the whole frame."""
        self.insert(
            "1.0", "Load some text from the menubar!")
        self.config(state=tk.DISABLED, wrap=tk.WORD)        
        
    def _styleWidget(self):
        """Style the widget."""
        self.config(
            bg=self.styles.c_1, font=self.styles.f_text,
            highlightbackground=self.styles.c_1)
        
    def configStyles(self, styles):
        """Change the desired stylesheet."""
        self.styles = styles
        self._styleWidget()
        self._createTags()    
    
        
    #-------------------------------------------------------------------       
    # Configuring and applying tags.
    
    def _createTags(self):
        """Create the tags that will be applied to a word in the text."""
        self.tag_configure("foundWord")
        self.tag_configure('multi', background=self.styles.h_multi)
        self.tag_configure('single', background=self.styles.h_single) 
        self.tag_configure('cur', background=self.styles.h_current)
        self.tag_configure('reg', background=self.styles.c_1)
        self.tag_configure("interviewer", foreground=self.styles.h_interviewer)
        self.tag_configure("interviewee")
        
    def _tagPersons(self):
        """Mute the interviewer text to make it less obtrusive."""
        length = math.floor(float(self.index(tk.END)))
        para_range = range(1, length, 4)
        
        for i in para_range:       
            inx = float(i)
            self.tag_add("interviewer", inx, inx + 1)     
            self.tag_add("interviewee", inx + 2, inx + 3)    
            
    def _applyTag(self, word, results):
        """Apply tags to words that have been found, so that they can be 
        referenced later. 
        """            
        if len(results) > 1:
            tag = "multi"
        else:
            tag = "single"
            
        wordStart = "1.0+%sc" % word.start()
        wordEnd   = "1.0+%sc" % word.stop()
        
        # Tag the relevant region of text.
        self.tag_add(tag, wordStart, wordEnd)
        self.tag_add("foundWord", wordStart, wordEnd)


    def tagAllElementsInTable(self):
        """ Tags every keyword present in the keywordTable with its appropiate
        color. Only called once when first loading text from file. """
        for word in self._keywordTable:
            results = word.entries()
            self._applyTag(word, results)

        #cur = self.index("1.0+%sc" % 20163) # hardcoding?
        #print("value:", self.keywordTable.lookup(self.count("1.0", cur)[0]))
        #print(self.keywordTable)
        
        
    #-------------------------------------------------------------------
    # User interaction and graphical functions.
    
    def onClick(self, event):
        """Cache the word that has been clicked on."""        
        location = self.index("@%s,%s" % (event.x, event.y))

        charCount = self.count("1.0", location)[0] # O(n)?
        self._keywordTable.lookup(charCount)
        print("REDRAWING")
        self._keywordTable.notifyViewersRedraw()
        
    def update(self):
        """ Moves the current coloring to the correct entry as per the
        keywordTable. """
        currentEntry = self._keywordTable.getCurrentEntry()

        self.tag_remove("cur", "1.0", tk.END)        
        self.tag_add(
            "cur", "1.0+%sc" % currentEntry.start(), 
            "1.0+%sc" % currentEntry.stop())

        self.see("1.0+%sc" % currentEntry.start())
 
#-----------------------------------------------------------------------
# Main.

if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.pack()

    root.mainloop()