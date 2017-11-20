# WordeCache.py

# Created as part of the William and Mary Russian Movie Theater Project,
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

""" This module contains classes to parse a specifically formatted XML file for
    keywords and data, and to parse a textfile for those keywords. """

class KeywordInstance:
    """ A data container for all relevant information about a "match instance", or
    an instance where the algorithm finds a matching string in the body of text
    that has been fed into it.

    The class contains this information in addition to meta information about the
    instance, such as whether the user can affect its values (unambiguous) and
    which entry out of the candidates the user wants associated with it
    (selectedEntry)

    The class also contains (and probably shouldn't, probably should be
    refactored since this creates a lot of duplicate and unnecessary
    information) a list of the candidate entries themselves.

    EDITED:

    Margaret, 4/22/17

    Changed style of code to conform to the PEP8 styleguide.
    """

    def __init__(self):

        self.__string = ""
        self.__start = None
        self.__stop = None
        self.__entries = []
        self.__selected_entry = 0
        self.__unambiguous = False

        self._confirmed = False

    def get_selection_index(self):
        """ Return the integer that corrosponds to the entry that has been
        selected for the instance."""
        return self.__selectedEntry

    def set_selection_index(self, index):
        self.__selected = index

    def get_selection(self):
        """ Return the Entry object that is currently selected. """
        return self.__entries[self.__selected_entry]

    def get_string(self):
        """Return the string of the instance."""
        return self.__string

    def get_start(self):
        """Return the start index (in charectors) of the instance."""
        return self.__start

    def get_stop(self):
        """Return the stop index (in charectors) of the instance."""
        return self.__stop

    def get_entries(self):
        """Return the list of possible entries for the instance."""
        return self.__entries

    def toggle_confirm(self):
        """Inverts the boolean value of confirmed."""
        self.__confirmed = not self.__confirmed

    def __eq__(self, other):
        """ Overloads the == operator. """

        # All instances have a unique start position, (number of charecors from
        # start) so use it to determine equality.
        return other.__start == self.__start
