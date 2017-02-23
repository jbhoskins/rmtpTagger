# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

from FramedText import *
import tkinter as tk

def getDim(root):
    return (root.winfo_screenwidth(), root.winfo_screenheight())


# make root, get the size of the screen.
root = tk.Tk()
dim = getDim(root)

# Make frames to fir the screen.
textFrame = tk.Frame(root, height = dim[1], width = dim[0] / 2, bg='red')
sidebarFrame = tk.Frame(root, height = dim[1], width = dim[0] / 4, bg='green')
textFrame.pack_propagate(0) # Stops frames from shrinking to fit contents.

txt = FramedText(textFrame)
txt.loadText("../../input/astaikina.txt")

# Pack the frames
textFrame.pack(side = tk.LEFT)
sidebarFrame.pack(side = tk.LEFT)

# Pack the FramedText object.
txt.pack()

root.mainloop()
