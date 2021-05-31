#New file: IncomeTax
from tkinter import *

import sys

import random

import math

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2")  #PolicyRatingDisplay
import PolicyRatingDisplay as PRD     #Policies Ratings Display



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\FiscalPolicy")
import FiscalSelected as FiscalSelected



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 4\Graph")
import Graph_Traversals as GT




class FiscalIncomeTax(PRD.policies_everything):  #Inherit the policies_everything class so that it can use the LoadRatings method etc...

    def __init__(self, choice, UserID, IncomeTax, maximumslidervalue):
        
        self.UserID = UserID
        self.choice = choice
        self.nameofpolicy = "Income Tax"
        self.IncomeT = IncomeTax
        self.maxslidervalue = maximumslidervalue
    
       
        super().__init__(self.nameofpolicy, self.choice, self.UserID)  #Inherit the constructer from the class policies_ratings so that the window can be displayed on the correct tkinter window
                                                          #   which is named self.policy_screen
                                                          #Must be after most of the child classes constuctor has been definied as these values as passed into the parent class


        self.display_all()
            

    def display_all(self):
        
        self.policy_showratings()
        self.policy_label()
        self.helpbutton()
        self.slider(self.IncomeT, self.maxslidervalue, 0.1, 10)   #Pass the IncomeT value for that user through to the abstract class which will the get the value it currently is and set the slider to start there
                                         #Also pass 100 there to represent the maximum the slider can go to (percentage)
                                    #DIFFERENT FOR MONETARY POLICY AS IT ONLY HAS INTEREST RATES SO CAN LOAD STATS THERE BUT HERE THE STATS MUST BE LOADED AS SOON AS FISCAL IS SELECTED
        self.backtochoice()
        

    
        
        
         
#-----------------------These are the methods I have overidden from the parent class----------------------------------------------------------------------------------------
    def backcommand(self, UserID):
        
        FiscalSelected.TaxOrSpending(self.UserID)
        self.policy_screen.destroy()
        

    def load_help(self, help_text):

        help_text = """Progressive Tax:    Income Tax is one of the most well-known taxes.
You will often have to refer to it when talking about Fiscal Policy. Increasing
Income Tax will mean that most of the economy is unhappy and there
will be several knock on effects. However, it generates the most
amount of tax revenue for the UK Government, so take that into
account when evaluating your decisions.
""" #EXPLAIN MORE ABOUT IT HEREE

        
        super(FiscalIncomeTax, self).load_help(help_text) #This allows us to call the parent class method load_help which will create the window AND THEN will it be overidden
                                                 #Without this the window would have to be created in every individual tax, spending, supply side and monetary policy etc...
                                                 #With this command we are able to call the parent method load_help then add any extra stuff independent to income tax etc...
        
        
        #DO SOME MORE HELP STUFF
        
            
    def confirm_changes(self, slider):
        
        newvalue = slider.get()
        self.CheckConfirmChanges(newvalue, self.IncomeT)

        #economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        #mycursor = economygamedb.cursor()

        

    def view_expectedchanges(self, slider):
        
        
        
        newvalue = slider.get()
        changedamount = newvalue - self.IncomeT
        #print(changedamount)
        if changedamount != 0:
            
            #change = GT.MakeChanges(self.UserID, startpoint)
            #weighteddictionary = change.RunTaxGraph(startpoint Start, changedamount)
            #print(weighteddictionary)
            #changedfigures = self.change_figures(weighteddictionary)
        
            #The method being called is in the policies_everything class.
            #This method will call another method inside the polcies_everything class called change_figures.
            #change_figures will loop through a list of every figure name and the acutal values (in the weighteddictionary) and update them and append them to
            #   another dictionary called changedfigures.
            #Originally, the whole method was in every single policy, but moving it to the abstract class policies_everything and changing a few lines makes the code much more efficient.
            self.display_temp_figures(changedamount, self.nameofpolicy)

            self.policy_screen.update()
        else:
            self.policy_screen.destroy()                                                        #Displays the default values, cannot just re call the method to display ratings
            self.__init__(self.nameofpolicy, self.UserID, self.IncomeT, self.maxslidervalue)    #   as this would not work properly with the slider after.
            
#End of file: IncomeTax
                
        #weighttest = {'HighIncome' : 2}
        #for figure in listtest:
        #    print(figure)
        #    for key in weighttest:
        #        if key == figure:
        #            print(key)
        #            print(weighttest[key])

                
        #print(self.HIR, " is timesing by ", weighteddictionary['HighIncome'])
        #self.Imports = self.Imports * weighteddictionary['Imports']

        #print((weighteddictionary['Consumption']-1)/((weighteddictionary['DisposableIncome']*self.DisposableIncome)-(self.DisposableIncome)))/100
        #print(self.UnemploymentRate - weighteddictionary['UnemploymentRate'])
        #if (self.UnemploymentRate -weighteddictionary['UnemploymentRate'] <= 0):
         #   print(random.uniform(0.1, 0.35))
        #print(self.CurrentAccount - weighteddictionary['CurrentAccount'])
        #print("GDP is ", self.GDP*weighteddictionary['GDP'])
        #print(weighteddictionary['MPC']*self.MPC)

    
        
        
        
            
            
            
        
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        

     

        
def mainmonetary():

    UserID = 1
    runmonetary = FiscalIncomeTax("Income Tax", UserID, 12, 100)
    

if __name__ == "__main__":
    mainmonetary()
