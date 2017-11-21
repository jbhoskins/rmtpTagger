# Created as part of the William and Mary Russian Movie Theater Project,
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu

# from bs4 import BeautifulSoup

""" This module contains classes to parse a specifically formatted XML file for
    keywords and data, and to parse a textfile for those keywords. """

class Entry:
    """Data Structure to store the information of each entry of index.xml.

    It is a ordered list of key:value pairs, where each key is the tag of
    the xml, and the value is the text associated with it. For example,

    <key>value</key>

    becomes

    (key, value)
    """

    def __init__(self, bs4_object):
        self.__info = []

        # Underscores to avoid name conflicts
        self.__info.append(("__type__", str(bs4_object.name)))

        # If an xml:id is not specified, set it to an empty get_string.
        try:
            self.__info.append(("__xml:id__", str(bs4_object["xml:id"])))
        except KeyError:
            self.__info.append(("__xml:id__", ""))


        # Attach all information in the index.xml entry to the object.
        for info in bs4_object:
            if str(info.name) != 'keys' and info.name is not None:
                self.__info.append((str(info.name), str(info.string)))

    def get_value(self, string):
        """ Return the value associated with the key provided."""
        for entry in self.__info:
            if entry[0] == string:
                return entry[1]
        return "" # Not found


    def __str__(self):
        string = ''
        for entry in self.__info:
            string = string + entry[0] + ': ' + entry[1] + '\n'
        return string
