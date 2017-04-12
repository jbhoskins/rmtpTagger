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
            
        def style(self, styles):
            self.styles = styles
            self.title.config(font = self.styles.f_title, bg = self.styles.c_2)
            self.descrip.config(font = self.styles.f_subtitle, bg = self.styles.c_2)


    class LabeledEntry:
        def __init__(self, root, labelString, fillString, styles):
            self.label = tk.Label(root, text = labelString)
            self.entry = tk.Entry(root)
            self.styles = styles
            
            self.entry.insert(0, fillString)
    
            self.label.pack()
            self.entry.pack()

        def style(self, styles):
            self.styles = styles
            self.label.config(font = self.styles.f_subtitle, bg = self.styles.c_2)
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
        self.key_word = key_word.lower()
            
        self._createWindow()
        self._styleWindow()


    def _createWindow(self):
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
        self.b_ok = tk.Button(self.root, text="Add tag to index", command = self._saveAnswers)
        self.b_ok.pack()
        self.b_nvm = tk.Button(self.root, text="Never mind", command = self._quitWindow)
        self.b_nvm.pack()


    def _saveAnswers(self):
        # This is where we would eventually save the keyword to the xml index
        self.getAnswers()
        new_string = self.key_word + ', ' + self.key_type + ', ' + self.key_decl
        self.root.destroy()


    def _quitWindow(self):
        self.root.destroy()


    def _getAnswers(self):
        self.key_word = self.Entries1.get()
        self.key_type = self.Entries2.get()
        self.key_decl = self.Entries3.get()


    #----------------------------------------------------------------------
    # Styling 
    
    def _styleWindow(self):
        self.root.config(bg = self.styles.c_2)
        
        self.EntriesTitle.style(self.styles)
        self.Entries1.style(self.styles)
        self.Entries2.style(self.styles)
        self.Entries3.style(self.styles)
        
        self.b_ok.config(font=self.styles.f_button, bg=self.styles.c_2, highlightbackground=self.styles.c_2, pady=25)
        self.b_nvm.config(font = self.styles.f_button, bg=self.styles.c_2, highlightbackground=self.styles.c_2)
        
    def configStyles(self, styles):
        self.styles = styles
        self._styleWindow()
        
    #----------------------------------------------------------------------


