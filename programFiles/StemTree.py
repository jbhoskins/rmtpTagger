class SentenceTree:
    """ 
    A tree-like structure built using only dictionaries, that can efficiently check
    whether a string with multiple words is a keyword.
    
    the quick brown fox
    the quick brown rabbit
    the quick red fox
    the slow fox
    the slow fox is running 
    """
    
    def __init__(self, sentences):
        self._dict = dict()
        self._active_dict = self._dict
        self._build(sentences)

    def _build(self, lst):
        """ Takes a list of lists, turns it into a list of lists, and then parses."""

        for sentence in lst:
            active_dict = self._dict
            
            i = 0
            for i in range(len(sentence) - 1):
                if sentence[i] not in active_dict.keys():
                    active_dict[sentence[i]] = dict()

                active_dict = active_dict[sentence[i]]

            i = i + 1
            # Serves as a marker for the end of a sentence.
            active_dict[sentence[i]] = {None : None}

    def print_(self):
        for key in self._dict.keys():
            print(key)
            print('  ', self._dict[key])

    def lookup(self, word):
        """
        2 = match found, end of sequence
        3 = match found, longer sequence possible.
        1 = possible match, continue...
        0 = No possible matches.
        """
        
        if word in self._active_dict.keys():
            self._active_dict = self._active_dict[word]
            
            # 
            if None in self._active_dict.keys() and len(self._active_dict.keys()) == 1:
                return 2
            elif None in self._active_dict.keys():
                return 3
            else:
                return 1
        else:
            return 0
                
    def reset(self):
        self._active_dict = self._dict


if __name__ == '__main__':
    a = 'the slow fox'
    b = 'the slow fox is running'
    c = 'the cat milk'
    d = 'green moose ear'
    e = 'red dog'

    A = [a.split(), b.split(), c.split(), d.split(), e.split()]

    tree = SentenceTree(A)
    tree.print_()
    print(tree.lookup('the'))
    print(tree.lookup('slow'))
    print(tree.lookup('fox'))
    print(tree.lookup('is'))
    print(tree.lookup('running'))
    print(tree.lookup('around'))
    tree.reset()
    print(tree.lookup('green'))




