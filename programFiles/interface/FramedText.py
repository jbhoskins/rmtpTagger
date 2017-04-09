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

"""New things 4/4/17:
    added self.cachedWord as a new variable. It stores a CachedWord object
        if the last word in the framedText that was clicked.
        
    implemented CachedWord -> inherits from WordStruct.
        all it is is a WordStruct with an extra field for saving the front and back
        indices of word. So now, instead of using the insertion cursor add xml tags
        (which was the root of the problem for most of the bugs) it uses the
        information stored in the cache.
        
    new functions:
        getCache()
            returns the CachedWord object stored in the cache.
        cacheWord()
            updates the Cache based on the location of the mouse cursor.

    significantly edited functions:
        draw()
            now draws each word in three parts. the beginning punctuation, the word
            itself, and the ending punctuation. This way we can highlight the word
            while leaving the punctuation unhighlighted.

            
    some other functions were edited to work correctly using this new convention - 
    the changes are pretty intuitive, though."""



class FramedText(tk.Text):
    def __init__(self, Frame):
        # tkinter things
        tk.Text.__init__(self, Frame)
        self.tag_configure('yellow', background = 'yellow')
        self.tag_configure('green', background = '#7CFC00')
        self.tag_configure('cyan', background = 'cyan')
        self.tag_configure("interviewer", background= "white")

        self.cachedWord = CachedWord("")
        self.ranges = []
 
    def loadText(self, path, index):
        """ Inserts text from a file into the widget, and highlights keywords."""
        f = open(path)
        string = f.read()
        self.insert(0.0, string, "bigger")

        for word in re.finditer("\w+", string):
            print(word.group())
            try:
                results = index.lookup(word.group().lower())
                # Ignore interviewer text
                if  int(self.index("1.0+%sc" % word.start()).split(".")[0]) % 4 - 1 == 0:
                    continue
            except:
                continue
            
            if len(results) > 1:
                tag = "yellow"
            else:
                tag = "green"

            wordStart = "1.0+%sc" % word.start()
            wordEnd   = "1.0+%sc" % word.end()
            self.tag_add(tag, wordStart, wordEnd)
            self.ranges.append((wordStart, wordEnd))

    def getWord(self, event):
        # Currently O(n) where n is the number of words found.
        location = self.index("@%s,%s" % (event.x, event.y))
        for range_ in self.ranges:
            if self.compare(range_[0], "<=", location) and self.compare(range_[1], ">=", location):
                print(self.get(range_[0], range_[1]))
        


if __name__ == "__main__":
    root = tk.Tk()

    txt = FramedText(root)
    txt.loadText("../../input/astaikina.txt", Index("../../META/index.xml"))
    txt.bind("<Button-1>", txt.getWord)
    txt.pack()

    root.mainloop()
