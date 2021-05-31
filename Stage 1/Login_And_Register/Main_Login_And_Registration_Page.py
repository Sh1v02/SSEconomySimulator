#File name: Main_Login_And_Registration_Page
from tkinter import * 
from tkinter import messagebox
from Login_Or_Register_Selected import *

#__________________________________________________________Creating the first window which gives the options of login, register or quit________________________#

class LoginOrRegister():
    
    def __init__(self):
        
        #Create the first page where the user can either register or login
        self.main_screen = Tk()
        self.main_screen.configure(bg = "aqua")
        self.main_screen.geometry("600x700+660+190") #+660+190 means display the window 660 to the right and 190 downwards
        self.main_screen.title("Login Or Register")
        self.main_screen.resizable(False,False)
        self.create_register_screen()
        


    #Display the buttons which can be selected
    def create_register_screen(self):
        
        #Create the login button which when clicked will open the login window
        select_login = Button(text = "Login", command = lambda:[login(),self.main_screen.destroy()], bg = "white", foreground = "black",
                                   font = ("Comic Sans", 12, "bold")).place(x = 200, y = 100, height = 100, width = 200)
                                   #lambda used to prevent the button from being pressed immediately without clicking it
                                
        #Create the login button which when clicked will open the registration window
        select_register = Button(text = "Register", command = lambda:[register(),self.main_screen.destroy()], bg = "white", foreground = "black",
                                      font = ("Comic Sans", 12, "bold")).place(x = 200, y = 250, height = 100, width = 200)

        quit_window = Button(text = "Quit", command = lambda: self.quit_program(), bg = "white", foreground = "black",
                           font = ("Comic Sans", 12, "bold")).place(x = 200, y = 400, height = 100, width = 200)

        
    def quit_program(self):
        
        choice = messagebox.askquestion(title = "But why :( ?", message = "Are you sure you want to quit?")
        if choice == "yes": #Quit the game and close the window
            quit()

#End of file: Main_Login_And_Registration_Page
        

#____________________________________________________________Call LoginOrRegister________________________________________________________#


def main():
    
    LoginOrRegister() #Calling the class which displays the window where the user will select login or register
    
    
#_________________________________________________________________________________________________________________________________________#


if __name__ == '__main__': #This is an in-built line which will prevent modules from being run instantly when they are imported.
                           #Without this function, when the program is run, an extra blank windwo will open.
    
    main()

    








