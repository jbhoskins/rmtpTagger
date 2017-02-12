from tkinter import *

def getString():
    st = ''
    f = open('../../input/astaikina.txt')

    for line in f:
        st += line
    return st
    f.close()

def delete():
    text["state"] = NORMAL
    
    text.delete('1.18', '1.27')
    text.delete('1.5', '1.13')
    
    text["state"] = DISABLED

def tag():
    text["state"] = NORMAL

    text.insert('1.10', "</scores>")
    text.tag_add('found', '1.5', '1.10')
    text.insert('1.5', "<scores>")

    text["state"] = DISABLED

stuff = 'Four score and seven years ago'

root = Tk()

text = Text(root, height=300, width=200)
text.tag_configure('nice', font=('Arial', 20))
text.tag_configure('found', font=('Arial', 20, 'bold'))
text.insert(INSERT, stuff, 'nice')

text.pack()

text["state"] = DISABLED

# Buttons
b = Button(root, text="Tag", command=tag)
c = Button(root, text="Untag", command=delete)

b.pack()
c.pack()

# Radio Buttons
val = StringVar()
score = Radiobutton(root, text='score', variable = val, value='score', command=tag)
other_tag = Radiobutton(root, text='other_tag', variable = val, value = 'other_tag')
score.pack()
other_tag.pack()



root.geometry("700x2000")
root.mainloop()
