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
    def __init__(self, Frame, indexObject):
        # tkinter things
        tk.Text.__init__(self, Frame)
        self._createTags()
 
        self.wordCache = Cache()
        self.indexObject = indexObject # Needs "object" name so as not to overwrite 
                                       # Text methods

    def _createTags(self):
        self.tag_configure("foundWord")
        self.tag_configure('yellow', background = 'yellow')
        self.tag_configure('green', background = '#7CFC00')
        self.tag_configure('cyan', background = 'cyan')
        self.tag_configure("interviewer", background= "white")
        
    
    def _applyTag(self, word, results):
        """Word is a reMatch object, not a string."""
            
        if len(results) > 1:
            tag = "yellow"
        else:
            tag = "green"

        wordStart = "1.0+%sc" % word.start()
        wordEnd   = "1.0+%sc" % word.end()
        self.tag_add(tag, wordStart, wordEnd)
        self.tag_add("foundWord", wordStart, wordEnd)
        
 
    def loadText(self, path):
        """ Inserts text from a file into the widget, and highlights keywords."""
        f = open(path)
        string = f.read()
        self.insert(0.0, string, "bigger")

        for word in re.finditer("\w+", string):
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
        # Currently O(n) where n is the number of words found. Technically constant time
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
        print(self.wordCache.string())
        return self.wordCache

    def insertAroundCache(self, index):
        if self.wordCache.entries() == []:
            return
            
        entry = self.wordCache.entries()[index]
        
        print(entry)
        
        start = self.wordCache.start()
        stop  = self.wordCache.stop()
        
        self.insert(stop, "</rs>")
        self.insert(start, "<rstype=\"%s\" key=\"%s\">" % (entry.name(), entry.xmlId()))

            
if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.pack()

    root.mainloop()
