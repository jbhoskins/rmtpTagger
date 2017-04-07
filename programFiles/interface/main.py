# Title: Main.py
# Description: Main Interface proof on concept.

# Allows importing from another folder
import sys
sys.path.insert(0, '../')

from FramedText import *
import tkinter as tk

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.dim = self._getDim()
        self.FramesLR = self._placeFrames()

    def _getDim(self):
        print(self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        return (self.root.winfo_screenwidth(), self.root.winfo_screenheight())

    def _placeFrames(self):

        textFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 2)
        textFrame.pack_propagate(0) # Stops frames from shrinking to fit contents.
            
        txt = FramedText(textFrame)
        txt.loadText("../../input/astaikina.txt")
        txt.pack()
        textFrame.pack(expand = True, side = tk.LEFT)
        
        sidebarFrame = tk.Frame(self.root, height = self.dim[1], width = self.dim[0] / 4, bg='green')
        sidebarFrame.pack_propagate(0)
        
        self._putListBox(sidebarFrame)
        self._putInformation(sidebarFrame)
        
        sidebarFrame.pack(side = tk.LEFT)
        return (textFrame, sidebarFrame)

    def _putListBox(self, sidebar):        
        title = Label(sidebar, text="Index Results", font="Verdana 20", bg = "green")
        title.pack(fill = Y, pady = 20)
        lst = Listbox(sidebar)
        lst.pack(fill = X, padx = 15)

    def _putInformation(self, sidebar):
        spacer = LabelFrame(sidebar, height = 100, bg="green")
        spacer.pack()

        
        info = Label(sidebar, text="Tag Information", font="Verdana 20", bg = "green")
        info.pack(fill = Y, pady = 20)
        lst = Listbox(sidebar)
        lst.pack(fill = X, padx = 15)

    def launch(self):
        self.root.mainloop()


        
# make root, 
app = Application()
app.launch()

