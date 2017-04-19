# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Menubar class. Not sure if each menu should be an object, or a function.

import tkinter as tk

class Menubar(tk.Menu):
    def __init__(self, app):
        tk.Menu.__init__(self, app.root)
        FileMenu(self, app)
        ThemeMenu(self, app)
        ToolsMenu(self, app)
        
        app.root.config(menu=self)


class FileMenu(tk.Menu):
    def __init__(self, menubar, app):
        tk.Menu.__init__(self, menubar, tearoff=0)
        self.add_command(label="Open", command = app.openFile)
        self.add_command(label="Save")
        self.add_separator()
        self.add_command(label="Export", command = app.export)
        self.add_command(label="Export as TEI...")
        
        menubar.add_cascade(label="File", menu=self)

class ThemeMenu(tk.Menu):
    def __init__(self, menubar, app):
        tk.Menu.__init__(self, menubar, tearoff=0)
        self.add_command(label="Bella", command=lambda: app._changeTheme(name = "bella"))
        self.add_command(label="Sasha", command=lambda: app._changeTheme(name = "sasha"))
        self.add_command(label="Elena", command=lambda: app._changeTheme(name = "elena"))
        self.add_command(label="Maggie", command=lambda: app._changeTheme(name = "maggie"))
        self.add_command(label="John", command=lambda: app._changeTheme(name = "john"))
        self.add_command(label="Helena", command=lambda: app._changeTheme(name = "helena"))
        
        menubar.add_cascade(label="Theme", menu=self)

class ToolsMenu(tk.Menu):
    def __init__(self, menubar, app):
        tk.Menu.__init__(self, menubar, tearoff=0)
        self.add_command(label="Hide Greens")
        self.add_command(label="Hide Interviewer Text")
        self.add_command(label="Iterate")
        self.add_separator()
        self.add_command(label="Edit index...")
        
        menubar.add_cascade(label="Tools", menu=self)
        
