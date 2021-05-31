#File name: OtherStatements
import mysql.connector
import json

from tkinter import *

import importlib #Import the import functions which include the .reload() function (used if the user loses)

economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
mycursor = economygamedb.cursor()



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 1\Login_And_Register")
import Main_Login_And_Registration_Page as MainPage

import Load_Everything as LE


class ExtraStatements():

    def __init__(self, UserID):
        self.UserID = UserID
        economygamedb.commit()  #Immediately do this so that if its a new game, the database will have its new/updated data in its columns. Without this command
                                #   what is returned when the game has been run for the first time will be an empty list/value.



    def getGDP(self):
        
        getGDP = "SELECT GDP FROM statistics WHERE StatsID = %s"
        usethisforGDP = self.UserID
        mycursor.execute(getGDP, (usethisforGDP,))
        GDP = mycursor.fetchall()[0][0]

        return GDP

    def IsNewGame(self):
        checkfornewgame = "SELECT NewGame FROM Users WHERE UserID = (%s)"%(self.UserID)#EXISTS(SELECT * FROM Users WHERE UserID = %s)"%(self.UserID)
        mycursor.execute(checkfornewgame)
        newgame = mycursor.fetchone()[0]
        print(newgame)

        if newgame:
            return True
        else:
            return False

    def addPoliciesConfirmed(self, policiesconfirmed):

        updatepoliciesconfirmed = "UPDATE PoliciesConfirmed SET Changes = (%s) WHERE ConfirmedID = (%s)"
        policiesconfirmed_string = json.dumps(policiesconfirmed)    #Convert to string to enter it into database.
        mycursor.execute(updatepoliciesconfirmed, (policiesconfirmed_string, self.UserID))  #Update the column which shows the changes with the User's ID.
        economygamedb.commit()

    def removePolicyFromConfirmed(self, keyToRemove):

        getpoliciesconfirmed = LE.Load(self.UserID)
        policiesconfirmed = getpoliciesconfirmed.LoadPoliciesConfirmed()
        print("from OS :",policiesconfirmed)
        del policiesconfirmed[keyToRemove]
        print("after removing the policy, policiesconfirmed is: ", policiesconfirmed)
        self.addPoliciesConfirmed(policiesconfirmed)    #Call the method which will now update the policies confirmed, which has now removed a policy and is updating itself in the
                                                        #   database.
        #removePolicy = "
        


    def getYear(self):

        mycursor.execute("SELECT Year FROM Statistics WHERE StatsID = %s"%(self.UserID),)
        Year = mycursor.fetchone()[0]

        
        #print(mycursor.execute('SELECT DATE_ADD("2017-06-15", INTERVAL +4 MONTH) result'))
        return Year


    def addQuarterToYear(self, Year):

        addquarter = "SELECT DATE_ADD((%s), INTERVAL +3 MONTH)"
        mycursor.execute(addquarter, (Year,))
        result = mycursor.fetchone()

        return result

    def getDifferenceInMonths(self):

        Year = self.getYear()
        print(Year)

        getdifference = "SELECT TIMESTAMPDIFF(MONTH,'2019-12-31',(%s))"
        mycursor.execute(getdifference, (Year,))
        difference = mycursor.fetchone()[0]
        print(difference)
        
        return difference

    def getDifficulty(self):

        difficulty = "SELECT Difficulty FROM Users WHERE UserID = (%s)"
        mycursor.execute(difficulty, (self.UserID,))
        difficulty = mycursor.fetchone()

        print(difficulty)



        return difficulty



    def Notices(self, message, endofgame, screen):

        
            
        notice_screen = Tk()
        notice_screen.geometry("800x500+560+290")
        notice_screen.title("Notices!")
        notice_screen.configure(bg = "red")
        notice_screen.resizable(False,False)

        notice_label = Label(notice_screen, text = message,
                            bg = "red", foreground = "white", font = ("Comic Sans", 14, "bold")).place(x = 10, y = 10, width = 780, height = 300)



        if endofgame:
            notice_button = Button(notice_screen, text = "Press to close", foreground = "white", font = ("Comic Sans", 10, "bold"),
                                   bg = "red",
                                   command = lambda : [notice_screen.destroy(), screen.destroy(), importlib.reload(MainPage), MainPage.main()]).place(x = 250, y = 350, width = 300, height = 100)
        else:
            Button(notice_screen, text = "Press to close", foreground = "white", font = ("Comic Sans", 10, "bold"),
                                   bg = "red", command = lambda : notice_screen.destroy()).place(x = 250, y = 350, width = 300, height = 100)
            

#End of file: OtherStatements
                
        

    









    

if __name__ == "__main__":
    now = ExtraStatements(1)
    print(now.Notices("Game Over", True, Tk()))
