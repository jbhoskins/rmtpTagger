# KeywordTable.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""A table to hold keywords and their current tags in the text.
LAST EDIT:
Margaret, 4/22/17
Changed style of code to conform to the PEP8 styleguide.
"""

import app.gui.view_controller as view
from app.backend.keyword_instance import KeywordInstance
from app.backend.index import Index

import re

# Use these to run this program as main
#import sys
#sys.path.insert(0, "../backend")
#from index import Index
#from keyword_instance import KeywordInstance

class KeywordInstanceTable(list):
    def __init__(self):
        list.__init__(self)
        self._current = 0
        
        # Registered viewers for observer design pattern
        self._views = []

        # This is the only data structure that needs the index
        self._indexObject = Index("../META/index.xml")
        

    def lookup(self, startIndex):        
        """Returns the entry that corrosponds to the given charector index."""
        
        # This needs optinization. For now, it just iterates to keep 
        # functionality.

        i = 0
        while i < len(self) and not (self[i].start() <= startIndex <= self[i].stop()):
            i += 1

        # index does not corrospond to an entry.
        if i == len(self):
            return None
        
        self._current = i
        return self[i]

    def saveEntries(self, entries):
        """Saves a list of entries to the currently selected entry in the
        table."""
        self[self._current]["entries"] = entries

    def getCurrentEntry(self):
        """Returns the currently selected entry."""
        return self[self._current]

    def getCurrentIndex(self):
        """Returns the index of the current value."""
        return self._current

    def reset(self):
        """Dereferences the table, and resets the current cursor to 0."""
        self[:] = []
        self._current = 0

    def nextValidEntry(self, setOfInvalidWords = {}):
        """ Returns the next valid entry that is not a member of the invalid
        set, and set the cursor to that index."""
        
        # Not yet implemented yet. Dummy method to maintain functinoality
        self._current = (self._current + 1) % len(self)

    def previousValidEntry(self, setOfInvalidWords = {}):
        """ Returns the next valid entry that is not a member of the invalid
        set, and set the cursor to that index."""
        
        # Not yet implemented yet. Dummy method to maintain functinoality
        self._current = (self._current - 1) % len(self)

    def nextTag(self):
        
        # Some weird mod arithmetic here, but it is needed to move seamlessly
        # through the range, (-1, len(possibleTags) - 1)
        self.getCurrentEntry()["selectedEntry"] += 2
        self.getCurrentEntry()["selectedEntry"] %=\
        (len(self.getCurrentEntry().entries()) + 1)
        self.getCurrentEntry()["selectedEntry"] -= 1


    def prevTag(self):
        
        # Some weird mod arithmetic here, but it is needed to move seamlessly
        # through the range, (-1, len(possibleTags) - 1)
        self.getCurrentEntry()["selectedEntry"] %=\
        (len(self.getCurrentEntry().entries()) + 1)
        self.getCurrentEntry()["selectedEntry"] -= 1 

    def fillTable(self, string):
        """Build a sorted table of all non-pronoun tags along with their 
        start and stop indices. 
        """
        
        self.reset()
        print("length of table", len(self))

        # Ideally, make a generator for each relevant line
        iterator = re.finditer("\w+", string) 
        keyword = ""
        cacheItem = KeywordInstance()
        foundMatch = False
        word = next(iterator)
        
        try:
            while True: # Gods of CS, forgive this infinite loop.
                
                # Kind of inefficient, but seems to be fast enough
                # inx = int(tk.Text.index("1.0+%sc" % word.start()).split(".")[0])
                inx = string.count("\n", 0, word.start()) + 1
                
                # Only run the next bit if it's an interviewee. use "if true"
                # to not skip anything.
                # if True:
                if  (inx % 4 - 1) != 0:
                    testCode = self._indexObject.multiTest(word.group().lower())

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
                            cacheItem["entries"] = self._indexObject.lookup(keyword.lower())
                            self.append(cacheItem)  
                            
                            # Reset the saved values.
                            keyword = ""
                            cacheItem = KeywordInstance()
                            foundMatch = False
                            
                            # Continue rechecks the same word with a re-
                            # set multiTest, in case two keywords are 
                            # next to each other.
                            continue

                        keyword = ""
                        cacheItem = KeywordInstance()
                    
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

    # ------- Methods to implement subject / observer design pattern --------
    
    def notifyViewersRedraw(self):
        for view in self._views:
            print("updating view:", view)
            view.update()
    
    def registerViewer(self, newView):
        self._views.append(newView)

    def deleteViewer(self, viewToDelete):
        self._views.remove(viewToDelete)



if __name__ == "__main__":
    kt = KeywordInstanceTable()

    f = open("../../../input/lebedeva.txt", encoding="UTF-8")
    string = f.read()
    string = string.replace("ё", "е")
    f.close()

    kt.fillTable(string)
