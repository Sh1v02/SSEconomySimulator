#New file: Education
from tkinter import *

import sys




sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2")  #PolicyRatingDisplay
import PolicyRatingDisplay as PRD     #Policies Ratings Display


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\FiscalPolicy")
import FiscalSelected as FiscalSelected


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
import OtherStatements as OS





class FiscalEducation(PRD.policies_everything, OS.ExtraStatements):  #Inherit the policies_everything class so that it can use the LoadRatings method etc...

    def __init__(self, choice, UserID, Education, maximumslidervalue):
        
        self.UserID = UserID
        self.choice = choice
        self.nameofpolicy = "Education"
        self.Education = Education
        self.original = Education
        self.maxslidervalue = maximumslidervalue

        print(self.Education)


        value = self.getGDP()   #Inherited method

        if value > 180:
            self.tick = 20
        else:
            self.tick = 10

            
        super().__init__(self.nameofpolicy, self.choice, self.UserID)  #Inherit the constructer from the class policies_ratings so that the window can be displayed on the correct tkinter window
                                                          #   which is named self.policy_screen
                                                          #Must be after most of the child classes constuctor has been definied as these values as passed into the parent class


        self.display_all()
            

    def display_all(self):
        
        self.policy_showratings()
        self.policy_label()
        self.helpbutton()
        self.slider(self.Education, self.maxslidervalue, 1, self.tick)   #Pass the IncomeT value for that user through to the abstract class which will the get the value it
                                                               # currently is and set the slider to start there. The resolution is also set to 1 for all fiscal spending policies.
                                    #DIFFERENT FOR MONETARY POLICY AS IT ONLY HAS INTEREST RATES SO CAN LOAD STATS THERE BUT HERE THE STATS MUST BE LOADED AS SOON AS FISCAL IS SELECTED
        self.backtochoice()
        

    
        
        
         
#-----------------------These are the methods I have overidden from the parent class----------------------------------------------------------------------------------------
    def backcommand(self, UserID):
        
        FiscalSelected.TaxOrSpending(self.UserID)
        self.policy_screen.destroy()



    def load_help(self, help_text):

        help_text = """Education is one of the biggest
reasons for a countries output. Higher spending on
Education can lead to much higher output, but this comes with
a time lag. Make sure you are aware of when your next election
is so that the effects will take place before then!""" #EXPLAIN MORE ABOUT IT HEREE

        
        super(FiscalEducation, self).load_help(help_text) #This allows us to call the parent class method load_help which will create the window AND THEN will it be overidden
                                                 #Without this the window would have to be created in every individual tax, spending, supply side and monetary policy etc...
                                                 #With this command we are able to call the parent method load_help then add any extra stuff independent to income tax etc...
        
        
        #DO SOME MORE HELP STUFF
        
            
    def confirm_changes(self, slider):
        newvalue = slider.get()
        self.CheckConfirmChanges(newvalue, self.original)

    def view_expectedchanges(self, slider):

      
        newvalue = slider.get()
        changedamount = newvalue - self.original

        if changedamount != 0:

            #The method being called is in the policies_everything class.
            #This method will call another method inside the polcies_everything class called change_figures.
            #change_figures will loop through a list of every figure name and the acutal values (in the weighteddictionary) and update them and append them to
            #   another dictionary called changedfigures.
            #Originally, the whole method was in every single policy, but moving it to the abstract class policies_everything and changing a few lines makes the code much more efficient.
            self.display_temp_figures(changedamount, self.nameofpolicy)

            self.policy_screen.update()
        else:
            self.policy_screen.destroy()                                                        #Displays the default values, cannot just re call the method to display ratings
            self.__init__(self.nameofpolicy, self.UserID, self.Education, self.maxslidervalue)    #   as this would not work properly with the slider after.

        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#End of file: Education
        

     

        
def mainmonetary():

    UserID = 1
    runmonetary = FiscalEducation("Education", UserID, 12, 200)
    

if __name__ == "__main__":
    mainmonetary()
