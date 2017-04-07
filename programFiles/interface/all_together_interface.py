from tkinter import *
from FramedText import *
import codecs
import re
import math

#--------------------------------------------------------------------
# MAIN WINDOW
#--------------------------------------------------------------------

class MainWindow(Tk):
    '''Our main window to hold both the text and the buttons.'''
    
    def __init__(self, parent):
        '''Initialize the parent window.'''
        Tk.__init__(self, parent)
        self.parent = parent
        self.widgets()
        
        
    def widgets(self):
        '''Organizes our widgets in a grid.'''
        self.left = LeftF(self)
        self.right = RightF(self)
        self.left.grid(row=0, column=0)
        self.right.grid(row=0, column=1)




#--------------------------------------------------------------------
# LEFT FRAME
#--------------------------------------------------------------------

class LeftF(Frame):
    '''Our left frame holds the text of the interview.'''
    
    def __init__(self, parent):
        '''Initialize the frame within the parent window.'''
        self.parent = parent
        self.color1 = "#FFC09B"
        self.color2 = "#D5CDFF"
        
        Frame.__init__(self, parent, bg = self.color1)
        self.leftWidgets()
        

    def leftWidgets(self):
        '''Fills the window with the interview text.'''
        self.LeftLabel = Label(self)
        self.LeftText = Text(self)
        
        self.LeftLabel.config(text = "Full Interview", bg=self.color1, font = ("Helvetica", 30))
        self.LeftText.config(wrap = WORD, highlightbackground=self.color1, height = 40, bg =self.color1,  font = ("Helvetica", 14))
        
        with codecs.open(text_file, 'r', 'utf-8') as f:
            content = f.readlines()   
            for i in range(len(content)):
                line = content[i].strip() + '\n'
                self.LeftText.insert(END, line)
        f.close()     
        self.LeftText.config(state=DISABLED)
        
        self.LeftLabel.grid(row=0, column=0, padx=5, pady=5)
        self.LeftText.grid(row=1, column=0, padx=5, pady=5)
        self.LeftText.bind("<ButtonRelease-1>", self.callback)
    

    def callback(self, event):
        '''A function to find the currently selected paragraph.'''
        position = self.LeftText.index(INSERT)
        position = float(math.floor(float(position)))
        
        # Un-highlight the text by rewriting the line the same as before.
        inx = self.parent.right.t_inx
        cur = self.LeftText.get(inx, inx + 1)
        self.rw_line(self.LeftText, cur, inx) 
        
        # Move to new paragraph
        self.parent.right.t_inx = position
        self.parent.right.c_inx = int(position - 1)
        self.parent.right.move_to_par(position)
        
    
    def rw_line(self, master, new_line, inx):
            '''Rewrites a line of text where you want it.'''
            self.LeftText.config(state=NORMAL)
            master.delete(inx, inx+1)
            master.insert(inx, new_line)
            self.LeftText.config(state=DISABLED)




#--------------------------------------------------------------------
# RIGHT FRAME
#--------------------------------------------------------------------

