# KeywordTable.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

from app.backend.index_entry import Entry
from bs4 import BeautifulSoup
from enum import Enum

class MatchState(Enum):
    """ Enumerated type to increase readibility of the match validator."""
    unique_match = 2 # kepy to ease integration, phase out references to this
    found_match = 2
    potential_match = 1
    no_match = 0

class ParseTree:
    """ Class that encapsulates all interaction with the index.xml file. It
    provides two primary functionalities:
        
        2: Builds a parse tree of the keys themselves, to provide a way to
        determine, one word at a time, if a string with an arbitrary number of
        words is a valid key. An important consequence of this is that longer keys
        will always take precedence over nested keys that are shorter.
        
        This should probably be refactored into a parse-tree class and a seperate
        index class, splitting up the functionalities."""

    def __init__(self, listOfWords):
        self._rootNode = dict()
        self._currentNode = self._rootNode

        self._makeParseTree(listOfWords)

    def _makeParseTree(self, listOfKeys):
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
        for key in listOfKeys:
            self._currentNode = self._rootNode

            i = 0
            for i in range(len(key) - 1):
                if key[i] not in self._currentNode.keys():
                    self._currentNode[key[i]] = dict()
                self._currentNode = self._currentNode[key[i]]
            
            # Handles the case of an empty key like <key></key>
            if len(key) > 1:
                i += 1
             
            try:
                self._currentNode = self._currentNode[key[i]]
            except:
                self._currentNode[key[i]] = dict()
                self._currentNode = self._currentNode[key[i]]
                
            self._currentNode[None] = None

        self.reset()
                
    def print_(self):
        """ Prints a semi-formatted representation of the multi-word validator.
        Used for debugging."""
        for key in self._rootNode.keys():
            print(key)
            print('  ', self._rootNode[key])
    
    def validate(self, word):
        """ Returns a value that tells you whether the string given is a valid
        next word in the parse tree. """
        if word in self._currentNode.keys(): # string is a valid next word
            # Prep the multiValidator to look at the next set of possible
            # strings.
            self._currentNode = self._currentNode[word]
            # The dictionary {None : None} signifies the termination of a key -
            # check if it is present, and if it is the only possible
            # continuation of the tree.
            if None in self._currentNode.keys():
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
        self._currentNode = self._rootNode
    
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
