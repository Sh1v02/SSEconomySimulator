#New file: PolicyRatingDisplay
from tkinter import *

import json
import sys
import random

import mysql.connector


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
import Load_Everything as LE
import OtherStatements as OS



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 4\Graph")
import Graph_Traversals as GT

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 4\Queue")
import PriorityQueue as PQ 



#This is an abstract base class
#This class is a superclass for many subclasses
#This class was created so that all policies can inherit it and its constructor so that this window can be used for all policies which cuts down large amounts of code and makes it
#   more robust

#The class polcies_ratings is the child class of Load, but is also the parent class of many other classes such as income tax, interest rates etc...

class policies_everything(LE.Load):
    
    def __init__(self, nameofpolicy, actualpolicy, UserID):
        self.policy_screen = Tk()
        self.policy_screen.configure(bg = "light grey")
        self.policy_screen.configure
        self.policy_screen.geometry("1000x800+460+140") #1000x800
        self.policy_screen.title(nameofpolicy)
        self.policy_screen.resizable(False,False)
        
        
        self.UserID = UserID
        self.actualpolicy = actualpolicy
        self.nameofpolicy = nameofpolicy

        
        self.startx, self.startwidth = 100, 800     #Values used for both the white ratings box and the slider


        #self.IncomeT, self.ExciseD, self.NationalI, self.CorpT, self.VAT, self.CarbonT = self.LoadFiscalTaxes()
        self.ratings, self.HIR, self.PR, self.MIR, self.UR, self.LIR, self.BR, self.OR = self.LoadRatings()
        #self.NationalD, self.CA, self.UnemploymentRate, self.Inflation, self.GDP, self.Year = self.LoadStatistics()
        #self.BudgetBalance, self.CurrencyVal, self.TaxRev, self.GovSpending, self.DisposableI, self.MPC, self.M, self.X = self.LoadExtraStatistics()
                                                                                                                                                    #M is imports and X is exports
                                                                                                                                                    #   (economics terminology)
        #self.PubInv, self.WelfareB, self.VocationalT, self.CouncilH = self.LoadSSPolicies()
        #self.SocialProt, self.Health, self.Education, self.Defence = self.LoadFiscalSpending()
        
        #self.listoffigures = [self.HIR, self.PR, self.MIR, self.UR, self.LIR, self.BR, self.OR] #Not including ratings dictionary in ratings here


        
        #Set the variables with names identical to those in the graphs to their values in the database so that the for loop when changing values can be more efficient.
        #Get the different policies that can be changed.                                                                                                                                                    
        self.IncomeTax, self.ExciseDuty, self.NationalInsurance, self.CorporationTax, self.ValueAddedTax, self.CarbonTax = self.LoadFiscalTaxes()
        self.SocialProtection, self.Health, self.Education, self.Defence = self.LoadFiscalSpending()
        self.InterestRates = self.LoadInterestRates()
        self.PublicInvestment, self.WelfareBenefits, self.VocationalTraining, self.CouncilHousing = self.LoadSSPolicies()

        #Get the different economic factors that can be affected.
        self.HighIncome,self.Pensioners,self.MiddleIncome,self.Unemployed,self.LowIncome,self.Businesses,self.Overall = self.HIR, self.PR, self.MIR, self.UR, self.LIR, self.BR, self.OR    
        self.NationalDebt,self.CurrentAccount,self.UnemploymentRate,self.Inflation,self.GDP,self.Year = self.LoadStatistics()
        self.BudgetBalance, self.CurrencyValue, self.TaxRevenue, self.GovernmentSpending, self.DisposableIncome, self.MPC, self.Imports, self.Exports = self.LoadExtraStatistics()
        
        
        

        #Create a list which has the name of each variable defined above so that the for loop can use the variable name and its value (using the eval() function).
        self.namesoffigures = [
            'HighIncome', 'Pensioners', 'MiddleIncome', 'Unemployed', 'LowIncome', 'Businesses',
            'NationalDebt', 'CurrentAccount', 'UnemploymentRate', 'Inflation', 'GDP', 'Year',
            'BudgetBalance', 'CurrencyValue', 'TaxRevenue', 'GovernmentSpending', 'DisposableIncome', 'MPC', 'Imports', 'Exports',
                            ]

        #Have a list of just the rating names
        self.namesofratings = ['HighIncome', 'Pensioners', 'MiddleIncome', 'Unemployed', 'LowIncome', 'Businesses', 'Overall']
            
            
                          
        #Create a list of names of each type of spending.
        self.namesofspending = ['SocialProtection', 'Health', 'Education', 'Defence',
                                'PublicInvestment', 'WelfareBenefits', 'VocationalTraining', 'CouncilHousing'
                            ]

        #Create a list that has names of each types of taxation, including Interest Rates.
        self.namesoftaxes = ['IncomeTax', 'ExciseDuty', 'NationalInsurance', 'CorporationTax', 'ValueAddedTax', 'CarbonTax', 'InterestRates'
                        ]
                                
                                 
        
        print("before change ratings are ", self.ratings)

        

    def policy_showratings(self):

        whiteboxforratings = Label(self.policy_screen, borderwidth = 2, relief = "solid",
                                        bg = "white").place(x = 100, y = 280, width = 800, height = 400) #The white box which the ratings are placed in

        
        HighIncomeText = Label(self.policy_screen, text = ("High Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 305, width = 280, height = 25)
        HighIncomePercentage = Label(self.policy_screen, text = (round(self.HIR), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = self.ratings[self.HIR], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 330, width = 280, height = 50)

        PensionersText = Label(self.policy_screen, text = ("Pensioners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 305, width = 280, height = 25)
        PensionersPercentage = Label(self.policy_screen, text = (round(self.PR), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = self.ratings[self.PR], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 330, width = 280, height = 50)
        
        MiddleIncomeText = Label(self.policy_screen, text = ("Middle Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 395, width = 280, height = 25)
        MiddleIncomePercentage = Label(self.policy_screen, text = (round(self.MIR), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                             bg = self.ratings[self.MIR], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 420, width = 280, height = 50)

        UnemployedText = Label(self.policy_screen, text = ("Unemployed Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 395, width = 280, height = 25)
        UnemployedPercentage = Label(self.policy_screen, text = (round(self.UR),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = self.ratings[self.UR], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 420, width = 280, height = 50)

        LowIncomeText = Label(self.policy_screen, text = ("Low Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 485, width = 280, height = 25)
        LowIncomePercentage = Label(self.policy_screen, text = ((round(self.LIR)),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                          bg = self.ratings[self.LIR], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 510, width = 280, height = 50)

        BusinessText = Label(self.policy_screen, text = ("Businesses Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 485, width = 280, height = 25)            
        BusinessPercentage = Label(self.policy_screen, text = ((round(self.BR)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                         bg = self.ratings[self.BR], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 510, width = 280, height = 50)

        OverallText = Label(self.policy_screen, text = ("Overall Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 14, "bold")).place(x = 130, y = 575, width = 760, height = 25)
        OverallPercentage = Label(self.policy_screen, text = ((round(self.OR)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                        bg = self.ratings[self.OR], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 600, width = 760, height = 50)

        


    
    
    #This method is used for both displaying temporary effects and calculating all temporary effects and for displaying and calculating all final changes (after simulate has been pressed).
    def change_figures(self, weighteddictionary):
        #This is the method that will update the actual values through calculations using the weights generated from the depth first traversal (the weights have been passed in)
        #print(weighteddictionary)
        changedfigures = {}    #New dictionary with the actual changed figures which will be returned.


        #For every element (name) in the list which contains all names of figures
        for name in self.namesoffigures:
            
            #For each key in the weighteddictionary, which contains the node name and the value it must change by
            for key in weighteddictionary:
                
                #If the key (visited node name) is equal to the current name in the list being looked at
                if key == name:

                    
                    indexofname = self.namesoffigures.index(name)   #self.namesoffigures.index(name) gets the index of the element being looked at.
                    
                    
                    
                    if name == "CurrentAccount":    #As the current account value is not timesed by the weight, an if statement can be used.

                        #Add self which increases efficiency as not every single figure needs to be passed through
                        newval = eval("self." + self.namesoffigures[indexofname]) - weighteddictionary[name]
                        
                    elif name == "UnemploymentRate":
                        #Add self which increases efficiency as not every single figure needs to be passed through
                        newval = eval("self." + self.namesoffigures[indexofname]) - weighteddictionary[name]
                        if newval < 0:  #As unemployment rate cannot be less than 0 randomise another value for new val that is very small.
                            newval = random.uniform(0.2, 0.5)

                    elif name == "GovernmentSpending":
                        newval = eval("self." + self.namesoffigures[indexofname]) + weighteddictionary[name]

                    elif name == "CurrencyValue":
                        newval = weighteddictionary[name]   #The value is not added or timesed etc... it is just the value that was generated.
                            
                    
                        
                    else:
                        #Otherwise times the actual figure by its weight
                        #Add self which increases efficiency as not every single figure needs to be passed through
                        newval = eval("self." + self.namesoffigures[indexofname]) * weighteddictionary[name]

                        #print("calc is ", eval("self." + self.namesoffigures[indexofname]), " * ", weighteddictionary[name])


                    #If the current key is a rating then check if its exceeds 100 or is less than 0 then alter the newvalue
                    if key in self.namesofratings:
                        if newval > 100:
                            newval = 100 - (random.uniform(1, 5))
                            #Set the value no a random number near 100 (between 95 and 99)
            
                        elif newval < 0:
                            newval = (random.uniform(1, 5))
                            #Set the value no a random number near 0 (between 1 and 5)
                        
                    changedfigures[key] = newval

                
                            
                    #print("newval is ", newval)

            
                    
                    
        return changedfigures
    
    def display_temp_figures(self, changedamount, startpoint):
        #print(changedfigures)

        #This method will call a method in this class called change_figures to update the figures.
        #It will then loop through again itself (in this method) a list and a dictionary (of updated values) and those values whose didn't change are appended to the dictionary
        #   with their original/current value so that updating the screen and later on the database can be more efficient.

        change = GT.MakeChanges(self.UserID, startpoint)
        if startpoint.replace(" ", "") in self.namesoftaxes:
            weighteddictionary = change.RunTaxGraph(startpoint + " Start", changedamount)
        elif startpoint.replace(" ", "") in self.namesofspending:
            weighteddictionary = change.RunSpendingGraph(startpoint + " Start", changedamount)
        #print(weighteddictionary)
        print("weighteddictionary is :")
        print(weighteddictionary)
        print(" ")
        
        if startpoint == "Interest Rates":  #For interest rates, take the total change, as there are two factors effecting it.
            weighteddictionary['CurrentAccount'] = weighteddictionary['CurrentAccount 1'] + weighteddictionary['CurrentAccount 2']
            del weighteddictionary['CurrentAccount 1'], weighteddictionary['CurrentAccount 2']  #Remove these from the dictionary to save running an extra 2 loops (as these aren't
                                                                                                #   factors which can be affected as they are only temporary)
            
        changedfigures = self.change_figures(weighteddictionary)    #Calls the method in policies_everything change_figures to update all the values with the generated values.

        #Now find which values were not changed and append them to the dictionary with their default/unchanged values so that everything can be accessed efficiently from one place.
        for name in self.namesoffigures:
            if name not in changedfigures:
                changedfigures[name] = eval("self." + name) #Add self as this is how it is accessed and use the eval function to get the value stored in it, not just the variable name.
                print(name)
        print(changedfigures)

        #Without this method appending values that didnt change to the changedfigures dictionary, changedfigures[nameofratingtoupdate]
        #   would not work as not all ratings are changed so would not be in the changedfiguresdictionary, meaning the code must must repeated in every policy with just a few 
        #   small changes which reduces efficiency. For example, without this method, corporation tax not affecting high income earners would require self.HIR instead of
        #   changedfigures[nameofratingtoupdate], and this is different for each policy etc...
        self.temp_policy_showratings(self.slider, changedfigures['HighIncome'],changedfigures['Pensioners'],changedfigures['MiddleIncome'],
                                         changedfigures['Unemployed'],changedfigures['LowIncome'],changedfigures['Businesses']) #Dont pass in overall as it is calculated later

        
            
        self.policy_screen.update()

        return changedfigures


    def temp_policy_showratings(self, slider, HighIncomeRating, PensionersRating, MiddleIncomeRating, UnemployedRating, LowIncomeRating, BusinessRating):
        #This method is used when the view expected changes button is pressed. As this button press does not add the changed values calculated through the depth first graph traversal to
        #   the database so a new method must be created to temporarily show the expected changes.
        #This method must therefore take in the temporarily changed values as opposed to extract them from the database and must calculate the colours for each label again.

        OverallRating = round(((HighIncomeRating + PensionersRating + MiddleIncomeRating + UnemployedRating + LowIncomeRating + BusinessRating)/6),2)

        #Once again re-calculate the colours based off of the values
        if HighIncomeRating < 40:
            HighIncomeColour = "red"
        elif HighIncomeRating < 70:
            HighIncomeColour = "orange"
        else: HighIncomeColour = "green"

        if PensionersRating < 40:
            PensionersColour = "red"
        elif PensionersRating < 70:
            PensionersColour = "orange"
        else: PensionersColour = "green"

        if MiddleIncomeRating < 40:
            MiddleIncomeColour = "red"
        elif MiddleIncomeRating < 70:
            MiddleIncomeColour = "orange"
        else: MiddleIncomeColour = "green"

        if UnemployedRating < 40:
            UnemployedColour = "red"
        elif UnemployedRating < 70:
            UnemployedColour = "orange"
        else: UnemployedColour = "green"

        if LowIncomeRating < 40:
            LowIncomeColour = "red"
        elif LowIncomeRating < 70:
            LowIncomeColour = "orange"
        else: LowIncomeColour = "green"

        if BusinessRating < 40:
            BusinessColour = "red"
        elif BusinessRating < 70:
            BusinessColour = "orange"
        else: BusinessColour = "green"

        if OverallRating < 40:
            OverallColour = "red"
        elif OverallRating < 70:
            OverallColour = "orange"
        else: OverallColour = "green"



        #Once again use a dictionary to store the ratings and colours
        ratings = {HighIncomeRating : HighIncomeColour,                 
                                 PensionersRating : PensionersColour,
                                 MiddleIncomeRating : MiddleIncomeColour,
                                 UnemployedRating : UnemployedColour,
                                 LowIncomeRating : LowIncomeColour,
                                 BusinessRating : BusinessColour,
                                 OverallRating : OverallColour}


                
        #whiteboxforratings = Label(self.policy_screen, borderwidth = 2, relief = "solid",
         #                               bg = "white").place(x = 100, y = 280, width = 800, height = 400) #The white box which the ratings are placed in

        
        HighIncomeText = Label(self.policy_screen, text = ("High Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 305, width = 280, height = 25)
        HighIncomePercentage = Label(self.policy_screen, text = (round(HighIncomeRating), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[HighIncomeRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 330, width = 280, height = 50)

        PensionersText = Label(self.policy_screen, text = ("Pensioners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 305, width = 280, height = 25)
        PensionersPercentage = Label(self.policy_screen, text = (round(PensionersRating), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[PensionersRating], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 330, width = 280, height = 50)
        
        MiddleIncomeText = Label(self.policy_screen, text = ("Middle Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 395, width = 280, height = 25)
        MiddleIncomePercentage = Label(self.policy_screen, text = (round(MiddleIncomeRating), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                             bg = ratings[MiddleIncomeRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 420, width = 280, height = 50)

        UnemployedText = Label(self.policy_screen, text = ("Unemployed Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 395, width = 280, height = 25)
        UnemployedPercentage = Label(self.policy_screen, text = (round(UnemployedRating),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[UnemployedRating], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 420, width = 280, height = 50)

        LowIncomeText = Label(self.policy_screen, text = ("Low Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 485, width = 280, height = 25)
        LowIncomePercentage = Label(self.policy_screen, text = ((round(LowIncomeRating)),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                          bg = ratings[LowIncomeRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 510, width = 280, height = 50)

        BusinessText = Label(self.policy_screen, text = ("Business Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 485, width = 280, height = 25)            
        BusinessPercentage = Label(self.policy_screen, text = ((round(BusinessRating)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                         bg = ratings[BusinessRating], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 510, width = 280, height = 50)

        OverallText = Label(self.policy_screen, text = ("Overall Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 14, "bold")).place(x = 130, y = 575, width = 760, height = 25)
        OverallPercentage = Label(self.policy_screen, text = ((round(OverallRating)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                        bg = ratings[OverallRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 600, width = 760, height = 50)



    def getChangedFigures(self, changedamount, startpoint):

        change = GT.MakeChanges(self.UserID, startpoint)
        
        if startpoint.replace(" ", "") in self.namesoftaxes:
            weighteddictionary = change.RunTaxGraph(startpoint + " Start", changedamount)
            
        elif startpoint.replace(" ", "") in self.namesofspending:
            weighteddictionary = change.RunSpendingGraph(startpoint + " Start", changedamount)



        print("weighteddictionary is :")
        print(weighteddictionary)
        new = weighteddictionary
        return weighteddictionary

        

    def showRatingsAfterSimulation():
        
        OverallRating = round(((HighIncomeRating + PensionersRating + MiddleIncomeRating + UnemployedRating + LowIncomeRating + BusinessRating)/6),2)

        #Once again re-calculate the colours based off of the values
        if HighIncomeRating < 40:
            HighIncomeColour = "red"
        elif HighIncomeRating < 70:
            HighIncomeColour = "orange"
        else: HighIncomeColour = "green"

        if PensionersRating < 40:
            PensionersColour = "red"
        elif PensionersRating < 70:
            PensionersColour = "orange"
        else: PensionersColour = "green"

        if MiddleIncomeRating < 40:
            MiddleIncomeColour = "red"
        elif MiddleIncomeRating < 70:
            MiddleIncomeColour = "orange"
        else: MiddleIncomeColour = "green"

        if UnemployedRating < 40:
            UnemployedColour = "red"
        elif UnemployedRating < 70:
            UnemployedColour = "orange"
        else: UnemployedColour = "green"

        if LowIncomeRating < 40:
            LowIncomeColour = "red"
        elif LowIncomeRating < 70:
            LowIncomeColour = "orange"
        else: LowIncomeColour = "green"

        if BusinessRating < 40:
            BusinessColour = "red"
        elif BusinessRating < 70:
            BusinessColour = "orange"
        else: BusinessColour = "green"

        if OverallRating < 40:
            OverallColour = "red"
        elif OverallRating < 70:
            OverallColour = "orange"
        else: OverallColour = "green"



        #Once again use a dictionary to store the ratings and colours
        ratings = {HighIncomeRating : HighIncomeColour,                 
                                 PensionersRating : PensionersColour,
                                 MiddleIncomeRating : MiddleIncomeColour,
                                 UnemployedRating : UnemployedColour,
                                 LowIncomeRating : LowIncomeColour,
                                 BusinessRating : BusinessColour,
                                 OverallRating : OverallColour}


                
        #whiteboxforratings = Label(self.policy_screen, borderwidth = 2, relief = "solid",
         #                               bg = "white").place(x = 100, y = 280, width = 800, height = 400) #The white box which the ratings are placed in

        
        HighIncomeText = Label(self.policy_screen, text = ("High Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 305, width = 280, height = 25)
        HighIncomePercentage = Label(self.policy_screen, text = (round(HighIncomeRating), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[HighIncomeRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 330, width = 280, height = 50)

        PensionersText = Label(self.policy_screen, text = ("Pensioners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 305, width = 280, height = 25)
        PensionersPercentage = Label(self.policy_screen, text = (round(PensionersRating), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[PensionersRating], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 330, width = 280, height = 50)
        
        MiddleIncomeText = Label(self.policy_screen, text = ("Middle Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 395, width = 280, height = 25)
        MiddleIncomePercentage = Label(self.policy_screen, text = (round(MiddleIncomeRating), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                             bg = ratings[MiddleIncomeRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 420, width = 280, height = 50)

        UnemployedText = Label(self.policy_screen, text = ("Unemployed Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 395, width = 280, height = 25)
        UnemployedPercentage = Label(self.policy_screen, text = (round(UnemployedRating),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[UnemployedRating], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 420, width = 280, height = 50)

        LowIncomeText = Label(self.policy_screen, text = ("Low Income Earners Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 130, y = 485, width = 280, height = 25)
        LowIncomePercentage = Label(self.policy_screen, text = ((round(LowIncomeRating)),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                          bg = ratings[LowIncomeRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 510, width = 280, height = 50)

        BusinessText = Label(self.policy_screen, text = ("Businesses Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 590, y = 485, width = 280, height = 25)            
        BusinessPercentage = Label(self.policy_screen, text = ((round(BusinessRating)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                         bg = ratings[BusinessRating], font = ("Comic Sans", 12, "bold")).place(x = 590, y = 510, width = 280, height = 50)

        OverallText = Label(self.policy_screen, text = ("Overall Satisfaction"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 14, "bold")).place(x = 130, y = 575, width = 760, height = 25)
        OverallPercentage = Label(self.policy_screen, text = ((round(OverallRating)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                        bg = ratings[OverallRating], font = ("Comic Sans", 12, "bold")).place(x = 130, y = 600, width = 760, height = 50)





    def CheckConfirmChanges(self, newvalue, original):
        #After the confirm button in each policy class is clicked (which overrides confirm_changes in this class), this method will calculate the changedamount and if this is 0, will
        #   remind the user that in order to confirm a change they must make a change.
        changedamount = newvalue - original
        if changedamount != 0:
            self.select_priority(changedamount)
        else:
            message = """Must change the
current level to
confirm changes"""
            self.Error(message)

        
    def select_priority(self, changedamount):
        priority_screen = Tk()
        priority_screen.configure(bg = "light grey")
        priority_screen.geometry("1000x800+460+140") #1000x800
        priority_screen.title("Select Priority")
        priority_screen.resizable(False,False)

        Highest = Button(priority_screen, text = "Highest", foreground = "white", command = lambda: self.priority_selected(priority_screen, 1, changedamount), 
                               bg = "black", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 40, width = 960, height = 150)
        Middle = Button(priority_screen, text = "Middle", foreground = "white", command = lambda: self.priority_selected(priority_screen, 2, changedamount) ,
                               bg = "black", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 230, width = 960, height = 150)
        Low = Button(priority_screen, text = "Low", foreground = "white", command = lambda: self.priority_selected(priority_screen, 3, changedamount), 
                               bg = "black", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 420, width = 960, height = 150)
        Lowest = Button(priority_screen, text = "Lowest", foreground = "white", command = lambda: self.priority_selected(priority_screen, 4, changedamount), 
                               bg = "black", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 610, width = 960, height = 150)

    def priority_selected(self, priority_screen, priority, changedamount):  #priority will become the key and the value will be a list with the first element being the policyname and
                                                                            #   the second element being the changedamount (as required for the priority queue class to function properly).
                                                                            
        try:    #As soon as a priority is selected, the priority selection screen will be destroyed, however if the user is changing a policy that is already in the confirmed policies
                #   and the policies confirmed is at its maximum, then it will remove the policy and re call this method, but priority_screen is already destroyed, so cannot be
                #   destroyed again, therefore if it is open, destroy it otherwise just move on.
            priority_screen.destroy()
        except:
            pass

        OtherStatements = OS.ExtraStatements(self.UserID)   #Intialise Extra Statements which will be used in this method.

        #Load policiesconfirmed as a dictionary (already been converted from a string dictionary to a dictionary)
        policiesconfirmed = self.LoadPoliciesConfirmed()

        PriorityQ = PQ.PriorityQueueFunctions(self.UserID, [], policiesconfirmed)

        #If the use has already used their maximum number of policies
        print("Before changes, the policies confirmed were previously: ", policiesconfirmed)
        if len(policiesconfirmed) == 4:
            print("Already 4 in there")
            toRemove = []
            for key, value in policiesconfirmed.items():
                if value[0] == self.nameofpolicy:   #If the policy being added is already in the confirmed policies, then the user doesn't need to remove any policies.
                    print("its already in there")
                    toRemove = [key]
            if toRemove == []:  #Then this policy being added is not already in the confirmed policies, so it must replace another one
                print("The policy being added is not already in the confirmed policies")
                replace = ReplaceOrRemovePolicy(self.UserID, policiesconfirmed, priority, [self.nameofpolicy, changedamount]) 
                replace.DisplayCurrentPoliciesForRemoval()
            else:   #The policy being added is already in the policies confirmed, so just needs to re-shuffle the policies priorities according to what the user has chosen.
                OtherStatements.removePolicyFromConfirmed(toRemove[0])
                self.priority_selected(priority_screen, priority, changedamount)
                return
                
                            
            
        elif not policiesconfirmed:   #If the dictionary is empty then just add the priority as the key and the value as a list of the changed policies name with its changedamount.
            print("Empty")
            policiesconfirmed[str(priority)] = [self.nameofpolicy, changedamount]   #prioirty converted to string as it will be converted to string anyways as soon as json.dumps
                                                                                    #   is run on it. By converting it to string, any policy that had previously been confirmed but has now
                                                                                    #   been confirmed again but with a different amount will just override itself/ update itself as the key
                                                                                    #   has been converted to string so will be the same.
        else:
            print("Not empty")
            priorityexists = False  #Set this to false before looping through to identify if a policy already has this priority.
            for key in policiesconfirmed.keys():
                if int(key) == priority: #Then a policy has already been confirmed with this priority.
                    priorityexists = True   #Then we know that there is already a policy that has been confirmed with this priority
            if len(policiesconfirmed) < 4:
                if priorityexists:  #Then we can actually still add this policy in, just shift every other policy with a lower priority (grater in value) down.
                    policiesconfirmed = PriorityQ.shift_priorities(priority)   #Shift down any priorities


            
            #If the user is just changing the priority
            policyexists = False
            for key, value in policiesconfirmed.items():
                print(value[0])
                if value[0] == self.nameofpolicy:   #Check if it is in the existing ones
                    print("policy exists now true")
                    policyexists = True #If it is set policyexists to True
                    existingpolicykey = key #Set the key to this so it can be referred to (does not need to be set before the loop as it is only used if policyexists is true).

                    
            if policyexists:
                del policiesconfirmed[existingpolicykey]    #If its in the existing ones just remove it.


            if len(policiesconfirmed) < 4:  #Policies with 0 or less as their key are added after the simulate button has been pressed, so at this point the maximum size of the dictionary
                                            #   can only ever be 4.
                policiesconfirmed[str(priority)] = [self.nameofpolicy, changedamount]



                
        print("new policies confirmed are: ",policiesconfirmed)

        OtherStatements.addPoliciesConfirmed(policiesconfirmed)
        #policiesconfirmed['AWESOME'] = 2
        #economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        #mycursor = economygamedb.cursor()
        #updatepoliciesconfirmed = "UPDATE PoliciesConfirmed SET Changes = (%s) WHERE ConfirmedID = (%s)"
        #policiesconfirmed_string = json.dumps(policiesconfirmed)    #Convert to string to enter it into database.
        #mycursor.execute(updatepoliciesconfirmed, (policiesconfirmed_string, self.UserID))  #Update the column which shows the changes with the User's ID.
        #economygamedb.commit()
        
        
        
    
    def policy_label(self): #This method may be overidden if the policy name label needs to be moved etc...
        if self.nameofpolicy.replace(" ", "") in self.namesoftaxes:
            additional = " %"   #Add the unit to the label
        else:
            additional = " £bn"
        policylabel = Label(self.policy_screen, text = self.actualpolicy + additional, foreground = "black",
                               bg = "light grey", font = ("Comic Sans", 18, "bold")).place(x = self.startx, y = 50, width = self.startwidth, height = 50)

    def helpbutton(self):
        infobutton = Button(self.policy_screen, text = "What do I do?", foreground = "black", command = lambda: self.load_help(""), 
                               bg = "white", font = ("Comic Sans", 18, "bold")).place(x = 350, y = 200, width = 300, height = 50)


    def slider(self, position, maximum, res, tick):   #This method will be overidden in some of its child classes. Most policies will use a percentage slider, but some may use actual currency values, or not got to 100.
                        #In this case, the method will be overidden (polymorphism). #Some may have a percentage tax of 150% (VAT), but unlikely. #Res represents the value increase as
                        #   the slider is dragged (.1 etc)

        slider = Scale(self.policy_screen, bg = "light grey", borderwidth = 2, highlightbackground = "lightgrey", from_ = 0, to = maximum,
                       length = 800, tickinterval = tick, resolution = res, orient = HORIZONTAL)
        slider.set(position)
        slider.place(x = 10, y = 100, width = 980, height = 100)
        #percentage_symbol = Label(self.policy_screen, text = "%", foreground = "black", 
         #                         bg = "light grey", font = ("Comic Sans", 10, "bold")).place(x = 980, y = 90, width = 20, height = 100)

  

        viewthechange = Button(self.policy_screen, text = """View Expected
Changes""", foreground = "black", command = lambda: self.view_expectedchanges(slider), borderwidth = 4, relief = "solid",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 420, y = 395, width = 160, height = 80)
        confirmthechange = Button(self.policy_screen, text = "Confirm Changes", foreground = "black", command = lambda: self.confirm_changes(slider),
                               bg = "magenta", font = ("Comic Sans", 18, "bold")).place(x = 350, y = 700, width = 300, height = 80)


    

    
    def backtochoice(self): #This method will also be overidden
       backbutton = Button(self.policy_screen, text = "Back", foreground = "black", command = lambda: self.backcommand(self.UserID), borderwidth = 4, relief = "solid",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 0, y = 700, width = 200, height = 100)     






    def load_help(self, help_text): #help text is passed as "" just so that a value is passed. Its actual text is determined in each sub policy such as IncomeTax
        helpwindow_screen = Tk()
        helpwindow_screen.configure(bg = "white")
        helpwindow_screen.title(self.actualpolicy)
        helpwindow_screen.geometry("700x500+660+390")
                #This method is unique to to the other methods that are to be overidden as before it is overidden, the parent method will run. This differs to the others as
                #   those methods are overidden instantly without doing anything inside the parent method.
                #This method being overidden after it has carried out its own sequence of steps (creating the help window) is highly important for reducing the lines of code
                #   and making the program more robust and efficient

        helptext = Label(helpwindow_screen, text = help_text, foreground = "black", 
                                  bg = "white", font = ("Comic Sans", 12)).place(x = 0, y = 100, width = 700, height = 300)
            
    def Error(self, message):

        #If the user presses confirm changes without changing the current level then a message will be displayed reminding them that they must make a change to press confirm.
        error_screen = Tk()
        error_screen.geometry("400x400+760+340")
        error_screen.title("Oops!")
        error_screen.configure(bg = "red")
        error_screen.resizable(False,False)

        error_label = Label(error_screen, text = message,
                            bg = "red", foreground = "white", font = ("Comic Sans", 14, "bold")).place(x = 0, y = 10, width = 400, height = 100)

        error_button = Button(error_screen, text = "Press to close", foreground = "white", font = ("Comic Sans", 10, "bold"),
                                   bg = "red", command = lambda : error_screen.destroy()).place(x = 50, y = 200, width = 300, height = 100)


    def restorePoliciesConfirmed(self):
        policiesconfirmed = {}
        resetpoliciesconfirmed = OS.ExtraStatements(self.UserID)
        resetpoliciesconfirmed.addPoliciesConfirmed(policiesconfirmed)
    #def PoliciesConfirmed(self, policiesconfirmed):
     #   print(policiesconfirmed)
#--------------These methods below are meant to be overidden. It is only defined so that the child class methods can be called, which will override the parent methods
    def confirm_changes(self, slider):
        pass

    def view_expectedchanges(self, slider):
        pass

    def backcommand(self, UserID):
        pass        
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



#-----------------------------------------------------When the user wants to replace or remove a policy that has been confirmed-----------------------------------------------------#
class ReplaceOrRemovePolicy():

    def __init__(self, UserID, policiesconfirmed, priority, replacing):

        self.UserID = UserID
        self.policiesconfirmed = policiesconfirmed
        self.priority = priority
        self.replacing = replacing  #Determines whether after removing the policy another one is added, or if it is left with an extra slot depending on if its empty or not.

        if self.replacing:
            title = "Select which one to remove"
        else:
            title = "Your confirmed policies"

        
        self.remove_screen = Tk()
        self.remove_screen.configure(bg = "aqua")
        self.remove_screen.geometry("1000x800+460+140") #1000x800
        self.remove_screen.title(title)
        self.remove_screen.resizable(False,False)


    def DisplayCurrentPolicies(self):
        #Not based on the order of priority

        policies = policies_everything(None, None, self.UserID)
        policies.policy_screen.destroy()
        current_confirmed = []  #Make a list of all the values in the dictionary policiesconfirmed (not the changed amount, so the first element only).
       
        for key, value in self.policiesconfirmed.items():
            if value[0].replace(" ", "") in policies.namesoftaxes:  #Remove the spaces.
                policyname_confirmed = (value[0] + ":    " + str(round(value[1],2)) + "%")   #The unit is %.
            else:
                policyname_confirmed = (value[0] + ":     £" + str(round(value[1],2)) + " billion")  #The unit is £ billion.
            current_confirmed.append(policyname_confirmed)
        
        #try and except is used as there may not be a full set of policies confirmed, therefore except is used to just ignore this and pass.
        try:
            FirstPolicy = Label(self.remove_screen, text = current_confirmed[0], foreground = "white", 
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 40, width = 960, height = 150)
        except: #If there is no first policy that can be displayed, this means there are no confirmed policies yet, so display that there are none.
            NoChanges = Label(self.remove_screen, text = "No Changes Made", foreground = "black", 
                               bg = "aqua", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 325, width = 960, height = 150)
            
            
        try:
            SecondPolicy = Label(self.remove_screen, text = current_confirmed[1], foreground = "white",
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 230, width = 960, height = 150)
        except:
            pass
        
        
        try:
            ThirdPolicy = Label(self.remove_screen, text = current_confirmed[2], foreground = "white", 
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 420, width = 960, height = 150)
        except:
            pass

        
        try:
            FourthPolicy = Label(self.remove_screen, text = current_confirmed[3], foreground = "white", 
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 610, width = 960, height = 150)
        except:
            pass

        
    def DisplayCurrentPoliciesForRemoval(self):

        current_confirmed = []  #Make a list of all the values in the dictionary policiesconfirmed (not the changed amount, so the first element only).

        for key, value in self.policiesconfirmed.items():
            policyname_confirmed = value[0] #Getting the first element in the list (which is the value of the dictonary) will give the name of the policy without its changed amount.
            current_confirmed.append(policyname_confirmed)

        FirstPolicy = Button(self.remove_screen, text = current_confirmed[0], foreground = "white", command = lambda: self.removePolicy(current_confirmed[0]), 
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 40, width = 960, height = 150)
        SecondPolicy = Button(self.remove_screen, text = current_confirmed[1], foreground = "white", command = lambda: self.removePolicy(current_confirmed[1]),
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 230, width = 960, height = 150)
        ThirdPolicy = Button(self.remove_screen, text = current_confirmed[2], foreground = "white", command = lambda: self.removePolicy(current_confirmed[2]), 
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 420, width = 960, height = 150)
        FourthPolicy = Button(self.remove_screen, text = current_confirmed[3], foreground = "white", command = lambda: self.removePolicy(current_confirmed[3]), 
                               bg = "blue", font = ("Comic Sans", 18, "bold")).place(x = 20, y = 610, width = 960, height = 150)
        

    def removePolicy(self, toRemove):
    
        print("removing ", toRemove)

        self.remove_screen.destroy()

        for key in self.policiesconfirmed:
            if (self.policiesconfirmed[key])[0] == toRemove:
                keyToRemove = key
                print("it is in key: ", key)
                OtherStatements = OS.ExtraStatements(self.UserID)
                OtherStatements.removePolicyFromConfirmed(keyToRemove)

        if self.replacing != []:   #Its not empty meaning there is another policy that needs to be added. After removing the policy, add the newone.
            addpolicy = policies_everything(self.replacing[0], self.replacing[0], self.UserID)
            addpolicy.policy_screen.destroy()   #Don't reload the policy screen.
            addpolicy.priority_selected(None, self.priority, self.replacing[1]) #Now with add the new policy in and shift other priorities if necessary.

#End of file: PolicyRatingDisplay
           

        

        
        
        

def mainpolicyratingload():
    nameofpolicy = "MonetaryPolicy"
    actualpolicy = "Interest Rates"
    UserID = 1
    loadstuff = policies_everything(nameofpolicy, actualpolicy, UserID)
    loadstuff.policy_showratings()
    loadstuff.policy_label()
    loadstuff.helpbutton()
    loadstuff.slider(40, 100, 0.1, 10)
    loadstuff.backtochoice()

if __name__ == "__main__":

    mainpolicyratingload()

#As this is an abstract base class, it will never be instantiated directly, only by child classes
