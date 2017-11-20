# Widgets.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""Widgets that go in the sidebar of the main application:  
     TagResults (tk.Listbox)
     TagInformationField (tk.Text)
     CurrentTagField (tk.Label)
     Table (tk.Text)


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""

import tkinter as tk
import tkinter.ttk as ttk
import app.gui.view_controller as view

from app.backend.keyword_instance import KeywordInstance
import app.backend.tag_templates as templates


class TagResults(tk.Listbox, view.Viewer, view.Stylable):
    """A ListBox of results pulled from the index."""
    
    def __init__(self, sidebar, scrollbar, app):
        tk.Listbox.__init__(self, sidebar, selectmode=tk.SINGLE, 
                            yscrollcommand=scrollbar.set)
        self.__app = app

        # Used to determine which kind of update to do.
        self.__old_entry = None
        
    def populate_tags(self, list_of_xml_ids):
        print("list: ", list_of_xml_ids)
        """Populate the ListBox with every element in a list."""
        self.delete(0, tk.END)

        # Don't display anything if an empty list is passed.
        if list_of_xml_ids != []:
            self.insert(tk.END, "NO TAG")

        for item in list_of_xml_ids:
            self.insert(tk.END, item)

    def cur_selection(self):
        """ Return an integer corrosponding to the value currently 
        selected in the listbox.
        """
        user_selection = self.curselection()
        if user_selection != ():
            # Returned as tuple, only want 1st value.
            return user_selection[0]
        else:
            return 0

    def xml_id_selection(self):
        """Returns the get_string in the listbox corrosponding to the current
        get_selected_entry."""
        user_selection = self.curselection()
        if user_selection != ():
            # Returned as tuple, only want 1st value.
            selected_index = user_selection[0]
            return self.get(selected_index)
        else:
            return ""

    def on_click(self, event):
        """Update the selected entry when an entry is clicked."""
        
        keyword_table = self.__app.get_keyword_table()

        # Don't allow changes to confirmed entries
        # This is trickier to do for clicks, since interacting with tkinter
        # using the mouse is not in this code. When you click, it sets the
        # get_selected_entry, and this on method is called after the click has been made
        # change the keyword table. this solution works, but causing a
        # "jumping get_selected_entry" and I don't like it - there must be a better
        # way.. you might need to find a way to access the default binding of
        # button one on nthe listbox.
        current_instance = keyword_table.get_current_entry()
        if current_instance.is_confirmed():
            self.update() # return the get_selected_entry to its proper place
            return
        
        current_instance.set_selection_index(self.cur_selection() - 1)

        keyword_table.notify_viewers_redraw()
    
    def update(self):
        """Redraw the widget based on the state of the program."""
       
        keyword_table = self.__app.get_keyword_table()

        current_instance = keyword_table.get_current_entry()
       
        # Makes sure not to repopulate everything unless the current entry has
        # been changed.
        if self.__old_entry != current_instance:
            print("Ignoring update...")
            self.populate_tags([entry.get_value("__xml:id__") for entry in current_instance.get_entries()])
            self.__old_entry = current_instance

        self.selection_clear(0, tk.END)
        if current_instance.get_selection_index() is not None:
            self.selection_set(current_instance.get_selection_index() + 1)
        else:
            self.selection_set(0)

        self.see(current_instance.get_selection_index() + 1)

    def style(self, styles):
        self.config(font=styles.f_subtitle, bg=styles.c_2)
        

class TagInformationField(tk.Text, view.Viewer, view.Stylable):
    """ Display information about the current get_selected_entry in TagResults."""
    
    def __init__(self, sidebar, app):
        tk.Text.__init__(self, sidebar)
        self.config(state=tk.DISABLED)
        self._app = app

    def __updateInformation(self, string):
        """ Display information about the item selected in TagResults."""
        self.config(state = tk.NORMAL)
        self.delete(0.0, tk.END)
        self.insert(tk.END, string)
        self.config(state = tk.DISABLED)
    
    def update(self):
        """Redraw the widget based on the state of the program."""

        keyword_table = self._app.get_keyword_table()

        current_instance = keyword_table.get_current_entry()
        selection_index = current_instance.get_selection_index()
       
        print("Current sel:", selection_index)
        if selection_index == -1:
            string = ""
        else:
            string = str(current_instance.get_selected_entry())
        
        self.__updateInformation(string)

    def style(self, styles):
        self.config(font=styles.f_text, bg=styles.c_2,
                highlightbackground=styles.c_2)


