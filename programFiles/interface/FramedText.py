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

    def __str__(self):
        return str(self._clean)

class FramedText:
    def __init__(self, Frame):
        # tkinter things
        self.text = Text(Frame)
        self.text.tag_configure('highlighted', background = 'yellow')
         
        # List of lists of individual words.
        self.tokenized = []
        
    def loadText(self, path):
        """ Inserts text from a file into the widget."""
        f = open(path)
        for line in f:
            line = line.split()
            self.tokenized.append([WordStruct(word) for word in line])
        f.close()

        string = ''
        for line in self.tokenized:
            for word in line:
                string += word.clean() + ' '

            string += '\n' 
        
        # Insert the string into the widget.
        self.text.insert(0.0, string)
    
    def tag(self, lineNumber, wordNumber, tagTuple):
        """ Tags a word on a line with the tags in the tuple "tagTuple". """
        
        # Delete the entire line.
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')
        
        # set the tags in the WordStruct of the word.
        token = self.tokenized[lineNumber - 1][wordNumber].setTag(tagTuple)
        
        # Draw the entire line again. Needs to affect the entire line, since it is not
        # possible to delete from a word on, only insert from a word on. draw()
        # automatically draws words with tags that are not NONE.
        self.draw(lineNumber)
    
    def draw(self, lineNumber, tokenStart = 0, tokenEnd = None):
        # If no end specified, then draw to the end of the line. tokenStart could be
        # specified in the constructor, but tokenEnd could not due to it calling len()
        if tokenEnd == None:
            tokenEnd = len(self.tokenized[lineNumber - 1])

        # Create a string from self.tokenized containing all words seperated by a space
        string = ''
        for word in self.tokenized[lineNumber - 1][tokenStart:tokenEnd]:
            if word._tags == None:
                string += word.clean() + ' '
            else:
                string += word.tagged() + ' '

        # Always inserts at the end of the line. To edit a line, you need to delete the
        # line first, outside of this function.
        self.text.insert(str(lineNumber) + '.end', string)

    def reDraw(self, lineNumber):
        """ Redraws an entire line. Used to clear highlighting from a line. Will not
        affect tags."""
        
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')
        self.draw(lineNumber)

    def highlight(self, lineNumber, wordNumber):
        """ Highlights a word in the text. Uses the same index conventions as a Text
        object: Line numbers start at 1, and word numbers start at 0."""
        
        # Delete the line
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')        

        # draw up the word being highlighted
        self.draw(lineNumber, tokenEnd = wordNumber)

        # draw the highlighted word with a ' ' after it.
        word = self.tokenized[lineNumber - 1][wordNumber]
        self.text.insert(str(lineNumber) + '.end', word.clean(), "highlighted")
        self.text.insert(str(lineNumber) + '.end', ' ')

        # draw until the end of the line.
        self.draw(lineNumber, tokenStart = wordNumber + 1)

    def pack(self):
        """ Uses appropiate settings to fill its parent frame. It is important to run
        Frame.pack_propegate(0) on the parent of this widget for it to fill the frame."""
        self.text.pack(expand = 1, fill = BOTH)

    def bind(self, button, function):
        self.text.bind(button, function)

    def insert(self, index, string):
        self.text.insert(index, string)
     
    def iterTest(self):
        """ For demonstration purposes, iterates through the FramedText object and
        highlights each word after an enter press."""
        for i in range(0, len(self.tokenized)):
            for j in range(0, len(self.tokenized[i])):
                self.highlight(i + 1, j)
                input()
                self.reDraw(i + 1)


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
    e = Button(root, text="Iter", command = lambda: tt.iterTest())

    a.pack()
    b.pack()
    c.pack()
    d.pack()
    e.pack()

    mainloop()    
