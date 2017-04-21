# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
#
# Description: Text object, inherits frame.

import tkinter as tk
import re
from WordCache import *
from KeywordTable import *
import math

import sys
sys.path.insert(0, '../')
from Index import *

class FramedText(tk.Text):
    """ Extends tk.Text, handles the finding and tagging of keywords. """
    def __init__(self, Frame, indexObject, styles):
        scrollbar = tk.Scrollbar(Frame)
        tk.Text.__init__(self, Frame, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.insert("1.0", "Load some text from the menubar!")
        self.config(state = tk.DISABLED, wrap=tk.WORD)

        self.styles = styles
        self._styleWidget()
        self._createTags()
                
        self.keywordTable = KeywordTable()
        self.indexObject = indexObject # Needs "object" name so as not to overwrite 
                                       # Text method "Text.index()"
        
    def _createTags(self):
        """ Create the tags that will be applied to word in the text. """
        self.tag_configure("foundWord") # All words that are keys
        self.tag_configure('multi', background = self.styles.h_multi) # Keys with multiple options
        self.tag_configure('single', background = self.styles.h_single) # Kets with one option
        self.tag_configure('cur', background = self.styles.h_current) # Not yet in use, could be for current click
        self.tag_configure('reg', background = self.styles.c_1)
        self.tag_configure("interviewer", foreground = self.styles.h_interviewer) # Interviewer text (not yet in use)
        self.tag_configure("interviewee")
        
    
    def _applyTag(self, word, results):
        """ Applies tags to words that have been found, so that they can be referenced 
            later. """            
        if len(results) > 1:
            tag = "multi"
        else:
            tag = "single"
            
        wordStart = "1.0+%sc" % word.start()
        wordEnd   = "1.0+%sc" % word.stop()
        self.tag_add(tag, wordStart, wordEnd) # Tag the relevant region of text
        self.tag_add("foundWord", wordStart, wordEnd)

    def tagAllElementsInTable(self):
        for word in self.keywordTable:
            results = self.indexObject.lookup(word.string().lower())
            self._applyTag(word, results)

        cur = self.index("1.0+%sc" % 20163)
        print("value:", self.keywordTable.lookup(self.count("1.0", cur)[0]))
        print(self.keywordTable)

    def _makeTable(self):
        """ Build a sorted table with all the tags and their start and stop points. """
        
        self.keywordTable[:] = []
        
        string = self.get("1.0", tk.END)
        iterator = re.finditer("\w+", string) # Ideally, make a generator for each relevant
                                             # line.
        keyword = ""
        cacheItem = Cache()
        foundMatch = False
        
        word = next(iterator)
        try:
            # Gods of CS, forgive this infinite loop.
            while True:
                if  int(self.index("1.0+%sc" % word.start()).split(".")[0]) % 4 - 1 != 0:
                    # If interviewee, continue. Can be optimized, should only get strings 
                    # from the interviewee text.
                                
                    # 2 = match found, 1 = potential match, 0 = no match
                    testCode = self.indexObject.multiTest(word.group().lower())
    
                    # Using the testCode, save object imformation accordingly
                    if testCode == 0:
                        # This is the point when an entry is actually saved. when it finds
                        # a match, it waits until it hits a zero to save it, in case you
                        # have a couple keys like so: "фон" "фон триер". You want the 
                        # second, longer tag, not the shorter one.
                        if foundMatch:
                            cacheItem["string"] = keyword
                            self.keywordTable.append(cacheItem)        
                            # Reset the saved values
                            keyword = ""
                            cacheItem = Cache()
                            foundMatch = False
                            # Continue does not move to the next word. rechecks the same
                            # word with a resetted multiTest. needed for 
                            # the case of two keywords next to each other.
                            continue

                        # Needed for if you hit a 1, but never a two.
                        keyword = ""
                        cacheItem = Cache()
                    
                    elif testCode == 1:
                        if keyword != "":
                            # if there is a word, then add a space before the next one
                            keyword += " "
                        else:
                            cacheItem["start"] = word.start()
                        
                        keyword += word.group()
                    else:
                        # when testCode == 2
                        if keyword != "":
                            keyword += " "
                        else:
                            cacheItem["start"] = word.start()
        
                        keyword += word.group()
                        cacheItem["stop"] = word.end()
                        foundMatch = True

                word = next(iterator)
        # Weird, but this was the best solution I could find for moving through an 
        # iterator with more control than a for loop.
        except StopIteration:
            # May need to save the last information, in case the final word is a keyword
            pass
        self.tagAllElementsInTable()
            
    def loadText(self, path, makeTable = True):
        """ Inserts text from a file into the widget, and highlights keywords upon
            initialization. """
        f = open(path, encoding="UTF-8")
        string = f.read()
        string = string.replace("ё", "е")
        f.close()
        self.config(state = tk.NORMAL)
        self.delete("1.0", tk.END)
        self.insert("1.0", string, "bigger")

        # Not sure the utility of making this optional tbh
        if makeTable is True:
            self._makeTable()
        
        self._grayInterviewer()
        self.config(state = tk.DISABLED)
                        
 
    def cacheWord(self, event):
        """ Caches the word that has been clicked on. """        
        location = self.index("@%s,%s" % (event.x, event.y))        
        current = self.keywordTable.currentVal()
        self.tag_remove("cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())   

        charCount = self.count("1.0", location)[0] # is this linear time?
        current = self.keywordTable.lookup(charCount)
        if self.keywordTable.currentVal().entries() == []:
            self.keywordTable.saveEntries(self.indexObject.lookup(current.string().lower()))
        self.tag_add("cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())

    def move(self, offset):
        """ Set the currently selected word to be the one offset by an integer value."""
        try:
            current = self.keywordTable.currentVal()
        except:
            # Catches first run issue
            return
        
        self.tag_remove("cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())   
        self.keywordTable.setCurrent((self.keywordTable.getVal() + offset) % len(self.keywordTable))
        current = self.keywordTable.currentVal()

        if self.keywordTable.currentVal().entries() == []:
            self.keywordTable.saveEntries(self.indexObject.lookup(current.string().lower()))
        self.tag_add("cur", "1.0+%sc" % current.start(), "1.0+%sc" % current.stop())
        

    def getCache(self):
        """ Returns the cache. """
        return self.keywordTable.currentVal()


    def getString(self):
        current = self.index(tk.CURRENT)
        
        count = 1
        expr = ''
        
        while self.get(current + expr) != ' ' and self.get(current + expr) != '\n' and\
        count <100:
            count += 1
            expr = '- ' + str(count - 1) + ' c'
            
        wordStart = current + expr + '+1c'
        string = self.get(wordStart, current + ' wordend')
            
        return string

    #-------------------------------------------------------------------
    # Styling
    
    def _styleWidget(self):
        self.config(bg = self.styles.c_1, highlightbackground = self.styles.c_1, font = self.styles.f_text)
        
    def _grayInterviewer(self):
        self.text_length = math.floor(float(self.index(tk.END)))
        para_range = range(1, self.text_length, 4)
        
        for i in para_range:       
            inx = float(i)
            self.tag_add("interviewer", inx, inx+1)     
            self.tag_add("interviewee", inx + 2, inx+3)

    
    def configStyles(self, styles):
        self.styles = styles
        self._createTags()
        self._styleWidget()


        
    #-------------------------------------------------------------------
  
         
          
if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.pack()

    root.mainloop()
