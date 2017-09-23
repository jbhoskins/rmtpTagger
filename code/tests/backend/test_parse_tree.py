import unittest
from app.backend.parse_tree import ParseTree
from app.backend.parse_tree import MatchState

class ParseTreeTesterSimple(unittest.TestCase):
    def setUp(self):
        testInput = [["John", "Hoskins"], 
                     ["John", "Wick", "Buddy"],
                     ["John"]]
        self._parseTree = ParseTree(testInput)

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
        assert len(self._parseTree._currentNode) == 3

    def test_correct_children(self):
        self._parseTree.validate("John")
        assert "Hoskins" in self._parseTree._currentNode.keys()
        assert "Wick" in self._parseTree._currentNode.keys()
        assert None in self._parseTree._currentNode.keys()

    def test_children_terminate_three(self):
        self._parseTree.validate("John")
        self._parseTree.validate("Wick")
        self._parseTree.validate("Buddy")
        assert len(self._parseTree._currentNode) == 1
        assert None in self._parseTree._currentNode.keys()
    
    def test_children_terminate_one(self):
        self._parseTree.validate("John")
        assert len(self._parseTree._currentNode) == 3
        assert None in self._parseTree._currentNode.keys()
    
    
    def test_children_terminate_two(self):
        self._parseTree.validate("John")
        self._parseTree.validate("Hoskins")
        assert None in self._parseTree._currentNode.keys()
        assert len(self._parseTree._currentNode) == 1

    # Match code testing
    def test_no_match_root(self):
        assert self._parseTree.validate("test") == MatchState.no_match
    
    def test_no_match_child(self):
        self._parseTree.validate("John")
        assert self._parseTree.validate("test") == MatchState.no_match

    def test_potential_match(self):
        self._parseTree.validate("John")
        assert self._parseTree.validate("Wick") == MatchState.potential_match
    
    def test_match_found_one(self):
        assert self._parseTree.validate("John") == MatchState.found_match

    def test_match_found_two(self):
        self._parseTree.validate("John")
        assert self._parseTree.validate("Hoskins") == MatchState.found_match

    def test_match_found_three(self):
        self._parseTree.validate("John")
        self._parseTree.validate("Wick")
        assert self._parseTree.validate("Buddy") == MatchState.found_match

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
    
    def test_match_found_one(self):
        assert self._parseTree.validate("John") == MatchState.no_match

class ParseTreeTesterDuplicateSingleKeys(unittest.TestCase):
    # Assumes that a null structure passed in should produce {None:None}
    def setUp(self):
        testInput = [["test"], ["test"], ["test"]]
        self._parseTree = ParseTree(testInput)
                     
    def test_not_none(self):
        assert self._parseTree != None
    
    def test_root_node_is_active_node(self):
        # Should be true after initialization
        assert self._parseTree._rootNode == self._parseTree._currentNode

    def test_is_one_level(self):
        assert len(self._parseTree._rootNode.keys()) == 1
        assert "test" in self._parseTree._rootNode.keys()

    def test_after_one_level_terminates(self):
        assert self._parseTree._rootNode["test"] == {None:None}
    
    def test_match_found(self):
        assert self._parseTree.validate("test") == MatchState.found_match
    
    def test_no_match(self):
        assert self._parseTree.validate("John") == MatchState.no_match

class ParseTreeTesterDuplicateMultipleKeys(unittest.TestCase):
    # Assumes that a null structure passed in should produce {None:None}
    def setUp(self):
        testInput = [["test", "one", "two", "three"], 
                     ["test", "one", "two", "three"], 
                     ["test", "one", "two", "three"]]
        self._parseTree = ParseTree(testInput)
                     
    def test_not_none(self):
        assert self._parseTree != None
    
    def test_root_node_is_active_node(self):
        # Should be true after initialization
        assert self._parseTree._rootNode == self._parseTree._currentNode

