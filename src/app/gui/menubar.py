# MenuBar.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by John Hoskins: jbhoskins@email.wm.edu
# Last edit 4/22/17 by Margaret.

"""The top menu bar for our main application.  Holds File, Theme, and
Tools menus.  Through these menus one can open a new file, change the 
theme, save edits, and export the file as TEI Standard as preferable.
"""


import codecs 
import pickle
import shelve
import tkinter as tk
from tkinter import filedialog
import app.gui.index_editor as index_editor
import app.gui.template_editor as template_editor
import app.backend.tag_templates as templates


class Menubar(tk.Menu):
    """The top menubar of the application."""
    def __init__(self, app):
        root = app.get_root()
        tk.Menu.__init__(self, root)
        
        FileMenu(self, app)
        # These menus had either only one elemenet, or tons of unused elements,
        # so for now, until we have more functionality, I combined them into
        # one EditMenu.
        # ToolsMenu(self, app)
        # IndexMenu(self, app)
        # TemplateMenu(self, app)
        EditMenu(self, app)
        
        ThemeMenu(self, app)
        root.config(menu=self)


class DropdownMenu(tk.Menu):
    """Abstract class to describe the menus that dropdown from the menubar."""
    def __init__(self, menubar, app):
        tk.Menu.__init__(self, menubar, tearoff = 0)
        self._app = app


