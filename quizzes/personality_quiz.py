# Learning GUI
# Maggie Swift
# 14 December 2016

#-----------------------------------------------------------------------
import tkinter
from tkinter import *
import codecs

#-----------------------------------------------------------------------
class Name:
      '''A class that gets the user's name.'''
      
      def __init__(self, root):
            # Initialize root and name.
            self.root = root
            self.name = ""
            
            # Create label and entry
            self.label = Label(root, text="Как вас зовут?")        
            self.label.pack()
            self.entry = Entry(root)
            self.entry.pack()
            
            # Create a button to get the user's name; link button to enter key
            self.get_button = Button(root, text = "Сохраните <Return>", command = self.get_name)
            self.get_button.pack()
            root.bind('<Return>', (lambda e, b=self.get_button: b.invoke()))
            
      def __str__(self):
            '''Defines how the test will be printed.'''
            return self.name
      
      def get_name(self):
            '''Sets name attribute to user's entry; exits application.'''
            self.name = self.entry.get()
            root.destroy()

#-----------------------------------------------------------------------
class Test:
      '''A class that starts a test based on user-defined questions and answers, saves user's 
      choices, and spits them out to be used later on.'''
      
      def __init__(self, root, question, choices):
            # Define the root, question, available choices, chosen answer (default first choice), 
            # and variable for radio button selection.
            self.root = root
            self.question = question
            self.choices = choices
            self.answer = self.choices[0]
            self.var = IntVar()
            
            # Show the title and the question label.
            root.title("Личностный Тест")
            self.label = Label(root, text=question)        
            self.label.pack()
    
            # For each answer choice, create a radio button and show the button.
            for i in range(len(self.choices)):
                  self.radio = Radiobutton(root, text=self.choices[i], variable=self.var, value=i, command=self.sel)
                  self.radio.pack()
  
            # Create a series of buttons to move to the next question, show the current selected 
            # answer, and to exit the test entirely.
            self.next_button = Button(root, text="Следующий вопрос <Return>", command=root.quit)
            self.show_button = Button(root, text="Показать ваш ответ <s>", command=self.fetch)
            self.exit_button = Button(root, text="Уйти <q>", command=root.destroy)
            self.nxt_button = Button(root, text="", command=self.sel_next)
            self.prev_button = Button(root, text="", command=self.sel_prev)
            
            # Show all these buttons on the screen.
            self.next_button.pack()
            self.show_button.pack()
            self.exit_button.pack()
            
            # Bind keystrokes to buttons. 
            root.bind('s', (lambda e, b=self.show_button: b.invoke()))
            root.bind('<Return>', (lambda e, b=self.next_button: b.invoke()))
            root.bind('<q>', (lambda e, b=self.exit_button: b.invoke()))
            root.bind('<Right>', (lambda e, b=self.nxt_button: b.invoke()))
            root.bind('<Down>', (lambda e, b=self.nxt_button: b.invoke()))
            root.bind('<Left>', (lambda e, b=self.prev_button: b.invoke()))
            root.bind('<Up>', (lambda e, b=self.prev_button: b.invoke()))        
        
      def __str__(self):
            '''Defines how the test will be printed.'''
            return self.answer
      
      def sel(self):
            '''Defines how an answer choice is selected.'''
            selection = self.var.get()
            self.answer = self.choices[selection]
            return selection  
      
      def sel_next(self):
            '''Selects the next radio button (for arrowkeys Right and Down).'''
            NEXT = (self.var.get() + 1) % len(self.choices)
            r = Radiobutton(root, text="", variable=self.var, value=NEXT, command=self.sel)
            r.invoke()   
          
      def sel_prev(self):
            '''Selects the previous radio button (for arrowkeys Left and Up).'''
            PREV = (self.var.get() - 1) % len(self.choices)
            r = Radiobutton(root, text="", variable=self.var, value=PREV, command=self.sel)
            r.invoke()  
          
      def fetch(self):
            '''Prints the current choice to the screen.'''
            print(self.choices[self.var.get()])
          
#-----------------------------------------------------------------------
class Personality_Type:
      '''A class for deciding a personality type based on the answers to the test.'''
      
      def __init__(self, root, my_name, choices, answer_list):
          # Define the root, choices, answers, and personality type.
            self.root = root
            self.choices = choices
            self.answers = answer_list
            self.my_type = ""
            self.my_name = str(my_name)
            
            # Show the title and the label.
            root.title("Ваша личность")
            label_text = "Спасибо за внимания, " + self.my_name + "."        
            self.label = Label(root, text=label_text)        
            self.label.pack()
            
            # Create a button to reveal the personality, show the button, and bind the enter key 
            # to that button.
            self.reveal_button = Button(root, text="Узнать личности <Return>", command=self.reveal)
            self.reveal_button.pack()
            root.bind('<Return>', (lambda e, b=self.reveal_button: b.invoke()))
          
      def __str__(self):
            '''Defines how the personality type will be printed.'''
            return(self.my_type)
  
      def reveal(self):
            '''A function to reveal one's true personality, based on answers to questions given 
            beforehand.'''
          
            # Create a list of personalities and initialize my_type to zero.
            labels = "Острая", "Сладкая", "Соленая", "Вкусная", "Горкая", "Кислая", "Безвкусная"
            my_type = 0
            
            # Find the sum of the user's answer indices.
            for i in range(1, len(self.answers)):
                  my_type += self.choices[i].index(self.answers[i])
        
            # Your personality is the corresponding index of the sum of your answers. Show that 
            # answer when the button is clicked.
            self.my_type = labels[my_type]
            label_text =  "Ваша личность--" + self.my_type
            new_label = Label(root, text = label_text)
            new_label.pack() 
            root.quit

#-----------------------------------------------------------------------
if __name__ == '__main__':    
    # Test questions and possible answers.
      test_answers = []
      count = 0
      with codecs.open('questions_Russian', 'r', 'utf-8') as file:
            for line in file:
                  line = line.strip().split(',')
                  if count == 0:
                        test_questions = line
                  else:
                        test_answers.append(line)
                  count += 1
      file.close()
      
      # Get user's name
      root = Tk()
      root.attributes("-topmost", True)
      my_name = Name(root)
      mainloop()    
    
      # Initialize answer_list (for storing answers) and run the mainloop. Destroy after each 
      # run and re-initialize with the next question-and-answer set.
      answer_list = []
      for i in range(len(test_questions)):
            root = Tk()
            root.attributes("-topmost", True)
            my_gui = Test(root, test_questions[i], test_answers[i])
            root.mainloop()
            root.attributes("-topmost", False)
            answer_list.append(str(my_gui))
            root.destroy()

      # After quitting the test, run the personality class to find your personality type!
      root = Tk()
      root.attributes("-topmost", True)
      my_type = Personality_Type(root, my_name, test_answers, answer_list)
      root.mainloop()
      root.attributes("-topmost", False)  
      print(my_type)