#File name: Main_Menu
from tkinter import *
from tkinter import messagebox
import random
import mysql.connector
import sys
import json
import math
#import PIL.Image  #For loading the image and rendering it.
#from PIL import ImageTk
sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases") #Load_Everything
import Load_Everything as LE

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\FiscalPolicy") #FiscalSelected
from FiscalSelected import *

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\MonetaryPolicy")   #MonetarySelected
import MonetarySelected as MonetarySelected

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\SSPolicy")    #SupplySidePolicySelected
import SSPSelected as SSPSelected

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
import OtherStatements as OS

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 3")
import Tutorial as TutorialGuide
import Charts as Chart
import PolicyRatingDisplay as PRD
import Simulate as Simulate


class NewOrContinue():

    def __init__(self, UserID, newgame):
        
        self.UserID = UserID
        self.newgame = newgame

    def check(self):

        
        
        if not self.newgame:  #There is already a game in progress so continue it
            
            print("USER DATA EXISTS")
            continuegame = menu_main(self.UserID)
            continuegame.GetRatings()
            continuegame.GetStatistics()
             
            
        else:   #This is a newgame so start one with new stats etc...
            print("there is no data")

            economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
            mycursor = economygamedb.cursor()

            
            setpoliciesconfirmed = "INSERT INTO PoliciesConfirmed(ConfirmedID, Changes, Q2Changes, Q3Changes, TimeLagged) VALUES (%s, %s, %s, %s, %s)"
            
            emptydictionary = {}
            touse = (self.UserID, str(emptydictionary), str(emptydictionary), str(emptydictionary), str([]))
        
            mycursor.execute(setpoliciesconfirmed, touse)

            newgameisfalse = "UPDATE USERS SET NewGame = 0 WHERE UserID = %s"
            mycursor.execute(newgameisfalse, (self.UserID,))

            economygamedb.commit()
            

            startnewgame = New_Game(self.UserID)
            startnewgame.RandomiseRatings() #MAYBE MAKE ANOTHER FUNCTION WHICH RUNS ALL OF THESE
            
            startnewgame.RandomiseStatistics()
            startnewgame.RandomiseMonetaryPolicies()
            startnewgame.RandomiseFiscalTaxes()
            startnewgame.RandomiseFiscalSpending()
            startnewgame.RandomiseSSSpending()
            startnewgame.RandomiseExtraStats()

                
            displayother = menu_main(self.UserID) #Will be UserID #THIS DOESNT WORK FIX THIS
            displayother.display_other()
            
                

        



