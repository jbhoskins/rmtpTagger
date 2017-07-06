# KeywordTable.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""
Reads and handles lookups from the Index.xml file, created by Sasha and 
Lena Prokhorov.

Since xml is structured in a machine readable format, I imported a 
module called 'beautiful soup' which can be used to easily parse an 
xml document. Upon initialization, the Index object reads the index.xml 
file passed to it, and creates a Python Dictionary object that is of the 
following structure:

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

The Dictionary will have an entry for each 'key' specified (in this case, 
тарковский, тарковского, андрей, and андрея) with an '_Entry' object as 
its value. The _Entry object is just a list of tuples of all the infor-
mation given in the Index entry, with two exceptions. Continuing with 
the example entry given above, this list would look like this (note that 
all words are string types):

[ ("type", "person"),
  ("xmlId", "andreiTerkovskii"),
  ("role", "Director"),
  ("surname", "Tarkovskii"),
  ("forename", "Andrei"),
  ("gender", "m"),
  ("nationality","Russia") ]

From this list of tuples, only the first two entries can be returned 
through a method:

type() returns "person"
xmlId() returns "andreiTerkovskii"

These are treated specially because their values are needed to generate 
the xml tags. So, after the creation of the Index object, you can easily 
find information on an individual by entering any of the keys. This was 
done so that each key could be a declension, or generally any key that 
may want to be tagged with specific information.


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide.

"""


from bs4 import BeautifulSoup


class Index:
    
    class _Entry:
        """Data Structure to store the information of each index entry."""
        
        def __init__(self, bs4_object):
            self._info = []
            self._info.append(("type", bs4_object.name))
            self._info.append(("xmlId", bs4_object["xml:id"]))
            
            for info in bs4_object:
                if info.name != 'keys' and info.name is not None:
                    self._info.append((info.name, info.string))

        def type(self):
            """ Return the TYPE of the _Entry, e.g. person."""
            return self._info[0][1]

        def xmlId(self):
            """Return the VALUE of the _Entry's xmlId, e.g. 
            andreiTarkovskii.
            """
            return self._info[1][1]

        def __str__(self):
            """Return the STRING REPRESENTATION of the _Entry with one 
            tuple per line, seperate by a colon.
            """
            string = ''
            for tup in self._info:
                string = string + tup[0] + ': ' + tup[1] + '\n'
            return string

    def __init__(self, path):
        """Create a Dictionary of keys and entries upon initialization.""" 

        # Creates the soup object for easy parsing. This line has been 
        # problematic in the past (Might need codecs).
        f = open(path, encoding="UTF-8")
        self._soup = BeautifulSoup(f, 'html')
        f.close()

        self._multiWords = []
        self._index = self._buildIndex(self._soup)
        
        # Needed for multiWord validation
        self._multiValidator = dict()
        self._activeDict = self._multiValidator
        self._buildValidator(self._multiWords)

    def _buildIndex(self, soup, opts = []):
        """Create a dictionary with <keys> (declined forms) as its 
        dictionary keys and lists of _Entry objects as its dictionary
        values.
        """
        index = {}

        # Handles keys with multiple entries by creating a list of 
        # _Entry objects for a key if there are more than one tied to a 
        # specific key.
        for key in soup.find_all('key'):
            try:
                index[key.string].append(self._Entry(key.parent.parent))
            except KeyError:
                index[key.string] = [self._Entry(key.parent.parent)]
            multi = key.string.strip().split()
            self._multiWords.append(multi)
        return index

    def _buildValidator(self, wordList):
        for sentence in wordList:
            activeDict = self._multiValidator

            i = 0
            for i in range(len(sentence) - 1):
                if sentence[i] not in activeDict.keys():
                    activeDict[sentence[i]] = dict()
                activeDict = activeDict[sentence[i]]
            
            if len(sentence) > 1:
                i += 1
             
            try:
                activeDict = activeDict[sentence[i]]
            except:
                activeDict[sentence[i]] = dict()
                activeDict = activeDict[sentence[i]]
                
            activeDict[None] = None
                
    def print_(self):
        for key in self._multiValidator.keys():
            print(key)
            print('  ', self._multiValidator[key])
    
    def multiTest(self, word):
        if word in self._activeDict.keys():
            self._activeDict = self._activeDict[word]
            if None in self._activeDict.keys():
                return 2 
            return 1
        
        self.reset()
        return 0

    def reset(self):
        self._activeDict = self._multiValidator
    
    def lookup(self, string):
        """Return a LIST of entry objects that is tied to each key."""
        return self._index[string]
   
    def keys(self):
        """Return all the keys of the index."""
        return self._index.keys()

    def multiKeys(self):
        """Return a LIST of all keys that have more than one word."""
        return self._multiWords
        



if __name__ == '__main__':
    ndx = Index('../../META/index.xml')
    ndx.print_()

    print("test", ndx.multiTest("ирония"))
    print("test", ndx.multiTest("судьбы"))
    print("test", ndx.multiTest("или"))
    print("test", ndx.multiTest("с"))
    print("test", ndx.multiTest("легким"))
    print("test", ndx.multiTest("паром"))
   
    print("Next:")
    print("test", ndx.multiTest("кинотеатр"))
    print("test", ndx.multiTest("кинотеатр"))
    print("test", ndx.multiTest("аврора"))
    print("test", ndx.multiTest("пп"))
    print("test", ndx.multiTest("пп"))


    print("Next:")
    print("test", ndx.multiTest("кинотеатров"))
    print("test", ndx.multiTest("кинотеатры"))
    print("test", ndx.multiTest("кинотеатр"))
