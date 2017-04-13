"""Eventually, we will have it so that TagWindow pops up whenever you hover the mouse over a word that has been tagged. 


If we could, when opening the application, bind mouse-hover events to all tagged words in FramedText, then they could pop up with just the name of the word, and later the tagged form of the word that will be exported. 

"""

import tkinter as tk

class TagWindow:

    def __init__(self, parent, word, styles):

        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.styles = styles
        self.word = word
        self.tag = word # this would be the tag currently assigned to the word. Default is just the keyword bc I don't know how to grab the tag yet.
            
        self.root.geometry('100x50+0+0')
        self.label = tk.Label(self.root, text = self.tag, bg = self.styles.c_2)
        self.label.pack()

    def quit(self):
        # Allows main to quit the TagWindow when mouse not hovering over word.
        self.root.destroy()