class FileMenu(DropdownMenu):
    """Menu that appears when you click 'File' on the top menubar."""
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)

        self.add_command(label="Open Session...", command=self.load_session)
        self.add_command(label="Save Session...", command=self.save_session)
        self.add_separator()
        self.add_command(label="Import text...", command=self.open_file)
        self.add_command(label="Export text...", command=self.export)
        self.add_separator()
        self.add_command(label="Export as TEI...")
        menubar.add_cascade(label="File", menu=self)
    
    def export(self):
        """ Exports the text of the interview with each word instance
        associated with its proper tag template, and arguments."""
        template_index = templates.TemplateIndex()
        
        string = self._app.get_text_view().get("1.0", tk.END)
        for instance in reversed(self._app.get_keyword_table()):
            word_inx = instance.get_selection_index()
            
            # Skip words set to NO TAG
            if word_inx == -1:
                continue

            # If no template is specified, use default template.
            if instance.get_selected_entry().get_value("template") is "":
                tag = template_index.lookup("default")
            else:
                tag = template_index.lookup(instance.get_selected_entry().get_value("template").lower())

            # Create the front and back tags from the templates
            front_tag = tag.get_front() % \
                        tuple([instance.get_selected_entry().get_value(x) for x in tag.get_arguments()])
            back_tag = tag.get_back()
            
            string = string[:instance.get_stop()] + back_tag + string[instance.get_stop():]
            string = string[:instance.get_start()] + front_tag + string[instance.get_start():]
        
        output_file = tk.filedialog.asksaveasfilename(defaultextension=".txt", initialdir="../output/")
        
        if output_file:
            with codecs.open(output_file, 'w', 'utf-8') as output_file:
                lines = string.splitlines()
                
                # Tag metadata and body.
                metadata = "<meta> metadata here </meta>\n\n"
                output_file.write(metadata)
                output_file.write("<body>\n\n")
                names = ["interviewer", "interviewee"] # Should ask the user for these

                j = 1
                # Run through lines, tag speaker utterances.
                for i in range(len(lines)):
                    line = lines[i]
                    name = names[(i % 4) // 2]
                    front_tag = '<u xml:id="sp' + str(j) + '" who="' \
                        + name + '">'
                    back_tag = '</u>\n\n'
                    if i % 2 == 0:
                        line = front_tag + line + back_tag
                        j += 1
                    output_file.write(line)
                
                # Close body tags and file.
                output_file.write("</body>")
            output_file.close()
            print("Export successful! Wrote %s" % output_file.name)

    def open_file(self):
        """Import text from a file into the program."""
        file_path = tk.filedialog.askopenfilename(initialdir="../input/")
        self._app.get_text_view().load_text(file_path)

    def save_session(self):
        """Saves the current session so that it can be resumed later."""
        
        output_file = tk.filedialog.asksaveasfilename(
            defaultextension=".rmtp", initialdir="../sessions/",
            filetypes=[("rmtp session files", "*.rmtp")]) 
        
        if output_file:
            shelf = shelve.open(output_file)
        else:
            raise IOError("File does not exist!")

        current_keyword_table = self._app.get_keyword_table()
        reference_to_views = current_keyword_table.get_viewers()
        reference_to_index = current_keyword_table.get_index()

        # Index object can be serialized, not sure if it needs to be. view
        # objects cannot be serialized, so they need to be erased from the
        # version being stored.
        current_keyword_table.prepare_for_serialization()

        # serialize the structures and save it as bytecode.
        shelf["keyword_table"] = current_keyword_table
        shelf["text"] = self._app.get_text_view().get("1.0", tk.END)
        shelf.close()

        # Bring the references back.
        for view in reference_to_views:
            current_keyword_table.register_viewer(view)

        current_keyword_table.set_index_object(reference_to_index)

    def load_session(self):
        """Loads a session from file so that it can be continued."""
        file_path = tk.filedialog.askopenfilename(initialdir="../sessions/",
                filetypes=[("rmtp session files", "*.rmtp")])

        if file_path:
            shelf = shelve.open(file_path)
            new_table = shelf["keyword_table"]
            text = shelf["text"]
            shelf.close()
        else:
            raise IOError("File does not exist.")

        # Restore the non-serializable data structure, and old text.
        for view in self._app.get_keyword_table().get_viewers():
            new_table.register_viewer(view)
        new_table.set_index_object(self._app.get_keyword_table().get_index())
        
        self._app.set_keyword_table(new_table)
        self._app.get_text_view().load_string(text)

        self._app.bind_keys()
        self._app.get_keyword_table().notify_viewers_redraw()


class ThemeMenu(DropdownMenu):
    """Menu that appears when you click 'Theme' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Bella", command=lambda: app.get_styler().change_theme(name="bella"))
        self.add_command(label="Sasha", command=lambda: app.get_styler().change_theme(name="sasha"))
        self.add_command(label="Elena", command=lambda: app.get_styler().change_theme(name="elena"))
        self.add_command(label="Maggie", command=lambda: app.get_styler().change_theme(name="maggie"))
        self.add_command(label="John", command=lambda: app.get_styler().change_theme(name="john"))
        self.add_command(label="Helena", command=lambda: app.get_styler().change_theme(name="helena"))
        
        menubar.add_cascade(label="Theme", menu=self)


class ToolsMenu(DropdownMenu):
    """Menu that appears when you click 'Tools' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Hide Greens")
        self.add_command(label="Hide Interviewer Text")
        self.add_command(label="Iterate")
        self.add_separator()
        self.add_command(label="Edit index...")
        
        menubar.add_cascade(label="Tools", menu=self)


class IndexMenu(DropdownMenu):
    """Menu that appears when you click 'Index' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Suggest new word")
        self.add_command(label="Edit index...", command=self.index_edit_pop)
        self.add_separator()
        self.add_command(label="Check for updates to index....")
        self.add_command(label="Submit updates to index...")
        
        menubar.add_cascade(label="Index", menu=self)

    def index_edit_pop(self):
        """ Opens the index editor popup window. """
        index_editor.IndexEditor(self._app.get_root())


class TemplateMenu(DropdownMenu):
    """Menu that appears when you click 'Templates' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Edit Templates...", command=self.template_edit_pop)

        menubar.add_cascade(label="Templates", menu=self)
    
    def template_edit_pop(self):
        """ Opens the template editor popup window. """
        template_editor.TemplateEditor(self._app.get_root())


class EditMenu(DropdownMenu):
    """Menu that appears when you click 'Edit' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Edit Templates...", command=self.template_edit_pop)
        self.add_command(label="Edit index...", command=self.index_edit_pop)

        menubar.add_cascade(label="Edit", menu=self)

    def template_edit_pop(self):
        """ Opens the template editor popup window. """
        template_editor.TemplateEditor(self._app.get_root())
    
    def index_edit_pop(self):
        """ Opens the index editor popup window. """
        index_editor.IndexEditor(self.app.get_root())
