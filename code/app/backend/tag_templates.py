# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Reads the templates specified, and returns a dictionary of them


class ParseError(Exception):
    pass


class Tag:
    def __init__(self, front = "", back=""):
        self._front = front
        self._back = back

    def setFront(self, string):
        self._front = string

    def setBack(self, string):
        self._back = string

    def getTuple(self):
        return (self._front, self._back)

    def getFront(self):
        return self._front

    def getBack(self):
        return self._back

    def __str__(self):
        return "%s\t%s" % (self.getFront(), self.getBack())

class TemplateIndex:
    def __init__(self):
        f = open("../META/tagTemplates.txt")
        
        self._templates = []
        
        for line in f:
            
            splitLine = line.split(':')
            if len(splitLine) > 3:
                raise ParseError("Lines may not contain more than two \":\"")
            elif len(splitLine) < 3:
                raise ParseError("Tag definitions must be of the type <name> :\
                    <tag> : </tag>")

            self._templates.append((splitLine[0].strip().lower(),
                    Tag(splitLine[1].strip(), splitLine[2].strip())))
        
        print(self)
        f.close()

    def getFileString(self):
        string = ""

        for entry in self._templates:
            string += entry[0] + ": " + entry[1].getFront() + " : " +\
            entry[1].getBack() + "\n"

        return string

    def getNames(self):
        return [entry[0] for entry in self._templates]

    def getValues(self):
        return [entry[1] for entry in self._templates]

    def getRaw(self):
        return self._rawLines

    def addTemplate(self, name, frontTag, backTag):
        self._templates.append((name, Tag(frontTag, backTag)))

    def deleteTemplate(self, index):
        self._templates.pop(index)

    def replaceTemplate(self, index, name, frontTag, backTag):
        self.deleteTemplate(index)
        self._templates.insert(index, (name, Tag(frontTag, backTag)))

    def lookup(self, name):
        i = 0
        while (i < len(self._templates) and name != self._templates[i][0]):
            i += 1

        if i == len(self._templates):
            raise Exception("Name is not a valid template.")

        return self._templates[i][1]
        
    

# The stuff here is a newer idea, is it better? 
class AbstractTemplate:
    def __init__(self):
        # String must have two %s 's 
        self._string = "<tag>"

    def get_string(self):
        return self._string


class defaultTemplate(AbstractTemplate):
    def __init__(self):
        self._string = ""

class pronounTemplate(AbstractTemplate):
    def __init__(self):
        self._string = ""



if __name__ == "__main__":
    ndx = TemplateIndex()

    print(ndx.getNames())
    print(ndx.getValues())
