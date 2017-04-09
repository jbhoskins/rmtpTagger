# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
#
# Description: Text object, inherits frame.

import tkinter as tk
from WordStruct import *

import re

import sys
sys.path.insert(0, '../')
from StemTree import *
from Index import *

class FramedText(tk.Text):
    def __init__(self, Frame):
        # tkinter things
        tk.Text.__init__(self, Frame)
        self.tag_configure('yellow', background = 'yellow')
        self.tag_configure('green', background = '#7CFC00')
        self.tag_configure('cyan', background = 'cyan')
        self.tag_configure("interviewer", background= "white")

        self.cachedWord = [0,0,0]
        self.ranges = []

    def _applyTag(self, word, results):
        """Word is a reMatch object, not a string."""
            
        if len(results) > 1:
            tag = "yellow"
        else:
            tag = "green"

        wordStart = "1.0+%sc" % word.start()
        wordEnd   = "1.0+%sc" % word.end()
        self.tag_add(tag, wordStart, wordEnd)
        self.ranges.append((wordStart, wordEnd))
        
 
    def loadText(self, path, index):
        """ Inserts text from a file into the widget, and highlights keywords."""
        f = open(path)
        string = f.read()
        self.insert(0.0, string, "bigger")

        for word in re.finditer("\w+", string):
            try:
                results = index.lookup(word.group().lower())
                # Ignore interviewer text
                if  int(self.index("1.0+%sc" % word.start()).split(".")[0]) % 4 - 1 == 0:
                    continue
            except:
                continue

            self._applyTag(word, results)
            
        for multiKey in index.multiKeys():
            print("MultiKey:", multiKey)
            for word in re.finditer(multiKey, string, re.IGNORECASE):
                print("found:", word.group())
                # Need to remove any preexisting tag here before applying the new one
                self._applyTag(word, index.lookup(word.group().lower()))

    def cacheWord(self, event):
        # Currently O(n) where n is the number of words found.
        location = self.index("@%s,%s" % (event.x, event.y))
        print("ranges:")
        print(self.tag_ranges("yellow"))
        for range_ in self.ranges:
            if self.compare(range_[0], "<=", location) and self.compare(range_[1], ">=", location):
                self.cachedWord = (self.get(range_[0], range_[1]), range_[0], range_[1])

    def getCache(self):
        return self.cachedWord



if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.pack()

    root.mainloop()
