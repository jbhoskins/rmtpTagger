# WordeCache.py

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.


class KeywordInstance(dict):
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
        dict.__init__(self)
        
        self["string"] = ""
        self["start"] = None
        self["stop"] = None
        self["entries"] = []
        self["selectedEntry"] = 0
        self["unambiguous"] = False

        self["confirmed"] = False

    def selectionIndex(self):
        """ Return the integer that corrosponds to the entry that has been
        selected for the instance."""
        return self["selectedEntry"]

    def selection(self):
        """ Return the Entry object that is currently selected. """
        return self["entries"][self["selectedEntry"]]

    def __eq__(self, other):
        """ Overloads the == operator. """

        # All instances have a unique start position, (number of charecors from
        # start) so use it to determine equality.
        return other["start"] == self["start"]

    def string(self):
        """Return the string of the instance."""
        return self["string"]

    def start(self):
        """Return the start index (in charectors) of the instance."""
        return self["start"]

    def stop(self):
        """Return the stop index (in charectors) of the instance."""
        return self["stop"]

    def entries(self):
        """Return the list of possible entries for the instance."""
        return self["entries"]

    def toggleConfirm(self):
        self["confirmed"] = not self["confirmed"]
        print(self["confirmed"])


if __name__ == "__main__":
    cce = [Cache()]

    cce[0]["string"] = "Hey"
    print(cce[0]["string"])
    print("before", cce[0]["selectedEntry"])
    cce[0].select(5)
    print("after", cce[0]["selectedEntry"])
