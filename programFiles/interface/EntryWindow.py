import sys
sys.path.insert(0, '../')

from FramedText import *
from Sidebar import *
from EntryWindow import *
import tkinter as tk

class EntryWindow:
#-------------------------------------------------------------
# Sub-classes
#-------------------------------------------------------------

    class Title:
        def __init__(self, root, titleString, descripString):
            self.title = Label(root, text = titleString)
            self.descrip = Label(root, text = descripString)
            self.title.pack()
            self.descrip.pack()

        def config(self, font1 = "Verdana", font2 = "Verdana", bg = "white"):
            self.title.config(font = font1, bg = bg)
            self.descrip.config(font = font2, bg = bg)


    class LabeledEntry:
        def __init__(self, root, labelString, fillString):
            self.label = Label(root, text = labelString)
            self.entry = Entry(root)
            self.entry.insert(0, fillString)
            self.label.pack()
            self.entry.pack()

        def config(self, font = "Verdana", bg = "white"):
            self.label.config(font = font, bg = bg)
            self.entry.config(font = font)

        def get(self):
            return(self.entry.get())

#---------------------------------------------------------------------------
# Main window
#---------------------------------------------------------------------------

    def __init__(self, parent, key_word, bg, font1, font2):

        self.parent = parent
        self.root = Toplevel(self.parent)
        self.bg = bg
        self.font1 = font1
        self.font2 = font2

        self.key_word = key_word.string().lower()
        self.createWindow()
        self.styleWindow()


    def createWindow(self):
        self.root.geometry('400x450+0+0')

        self.title = "Add a new tag"
        self.root.wm_title(self.title)
        self.descrip = "If a keyword does not already have an \nassociated tag, create one here.\n"

        # Entries
        self.EntriesTitle = EntryWindow.Title(self.root, self.title, self.descrip)
        self.Entries1 = EntryWindow.LabeledEntry(self.root, "Word to Tag", self.key_word)
        self.Entries2 = EntryWindow.LabeledEntry(self.root, "XML type:", 'place, person, etc.')
        self.Entries3 = EntryWindow.LabeledEntry(self.root, "Declensions", 'Separate, by, commas')

        # Buttons
        self.b_ok = Button(self.root, text="Add tag to index", command = self.saveAnswers)
        self.b_ok.pack()
        self.b_nvm = Button(self.root, text="Never mind", command = self.quitWindow)
        self.b_nvm.pack()


    def saveAnswers(self):
        # This is where we would eventually save the keyword to the xml index
        self.getAnswers()
        new_string = self.key_word + ', ' + self.key_type + ', ' + self.key_decl
        print(new_string)
        self.root.destroy()


    def quitWindow(self):
        self.root.destroy()


    def getAnswers(self):
        self.key_word = self.Entries1.get()
        self.key_type = self.Entries2.get()
        self.key_decl = self.Entries3.get()


    def styleWindow(self):
        self.root.config(bg = self.bg)
        self.b_ok.config(font=self.font2, bg=self.bg, highlightbackground=self.bg, pady=25)
        self.b_nvm.config(font = self.font2, bg=self.bg, highlightbackground=self.bg)
        self.EntriesTitle.config(font1 = self.font1, font2 = self.font2, bg = self.bg)
        self.Entries1.config(font = self.font2, bg = self.bg)
        self.Entries2.config(font = self.font2, bg = self.bg)
        self.Entries3.config(font = self.font2, bg = self.bg)
