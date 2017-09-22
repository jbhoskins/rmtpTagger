# KeywordTable.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

from bs4 import BeautifulSoup

class Entry:
    """Data Structure to store the information of each entry of index.xml."""
    
    def __init__(self, bs4_object):
        self._info = []

        # Underscores to avoid name conflicts, if it was just "type"
        # instead of "__type__" you would run into issues if the user
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
