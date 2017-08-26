import tkinter as tk

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(True)
        self.centerOnScreen(parent)
        self.title("RMTP Tagger")
        self.configure(background="white")
        tk.Label(self, text="RMTP Contextual XML Tagger", font=("Helvetica",
            25), bg="white").pack(pady=100)
        tk.Label(self, text="Version 1.0", font=("Helvetica", 25),
            bg="white").pack()
        tk.Label(self, text="Created by: John Hoskins and Margaret Swift",
                font=("Helvetica", 15), bg="white").pack()
        self.update()

    def centerOnScreen(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        splash_screen_width = 500
        splash_screen_height = 500

        x = (screen_width / 2) - (splash_screen_width / 2)
        y = (screen_height / 2) - (splash_screen_height / 2)

        self.geometry("%dx%d+%d+%d" % (
            splash_screen_width, splash_screen_height, x, y))
