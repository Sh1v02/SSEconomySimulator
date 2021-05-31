#File name: Login_Or_Register_Selected
from tkinter import *
from tkinter import messagebox
import time


import sys
sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2")
from Main_Menu import *


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
import OtherStatements as OS    #Used here to check for new game


import mysql.connector


import importlib #Import the import functions which include the .reload() function (used in the back buttons)
                 
from Main_Login_And_Registration_Page import * #Import the file which originally runs the main login/registration page

import Main_Login_And_Registration_Page as MainPage #Used to work with the importlibrary commands, MainPage is an alternative way of refering to the file



#___________________________________________________________________________________________________________________________________________________
#______________________________________________________Create the login class which runs when the login button is selected__________________________
#___________________________________________________________________________________________________________________________________________________


class login():
    
    def __init__(self): #Intitialise my class. This is the method that will immediately run as soon as this class is called
        #Create the basic screen once login has been selected
        self.login_screen = Tk()
        self.login_screen.configure(bg= "aqua")
        self.login_screen.geometry("700x500+610+290")
        self.login_screen.title("Login Page")
        self.login_screen.resizable(False, False) #Cannot expand either the width or height of window
        self.login_label = Label(self.login_screen, text = "Login Page",foreground = "black",
                                 bg = "aqua", font = ("Comic Sans", 18, "bold")).place(x=250,y=50,height = 50, width = 200)

        #Call create_login_screen to place the buttons etc on the window
        self.create_login_screen()

        
    def create_login_screen(self): 
        #Create the labels which display where to enter the username or password
        username_label = Label(self.login_screen, text = "Enter username", foreground = "black",
                               bg = "aqua", font = ("Comic Sans", 9, "bold")).place(x = 140, y = 125, height = 20, width = 115)
        password_label = Label(self.login_screen, text = "Enter password", foreground = "black",
                               bg = "aqua", font = ("Comic Sans", 9,"bold")).place(x = 140, y = 165, height = 20, width = 115)

        #Create the widget where the user can enter their username and password to login
        username_entry = Entry(self.login_screen)
        username_entry.place(x = 260, y = 125, height = 20, width = 180)
        
        password_entry = Entry(self.login_screen)
        password_entry.place(x = 260, y = 165, height = 20, width = 180)

        #Create the button that the user will click to submit their username and password
        details_check = Button(self.login_screen, text = "Submit Details",command = lambda: self.CheckLoginDetails(username_entry,password_entry),
                                bg = "white", foreground = "black", font = ("Comic Sans", 12, "bold")).place(x = 275, y = 225, height = 30,width = 150)

        #Create back button
        login_back_button = Button(self.login_screen, text = "Back",command = lambda: [importlib.reload(MainPage),MainPage.main(),self.login_screen.destroy()],
                                  bg = "white", font = ("Comic Sans", 18, "bold")).place(x=550,y=400,height = 100, width = 150)
                                #The reload function is extremely important as it re-imports everything that the other file imports.
                                #Without this, the back button will take the user back to the old menu, but they cannot select another option as
                                #   those files have not been re-imported in this case.



    def CheckLoginDetails(self,username_entry,password_entry):

        #Take the user's entries for username and password
        username = username_entry.get()
        password = password_entry.get()

        #Hash the details
        PHash1 = register.Hash1(self, username, password)
        PHash2 = register.Hash2(self, username, password)
        
        
        #Connect to the database
        gamedb = mysql.connector.connect(host="localhost",user="root",passwd="notThePassword_321",database = "economygame") #Connect to MySQL
        mycursor = gamedb.cursor()

        #Check if their username and hashed values are in the database and if they match
        tocheck =("SELECT * FROM Users WHERE username = %s AND PHash1 = %s AND PHash2 = %s")
        valuestocheck = (username, PHash1, PHash2)
        mycursor.execute(tocheck, valuestocheck)
        
        result = mycursor.fetchall() #Gets all the data from the latest executed statement

        if result:
            
            #If they match start the game

            #Get that users UserID as this is what will be used as the foreign key to link tables so is needed to store and update scores later on
            getUserID = "SELECT UserID FROM Users WHERE username = %s AND PHash1 = %s AND PHash2 = %s" #Cannot just be username as more than one username may have this
            usethesevaluestogetUserID = (username, PHash1, PHash2)
            
            mycursor.execute(getUserID, usethesevaluestogetUserID)
            UserID = mycursor.fetchall()
            
            UserID = (UserID[0])[0] #This is done as the data is stored in a tuple in a tuple (essentially a list of lists) so I need to take the value only.
                                    #[0] Will take the first value in that list and as it is a list in a list this needs to be done twice to get the value alone.
                                    #There will only be one value in this list as well as I am only selecting UserID and nothing else.

            self.login_screen.after(500, self.login_screen.destroy)
            newgamecheck = OS.ExtraStatements(UserID)
            newgame = newgamecheck.IsNewGame()
            if not newgame:
                Stage2 = NewOrContinue(UserID, False)
                Stage2.check()
            else:
                selectdifficulty = CorrectDetails(UserID)
                selectdifficulty.SelectDifficulty()
  
        else:
            #If the details are not in the database then display an apporpriate message
            mycursor.execute("SELECT * FROM Users WHERE username = %s",(username,))
            checkusername = mycursor.fetchall()

            
            
            error("Incorrect Details")
                
        gamedb.commit()

        #Close the connection to the database
        mycursor.close()
        gamedb.close()


