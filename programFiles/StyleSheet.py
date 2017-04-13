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
            self.dimensions = dim
            
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
            elif name.lower() == "maggie":
                  self._Maggie()
            elif name.lower() == "john":
                  self._John()
            else:
                  print("Error, invalid name!")
            
            
      # Style options
      
      def _Bella(self):
            self.c_1 = "#e0e0eb"
            self.c_2 = "#ffffcc"  
            self.c_3 = "white"
            
            self.h_single = "#8585ad"
            self.h_multi = "#ffff80"
            self.h_current = "yellow"      
            
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
