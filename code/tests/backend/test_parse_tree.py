import unittest
from bs4 import BeautifulSoup
from app.backend.parse_tree import ParseTree
from app.backend.parse_tree import MatchState

class ParseTreeTesterSimple(unittest.TestCase):
    def setUp(self):
        self._parseTree = ParseTree([["John", "Hoskins"], ["John", "Wick"]])

    def test_not_none(self):
        assert self._parseTree != None

    def test_root_node_is_active_node(self):
        # Should be true after initialization
        assert self._parseTree._rootNode == self._parseTree._currentNode

    def test_one_root_key(self):
        assert len(self._parseTree._rootNode.keys()) == 1
        assert "John" in self._parseTree._rootNode.keys()

    def test_two_children(self):
        self._parseTree.validate("John")
        assert len(self._parseTree._currentNode) == 2

    def test_correct_children(self):
        self._parseTree.validate("John")
        assert "Hoskins" in self._parseTree._currentNode.keys()
        assert "Wick" in self._parseTree._currentNode.keys()


    def test_children_terminate_one(self):
        self._parseTree.validate("John")
        self._parseTree.validate("Hoskins")
        assert len(self._parseTree._currentNode) == 1
        assert None in self._parseTree._currentNode.keys()
    
    def test_children_terminate_two(self):
        self._parseTree.validate("John")
        self._parseTree.validate("Wick")
        assert len(self._parseTree._currentNode) == 1
        assert None in self._parseTree._currentNode.keys()

    # Match code testing
    def test_no_match_root(self):
        assert self._parseTree.validate("test") == MatchState.no_match
    
    def test_no_match_child(self):
        self._parseTree.validate("John")
        assert self._parseTree.validate("test") == MatchState.no_match

    def test_potential_match(self):
        assert self._parseTree.validate("John") == MatchState.potential_match
    
    def test_match_found_one(self):
        self._parseTree.validate("John")
        assert self._parseTree.validate("Hoskins") == MatchState.found_match

    def test_match_found_two(self):
        self._parseTree.validate("John")
        assert self._parseTree.validate("Wick") == MatchState.found_match

class ParseTreeTesterNull(unittest.TestCase):
    # Assumes that a null structure passed in should produce {None:None}
    def setUp(self):
        self._parseTree = ParseTree([[]])
    
    def test_not_none(self):
        assert self._parseTree != None
    
    def test_root_node_is_active_node(self):
        # Should be true after initialization
        assert self._parseTree._rootNode == self._parseTree._currentNode

    def test_one_level_none(self):
        assert len(self._parseTree._rootNode.keys()) == 1
        assert None in self._parseTree._rootNode.keys()

    def test_one_level_none_termination(self):
        assert self._parseTree._rootNode[None] == None
