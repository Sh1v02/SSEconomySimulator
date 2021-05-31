import sys

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2")
import Main_Menu as MainMenu

class Election(MainMenu.menu_main):

    def __init__(self, UserID, mainmenu_screen):

        self.mainmenu_screen = mainmenu_screen
        self.UserID = UserID
        self.OtherStatements = OS.ExtraStatements(self.UserID)
        self.difficultyselected = self.OtherStatements.getDifficulty()[0]
        print(self.difficultyselected)



        

    def ElectionTime(self):

        monthsdifference = self.OtherStatements.getDifferenceInMonths()
        

        

        if self.difficultyselected == 'Hard':
            electiontime = 12    #Only one year until the next election
        else:
            electiontime = 24   #Two years until the next election.


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
            totalScore += 5
        elif Overall > 70:
            totalScore += 4
        elif Overall > 60:
            totalScore += 3
        elif Overall > 50:
            totalScore += 2
        elif Overall > 45:
            totalScore += 1
        elif Overall > 40:
            totalScore += 0.4
        elif Overall > 30:
            totalScore -= 0.4
        elif Overall > 25:
            totalScore -= 1
        elif Overall > 20:
            totalScore -= 2
        elif Overall > 10:
            totalScore -= 3
        else:
            totalScore -= 4


        #For every group in society, if they are unhappy then reduce the totalScore, but if they are happy increase the totalScore.
        #   This prevents the user from focussing on only a few groups to increase their overall rating and makes them focus on all groups, just how an economy would function/priorities
        #   its objectives.
        for rating in listofratings:
            if rating < 40:
                totalScore -= 2
            elif rating > 60:
                totalScore +=2


        #If the current account is in a deficit, the totalScore should decrease.
        if CurrentAccount < 0:
            change = -1
        else:
            change = 1

        ModCurrentAccount = math.sqrt(CurrentAccount**2)
        #If the modulus (squareroot of the value squared). Using this method, we don't need to use if statements for negative values as well, as the change generated above will
        #   be timesed by the amount totalscore will change by and the result will be added on. This way, the total score will decrease if in a deficit and increase if in a surplus.
        if ModCurrentAccount > 10:
            totalScore += change*1
        elif ModCurrentAccount > 15:
            totalScore += change*1.5
        elif ModCurrentAccount > 20:
            totalScore += change*2
        elif ModCurrentAccount > 25:
            totalScore += change*2.5
        elif ModCurrentAccount > 30:
            totalScore += change*3
        elif ModCurrentAccount > 35:
            totalScore += change*3.5
        elif ModCurrentAccount > 40:
            totalScore += change*4
        elif ModCurrentAccount > 45:
            totalScore += change*4.5
        elif ModCurrentAccount > 50:
            totalScore += change*5


        if UnemploymentRate < 1:
            totalScore += 5
        elif UnemploymentRate < 1.5:
            totalScore += 4
        elif UnemploymentRate < 2:
            totalScore += 3
        elif UnemploymentRate < 2.5:
            totalScore += 2
        elif UnemploymentRate < 3:
            totalScore += 1
        elif UnemploymentRate < 4:
            totalScore -= 1
        elif UnemploymentRate < 4.5:
            totalScore -= 1.5
        elif UnemploymentRate < 5:
            totalScore -= 2
        elif UnemploymentRate < 5.5:
            totalScore -= 3
        elif UnemploymentRate < 6:
            totalScore -= 4
        elif UnemploymentRate < 7:
            totalScore -= 5
        elif UnemploymentRate < 8:
            totalScore -= 6
        elif UnemploymentRate < 9:
            totalScore -= 7
        elif UnemploymentRate < 10:
            totalScore -= 8
        else:
            totalScore -= 9



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
            change = 1
        else:
            change = -1

        ModNationalDebtChange = math.sqrt(NationalDebtChange**2)
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



        print("Total Score Is: ", totalScore)
        
        
        self.RunElection(totalScore)



    def RunElection(self, Score):

        comparedScore = -100    #Initial starting point for compared score
        upperbound = 1          #Initial starting point for the uppder bound used in randomising the final result used for the election.
        losechance = 0.025           #Incase the Score is extremely high and does not lie within any of the if statements, losechance must have an actual value.

        for n in range(40): #More than this number of times just results in the losechance becoming 0, but there still needs to be a chance that they don't with the election, so losechance
                            #   is set to 0.025. Scores on 95 or more result in losechance being 0.025.
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


        ChanceOfLosing = random.uniform(0, 1)

        print("chance of losing is: ", ChanceOfLosing)

        
        if losechance > ChanceOfLosing:  #The user loses the election and the simulator ends.
            print("User has lost the election, with ChanceOfLosing being: ", ChanceOfLosing, " and losechance being: ", losechance)
            self.EndSimulator()
            message = ("""You have lost the Election:
    If you would like to play again, simply login
    with your details... Thank you for playing""")
                       
            self.OtherStatements.Notices(message, True, self.mainmenu_screen)

            print("losechance: ", losechance, " is greater than ChanceOfLosing: ", ChanceOfLosing, " therefore the User has lost the election")

        else:

            print("losechance: ", losechance, " is less than ChanceOfLosing: ", ChanceOfLosing, " therefore the User has won the election")

            economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
            mycursor = economygamedb.cursor()

            NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year = self.LoadStatistics()

            updatelastelection = """UPDATE GDPStatistics SET LastElectionGDP = %s,
                                                             LastElectionNationalDebt = %s WHERE GDPID = %s"""
            usethese = (GDP, NationalDebt, self.UserID)

            mycursor.execute(updatelastelection, usethese)
            economygamedb.commit()

            message = ("""You have won the latest election:
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

        
