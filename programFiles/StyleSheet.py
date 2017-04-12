'''Style Sheet:

Use in Application might look like:

self.styles = StyleSheet(name = "bella")

Let's say you want a button to have the button font; just call 

self.whatever_button.config(font = self.styles.f_button)

'''
class StyleSheet:
      
      def __init__(self, name = 'bella', dim = (700, 700)):
            '''Default fonts, Bella is default style'''
            
            # Set dimension
            dim = self.dim
            
            # Default fonts
            self.f_title = "Verdana", 24
            self.f_subtitle = "Verdana", 20      
            self.f_text = "Verdana", 18   
            self.f_button = "Verdana", 18 
            
            # Default style
            self._Bella()
            
            # Here we can choose the style based on the name.
            if name.lower() == "bella":
                  self._Bella()
            elif name.lower() == "sasha":
                  self._Sasha()
            elif name.lower() == "elena":
                  self._Elena()        
            elif name.lower() == "robert":
                  self._Robert()
            elif name.lower() == "fred":
                  self._Fred()
            else:
                  print("Error, invalid name!")
            
            
      def _Bella(self):
            self.c_1 = "#e0e0eb"
            self.c_2 = "#ffffcc"  
            self.c_3 = "white"
            
            self.h_single = "#8585ad"
            self.h_multi = "#ffff80"
            self.h_current = "yellow"      
            
            self.h_interviewer = "#666699"
            
            
      def _Sasha(self):
            self.c_1 = "#D5CDFF"
            self.c_2 = "#AFC0AA" 
            self.c_3 = "blue"
            
            self.h_single = "red"
            self.h_multi = "white"
            self.h_current = "blue"    

            self.h_interviewer = "#666699"
