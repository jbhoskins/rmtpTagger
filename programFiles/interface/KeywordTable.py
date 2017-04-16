# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: A table.

class KeywordTable(list):
    def __init__(self):
        list.__init__(self)
        self._current = int()


    def lookup(self, startIndex):        
        # This needs optinization. For now, it just iterates to keep functionality.

        i = 0
        while i < len(self) and (self[i].start() <= startIndex <= self[i].stop()) is False:
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

    def printTable(self):
        for line in self:
            print(line)

