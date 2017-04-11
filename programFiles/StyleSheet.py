'''Style Sheet:

Use in Application might look like:

self.styles = StyleSheet(name = "bella")

Let's say you want a button to have the button font; just call 

self.whatever_button.config(font = self.styles.f_button)

'''
class StyleSheet:
      
      def __init__(self, name = 'bella'):
            '''Default fonts, Bella is default style'''
            
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
            self.c_1 = "#D5CDFF"
            self.c_2 = "#AFC0AA"  
            self.c_3 = "white"
            
            self.h_good = "green"
            self.h_problem = "yellow"
            self.h_current = "red"      
            
      def _Sasha(self):
            self.c_1 = "red"
            self.c_2 = "white"  
            self.c_3 = "blue"
            
            self.h_good = "red"
            self.h_problem = "white"
            self.h_current = "blue"    
