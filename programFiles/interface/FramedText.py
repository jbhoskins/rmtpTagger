# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
#
# Description: Text object, inherits frame.

from tkinter import *

class WordStruct:
    def __init__(self, word):
        self._clean = word
        self._tags = None
        
    def clean(self):
        return self._clean
    
    def tagged(self):
        return self._tags[0] + self._clean + self._tags[1]
    
    def setTag(self, tagTup):
        self._tags = tagTup

class FramedText:
    def __init__(self, Frame):
        # tkinter settings
        self.text = Text(Frame)
         
        # Other
        self.tokenized = []
        
        # Tag setup
        self.text.tag_configure('found', font=('Arial', 20, 'bold'))
           
    def loadText(self, path):
        f = open(path)
        string = ""
        for line in f:
            string += line
            self.tokenized.append([WordStruct(word) for word in line.split()])
        f.close()
        
        self.text.insert(0.0, string)
    
    def tag(self, lineNumber, wordNumber, tagTuple):
        """ Redraws the line on which the word to be tagged is located. """
        
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')
        
        # pulls out the word from the list of tokens and assigns it tag values.
        token = self.tokenized[lineNumber - 1][wordNumber]
        token.setTag(tagTuple)  
        self.tokenized[lineNumber - 1][wordNumber] = token
        
        string = ""
        for word in self.tokenized[lineNumber - 1]:
            if word._tags == None:
                string += word.clean() + ' '
            else:
                string += word.tagged() + ' '
            
        self.text.insert(str(lineNumber) + '.0', string)
    
    def highlight(self, wordNumber):
        # do in three parts, beginning string with normal style, insert next with 
        # special, and then the rest as normal again.
        pass
        
        
    def pack(self):
        """ Uses appropiate settings to fill its parent frame."""
        self.text.pack(expand = 1, fill = BOTH)
        
if __name__ == "__main__":
    root = Tk()
    textFrame = Frame(root, height = 500, width = 500, bg = 'red')
    tt = FramedText(textFrame)

    textFrame.pack_propagate(0)
    textFrame.pack()

    tt.loadText('../../input/astaikina.txt')
    tt.pack()

    a = Button( root, text="<pronoun>Мы<Pronoun>", command = lambda: tt.tag(1, 5, ('<pronoun>', '</pronoun>')) )
    b = Button(root, text="<otherTag>Мы<otherTag>", command = lambda: tt.tag(1, 5, ('<otherTag>', '</otherTag>')))
    c = Button(root, text="<Theater>Мы<Theater>", command = lambda: tt.tag(1, 5, ('<Theater>', '</Theater>')))
    d = Button(root, text="Мы", command = lambda: tt.tag(1, 5, ('', '')))

    a.pack()
    b.pack()
    c.pack()
    d.pack()

    mainloop()
        
        
        
