#New file: Charts
import sys

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
import Load_Everything as LE

import matplotlib.pyplot as plt




class Charts(LE.Load):

    def __init__(self, UserID):

        self.UserID = UserID

    def P_GovernmentSpending(self):

        SocialProtection, Health, Education, Defence = self.LoadFiscalSpending()
        PublicSectorInvestment, WelfareBenefits, VocationalTraining, CouncilHousing = self.LoadSSPolicies()
        
        
        
        policies = ['Social Protection', 'Health', 'Education', 'Defence', 'Public Sector Investment', 'Welfare Benefits', 'Vocational Training', 'Council Housing']

        maximum = 0     #Temporary maximum is 0
        maximumpolicy = []
     
        for policy in policies:
            
            if eval(policy.replace(" ", "")) >= maximum: #Get the one that is the biggest so that it is the one that is exploded
                if maximumpolicy:   #If its not empty
                    indexoflastadded = len(maximumpolicy) - 1   #Get the last value (as this is the last one that was added
                    if eval(maximumpolicy[indexoflastadded].replace(" ", "")) < eval(policy.replace(" ", "")):  #See if the last value has a value lower than the one being added
                        maximumpolicy.remove(maximumpolicy[indexoflastadded])   #If its value is lower, remove it from the list
                maximum = eval(policy.replace(" ", ""))
                maximumpolicy.append(policy)
        print(maximumpolicy)
            
        colours = ['red', 'yellowgreen', 'lightcoral', 'lightskyblue', 'aqua', 'coral', 'magenta', 'pink']
        sizes = [SocialProtection, Health, Education, Defence, PublicSectorInvestment, WelfareBenefits, VocationalTraining, CouncilHousing]

        
        explode = []
        for policy in policies: #This loop decides which parts of the pie chart are exploded
            if policy in maximumpolicy:
                explode.append(0.1)
            else:
                explode.append(0)
        
        spendingpiechart = plt.pie(sizes, labels=policies, explode = explode, colors=colours,
                                    autopct='%1.1f%%', shadow=True, startangle=90)  #autopct meaning the digits displayed
        plt.axis('equal')   #So that it appears as a circle.
        plt.show()



        

    def B_TaxRates(self):

        IncomeTax, ExciseDuty, NationalInsurance, CorporationTax, VAT, CarbonTax = self.LoadFiscalTaxes()


        x = ['Income Tax', 'National Insurance']
        
        IncomeT = plt.bar("""Income
Tax""",IncomeTax, label = 'Income Tax', color = 'aqua')
                          
        ExciseD = plt.bar('Excise Duty', ExciseDuty, label = 'Excise Duty', color = 'pink')
                          
        NationalI = plt.bar("""National
Insurance""", NationalInsurance, label = 'National Insurance', color = 'red')
        
        CorporationT = plt.bar("""Corporation
Tax""", CorporationTax, label = 'Corporation Tax', color = 'lightcoral')
        
        VATT = plt.bar('VAT', VAT, label = 'Value Added Tax', color = 'pink')
        
        CarbonT = plt.bar("""Carbon
Tax""", CarbonTax, label = 'Carbon Tax', color = 'yellowgreen')
        
        plt.xlabel('Taxes')
        plt.ylabel('Tax Rate (%)')
        plt.title('Your Tax Rates (%)')
        plt.legend()
        plt.show()

#End of file: Charts

        
if __name__ == "__main__":

    pieChart = Charts(1)
    pieChart.B_TaxRates()
