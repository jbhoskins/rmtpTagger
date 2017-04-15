# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: A Cache for FramedText that saves the latest lookup, and important 
# information about it.

import tkinter as tk

class Cache(dict):
    """ Cache to save information about a word in FramedText """
    def __init__(self):
        dict.__init__(self)
        
        self["string"] = ""
        self["start"] = "1.0"
        self["stop"] = "1.0"
        self["entries"] = []
        self["selectedEntry"] = None

    def select(self, index):
        self._selectedEntry = index

    def selected(self):
        return self._selectedEntry

    def __eq__(self, other):
        return other["start"] == self["start"]

    def string(self):
        return self["string"]

    def start(self):
        return self["start"]

    def stop(self):
        return self["stop"]

    def entries(self):
        return self["entries"]

if __name__ == "__main__":
    cce = Cache()

    cce["string"] = "Hey"
    print(cce["string"])
