# WordeCache.py

# Created as part of the William and Mary Russian Movie Theater Project,
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu

""" This module contains classes to parse a specifically formatted XML file for
    keywords and data, and to parse a textfile for those keywords. """

class KeywordInstance:
    """ A data container for all relevant information about a "match instance", or
    an instance where the algorithm finds a matching get_string in the body of text
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
        self.__ambiguous = True

        self.__confirmed = False

    def set_start(self, start):
        self.__start = start

    def set_stop(self, stop):
        self.__stop = stop

    def set_string(self, string):
        self.__string = string

    def set_start(self, start):
        self.__start = start

    def set_entries(self, entries):
        self.__entries = entries

    def set_selection_index(self, index):
        self.__selected_entry = index

    def get_selection_index(self):
        """ Return the integer that corrosponds to the entry that has been
        selected for the instance."""
        return self.__selected_entry

    def get_selected_entry(self):
        """ Return the Entry object that is currently selected. """
        print("selected entry", self.__entries[self.__selected_entry])
        return self.__entries[self.__selected_entry]

    def get_string(self):
        """Return the get_string of the instance."""
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

    def is_ambiguous(self):
        return self.__ambiguous

    def is_confirmed(self):
        return self.__confirmed

    def toggle_confirm(self):
        """Inverts the boolean value of confirmed."""
        self.__confirmed = not self.__confirmed

    def toggle_ambiguous(self):
        print("b4", self.__ambiguous)
        self.__ambiguous = not self.__ambiguous
        print("aftr", self.__ambiguous)

    def __eq__(self, other):
        """ Overloads the == operator. """

        # All instances have a unique start position, (number of charecors from
        # start) so use it to determine equality.
        if other is None:
            return False
        else:
            return other.__start == self.__start
