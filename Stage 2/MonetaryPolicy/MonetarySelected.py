#New file: MonetarySelected
from tkinter import *

import sys




sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2")  #PolicyRatingDisplay
import PolicyRatingDisplay as PRD     #Policies Ratings Display


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")    #Load_Everything
import Load_Everything as LE    







class InterestRatesOr():
    
    def __init__(self, UserID):

        self.which_screen_ = Tk()
        self.which_screen_.configure(bg = "light grey")
        self.which_screen_.geometry("420x330+750+250")
        self.which_screen_.title("Monetary Policy - Please Select")
        self.which_screen_.resizable(False,False)

        self.UserID = UserID
  
 
        self.interestratebutton = Button(self.which_screen_, command = lambda: self.interestratesselected(), text = "Interest Rates", foreground = "black",
                                borderwidth = 2, relief = "solid", bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=10, y=10, width = 400, height = 150)



    def interestratesselected(self):
        choice = "Interest Rates"
        self.which_screen_.destroy()
        monetary_run = MonetaryInterestRates(choice, self.UserID, 100)
        
        





class MonetaryInterestRates(PRD.policies_everything):  #Inherit the policies_everything class so that it can use the LoadRatings method etc...

    def __init__(self, choice, UserID, maximumslidervalue):
        
        self.UserID = UserID
        self.choice = choice
        self.nameofpolicy = "Interest Rates"
        self.InterestRates = self.LoadInterestRates()
        self.maxslidervalue = maximumslidervalue 
    
       
        super().__init__(self.nameofpolicy, self.choice, self.UserID)  #Inherit the constructer from the class policies_ratings so that the window can be displayed on the correct tkinter window
                                                          #   which is named self.policy_screen
                                                          #Must be after most of the child classes constuctor has been definied as these values as passed into the parent class


        #self.monetary_showratings() #From the parent class, run the method that displays all of the ratings from groups in the economy
        if self.choice == "Interest Rates":
            #If choice is interest rates we display all that is needed to adjust the interest rate level
            self.display_all()
            

    def display_all(self):

        
        
        
        
        
        self.policy_showratings()
        self.policy_label()
        self.helpbutton()
        self.slider(self.InterestRates, self.maxslidervalue, 0.1, 10)
        self.backtochoice()
        #self.confirm_or_view()
        
         
#-----------------------These are the methods I have overidden from the parent class----------------------------------------------------------------------------------------
    def backcommand(self, UserID):

        InterestRatesOr(self.UserID)
        self.policy_screen.destroy()
        

    def load_help(self, help_text):


        help_text = """Interest Rates are the costs of borrowing and
the rewards for saving. Your currency value can be easily changed through
Interest Rates. The Interest Rates in the US are constantly 2.5%, so keep
this in mind when you make changes. If your Interest Rate exceeds that
in the US, it will often mean the value of your currency increases as more
people start to save with your currency. However, a stronger currency will
mean imports increase and exports decrease, worsening your Current Account,
one of your Government Objectives. Also take into account your economies
MPC values, found in 'Additional Statistics'. The higher this value is
the more imports will change by.""" #EXPLAIN MORE ABOUT THIS HERE!!
        
        super(MonetaryInterestRates, self).load_help(help_text) #This allows us to call the parent class method load_help which will create the window AND THEN will it be overidden
                                                 #Without this the window would have to be created in every individual tax, spending, supply side and monetary policy etc...
                                                 #With this command we are able to call the parent method load_help then add any extra stuff independent to income tax etc...
            
    def confirm_changes(self, slider):
        newvalue = slider.get()
        self.CheckConfirmChanges(newvalue, self.InterestRates)


    def view_expectedchanges(self, slider):


        
        
        newvalue = slider.get()
        changedamount = newvalue - self.InterestRates
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
            self.__init__(self.nameofpolicy, self.UserID, self.maxslidervalue)    #   as this would not work properly with the slider after.
                

        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#End of file: MonetarySelected
        

     

        
def mainmonetary():

    UserID = 1
    runmonetary = InterestRatesOr(UserID)
    

if __name__ == "__main__":
    mainmonetary()
