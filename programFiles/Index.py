"""
Reads and handles lookups from the Index.xml file, created by Sasha and Lena Prokhorov.

Since xml is structured in a machine readable format, I imported a module called 'beautiful
soup' which can be used to easily parse an xml document. Upon initialization, the Index 
object reads the index.xml file passed to it, (it is not hard coded, in case the name of
the file will be changed in the future. This also allows the path to it to be specified
later) and creates a python Dictionary object that is of the following structure:

Given a document with a number of index entries like the following:

<person xml:id="andreiTarkovskii">
    <role>Director</role>
    <surname>Tarkovskii</surname>
    <forename>Andrei</forname>
    <gender>m</gender>
    <nationality>Russia</nationality>
    <keys>
        <key>тарковский</key>
        <key>тарковского</key>
        <key>андрей</key>
        <key>андрея</key>
    </keys>

The Dictionary will have an entry for each 'key' specified (in this case, тарковский,
тарковского, андрей, and андрея, with an '_Entry' object as it's value. The Entry object
is just a list of tuples of all the information given in the Index entry. Continuing with
the example entry given above, this list would look like this: note that all words are
string types.

[ ('xml:id', 'andreiTarkovskii'),
  ('role', 'Director'),
  ('surname', Tarkovskii),
  ('forename', 'Andrei'),
  ('gender', 'm'),
  ('nationality','Russia') ]


So, after the creation of the Index object, you can easily find information on an
individual by entering any of the keys. 

This was done so that each key could be a declension, or generally any key that may want
to be tagged with specific information.

"""
# NEEDS TO BE UNIT-TESTED, I am not sure how it handles empty things / special cases...
# After a quick trivial test, seems like it handle it pretty well. If there are no keys, it
# simply does not add th the index Dictionary.

# The solutions as is now work very well, but we need to find a clever way to handle multi
# word keys. Maybe when building the dictionary, only use the first word of the string, and
# then return some kind of message to look at the next word?
from bs4 import BeautifulSoup

class Index:   
    class _Entry:
        """
        A Way to represent the information stored in the index.
        """
        
        def __init__(self, bs4_object):
            self._info = []
            self._info.append(('xml:id', bs4_object['xml:id']))
            
            for info in bs4_object:
                if info.name != 'keys' and info.name is not None:
                    self._info.append((info.name, info.string))

        def keys(self):
            return [tup[0] for tup in self._info]

        def values(self):
            return [tup[1] for tup in self._info]

        def __str__(self):
            string = ''
            for tup in self._info:
                string = string + tup[0] + ': ' + tup[1] + '\n'

            return string

    def __init__(self, path):
        """ Creates a Dictionary of keys and entries upon initialization. """ 

        # Creates the soup object for easy parsing.
        f = open(path)
        self._soup = BeautifulSoup(f, 'xml')
        f.close()

        self._multi_words = []

        self._index = self._build(self._soup)

    def _build(self, soup, opts = []):
        """ Creates a dictionary with keys (declined forms, etc) as it's keys, and 
        Entry objects as its values. """
        index = {}

        # Handles keys with multiple entries by creating a list of Entry objects for a key
        # if there are more than one tied to a specific key.
        for key in soup.find_all('key'):
            try:
                index[key.string].append(self._Entry(key.parent.parent))
            except KeyError:
                index[key.string] = [self._Entry(key.parent.parent)]

            
            multi = key.string.strip().split()
            if len(multi) > 1:
                self._multi_words.append(multi)

        return index

    
    def lookup(self, string):
        """ Returns the entry object that is tied to each key. """
        return self._index[string]
   
    def keys(self):
        return self._index.keys()

    def multiKeys(self):
        return self._multi_words
        



if __name__ == '__main__':
    ndx = Index('index.xml')
    print(ndx._index.keys())
    print(ndx.multiKeys())
    
#    print('keys', ndx.lookup('test')[0].keys(),
#    ndx.lookup('test')[0].values())
    print()
    print(ndx.lookup('test'))
    print()

#    print('keys', ndx.lookup('blahblah')[0].keys(),
#    ndx.lookup('blahblah')[0].values())
    print()
    print(ndx.lookup('blahblah'))
    print()