#___________________________________________________________________________________________________________________________________________________________________
#______________________________________________________Create the register class which runs when the register button is selected___________________________________#
#___________________________________________________________________________________________________________________________________________________________________

class register():
    def __init__(self):
        self.register_screen = Tk()
        self.register_screen.configure(bg = "aqua")
        self.register_screen.geometry("700x500+610+290")
        self.register_screen.title("Registration Page")
        self.register_screen.resizable(False,False) #Cannot expand either the width or height of the window
        self.register_label = Label(self.register_screen, text = "Registration Page",foreground = "black", bg = "aqua",
                                    font = ("Comic Sans", 18, "bold")).place(x=140,y=50,height = 50, width = 420)
        
        
        self.create_register_screen()


        
    def create_register_screen(self):
        username_label = Label(self.register_screen, text = "Enter username", foreground = "black",
                               bg = "aqua", font = ("Comic Sans", 9, "bold")).place(x = 140, y = 125, height = 20, width = 115)
        password_label = Label(self.register_screen, text = "Enter password", foreground = "black",
                               bg = "aqua", font = ("Comic Sans", 9,"bold")).place(x = 140, y = 165, height = 20, width = 115)
        reenterpassword_label = Label(self.register_screen, text = "Re-Enter password", foreground = "black",
                                      bg = "aqua", font = ("Comic Sans", 9,"bold")).place(x = 112, y = 205, height = 20, width = 150)

        #Create the widget where the user can enter their username and password to login
        username_entry = Entry(self.register_screen)
        username_entry.place(x = 260, y = 125, height = 20, width = 180) #Must be placed after declaration in order to take in input
        
        password_entry = Entry(self.register_screen)
        password_entry.place(x = 260, y = 165, height = 20, width = 180) #Must be placed after declaration in order to take in input
        
        reenterpassword_entry = Entry(self.register_screen)
        reenterpassword_entry.place(x = 260, y = 205, height = 20, width = 180) #Must be placed after declaration in order to take in input

        #Create the button that the user will click to submit their username and password
        details_submit = Button(self.register_screen, text = "Submit Details",command = lambda: self.validpassword(username_entry,password_entry,reenterpassword_entry),
                                bg = "white", foreground = "black", font = ("Comic Sans", 12, "bold")).place(x = 275, y = 265, height = 30,width = 150)
        
        register_back_button = Button(self.register_screen, text = "Back",command = lambda: [importlib.reload(MainPage),MainPage.main(),self.register_screen.destroy()],
                                  bg = "white", font = ("Comic Sans", 18, "bold")).place(x=550,y=400,height = 100, width = 150)


        

        
    
    def validpassword(self, username_entry, password_entry, reenterpassword_entry): #Make sure password matches the valid requirements
        
        username = username_entry.get()
        password = password_entry.get()
        reentered = reenterpassword_entry.get()
        
        digit = False
        digitlist = ["0","1","2","3","4","5","6","7","8","9"]
        uppercase = False
        matching = False
        
        if password == reentered:
            matching = True
        if not matching:
            messagebox.showinfo(title = "Oops", message = "Passwords must match")
        if username == "":
            messagebox.showinfo(title = "Oops", message = "Please enter a username")
        for character in password:
            if character in digitlist:
                digit = True
            if character.isupper():
                uppercase = True

                
        if len(password) < 8 or digit == False or uppercase == False or matching == False:
            messagebox.showinfo(title = "Oops", message = """Password must:
            - Be at least 8 characters
            - Contain one or more digits
            - Contain one or more upper case characters""")
            
        else:
            valueoffirsthash = self.Hash1(username, password)
            valueofsecondhash = self.Hash2(username, password)
            self.AddDetails(username, valueoffirsthash, valueofsecondhash)
                                                        
            
        
    def Hash1(self, username, password):

        #reset the values when the button is pressed again
        tohash = username + password

        value = 0

        #calculate the first hash value using the first algorithm

        for character in tohash:
            ascii_value = ord(character)
            current_value = (((5+ascii_value) * 2) + 5)
            value += current_value

        final_value = value % 100
        return final_value

    def Hash2(self, username, password):
        
        #reset the values when the button is pressed again
        tohash = username + password

        value = 0
        
        #If the first hash matches, I used bucketing to eliminate the idea of an incorrect password being matched with another username with the same hash
        #The second hash makes it so that the order of the character matters and affects the final hash value, so unless the passwords are identical (not possible) chances of
        #This situation are extremely unlikely


        extravalue = [] #Create an empty list extravalue
        for x in range(8):
            print(x)
            extravalue.append(len(tohash) - (x)) #Add the length minus x to the list extravalue
            print(extravalue)
                                #For every character in toHash, perform this calculation on it.
        for character in tohash:    
            ascii_value = ord(character)
            current_value = (((((ascii_value+12)*4)-2)*4)-2)
            value += current_value

            indexofcharacter = tohash.index(character)  #Get the index of the character in the password
            if indexofcharacter in extravalue:   #If the index is in the list extravalue
                value += ((ascii_value*indexofcharacter)-indexofcharacter)  #Makes it very unlikely for another password to match this hash value
                
                


        final_value2 = value % 100
        return final_value2


    def AddDetails(self,username, valueoffirsthash, valueofsecondhash):
        
        
        print(valueoffirsthash, valueofsecondhash)

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="notThePassword_321",database = "economygame") #Connect to MySQL
        mycursor = economygamedb.cursor()

        #Check if a row has the same two hash values
        check = "SELECT * FROM Users WHERE EXISTS (SELECT * FROM Users WHERE (PHash1, PHash2) = (%s, %s))"  #Check if another user's details generated the same hash values, which is
                                                                                                            #   unlikely but not impossible.
        checkvalues = (valueoffirsthash, valueofsecondhash)
        mycursor.execute(check, checkvalues)
        suitablehashes = mycursor.fetchall()
        
        if suitablehashes:
            error("""A similar username and/or password has
already been chosen, please choose another
username and/or password""")
            
            
        else:

            adddetails = ("INSERT INTO Users (Username, NewGame, PHash1, PHash2) values (%s, %s, %s, %s)")
            toadd = (username, 1, valueoffirsthash, valueofsecondhash)

            mycursor.execute(adddetails, toadd)



            #The user should be sent back to the login screen, indicating they have registered
            self.register_screen.destroy()
            importlib.reload(MainPage)
            MainPage.main()
            

        economygamedb.commit()

