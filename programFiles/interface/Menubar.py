# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Menubar class. Not sure if each menu should be an object, or a function.

import tkinter as tk
import codecs 

class Menubar(tk.Menu):
    def __init__(self, app):
        tk.Menu.__init__(self, app.root)
        
        FileMenu(self, app)
        ThemeMenu(self, app)
        ToolsMenu(self, app)
        
        app.root.config(menu=self)



class DropdownMenu(tk.Menu):
    def __init__(self, menubar, app):
        tk.Menu.__init__(self, menubar, tearoff = 0)
        self.app = app

class FileMenu(DropdownMenu):
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Open", command = self.openFile)
        self.add_command(label="Save")
        self.add_separator()
        self.add_command(label="Export", command = self.export)
        self.add_command(label="Export as TEI...")
        
        menubar.add_cascade(label="File", menu=self)
    
    def export(self):
        """ Confirms, and exports the changes to a file. """
        string = self.app.fText.get("1.0", tk.END)

        for entry in reversed(self.app.fText.keywordTable):
            sel = self.app.index.lookup(entry.string().lower())[entry.selectionIndex()]
            frontTag = "<rs type=\"%s\" key=\"%s\">" % (sel.type(), sel.xmlId())
            backTag = "</rs>"
            string = string[:entry.stop()] + backTag + string[entry.stop():]
            string = string[:entry.start()] + frontTag + string[entry.start():]
        
        outputFile = tk.filedialog.asksaveasfilename(defaultextension=".txt", initialdir="../../output/")
        
        if outputFile:
    
            with codecs.open(outputFile, 'w', 'utf-8') as outputFile:
                lines = string.splitlines()
                j = 1
                
                metadata = "<meta> metadata here </meta>\n\n"
                outputFile.write(metadata)
                outputFile.write("<body>\n\n")
                for i in range(len(lines)):
                    line = lines[i]
                    names = ["bailey", "astaikina"]
                    
                    name = names[ i%4 // 2]
                    
                    if i % 2 == 0:
                        frontTag = '<u xml:id="sp' + str(j) + '" who="' + name + '">'
                        backTag = '</u>\n\n'
                        line = frontTag + line + backTag
                        j += 1
                    
                    outputFile.write(line)
                        
                outputFile.write("</body>")    
                
            outputFile.close()
            print("Export successful! Wrote %s" % outputFile.name)

    def openFile(self):
        filePath = tk.filedialog.askopenfilename(initialdir="../../input/")
        self.app.fText.loadText(filePath)


class ThemeMenu(tk.Menu):
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Bella", command=lambda: app._changeTheme(name = "bella"))
        self.add_command(label="Sasha", command=lambda: app._changeTheme(name = "sasha"))
        self.add_command(label="Elena", command=lambda: app._changeTheme(name = "elena"))
        self.add_command(label="Maggie", command=lambda: app._changeTheme(name = "maggie"))
        self.add_command(label="John", command=lambda: app._changeTheme(name = "john"))
        self.add_command(label="Helena", command=lambda: app._changeTheme(name = "helena"))
        
        menubar.add_cascade(label="Theme", menu=self)

class ToolsMenu(tk.Menu):
    def __init__(self, menubar, app):
        DropdownMenu.__init__(self, menubar, app)
        self.add_command(label="Hide Greens")
        self.add_command(label="Hide Interviewer Text")
        self.add_command(label="Iterate")
        self.add_separator()
        self.add_command(label="Edit index...")
        
        menubar.add_cascade(label="Tools", menu=self)
        
