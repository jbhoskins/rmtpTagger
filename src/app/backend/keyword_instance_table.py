# KeywordTable.py

# Created as part of the William and Mary Russian Movie Theater Project,
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu

""" A table of KeywordInstances, with the inclusion of a index, to keep track
of which instance is currently being examined/edited.

This the main data structure of the program during runtime.

This program utilizes the Observer design pattern, and this class is the
"Subject" of this pattern - whenever it changes, it's viewers need to be
updated to reflect the new changes.


EDITED:
Margaret, 4/22/17
Changed style of code to conform to the PEP8 styleguide.
"""
import os
from bs4 import BeautifulSoup
import re

import app.gui.view_controller as view
from app.backend.keyword_instance import KeywordInstance
from app.backend.index import Index
from app.backend.parse_tree import ValidityCode
from app.backend.parse_tree import ParseTree

class KeywordInstanceTable:
    def __init__(self):
        self.__current = 0
        self.__instances = []

        # Registered viewers for observer design pattern
        self.__views = []

        self.__indexObject = Index(os.path.join("res", "index.xml"))
        self.__parse_tree = ParseTree(self.__indexObject.keys())

    def get_current_entry(self):
        """Returns the currently selected KeywordInstance."""
        if len(self.__instances) == 0:
            return None
        else:
            return self.__instances[self.__current]

    def get_current_index(self):
        return self.__current

    def get_viewers(self):
        return self.__views

    def get_index(self):
        return self.__indexObject

    def set_index_object(self, index):
        self.__indexObject = index

    def append(self, keyword_instance):
        assert type(keyword_instance) is KeywordInstance, "Only KeywordInstances can be appended."
        self.__instances.append(keyword_instance)

    def lookup(self, start_index):
        """Returns the KeywordInstance that corrosponds to the given CHARECTOR index."""

        # This could be a binary search.

        for index, instance in enumerate(self.__instances):
            if instance.get_start() <= start_index <= instance.get_stop():
                if instance.is_ambiguous():
                    self.__current = index
                    return instance
                else:
                    return None
        return None

    def jump_to(self, tableIndex):
        """Skip to a certain keyword table index."""
        # assert to prevent jumps to pronouns, etc.
        assert self.__instances[tableIndex].is_ambiguous()
        self.__current = tableIndex % len(self.__instances)
        self.notify_viewers_redraw()

    def make_index(self):
        """Instantiates an Index object. Needed for session loading."""
        self.__indexObject = Index("../META/index.xml")

    def reset(self):
        """Dereferences the table, and resets the current cursor to 0."""
        self.__instances = []
        self.__current = 0

    def next_valid_entry(self, event=None):
        """ Returns the next valid entry that is ambiguous, and set the cursor
        to that index."""

        table_length = len(self.__instances)
        for i in range(1, table_length):
            new_index = (self.__current + i) % table_length
            if self.__instances[new_index].is_ambiguous():
                break
        self.__current = new_index

        self.notify_viewers_redraw()

    def previous_valid_entry(self, event=None):
        """ Returns the previous valid entry that is ambiguous, and set the cursor
        to that index."""

        table_length = len(self.__instances)
        for i in range(1, table_length):
            new_index = (self.__current - i) % table_length
            if self.__instances[new_index].is_ambiguous():
                break
        print("new:", new_index)
        self.__current = new_index

        self.notify_viewers_redraw()
    
    def next_tag(self, event=None):
        """ Move to the next tag in the list of tag suggestions (entry list) """

        # Don't allow changes to confirmed entries
        if self.get_current_entry().is_confirmed():
            return

        # Some weird mod arithmetic here, but it is needed to move seamlessly
        # through the range, (-1, len(possibleTags) - 1)
        new_index = self.get_current_entry().get_selection_index()
        new_index += 2
        new_index %= (len(self.get_current_entry().get_entries()) + 1)
        new_index -= 1
        self.get_current_entry().set_selection_index(new_index)

        self.notify_viewers_redraw()

    def prev_tag(self, event=None):
        """ Move to the previous tag in the list of tag suggestions (entry list) """

        # Don't allow changes to confirmed entries
        if self.get_current_entry().is_confirmed():
            return

        # Some weird mod arithmetic here, but it is needed to move seamlessly
        # through the range, (-1, len(possibleTags) - 1)
        new_index = self.get_current_entry().get_selection_index()
        new_index %= (len(self.get_current_entry().get_entries()) + 1)
        new_index -= 1
        self.get_current_entry().set_selection_index(new_index)

        self.notify_viewers_redraw()

    def toggle_confirm_current(self, event=None):
        self.get_current_entry().toggle_confirm()
        self.notify_viewers_redraw()

    def fill_table(self, string):
        """Build a sorted (by start index) table of all KeywordInstances."""

        self.reset()

        # Ideally, make a generator for each relevant line
        iterator = re.finditer("\w+(-\w+)?", string)
        keyword = ""
        potential_instance = KeywordInstance()
        found_match = False
        word = next(iterator)

        try:
            while True: # Yes, it's an infinite loop. It's the solution the
                        # docs suggested.

                # Kind of inefficient, but seems to be fast enough
                # inx = int(tk.Text.index("1.0+%sc" % word.start()).split(".")[0])
                inx = string.count("\n", 0, word.start()) + 1

                # Only run the next bit if it's an interviewee. use "if true"
                # to not skip any lines.
                # if True:
                if  (inx % 4 - 1) != 0:
                    validity_code = self.__parse_tree.validate(word.group().lower())

                    if validity_code == ValidityCode.no_match:

                        # This is the point when an entry is actually
                        # saved. When it finds a match, it waits until
                        # it hits a zero to save it, in case there are a
                        # couple keys like so: "фон", "фон триер". We
                        # want the second, longer tag, not the shorter.
                        if found_match:
                            potential_instance.set_string(keyword)
                            index_entries = self.__indexObject.lookup(keyword.lower())
                            potential_instance.set_entries(index_entries)
                            # set to unambiguous. checks len is 1 to avoid
                            # multiple definitions of word bugs by accident.

                            if len(index_entries) == 1 and index_entries[0].get_value("unambiguous") == "true":
                                potential_instance.toggle_ambiguous() # set to false (unambiguous)

                            self.__instances.append(potential_instance)

                            # Reset the saved values.
                            keyword = ""
                            potential_instance = KeywordInstance()
                            found_match = False

                            # Continue rechecks the same word with a re-
                            # set multiTest, in case two keywords are
                            # next to each other.
                            continue

                        keyword = ""
                        potential_instance = KeywordInstance()

                    elif validity_code == ValidityCode.potential_match:
                        # If there is a word, add a space before the
                        # next one.
                        if keyword != "":
                            keyword += " "
                        else:
                            potential_instance.set_start(word.start())
                        keyword += word.group()

                    elif validity_code == ValidityCode.found_match:
                        if keyword != "":
                            keyword += " "
                        else:
                            potential_instance.set_start(word.start())

                        keyword += word.group()
                        potential_instance.set_stop(word.end())
                        found_match = True

                word = next(iterator)

        except StopIteration:
            # May need to save the last information, in case the final
            # word is a keyword
            pass

        self.next_valid_entry() # start at the first value

    # ------- Methods to implement subject / observer design pattern --------

    def notify_viewers_redraw(self):
        for view in self.__views:
            view.update()

    def register_viewer(self, newView):
        self.__views.append(newView)

    def delete_viewer(self, viewToDelete):
        self.__views.remove(viewToDelete)

    # ------------------------------------------------------------------------

    def prepare_for_serialization(self):
        # These elements are not serializable, so they need to be deleted.
        self.__views = []
        self.__indexObject = None

    def __next__(self):
        if self.__iter_current == len(self.__instances) - 1:
            raise StopIteration
        else:
            self.__iter_current += 1
            return self.__instances[self.__iter_current]

    def __iter__(self):
        self.__iter_current = -1
        return self

    def __reversed__(self):
        return reversed(self.__instances)
