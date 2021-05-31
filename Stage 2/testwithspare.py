from tkinter import *
from tkinter import messagebox
import random
import mysql.connector
import sys





sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases") #Load_Everything
import Load_Everything as LE

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\FiscalPolicy") #FiscalSelected
from FiscalSelected import *

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\MonetaryPolicy")   #MonetarySelected
import MonetarySelected as MonetarySelected









class CheckForNewGame():

    def __init__(self, UserID):
        
        self.UserID = UserID

    def check(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        
        checkfornewgame = "SELECT RatingsID FROM Ratings WHERE EXISTS(SELECT * FROM Ratings WHERE RatingsID = %s)"%(self.UserID)
        mycursor.execute(checkfornewgame)
        exists = mycursor.fetchone()
        print(exists)
        if exists:
            print("USER DATA EXISTS")
            continuegame = menu_main(self.UserID)
            continuegame.GetRatings()
            continuegame.GetStatistics()
             
            
        else:
            print("there is no data")
            startnewgame = New_Game(self.UserID)
            startnewgame.RandomiseRatings() #MAYBE MAKE ANOTHER FUNCTION WHICH RUNS ALL OF THESE
            startnewgame.RandomiseStatistics()

            
            displayother = menu_main(self.UserID) #Will be UserID #THIS DOESNT WORK FIX THIS 
            displayother.GetStatistics()
            displayother.GetRatings()
        



class New_Game():

    def __init__(self, UserID):
        self.ratings = {}
        self.UserID = UserID 
        

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

        HIR, PR, MIR, UR, LIR, BR, OR = None, None, None, None, None, None, None
        getratings = LE.Load(self.UserID)
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings(HIR, PR, MIR, UR, LIR, BR, OR)
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
        if UR > 0.8:
            UnemploymentRate = round((random.uniform(2,6)),2)
        elif UR > 0.6:
            UnemploymentRate = round((random.uniform(4,8)),2)
        elif UR > 0.4:
            UnemploymentRate = round((random.uniform(4,10)),2)
        else:
            UnemploymentRate = round((random.uniform(6,14)),2)

        #Realistically randomise the Inflation Rate
        if PR and BR > 0.6:
            InflationRate = round((random.uniform(1.5,3.5)),2)
        elif PR and BR > 0.4:
            InflationRate = round((random.uniform(0.8,6)),2)
        else:
            InflationRate = round((random.uniform(0.1,10)),2)

        #Realistically randomise the GDP, a good representation of economic growth -- This is not Real GDP!
        if HIR and MIR and LIR > 0.8 and BR > 0.6:
            GDP = round((random.uniform(200, 400)),2) #Billion #MAYBE CHANGE TO TRILLION LATER
        elif HIR and MIR and LIR > 0.6 and BR > 0.6:
            GDP = round((random.uniform(100,280)),2)
        elif HIR and MIR and LIR > 0.4 and BR > 0.6:
            GDP = round((random.uniform(50,240)),2)
        elif HIR and MIR and LIR > 0.8 and BR > 0.4:
            GDP = round((random.uniform(100,280)),2)
        elif HIR and MIR and LIR > 0.6 and BR > 0.4:
            GDP = round((random.uniform(50,240)),2)
        elif HIR and MIR and LIR > 0.4 and BR > 0.4:
            GDP = round((random.uniform(50,180)),2)
        elif HIR and MIR and LIR > 0.6 and BR < 0.4:
            GDP = round((random.uniform(100, 240)),2)
        else:
            GDP = round((random.uniform(50,120)),2)

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
        statstoadd = (self.UserID, NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, '2019-04-04')
        mycursor.execute(addstats, statstoadd)
        economygamedb.commit()

        

    def RandomiseMonetaryPolicies(self):

#------------------------Interest Rates-----------------------------------------------------------------------------------------------------------------------------------#
        HIR, PR, MIR, UR, LIR, BR, OR = None, None, None, None, None, None, None
        getratings = LE.Load(self.UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings(HIR, PR, MIR, UR, LIR, BR, OR)
        #print(HIR, PR, MIR, UR, LIR, BR, OR)

        ND, CA, UR, InfR, GDP, Year = None, None, None, None, None, None #Set all to none first so that I can pass them through
        ND, CA, UR, InfR, GDP, Year = getratings.LoadStatistics(ND, CA, UR, InfR, GDP, Year)    #Use the method LoadRatings that was inherited from its parent class Load
        #print(ND, CA, UR, InfR, GDP, Year)


        #Realistically randomise Interest Rates
        if GDP < 120 and BR < 40 and HIR > 60:
            InterR = round((random.uniform(8, 25)),2)   #Will not allow interest rates to start higher than 25 as this is unrealistic, but the user can take them to 100%
        elif ((GDP < 180 and BR < 40) or (GDP < 120 and BR < 60)) and HIR > 60:
            InterR = round((random.uniform(6, 18)),2)
        elif GDP < 120 and BR < 40 and HIR > 40:
            InterR = round((random.uniform(3, 15)),2)
        elif GDP < 180 and BR < 60 and HIR > 40:
            InterR = round((random.uniform(3, 12)),2)
        else:
            InterR = round((random.uniform(0.5, 8)),2)

        print("Interest Rates are: ", InterR, " %")

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()
        addinterestrate = ("INSERT INTO MonetaryPolicies(MonetaryID, InterestRate) VALUES (%s, %s)")
        interestratetoadd = (self.UserID, InterR)
        mycursor.execute(addinterestrate, interestratetoadd)
        economygamedb.commit()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
        

        


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
        self.display_exit()
        self.display_tutorial_option()

    
        
    def display_policies(self):
        
        #Create the policy labels and display them
        FiscalPolicy = Button(self.mainmenu_screen, text = "Fiscal Policy", command = lambda: TaxOrSpending(), foreground = "black", borderwidth = 2, relief = "sunken",
                             bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=0, y=100, width = self.policy_size, height = 175)
        
        MonetaryPolicy = Button(self.mainmenu_screen, text = "Monetary Policy", command = lambda: MonetarySelected.InterestRatesOr(self.UserID), foreground = "black", borderwidth = 2, relief = "sunken",
                             bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=self.policy_size, y=100, width = self.policy_size, height = 175)
        
        SupplySidePolicy = Button(self.mainmenu_screen, text = "Supply Side Policy", foreground = "black", borderwidth = 2, relief = "sunken",
                             bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=2*self.policy_size, y=100, width = self.policy_size, height = 175)

    def GetRatings(self):

        HIR, PR, MIR, UR, LIR, BR, OR = None, None, None, None, None, None, None #Set all to none first so that I can pass them through
        ratings, HIR, PR, MIR, UR, LIR, BR, OR = self.LoadRatings(HIR, PR, MIR, UR, LIR, BR, OR)    #Use the method LoadRatings that was inherited from its parent class Load
            


        HighIncomeText = Label(self.mainmenu_screen, text = ("High Income Earners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 400, y = 385, width = 380, height = 50)
        HighIncomePercentage = Label(self.mainmenu_screen, text = (round(HIR*100), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[HIR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 425, width = 380, height = 70)

        PensionersText = Label(self.mainmenu_screen, text = ("Pensioners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 1155, y = 385, width = 380, height = 50)
        PensionersPercentage = Label(self.mainmenu_screen, text = (round(PR*100), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[PR], font = ("Comic Sans", 12, "bold")).place(x = 1155, y = 425, width = 380, height = 70)
        
        MiddleIncomeText = Label(self.mainmenu_screen, text = ("Middle Income Earners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 400, y = 535, width = 380, height = 50)
        MiddleIncomePercentage = Label(self.mainmenu_screen, text = (round(MIR*100), "%"), foreground = "white", borderwidth = 2, relief = "solid",
                             bg = ratings[MIR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 575, width = 380, height = 70)

        UnemployedText = Label(self.mainmenu_screen, text = ("Unemployed Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 1155, y = 535, width = 380, height = 50)
        UnemployedPercentage = Label(self.mainmenu_screen, text = (round(UR*100),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                           bg = ratings[UR], font = ("Comic Sans", 12, "bold")).place(x = 1155, y = 575, width = 380, height = 70)

        LowIncomeText = Label(self.mainmenu_screen, text = ("Low Income Earners Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 400, y = 685, width = 380, height = 50)
        LowIncomePercentage = Label(self.mainmenu_screen, text = ((round(LIR*100)),"%"), foreground = "white", borderwidth = 2, relief = "solid",
                          bg = ratings[LIR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 725, width = 380, height = 70)

        BusinessText = Label(self.mainmenu_screen, text = ("Businesses Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 10, "bold")).place(x = 1155, y = 685, width = 380, height = 50)            
        BusinessPercentage = Label(self.mainmenu_screen, text = ((round(BR*100)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                         bg = ratings[BR], font = ("Comic Sans", 12, "bold")).place(x = 1155, y = 725, width = 380, height = 70)

        OverallText = Label(self.mainmenu_screen, text = ("Overall Happiness"), foreground = "black",
                               bg = "white", font = ("Comic Sans", 14, "bold")).place(x = 400, y = 835, width = 1135, height = 50)
        OverallPercentage = Label(self.mainmenu_screen, text = ((round(OR*100)),"%"), foreground = "white",borderwidth = 2, relief = "solid",
                        bg = ratings[OR], font = ("Comic Sans", 12, "bold")).place(x = 400, y = 875, width = 1135, height = 70)
        
        
    def GetStatistics(self):

        ND, CA, UR, InR, GDP, Year = None, None, None, None, None, None #Set all to none first so that I can pass them through
        ND, CA, UR, InR, GDP, Year = self.LoadStatistics(ND, CA, UR, InR, GDP, Year)    #Use the method LoadRatings that was inherited from its parent class Load
        
        

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
        Tutorial = Button(self.mainmenu_screen, text = "Tutorial", foreground = "black", borderwidth = 2,relief = "solid",
                      bg = "royal blue", font = ("Comic Sans", 18, "bold")).place(x=0, y=900, width = 240, height = 150)



    



        
if __name__ == "__main__":
    UserID = 2
    rungame = CheckForNewGame(UserID)#UserID
    rungame.check()     #Login screen will take them to CheckForNewGame class
