# KeywordTable.py

# Created as part of the William and Mary Russian Movie Theater Project,
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu

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
words are get_string types):

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
    """ Class that encapsulates all interaction with the index.xml file, and
        facilitate the lookup of information in the xml file based on <key>
        attributes defined in the index.xml file itself.
    """

    def __init__(self, path):
        """Create a dictionary with <keys> (declined forms) as its
        dictionary keys and LISTS of Entry objects as its dictionary
        values.
        """
        input_file = open(path, "r", encoding="UTF-8")
        soup = BeautifulSoup(input_file, 'xml')
        input_file.close()

        self.__dictionary = dict()
        for key in soup.find_all('key'):
            key_string = str(key.string) # key.string is not a raw type
            if key_string in self.__dictionary.keys():
                self.__dictionary[key_string].append(Entry(key.parent.parent))
            else:
                self.__dictionary[key_string] = [Entry(key.parent.parent)]

    def lookup(self, string):
        return self.__dictionary[string]

    def keys(self):
        return self.__dictionary.keys()
