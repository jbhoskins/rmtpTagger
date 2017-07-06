# TagWindow.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""Shows the current tags assigned to the selected word.


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide.
"""

"""Eventually, we will have it so that TagWindow pops up whenever you 
hover the mouse over a word that has been tagged. 


If we could, when opening the application, bind mouse-hover events to all 
tagged words in FramedText, then they could pop up with just the name of 
the word, and later the tagged form of the word that will be exported. 
"""


import tkinter as tk


class TagWindow:

    def __init__(self, parent, word, styles):

        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.styles = styles
        self.word = word
        
        # this would be the tag currently assigned to the word. Default 
        # is just the keyword bc I don't know how to grab the tag yet.        
        self.tag = word 
        self.root.geometry('100x50+0+0')
        self.label = tk.Label(self.root, text=self.tag, bg=self.styles.c_2)
        self.label.pack()

    def quit(self):
        # Allows main to quit the TagWindow when mouse not hovering over 
        # word.
        self.root.destroy()