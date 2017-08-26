# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Reads the templates specified, and returns a dictionary of them


class ParseError(Exception):
    """ I wanted a more descriptive exception name, so I made this."""
    pass


class Tag:
    """Data container for an XML tag."""
    def __init__(self, front = "", back="", arguments = []):
        self._front = front # Front tag
        self._back = back # Back tag
        
        # Any arguments that need to be inserted into the front tag.
        if self._front.count(r"%s") != len(arguments):
            raise ParseError(r"%s count is not equal to number of arguments.")
        self._arguments = arguments

    def setFront(self, string):
        """ Set the value of the front tag. """
        self._front = string

    def setBack(self, string):
        """ Set the value of the back tag. """
        self._back = string

    def setArguments(self, arguments):
        """ Set the value of the arguments to be inserted into the front tag."""
        self._arguments = arguments

    def getFront(self):
        """ Get the value of the front tag. """
        return self._front

    def getBack(self):
        """ Get the value of the back tag. """
        return self._back

    def getArguments(self):
        """ Get the value of the list of arguments to be inserted into the
        front tag. """
        return self._arguments
    
    def getTuple(self):
        """Get a tuple of the front and back tag in the form (front, back,
        arguments)."""
        return (self._front, self._back, "   ".join(self._arguments))

    def __str__(self):
        return "%s\t%s" % (self.getFront(), self.getBack())

class TemplateIndex:
    """Data container to access the tagTemplates configuration file, and
    encapsulate all access to it. Stores information as tuples, in a list of 
    key:value pairs with strings as keys and Tag objects as values."""
    def __init__(self):
        """ Open the file and parse it for tag templates."""
        f = open("../META/tagTemplates.txt")
        
        self._templates = []
        
        for line in f:
            
            # Allow for comments & whitespace
            if line.isspace() or line == "" or line.strip()[0] == "#":
                continue

            splitLine = line.split('__+__')
            if len(splitLine) > 4:
                raise ParseError("Lines may not contain more than three \"__+__\"")
            elif len(splitLine) < 4:
                raise ParseError("Tag definitions must be of the type <name>\
                __+__ <tag> __+__ </tag> __+__ <arguments>")

            self._templates.append((splitLine[0].strip().lower(),
                    Tag(splitLine[1].strip(), splitLine[2].strip(),
                        splitLine[3].strip().split())))
        
        print([entry[0] for entry in self._templates])
        f.close()

    def getFileString(self):
        """Used for writing the data structure as a tag configuration file. Has
        not been tested or finished yet. """
        string = ""

        for entry in self._templates:
            string += entry[0] + "__+__ " + entry[1].getFront() + " __+__ " +\
            entry[1].getBack() + "\n"

        return string

    def getNames(self):
        """Return a list of the names of the templates."""
        return [entry[0] for entry in self._templates]

    def getValues(self):
        """Returns a list of the Tag objects in the data structure."""
        return [entry[1] for entry in self._templates]

    def getTemplates(self):
        return self._templates

    def addTemplate(self, name, frontTag, backTag, arguments):
        """Appends a new template to the index."""
        self._templates.append((name, Tag(frontTag, backTag, arguments)))

    def deleteTemplate(self, index):
        """Deletes the template at the given index."""
        self._templates.pop(index)

    def replaceTemplate(self, index, name, frontTag, backTag, arguments):
        """Replaces the template aat the given index. Used for editing tags."""
        self.deleteTemplate(index)
        self._templates.insert(index, (name, Tag(frontTag, backTag, arguments)))

    def lookup(self, name):
        """Looks up and returns the Tag object associated with the given name."""
        
        # this thing that I keep doing can probably replaced with a normal,
        # built in list method.
        
        i = 0
        while (i < len(self._templates) and name != self._templates[i][0]):
            i += 1

        if i == len(self._templates):
            raise Exception("Name is not a valid template.")

        return self._templates[i][1]
         
if __name__ == "__main__":
    ndx = TemplateIndex()

    print(ndx.getNames())
    print(ndx.getValues())
