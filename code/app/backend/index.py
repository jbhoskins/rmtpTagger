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

"""


from bs4 import BeautifulSoup
from app.backend.index_entry import Entry

class Index:
    """ Class that encapsulates all interaction with the index.xml file. It
    provides two primary functionalities:
        
        1: Permit the lookup of information in the xml file based on <key>
        attributes defined in the index.xml file itself.
    """
        
    def __init__(self, path):
        """Create a dictionary with <keys> (declined forms) as its 
        dictionary keys and LISTS of _Entry objects as its dictionary
        values.
        """
        f = open(path, "r", encoding="UTF-8")
        soup = BeautifulSoup(f, 'xml')
        f.close()

        self._index = dict()
        for key in soup.find_all('key'):
            try:
                self._index[key.string].append(Entry(key.parent.parent))
            except KeyError:
                self._index[key.string] = [Entry(key.parent.parent)]

    def lookup(self, string):
        """Return a LIST of entry objects that is tied to each key."""
        return self._index[string]
   
    def keys(self):
        """Return all the keys of the index."""
        return self._index.keys()

