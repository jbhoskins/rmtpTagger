# Static functions that implement file input/output. Not yet implemented.

def loadText(self, path, makeTable = True):
    """Insert text from desired file into the widget, then highlight 
    keywords upon initialization. 
    """
    f = open(path, encoding="UTF-8")
    string = f.read()
    string = string.replace("ё", "е")
    f.close()

    self._keywordTable.fillTable(string)
    
    self.config(state=tk.NORMAL)
    self.delete("1.0", tk.END)
    self.insert("1.0", string, "bigger")
        
    self._tagPersons()
    self.tagAllElementsInTable()
    self.config(state=tk.DISABLED) 
