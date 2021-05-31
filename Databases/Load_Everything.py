#New file: Load_Everything
import mysql.connector
import random
import json #Used in LoadPoliciesConfirmed to convert the string that has been selected into a dictionary so that key value pairs can be used to store the changed policies.

class Load():
    def __init__(self, UserID):
        self.UserID = UserID

    def LoadRatings(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT HighIncome FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        HighIncomeRating = (mycursor.fetchone()[0]*100)
        

        mycursor.execute("SELECT MiddleIncome FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        MiddleIncomeRating = (mycursor.fetchone()[0]*100)

        mycursor.execute("SELECT LowIncome FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        LowIncomeRating = (mycursor.fetchone()[0]*100)

        mycursor.execute("SELECT Pensioners FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        PensionersRating = (mycursor.fetchone()[0]*100)

        mycursor.execute("SELECT Unemployed FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        UnemployedRating = (mycursor.fetchone()[0]*100)

        mycursor.execute("SELECT Businesses FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        BusinessRating = (mycursor.fetchone()[0]*100)

        mycursor.execute("SELECT Overall FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        OverallRating = (mycursor.fetchone()[0]*100)


        #Determine what colour/ the value will be
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

        #Store ratings in a dictionary with the rating as the key and the colour as the value
        ratings = {HighIncomeRating : HighIncomeColour,
                         PensionersRating : PensionersColour,
                         MiddleIncomeRating : MiddleIncomeColour,
                         UnemployedRating : UnemployedColour,
                         LowIncomeRating : LowIncomeColour,
                         BusinessRating : BusinessColour,
                         OverallRating : OverallColour}
        
        
        
        #return ratings and all keys so that values can be accessed 
        return ratings, HighIncomeRating, PensionersRating, MiddleIncomeRating, UnemployedRating, LowIncomeRating, BusinessRating, OverallRating

    def LoadStatistics(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT NationalDebt FROM Statistics WHERE StatsID = %s"%(self.UserID))
        NationalDebt = mycursor.fetchone()[0]
        

        mycursor.execute("SELECT CurrentAccount FROM Statistics WHERE StatsID = %s"%(self.UserID))
        CurrentAccount = mycursor.fetchone()[0]

        mycursor.execute("SELECT UnemploymentRate FROM Statistics WHERE StatsID = %s"%(self.UserID))
        UnemploymentRate = mycursor.fetchone()[0]

        mycursor.execute("SELECT InflationRate FROM Statistics WHERE StatsID = %s"%(self.UserID))
        InflationRate = mycursor.fetchone()[0]

        mycursor.execute("SELECT GDP FROM Statistics WHERE StatsID = %s"%(self.UserID))
        GDP = mycursor.fetchone()[0]

        mycursor.execute("SELECT Year FROM Statistics WHERE StatsID = %s"%(self.UserID))
        Year = mycursor.fetchone()[0]

        return NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year

    def LoadInterestRates(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT InterestRate FROM MonetaryPolicies WHERE MonetaryID = %s"%(self.UserID))
        InterestRate = mycursor.fetchone()[0]

        return InterestRate




    def LoadFiscalTaxes(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT IncomeTax FROM FiscalTaxes WHERE TaxesID = %s"%(self.UserID))
        IncomeTax = mycursor.fetchone()[0]
        
        mycursor.execute("SELECT ExciseDuty FROM FiscalTaxes WHERE TaxesID = %s"%(self.UserID))
        ExciseDuty = mycursor.fetchone()[0]

        mycursor.execute("SELECT NationalInsurance FROM FiscalTaxes WHERE TaxesID = %s"%(self.UserID))
        NationalInsurance = mycursor.fetchone()[0]

        mycursor.execute("SELECT CorporationTax FROM FiscalTaxes WHERE TaxesID = %s"%(self.UserID))
        CorporationTax = mycursor.fetchone()[0]

        mycursor.execute("SELECT VAT FROM FiscalTaxes WHERE TaxesID = %s"%(self.UserID))
        VAT = mycursor.fetchone()[0]

        mycursor.execute("SELECT CarbonTax FROM FiscalTaxes WHERE TaxesID = %s"%(self.UserID))
        CarbonTax = mycursor.fetchone()[0]


        return IncomeTax, ExciseDuty, NationalInsurance, CorporationTax, VAT, CarbonTax



    def LoadFiscalSpending(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT SocialProtection FROM FiscalSpending WHERE SpendingID = %s"%(self.UserID))
        SocialProt = mycursor.fetchone()[0]

        mycursor.execute("SELECT Health FROM FiscalSpending WHERE SpendingID = %s"%(self.UserID))
        Health = mycursor.fetchone()[0]

        mycursor.execute("SELECT Education FROM FiscalSpending WHERE SpendingID = %s"%(self.UserID))
        Education = mycursor.fetchone()[0]

        mycursor.execute("SELECT Defence FROM FiscalSpending WHERE SpendingID = %s"%(self.UserID))
        Defence = mycursor.fetchone()[0]



        return SocialProt, Health, Education, Defence



    def LoadSSPolicies(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT PublicSectorInvestment FROM SupplySidePolicies WHERE SupplySideID = %s"%(self.UserID))
        PubInv = mycursor.fetchone()[0]

        mycursor.execute("SELECT WelfareBenefits FROM SupplySidePolicies WHERE SupplySideID = %s"%(self.UserID))
        WelfareB = mycursor.fetchone()[0]

        mycursor.execute("SELECT VocationalTraining FROM SupplySidePolicies WHERE SupplySideID = %s"%(self.UserID))
        VocationalT = mycursor.fetchone()[0]

        mycursor.execute("SELECT CouncilHousing FROM SupplySidePolicies WHERE SupplySideID = %s"%(self.UserID))
        CouncilH = mycursor.fetchone()[0]


        return PubInv, WelfareB, VocationalT, CouncilH


    def LoadExtraStatistics(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT BudgetBalance FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        BudgetBalance = mycursor.fetchone()[0]

        mycursor.execute("SELECT CurrencyValue FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        CurrencyValue = mycursor.fetchone()[0]

        mycursor.execute("SELECT TaxRevenue FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        TaxRevenue = mycursor.fetchone()[0]

        mycursor.execute("SELECT GovernmentSpending FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        GovernmentSpending = mycursor.fetchone()[0]

        mycursor.execute("SELECT DisposableIncome FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        DisposableIncome = mycursor.fetchone()[0]

        mycursor.execute("SELECT MPC FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        MPC = mycursor.fetchone()[0]

        mycursor.execute("SELECT Imports FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        Imports = mycursor.fetchone()[0]

        mycursor.execute("SELECT Exports FROM ExtraStatistics WHERE ExtraStatsID = %s"%(self.UserID))
        Exports = mycursor.fetchone()[0]


        return BudgetBalance, CurrencyValue, TaxRevenue, GovernmentSpending, DisposableIncome, MPC, Imports, Exports



    def LoadPreviousGDP(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT LastElectionGDP FROM GDPStatistics WHERE GDPID = %s"%(self.UserID))
        GDP = mycursor.fetchall()[0][0]

        mycursor.execute("SELECT LastElectionNationalDebt FROM GDPStatistics WHERE GDPID = %s"%(self.UserID))
        NationalDebt = mycursor.fetchall()[0][0]

        return GDP, NationalDebt

        

        
    def LoadPoliciesConfirmed(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT Changes FROM PoliciesConfirmed WHERE ConfirmedID = %s"%(self.UserID))
        policiesconfirmed_string = mycursor.fetchall()[0][0]

        policiesconfirmed = json.loads(policiesconfirmed_string)    #Convert the string dictionary into a dictionary to be manipulated on later



        
        return policiesconfirmed        #Return it as a dictionary.


    def LoadQ2PoliciesConfirmed(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT Q2Changes FROM PoliciesConfirmed WHERE ConfirmedID = %s"%(self.UserID))
        Q2policiesconfirmed_string = mycursor.fetchall()[0][0]

        Q2policiesconfirmed = json.loads(Q2policiesconfirmed_string)    #Convert the string dictionary into a dictionary to be manipulated on later


        return Q2policiesconfirmed


    def LoadQ3PoliciesConfirmed(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT Q3Changes FROM PoliciesConfirmed WHERE ConfirmedID = %s"%(self.UserID))
        Q3policiesconfirmed_string = mycursor.fetchall()[0][0]

        Q3policiesconfirmed = json.loads(Q3policiesconfirmed_string)    #Convert the string dictionary into a dictionary to be manipulated on later


        return Q3policiesconfirmed


    def LoadTimeLagged(self):

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT TimeLagged FROM PoliciesConfirmed WHERE ConfirmedID = %s"%(self.UserID))
        TimeLagged_string = mycursor.fetchall()[0][0]

        TimeLagged = json.loads(TimeLagged_string)

        


        return TimeLagged

#End of file: Load_Everything
        
        

        
        

        

        

        

        
            






if __name__ == "__main__":
    loadit = Load(1)
    #TimeLagged = loadit.LoadTimeLagged()
    #TimeLagged.append('Income Tax')
    print(loadit.LoadPreviousGDP())
        
