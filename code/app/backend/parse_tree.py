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
    found_match = 2
    potential_match = 1
    no_match = 0

class ParseTree:
    """ Class that encapsulates all interaction with the index.xml file. It
    provides two primary functionalities:
        
        2: Builds a parse tree of the keys themselves, to provide a way to
        determine, one word at a time, if a get_string with an arbitrary number of
        words is a valid key. An important consequence of this is that longer keys
        will always take precedence over nested keys that are shorter.
        
        This should probably be refactored into a parse-tree class and a seperate
        index class, splitting up the functionalities."""

    def __init__(self, list_of_words):
        self.__root_node = dict()
        self.__current_node = self.__root_node

        self.__make_parse_tree(list_of_words)

    def __make_parse_tree(self, list_of_keys):
        """ Creates a tree of dictionaries that represents a parse-tree of
        every <key>.
        
        For example, given four keys:
        
        The
        The Quick
        The Slow
        Fox

        The Dictionary {None : None} is used to signify the termination of a
        get_string.

        the resulting dictoinary would have the keys {The, Fox}.
        
        - The value of ["The"] would be another dictionary with the keys
          {"Quick", "Slow", None}
        - The value of ["Fox"] would be another dictionary with the keys {None}
        """
        for key in list_of_keys:
            self.__current_node = self.__root_node
            key = key.split()
            for word in key:
                if word not in self.__current_node.keys():
                    self.__current_node[word] = dict()
                
                self.__current_node = self.__current_node[word]

            self.__current_node[None] = None

        self.reset()
                
    def print_(self):
        """ Prints a semi-formatted representation of the multi-word validator.
        Used for debugging."""
        for key in self.__root_node.keys():
            print(key)
            print('  ', self.__root_node[key])
    
    def validate(self, word):
        """ Returns a value that tells you whether the get_string given is a valid
        next word in the parse tree. """
        if word in self.__current_node.keys(): # get_string is a valid next word
            # Prep the multiValidator to look at the next set of possible
            # strings.
            self.__current_node = self.__current_node[word]
            # The dictionary {None : None} signifies the termination of a key -
            # check if it is present, and if it is the only possible
            # continuation of the tree.
            if None in self.__current_node.keys():
                return MatchState.found_match
            return MatchState.potential_match
        
        # It is important to note here, that the parse tree is only reset
        # automatically when it hits a "no_match". This is deliberate, and used
        # in the actual parse algorithm to make sure that all keys, including
        # consecutive keys, are considered.
        self.reset()
        return MatchState.no_match

    def reset(self):
        """ Resets the multi-word validator to the beginning of the parse tree."""
        self.__current_node = self.__root_node
    
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
