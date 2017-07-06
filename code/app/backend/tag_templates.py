# Created by: John Hoskins
# Email: jbhoskins@email.wm.edu
# 
# Description: Reads the templates specified, and returns a dictionary of them


class ParseError(Exception):
    pass

class TemplateIndex(dict):
    def __init__(self):
        f = open("../../META/tagTemplates.txt")
        for line in f:
            splitLine = line.split(':')
            if len(splitLine) > 3:
                raise ParseError("Lines may not contain more than two \":\"")
            elif len(splitLine) < 3:
                raise ParseError("Tag definitions must be of the type <name> :\
                    <tag> : </tag>")

            self[splitLine[0].strip().lower()] = (splitLine[1].strip(),
                splitLine[2].strip())
        
        print(self)
        f.close()