class New_Game():

    def __init__(self, UserID):
        self.ratings = {}
        self.UserID = UserID

        self.GovernmentSpending = 0     #So that the total government spending used later can be accumulated as stats are generated and stored in the database.


        

    def RandomiseRatings(self):

        HighIncomeRating = round(random.uniform(0.1, 0.9,),2) #Round to 2dp so the percentage is an integer
        PensionersRating = round(random.uniform(0.1, 0.9,),2)
        MiddleIncomeRating = round(random.uniform(0.1, 0.9,),2)
        UnemployedRating = round(random.uniform(0.1, 0.9,),2)
        LowIncomeRating = round(random.uniform(0.1, 0.9,),2)
        BusinessRating = round(random.uniform(0.1, 0.9,),2)
        
        OverallRating = round(((HighIncomeRating + PensionersRating + MiddleIncomeRating + UnemployedRating + LowIncomeRating + BusinessRating)/6),2)



        if HighIncomeRating < 0.4:
            HighIncomeColour = "red"
        elif HighIncomeRating < 0.7:
            HighIncomeColour = "orange"
        else: HighIncomeColour = "green"

        if PensionersRating < 0.4:
            PensionersColour = "red"
        elif PensionersRating < 0.7:
            PensionersColour = "orange"
        else: PensionersColour = "green"

        if MiddleIncomeRating < 0.4:
            MiddleIncomeColour = "red"
        elif MiddleIncomeRating < 0.7:
            MiddleIncomeColour = "orange"
        else: MiddleIncomeColour = "green"

        if UnemployedRating < 0.4:
            UnemployedColour = "red"
        elif UnemployedRating < 0.7:
            UnemployedColour = "orange"
        else: UnemployedColour = "green"

        if LowIncomeRating < 0.4:
            LowIncomeColour = "red"
        elif LowIncomeRating < 0.7:
            LowIncomeColour = "orange"
        else: LowIncomeColour = "green"

        if BusinessRating < 0.4:
            BusinessColour = "red"
        elif BusinessRating < 0.7:
            BusinessColour = "orange"
        else: BusinessColour = "green"

        if OverallRating < 0.4:
            OverallColour = "red"
        elif OverallRating < 0.7:
            OverallColour = "orange"
        else: OverallColour = "green"


        self.ratings = {HighIncomeRating : HighIncomeColour,
                         PensionersRating : PensionersColour,
                         MiddleIncomeRating : MiddleIncomeColour,
                         UnemployedRating : UnemployedColour,
                         LowIncomeRating : LowIncomeColour,
                         BusinessRating : BusinessColour,
                         OverallRating : OverallColour}

        print("generated ratings are: ", self.ratings)


        #Insert these new values into the database
        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addratings = ("INSERT INTO Ratings(RatingsID, HighIncome, MiddleIncome, LowIncome, Pensioners, Unemployed, Businesses, Overall) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        ratingstoadd = (self.UserID, HighIncomeRating, MiddleIncomeRating, LowIncomeRating, PensionersRating, UnemployedRating, BusinessRating, OverallRating)
        mycursor.execute(addratings, ratingstoadd)
        economygamedb.commit()

        #displayratings = menu_main(self.UserID) #Will be UserID #THIS DOESNT WORK FIX THIS 
        #displayratings.GetRatings()

    def RandomiseStatistics(self):

        
        getratings = LE.Load(self.UserID)
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings()
        print(HIR, PR, MIR, UR, LIR, BR, OR)

        #When generating other values, they must be realistic
        #Therefore for example, if high, middle and low income earners are relatively happy, the current account would most likely be a negative value (deficit) as imports would be higher
        #   as the green indicates that they have more money (happier with the economy as they are better off)

        
        #Realistically randomise the Current Account
        if HIR and MIR and LIR > 0.6:
            CurrentAccount = round((random.uniform(-50,10)),2) #Billion
        elif HIR and MIR and LIR > 0.4:
            CurrentAccount = round((random.uniform(-30,30)),2) #Billion
        else:
            CurrentAccount = round((random.uniform(-10,50)),2) #Billion
        
        #Realistically randomise the Unemployment Rate
        if UR > 80:
            UnemploymentRate = round((random.uniform(2,4)),2)
        elif UR > 60:
            UnemploymentRate = round((random.uniform(2,5)),2)
        elif UR > 40:
            UnemploymentRate = round((random.uniform(4,6)),2)
        else:
            UnemploymentRate = round((random.uniform(6,8)),2)

        #Realistically randomise the Inflation Rate
        if PR and BR > 60:
            InflationRate = round((random.uniform(1.5,3.5)),2)
        elif PR and BR > 40:
            InflationRate = round((random.uniform(0.8,5)),2)
        else:
            InflationRate = round((random.uniform(0.1,7)),2)

        #Realistically randomise the GDP, a good representation of economic growth -- This is not Real GDP!
        if HIR > 80 and MIR > 80 and LIR > 80 and BR > 60:
            GDP = round((random.uniform(200, 400)),2) #Billion #MAYBE CHANGE TO TRILLION LATER
        elif HIR > 60 and MIR > 60 and LIR > 60 and BR > 60:
            GDP = round((random.uniform(100,280)),2)
        elif HIR > 60 and MIR > 60 and LIR > 0.4 and BR > 0.6:
            GDP = round((random.uniform(100,240)),2)
        elif HIR > 60 and MIR > 60 and LIR > 0.8 and BR > 0.4:
            GDP = round((random.uniform(150,280)),2)
        elif HIR > 40 and MIR > 60 and LIR > 0.6 and BR > 0.4:
            GDP = round((random.uniform(95,240)),2)
        elif HIR > 60 and MIR > 40 and LIR > 0.4 and BR > 0.4:
            GDP = round((random.uniform(90,180)),2)
        elif HIR > 40 and MIR > 40 and LIR > 0.6 and BR < 0.4:
            GDP = round((random.uniform(100, 240)),2)
        else:
            GDP = round((random.uniform(80,120)),2)

        #Randomise National Debt as a %
        NationalDebt = (round(random.uniform(15, 90),2)) #if national debt is high then supply side policies should be highly in use as the government is spending lots so needs to borrow lots etc...
        

        print("Current Account in Bn £: " , CurrentAccount)
        print("Unemployment as a % of the population: ", UnemploymentRate)
        print("Inflation Rate as a %: ", InflationRate)
        print("GDP in Bn £: ", GDP)
        print("National Debt as a % of GDP: ", NationalDebt)
        

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addstats = ("INSERT INTO Statistics(StatsID, NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        statstoadd = (self.UserID, NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, '2020-01-01')    #Always starts at the end of 2019/ beginning of 2020

        updateGDP = ("INSERT INTO GDPStatistics(GDPID, LastElectionGDP, LastElectionNationalDebt) VALUES (%s, %s, %s)")
        GDPupdate = (self.UserID, GDP, NationalDebt)

        
        mycursor.execute(addstats, statstoadd)
        mycursor.execute(updateGDP, GDPupdate)
        economygamedb.commit()

        

    def RandomiseMonetaryPolicies(self):

#------------------------Interest Rates-----------------------------------------------------------------------------------------------------------------------------------#
        
        getratings = LE.Load(self.UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings()

        ND, CA, UR, InfRate, GDP, Year = getratings.LoadStatistics()    #Use the method LoadRatings that was inherited from its parent class Load
        #print(ND, CA, UR, InfRate, GDP, Year)


        #Realistically randomise Interest Rates
        if InfRate < 0.8 and BR < 40:
            InterRate = round(random.uniform(8, 30),1)   #Will not allow interest rates to start higher than 30 as this is unrealistic, but the user can take them to 100%
        elif InfRate < 0.8 and BR < 60:
            InterRate = round(random.uniform(8, 25),1)
        elif InfRate < 0.8 and BR < 80:
            InterRate = round(random.uniform(8, 20),1)
        elif (InfRate < 1.2 and BR < 40) or (GDP < 0.8 and BR < 60):
            InterRate = round(random.uniform(6, 12),1)
        elif (InfRate < 1.8 and BR < 40) or (InfRate < 1.2 and BR < 60):
            InterRate = round(random.uniform(3, 10),1)
        elif (InfRate < 2.5 and BR < 40) or (InfRate < 1.8 and BR < 60):
            InterRate = round(random.uniform(3, 8),1)
        elif (InfRate < 4):
            InterRate = round(random.uniform(0.8, 5),1)
        else:
            InterRate = round(random.uniform(0.5, 1),1)

        print("Interest Rates are: ", InterRate, " %")

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addinterestrate = ("INSERT INTO MonetaryPolicies(MonetaryID, InterestRate) VALUES (%s, %s)")
        interestratetoadd = (self.UserID, InterRate)
        mycursor.execute(addinterestrate, interestratetoadd)
        economygamedb.commit()


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#



        

    def RandomiseFiscalTaxes(self):

        
        getratings = LE.Load(self.UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings()

        ND, CA, UR, InfRate, GDP, Year = getratings.LoadStatistics()

        

        #Realistically randomise Income Tax         #One income tax for all, not different brackets
        
        if HIR < 40 and MIR < 60 and LIR < 80:  #As income tax is progressive it will affect higher income earners the most 
            IncomeT = round(random.uniform(40, 70),1)   #Will never start at more than 80%
        elif HIR < 40 and MIR < 60 and LIR < 60:
            IncomeT = round(random.uniform(35, 60),1)
        elif HIR < 60 and (MIR < 80 or LIR < 80):
            IncomeT = round(random.uniform(30, 50),1)
        elif HIR < 60 and MIR < 60 and LIR < 60 :
            IncomeT = round(random.uniform(25, 40),1)
        elif HIR > 80 or MIR > 80:
            IncomeT = round(random.uniform(15, 25),1)
        else:
            IncomeT = round(random.uniform(15, 22),1) 


        #Realistically randomise Excise Duty
        if LIR < 40 and UR < 40:
            ExciseD = round(random.uniform(10, 40), 1)
        elif (LIR < 60 and UR < 40) or (LIR < 40 and UR < 60):
            ExciseD = round(random.uniform(8, 35), 1)
        elif (LIR < 80 and UR < 60) or (LIR < 60 and UR < 80):
            ExciseD = round(random.uniform(8, 25),1)
        elif LIR < 60 and UR < 60:
            ExciseD = round(random.uniform(8, 18), 1)
        else:
            ExciseD = round(random.uniform(5, 10), 1)


        #Realistically randomise National Insurance. Although pensioners don't pay national insurance on earnings, they may be unhappy about the levels due to their past incomes
        #   being used for the national insurance, so their unhappiness carries forward to when the user's economy loads.
        if HIR < 40 and PR < 40:
            NationalI = round(random.uniform(10, 25), 1)
        elif (HIR < 60 and PR < 40) or (HIR < 40 and PR < 60):
            NationalI = round(random.uniform(8, 20), 1)
        elif (HIR < 60 and PR < 80) or (HIR < 80 and PR < 60):
            NationalI = round(random.uniform(8, 15),1)
        elif HIR < 80 and PR < 80:
            NationalI = round(random.uniform(8, 12),1)
        elif HIR < 60 and PR < 60:
            NationalI = round(random.uniform(6, 12), 1)
        else:
            NationalI = round(random.uniform(3, 8), 1)


        #Realistically randomise Corporation Tax
        if HIR < 40 and BR < 40:
            CorpT = round(random.uniform(5, 40), 1)
        elif (HIR < 60 and BR < 40) or (HIR < 40 and BR < 60):
            CorpT = round(random.uniform(10, 25), 1)
        elif HIR < 60 and BR < 60:
            CorpT = round(random.uniform(8, 17), 1)
        elif (HIR < 60 and BR < 80) or (HIR < 80 or BR < 60):
            CorpT = round(random.uniform(8, 20),1)
        else:
            CorpT = round(random.uniform(5, 17), 1)

        

        #Realistically randomise VAT
        if LIR < 40 and MIR < 60:
            VAT = round(random.uniform(15, 30),1)
        elif (LIR < 80 and MIR < 60) or (LIR < 60 and MIR < 80):
            VAT = round(random.uniform(10, 25),1)
        elif LIR < 60 and MIR < 60:
            VAT = round(random.uniform(10, 20),1)
        else:
            VAT = round(random.uniform(5, 18),1)
            


        #Realistically randomise Carbon Tax
        if BR < 40 and PR < 40:
            CarbonT = round(random.uniform(10, 20),1)
        elif (BR < 60 and PR < 40) or (BR < 40 and PR < 60):
            CarbonT = round(random.uniform(5, 15),1)
        elif BR < 60 and PR < 60:
            CarbonT = round(random.uniform(5, 8),1)
        elif (BR < 80 and PR < 60) or (BR < 60 and PR < 80):
            CarbonT = round(random.uniform(5, 10),1)
        else:
            CarbonT = round(random.uniform(2, 8),1)
            
            
            
            
        print(IncomeT, ExciseD, NationalI, CorpT, VAT, CarbonT)

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addtaxes = ("INSERT INTO FiscalTaxes(TaxesID, IncomeTax, ExciseDuty, NationalInsurance, CorporationTax, VAT, CarbonTax) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        taxestoadd = (self.UserID, IncomeT, ExciseD, NationalI, CorpT, VAT, CarbonT)
        mycursor.execute(addtaxes, taxestoadd)
        economygamedb.commit()



    def RandomiseFiscalSpending(self):

        
        getratings = LE.Load(self.UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings()

        ND, CA, UR, InfRate, GDP, Year = getratings.LoadStatistics()

            

        spendingpercentage = round(random.uniform(0.35, 0.6),1)  #Randomise the maximum that total governement fiscal spending as a % of GDP could be (won't exceed GDP, but might with SSPs)
        spendingvalue = GDP * spendingpercentage    #Calculate the maximum spending value from spendingpercentage
        spendingleft = spendingvalue    #Set the remaining spending to start at the total maximum spendning value
        print("GDP = ", GDP, " SpendingLeft ", spendingleft)


        #The order randomised in this is determined on the UK's actual spending. It tends to spend the most money on the policies from top (most) to bottom (lowest)
        #Therefore those at the top take higher priority so are determined first

        #Randomise Social Protection Spending
        if PR > 80 and UR > 80:
            SocialProt = round(random.uniform(spendingleft*0.2, spendingleft*0.8))
        elif (PR > 80 and UR > 60) or (PR > 60 and UR > 80):
            SocialProt = round(random.uniform(spendingleft*0.2, spendingleft*0.6))
        else:
            SocialProt = round(random.uniform(spendingleft*0.2, spendingleft*0.5))

        print("Social ", SocialProt)


        spendingleft = spendingleft - SocialProt    #Recalculate  the remaining spending


        #Randomise Health Spending
        if LIR > 60 and MIR > 60 and HIR > 60 and PR > 60:
            HealthS = round(random.uniform(spendingleft*0.2, spendingleft*0.8))
        elif (LIR>40 and MIR>60 and HIR>60 and PR>60) or (LIR>60 and MIR>40 and HIR>60 and PR>60) or (LIR>60 and MIR>60 and HIR>40 and PR>60) or (LIR>60 and MIR>60 and HIR>60 and PR>40):
            HealthS = round(random.uniform(spendingleft*0.2, spendingleft*0.6))
        else:
            HealthS = round(random.uniform(spendingleft*0.2, spendingleft*0.5))

        print("Health ", HealthS)


        spendingleft = spendingleft - HealthS



        #Randomise Education Spending
        if HIR > 60 and PR > 60:
            EducationS = round(random.uniform(spendingleft*0.2, spendingleft*0.8))
        elif (HIR > 40 and PR > 60) or (HIR > 60 or PR > 40):
            EducationS = round(random.uniform(spendingleft*0.2, spendingleft*0.6))
        else:
            EducationS = round(random.uniform(spendingleft*0.2, spendingleft*0.5))

        print("Education ", EducationS)


        spendingleft = spendingleft - HealthS



        #Randomise Defence Spending
        if ND > 80:
            DefenceS = round(random.uniform(spendingleft*0.2, spendingleft))
        elif ND > 60:
            DefenceS = round(random.uniform(spendingleft*0.2, spendingleft*0.8))
        elif ND > 40:
            DefenceS = round(random.uniform(spendingleft*0.2, spendingleft*0.6))
        else:
            DefenceS = round(random.uniform(spendingleft*0.2, spendingleft*0.5))

        print("Defence ", DefenceS)

        self.GovernmentSpending += SocialProt + HealthS + EducationS + DefenceS


        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addfiscalspending = ("INSERT INTO FiscalSpending(SpendingID, SocialProtection, Health, Education, Defence) VALUES (%s, %s, %s, %s, %s)")
        fiscalspendingtoadd = (self.UserID, SocialProt, HealthS, EducationS, DefenceS)
        mycursor.execute(addfiscalspending, fiscalspendingtoadd)
        economygamedb.commit()

        


    def RandomiseSSSpending(self):

        
        getratings = LE.Load(self.UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings()

        
        ND, CA, UR, InfRate, GDP, Year = getratings.LoadStatistics()

        
        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        calcspentsofar = """SELECT SUM(SocialProtection+Health+Education+Defence) FROM FiscalSpending WHERE SpendingID = %s"""  #Used the aggregate function SUM to calculate spending so far
        usethisID = self.UserID
        mycursor.execute(calcspentsofar, (usethisID,))
        spentsofar = round(mycursor.fetchall()[0][0])
        print(spentsofar, GDP)

        spendingleft = round((GDP - spentsofar),1)  #Calcualte the maximum spending left if all of GDP were to be spent by the government
        print("total amount left to spend on SSP: ", spendingleft)
        
        if spentsofar > GDP*0.7:
          spendingleft = round(random.uniform(GDP * 0.2, (spendingleft * 0.7)),1)  #This way the total spending by the government will never start greater than its GDP, but close.
          
          
        else:
          spendingleft = round(random.uniform(GDP * 0.3, (spendingleft * 0.8)),1)
          
          

        print(spendingleft)
                               

        #NOW RANDOMISE EACH SSP ETC... THEN INSERT THEM THEN LOAD THEM ETC...

        
        #The order they are randomised in is based off of the UK's actual stats and which one they spend most on (so the top have the highest priority)
        #Realistically randomise Public Sector Investment
        if UR < 40 and PR < 40:
          PubInv = round(random.uniform(spendingleft*0.2, spendingleft*0.3))
        elif (UR < 60 and PR < 40) or (UR < 40 and PR < 60):
          PubInv = round(random.uniform(spendingleft*0.2, spendingleft*0.4))
        elif UR < 60 and PR < 60:
          PubInv = round(random.uniform(spendingleft*0.2, spendingleft*0.5))
        else:
          PubInv = round(random.uniform(spendingleft*0.2, spendingleft*0.5))

        spendingleft = spendingleft - PubInv

        

        #Realistically randomise Welfare Benefits
        if UR < 40:
          WelfareB = round(random.uniform(spendingleft*0.2, spendingleft*0.3))
        elif UR < 60:
          WelfareB = round(random.uniform(spendingleft*0.2, spendingleft*0.4))
        elif UR < 80:
          WelfareB = round(random.uniform(spendingleft*0.2, spendingleft*0.5))
        else:
          WelfareB = round(random.uniform(spendingleft*0.2, spendingleft*0.6))


        spendingleft = spendingleft - WelfareB


        #Realistically randomise Vocational Training
        if UR < 45:
          VocationalT = round(random.uniform(spendingleft*0.2, spendingleft*0.4))
        elif UR < 70:
          VocationalT = round(random.uniform(spendingleft*0.2, spendingleft*0.5))
        else:
          VocationalT = round(random.uniform(spendingleft*0.2, spendingleft*0.6))
          



        spendingleft = spendingleft - VocationalT


        #Realistically randomise Council Housing
        if LIR < 40 and UR < 40:
          CouncilH = round(random.uniform(spendingleft*0.2, spendingleft*0.3))
        elif (LIR < 60 and UR < 40) or (LIR < 40 and UR < 60):
          CouncilH = round(random.uniform(spendingleft*0.2, spendingleft*0.4))
        elif LIR < 60 and UR < 60:
          CouncilH = round(random.uniform(spendingleft*0.2, spendingleft*0.5))
        else:
          CouncilH = round(random.uniform(spendingleft*0.2, spendingleft*0.6))




        print(PubInv, WelfareB, VocationalT, CouncilH)

        self.GovernmentSpending += PubInv + WelfareB + VocationalT + CouncilH
        print(self.GovernmentSpending)
    
        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addsupplyside = ("INSERT INTO SupplySidePolicies(SupplySideID, PublicSectorInvestment, WelfareBenefits, VocationalTraining, CouncilHousing) VALUES (%s, %s, %s, %s, %s)")
        supplysidetoadd = (self.UserID, PubInv, WelfareB, VocationalT, CouncilH)
        mycursor.execute(addsupplyside, supplysidetoadd)
        economygamedb.commit()

            
    def RandomiseExtraStats(self):

        
        getvalues = LE.Load(self.UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getvalues.LoadRatings()

        
        ND, CA, UR, InfRate, GDP, Year = getvalues.LoadStatistics()


        InterestRate = getvalues.LoadInterestRates()

          #Realistically randomise Tax Revenue
        if HIR < 40 and MIR < 40:                             #Progressive tax therefore affects HIR and MIR more
            TaxRevenue = round(random.uniform(25, 35),1)
        elif (HIR < 40 and MIR < 60) or (HIR < 60 and MIR < 40):
            TaxRevenue = round(random.uniform(18, 25),1)
        elif HIR < 60 and MIR < 60:
            TaxRevenue = round(random.uniform(14, 18),1)
        else:
            TaxRevenue = round(random.uniform(5, 14),1)

        TaxRevenue = round((TaxRevenue/100 * GDP),1)

        print("Tax Revenue is ",TaxRevenue)




        #Realistically randomise median Disposable Income
        if HIR < 40 and MIR < 40 and LIR < 40:
          DisposableI = round(random.uniform(10, 23),1)
        elif (HIR < 60 and MIR < 40 and LIR < 40) or (HIR < 40 and MIR < 60 and LIR < 40):
          DisposableI = round(random.uniform(14, 25),1)
        elif HIR < 60 and MIR < 60:
          DisposableI = round(random.uniform(18, 30),1)
        elif (HIR < 80 and MIR < 60 and LIR < 60) or (HIR < 60 and MIR < 80 and LIR < 60):
          DisposableI = round(random.uniform(20, 32),1)
        elif HIR < 80 and MIR < 80:
          DisposableI = round(random.uniform(24, 36),1)
        else:
          DisposableI = round(random.uniform(25, 40),1)

        print("Mean Disposable Income ", DisposableI)
            


        #Realistically randomise Marginal Propensity To Consume (The proportion of extra income spent on consumption) Higher income normally means a higher MPC
        if InfRate > 3.5 and CA < -10:
          MPC = round(random.uniform(0.7,0.9),1)
        elif (InfRate > 2.8 and CA < -10) or (InfRate > 3.5 and CA < 0):
          MPC = round(random.uniform(0.5,0.7),2)
        else:
          MPC = round(random.uniform(0.2,0.6),2)

        print("MPC is ",MPC)



        #Realistically randomise Imports and Exports
        if CA < 0:
          if CA < -40 and MPC > 0.7:
            ImportsMultiplier = round(random.uniform(4, 5.5),1)
          elif (CA < -30 and MPC > 0.7) or (CA < -40 and MPC > 0.5):
            ImportsMultiplier = round(random.uniform(3, 5.5),1)
          elif (CA < -20 and MPC > 0.7) or (CA < -30 and MPC > 0.5):
            ImportsMultiplier = round(random.uniform(3, 4.8),1)
          elif (CA < -30 and MPC > 0.5) or (CA < -40 and MPC > 0.4):
            ImportsMultiplier = round(random.uniform(2.5, 4),1)
          elif CA < -30:
            ImportsMultiplier = round(random.uniform(2.5, 3.8),1)
          elif CA < -10:
            ImportsMultiplier = round(random.uniform(2.5, 3.2),1)
          else:
            ImportsMultiplier = round(random.uniform(2, 3),1)

          Imports = round((-CA * ImportsMultiplier),1)
          Exports = round((CA + Imports  ),1) #As Current Account = Exports - Imports
                
        else:
          if CA > 40 and MPC < 0.5:
            ExportsMultiplier = round(random.uniform(4, 5.5),1)
          elif (CA > 30 and MPC < 0.5) or (CA > 40 and MPC < 0.4):
            ExportsMultiplier = round(random.uniform(3, 5.5),1)
          elif (CA > 20 and MPC < 0.5) or (CA > 30 and MPC < 0.4):
            ExportsMultiplier = round(random.uniform(3, 4.8),1)
          elif CA > 30:
            ExportsMultiplier = round(random.uniform(2.5, 3.8),1)
          elif CA > 10:
            ExportsMultiplier = round(random.uniform(2.5, 3.2),1)
          else:
            ExportsMultiplier = round(random.uniform(2, 3),1)

          Exports = round((CA * ExportsMultiplier),1)
          Imports = round((Exports - CA),1)  #As Current Account = Exports - Imports
        
          
        print("Imports are ",Imports)
        print("Exports are ",Exports)




        
        #Randomise the Value of the Currency to the USD
        #In this simulation, it is assumed that the value of interest rates in the USA is 2.5%.s 
        if InterestRate > 90:   #Which is extremely unrealisitc, but the user can do this.
            CurrencyValue = round(random.uniform(0.1, 0.15),2)
        elif InterestRate > 75:
            CurrencyValue = round(random.uniform(0.15, 0.2),2)
        elif InterestRate > 60:
            CurrencyValue = round(random.uniform(0.2, 0.25),2)
        elif InterestRate > 50:
            CurrencyValue = round(random.uniform(0.25, 0.3),2)
        elif InterestRate > 40:
            CurrencyValue = round(random.uniform(0.3, 0.35),2)
        elif InterestRate > 30:
            CurrencyValue = round(random.uniform(0.35, 0.4),2)
        elif InterestRate > 15:
            CurrencyValue = round(random.uniform(0.4, 0.45),2)
        elif InterestRate > 13:
            CurrencyValue = round(random.uniform(0.45, 0.5),2)
        elif InterestRate > 11:
            CurrencyValue = round(random.uniform(0.5, 0.6),2)
        elif InterestRate > 9:
            CurrencyValue = round(random.uniform(0.6, 0.7),2)
        elif InterestRate > 7:
            CurrencyValue = round(random.uniform(0.7, 0.8),2)
        elif InterestRate > 5:
            CurrencyValue = round(random.uniform(0.8, 0.9),2)
        elif InterestRate > 2.5:
            CurrencyValue = round(random.uniform(0.9, 0.95),2)
        elif InterestRate == 2.5:
            CurrencyValue = round(random.uniform(0.95, 1.05),2)
        elif InterestRate == 0:
            CurrencyValue = round(random.uniform(2, 2.8),2)
        elif InterestRate < 0.2:
            CurrencyValue = round(random.uniform(1.9, 2),2)
        elif InterestRate < 0.3:
            CurrencyValue = round(random.uniform(1.8, 1.9),2)
        elif InterestRate < 0.4:
            CurrencyValue = round(random.uniform(1.7, 1.8),2)
        elif InterestRate < 0.45:
            CurrencyValue = round(random.uniform(1.6, 1.7),2)
        elif InterestRate < 0.5:
            CurrencyValue = round(random.uniform(1.5, 1.6),2)
        elif InterestRate < 0.75:
            CurrencyValue = round(random.uniform(1.45, 1.5),2)
        elif InterestRate < 1:
            CurrencyValue = round(random.uniform(1.4, 1.45),2)
        elif InterestRate < 1.25:
            CurrencyValue = round(random.uniform(1.35, 1.4),2)
        elif InterestRate < 1.5:
            CurrencyValue = round(random.uniform(1.3, 1.35),2)
        elif InterestRate < 1.75:
            CurrencyValue = round(random.uniform(1.25, 1.3),2)
        elif InterestRate < 2:
            CurrencyValue = round(random.uniform(1.2, 1.25),2)
        elif InterestRate < 2.25:
            CurrencyValue = round(random.uniform(1.15, 1.2),2)
        elif InterestRate < 2.5:
            CurrencyValue = round(random.uniform(1.05, 1.15),2)
            

        print("Currency Value is: ", CurrencyValue)
        
        BudgetBalance = TaxRevenue - self.GovernmentSpending
        print("Budget Balance is: ", BudgetBalance)

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addextrastats = ("INSERT INTO ExtraStatistics(ExtraStatsID, BudgetBalance, CurrencyValue, TaxRevenue, GovernmentSpending, DisposableIncome, MPC, Imports, Exports) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        extrastatstoadd = (self.UserID, BudgetBalance, CurrencyValue, TaxRevenue, self.GovernmentSpending, DisposableI, MPC, Imports, Exports)
        mycursor.execute(addextrastats, extrastatstoadd)
        economygamedb.commit()
            
                
                
        

        
    
        

        


class menu_main(LE.Load):
    def __init__(self, UserID):
        
        self.mainmenu_screen = Tk()
        self.width = 1920
        self.height = 1080
        self.mainmenu_screen.configure(bg = "light blue")
        self.mainmenu_screen.geometry("1920x1080")
        self.mainmenu_screen.title("Your Economy")
        
        self.UserID = UserID

        self.statistic_size = 213.33
        self.policy_size = 640
        
        
        self.whitebox = Label(self.mainmenu_screen, borderwidth = 2, relief = "solid",
                              bg = "white").place(x = 340, y = 345, width = 1255, height = 625) #The white box which the ratings are placed in
    
        self.display_other()


    def display_other(self):
        self.display_policies()
        self.display_simulate()
        self.display_exit()
        self.display_tutorial_option()
        self.displayAdditionalStatistics()

        self.GetRatings()
        self.GetStatistics()


    def GetRatings(self):

        
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = self.LoadRatings()    #Use the method LoadRatings that was inherited from its parent class Load

        

        HighIncomeText = Label(self.mainmenu_screen, text = ("High Income Earners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 400, y = 385, width = 380, height = 50)
        HighIncomePercentage = Label(self.mainmenu_screen, text = (round(HIR), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[HIR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 425, width = 380, height = 70)

        PensionersText = Label(self.mainmenu_screen, text = ("Pensioners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 1155, y = 385, width = 380, height = 50)
        PensionersPercentage = Label(self.mainmenu_screen, text = (round(PR), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[PR], font = ("Comic Sans", 12, "bold")).place(x = 1155, y = 425, width = 380, height = 70)
        
        MiddleIncomeText = Label(self.mainmenu_screen, text = ("Middle Income Earners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 400, y = 535, width = 380, height = 50)
        MiddleIncomePercentage = Label(self.mainmenu_screen, text = (round(MIR), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                             bg = ratings[MIR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 575, width = 380, height = 70)

        UnemployedText = Label(self.mainmenu_screen, text = ("Unemployed Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 1155, y = 535, width = 380, height = 50)
        UnemployedPercentage = Label(self.mainmenu_screen, text = (round(UR),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[UR], font = ("Comic Sans", 12, "bold")).place(x = 1155, y = 575, width = 380, height = 70)

        LowIncomeText = Label(self.mainmenu_screen, text = ("Low Income Earners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 400, y = 685, width = 380, height = 50)
        LowIncomePercentage = Label(self.mainmenu_screen, text = ((round(LIR)),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                          bg = ratings[LIR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 725, width = 380, height = 70)

        BusinessText = Label(self.mainmenu_screen, text = ("Business Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 1155, y = 685, width = 380, height = 50)            
        BusinessPercentage = Label(self.mainmenu_screen, text = ((round(BR)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                         bg = ratings[BR], font = ("Comic Sans", 12, "bold")).place(x = 1155, y = 725, width = 380, height = 70)

        OverallText = Label(self.mainmenu_screen, text = ("Overall Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 14, "bold")).place(x = 400, y = 835, width = 1135, height = 50)
        OverallPercentage = Label(self.mainmenu_screen, text = ((round(OR)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                        bg = ratings[OR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 875, width = 1135, height = 70)
        
        
    def GetStatistics(self):

        ND, CA, UR, InR, GDP, Year = self.LoadStatistics()    #Use the method LoadRatings that was inherited from its parent class Load
        
        

        NationalDebtText = Label(self.mainmenu_screen, text = "National Debt (% of GDP)", foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 10, "bold")).place(x=0, y=0, width = self.statistic_size, height = 25)
        NationalDebtFigure = Label(self.mainmenu_screen, text = (ND, "%"), foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 12, "bold")).place(x=0, y=25, width = self.statistic_size, height = 75)
        
        CurrentAccountText = Label(self.mainmenu_screen, text = "Current Account (£bn)", foreground = "black", borderwidth = 1, relief = "solid",
                                   bg = "grey", font = ("Comic Sans", 10, "bold")).place(x=self.statistic_size, y=0, width = self.statistic_size, height = 25)
        CurrentAccountFigure = Label(self.mainmenu_screen, text = ("£",CA), foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 12, "bold")).place(x=self.statistic_size, y=25, width = self.statistic_size, height = 75)
    
        UnemploymentRateText = Label(self.mainmenu_screen, text = "Unemployment Rate", foreground = "black", borderwidth = 1, relief = "solid",
                                     bg = "grey", font = ("Comic Sans", 10, "bold")).place(x=2*self.statistic_size, y=0, width = self.statistic_size, height = 25)
        UnemploymentRateFigure = Label(self.mainmenu_screen, text = (UR, "%"), foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 12, "bold")).place(x=2*self.statistic_size, y=25, width = self.statistic_size, height = 75)

        InflationRateText = Label(self.mainmenu_screen, text = "Inflation Rate (CPI)", foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 10, "bold")).place(x=3*self.statistic_size, y=0, width = self.statistic_size, height = 25)
        InflationRateFigure = Label(self.mainmenu_screen, text = (InR, "%"), foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 12, "bold")).place(x=3*self.statistic_size, y=25, width = self.statistic_size, height = 75) #No deflation in this

        GDPText = Label(self.mainmenu_screen, text = "GDP (£bn)", foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 10, "bold")).place(x=4*self.statistic_size, y=0, width = self.statistic_size, height = 25)
        GDPFigure = Label(self.mainmenu_screen, text = ("£", GDP), foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 12, "bold")).place(x=4*self.statistic_size, y=25, width = self.statistic_size, height = 75)

        YearText = Label(self.mainmenu_screen, text = "Year", foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 14, "bold")).place(x=5*self.statistic_size, y=0, width = (self.width-(5*self.statistic_size)+1), height = 25)
        YearFigure = Label(self.mainmenu_screen, text = Year, foreground = "black", borderwidth = 1, relief = "solid",
                             bg = "grey", font = ("Comic Sans", 20, "bold")).place(x=5*self.statistic_size, y=25, width = (self.width-(5*self.statistic_size)+1), height = 75)
                #The year wil be updated after every simulation button click or something similar





    def display_policies(self):
        
        #Create the policy labels and display them
        FiscalPolicy = Button(self.mainmenu_screen, text = "Fiscal Policy", command = lambda: TaxOrSpending(self.UserID),
                              foreground = "black", borderwidth = 2, relief = "sunken",
                              bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=0, y=100, width = self.policy_size, height = 175)
        
        MonetaryPolicy = Button(self.mainmenu_screen, text = "Monetary Policy", command = lambda: MonetarySelected.InterestRatesOr(self.UserID),
                             foreground = "black", borderwidth = 2, relief = "sunken", bg = "royal blue",
                             font = ("Comic Sans", 20, "bold")).place(x=self.policy_size, y=100, width = self.policy_size, height = 175)
        
        SupplySidePolicy = Button(self.mainmenu_screen, text = "Supply Side Policy", command = lambda: SSPSelected.SSPolicy(self.UserID),
                             foreground = "black", borderwidth = 2, relief = "sunken", bg = "royal blue",
                             font = ("Comic Sans", 20, "bold")).place(x=2*self.policy_size, y=100, width = self.policy_size, height = 175)

    def displayAdditionalStatistics(self):


        AdditionalStats1 = Button(self.mainmenu_screen, text = "Additional Statistics", command = lambda: self.AdditionalStats(),
                                 foreground = "black", borderwidth = 1, relief = "sunken",
                                 bg = "royal blue", font = ("Comic Sans", 12, "bold")).place(x=0, y=275, width = 250, height = 70)

        AdditionalStats2 = Button(self.mainmenu_screen, text = "Additional Statistics", command = lambda: self.AdditionalStats(),
                                 foreground = "black", borderwidth = 1, relief = "sunken",
                                 bg = "royal blue", font = ("Comic Sans", 12, "bold")).place(x=1670, y=275, width = 250, height = 70)

    def AdditionalStats(self):

        BudgetBalance, CurrencyValue, TaxRevenue, GovernmentSpending, DisposableIncome, MPC, Imports, Exports = self.LoadExtraStatistics()

        additionalstats_screen = Tk()
        additionalstats_screen.configure(bg = "white")
        additionalstats_screen.configure
        additionalstats_screen.geometry("1000x800+460+140") 
        additionalstats_screen.title("Additional Statistics About Your Economy")
        additionalstats_screen.resizable(False,False)

        BudgetBalanceLabel = Label(additionalstats_screen, text = "Budget Balance", foreground = "black", borderwidth = 1, relief = "sunken",
                                     bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=10, width = 700, height = 87.5)
        BudgetBalanceFigure = Label(additionalstats_screen, text = ("£"+str(BudgetBalance)+" billion"), foreground = "black", borderwidth = 1, relief = "sunken",
                                     bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=10, width = 280, height = 87.5)

        
        TaxRevenueLabel = Label(additionalstats_screen, text = "Total Tax Revenue", foreground = "black", borderwidth = 1, relief = "sunken",
                                 bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=107.5, width = 700, height = 87.5)
        TaxRevenueFigure = Label(additionalstats_screen, text = ("£"+str(TaxRevenue)+" billion"), foreground = "black", borderwidth = 1, relief = "sunken",
                                 bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=107.5, width = 280, height = 87.5)
        viewTaxRatesBarChart = Button(additionalstats_screen, text = "Tax Rates", foreground = "black", borderwidth = 4, relief = "solid", command = lambda: self.openTaxRatesBarChart(),
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=550, y=107.5, width = 120, height = 87.5)

        
        GovernmentSpendingLabel = Label(additionalstats_screen, text = "Total Government Spending", foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=205, width = 700, height = 87.5)
        GovernmentSpendingFigure = Label(additionalstats_screen, text = ("£"+str(GovernmentSpending)+" billion"), foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=205, width = 280, height = 87.5)
        #Give them the option to view all of their spending as a pie chart, which is extremely helpful if they want to change their spending but don't know where to.
        viewSpendingPieChart = Button(additionalstats_screen, text = "Pie Chart", foreground = "black", borderwidth = 4, relief = "solid", command = lambda: self.openSpendingPieChart(),
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=550, y=205, width = 120, height = 87.5)



        DisposableIncomeLabel = Label(additionalstats_screen, text = "Average Household Disposable Income", foreground = "black", borderwidth = 1, relief = "sunken",
                                       bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=302.5, width = 700, height = 87.5)
        DisposableIncomeFigure = Label(additionalstats_screen, text = ("£"+str(DisposableIncome)+" thousand"), foreground = "black", borderwidth = 1, relief = "sunken",
                                       bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=302.5, width = 280, height = 87.5)


        MPCLabel = Label(additionalstats_screen, text = "Marginal Propensity To Consume", foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=400, width = 700, height = 87.5)
        MPCFigure = Label(additionalstats_screen, text = MPC, foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=400, width = 280, height = 87.5)


        CurrencyValueLabel = Label(additionalstats_screen, text = "Exchange Rate £ : $", foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=497.5, width = 700, height = 87.5)
        CurrencyValueFigure = Label(additionalstats_screen, text = ("£" + str(CurrencyValue) + " : " + "$1"), foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=497.5, width = 280, height = 87.5)
        

        ImportsLabel = Label(additionalstats_screen, text = "Imports Value", foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=595, width = 700, height = 87.5)
        ImportsFigure = Label(additionalstats_screen, text = ("£"+str(Imports)+" billion"), foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=595, width = 280, height = 87.5)


        ExportsLabel = Label(additionalstats_screen, text = "Exports Value", foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=0, y=692.5, width = 700, height = 87.5)
        ExportsFigure = Label(additionalstats_screen, text = ("£"+str(Exports)+" billion"), foreground = "black", borderwidth = 1, relief = "sunken",
                                         bg = "white", font = ("Comic Sans", 12, "bold")).place(x=710, y=692.5, width = 280, height = 87.5)


    def openTaxRatesBarChart(self):

        barChart = Chart.Charts(self.UserID)
        barChart.B_TaxRates()

        

    def openSpendingPieChart(self):

        pieChart = Chart.Charts(self.UserID)
        pieChart.P_GovernmentSpending()
        

    def display_simulate(self):

        resetPoliciesConfirmed = Button(self.mainmenu_screen, text = """Reset
Policies Confirmed""",

                                        command = lambda: self.resetPoliciesConfirmed(),foreground = "black", borderwidth = 1, relief = "solid",
                                        bg = "royal blue", font = ("Comic Sans", 10, "bold")).place(x=875, y=300, width = 185, height = 45)

        
        
        SimulateButton = Button(self.mainmenu_screen, text = "Simulate Economy", command = lambda: self.SimulateEconomy(),
                                foreground = "black", borderwidth = 2, relief = "solid",
                                bg = "magenta", font = ("Comic Sans", 20, "bold")).place(x=800, y=560, width = 335, height = 100)


        #So that the policies to be changed can be viewed
        viewConfirmedButton = Button(self.mainmenu_screen, text = "Confirmed Policies", command = lambda: self.showPolicies(),
                                    foreground = "black", borderwidth = 2, relief = "solid",
                                    bg = "royal blue", font = ("Comic Sans", 12, "bold")).place(x=850, y=345, width = 235, height = 70)

        
    def resetPoliciesConfirmed(self):

        resetconfirmed = PRD.policies_everything(None, None, self.UserID)
        resetconfirmed.policy_screen.destroy()
        resetconfirmed.restorePoliciesConfirmed()

        

    def SimulateEconomy(self):
        policyfunctions = PRD.policies_everything(None, None, self.UserID)
        policyfunctions.policy_screen.destroy()
        simulateEconomy = Simulate.Simulate(self.UserID)
        policiesconfirmed, Q2Changes, Q3Changes, TimeLagged = simulateEconomy.SimulateClicked()

        policiesconfirmed_string = json.dumps(policiesconfirmed)
        Q2Changes_string = json.dumps(Q2Changes)    #Convert all three to string so that they can be updated in the database.
        Q3Changes_string = json.dumps(Q3Changes)
        TimeLagged_string = json.dumps(TimeLagged)

        

        print("Changes are: ", policiesconfirmed_string, " Q2 Changes are: ", Q2Changes_string, " Q3 Changes are: ", Q3Changes_string, " Time Lagged are: ", TimeLagged_string)

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        updatepoliciesconfirmed = ("""UPDATE PoliciesConfirmed SET Changes = %s,
                                                                Q2Changes = %s,
                                                                Q3Changes = %s,
                                                                TimeLagged = %s WHERE ConfirmedID = %s""")
        policiesconfirmedupdates = (policiesconfirmed_string, Q2Changes_string, Q3Changes_string, TimeLagged_string, self.UserID)
        mycursor.execute(updatepoliciesconfirmed, policiesconfirmedupdates)
        economygamedb.commit()

        FailedPolicies = simulateEconomy.AddToPriorityQueue()

        print("HAVE FAILED IS: ", FailedPolicies)

        #Display policies and statisstics by re-displaying them which will place them above themselves.
        self.GetStatistics()
        self.GetRatings()
        self.mainmenu_screen.update()


        #Inform the user if there were any failed policies
        if FailedPolicies:
                
            message = ("""The following
policies
failed to have
effect:
""" + str(FailedPolicies))
            informuser = OS.ExtraStatements(self.UserID)
            informuser.Notices(message, False, self.mainmenu_screen)
            

        

            
            

        #Then reset the policies as the policies confirmed will either be empty or full, but need to end up as empty.
        self.resetPoliciesConfirmed()


        election = Election(self.UserID, self.mainmenu_screen)
        election.ElectionTime()


        


        #Check whether it is time for another election and whether the user has any effects running, if they don't don't run the election.
        



         

    def showPolicies(self):

        policiesconfirmed = self.LoadPoliciesConfirmed()
        showPoliciesConfirmed = PRD.ReplaceOrRemovePolicy(self.UserID, policiesconfirmed, None, [])
        showPoliciesConfirmed.DisplayCurrentPolicies()


    def display_exit(self):
        #Create the exit button
        Exit = Button(self.mainmenu_screen, text = "Exit Game", command = lambda: self.quit_mainmenu(), foreground = "black", borderwidth = 2, relief = "solid",
                      bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=1680, y=900, width = 240, height = 150)

    def quit_mainmenu(self):
        choicetoquit = messagebox.askquestion(title = "But why :( ?", message = "Are you sure you want to quit?")
        if choicetoquit == "yes": #Quit the game and close the window
            quit()
        

    def display_tutorial_option(self):
        #Create the tutorial button

       
        
        Tutorial = Button(self.mainmenu_screen, text = "Tutorial", foreground = "black", borderwidth = 2,relief = "solid", command = lambda: self.RunTutorial(),
                      bg = "royal blue", font = ("Comic Sans", 18, "bold")).place(x=0, y=900, width = 240, height = 150)

    def RunTutorial(self):

        tutorial = TutorialGuide.Tutorial()
        tutorial.QuickIntro()

   
        

        

        



class Election(menu_main):

    def __init__(self, UserID, mainmenu_screen):

        self.mainmenu_screen = mainmenu_screen
        self.UserID = UserID
        self.OtherStatements = OS.ExtraStatements(self.UserID)
        self.difficultyselected = self.OtherStatements.getDifficulty()[0]
        print(self.difficultyselected)



        

    def ElectionTime(self):

        monthsdifference = self.OtherStatements.getDifferenceInMonths()
        

        

        if self.difficultyselected == 'Hard':
            electiontime = 12    #Only two years until the next election
        else:
            electiontime = 24   #Four years until the next election.


        print("Election time is: ", electiontime)

        if monthsdifference != 0:
            
            print(monthsdifference % electiontime)

            if monthsdifference % electiontime == 0:    #Then run the election to determine if the user is re-elected.

                print("ELECTION HAPPENING NOW")
                self.DetermineResults()




    def DetermineResults(self):


        #Load every statistic that will influence the result of the election.
        ratings, HighIncome, Pensioners, MiddleIncome, Unemployed, LowIncome, Businesses, Overall = self.LoadRatings()
        listofratings = [HighIncome, Pensioners, MiddleIncome, Unemployed, LowIncome, Businesses]
        NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year = self.LoadStatistics()
        BudgetBalance, CurrencyValue, TaxRevenue, GovernmentSpending, DisposableIncome, MPC, Imports, Exports = self.LoadExtraStatistics()
        LastElectionGDP, LastElectionNationalDebt = self.LoadPreviousGDP()

        #Calculate economic growth, which is one of the biggest determinants of how well an economy is doing.
        EconomicGrowth = ((GDP-LastElectionGDP)/(LastElectionGDP)) * 100
        NationalDebtChange = LastElectionNationalDebt - NationalDebt


        print(LastElectionGDP, NationalDebt, EconomicGrowth)



        totalScore = 0     #Set a start totalScore. If the result is less than 0 they are likely to lose the election


        #Change the totalScore based on the user economies overall rating from different groups in society.
        if Overall > 80:
            totalScore += 10
        elif Overall > 70:
            totalScore += 9
        elif Overall > 60:
            totalScore += 8
        elif Overall > 50:
            totalScore += 7
        elif Overall > 45:
            totalScore += 6
        elif Overall > 40:
            totalScore += 5
        elif Overall > 30:
            totalScore -= 5
        elif Overall > 25:
            totalScore -= 6
        elif Overall > 20:
            totalScore -= 7
        elif Overall > 10:
            totalScore -= 8
        else:
            totalScore -= 9


        #For every group in society, if they are unhappy then reduce the totalScore, but if they are happy increase the totalScore.
        #   This prevents the user from focussing on only a few groups to increase their overall rating and makes them focus on all groups, just how an economy would function/priorities
        #   its objectives.
        for rating in listofratings:
            if rating < 40:
                totalScore -= 4
            elif rating > 60:
                totalScore +=4



        print("After ratings total score is: ", totalScore)


        #If the current account is in a deficit, the totalScore should decrease.
        if CurrentAccount < 0:
            change = -1
        else:
            change = 1

        ModCurrentAccount = math.sqrt(CurrentAccount**2)
        print("ModCurrentAccount is: ", ModCurrentAccount)
        #If the modulus (squareroot of the value squared). Using this method, we don't need to use if statements for negative values as well, as the change generated above will
        #   be timesed by the amount totalscore will change by and the result will be added on. This way, the total score will decrease if in a deficit and increase if in a surplus.
        if ModCurrentAccount < 5:
            totalScore += change*1
        elif ModCurrentAccount < 10:
            totalScore += change*4
        elif ModCurrentAccount < 15:
            totalScore += change*6
        elif ModCurrentAccount < 20:
            totalScore += change*8
        elif ModCurrentAccount < 25:
            totalScore += change*10
        elif ModCurrentAccount < 30:
            totalScore += change*12
        elif ModCurrentAccount < 35:
            totalScore += change*15
        elif ModCurrentAccount < 40:
            totalScore += change*18
        elif ModCurrentAccount < 45:
            totalScore += change*20
        elif ModCurrentAccount < 50:
            totalScore += change*23
        elif ModCurrentAccount < 60:
            totalScore += change*25
        elif ModCurrentAccount < 70:
            totalScore += change*28
        elif ModCurrentAccount < 80:
            totalScore += change*30
        elif ModCurrentAccount < 90:
            totalScore += change*32
        elif ModCurrentAccount < 100:
            totalScore += change*35
        else:
            totalScore += change*38

        print("After Current Account total score is: ", totalScore)

        if UnemploymentRate < 1:
            totalScore += 8
        elif UnemploymentRate < 1.5:
            totalScore += 7
        elif UnemploymentRate < 2:
            totalScore += 6
        elif UnemploymentRate < 2.5:
            totalScore += 5
        elif UnemploymentRate < 3:
            totalScore += 4
        elif UnemploymentRate < 4:
            totalScore -= 3
        elif UnemploymentRate < 4.5:
            totalScore -= 4
        elif UnemploymentRate < 5:
            totalScore -= 5
        elif UnemploymentRate < 5.5:
            totalScore -= 6
        elif UnemploymentRate < 6:
            totalScore -= 7
        elif UnemploymentRate < 7:
            totalScore -= 8
        elif UnemploymentRate < 8:
            totalScore -= 9
        elif UnemploymentRate < 9:
            totalScore -= 10
        elif UnemploymentRate < 10:
            totalScore -= 11
        else:
            totalScore -= 12

        print("After UnemploymentRate totalScore is: ", totalScore)



        if 1.9 < InflationRate < 2.1:   #The target for inflation in the UK is 2 +- 1%.
            totalScore += 10
        elif 1.8 < InflationRate < 2.2:
            totalScore += 9
        elif 1.7 < InflationRate < 2.3:
            totalScore += 8
        elif 1.6 < InflationRate < 2.4:
            totalScore += 7
        elif 1.5 < InflationRate < 2.5:
            totalScore += 6
        elif 1.4 < InflationRate < 2.6:
            totalScore += 5
        elif 1.3 < InflationRate < 2.7:
            totalScore += 4
        elif 1.2 < InflationRate < 2.8:
            totalScore += 3
        elif 1.1 < InflationRate < 2.9:
            totalScore += 2
        elif 1 < InflationRate < 3:
            totalScore += 1
        elif 0.9 < InflationRate < 3.1:
            totalScore -= 1
        elif 0.8 < InflationRate < 3.4:
            totalScore -= 2
        elif 0.7 < InflationRate < 3.7:
            totalScore -= 3
        elif 0.6 < InflationRate < 4:
            totalScore -= 4
        elif 0.5 < InflationRate < 4.3:
            totalScore -= 5
        elif 0.4 < InflationRate < 4.6:
            totalScore -= 6
        elif 0.3 < InflationRate < 4.9:
            totalScore -= 7
        elif 0.2 < InflationRate < 5.2:
            totalScore -= 8
        elif 0.1 < InflationRate < 5.5:
            totalScore -= 9
        elif 0 < InflationRate < 5.8:
            totalScore -= 10
        else:
            totalScore -= 11

        print("After Inflation total score is: ", totalScore)
            

        if NationalDebt > 300:
            totalScore -= 50
        elif NationalDebt > 250:
            totalScore -= 45
        elif NationalDebt > 200:
            totalScore -= 40
        elif NationalDebt > 180:
            totalScore -= 30
        elif NationalDebt > 150:
            totalScore -= 25
        elif NationalDebt > 120:
            totalScore -= 20
        elif NationalDebt > 100:
            totalScore -= 12
        elif NationalDebt > 90:
            totalScore -= 10
        elif NationalDebt > 80:
            totalScore -= 9
        elif NationalDebt > 70:
            totalScore -= 8
        elif NationalDebt > 60:
            totalScore -= 7

        #Again use the modulus function, but this time with the NationalDebtChange.
        if NationalDebtChange < 0:  #Lower national debt is better for the economy and the chances of getting re-elected.
            change = -1
        else:
            change = 1

        ModNationalDebtChange = math.sqrt(NationalDebtChange**2)
        print("National Debt Change is: ", NationalDebtChange, " so change is: ", change)
        if ModNationalDebtChange < 3:
            totalScore += change*1
        elif ModNationalDebtChange < 5:
            totalScore += change*5
        elif ModNationalDebtChange < 7:
            totalScore += change*9
        elif ModNationalDebtChange < 9:
            totalScore += change*13
        elif ModNationalDebtChange < 12:
            totalScore += change*17
        elif ModNationalDebtChange < 15:
            totalScore += change*21
        elif ModNationalDebtChange < 18:
            totalScore += change*25
        elif ModNationalDebtChange < 20:
            totalScore += change*29
        elif ModNationalDebtChange < 24:
            totalScore += change*32
        elif ModNationalDebtChange < 30:
            totalScore += change*35
        else:
            totalScore += change*40



        print("After NationalDebt total score is: ", totalScore)


        #Again use the modulus function, but this time with the BudgetBalance.
        if BudgetBalance < 0:
            change = -1
        else:
            change = 1

        ModBudgetBalance = math.sqrt(BudgetBalance**2)
        if ModBudgetBalance > 80:
            totalScore += 14
        elif ModBudgetBalance > 70:
            totalScore += 12
        elif ModBudgetBalance > 60:
            totalScore += 10
        elif ModBudgetBalance > 50:
            totalScore += 8
        elif ModBudgetBalance > 40:
            totalScore += 6
        elif ModBudgetBalance > 30:
            totalScore += 5
        elif ModBudgetBalance > 20:
            totalScore += 4


        print("After Budget Balance total score is: ", totalScore)

        
        #Finally use economic growth to determine the final changes to totalScore.
        #Again the modulus function will be used to reduce the number of if statements.

        if EconomicGrowth > 0:
            change = 1
        else:
            change = -1

        ModEconomicGrowth = math.sqrt(EconomicGrowth**2)
        #Too high economic growth is bad for an economy.
        if ModEconomicGrowth > 15:  
            totalScore -= 20
        elif ModEconomicGrowth > 12:
            totalScore -= 18
        elif ModEconomicGrowth > 10:
            totalScore -= 16
        elif ModEconomicGrowth > 8:
            totalScore -= 15
        #However small consistant amounts of economic growth are good for an economy.
        elif ModEconomicGrowth > 6:
            totalScore += change*14
        elif ModEconomicGrowth > 5.5:
            totalScore += change*13
        elif ModEconomicGrowth > 5:
            totalScore += change*12
        elif ModEconomicGrowth > 4.5:
            totalScore += change*11
        elif ModEconomicGrowth > 4:
            totalScore += change*10
        elif ModEconomicGrowth > 3.5:
            totalScore += change*9
        elif ModEconomicGrowth > 3:
            totalScore += change*8
        elif ModEconomicGrowth > 2.5:
            totalScore += change*7
        elif ModEconomicGrowth > 2:
            totalScore += change*6
        elif ModEconomicGrowth > 1:
            totalScore += change*5



        print("After Economic Growth total score is: ", totalScore)



        print("Final Total Score Is: ", totalScore)
        
        
        self.RunElection(totalScore)



    def RunElection(self, Score):

        comparedScore = -100    #Initial starting point for compared score
        upperbound = 1          #Initial starting point for the uppder bound used in randomising the final result used for the election.
        losechance = 0.025           #Incase the Score is extremely high and does not lie within any of the if statements, winchance must have an actual value.

        for n in range(40): #More than this number of times just results in the winchance becoming 0, but there still needs to be a chance that they don't with the election, so winchance
                            #   is set to 0.025. Scores on 95 or more result in winchance being 0.025.
            print(n)
            if Score < comparedScore:
                losechance = upperbound - (n*losechance)
                #Stop the loop so that the value does not change anymoer
                break
            else:
                comparedScore = comparedScore + 5


        if self.difficultyselected == "Easy":
            losechance = losechance * 0.9     #Reduces the value by more for difficulty easy.
            
        

        print("final losechance is: ", losechance)


        MinimumToLose = random.uniform(0, 1)

        print("chance of losing is: ", MinimumToLose)

        monthsInCharge = str(self.OtherStatements.getDifferenceInMonths())
        
        if losechance > MinimumToLose:  #The user loses the election and the simulator ends.
            print("User has lost the election, with ChanceOfLosing being: ", MinimumToLose, " and winchance being: ", losechance)
            self.EndSimulator()
            message = ("""You have lost the Election: You were
responsible for your economy for:  """ + str(monthsInCharge) + """ months.
    If you would like to play again, simply login
    with your details... Thank you for playing""")
                       
            self.OtherStatements.Notices(message, True, self.mainmenu_screen)

            print("winchance: ", losechance, " is greater than ChanceOfLosing: ", MinimumToLose, " therefore the User has lost the election")

        else:

            print("winchance: ", losechance, " is less than ChanceOfLosing: ", MinimumToLose, " therefore the User has won the election")

            economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
            mycursor = economygamedb.cursor()

            NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year = self.LoadStatistics()

            updatelastelection = """UPDATE GDPStatistics SET LastElectionGDP = %s,
                                                             LastElectionNationalDebt = %s WHERE GDPID = %s"""
            usethese = (GDP, NationalDebt, self.UserID)

            mycursor.execute(updatelastelection, usethese)
            economygamedb.commit()

            message = ("""You have won the latest election: You have
been in charge for """ + str(monthsInCharge) + """ months now!
    Keep up the good work!""")
                       
            self.OtherStatements.Notices(message, False, self.mainmenu_screen)
                


    def EndSimulator(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
        resetratings = "DELETE FROM Ratings WHERE RatingsID = (%s)"            
        resetstatistics = "DELETE FROM Statistics WHERE StatsID = (%s)"        
        resetextrastatistics = "DELETE FROM ExtraStatistics WHERE ExtraStatsID = (%s)"
        resetfiscaltaxes = "DELETE FROM  FiscalTaxes WHERE TaxesID = (%s)"
        resetfiscalspending = "DELETE FROM FiscalSpending WHERE SpendingID = (%s)"
        resetmonetarypolicies = "DELETE FROM MonetaryPolicies WHERE MonetaryID = (%s)"
        resetsupplysidepolicies = "DELETE FROM SupplySidePolicies WHERE SupplySideID = (%s)"
        resetpoliciesconfirmed = "DELETE FROM PoliciesConfirmed WHERE ConfirmedID = (%s)"
        resetgdpstatistics = "DELETE FROM GDPStatistics WHERE GDPID = (%s)"
        resetdifficulty = """UPDATE Users SET Difficulty = NULL,
                                                NewGame = 1 WHERE UserID = (%s)"""    
        mycursor.execute(resetratings, (self.UserID,))
        mycursor.execute(resetstatistics, (self.UserID,))
        mycursor.execute(resetextrastatistics, (self.UserID,))
        mycursor.execute(resetfiscaltaxes, (self.UserID,))
        mycursor.execute(resetfiscalspending, (self.UserID,))
        mycursor.execute(resetmonetarypolicies, (self.UserID,))
        mycursor.execute(resetsupplysidepolicies, (self.UserID,))
        mycursor.execute(resetpoliciesconfirmed, (self.UserID,))
        mycursor.execute(resetgdpstatistics, (self.UserID,))
        mycursor.execute(resetdifficulty, (self.UserID,))
        #mycursor.execute("SET FOREIGN_KEY_CHECKS=1")
        economygamedb.commit()

        
if __name__ == "__main__":
    #UserID = 1
    #Economy = Election(1, Tk())
    #Economy.RunElection(-100)
    rungame = NewOrContinue(UserID, False)#UserID
    rungame.check()     #Login screen will take them to CheckForNewGame class
