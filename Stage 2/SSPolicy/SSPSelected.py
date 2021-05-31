#New file: SSPSelected
from tkinter import *


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")    #Load_Everything
import Load_Everything as LE
import OtherStatements as OS


import PublicInvestment as PublicInvestment
import WelfareBenefits as WelfareBenefits
import VocationalTraining as VocationalTraining
import CouncilHousing as CouncilHousing




class SSPolicy():

    def __init__(self, UserID):

        self.ss_screen = Tk()
        self.ss_screen.configure(bg = "light grey")
        self.ss_screen.geometry("1000x800+460+140") 
        self.ss_screen.title("Supply Side Policy")
        self.ss_screen.resizable(False,False)
        self.UserID = UserID

        getSSPolicies = LE.Load(self.UserID)
        self.PubInv, self.WelfareB, self.VocationalT, self.CouncilH = getSSPolicies.LoadSSPolicies()

        giveGDP = OS.ExtraStatements(self.UserID)
        self.maximumslidervalue = giveGDP.getGDP()    
        self.displayall()


    def displayall(self):
        self.SSGuide()
        self.SSbackbutton()
        
        self.WelfareBenefits()
        self.PublicInvestment()
        self.VocationalTraining()
        self.CouncilHousing()


    def SSGuide(self):

        briefexplanation = """The Supply Side Policy is one of the governments most used policies.
They are used to increase productivity and efficiency in an economy, increasing output.
This will often lead to increased GDP, however they may fail to have any effect at all
and money may be wasted. Selecting a higher priority will reduce the chances of this
happening, however there will always be a time lag that comes with these policies.
The time lag in your economy is 3 quarters of a year, so take that into account
before you make any changes.
You have access to 4 different types of Supply Side Policies:
Public Sector Investment, Welfare Benefits, Vocational Training and Council Housing."""

        whiteguidebox = Label(self.ss_screen, text = briefexplanation,
                             foreground = "black", borderwidth = 2, relief = "solid",
                             bg = "white", font = ("Comic Sans", 12)).place(x=10, y=490, width = 980, height = 300)
        
        FiscalTitle = Label(self.ss_screen, text = "Supply Side Policy", foreground = "black", borderwidth = 2, relief = "solid",
                             bg = "white", font = ("Comic Sans", 20, "bold")).place(x=10, y=490, width = 980, height = 40)



    def SSbackbutton(self):

        SSbackbutton = Button(self.ss_screen, command = lambda: self.backbuttoncommand(), text = "Back", foreground = "black",
                                borderwidth = 2, relief = "solid", bg = "magenta", font = ("Comic Sans", 20, "bold")).place(x = 420, y = 195, width = 160, height = 100)
        
    def backbuttoncommand(self):

        self.ss_screen.destroy()    #As there is no chocie before being shown the policies, the screen is just destroyed and nothing else is opened (so they just go back to the main menu)







    #PUBLIC INVESTMENT
    def PublicInvestment(self):
        PublicInvestment = Button(self.ss_screen, text = "Public Investment", foreground = "black", command = lambda: self.OpenPublicInvestment(),
                                borderwidth = 2, relief = "solid", bg = "royal blue",
                                font = ("Comic Sans", 20, "bold")).place(x=10, y=10, width = 400, height = 150)
    def OpenPublicInvestment(self):
        choice = "Public Sector Investment"
        PublicInv = PublicInvestment.SSPublicInvestment(choice, self.UserID, self.PubInv, self.maximumslidervalue)
        self.ss_screen.destroy()
        

  

    #WELFARE BENEFITS
    def WelfareBenefits(self):

        WBenefits = Button(self.ss_screen, text = "Welfare Benefits", foreground = "black", command = lambda: self.OpenWelfareBenefits(),
                            borderwidth = 2, relief = "solid", bg = "royal blue",
                            font = ("Comic Sans", 20, "bold")).place(x=590, y=10, width = 400, height = 150)
    def OpenWelfareBenefits(self):
        choice = "Welfare Benefits"
        WelfB = WelfareBenefits.SSWelfareBenefits(choice, self.UserID, self.WelfareB, self.maximumslidervalue)
        self.ss_screen.destroy()

    

        

    #VOCATIONAL TRAINING
    def VocationalTraining(self):
        VocationalTraining = Button(self.ss_screen, text = "Vocational Training", foreground = "black", command = lambda: self.OpenVocationalTraining(),
                                   borderwidth = 2, relief = "solid", bg = "royal blue",
                                   font = ("Comic Sans", 20, "bold")).place(x=10, y=330, width = 400, height = 150)
    def OpenVocationalTraining(self):
        choice = "Vocational Training"
        VocT = VocationalTraining.SSVocationalTraining(choice, self.UserID, self.VocationalT, self.maximumslidervalue)
        self.ss_screen.destroy()
    
        



    #COUNCIL HOUSING
    def CouncilHousing(self):
        CouncilHousing = Button(self.ss_screen, text = "Council Housing", foreground = "black", command = lambda: self.OpenCouncilHousing(),
                                 borderwidth = 2, relief = "solid", bg = "royal blue",
                                 font = ("Comic Sans", 20, "bold")).place(x=590, y=330, width = 400, height = 150)
    def OpenCouncilHousing(self):
        choice = "Council Housing"
        CH = CouncilHousing.SSCouncilHousing(choice, self.UserID, self.CouncilH, self.maximumslidervalue)
        self.ss_screen.destroy()

#End of file: SSPSelected

    






if __name__ == "__main__":
    run = SSPolicy(1)
    run.displayall()