class RightF(Frame):
    '''The right frame holds our current paragraph and buttons to edit or move through the
    interview.'''
    
    def __init__(self, parent):
        '''Initializes important variables.'''
        
        # Create the frame and set up class variables.
        self.parent = parent
        self.left_frame = self.parent.left.LeftText
        self.color1 = "#FFC09B"
        self.color2 = "#D5CDFF"  
        Frame.__init__(self, parent, bg=self.color1)
        self.content = ""
        self.OldText = ""
        self.tag_list = []
        
        # Content starts at position 2, text starts at line 3.0.
        self.t_inx = 3.0
        self.c_inx = 2
        
        self.rightWidgets()
        
        
    def rightWidgets(self):
        '''Right widgets include the current paragraph and various buttons for moving through
        and editing the interview text.'''
        self.RightFrame = Frame(self)
        self.RightText = FramedText(self.RightFrame)
        self.RightLabel = Label(self)
        
        with codecs.open(text_file, 'r', 'utf-8') as f:
            self.content = f.readlines()
            line = self.content[self.c_inx].strip()
            self.OldText = line
            self.RightText.insert("1.0", line)
            self.highlight(self.left_frame, self.t_inx)
        f.close()        
        
        self.RightFrame.config(height=400, width=600, bg=self.color2)
        self.RightText.text.config(bg=self.color2, highlightbackground=self.color2, font=("Helvetica", 20))
        self.RightLabel.config(text="Edited Text", bg=self.color1, font=("Helvetica", 30))
        
        self.RightLabel.grid(row=4, column=0, padx=5, pady=5)
        self.RightFrame.grid(row=5, column=0, padx=5, pady=5)
        self.RightFrame.pack_propagate(0)
        self.RightText.pack()     
        
        
        # Create tag list.
        with codecs.open('tag_dictionary.txt', 'r', 'utf-8') as f:
            for line in f:
                self.tag_list.append(line.strip().split(', '))
        f.close()            


        # Now create the buttons
        self.b_prev = Button(self, text="previous", command=self.prev)
        self.b_nxt = Button(self, text="next", command=self.nxt)
        self.b_tag = Button(self, text="TAG", command=self.tag)
        self.b_commit = Button(self, text="COMMIT", command=self.commit)
        self.b_revert_orig = Button(self, text="Original", command=self.revert_orig)
        self.b_revert_cur = Button(self, text="Latest edit", command=self.revert_cur)
        self.b_save = Button(self, text="SAVE", command=self.save)

        button_list = [self.b_prev, self.b_nxt, self.b_tag, self.b_commit, self.b_revert_orig, self.b_revert_cur, self.b_save]
        for button in button_list:
            button.configure(highlightbackground=self.color1, font=("Helvetica", 20))

        self.b_prev.grid(row=6, column=0, padx=5, pady=5, sticky = W)
        self.b_nxt.grid(row=6, column=0, padx=5, pady=5, sticky = E)
        self.b_tag.grid(row=6, column=0, padx=5, pady=5)
        self.b_revert_orig.grid(row=7, column=0, padx=5, pady=5, sticky = W)
        self.b_revert_cur.grid(row=7, column=0, padx=5, pady=5, sticky = E)
        self.b_commit.grid(row=7, column=0, padx=5, pady=5)
        self.b_save.grid(row=8, column=0, padx=5, pady=5)
        
        
    ##-------------------------------------------
    ## Functions for buttons. 
    ##-------------------------------------------
    def commit(self):
        '''A function that commits a change in the interviewee's paragraph.'''
        
        # Get the new text from the bottom of the two right boxes; change the left
        # text-box paragraph to match.
        new_line = self.RightText.text.get(1.0, END)        
        self.parent.left.rw_line(self.left_frame, new_line, self.t_inx)
        self.move_on()
        self.move_to_par(self.t_inx)
        
        
    def revert_orig(self):
        '''Temporarily reverts the selected paragraph to the original text.'''
        og = self.OldText
        og = og.strip()      
        self.rw_line(self.RightText, og, 1.0)
        
        
    def revert_cur(self):
        '''Temporarily reverts the selected paragraph to the current text.'''
        self.move_to_par(self.t_inx)
        
    
    def nxt(self):
        '''Un-highlights the text and moves on to the next paragraph.'''
        if self.t_inx <= len(self.content) - 4:
            cur = self.left_frame.get(self.t_inx, self.t_inx + 1) 
            self.parent.left.rw_line(self.left_frame, cur, self.t_inx)
            self.move_on()
            self.move_to_par(self.t_inx)
        

    def prev(self):
        '''Un-highlights the text and moves back to the previous paragraph.'''
        if self.t_inx >= 4:
            cur = self.left_frame.get(self.t_inx, self.t_inx + 1)  
            self.parent.left.rw_line(self.left_frame, cur, self.t_inx)
            self.move_back()
            self.move_to_par(self.t_inx)
            
    
    def tag(self):
        '''Runs through the paragraph and looks for things to tag.'''
        text = self.left_frame.get(self.t_inx, self.t_inx + 1)
        for i in range(len(self.tag_list)):
            line = self.tag_list[i]
            split_text = re.findall(r"[\w']+|[.,!?;]", text.lower())
            if line[0] in split_text:
                tagged_word = line[1] + line[0] + line[2]     
                cap_word = line[1] + line[0].title() + line[2]                
                text = text.replace(line[0], tagged_word).replace(line[0].title(), cap_word)
                self.rw_line(self.RightText, text.strip('\n'), 1.0)
        
        
    def save(self):
        '''Saves the file's current state into a separate file. This rewrites previous saves
        but NOT the original text file.'''
        full_text = self.left_frame.get(1.0, END) 
        save_file = "edited" + text_file
        with codecs.open(save_file, 'w', 'utf-8') as f:
            f.write(full_text)
        f.close()
            
        
    ##-------------------------------------------
    ## Helper functions
    ##-------------------------------------------
    def move_to_par(self, inx):
        '''A function that moves the cursor & highlighter to a paragraph.'''
        t_inx = inx
        c_inx = int(inx - 1)
        
        self.left_frame.see(t_inx)
        self.highlight(self.left_frame, t_inx)
        
        # Change the text shown on the right widget to match. 
        self.OldText = self.content[c_inx]
        cur_bottom = self.left_frame.get(t_inx, t_inx + 1).strip()       
        self.rw_line(self.RightText, cur_bottom, 1.0)
        
    def highlight(self, master, inx):
        '''Highlights text.'''
        master.tag_add("here", inx, inx + 1)
        master.tag_config("here", background=self.color2)  
        
    def rw_line(self, master, new_line, inx):
        '''Rewrites a line of text where you want it.'''
        master.delete(inx, inx+1)
        master.insert(inx, new_line)     
    
    def move_on(self):
        '''Updates t_inx and c_inx forward one paragraph'''
        self.t_inx += 4
        self.c_inx += 4    
        
    def move_back(self):
        '''Updates t_inx and c_inx backward one paragraph'''
        self.t_inx -= 4
        self.c_inx -= 4       


#---------------------------------------------------------------------------
if __name__=="__main__":
    
    text_file = '../../input/astaikina.txt'
    root = MainWindow(None)
    root.attributes("-topmost", True)
    root.geometry('1600x1500+0+0')
    root.configure(bg = '#FFC09B')
    root.mainloop()
