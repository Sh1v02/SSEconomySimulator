import mysql.connector

class letssee():

    def __init__(self):
        
        self.UserID = 1
        
    def LoadRatings(self, HighIncomeRating, PensionersRating, MiddleIncomeRating, UnemployedRating, LowIncomeRating, BusinessRating, OverallRating):
        print("loading ratings")

        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="Sonal_321",database="economygame")
        mycursor = economygamedb.cursor()

        mycursor.execute("SELECT HighIncome FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        HighIncomeRating = mycursor.fetchone()[0]
        

        mycursor.execute("SELECT MiddleIncome FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        MiddleIncomeRating = mycursor.fetchone()[0]

        mycursor.execute("SELECT LowIncome FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        LowIncomeRating = mycursor.fetchone()[0]

        mycursor.execute("SELECT Pensioners FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        PensionersRating = mycursor.fetchone()[0]

        mycursor.execute("SELECT Unemployed FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        UnemployedRating = mycursor.fetchone()[0]

        mycursor.execute("SELECT Businesses FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        BusinessRating = mycursor.fetchone()[0]

        mycursor.execute("SELECT Overall FROM Ratings WHERE RatingsID = %s"%(self.UserID))
        OverallRating = mycursor.fetchone()[0]


        #ADD A SEPARATE FUNCTION SO THAT THIS CAN BE CALLED SO ITS NOT REPEATED
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


        ratings = {HighIncomeRating : HighIncomeColour,
                         PensionersRating : PensionersColour,
                         MiddleIncomeRating : MiddleIncomeColour,
                         UnemployedRating : UnemployedColour,
                         LowIncomeRating : LowIncomeColour,
                         BusinessRating : BusinessColour,
                         OverallRating : OverallColour}
        print(ratings)
        
        
        
        return ratings, HighIncomeRating, PensionersRating, MiddleIncomeRating, UnemployedRating, LowIncomeRating, BusinessRating, OverallRating
        

def main():
    HI, PR = None, None
   
  
    MI = None
    U = None
    LI = None
    B = None
    O = None
    test = letssee()
    ratings, HI, PR, MI, U, LI, B, O = test.LoadRatings(HI, PR, MI, U, LI, B, O)
    print(HI)
    
    print("these are the ratings returned" , ratings[HI])

main()
