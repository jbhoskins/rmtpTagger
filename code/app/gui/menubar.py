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
        tk.Menu.__init__(self, app._root)
        
        FileMenu(self, app)
        # These menus had either only one elemenet, or tons of unused elements,
        # so for now, until we have more functionality, I combined them into
        # one EditMenu.
        # ToolsMenu(self, app)
        # IndexMenu(self, app)
        # TemplateMenu(self, app)
        EditMenu(self, app)
        
        ThemeMenu(self, app)
        app._root.config(menu=self)


class DropdownMenu(tk.Menu):
    """Abstract class to describe the menus that dropdown from the menubar."""
    def __init__(self, menubar, app):
        tk.Menu.__init__(self, menubar, tearoff = 0)
        self.app = app


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
        
        string = self.app._textView.get("1.0", tk.END)
        for entry in reversed(self.app._keywordTable):
            word = entry.string().lower()
            word_inx = entry.selectionIndex()
            #sel = self.app.index.lookup(word)[word_inx]
            
            # Skip words set to NO TAG
            if word_inx == -1:
                continue

            # These lines are the ones that need updating.
            # frontTag = "<rs type=\"%s\" key=\"%s\">" % (sel.type(), sel.xmlId())
            # backTag = "</rs>"
            if entry.selection().getValue("template") is "":
                tag = templateIndex.lookup("default")
            else:
                tag =\
                templateIndex.lookup(entry.selection().getValue("template").lower())

            # Interesting problem, to have strings with a variable number of
            # arguments. It looks like you can do it with tuples. Use a string,
            # cast is as a tuple, and then mod it with the tags.
            frontTag = tag.getFront() % tuple([entry.selection().getValue(x)\
                for x in tag.getArguments()])
            backTag = tag.getBack()
            
            string = string[:entry.stop()] + backTag + string[entry.stop():]
            string = string[:entry.start()] + frontTag + string[entry.start():]
        
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
        self.app._textView.loadText(filePath)

    def saveSession(self):
        """Saves the current session so that it can be resumed later."""
        
        outputFile = tk.filedialog.asksaveasfilename(
            defaultextension=".rmtp", initialdir="../sessions/") 
        
        if outputFile:
            shelf = shelve.open(outputFile)
        else:
            print("File does not exist!")
            return
        
        print("Currently Selected entry is ON SAVE:", self.app._keywordTable[11]["selectedEntry"])

        referenceToIndex = self.app._keywordTable._indexObject
        referenceToViews = self.app._keywordTable._views

        # Index object can be serialized, not sure if it needs to be. view
        # objects cannot be serialized, so they need to be erased from the
        # version being stored. 
        self.app._keywordTable._indexObject = None
        self.app._keywordTable._views = []

        # serialize the structures and save it as bytecode.
        shelf["keywordTable"] = self.app._keywordTable
        shelf["text"] = self.app._textView.get("1.0", tk.END)
        shelf.close()

        # Bring the references back.
        self.app._keywordTable._indexObject = referenceToIndex
        self.app._keywordTable._views = referenceToViews
        

    def loadSession(self):
        """Loads a session from file so that it can be continued."""
        filePath = tk.filedialog.askopenfilename(initialdir="../sessions/")

        if filePath:
            shelf = shelve.open(filePath)
#            f = open("../sessions/savedSessionDude", "rb")
            newTable = shelf["keywordTable"]
            text = shelf["text"]
            shelf.close()
        else:
            print("File does not exist.")
            return

        print("Currently Selected entry is ON LOAD:", newTable[11]["selectedEntry"])
        
        
        newTable._indexObject = self.app._keywordTable._indexObject
        newTable._views = self.app._keywordTable._views
        
        self.app._keywordTable = newTable
        self.app._textView.loadString(text)

        self.app._bindKeys()
        self.app._keywordTable.notifyViewersRedraw()
        

class ThemeMenu(DropdownMenu):
    """Menu that appears when you click 'Theme' from the top menubar. """
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(
            label="Bella", command=lambda: app._changeTheme(name="bella"))
        self.add_command(
            label="Sasha", command=lambda: app._changeTheme(name="sasha"))
        self.add_command(
            label="Elena", command=lambda: app._changeTheme(name="elena"))
        self.add_command(
            label="Maggie", command=lambda: app._changeTheme(name="maggie"))
        self.add_command(
            label="John", command=lambda: app._changeTheme(name="john"))
        self.add_command(
            label="Helena", command=lambda: app._changeTheme(name="helena"))
        
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
        index_editor.IndexEditor(self.app.getRoot())

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
        template_editor.TemplateEditor(self.app.getRoot())

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
        template_editor.TemplateEditor(self.app.getRoot())
    
    def indexEditPop(self):
        """ Opens the index editor popup window. """
        index_editor.IndexEditor(self.app.getRoot())
