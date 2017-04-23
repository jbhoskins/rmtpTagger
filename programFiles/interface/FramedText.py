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

from Index import *
from KeywordTable import *
from WordCache import *


class FramedText(tk.Text):
    def __init__(self, Frame, indexObject, styles, scrollbar):
        """Initialize the text, keyword table, index, styles, variable 
        tags, and widgets.
        """
        tk.Text.__init__(self, Frame, yscrollcommand=scrollbar.set)
        
        # The following needs "object" name so as not to overwrite the 
        # Text method Text.index()
        self.indexObject = indexObject         
        self.keywordTable = KeywordTable()
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
        
        self.config(state=tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert("1.0", string, "bigger")
    
        # Not sure the utility of making this optional 
        if makeTable is True:
            self._makeTable()
        
        self._tagPersons()
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


    #-------------------------------------------------------------------
    # Making and tagging from table.

    def _makeTable(self):
        """Build a sorted table of all non-pronoun tags along with their 
        start and stop indices. 
        """
        self.keywordTable[:] = []
        string = self.get("1.0", tk.END)
        
        # Ideally, make a generator for each relevant line
        iterator = re.finditer("\w+", string) 
        keyword = ""
        cacheItem = Cache()
        foundMatch = False
        word = next(iterator)
        
        try:
            while True: # Gods of CS, forgive this infinite loop.
                inx = int(self.index("1.0+%sc" % word.start()).split(".")[0])
                
                # Only run the next bit if it's an interviewee.
                if  (inx % 4 - 1) != 0:
                    testCode = self.indexObject.multiTest(word.group().lower())
    
                    # For this next block of if, elif, else:
                    # Using the testCode, save object information:
                    # 2 = unique match found, 
                    # 1 = potential match,
                    # 0 = no match.                     
                    if testCode == 0:
                        
                        # This is the point when an entry is actually 
                        # saved. When it finds a match, it waits until 
                        # it hits a zero to save it, in case there are a
                        # couple keys like so: "фон", "фон триер". We  
                        # want the second, longer tag, not the shorter.
                        if foundMatch:
                            cacheItem["string"] = keyword
                            self.keywordTable.append(cacheItem)  
                            
                            # Reset the saved values.
                            keyword = ""
                            cacheItem = Cache()
                            foundMatch = False
                            
                            # Continue rechecks the same word with a re-
                            # set multiTest, in case two keywords are 
                            # next to each other.
                            continue

                        keyword = ""
                        cacheItem = Cache()
                    
                    elif testCode == 1:
                        # If there is a word, add a space before the
                        # next one.                       
                        if keyword != "":
                            keyword += " "
                        else:
                            cacheItem["start"] = word.start()
                        keyword += word.group()
                        
                    else:
                        if keyword != "":
                            keyword += " "
                        else:
                            cacheItem["start"] = word.start()
        
                        keyword += word.group()
                        cacheItem["stop"] = word.end()
                        foundMatch = True
                        
                word = next(iterator)

        except StopIteration:
            # May need to save the last information, in case the final 
            # word is a keyword
            pass
        self.tagAllElementsInTable()                     
        
    def tagAllElementsInTable(self):
        """Function description here."""
        for word in self.keywordTable:
            results = self.indexObject.lookup(word.string().lower())
            self._applyTag(word, results)

        cur = self.index("1.0+%sc" % 20163) # hardcoding?
        print("value:", self.keywordTable.lookup(self.count("1.0", cur)[0]))
        print(self.keywordTable)
        
        
    #-------------------------------------------------------------------
    # Extra functions.
    
    def cacheWord(self, event):
        """Cache the word that has been clicked on."""        
        location = self.index("@%s,%s" % (event.x, event.y))        
        current = self.keywordTable.currentVal()
        self.tag_remove(
            "cur", "1.0+%sc" % current.start(),"1.0+%sc" % current.stop())   

        charCount = self.count("1.0", location)[0] # O(n)?
        current = self.keywordTable.lookup(charCount)
        if self.keywordTable.currentVal().entries() == []:
            word = current.string().lower()
            self.keywordTable.saveEntries(self.indexObject.lookup(word))
        self.tag_add(
            "cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())

    def move(self, offset):
        """Set the currently selected word to be the one offset by an 
        integer value.
        """
        try:
            current = self.keywordTable.currentVal()
        except:
            # Catches first run issue
            return
        
        self.tag_remove(
            "cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())   
        self.keywordTable.setCurrent(
            (self.keywordTable.getVal() + offset) % len(self.keywordTable))
        current = self.keywordTable.currentVal()

        if self.keywordTable.currentVal().entries() == []:
            word = current.string().lower()
            self.keywordTable.saveEntries(self.indexObject.lookup(word))
        self.tag_add(
            "cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())

    def getCache(self):
        """Return the cache."""
        return self.keywordTable.currentVal()

    def getString(self):
        """Return a string of the current selection."""
        current = self.index(tk.CURRENT)
        cur_word = self.get(current + expr)
        omits = ['\n', '']
        count = 1
        expr = ''
        while cur_word not in omits and count < 100:
            count += 1
            expr = '- ' + str(count - 1) + ' c'
            cur_word = self.get(current + expr)
            
        wordStart = current + expr + '+1c'
        string = self.get(wordStart, current + ' wordend')
            
        return string
        
    
#-----------------------------------------------------------------------
# Main.

if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.pack()

    root.mainloop()