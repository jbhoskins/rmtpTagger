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


class KeywordTable(list):
    def __init__(self):
        list.__init__(self)
        self._current = int()


    def lookup(self, startIndex):        
        # This needs optinization. For now, it just iterates to keep 
        # functionality.

        i = 0
        while i < len(self) and not (self[i].start() <= startIndex <= self[i].stop()):
            i += 1

        if i == len(self):
            return None
        else:
            self._current = i
            return self[i]

    def saveEntries(self, entries):
        self[self._current]["entries"] = entries

    def currentVal(self):
        return self[self._current]

    def getVal(self):
        return self._current

    def setCurrent(self, value):
        self._current = value

    def printTable(self):
        for line in self:
            print(line)