import sys
import random

import mysql.connector





sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases") #Load_Everything
import Load_Everything as LE


class Randomise():

  def __init__(self):
      self.UserID = 1




def RandomiseSSSpending():
      UserID = 1
      HIR, PR, MIR, UR, LIR, BR, OR = None, None, None, None, None, None, None
      getratings = LE.Load(UserID)   #Load the users ratings and stats to determine a realistic Interest Rate
      ratings, HIR, PR, MIR, UR, LIR, BR, OR = getratings.LoadRatings(HIR, PR, MIR, UR, LIR, BR, OR)

      ND, CA, UR, InfRate, GDP, Year = None, None, None, None, None, None #Set all to none first so that I can pass them through
      ND, CA, UR, InfRate, GDP, Year = getratings.LoadStatistics(ND, CA, UR, InfRate, GDP, Year)


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
        MPC = round(random.uniform(0.6,0.9),1)
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

        imports = -CA * ImportsMultiplier
        exports = round((CA + imports  ),1) #As Current Account = Exports - Imports
        
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

        exports = CA * ExportsMultiplier
        imports = round((exports - CA),1)  #As Current Account = Exports - Imports

      print("Current Account is ", CA)
      print("Imports are ",imports)
      print("Exports are ",exports)

          
        
        
        
          

      
        

      



RandomiseSSSpending()
        