#_____________________________________________________________________________________________________________________________________________________________________________________#
        

class error():
    def __init__(self, typeoferror):
        self.error_screen = Tk()
        self.error_screen.geometry("400x400+760+340")
        self.error_screen.title("Oops!")
        self.error_screen.configure(bg = "red")
        self.error_screen.resizable(False,False)

        self.error_label = Label(self.error_screen, text = typeoferror,bg = "red", foreground = "white", font = ("Comic Sans", 10, "bold")).place(x = 0, y = 0, width = 400, height = 100)

        self.display_error()


    def display_error(self):
        
        error_button = Button(self.error_screen, text = "Press to re-try", foreground = "white", font = ("Comic Sans", 10, "bold"),
                                   bg = "red", command = lambda : self.error_screen.destroy()).place(x = 50, y = 200, width = 300, height = 100)

        messagebox.showinfo(title = "Oops", message = """Password must:
        Be at least 8 characters
        Must contain one or more digits
        Must contain one or more upper case characters""")
        
##########################Probably get rid of the class CorrectDetails################################################
class CorrectDetails():
    def __init__(self, UserID):
        self.UserID = UserID
        self.difficulty_screen = Tk()
        self.difficulty_screen.geometry("400x400+760+340")
        self.difficulty_screen.title("Difficulty Selection")
        self.difficulty_screen.configure(bg = "aqua")


    def SelectDifficulty(self):
        

        easy_button = Button(self.difficulty_screen, text = "Easy", bg = "light grey", command = lambda : self.difficulty_selected("Easy"),
                             font = ("Comic Sans", 10, "bold")).place(x = 40,y = 40, width = 320, height = 150)
        hard_button = Button(self.difficulty_screen, text = "Hard", bg = "light grey", command = lambda : self.difficulty_selected("Hard"),
                             font = ("Comic Sans", 10, "bold")).place(x = 40,y = 210, width = 320, height = 150)

    def difficulty_selected(self, difficulty):
        print(difficulty)
        print(self.UserID, " self.UserID")
        
        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="notThePassword_321",database = "economygame") #Connect to MySQL
        mycursor = economygamedb.cursor()

        #Check if a row has the same two hash values
        adddifficulty = "UPDATE Users SET Difficulty = (%s) WHERE UserID = (%s)"
        difficultytoadd = (difficulty, self.UserID)
        mycursor.execute(adddifficulty, difficultytoadd)
        economygamedb.commit()

        self.difficulty_screen.destroy()

        #After a difficulty has been selected, run the main menu.
        Stage2 = NewOrContinue(self.UserID, True)
        Stage2.check()

#End of file: Login_Or_Register_Selected
        

if __name__ == "__main__":
    runit = register()
    print(runit.Hash2('Test', 'Test1234'))
    #runit.display_welcome(1)
    
    #runnow.SelectDifficulty()

        
            
        
            
        
          
       
        
        
        


    
    

