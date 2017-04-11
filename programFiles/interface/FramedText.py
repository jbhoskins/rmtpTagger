# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
#
# Description: Text object, inherits frame.

import tkinter as tk
import re
from WordCache import *

import sys
sys.path.insert(0, '../')
from Index import *

class FramedText(tk.Text):
    """ Extends tk.Text, handles the finding and tagging of keywords. """
    def __init__(self, Frame, indexObject, styles):
        tk.Text.__init__(self, Frame)
        self.styles = styles
        self._createTags()
        
 
        self.wordCache = Cache()
        self.indexObject = indexObject # Needs "object" name so as not to overwrite 
                                       # Text method "Text.index()"

    def _createTags(self):
        """ Create the tags that will be applied to word in the text. """
        self.tag_configure("foundWord") # All words that are keys
        self.tag_configure('multi', background = self.styles.h_multi) # Keys with multiple options
        self.tag_configure('single', background = self.styles.h_single) # Kets with one option
        self.tag_configure('cur', background = self.styles.h_current) # Not yet in use, could be for current click
        self.tag_configure("interviewer") # Interviewer text (not yet in use)
        
    
    def _applyTag(self, word, results):
        """ Applies tags to words that have been found, so that they can be referenced 
            later. """            
        if len(results) > 1:
            tag = "multi"
        else:
            tag = "single"
            

        wordStart = "1.0+%sc" % word.start()
        wordEnd   = "1.0+%sc" % word.end()
        self.tag_add(tag, wordStart, wordEnd) # Tag the relevant region of text
        self.tag_add("foundWord", wordStart, wordEnd)
        
 
    def loadText(self, path):
        """ Inserts text from a file into the widget, and highlights keywords upon
            initialization. """
        f = open(path, encoding="UTF-8")
        string = f.read()
        self.insert(0.0, string, "bigger")

        for word in re.finditer("\w+", string):
            # Saves indices of word as you go; grabs words without punctuation
            try:
                results = self.indexObject.lookup(word.group().lower())
                # Ignore interviewer text
                if  int(self.index("1.0+%sc" % word.start()).split(".")[0]) % 4 - 1 == 0:
                    continue
            except:
                continue

            self._applyTag(word, results)
            
        # Using stem tree, you may be able to optimize here using next() and saving the 
        # Location of the most recent match...
        # Maybe implement both, and then time them?

        for multiKey in self.indexObject.multiKeys():
            print("MultiKey:", multiKey)
            for word in re.finditer(multiKey, string, re.IGNORECASE):
                print("found:", word.group())
                # Need to remove any preexisting tag here before applying the new one
                self._applyTag(word, self.indexObject.lookup(word.group().lower()))
        
 
    def cacheWord(self, event):
        """ Caches the word that has been clicked on. """        
        # Currently O(n) where n is the number of words found. Technically constant time.
        location = self.index("@%s,%s" % (event.x, event.y))
        ranges = self.tag_ranges("foundWord")
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            stop = ranges[i + 1]
            if self.compare(location, ">=", start) and self.compare(location, "<=", stop):
                word = self.get(start, stop).lower()
                # This next line should never throw an error... Theoretically
                self.wordCache.update(word, start, stop, self.indexObject.lookup(word))
                

    def getCache(self):
        """ Returns the cache. """
        print(self.wordCache.string())
        return self.wordCache


    def insertAroundCache(self, index):
        """ Based on the index of the selection in the tagResults listbox, applies the
            appropiate tags around the word. """
        if self.wordCache.entries() == []:
            return
            
        entry = self.wordCache.entries()[index]
        
        print(entry)
        
        start = self.wordCache.start()
        stop  = self.wordCache.stop()
        
        self.insert(stop, "</rs>")
        self.insert(start, "<rstype=\"%s\" key=\"%s\">" % (entry.type(), entry.xmlId()))
            
            
    def getString(self):
        current = self.index(tk.CURRENT)
        
        count = 1
        expr = ''
        
        while self.get(current + expr) != ' ' and self.get(current + expr) != '\n' and count <100: 
            count += 1
            expr = '- ' + str(count - 1) + ' c'
            
        wordStart = current + expr
        string = self.get(wordStart, current + ' wordend')
            
        return string
          
          
if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.pack()

    root.mainloop()
