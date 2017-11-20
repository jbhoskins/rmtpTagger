# StyleSheet.py 

# Created as part of the William and Mary Russian Movie Theater Project, 
# this is the work of John Hoskins and Margaret Swift, under the
# direction of Sasha and Elena Prokhorov.
# https://rmtp.wm.edu

# Authored by Margaret Swift: meswift@email.wm.edu
# Last edit 4/22/17 by Margaret.


"""A style sheet for the main application.  Holds fonts (title, subtitle, 
text, buttons), background colors (main, secondary, tertiary) high-
lighting colors (single key, multi-key, current get_selected_entry, interviewee
text)

Use in Application might look like:
self.styles = StyleSheet(name = "bella")

or:
self.button.config(font=self.styles.f_button)


LAST EDIT:

Margaret, 4/22/17

Changed style of code to conform to the PEP8 styleguide. 
"""

import app.gui.view_controller as view

class StyleSheet(view.Styler):
    def __init__(self, name='bella', dim=(700, 700)):
        """Set default fonts and style (Bella)."""
        view.Styler.__init__(self)
        
        self.dimensions = dim
        
        # Default fonts.
        self.f_title = "Verdana", 24
        self.f_subtitle = "Verdana", 20      
        self.f_text = "Verdana", 18   
        self.f_button = "Verdana", 18 
 
        self.changeTheme("bella")

    def changeTheme(self, name):
        # Choose the theme based on the name.
        if name.lower() == "bella":
             self._Bella()
        elif name.lower() == "sasha":
              self._Sasha()
        elif name.lower() == "elena":
              self._Elena()        
        elif name.lower() == "maggie":
              self._Maggie()
        elif name.lower() == "john":
              self._John()
        elif name.lower() == "helena":
              self._Helena()            
        else:
            raise Exception("Invalid name of theme.")

        self.notify_viewers_redraw()

            
      #-------------------------------------    
      # Style options
      
    def _Bella(self):
        self.c_1 = "#e0e0eb"
        self.c_2 = "#ffffcc"  
        self.c_3 = "white"
        self.h_single = "#8585ad"
        self.h_multi = "#ffff80"
        self.h_current = "#ff66d9"      
        self.h_interviewer = "#666699"            
        
    def _Sasha(self):
        self.c_1 = "#c3c388"
        self.c_2 = "#608000" 
        self.c_3 = "#66ff99"
        self.h_single = "#99994d"
        self.h_multi = "#ff794d"
        self.h_current = "blue"
        self.h_interviewer = "#e5e5cc"

    def _Elena(self):
        self.c_1 = "#ffcce6"
        self.c_2 = "#ccffe4"  
        self.c_3 = "white"
        self.h_single = "#ff80b3"
        self.h_multi = "#80ffbb"
        self.h_current = "yellow"      
        self.h_interviewer = "#ff80b3"
         
    def _Maggie(self):
        self.c_1 = "#ffcccc"
        self.c_2 = "#ff8080"  
        self.c_3 = "white"
        self.h_single = "#ff8080"
        self.h_multi = "#99ff99"
        self.h_current = "yellow"      
        self.h_interviewer = "#ff8080"
        
    def _John(self):
        self.c_1 = "#fffaf0"
        self.c_2 = "#cccccc"  
        self.c_3 = "#cccccc"
        self.h_single = "#96ceb4"
        self.h_multi = "#f0e68c"
        self.h_current = "#7bb3ff"      
        self.h_interviewer = "#a3a3a3"
        
    def _Helena(self):
        self.c_1 = "#e0e0eb"
        self.c_2 = "#ffffcc"  
        self.c_3 = "white"
        self.h_single = "#8585ad"
        self.h_multi = "#ffff80"
        self.h_current = "yellow"      
        self.h_interviewer = "#666699"
