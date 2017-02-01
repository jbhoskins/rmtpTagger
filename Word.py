class Word:
    def __init__(self, word):
        self.__word = word
        self.__clean = ''  # These get initialized only if the 
        self.__ndx_f = 0   # cleanse function is called.
        self.__ndx_b = 0
        
    def cleanse(self):
        # can probably be done more elegantly

        self.__clean = ''
        self.__ndx_f = 0
        self.__ndx_b = 0
        
        i = 0
        try:
            while not self.__word[i].isalnum():
                i += 1
            self.__ndx_f = i
    
            i = len(self.__word) - 1
            while not self.__word[i].isalnum():
                i -= 1
            self.__ndx_b = i
        except IndexError:
            self.__clean = self.__word
            return self.__clean
        
        # Except block Covers the case of a word object of only punctuation.
        self.__clean =  (self.__word[self.__ndx_f : self.__ndx_b + 1])
        self.__clean = self.__clean
        return self.__clean

    def replace(self, replacement):
        # be careful with this one. if word is not cleansed, returns ''

        if self.__ndx_f != self.__ndx_b:
            return self.__word[:self.__ndx_f] + replacement + self.__word[self.__ndx_b + 1:]
        else:
            return self.__word

    def clean(self):
        return self.__clean

    def front_ndx(self):
        return self.__ndx_f

    def back_ndx(self):
        return self.__ndx_b

    def __str__(self):
        return self.__word

    def __add__(self, other):
        return str(self) + other


if __name__ == '__main__':
    word = Word('.sdlkfjlskdf.')
    print(word)
    print(word.cleanse())
    print(word.clean())
    print(word.replace(word.clean()), end = '')
    print('hi')
    print(word.front_ndx())
    print(word.back_ndx())
    print(word)
