# Keywords.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Co-authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""String Utilities that are useful in the manipulation of our invertiew 
data.  Is not technically optimal, some stuff could be cached, but for 
now, I like this solution better. It seems more straightforwards than 
initializing a word object, handling cleanses, etc. Here things are 
called only when they are needed, and never otherwise.

LAST EDIT:

Margaret, 4/22/17

Changed style of code to be more like the PEP8 styleguide.  Rearranged 
things so that like functions would be in same block of code.  Rewrote 
some comments and code to make it more readable.
"""


class Keyword:
 
    def __init__(self, string):
        self._string = string
        self._ndx_f, self._ndx_b = self._get_indices(string)
        self._clean = self._string[self._ndx_f : self._ndx_b + 1]
        self._declensions = []
    
    def _get_indices(self, string):
        """Gets the front and back indices of the punctuation in a
        phrase.
        """
        ndx_f = 0
        ndx_b = 0
        i = 0

        # This try block catches the case when a word is all punctuation, 
        # such as an emdash '-'.  In this case, it changes nothing, and 
        # just returns itself.
        try:
            # Iterate from the front to first alpha character. isalpha() 
            # returns True when a char is a-z/0-9.
            while not string[i].isalnum():
                i += 1
            ndx_f = i
    
            # Iterate from the back to the last alpha character.
            i = len(string) - 1
            while not string[i].isalnum():
                i -= 1
            ndx_b = i
        except IndexError:
            return (0, len(string) + 1)
        return ndx_f, ndx_b
    
    def clean(self):
        """Moove backwards and forwards through a string with punctuation 
        until an alphanumeric charector is hit; return the inner word.
        """
        return self._clean

    def replace(self, replacement):
        """Given a string, place that string within the punctuation of 
        another word.
    
        test = Word(',,Hats...')
        test.replace('Shoes') # This will return: ,,Shoes...
        """
        return self._string[:self._ndx_f] + replacement + self._string[self._ndx_b + 1:]

    def set_declensions(self, lst):
        """ Store the declined forms of the word as the list passed."""
        self._declensions = lst

    def get_entries(self, soup):
        """Return a list of all the relevant... will be replaced by a 
        lookup function.
        """
        entries = []
        for entry in soup.find_all('person'):
            entries.append(entry)
        return entries

    
    # place, key, word to be tagged as both place and key
    # title, key, word to be tagged as both title and key
    # person, key, name to be tagged as both a person and key
    # nationalCinema, key, place to be tagged as related to national cinema
    # genre, key (type of genre), word to be tagged as the genre that it is.
    
    # (non)lexical hesitations
    
    # pronouns
    #   Я   -  pron, persSing
    #   мы  -  pron, persPlur
    #   мой -  pron, possSing
    #   наш -  pron, possPlur
 
    
def tag_user(string, name, sp):
    """Tag string (a line, in this case) with the proper tag."""
    return '<u xml:id="sp%i" who="%s">' % (sp, name) + string + '</u>'

def tag_type(string, typ):
    """Tag string (a line, in this case) with the proper tag."""
    return '<rs type="%s" subtype="%s">' % (typ[0], typ[1]) + string + '</rs>'
    
    
if __name__ == '__main__':
    word = Keyword(')))привет, мир.')
    print(word._string)
    print(word.clean())
    print(word.replace('bob'))
