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

LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide.
"""


import codecs 
import tkinter as tk
import pickle
import shelve
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

        self.add_command(label="Open Session...", command=self.loadSession)
        self.add_command(label="Save Session...", command=self.saveSession)
        self.add_separator()
        self.add_command(label="Import text...", command=self.openFile)
        self.add_command(label="Export text...", command=self.export)
        self.add_separator()
        self.add_command(label="Export as TEI...")
        menubar.add_cascade(label="File", menu=self)
    
    def export(self):
        """ Exports the text of the interview with each word instance
        associated with its proper tag template, and arguments."""
        templateIndex = templates.TemplateIndex()
        
        string = self._app.get_text_view().get("1.0", tk.END)
        for instance in reversed(self._app.get_keyword_table()):
            word_inx = instance.get_selection_index()
            
            # Skip words set to NO TAG
            if word_inx == -1:
                continue

            # If no template is specified, use default template.
            if instance.get_selected_entry().get_value("template") is "":
                tag = templateIndex.lookup("default")
            else:
                tag =\
                templateIndex.lookup(instance.get_selected_entry().get_value("template").lower())

            # Create the front and back tags from the templates
            frontTag = tag.get_front() % tuple([instance.get_selected_entry().get_value(x) \
                                                for x in tag.get_arguments()])
            backTag = tag.get_back()
            
            string = string[:instance.get_stop()] + backTag + string[instance.get_stop():]
            string = string[:instance.get_start()] + frontTag + string[instance.get_start():]
        
        outputFile = tk.filedialog.asksaveasfilename(
            defaultextension=".txt", initialdir="../output/")
        
        if outputFile:
            with codecs.open(outputFile, 'w', 'utf-8') as outputFile:
                lines = string.splitlines()
                j = 1
                
                # Tag metadata and body.
                metadata = "<meta> metadata here </meta>\n\n"
                outputFile.write(metadata)
                outputFile.write("<body>\n\n")
                names = ["interviewer", "interviewee"] #should ask the user.
                
                # Run through lines, tag speaker utterances.
                for i in range(len(lines)):
                    line = lines[i]
                    name = names[(i % 4) // 2]
                    frontTag = '<u xml:id="sp' + str(j) + '" who="' \
                        + name + '">'
                    backTag = '</u>\n\n'                    
                    if i % 2 == 0:
                        line = frontTag + line + backTag
                        j += 1
                    outputFile.write(line)
                
                # Close body tags and file.
                outputFile.write("</body>")    
            outputFile.close()
            print("Export successful! Wrote %s" % outputFile.name)



    def openFile(self):
        """Import text from a file into the program."""
        filePath = tk.filedialog.askopenfilename(initialdir="../input/")
        self._app.get_text_view().load_text(filePath)

    def saveSession(self):
        """Saves the current session so that it can be resumed later."""
        
        outputFile = tk.filedialog.asksaveasfilename(
            defaultextension=".rmtp", initialdir="../sessions/",
            filetypes=[("rmtp session files", "*.rmtp")]) 
        
        if outputFile:
            shelf = shelve.open(outputFile)
        else:
            print("File does not exist!")
            return

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

        current_keyword_table.set_index(reference_to_index)

    def loadSession(self):
        """Loads a session from file so that it can be continued."""
        file_path = tk.filedialog.askopenfilename(initialdir="../sessions/",
                filetypes=[("rmtp session files", "*.rmtp")])

        if file_path:
            shelf = shelve.open(file_path)
#            f = open("../sessions/savedSessionDude", "rb")
            new_table = shelf["keyword_table"]
            text = shelf["text"]
            shelf.close()
        else:
            print("File does not exist.")
            return

        for view in self._app.get_keyword_table().get_viewers():
            new_table.register_viewer(view)
        new_table.set_index(self._app.get_keyword_table().get_index())
        
        self._app.set_keyword_table(new_table)
        self._app.get_text_view().load_string(text)

        self._app.bind_keys()
        self._app.get_keyword_table().notify_viewers_redraw()


class ThemeMenu(DropdownMenu):
    """Menu that appears when you click 'Theme' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(
            label="Bella", command=lambda: app.get_styler().changeTheme(name="bella"))
        self.add_command(
            label="Sasha", command=lambda: app.get_styler().changeTheme(name="sasha"))
        self.add_command(
            label="Elena", command=lambda: app.get_styler().changeTheme(name="elena"))
        self.add_command(
            label="Maggie", command=lambda: app.get_styler().changeTheme(name="maggie"))
        self.add_command(
            label="John", command=lambda: app.get_styler().changeTheme(name="john"))
        self.add_command(
            label="Helena", command=lambda: app.get_styler().changeTheme(name="helena"))
        
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
        
        self.app = app
        
        self.add_command(label="Suggest new word")
        self.add_command(label="Edit index...", command=self.indexEditPop)
        self.add_separator()
        self.add_command(label="Check for updates to index....")
        self.add_command(label="Submit updates to index...")
        
        menubar.add_cascade(label="Index", menu=self)

    def indexEditPop(self):
        """ Opens the index editor popup window. """
        index_editor.IndexEditor(self.app.get_root())

class TemplateMenu(DropdownMenu):
    """Menu that appears when you click 'Templates' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)

        self.app = app

        self.add_command(label="Edit Templates...",
                command=self.templateEditPop)
        
        menubar.add_cascade(label="Templates", menu=self)
    
    def templateEditPop(self):
        """ Opens the template editor popup window. """
        template_editor.TemplateEditor(self.app.get_root())

class EditMenu(DropdownMenu):
    """Menu that appears when you click 'Edit' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)

        self.app = app

        self.add_command(label="Edit Templates...",
                command=self.templateEditPop)
        self.add_command(label="Edit index...", command=self.indexEditPop)
        
        menubar.add_cascade(label="Edit", menu=self)

    def templateEditPop(self):
        """ Opens the template editor popup window. """
        template_editor.TemplateEditor(self.app.get_root())
    
    def indexEditPop(self):
        """ Opens the index editor popup window. """
        index_editor.IndexEditor(self.app.get_root())
