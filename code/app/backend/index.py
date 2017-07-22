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
mation given in the Index entry.

There are two exceptions - type (person, in this case), and xml:id are treated
specially, as they are important values (used in other contexts) that every
entry needs to have. they are given underscores to prevent being overwritten by
user defined attributes.

continuing with the example, this list would look like this (note that all
words are string types):

[ ("__type__", "person"),
  ("__xml:id__", "andreiTerkovskii"),
  ("role", "Director"),
  ("surname", "Tarkovskii"),
  ("forename", "Andrei"),
  ("gender", "m"),
  ("nationality","Russia") ]


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide.

"""


from bs4 import BeautifulSoup
from enum import Enum

class MatchState(Enum):
    """ Enumerated type to increase readibility of the match validator."""
    unique_match = 2
    potential_match = 1
    no_match = 0

class Entry:
    """Data Structure to store the information of each entry of index.xml."""
    
    def __init__(self, bs4_object):
        self._info = []

        # Underscores to avoid name conflicts, if it was just "type"
        # instead of "__type__" You would run into issues if the user
        # specified an attribute called "type", since you would have two
        # values with the same key.
        self._info.append(("__type__", str(bs4_object.name)))
        
        # If an xml:id is not specified, set it to an empty string.
        try:
            self._info.append(("__xml:id__", str(bs4_object["xml:id"])))
        except:
            self._info.append(("__xml:id__", ""))

        
        # Attach all information in the index.xml entry to the object.
        for info in bs4_object:
            if str(info.name) != 'keys' and info.name is not None:
                self._info.append((str(info.name), str(info.string)))
    
    def getValue(self, string):
        """ Returns the value of the associated with the key
        provided."""
        
        i = 0
        while i < len(self._info) and self._info[i][0] != string:
            i += 1

        if i == len(self._info):
            # not found
            return ""
        else:
            return self._info[i][1]

    def __str__(self):
        """Return a nicely formatted string of the _Entry with one 
        tuple per line, seperate by a colon.
        """
        string = ''
        for tup in self._info:
            string = string + tup[0] + ': ' + tup[1] + '\n'
        return string

class Index:
    """ Class that encapsulates all interaction with the index.xml file. It
    provides two primary functionalities:
        
        1: Permit the lookup of information in the xml file based on <key>
        attributes defined in the index.xml file itself.
        
        2: Builds a parse tree of the keys themselves, to provide a way to
        determine, one word at a time, if a string with an arbitrary number of
        words is a valid key. An important consequence of this is that longer keys
        will always take precedence over nested keys that are shorter.
        
        This should probably be refactored into a parse-tree class and a seperate
        index class, splitting up the functionalities."""

    def __init__(self, path):

        # Creates the soup object for easy parsing. This line has been 
        # problematic in the past (Might need codecs).
        f = open(path, encoding="UTF-8")
        self._soup = BeautifulSoup(f, 'html')
        f.close()

        self._multiWords = []
        self._index = self._buildIndex(self._soup)
        
        # These lines needed for multi-word validation
        self._multiValidator = dict()
        self._activeDict = self._multiValidator
        self._buildValidator(self._multiWords)

    def _buildIndex(self, soup, opts = []):
        """Create a dictionary with <keys> (declined forms) as its 
        dictionary keys and LISTS of _Entry objects as its dictionary
        values.
        """
        index = {}

        # Handles keys with multiple possible entries by creating a list of 
        # _Entry objects for a key.
        for key in soup.find_all('key'):
            try:
                index[key.string].append(Entry(key.parent.parent))
            except KeyError:
                index[key.string] = [Entry(key.parent.parent)]
            multi = key.string.strip().split()
            self._multiWords.append(multi)
        return index

    def _buildValidator(self, listOfMultiWordedKeys):
        """ Creates a tree of dictionaries that represents a parse-tree of
        every <key>.
        
        For example, given four keys:
        
        The
        The Quick
        The Slow
        Fox

        The Dictionary {None : None} is used to signify the termination of a
        string.

        the resulting dictoinary would have the keys {The, Fox}.
        
        - The value of ["The"] would be another dictionary with the keys
          {"Quick", "Slow", None}
        - The value of ["Fox"] would be another dictionary with the keys {None}
        """
        for sentence in listOfMultiWordedKeys:
            activeDict = self._multiValidator

            i = 0
            for i in range(len(sentence) - 1):
                if sentence[i] not in activeDict.keys():
                    activeDict[sentence[i]] = dict()
                activeDict = activeDict[sentence[i]]
            
            # Handles the case of an empty key like <key></key>
            if len(sentence) > 1:
                i += 1
             
            try:
                activeDict = activeDict[sentence[i]]
            except:
                activeDict[sentence[i]] = dict()
                activeDict = activeDict[sentence[i]]
                
            activeDict[None] = None
                
    def print_(self):
        """ Prints a semi-formatted representation of the multi-word validator.
        Used for debugging."""
        for key in self._multiValidator.keys():
            print(key)
            print('  ', self._multiValidator[key])
    
    def multiTest(self, word):
        """ Returns a value that tells you whether the string given is a valid
        next word in the parse tree. """
        if word in self._activeDict.keys(): # string is a valid next word
            # Prep the multiValidator to look at the next set of possible
            # strings.
            self._activeDict = self._activeDict[word]
            # The dictionary {None : None} signifies the termination of a key -
            # check if it is present, and if it is the only possible
            # continuation of the tree.
            if None in self._activeDict.keys():
                return MatchState.unique_match
            return MatchState.potential_match
        
        # It is important to note here, that the parse tree is only reset
        # automatically when it hits a "no_match". This is deliberate, and used
        # in the actual parse algorithm to make sure that all keys, including
        # consecutive keys, are considered.
        self.reset()
        return MatchState.no_match

    def reset(self):
        """ Resets the multi-word validator to the beginning of the parse tree."""
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
    ndx = Index('../../../META/index.xml')
    ndx.print_()

    print("test", ndx.multiTest("ирония"))
    print("test", ndx.multiTest("судьбы"))
    print("test", ndx.multiTest("или"))
    print("test", ndx.multiTest("с"))
    print("test", ndx.multiTest("легким"))
    print("test", ndx.multiTest("паром"))
    print("test", ndx.multiTest("кинотеатров"))
   
    print("Next:")
    print("test", ndx.multiTest("кинотеатр"))
    print("test", ndx.multiTest("аврора"))
    print("test", ndx.multiTest("пп"))
    print("test", ndx.multiTest("пп"))


    print("Next:")
    print("test", ndx.multiTest("кинотеатров"))
    print("test", ndx.multiTest("кинотеатры"))
    print("test", ndx.multiTest("кинотеатр"))
    print("test", ndx.multiTest("кинотеатров"))
