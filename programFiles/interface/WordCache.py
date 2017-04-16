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
        self["start"] = None
        self["stop"] = None
        self["entries"] = []
        self["selectedEntry"] = None

    def selectionIndex(self):
        print("returning", self["selectedEntry"])
        return self["selectedEntry"]

    def selection(self):
        return self["entries"][self["selectedEntry"]]

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
    cce = [Cache()]

    cce[0]["string"] = "Hey"
    print(cce[0]["string"])
    print("before", cce[0]["selectedEntry"])
    cce[0].select(5)
    print("after", cce[0]["selectedEntry"])
