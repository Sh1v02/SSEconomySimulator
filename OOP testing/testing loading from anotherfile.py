
import sys
sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
from Load_Everything import *

def main():
    HI,PR = None, None
   
    
    MI = None
    U = None
    LI = None
    B = None
    O = None
    test = Load(1)
    ratings, HI, PR, MI, U, LI, B, O = test.LoadRatings(HI, PR, MI, U, LI, B, O)
    print(HI)
    
    print("these are the ratings returned" , ratings[HI])

main()