class CurrentTagField(tk.Label, view.Viewer, view.Stylable):
    """A label that shows the xml:id of the current get_selected_entry of the possible
    tags."""
    def __init__(self, sidebar, app):
        tk.Label.__init__(self, sidebar, text="Current:")
        self.__app = app

    def update(self):
        """Redraw the widget based on the state of the program."""

        keyword_table = self.__app.get_keyword_table()

        current_instance = keyword_table.get_current_entry()
        selection_index = current_instance.get_selection_index()
        
        if selection_index == -1:
            string = "NO TAG"
        else:
            string = str(current_instance.get_selected_entry().get_value("__xml:id__"))
        
        string = "Current:  " + string
        self.config(text=string)

    def style(self, styles):
        self.config(font=styles.f_button, bg=styles.c_2,
                highlightbackground=styles.c_2)


class TagPreviewField(tk.Label, view.Viewer, view.Stylable):
    """Shows a preview of how the xml tags around the current selecion will
    look."""
    def __init__(self, sidebar, app):
        tk.Label.__init__(self, sidebar, text="Preview:")
        self.__app = app

        # Will need updating after changes to templates.
        self.__templates = templates.TemplateIndex()

    def update(self):
        """Redraw the widget based on the current state of the program."""

        keyword_table = self.__app.get_keyword_table()

        current_instance = keyword_table.get_current_entry()
        selection_index = current_instance.get_selection_index()
        
        if selection_index == -1:
            string = ""
        else:
            template = current_instance.get_selected_entry().get_value("template")

            if template is "":
                tag = self.__templates.lookup("default")
            else:
                tag = self.__templates.lookup(template.lower())

            front_tag = tag.get_front() % tuple([current_instance.get_selected_entry().get_value(x) \
                                                 for x in tag.get_arguments()])
            back_tag = tag.get_back()
        
            string = "Preview:  " + front_tag + current_instance.get_string() + back_tag
        self.config(text=string)

    def style(self, styles):
        self.config(bg=styles.c_2, highlightbackground=styles.c_2)


class AllTaggedResultsTable(ttk.Treeview, view.Viewer, view.Stylable):
    def __init__(self, parent, app):
        self.treeStyle = ttk.Style() # Needed to change the background
        
        headings = ("#", "word", u"\u2713")
        ttk.Treeview.__init__(self, parent, columns=headings, show="headings")

        self._app = app

        for col in headings:
            self.heading(col, text=col.title())

        self.column("#", width=35, stretch=False)
        self.column("word", width=0, stretch=True)
        self.column(u"\u2713", width=20, stretch=False)

        self.unbind("<Up>")
        self.unbind("<Down>")

    def on_click(self, event):
        index = int(self.focus()) - 1
        self._app.get_keyword_table().jump_to(index)

    def update(self):
        keyword_table = self._app.get_keyword_table()

        # Delete everything, and repopulate it.
        for row in self.get_children():
            self.delete(row)

        # saves each row under a get_string version of its index in the
        # keyword table. row index is only incremented once each time,
        # to put a nice looking index on the sidebar.
        keyword_table_index = 0
        row_index = 1
        for entry in keyword_table:
            keyword_table_index += 1
            if not entry.is_ambiguous():
                continue

            # If the entry has been confirmed, give it a checkmark in the
            # table.
            confirmed_check = ""
            if entry.is_confirmed():
                confirmed_check = u"\u2713"

            self.insert("", tk.END, str(keyword_table_index), values=("%d" %
                                                                      row_index, entry.get_string(), confirmed_check))
            row_index += 1

        self.selection_add(str(keyword_table.get_current_index() + 1))
        self.see(str(keyword_table.get_current_index() + 1))

    def style(self, styles):
        self.treeStyle.configure("Treeview", background=styles.c_2,
                fieldbackground=styles.c_2)
