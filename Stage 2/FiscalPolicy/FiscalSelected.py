#New file: FiscalSelected
from tkinter import *
import mysql.connector



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\FiscalPolicy\Taxation")    #Add Taxation Folder to path
#import taxes
import IncomeTax as IncomeTax
import ExciseDuty as ExciseDuty
import NationalInsurance as NationalInsurance
import CorporationTax as CorporationTax
import VAT as VAT
import CarbonTax as CarbonTax


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 2\FiscalPolicy\Spending")     #Add Spending Folder to path
#import spending
import SocialProtection as SocialProtection
import Health as Health
import Education as Education
import Defence as Defence



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")    #Load_Everything
import Load_Everything as LE
import OtherStatements as OS



class TaxOrSpending():

    def __init__(self, UserID):

        self.which_screen = Tk()
        self.which_screen.configure(bg = "light grey")
        self.which_screen.geometry("420x330+750+250") 
        self.which_screen.title("Fiscal Policy - Please Select")
        self.which_screen.resizable(False,False)

        self.UserID = UserID

        self.taxbutton = Button(self.which_screen, command = lambda: taxationselected(self), text = "Taxation", foreground = "black",
                                borderwidth = 2, relief = "solid", bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=10, y=10, width = 400, height = 150)
        
        self.spendingbutton = Button(self.which_screen, command = lambda: spendingselected(self), text = "Spending", foreground = "black",
                                borderwidth = 2, relief = "solid", bg = "royal blue", font = ("Comic Sans", 20, "bold")).place(x=10, y=170, width = 400, height = 150)

        
        def taxationselected(self):
            choice = "Tax"
            self.which_screen.destroy()
            Fiscal_Taxation = FiscalPolicy(choice, self.UserID)
            
            

        def spendingselected(self):
            choice = "Spending"
            self.which_screen.destroy()
            Fiscal_Taxation = FiscalPolicy(choice, self.UserID)
            

        
            

            
class FiscalPolicy():
    
    def __init__(self, choice, UserID):
        self.fiscal_screen = Tk()
        self.fiscal_screen.configure(bg = "light grey")
        self.fiscal_screen.geometry("1000x800+460+140") 
        self.fiscal_screen.title("Fiscal Policy")
        self.fiscal_screen.resizable(False,False)
        self.UserID = UserID
        self.choice = choice
        
        
        self.fiscalbackbutton = Button(self.fiscal_screen, command = lambda: self.backbuttoncommand(), text = "Back", foreground = "black",
                                borderwidth = 2, relief = "solid", bg = "magenta", font = ("Comic Sans", 20, "bold")).place(x = 420, y = 195, width = 160, height = 100)
        
        
        if choice == "Tax":
            
            whichtype = "Taxation"
            self.maximumslidervalue = 100 #The maximum value the slider can go to for a tax is 100 (100%)
            self.DisplayTaxes()
            self.FiscalGuide(whichtype)
            
        else:
            
            whichtype = "Expenditure"

            #Max slider value can be will be the GDP (user will not be allowed to spend more than their GDP for one policy, but can spend a total worth more than their GDP)
            giveGDP = OS.ExtraStatements(self.UserID)
            self.maximumslidervalue = giveGDP.getGDP()
            print("maxslidervalue is: ", self.maximumslidervalue)

            
            self.DisplayExpenditure()
            self.FiscalGuide(whichtype)

        

        #Must get all tax values here so that they can be accessed when inherited by each individual fiscal tax
        
        getTaxes = LE.Load(self.UserID)
        self.IncomeT,self.ExciseD,self.NationalI,self.CorpT,self.VAT,self.CarbonT = getTaxes.LoadFiscalTaxes()

        
        getSpending = LE.Load(self.UserID)
        self.SocialProt, self.Health, self.Education, self.Defence = getSpending.LoadFiscalSpending()
        

    
    def DisplayTaxes(self):
        self.IncomeTax()
        self.CorporationTax()
        self.ExciseDuty()
        self.VAT()
        self.NationalInsurance()
        self.CarbonTax()

    def DisplayExpenditure(self):
        self.SPExpenditure()
        self.HealthExpenditure()
        self.EducationExpenditure()
        self.DefenceExpenditure()
        
        
    def FiscalGuide(self, whichtype):

        if whichtype == "Taxation":

            briefexplanation = """ The Fiscal Policy is a commonly used policy where the Government will control taxes
and government spending to control aggregate demand in the economy. There are several
different types of taxes that can be used. You have access to six of these:
Income Tax, Corporation Tax, Excise Duty, VAT, National Insurance and Carbon Tax.
You can use these to stimulate or decrease aggregate demand if you need. When
your Government is spending more than it is receiving through tax revenue, it is called a
budget deficit. When your Government is spending less than it is receiving through tax revenue,
it is called a budget surplus. Each pf these have their own advantages and disadvantages.
Use the above taxes to see how increasing or decreasing certain taxes will affect your economy!"""

        else:
            briefexplanation = """
The Fiscal Policy is a commonly used policy where the Government will control taxes
and government spending to control aggregate demand in the economy. There are several
different types of spending that can be controlled. You have access to four of these:
Social Protection, Health, Education and Defence.
You can use these to stimulate or decrease aggregate demand if you need. When
your Government is spending more than it is receiving through tax revenue, it is called a
budget deficit. When your Government is spending less than it is receiving through tax revenue,
it is called a budget surplus. Each pf these have their own advantages and disadvantages.
Use the above types of government spending to see how increasing or decreasing certain taxes will
affect your economy!"""

    
        whiteguidebox = Label(self.fiscal_screen, text = briefexplanation,
                             foreground = "black", borderwidth = 2, relief = "solid",
                             bg = "white", font = ("Comic Sans", 12)).place(x=10, y=490, width = 980, height = 300)
        
        FiscalTitle = Label(self.fiscal_screen, text = whichtype, foreground = "black", borderwidth = 2, relief = "solid",
                             bg = "white", font = ("Comic Sans", 20, "bold")).place(x=10, y=490, width = 980, height = 40)


    def backbuttoncommand(self):

        
        TaxOrSpending(self.UserID)
        self.fiscal_screen.destroy()
        
        

        
