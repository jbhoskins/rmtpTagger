# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

import tkinter as tk
from Text import *

def getDim(root):
    return (root.winfo_screenwidth(), root.winfo_screenheight())


# Text object for easy reading and writing.
txt = Text("../../input/astaikina.txt")

# make root, get the size of the screen.
root = tk.Tk()
dim = getDim(root)

# Make frames to fir the screen.
textFrame = tk.Frame(root, height = dim[1], width = dim[0] / 2, bg='red')
sidebarFrame = tk.Frame(root, height = dim[1], width = dim[0] / 4, bg='green')
textFrame.pack_propagate(0) # Stops frames from shrinking to fit contents.
text = tk.Text(textFrame) # Actual text widget

# Pack the frames
textFrame.pack(side = tk.LEFT)
sidebarFrame.pack(side = tk.LEFT)

# Put the text widget into the frame for text, options make sure it fills the whole frame.
text.pack(expand = 1, fill = tk.BOTH)

# Put the interviw text into the text widget.
text.insert(tk.INSERT, txt.string())

root.mainloop()
