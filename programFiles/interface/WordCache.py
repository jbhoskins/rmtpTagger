# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: A Cache for FramedText that saves the latest lookup, and important 
# information about it.

class Cache:
    """ Cache to save information about a word in FramedText """
    def __init__(self):
        self._string = ""
        self._start = "1.0"
        self._stop = "1.0"
        self._entries = []
        self._selectedEntry = None

    def update(self, word, start, stop, indexEntryList):
        self._string = word
        self._start = start
        self._stop = stop
        self._entries = indexEntryList

    def select(self, index):
        self._selectedEntry = index

    def selected(self):
        return self._selectedEntry

    def __eq__(self, other):
        if other._start == self._start:
            return True
        else:
            return False

    def string(self):
        return self._string

    def start(self):
        return self._start

    def stop(self):
        return self._stop

    def entries(self):
        return self._entries