#-------------------------------------------Fiscal Tax Buttons--------------------------------------------------------------------#


    #INCOME TAX
    def IncomeTax(self):
        IncomeTax = Button(self.fiscal_screen, text = "Income Tax", foreground = "black", command = lambda: self.OpenIncomeTax(),
                           borderwidth = 2, relief = "solid",bg = "royal blue",
                           font = ("Comic Sans", 20, "bold")).place(x=10, y=10, width = 400, height = 150)
    def OpenIncomeTax(self):        
        choice = "Income Tax"
        incometax = IncomeTax.FiscalIncomeTax(choice, self.UserID, self.IncomeT, self.maximumslidervalue)
        self.fiscal_screen.destroy()

        
        
    #EXCISE DUTY
    def ExciseDuty(self):
        ExciseTax = Button(self.fiscal_screen, text = "Excise Duty", foreground = "black", command = lambda: self.OpenExciseDuty(),
                           borderwidth = 2, relief = "solid", bg = "royal blue",
                           font = ("Comic Sans", 20, "bold")).place(x=10, y=170, width = 400, height = 150)
    def OpenExciseDuty(self):
        choice = "Excise Duty"
        exciseduty = ExciseDuty.FiscalExciseDuty(choice, self.UserID, self.ExciseD, self.maximumslidervalue)
        self.fiscal_screen.destroy()




    #NATIONAL INSURANCE
    def NationalInsurance(self):
        NATax = Button(self.fiscal_screen, text = "National Insurance", foreground = "black", command = lambda: self.OpenNationalInsurance(),
                       borderwidth = 2, relief = "solid", bg = "royal blue",
                       font = ("Comic Sans", 20, "bold")).place(x=10, y=330, width = 400, height = 150)
    def OpenNationalInsurance(self):
        choice = "National Insurance"
        nationalinsurance = NationalInsurance.FiscalNationalInsurance(choice, self.UserID, self.NationalI, self.maximumslidervalue)
        self.fiscal_screen.destroy()




    #CORPORATION TAX
    def CorporationTax(self):
        CorpTax = Button(self.fiscal_screen, text = "Corporation Tax", foreground = "black", command = lambda: self.OpenCorporationTax(),
                         borderwidth = 2, relief = "solid", bg = "royal blue",
                         font = ("Comic Sans", 20, "bold")).place(x=590, y=10, width = 400, height = 150)
    def OpenCorporationTax(self):
        choice = "Corporation Tax"
        corporationtax = CorporationTax.FiscalCorporationTax(choice, self.UserID, self.CorpT, self.maximumslidervalue)
        self.fiscal_screen.destroy()



        
    #VALUE ADDED TAX
    def VAT(self):
        VAT = Button(self.fiscal_screen, text = "Value Added Tax", foreground = "black", command = lambda: self.OpenVAT(),
                     borderwidth = 2, relief = "solid", bg = "royal blue",
                     font = ("Comic Sans", 20, "bold")).place(x=590, y=170, width = 400, height = 150)
    def OpenVAT(self):
        choice = "Value Added Tax"
        vat = VAT.FiscalVAT(choice, self.UserID, self.VAT, self.maximumslidervalue)  #Lower case vat as VAT has already been defined
        self.fiscal_screen.destroy()

    


    #CARBON TAX
    def CarbonTax(self):
        CarbonTax = Button(self.fiscal_screen, text = "Carbon Tax", foreground = "black", command = lambda: self.OpenCarbonTax(),
                           borderwidth = 2, relief = "solid", bg = "royal blue",
                           font = ("Comic Sans", 20, "bold")).place(x=590, y=330, width = 400, height = 150)
    def OpenCarbonTax(self):
        choice = "Carbon Tax"
        carbontax = CarbonTax.FiscalCarbonTax(choice, self.UserID, self.CarbonT, self.maximumslidervalue)
        self.fiscal_screen.destroy()


