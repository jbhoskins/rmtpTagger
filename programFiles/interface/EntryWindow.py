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
        def __init__(self, root, titleString, descripString, styles):
            self.title = tk.Label(root, text = titleString)
            self.descrip = tk.Label(root, text = descripString)
            self.styles = styles
            
            self.title.pack()
            self.descrip.pack()
            
            self.title.config(font = self.styles.f_title, bg = self.styles.c_1)
            self.descrip.config(font = self.styles.f_subtitle, bg = self.styles.c_1)


    class LabeledEntry:
        def __init__(self, root, labelString, fillString, styles):
            self.label = tk.Label(root, text = labelString)
            self.entry = tk.Entry(root)
            self.styles = styles
            
            self.entry.insert(0, fillString)
    
            self.label.pack()
            self.entry.pack()

            self.label.config(font = self.styles.f_subtitle, bg = self.styles.c_1)
            self.entry.config(font = self.styles.f_text)

        def get(self):
            return(self.entry.get())

#---------------------------------------------------------------------------
# Main window
#---------------------------------------------------------------------------

    def __init__(self, parent, key_word, styles):

        self.parent = parent
        self.root = tk.Toplevel(self.parent)
        self.styles = styles

        self.key_word = key_word.string().lower()
        self.createWindow()
        self.styleWindow()


    def createWindow(self):
        self.root.geometry('400x450+0+0')

        self.title = "Add a new tag"
        self.root.wm_title(self.title)
        self.descrip = "If a keyword does not already have an \nassociated tag, create one here.\n"

        # Entries
        self.EntriesTitle = EntryWindow.Title(self.root, self.title, self.descrip, self.styles)
        self.Entries1 = EntryWindow.LabeledEntry(self.root, "Word to Tag", self.key_word, self.styles)
        self.Entries2 = EntryWindow.LabeledEntry(self.root, "XML type:", 'place, person, etc.', self.styles)
        self.Entries3 = EntryWindow.LabeledEntry(self.root, "Declensions", 'Separate, by, commas', self.styles)

        # Buttons
        self.b_ok = tk.Button(self.root, text="Add tag to index", command = self.saveAnswers)
        self.b_ok.pack()
        self.b_nvm = tk.Button(self.root, text="Never mind", command = self.quitWindow)
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
        self.root.config(bg = self.styles.c_1)
        self.b_ok.config(font=self.styles.f_button, bg=self.styles.c_1, highlightbackground=self.styles.c_1, pady=25)
        self.b_nvm.config(font = self.styles.f_button, bg=self.styles.c_1, highlightbackground=self.styles.c_1)


