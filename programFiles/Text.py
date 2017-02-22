# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
#
# Description: Class for controlling input and output from the file.

class Text:
    def __init__(self, path):
        self._path = path
        self._string = self._read(path)
        
    def _read(self, path):
        f = open(path)
        string = ''
        for line in f:
            string += line
        f.close()
            
        return string
    
    def copyToFile(self, fileName):
        # Should have some protection from overwriting files
        f = open(fileName, 'w')        
        f.write(self._string)
        f.close()
    
    def path(self):
        return self._path
    
    def string(self):
        return self._string


if __name__ == "__main__":
    # Debug Testing
    fle = Text("../input/astaikina.txt")
    print(fle.string())
    fle.copyToFile("test.txt")
