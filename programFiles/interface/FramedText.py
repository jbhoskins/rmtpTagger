# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
#
# Description: Text object, inherits frame.

from tkinter import *
from WordStruct import *

import sys
sys.path.insert(0, '../')
from StemTree import *

"""New things 4/4/17:
    added self.cachedWord as a new variable. It stores a CachedWord object
        if the last word in the framedText that was clicked.
        
    implemented CachedWord -> inherits from WordStruct.
        all it is is a WordStruct with an extra field for saving the front and back
        indices of word. So now, instead of using the insertion cursor add xml tags
        (which was the root of the problem for most of the bugs) it uses the
        information stored in the cache.
        
    new functions:
        getCache()
            returns the CachedWord object stored in the cache.
        cacheWord()
            updates the Cache based on the location of the mouse cursor.

    significantly edited functions:
        draw()
            now draws each word in three parts. the beginning punctuation, the word
            itself, and the ending punctuation. This way we can highlight the word
            while leaving the punctuation unhighlighted.

            
    some other functions were edited to work correctly using this new convention - 
    the changes are pretty intuitive, though."""



class FramedText:
    def __init__(self, Frame):
        # tkinter things
        self.text = Text(Frame, wrap=WORD)
        self.text.tag_configure('yellow', background = 'yellow')
        self.text.tag_configure('green', background = '#7CFC00')
        self.text.tag_configure('cyan', background = 'cyan')

        self.cachedWord = CachedWord("")

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
                string += str(word) + ' '

            string += '\n' 
        
        # Insert the string into the widget.
        self.text.insert(0.0, string, "bigger")
    
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
        """ Replaces a line with """
        # If no end specified, then draw to the end of the line. tokenStart could be
        # specified in the constructor, but tokenEnd could not due to it calling len()
        if tokenEnd == None:
            tokenEnd = len(self.tokenized[lineNumber - 1])

        # Create a string from self.tokenized containing all words seperated by a space
        string = ''
        for word in self.tokenized[lineNumber - 1][tokenStart:tokenEnd]:
            if word._color is None:
                self.text.insert(str(lineNumber) + '.end', word.string() + ' ')
            else:
                self.text.insert(str(lineNumber) + '.end', word.frontPunctuation())
                self.text.insert(str(lineNumber) + '.end', word.noPunctuation(), word.color())
                self.text.insert(str(lineNumber) + '.end', word.backPunctuation())
                self.text.insert(str(lineNumber) + '.end', ' ')
                

        # Always inserts at the end of the line. To edit a line, you need to delete the
        # line first, outside of this function.
        self.text.insert(str(lineNumber) + '.end', string)

    def reDraw(self, lineNumber):
        """ Redraws an entire line. Used to clear highlighting from a line. Will not
        affect tags."""
        
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')
        self.draw(lineNumber)

    def highlight(self, lineNumber, wordNumber, color = "yellow"):
        """ Highlights a word in the text. Uses the same index conventions as a Text
        object: Line numbers start at 1, and word numbers start at 0."""
        
        # Delete the line from the word in question to the end.
        self.text.delete(str(lineNumber) + '.0', str(lineNumber) + '.end')        

        # draw up the word being highlighted
        self.draw(lineNumber, tokenEnd = wordNumber)

        # draw the highlighted word with a ' ' after it.
        word = self.tokenized[lineNumber - 1][wordNumber]
        self.text.insert(str(lineNumber) + '.end', word.noPunctuation(), color)
        self.text.insert(str(lineNumber) + '.end', ' ')

        # draw until the end of the line.
        self.draw(lineNumber, tokenStart = wordNumber + 1)

    def pack(self):
        """ Uses appropiate settings to fill its parent frame. It is important to run
        Frame.pack_propegate(0) on the parent of this widget for it to fill the frame."""
        self.text.pack(expand = True, fill = BOTH)

    def bind(self, button, command):
        self.text.bind(button, command)

    def insert(self, index, string):
        self.text.insert(index, string)
     
    def cacheWord(self): 
        current = self.text.index(CURRENT)

        count = 0
        expr = ''
        while self.text.get(current + expr) != ' ' and self.text.get(current + expr) != '\n' and count < 100: # If you click on the first word, (which you shouldnt be doing, just stops after 100)
            count += 1
            expr = '- ' + str(count) + ' c'
            print("." + self.text.get(current + expr) + ".")

        expr = '- ' + str(count - 1) + ' c'
        wordStart = current + expr

        string = self.text.get(wordStart, current + ' wordend')

        self.cachedWord = CachedWord(string)
        self.cachedWord.setInsertionIndices(wordStart, current + ' wordend')

    def getCache(self):
        return self.cachedWord

    def insertAround(self, key):

        print(self.cachedWord.front())
        print(self.cachedWord.back())
        
        self.text.insert(self.cachedWord.back(), "</%s>" % key)
        self.text.insert(self.cachedWord.front(), "<%s>" % key)
        

    def findAndFlag(self, index):
        print("going...")
        print(index.keys())
        for i in range(0, len(self.tokenized)):
            if ((i % 4) == 0):
                print("cont", i)
                continue
                
            for j in range(0, len(self.tokenized[i])):
                try:
                    cl = self.tokenized[i][j]
                    look = cl.noPunctuation().lower()
                    lst = index.lookup(look)
                except KeyError:
                    continue
                
                if len(lst) == 1:
                    self.tokenized[i][j].highlight("green")
                    print("FOUND!", i)
                else:
                    self.tokenized[i][j].highlight("yellow")

            self.reDraw(i + 1)
        print("Done")

    def consolidateMultiKeys(self, index):

        tree = SentenceTree(index.multiKeys())
        tree.print_()
 
        i = 0
        numberOfLines = len(self.tokenized)
        while i < numberOfLines:
            numberOfWords = len(self.tokenized[i])
            j = 0
            while j < numberOfWords:
                tree.reset()
                code = tree.lookup(str(self.tokenized[i][j].noPunctuation().lower()))
#                print(code, str(self.tokenized[i][j]))
                count = 0
                while code != 2 and code != 0:
                    count += 1
                    code = tree.lookup(str(self.tokenized[i][j + count].noPunctuation()).lower())
                    print("Tested:", str(self.tokenized[i][j + count].noPunctuation()).lower(), code)

                if code == 2:
                    print("Successful!")
                    while count > 0:
                        count -= 1
                        self.tokenized[i][j] = WordStruct(self.tokenized[i][j]._string + ' ' + self.tokenized[i][j+ 1]._string)
                        del self.tokenized[i][j + 1]
                        numberOfWords -= 1
                    
                    print(self.tokenized[i][j])
                    print(self.tokenized[i][j + count])
                    print([str(w) for w in self.tokenized[i]])

                j += 1
            i += 1



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
