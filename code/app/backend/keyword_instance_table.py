# KeywordTable.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

""" A table of KeywordInstances, with the inclusion of a index, to keep track
of which instance is currently being examined/edited. 

This the main data structure of the program during runtime.

This program utilizes the Observer design pattern, and this class is the
"Subject" of this pattern - whenever it changes, it's viewers need to be
updated to reflect the new changes.


EDITED:
Margaret, 4/22/17
Changed style of code to conform to the PEP8 styleguide.
"""

import app.gui.view_controller as view
from app.backend.keyword_instance import KeywordInstance
import os
from bs4 import BeautifulSoup
from app.backend.index import Index
from app.backend.parse_tree import MatchState
from app.backend.parse_tree import ParseTree

import re

# Use these instead of the imports above re to run this program as main
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
        # Shouldnt open the file twice but hey
        self._indexObject = Index(os.path.join("res", "index.xml"))
        self._parseTree = ParseTree(os.path.join("res", "index.xml"))
        

    def lookup(self, startIndex):        
        """Returns the KeywordInstance that corrosponds to the given CHARECTOR index."""
        
        # This could be a binary search. For now, it's linear to keep 
        # functionality.

        i = 0
        while i < len(self) and not (self[i].start() <= startIndex <= self[i].stop()):
            i += 1

        # If index does not corrospond to any entry, or is marked as
        # uninteractable
        if i == len(self) or self[i]["unambiguous"]:
            return None
        
        self._current = i
        return self[i]

    def jumpTo(self, tableIndex):
        
        # assert to prevent jumps to pronouns, etc.
        assert self[tableIndex]["unambiguous"] == False
        self._current = tableIndex % len(self)
        self.notifyViewersRedraw()

    def makeIndex(self):
        """Instantiates an Index object. Needed for session loading."""
        self._indexObject = Index("../META/index.xml")

    def getCurrentEntry(self):
        """Returns the currently selected KeywordInstance."""
        if len(self) == 0:
            return KeywordInstance()


    def getCurrentIndex(self):
        """Returns the value of the index of the entry currently being
        examined/edited."""
        return self._current

    def reset(self):
        """Dereferences the table, and resets the current cursor to 0."""
        self[:] = []
        self._current = 0

    def nextValidEntry(self, event=None):
        """ Returns the next valid entry that is ambiguous and set the cursor
        to that index."""
        
        i = 1
        while i < len(self) and self[(self._current + i) % len(self)]["unambiguous"]:
            i = i + 1

        self._current = (self._current + i) % len(self)

        self.notifyViewersRedraw()

    def previousValidEntry(self, event=None):
        """ Returns the previous valid entry that is ambiguous and set the cursor
        to that index."""
        
        i = 1
        while i < len(self) and self[(self._current - i) % len(self)]["unambiguous"]:
            i = i + 1

        self._current = (self._current - i) % len(self)

        self.notifyViewersRedraw()

    def nextTag(self, event=None):
        """ Move to the next tag in the list of tag suggestions (entry list) """

        # Don't allow changes to confirmed entries
        if self.getCurrentEntry()["confirmed"]:
            return
        
        # Some weird mod arithmetic here, but it is needed to move seamlessly
        # through the range, (-1, len(possibleTags) - 1)
        self.getCurrentEntry()["selectedEntry"] += 2
        self.getCurrentEntry()["selectedEntry"] %=\
        (len(self.getCurrentEntry().entries()) + 1)
        self.getCurrentEntry()["selectedEntry"] -= 1

        self.notifyViewersRedraw()


    def prevTag(self, event=None):
        """ Move to the previous tag in the list of tag suggestions (entry list) """
        
        # Don't allow changes to confirmed entries
        if self.getCurrentEntry()["confirmed"]:
            return
        
        # Some weird mod arithmetic here, but it is needed to move seamlessly
        # through the range, (-1, len(possibleTags) - 1)
        self.getCurrentEntry()["selectedEntry"] %=\
        (len(self.getCurrentEntry().entries()) + 1)
        self.getCurrentEntry()["selectedEntry"] -= 1 

        self.notifyViewersRedraw()

    def toggleConfirmCurrent(self, event=None):
        self.getCurrentEntry().toggleConfirm()
        self.notifyViewersRedraw()

    def fillTable(self, string):
        """Build a sorted table of all KeywordInstances in the given string."""
        
        self.reset()

        # Ideally, make a generator for each relevant line
        iterator = re.finditer("\w+(-\w+)?", string) 
        keyword = ""
        cacheItem = KeywordInstance()
        foundMatch = False
        word = next(iterator)
        
        try:
            while True: # Yes, it's an infinite loop. It's the solution the
                        # docs suggested.
                
                # Kind of inefficient, but seems to be fast enough
                # inx = int(tk.Text.index("1.0+%sc" % word.start()).split(".")[0])
                inx = string.count("\n", 0, word.start()) + 1
                
                # Only run the next bit if it's an interviewee. use "if true"
                # to not skip anything.
                # if True:
                if  (inx % 4 - 1) != 0:
                    testCode = self._indexObject.validate(word.group().lower())

                    if testCode == MatchState.no_match:
         
                        # This is the point when an entry is actually 
                        # saved. When it finds a match, it waits until 
                        # it hits a zero to save it, in case there are a
                        # couple keys like so: "фон", "фон триер". We  
                        # want the second, longer tag, not the shorter.
                        if foundMatch:
                            cacheItem["string"] = keyword
                            cacheItem["entries"] = self._indexObject.lookup(keyword.lower())
                            # set to unambiguous. checks len is 1 to avoid
                            # multiple definitions of word bugs by accident.
                            if len(cacheItem["entries"]) == 1 and\
                            cacheItem["entries"][0].getValue("unambiguous")\
                            == "true":
                                cacheItem["unambiguous"] = True
                            
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
                    
                    elif testCode == MatchState.potential_match:
                        # If there is a word, add a space before the
                        # next one.                       
                        if keyword != "":
                            keyword += " "
                        else:
                            cacheItem["start"] = word.start()
                        keyword += word.group()
                        
                    elif testCode == MatchState.unique_match:
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

        self.nextValidEntry() # start at the first value

    # ------- Methods to implement subject / observer design pattern --------
    
    def notifyViewersRedraw(self):
        """ Notify all the viewers to redraw themselves based on the current 
        state of the table. """
        
        for view in self._views:
            view.update()
    
    def registerViewer(self, newView):
        """ Add a viewer that will update whenever notifyViewersRedraw is
        called. """
        self._views.append(newView)

    def deleteViewer(self, viewToDelete):
        """ Remove a viewer that will update whenever notifyViewersRedraw is
        called. """
        self._views.remove(viewToDelete)



if __name__ == "__main__":
    kt = KeywordInstanceTable()

    f = open("../../../input/lebedeva.txt", encoding="UTF-8")
    string = f.read()
    string = string.replace("ё", "е")
    f.close()

    kt.fillTable(string)
