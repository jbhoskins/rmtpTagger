# Russian Tagging Program
# Created By Maggie Swift 
# 12 December 2016
# Word class created by John Hoskins

#======================================================
# Import Word class, re (to replace), and codecs (to read Russian)
from Word import Word
import re
import codecs

#======================================================
def tag_word(word, tags):
    '''A helper function to tag words.'''
    
    # Make the word a Word class. Cleanse it.
    word = Word(word)
    word.cleanse()
    
    # Open the tagging file. Match each tag with word in question. Once found, replace word
    # with tagged word.
    with codecs.open(tags, "r", "utf-8") as tags:   
        for tagline in tags:
            tagline = tagline.strip().split(', ')
            if word.clean().lower() == tagline[0]:
                replacement = tagline[1] + word.__str__() + tagline[2]
                return replacement
    
    # If the word's not in the tag list, close tagging file and return the word as is.
    tags.close()
    return word.__str__()

#======================================================
def tag_text(text, tags, writefile, interviewer, interviewee):
    '''A function to tag a text and output it into writefile.'''
    
    # Initialize paragraph counter and open an interlude text as the writing file.
    i = 0
    with codecs.open("interlude.txt", "w", "utf-8") as interlude: 
            
        # Write meta tags into the document.
        interlude.write("<document>\n")
        interlude.write("<meta>\n")
        interlude.write("RMTP (Russian Movie Theater Project)\n")
        interlude.write("College of WIlliam and Mary Interview with Ekaterina Lebedeva https://vimeo.com/180984724\n")
        interlude.write("Interview conducted in St. Petersburg, Russia in July, 2016 by Margaret Swift (interviewer) and Bailey Orr (camera and sound).\n")
        interlude.write("Transcribed and translated by Bailey Orr, Maggie Swift, Gabriella Carney, and Molly Charles in Fall 2016.")
        interlude.write('\n')
        interlude.write("<\\meta>\n")
        interlude.write("\n<text>\n<body>\n\n")    

        # Open the text file you want to tag & split lines.
        with codecs.open(text, "r", "utf-8") as text:
            for line in text:          
                line = line.split()
                
                # If i is odd, we're on an interviewer line. Don't tag, just wrap in speaker tags 
                # and write to interlude.
                if i % 4 == 0:
                    speaker_tag =  '<u xml:id="sp' + str(i // 2 + 1)+ '" who="' + interviewer +'">'
                    interlude.write(speaker_tag)
                    for word in line:
                        interlude.write(word + " ")      
                
                # If i is even, we're on an interviewee line. Wrap in speaker tags, tag words that
                # are in the tagging list, and write to file.
                elif i % 4 == 2:
                    speaker_tag =  '<u xml:id="sp' + str(i // 2 + 1)+ '" who="' + interviewee +'">'
                    interlude.write(speaker_tag)
                    for word in line:                      
                        word = tag_word(word, tags)
                        interlude.write(word + " ")
        
                # Close speaker tags, write newline character, and increase line counter after 
                # line is finished.
                if i % 2 == 0:
                    interlude.write("</u>")
                else:
                    interlude.write("\n\n")
                i += 1
                
        # Close body tags and files used.              
        interlude.write("\n\n</body>\n</text>\n</document>")
        text.close()
    interlude.close()  
    
    # Second part:  go through and match multi-word tags
    # This part doesn't work right yet so I'm toying with it.
    # It does remove the spaces before </u> which is nice.
    with codecs.open(writefile, "w", "utf-8") as writefile:
        with codecs.open("title_tag_list.txt", "r", "utf-8") as tags: 
            with codecs.open("interlude.txt", "r", "utf-8") as readfile: 
                for line in readfile:
                    tags.seek(0)
                    line = line.replace(' </u>', '</u>')
                    for line_2 in tags:
                        line_2 = line_2.split(', ')
                        to_replace = "r\b" + line_2[0] + "\b"
                        replacement = line_2[1] + line_2[0] + line_2[2]
                        line = re.sub(to_replace, replacement, line)
                    writefile.write(line)
                    
            # Close all files.
            readfile.close()
        tags.close()
    writefile.close()
        
        
#======================================================
# Main program.
#======================================================

if __name__ == '__main__':
    
    text = 'astaikina.txt'
    tags = 'master_keys_and_tags.txt'
    writefile = 'astaikina_output.txt'
    interviewer = 'interviewer'
    interviewee = 'interviewee'
    
    tag_text(text, tags, writefile, interviewer, interviewee)