#--------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------Fiscal Spending Buttons----------------------------------------------------------

    #SOCIAL PROTECTION SPENDING
    def SPExpenditure(self):
        SPSpending = Button(self.fiscal_screen, text = "Social Protection", foreground = "black", command = lambda: self.OpenSPSpending(),
                            borderwidth = 2, relief = "solid", bg = "royal blue",
                            font = ("Comic Sans", 20, "bold")).place(x=10, y=10, width = 400, height = 150)
    def OpenSPSpending(self):
        choice = "Social Protection"
        SocProt = SocialProtection.FiscalSocialProtection(choice, self.UserID, self.SocialProt, self.maximumslidervalue)
        self.fiscal_screen.destroy()


        
    #HEALTH SPENDING
    def HealthExpenditure(self):
        HealthSpending = Button(self.fiscal_screen, text = "Health", foreground = "black",command = lambda: self.OpenHealthSpending(),
                                borderwidth = 2, relief = "solid", bg = "royal blue",
                                font = ("Comic Sans", 20, "bold")).place(x=590, y=10, width = 400, height = 150)
    def OpenHealthSpending(self):
        choice = "Health"
        HEALTH = Health.FiscalHealth(choice, self.UserID, self.Health, self.maximumslidervalue)
        self.fiscal_screen.destroy()

        

    #EDUCATION SPENDING
    def EducationExpenditure(self):
        EducationSpending = Button(self.fiscal_screen, text = "Education", foreground = "black", command = lambda: self.OpenEducationSpending(),
                                   borderwidth = 2, relief = "solid", bg = "royal blue",
                                   font = ("Comic Sans", 20, "bold")).place(x=10, y=330, width = 400, height = 150)
    def OpenEducationSpending(self):
        choice = "Education"
        print(self.Education)
        EDUCATION = Education.FiscalEducation(choice, self.UserID, self.Education, self.maximumslidervalue)
        self.fiscal_screen.destroy()
        
        

    #DEFENCE SPENDING
    def DefenceExpenditure(self):
        DefenceSpending = Button(self.fiscal_screen, text = "Defence", foreground = "black", command = lambda: self.OpenDefenceSpending(),
                                 borderwidth = 2, relief = "solid", bg = "royal blue",
                                 font = ("Comic Sans", 20, "bold")).place(x=590, y=330, width = 400, height = 150)
    def OpenDefenceSpending(self):
        print(self.Defence)
        choice = "Defence"
        DEFENCE = Defence.FiscalDefence(choice, self.UserID, self.Defence, self.maximumslidervalue)
        self.fiscal_screen.destroy()

#----------------------------------------------------------------------------------------------------------------------------------------

#End of file: FiscalSelected

def main():

    
    Fiscal = TaxOrSpending(1)

    
if __name__ == "__main__":
    main()
    




