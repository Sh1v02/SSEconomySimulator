import mysql.connector

economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")

mycursor = economygamedb.cursor()



mycursor.execute("SET FOREIGN_KEY_CHECKS=0")
mycursor.execute("DROP TABLE IF EXISTS Users")
mycursor.execute("DROP TABLE IF EXISTS Ratings")
mycursor.execute("DROP TABLE IF EXISTS Statistics")
mycursor.execute("DROP TABLE IF EXISTS ExtraStatistics")
mycursor.execute("DROP TABLE IF EXISTS FiscalTaxes")
mycursor.execute("DROP TABLE IF EXISTS FiscalSpending")
mycursor.execute("DROP TABLE IF EXISTS MonetaryPolicies")
mycursor.execute("DROP TABLE IF EXISTS SupplySidePolicies")
mycursor.execute("DROP TABLE IF EXISTS ExtraStats")
mycursor.execute("DROP TABLE IF EXISTS GDPStatistics")
mycursor.execute("DROP TABLE IF EXISTS PoliciesConfirmed")



mycursor.execute("""CREATE TABLE IF NOT EXISTS Users (
               UserID int PRIMARY KEY AUTO_INCREMENT,
               Username VARCHAR(100),
               Difficulty VARCHAR(10),
               NewGame BOOLEAN,
               PHash1 int,
               PHash2 int)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS Statistics (
               StatsID int PRIMARY KEY, FOREIGN KEY(StatsID) REFERENCES Users(UserID),
               NationalDebt FLOAT,
               CurrentAccount FLOAT,
               UnemploymentRate FLOAT,
               InflationRate FLOAT,
               GDP FLOAT,
               Year date)
               """)  #Can make the primary key foreign as it is a one to one relationship, not many to many

mycursor.execute("""CREATE TABLE IF NOT EXISTS ExtraStatistics (
               ExtraStatsID int PRIMARY KEY, FOREIGN KEY(ExtraStatsID) REFERENCES Users(UserID),
               BudgetBalance FLOAT,
               CurrencyValue FLOAT,
               TaxRevenue FLOAT,
               GovernmentSpending FLOAT,
               DisposableIncome FLOAT,
               MPC FLOAT,
               Imports FLOAT,
               Exports FLOAT)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS Ratings (
               RatingsID int PRIMARY KEY, FOREIGN KEY(RatingsID) REFERENCES Users(UserID),
               HighIncome FLOAT,
               MiddleIncome FLOAT,
               LowIncome FLOAT,
               Pensioners FLOAT,
               Unemployed FLOAT,
               Businesses FLOAT,
               Overall FLOAT)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS FiscalTaxes (
               TaxesID int PRIMARY KEY, FOREIGN KEY(TaxesID) REFERENCES Users(UserID),
               IncomeTax FLOAT,
               ExciseDuty FLOAT,
               NationalInsurance FLOAT,
               CorporationTax FLOAT,
               VAT FLOAT,
               CarbonTax FLOAT)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS FiscalSpending (
               SpendingID int PRIMARY KEY, FOREIGN KEY(SpendingID) REFERENCES Users(UserID),
               SocialProtection FLOAT,
               Education FLOAT,
               Health FLOAT,
               Defence FLOAT)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS MonetaryPolicies (
               MonetaryID int PRIMARY KEY, FOREIGN KEY(MonetaryID) REFERENCES Users(UserID),
               InterestRate FLOAT)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS SupplySidePolicies (
               SupplySideID int PRIMARY KEY, FOREIGN KEY(SupplySideID) REFERENCES Users(UserID),
               PublicSectorInvestment FLOAT,
               WelfareBenefits FLOAT,
               VocationalTraining FLOAT,
               CouncilHousing FLOAT)
               """)

#One to many... One user can have many quarters
mycursor.execute("""CREATE TABLE IF NOT EXISTS GDPStatistics (
               GDPID int PRIMARY KEY, FOREIGN KEY(GDPID) REFERENCES Users(USERID),
               LastElectionGDP FLOAT,
               LastElectionNationalDebt FLOAT)
               """)

mycursor.execute("""CREATE TABLE IF NOT EXISTS PoliciesConfirmed (
               ConfirmedID int PRIMARY KEY, FOREIGN KEY(ConfirmedID) REFERENCES Users(UserID),
               Changes VARCHAR(200),
               Q2Changes VARCHAR(200),
               Q3Changes VARCHAR(200),
               TimeLagged VARCHAR(200))
               """)



#userid = 2
#checkfornewgame = "SELECT HighIncome FROM Ratings WHERE RatingsID = %s"% (userid)
#mycursor.execute(checkfornewgame)
#exists = mycursor.fetchall()
#print(exists)

#getGDP = "SELECT GDP FROM statistics WHERE StatsID = %s"%(4)
#usethis = 4
#mycursor.execute(getGDP)
#GDP = mycursor.fetchall()[0][0]
#print(GDP)


#mycursor.execute("SELECT HighIncome FROM Ratings WHERE RatingsID = %s"%(1))
#ratings = mycursor.fetchall()


#print(ratings)






#addstats = "INSERT INTO Statistics (StatsID, NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#statstoadd = (12,500, 400, 500, 400, 500, "2000-10-10")

#mycursor.execute("INSERT INTO Users(Username, PHash1, PHash2) VALUES ('Works', 30, 0)")
#mycursor.execute(addstats, statstoadd)

#mycursor.execute(addstats, statstoadd)

#delete = ("DELETE from Ratings where RatingsID = 2")
#mycursor.execute(delete)



#addthisnow = "UPDATE Statistics SET NationalDebt = %s WHERE StatsID = %s"           
#mycursor.execute(addthisnow, (500, UserID))




economygamedb.commit()
