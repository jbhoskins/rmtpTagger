# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: 


class WordStruct: 
    def __init__(self, word):
        self._ndxs = self._getIndices(word)
        self._string = word
        self._noPunctuation = word[self._ndxs[0] : self._ndxs[1] + 1]
        self._tags = None
        self._color = None
        
    def noPunctuation(self):
        return self._noPunctuation

    def frontPunctuation(self):
        return self._string[:self._ndxs[0]]

    def backPunctuation(self):
        return self._string[self._ndxs[1] + 1:]

    def string(self):
        return self._string

    def color(self):
        return self._color

    def highlight(self, color):
        self._color = color
    
    def tagged(self):
        return self._tags[0] + self._clean + self._tags[1]
    
    def setTag(self, tagTup):
        self._tags = tagTup
    
    def _getIndices(self, string):
        """ Gets the front and back indices of the punctuation in a phrase."""
        
        ndx_f = 0
        ndx_b = 0

        # This try block catches the case when a word is all punctuation, such as an emdash '-'
        # in this case, it changes nothing, and just returns itself.
        i = 0
        try:
            # Iterate from the fron to first alpha car
            while not string[i].isalnum(): #isalpha() returns True when a char is a-z/0-9
                i += 1
            ndx_f = i
    
            # Iterate from the back to the last alpha charector
            i = len(string) - 1
            while not string[i].isalnum():
                i -= 1
            ndx_b = i
        except IndexError:
            return (0, len(string) + 1)
    
        return ndx_f, ndx_b

    def __str__(self):
        return str(self._string)

class CachedWord(WordStruct):
    def __init__(self, string):
        WordStruct.__init__(self, string)
        self._front = None
        self._back = None

    def setInsertionIndices(self, front, back):
        self._front = front
        self._back = back

    def front(self):
        return self._front

    def back(self):
        return self._back


if __name__ == "__main__":
    do = Word("....")
    print(do.frontPunctuation())
    print(do.backPunctuation())
