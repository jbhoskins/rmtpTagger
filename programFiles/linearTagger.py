# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: testing how iterators work...

import tkinter as tk
import re
import sys
sys.path.insert(0, "rmtp/programFiles")
from Index import *
sys.path.insert(0, "rmtp/programFiles/interface")
from WordCache import *

def test():
    string = "I am not a hat"

    iterator = re.finditer("\w+", string)
    try:
        while True:
            i = next(iterator)
            print(i.group())
            if i.group() == "not":
                next(iterator)
    except StopIteration:
        pass

    iterator = re.finditer("\w+", string)
    for i in iterator:
        print(i.group())
        if i.group() == "not":
            next(iterator)


ndx = Index("rmtp/META/index.xml")

f = open("rmtp/input/astaikina.txt")
iterator = re.finditer("\w+", f.read())

string = ""
cacheItem = Cache()
table = []
for word in iterator:
    testCode = ndx.multiTest(word.group().lower())
    
    if testCode == 0:
        if string != "":
            cacheItem["string"] = string
            print(cacheItem)
            table.append(cacheItem)
            # Reset the saved values
            string = ""
            cacheItem = Cache()

        continue
    elif testCode == 1:
        if string != "":
            string += " "
        else:
            cacheItem["start"] = word.start()
        string += word.group()
    else:
        if string != "":
            string += " "
        else:
            cacheItem["start"] = word.start() 
        
        string += word.group()
        cacheItem["stop"] = word.end()
        

for key in table:
    print("word:\t\t%s\t\t\tstart:\t%s\tstop:\t%s" % (key.string(), key.start(), key.stop()))
