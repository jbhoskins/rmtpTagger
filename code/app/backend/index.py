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
from app.backend.index_entry import Entry

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

    def __init__(self, soup):
        self._index = self._buildIndex(self._soup)

    def _buildIndex(self, soup, opts = []):
        """Create a dictionary with <keys> (declined forms) as its 
        dictionary keys and LISTS of _Entry objects as its dictionary
        values.
        """
        index = dict()

        # Handles keys with multiple possible entries by creating a list of 
        # _Entry objects for a key.
        for key in soup.find_all('key'):
            try:
                index[key.string].append(Entry(key.parent.parent))
            except KeyError:
                index[key.string] = [Entry(key.parent.parent)]
        return index

    def lookup(self, string):
        """Return a LIST of entry objects that is tied to each key."""
        return self._index[string]
   
    def keys(self):
        """Return all the keys of the index."""
        return self._index.keys()

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
