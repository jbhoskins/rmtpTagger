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

    def __len__(self):
        if self._tags == None:
            return len(self._clean)
        else:
            return len(self.tagged())

class FramedText:
    def __init__(self, Frame):
        # tkinter settings
        self.text = Text(Frame)
         
        # Other
        self.tokenized = []
        
        # Tag setup
        self.text.tag_configure('found', background = 'yellow')
           
    def loadText(self, path):
        """ Inserts text from a file into the widget."""
        f = open(path)
        for line in f:
            self.tokenized.append([WordStruct(word) for word in line.split()])
        f.close()

        string = ''
        for line in self.tokenized:
            for word in line:
                string += word.clean() + ' '

            string += '\n' 
        
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
    
    def highlight(self, lineNumber, wordNumber):
        
        # Delete the line
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')        

        # Rebuild and insert the line up the word to be highlighted.
        preString = ''
        for word in self.tokenized[lineNumber - 1][:wordNumber]:
            if word._tags == None:
                preString += word.clean() + ' '
            else:
                preString += word.tagged() + ' '
        self.text.insert(str(lineNumber) + '.0', preString)

        # Insert the word with the tag.
        word = self.tokenized[lineNumber - 1][wordNumber]
        self.text.insert(str(lineNumber) + '.end', word.clean(), "found")

        # Rebuid insert the rest of the line.
        postString = ' '
        for word in self.tokenized[lineNumber - 1][wordNumber + 1:]:
            if word._tags == None:
                postString += word.clean() + ' '
            else:
                postString += word.tagged() + ' '
        self.text.insert(str(lineNumber) + '.end', postString)

    def pack(self):
        """ Uses appropiate settings to fill its parent frame."""
        self.text.pack(expand = 1, fill = BOTH)

    def bind(self, button, function):
        self.text.bind(button, function)
        
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
    c = Button(root, text="Highlight", command = lambda: tt.highlight(1, 5))
    d = Button(root, text="Мы", command = lambda: tt.tag(1, 5, ('', '')))

    a.pack()
    b.pack()
    c.pack()
    d.pack()

    mainloop()
        
        
        
