# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Reads the templates specified, and returns a dictionary of them

import os

class ParseError(Exception):
    """ I wanted a more descriptive exception name, so I made this."""
    pass


class Tag:
    """Data container for an XML tag."""
    def __init__(self, front = "", back="", arguments = []):
        self.__front = front # Front tag
        self.__back = back # Back tag
        
        # Any arguments that need to be inserted into the front tag.
        if self.__front.count(r"%s") != len(arguments):
            raise ParseError(r"%s count is not equal to number of arguments.")
        self.__arguments = arguments

    def set_front(self, string):
        """ Set the value of the front tag. """
        self.__front = string

    def set_back(self, string):
        """ Set the value of the back tag. """
        self.__back = string

    def set_arguments(self, arguments):
        """ Set the value of the arguments to be inserted into the front tag."""
        self.__arguments = arguments

    def get_front(self):
        """ Get the value of the front tag. """
        return self.__front

    def get_back(self):
        """ Get the value of the back tag. """
        return self.__back

    def get_arguments(self):
        """ Get the value of the list of arguments to be inserted into the
        front tag. """
        return self.__arguments
    
    def get_tuple(self):
        """Get a tuple of the front and back tag in the form (front, back,
        arguments)."""
        return (self.__front, self.__back, "   ".join(self.__arguments))

    def __str__(self):
        return "%s\t%s" % (self.get_front(), self.get_back())


class TemplateIndex:
    """Data container to access the tagTemplates configuration file, and
    encapsulate all access to it. Stores information as tuples, in a list of 
    key:value pairs with strings as keys and Tag objects as values."""
    def __init__(self):
        """ Open the file and parse it for tag templates."""
        f = open(os.path.join("res", "tagTemplates.txt"))
        
        self.__templates = []
        
        for line in f:
            
            # Allow for comments & whitespace
            if line.isspace() or line == "" or line.strip()[0] == "#":
                continue

            split_line = line.split('__+__')
            if len(split_line) > 4:
                raise ParseError("Lines may not contain more than three \"__+__\"")
            elif len(split_line) < 4:
                raise ParseError("Tag definitions must be of the type <name>\
                __+__ <tag> __+__ </tag> __+__ <arguments>")

            self.__templates.append((split_line[0].strip().lower(),
                                     Tag(split_line[1].strip(), split_line[2].strip(),
                        split_line[3].strip().split())))
        
        print([entry[0] for entry in self.__templates])
        f.close()

    def get_file_string(self):
        """Used for writing the data structure as a tag configuration file. Has
        not been tested or finished yet. """
        string = ""

        for entry in self.__templates:
            string += entry[0] + "__+__ " + entry[1].get_front() + " __+__ " + \
                      entry[1].get_back() + "\n"

        return string

    def get_names(self):
        """Return a list of the names of the templates."""
        return [entry[0] for entry in self.__templates]

    def get_values(self):
        """Returns a list of the Tag objects in the data structure."""
        return [entry[1] for entry in self.__templates]

    def get_templates(self):
        return self.__templates

    def add_template(self, name, frontTag, backTag, arguments):
        """Appends a new template to the index."""
        self.__templates.append((name, Tag(frontTag, backTag, arguments)))

    def delete_template(self, index):
        """Deletes the template at the given index."""
        self.__templates.pop(index)

    def replace_template(self, index, name, frontTag, backTag, arguments):
        """Replaces the template aat the given index. Used for editing tags."""
        self.delete_template(index)
        self.__templates.insert(index, (name, Tag(frontTag, backTag, arguments)))

    def lookup(self, name):
        """Looks up and returns the Tag object associated with the given name."""
        
        # this thing that I keep doing can probably replaced with a normal,
        # built in list method.

        print(self.__templates)
        print("name is: ", name)
        for template in self.__templates:
            if name == template[0]:
                return template[1]

        raise Exception("Name is not a valid template.")
         
if __name__ == "__main__":
    ndx = TemplateIndex()

    print(ndx.get_names())
    print(ndx.get_values())
