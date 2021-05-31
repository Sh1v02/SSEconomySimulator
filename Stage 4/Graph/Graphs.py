#New file: Graphs

import sys
import math
import random



sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")    #Load_Everything
import Load_Everything as LE




class GraphCreations(LE.Load):
    def __init__(self, UserID):

        self.UserID = UserID
        
        
        
        self.IncomeT, self.ExciseD, self.NationalI, self.CorpT, self.VAT, self.CarbonT = self.LoadFiscalTaxes()
        self.ratings, self.HighIncome, self.Pensioners, self.MiddleIncome, self.Unemployed, self.LowIncome, self.Business, self.Overall = self.LoadRatings()
        self.NationalDebt, self.CurrentAccount, self.UnemploymentRate, self.Inflation, self.GDP, self.Year = self.LoadStatistics()
        self.BudgetBalance, self.CurrencyValue, self.TaxRevenue, self.GovernmentSpending, self.DisposableIncome, self.MPC, self.Imports, self.Exports = self.LoadExtraStatistics()
        self.InterestRate = self.LoadInterestRates()
        self.SocialProtection, self.Health, self.Education, self.Defence = self.LoadFiscalSpending()
        self.PublicInvestment, self.WelfareBenefits, self.VocationalTraining, self.CouncilHousing = self.LoadSSPolicies()
        
        if self.CurrentAccount < 0: #If the current account is in a deficit (< 0) then make the imports weight value greater than 0.5 so that imports take up a large amount of consumption.
            self.importsweightvalue = 0.8
            self.exportsweightvalue = 0.5
        else:
            self.importsweightvalue = 0.5
            self.exportsweightvalue = 0.8

        #Marginal Propensity To Consume plays a big role on how much is consumed in an economy. Although normally the exact MPC value would be used, a different value is used in this 
        #   simulation as there are not enough factors to go along with the MPC in the economy to make the effects come through properly and therefore the simulation would not be 
        #   realistic enough. Instead, if the MPC value is greater than 0.5 then the value to use will be higher than if it was less than 0.5.
        #   While the values are only 0.11 apart, this will have a big effect on consumption and inflation in the economy etc...
        if self.MPC > 0.5:
            self.MPC_value = 0.995
        else:
            self.MPC_value = 0.885
       

        
    #INCOME TAX GRAPH
    def IncomeTaxGraph(self, changedamount, listofreturns):

        

        #The calculations in here are all calculated with the influence of research and actual economic effects.
        #Income tax is calculated by adding the disposable income value*0.99 to 1. However, the disposable income value subtracts 1 then divides itself by the modulus (maths modulus)
        #   of itself to determine if it has increased or decreased. Decreased would result in -1, increased in +1. Therfore the 1 + will decrease the value if income tax decreases and 
        #   increase it if income tax has increased.


        #1 + (((listofreturns['Disposable Income Start Multiple']-1)/(math.sqrt((listofreturns['Disposable Income Start Multiple']-1)**2))) * 
                                                      #(listofreturns['Disposable Income Start Multiple'])*0.95)
        
        graph = {
            #Income Tax
            'Income Tax Start' : {'IncomeTax' : changedamount},
            'IncomeTax' : {'TaxRevenue' : (1+(changedamount/100)) , 'Disposable Income Start Multiple' : None, 'UnemploymentRate Start Multiple' : None},

            


            
            'TaxRevenue' : {'NationalDebt' : 1-((changedamount-1)/2.75)},      #- changedamount as it is an inverse relationship (if one goes up the other goes down)
            'NationalDebt' : {None: None},



            #Multiple after its name meaning it has multiple child nodes.
            #Not necessary for start nodes!
            'Disposable Income Start Multiple' : {'DisposableIncome': (1-(listofreturns["Start"]/100))},  


            #DONT EVEN NEED LOWINCOME IN HERE  BUT I MIGHT FOR WHEN USING THE PASSED VALUES IN THE ACTUAL TAX FILE 
            'DisposableIncome' : {'LowIncome' : 1+((listofreturns['Start'] * 0.3)/100),  #LowIncome happier as it is a progressive tax so inequality is reduced if raised.
                                   'MiddleIncome Start' : None, 'HighIncome Start' : None, 'Pensioners Start' : None, 'Consumption Start Multiple' : None}, 
            'LowIncome' : {None : None},
            'MiddleIncome Start' : {'MiddleIncome' : listofreturns['Disposable Income Start Multiple'] * 0.98}, #Although close to one, this has a large but also accurate effect.
            'HighIncome Start' : {'HighIncome' : listofreturns['Disposable Income Start Multiple'] * 0.99},
                                                
                                            #This works well as an increase in disposable income affects higher income earners more than middle, but a decrease affects middle incomes
                                            #   more than higher incomes.
            'Pensioners Start' : {'Pensioners' : listofreturns['Disposable Income Start Multiple']*0.97},    #Pensioners are not affected as much.
            'MiddleIncome' : {None: None},
            'HighIncome' : {None: None},
            'Pensioners' : {'Pensioners' : None},


            'Consumption Start Multiple' : {'Consumption' : 1-(1-(listofreturns['Disposable Income Start Multiple'] * self.MPC_value))},#Of the increase in disposable income,
                                                                                                                                        #   self.MPC_value is consumption.
            'Consumption' : {'Imports': 1-((1-changedamount)*self.importsweightvalue), 'Inflation Start' : None},
            
            'Imports' : {'CurrentAccount' : ((self.Imports*changedamount)-self.Imports)}, #The change in Imports determines how current account changes.
            'CurrentAccount' : {None : None},
            

            #This is what MPC will be timesed by
            #'Consumption Start' : {'MPC' : ((listofreturns['Consumption Start Multiple']-1)/((listofreturns['Disposable Income Start Multiple']*self.DisposableIncome)-(self.DisposableIncome)))/100},
                                                                                                    
            #'MPC' : {'Inflation' : listofreturns['Consumption Start Multiple']},

            #'MPC Start' : {'MPC' : (listofreturns['Consumption Start Multiple']-1)/(listofreturns['Disposable Income Start Multiple']-1)},
            #'MPC' : {None : None},



            
            'Inflation Start' : {'Inflation' : (listofreturns['Consumption Start Multiple'])+0.2},  #With the lack of factors, calculating some values such as inflation is
                                                                                                    #   very hard. Inflation normally has a proportional relationship with consumption, but
                                                                                                    #   increases at a slightly higher rate. Inflation was one of them main reasons that
                                                                                                    #   consumption was added, just so that it could be calculated more accurately to produce
                                                                                                    #   a more realistic game.
                                                                                                                
            'Inflation' : {None : None},
            
            
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.075))},#Unemployment is changed uniquely by so is uniquely calculated.
            
            #The Unemployment Rate has a very large affect on GDP (productivity and output etc)
            'UnemploymentRate' : {'GDP' : ((changedamount*3)+100)/100, 'Businesses Start' : None, 'Unemployed Start' : None},   
            'GDP' : {None : None},
            'Businesses Start' : {'Businesses' : ((listofreturns['UnemploymentRate Start Multiple']*2)/100)+1}, #UnemploymentBusiness for business change caused by unemployment.
            'Businesses' : {None : None},
            'Unemployed Start' : {'Unemployed' : ((listofreturns['UnemploymentRate Start Multiple']*7.5)/100)+1}, #Unemployed affected almost four times as much as businesses in this case,
                                                                                                            #   as it is unemployment itself that is changing.
            'Unemployed' : {None : None},
        }


        return graph


    #NATIONAL INSURANCE GRAPH#
    def NationalInsuranceGraph(self, changedamount, listofreturns):

        #In this graph, the unemployment rate does not affect the satisfaction of the unemployed, only GDP (as the unemployed themselves arent affected.
        #Low income earners are also affected by changes in disposable income in this graph.
        #Businesses in this graph don't affect unemployment.

        graph = {
            #NationalInsurance
            'National Insurance Start' : {'National Insurance' : changedamount},
            'National Insurance' : {'TaxRevenue' : (1+((changedamount/1.5)/100)), 'Disposable Income Start Multiple' : None, 'UnemploymentRate Start Multiple' : None},

           
            


            
            'TaxRevenue' : {'NationalDebt' : 1-((changedamount-1)/2.75)},      #- changedamount as it is an inverse relationship (if one goes up the other goes down)
            'NationalDebt' : {None: None},



            #Multiple after its name meaning it has multiple child nodes.
            #Not necessary for start nodes!
            'Disposable Income Start Multiple' : {'DisposableIncome': (1-(0.8*listofreturns["Start"])/100)},  #Almost the same effect as Income Tax, but still a smaller effect.


            #DONT EVEN NEED LOWINCOME IN HERE  BUT I MIGHT FOR WHEN USING THE PASSED VALUES IN THE ACTUAL TAX FILE 
            'DisposableIncome' : {'LowIncome' : 1-((listofreturns['Start'] * 0.05)/100),  #LowIncome not affected by income tax as it is a progressive tax!
                                   'MiddleIncome Start' : None, 'HighIncome Start' : None, 'Pensioners Start' : None, 'Consumption Start Multiple' : None}, 
            'LowIncome' : {None : None},
            'MiddleIncome Start' : {'MiddleIncome' : (listofreturns['Disposable Income Start Multiple'])*1}, #Although close to one, this has a large but also accurate effect.
            'HighIncome Start' : {'HighIncome' : 1-((listofreturns['Start'] * 0.59)/100)},     #This works well as an increase in disposable income affects higher income
                                                                                                                #   earners more than middle, but a decrease affects middle more than higher.
            'Pensioners Start' : {'Pensioners' : 1},    #Pensioners aren't affected
            'MiddleIncome' : {None: None},
            'HighIncome' : {None: None},
            'Pensioners' : {'Pensioners' : None},


            'Consumption Start Multiple' : {'Consumption' : 1-(1-(listofreturns['Disposable Income Start Multiple'] * 0.995))}, #Of the increase in disposable income, 0.996 is consumption.
            'Consumption' : {'Imports': 1-((1-changedamount)*self.importsweightvalue), 'Inflation Start' : None},
            
            'Imports' : {'CurrentAccount' : ((self.Imports*changedamount)-self.Imports)}, #The change in Imports determines how current account changes.
            'CurrentAccount' : {None : None},
            

            
            'Inflation Start' : {'Inflation' : (listofreturns['Consumption Start Multiple'])+0.2},  #With the lack of factors, calculating some values such as inflation is
                                                                                                    #   very hard. Inflation normally has a proportional relationship with consumption, but
                                                                                                    #   increases at a slightly higher rate. Inflation was one of them main reasons that
                                                                                                    #   consumption was added, just so that it could be calculated more accurately to produce
                                                                                                    #   a more realistic game.
                                                                                                                
            'Inflation' : {None : None},
            
            
            
            
            
            
            
            

            #Businesses Start when something has a direct affect on businesses.
            'Businesses Start Multiple' : {'Businesses' : ((100-listofreturns['Start'])/100)*1.1},
            'Businesses' : {None : None},
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.07))},#Unemployment is changed uniquely by so is uniquely calculated.
            
            #The Unemployment Rate has a very large affect on GDP (productivity and output etc)
            'UnemploymentRate' : {'GDP' : ((changedamount*3)+100)/100},
            'GDP' : {None : None},
        
            'Unemployed Start' : {'Unemployed' : ((listofreturns['UnemploymentRate Start Multiple']*7.5)/100)+1}, 
            
            'Unemployed' : {None : None}
        }


        return graph
    
    
    #CORPORATION TAX GRAPH#
    def CorporationCarbonTaxGraph(self, changedamount, listofreturns):



        graph = {
            #Corporation Tax
            'Corporation Tax Start' : {'Corporation Tax' : changedamount},
            'Corporation Tax' : {'TaxRevenue' : 1+((changedamount/2)/100), 'Businesses Start Multiple' : None},

            #Carbon Tax
            'Carbon Tax Start' : {'Carbon Tax' : changedamount},
            'Carbon Tax' : {'HighIncome' : math.sqrt(((1-((listofreturns['Start'] * 1.4)/100))**2)), 'TaxRevenue Start' : None, 'Businesses Start Multiple' : None},
                                                         #math.sqrt(of the number squared) to obtain the modulus (maths modulus) so that it is never a negative number.                                                                                       



            'TaxRevenue Start': {'TaxRevenue' : 1+((listofreturns['Start']/2.222222)/100)}, #Tax revenue started needed here as it is not the first element in the carbon tax dictionary
                                                                                            #   key.
                                                                                            #The weight should be the changedamount/4, but as listofreturns['Start'] 
                                                                                            #   is changedamount/2 so that the business weight will work effectlively and accurately, 
                                                                                            #   it becomes /2.2222222 to make up for dividing by the 1.8.
            
            'TaxRevenue' : {'NationalDebt' : 1-((changedamount-1)/2.75)},      #- changedamount as it is an inverse relationship (if one goes up the other goes down)
            'NationalDebt' : {None: None},



            #Multiple after its name meaning it has multiple child nodes.
            #Not necessary for start nodes!
            'Disposable Income Start Multiple' : {'DisposableIncome': (1-(listofreturns["Start"]/100))},  


            #DONT EVEN NEED LOWINCOME IN HERE  BUT I MIGHT FOR WHEN USING THE PASSED VALUES IN THE ACTUAL TAX FILE 
            'DisposableIncome' : {'LowIncome' : 1,  #LowIncome not affected by income tax as it is a progressive tax!
                                   'MiddleIncome Start' : None, 'HighIncome Start' : None, 'Pensioners Start' : None, 'Consumption Start Multiple' : None}, 
            'LowIncome' : {None : None},
            'MiddleIncome Start' : {'MiddleIncome' : (listofreturns['Disposable Income Start Multiple'])*0.98}, #Although close to one, this has a large but also accurate effect.
            'HighIncome Start' : {'HighIncome' : (listofreturns['Disposable Income Start Multiple'])*0.99},     #This works well as an increase in disposable income affects higher income
                                                                                                                #   earners more than middle, but a decrease affects middle more than higher.
            'Pensioners Start' : {'Pensioners' : (listofreturns['Disposable Income Start Multiple'])*0.999},    #Pensioners are not affected as much.
            'MiddleIncome' : {None: None},
            'HighIncome' : {None: None},
            'Pensioners' : {'Pensioners' : None},


            'Consumption Start Multiple' : {'Consumption' : 1-(1-(listofreturns['Disposable Income Start Multiple'] * 0.995))}, #Of the increase in disposable income, 0.996 is consumption.
            'Consumption' : {'Imports': 1-((1-changedamount)*self.importsweightvalue), 'Inflation Start' : None},
            
            'Imports' : {'CurrentAccount' : ((self.Imports*changedamount)-self.Imports)}, #The change in Imports determines how current account changes.
            'CurrentAccount' : {None : None},
            

            'Inflation Start' : {'Inflation' : (listofreturns['Consumption Start Multiple'])+0.2},  #With the lack of factors, calculating some values such as inflation is
                                                                                                    #   very hard. Inflation normally has a proportional relationship with consumption, but
                                                                                                    #   increases at a slightly higher rate. Inflation was one of them main reasons that
                                                                                                    #   consumption was added, just so that it could be calculated more accurately to produce
                                                                                                    #   a more realistic game.
                                                                                                                
            'Inflation' : {None : None},
            
            
            
            
            
            
            
            

            #Businesses Start when something has a direct affect on businesses.
            'Businesses Start Multiple' : {'Businesses' : 1-(((listofreturns['Start']*4)/100))},    #((100-listofreturns['Start'])/100)*3
            'Businesses' : {'UnemploymentRate Start Multiple' : None},
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.07))},#Unemployment is changed uniquely by so is uniquely calculated.
            
            #The Unemployment Rate has a very large affect on GDP (productivity and output etc)
            'UnemploymentRate' : {'GDP' : ((changedamount*3)+100)/100, 'Unemployed Start' : None},
            'GDP' : {None : None},
        
            'Unemployed Start' : {'Unemployed' : ((listofreturns['UnemploymentRate Start Multiple']*7.5)/100)+1}, 
            
            'Unemployed' : {None : None}
        }


        return graph



    





        
    def VATGraph(self, changedamount, listofreturns):

        #In this graph, the unemployment rate does not affect the satisfaction of the unemployed, only GDP (as the unemployed themselves arent affected).
        #Low income earners are also affected by changes in disposable income in this graph.
        #Businesses in this graph don't affect unemployment.
        
        #VAT
        graph = {
            #VAT
            'Value Added Tax Start' : {'Value Added Tax': changedamount},
            'Value Added Tax' : {'TaxRevenue' : (1+((changedamount/1.75)/100)), 'Disposable Income Start Multiple' : None, 'Businesses Start Multiple' : None},


            'TaxRevenue' : {'NationalDebt' : 1-((changedamount-1)/2.75)},      #- changedamount as it is an inverse relationship (if one goes up the other goes down)
            'NationalDebt' : {None: None},



            #Multiple after its name meaning it has multiple child nodes.
            #Not necessary for start nodes!
            'Disposable Income Start Multiple' : {'DisposableIncome': (1-(0.5*listofreturns["Start"])/100)},  #Less effect on income than national insurance as it is an indirect tax.


            #DONT EVEN NEED LOWINCOME IN HERE  BUT I MIGHT FOR WHEN USING THE PASSED VALUES IN THE ACTUAL TAX FILE 
            'DisposableIncome' : {'LowIncome' : listofreturns['Disposable Income Start Multiple'] * 0.99,  #LowIncome are massively affected by VAT as it is a regressive tax!
                                                                                           #Calculated through use of teachers and research.
                                   'MiddleIncome Start' : None, 'HighIncome Start' : None, 'Pensioners Start' : None, 'Consumption Start Multiple' : None}, 
            'LowIncome' : {None : None},
            'MiddleIncome Start' : {'MiddleIncome' : listofreturns['Disposable Income Start Multiple'] * 0.975},
            'HighIncome Start' : {'HighIncome' : 1},    #High Income Earners are less affected by paying extra compared to low income earners
            
            'Pensioners Start' : {'Pensioners' : (listofreturns['Disposable Income Start Multiple'])*0.999},    #Pensioners are not affected as much.
            'MiddleIncome' : {None: None},
            'HighIncome' : {None: None},
            'Pensioners' : {'Pensioners' : None},


            'Consumption Start Multiple' : {'Consumption' : 1-(1-(listofreturns['Disposable Income Start Multiple'] * 0.995))}, #Of the increase in disposable income, 0.996 is consumption.
            'Consumption' : {'Imports': 1-((1-changedamount)*self.importsweightvalue), 'Inflation Start' : None},
            
            'Imports' : {'CurrentAccount' : ((self.Imports*changedamount)-self.Imports)}, #The change in Imports determines how current account changes.
            'CurrentAccount' : {None : None},
            

            
            'Inflation Start' : {'Inflation' : (listofreturns['Consumption Start Multiple'])+0.1},  #Inflation not affected as much with this graph.
                                                                                                                
            'Inflation' : {None : None},
            
            
            
            
            
            
            
            

            #Businesses Start when something has a direct affect on businesses.
            'Businesses Start Multiple' : {'Businesses' : ((100-(listofreturns['Start'])/2)/100)*1.1},
            'Businesses' : {None : None},
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.07))},#Unemployment is changed uniquely by so is uniquely calculated.
            
            #The Unemployment Rate has a very large affect on GDP (productivity and output etc)
            'UnemploymentRate' : {'GDP' : ((changedamount*3)+100)/100},
            'GDP Start' : {'GDP' : listofreturns['Consumption Start Multiple']*0.99},
            'GDP' : {None : None},
        
            'Unemployed Start' : {'Unemployed' : ((listofreturns['UnemploymentRate Start Multiple']*7.5)/100)+1}, 
            
            'Unemployed' : {None : None}
        }


        return graph

    def ExciseDutyGraph(self, changedamount, listofreturns):
        
        #In this graph, low income earners are significantly effected by a change in disposable income.

        
        graph = {
            #Excise Duty
            'Excise Duty Start' : {'Excise Duty': changedamount},
            'Excise Duty' : {'TaxRevenue' : (1+((changedamount/2.5)/100)), 'Disposable Income Start Multiple' : None},


            'TaxRevenue' : {'NationalDebt' : 1-((changedamount-1)/3)},      #- changedamount as it is an inverse relationship (if one goes up the other goes down)
            'NationalDebt' : {None: None},



            #Multiple after its name meaning it has multiple child nodes.
            #Not necessary for start nodes!
            'Disposable Income Start Multiple' : {'DisposableIncome': (1-(0.7*listofreturns["Start"])/100)},  #Less effect on income than national insurance as it is an indirect tax.


            #DONT EVEN NEED LOWINCOME IN HERE  BUT I MIGHT FOR WHEN USING THE PASSED VALUES IN THE ACTUAL TAX FILE 
            'DisposableIncome' : {'LowIncome' : (listofreturns['Disposable Income Start Multiple'])*0.99,  #LowIncome are massively affected by VAT as it is a regressive tax!
                                   'MiddleIncome Start' : None, 'HighIncome Start' : None, 'Pensioners Start' : None, 'Consumption Start Multiple' : None}, 
            'LowIncome' : {None : None},
            'MiddleIncome Start' : {'MiddleIncome' : 1}, #Essentially 1.
            'HighIncome Start' : {'HighIncome' : 1},    #High Income Earners are less affected by paying extra compared to low income earners
            
            'Pensioners Start' : {'Pensioners' : (listofreturns['Disposable Income Start Multiple'])*0.999},    #Pensioners are not affected as much.
            'MiddleIncome' : {None: None},
            'HighIncome' : {None: None},
            'Pensioners' : {'Pensioners' : None},


            'Consumption Start Multiple' : {'Consumption' : 1-(1-(listofreturns['Disposable Income Start Multiple'] * 0.995))}, #Of the increase in disposable income, 0.996 is consumption.
            'Consumption' : {'Imports': 1-((1-changedamount)*self.importsweightvalue), 'Inflation Start' : None},
            
            'Imports' : {'CurrentAccount' : ((self.Imports*changedamount)-self.Imports)}, #The change in Imports determines how current account changes.
            'CurrentAccount' : {None : None},
            

            
            'Inflation Start' : {'Inflation' : (listofreturns['Consumption Start Multiple'])+0.05},  #Inflation not affected as much with this graph. Inflation will
                                                                                                    #   increase even if consumption is 0.
                                                                                                                
            'Inflation' : {None : None},
            
            
            
            
            
            
            
            

            #Businesses Start when something has a direct affect on businesses.
            'Businesses Start Multiple' : {'Businesses' : ((100-(listofreturns['Start'])/2)/100)*1.1},
            'Businesses' : {None : None},
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.07))},#Unemployment is changed uniquely by so is uniquely calculated.
            
            #The Unemployment Rate has a very large affect on GDP (productivity and output etc)
            'UnemploymentRate' : {'GDP' : ((changedamount*3)+100)/100},
            'GDP Start' : {'GDP' : listofreturns['Consumption Start Multiple']*0.99},
            'GDP' : {None : None},
        
            'Unemployed Start' : {'Unemployed' : ((listofreturns['UnemploymentRate Start Multiple']*7.5)/100)+1}, 
            
            'Unemployed' : {None : None}
        }


        return graph




    ####################################        Fiscal Spending Graphs Now      ##########################################################

    def SocialProtectionGraph(self, changedamount, listofreturns):

        #Fiscal Spending


        graph = {
            #Social Protection
            'Social Protection Start' : {'SocialProtection' : changedamount},
            'SocialProtection' : {'GovernmentSpending Start' : None, 'Pensioners Start' : None, 'Unemployed Start' : None, 'LowIncome Start' : None},   #GovernmentSpending value
                                                                                                                                                        #   is simply just adding the
                                                                                                                                                        #   value changed on


            
            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*0.15)/2.75)/100))},
            'NationalDebt' : {None : None},

            
            'Pensioners Start' : {'Pensioners' : 1+((listofreturns['%change'] * 0.24)/100)},
            'Pensioners' : {None : None},

            'Unemployed Start' : {'Unemployed' : 1+((listofreturns['%change'] * 0.16)/100)},
            'Unemployed' : {'Businesses' : 1+((changedamount-1)*0.15)}, #Businesses are affected as if unemployed people have higher standards of living then they may seeks jobs
                                                                        #   which will benefit businesses seeking workers.
            'Businesses' : {None : None},
            
            'LowIncome Start' : {'LowIncome' : 1+((listofreturns['%change'] * 0.1)/100)},
            'LowIncome' : {None : None},

            
            

            
        }
            

        return graph


    def HealthEducationGraph(self, changedamount, listofreturns, Type): #This graph is different as it is a spending graph which is used by 2 policies, but government spending must
                                                                        #   have the same effect on national debt as all other spending graphs. As the %change is changed in the
                                                                        #   MakeChanges class, those changes need to be reversed for the nationaldebt effects, which is why
                                                                        #   Type is needed to determine how much to invert the changes by.

                                
        
        #Fiscal Spending

        #A new graph is made separately to Social Protection as businesses are affected directly here, not becuase of unemployment.
        #If businesses were also to be added as a direct effect along with being affected by the unemployed, then even though it should be affected twice, the visitedlist will not append
        #   it as it has already been visited (my depth first traversal algorithm design).
        #Therefore a new graph is made, but this also has other effects and different calculations.



        if Type == "Health":
            #For Health, National Debt generated must be timesed by 2.
            ND_multiplier = 2
        else:
            #For education, National Debt generated must be timesed by 1.8.
            ND_multiplier = 1.8
            

        graph = {
            #Health
            'Health Start' : {'Health' : changedamount},
            'Health' : {'GovernmentSpending Start' : None, 'Pensioners Start' : None, 'Unemployed Start' : None, 'LowIncome Start' : None, 'MiddleIncome Start' : None,
                        'Businesses Start' : None},

            #Education
            'Education Start' : {'Education' : changedamount},
            'Education' : {'Unemployed' : 1+((listofreturns['%change'] * 0.02)/100), 'GovernmentSpending Start' : None, 'LowIncome Start' : None, 'MiddleIncome Start' : None,
                           'Businesses Start' : None, 'GDP Start' : None},

            

            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*ND_multiplier*0.15)/2.75)/100))},  #1+(((listofreturns['%change']*0.8)/100))
            'NationalDebt' : {None : None},

            
            'Pensioners Start' : {'Pensioners' : 1+((listofreturns['%change'] * 0.25)/100)},
            'Pensioners' : {None : None},

            'Unemployed Start' : {'Unemployed' : 1+((listofreturns['%change'] * 0.21)/100)},
            'Unemployed' : {None : None},
            
            
            'LowIncome Start' : {'LowIncome' : 1+((listofreturns['%change'] * 0.2)/100)},
            'LowIncome' : {None : None},

            'MiddleIncome Start' : {'MiddleIncome' : 1+((listofreturns['%change'] * 0.18)/100)},
            'MiddleIncome' : {'MiddleIncome' : None},
            'Businesses Start' : {'Businesses' : 1+((listofreturns['%change'] * 0.05)/100)},    #Improved Health means workers are more productive so output increases.
            'Businesses' : {None : None},

            'GDP Start' : {'GDP' : 1+((listofreturns['%change'] * 0.025)/100)},
            'GDP' : {None : None}
            

            
        }
            

        return graph
        

    def DefenceGraph(self, changedamount, listofreturns):
        
        #Fiscal Spending

        
        #This graph is different as defence actually has a negative effect on economic growth and therefore investors/businesses.
        #The values here are timesed by very small numbers because defence often starts at a low value, therfore a small increase becomes a large percentage change, so values must be
        #   timesed by smaller values.

        
        graph = {
            #Defence
            'Defence Start' : {'Defence' : changedamount},
            'Defence' : {'GovernmentSpending Start' : None, 'HighIncome Start' : None, 'Pensioners Start' : None, 'MiddleIncome Start' : None,
                        'Businesses Start' : None},

            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*0.15)/2.75)/100))}, 
            'NationalDebt' : {None : None},

            
            'Pensioners Start' : {'Pensioners' : 1+((listofreturns['%change'] * 0.01)/100)},
            'Pensioners' : {None : None},

            'HighIncome Start' : {'HighIncome' : 1+((listofreturns['%change'] * 0.0125)/100)},
            'HighIncome' : {None : None},
            
            'MiddleIncome Start' : {'MiddleIncome' : 1+((listofreturns['%change'] * 0.0075)/100)},
            'MiddleIncome' : {'MiddleIncome' : None},
            'Businesses Start' : {'Businesses' : 1-((listofreturns['%change'] * 0.08)/100)},    #This is acutally inversed, if more money is spent on defence, economic growth tends to
                                                                                                #   decrease, resulting in investors and businesses being less happy.
            'Businesses' : {None : None},

            'GDP Start' : {'GDP' : 1-((listofreturns['%change'] * 0.05)/100)},
            'GDP' : {None : None}
            

            
        }
            

        return graph



    def PublicInvestmentGraph(self, changedamount, listofreturns):

        #Supply Side Policy



        graph = {
            #Public Sector Investment
            'Public Investment Start' : {'PublicInvestment' : changedamount},
            'PublicInvestment' : {'GovernmentSpending Start' : None, 'Pensioners Start' : None, 'LowIncome Start' : None, 'MiddleIncome Start' : None, 'HighIncome Start' : None,
                                  'Businesses Start' : None},

            

            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*0.15)/2.75)/100))}, 
            'NationalDebt' : {None : None},

            
            'Pensioners Start' : {'Pensioners' : 1+((listofreturns['%change'] * 0.035)/100)},
            'Pensioners' : {None : None},

            'LowIncome Start' : {'LowIncome' : 1+((listofreturns['%change'] * 0.025)/100)},
            'LowIncome' : {None : None},
            
            'MiddleIncome Start' : {'MiddleIncome' : 1+((listofreturns['%change'] * 0.0225)/100)},
            'MiddleIncome' : {'MiddleIncome' : None},
            
            'Businesses Start' : {'Businesses' : 1+((listofreturns['%change'] * 0.02)/100)},    #This is acutally inversed, if more money is spent on defence, economic growth tends to
                                                                                                #   decrease, resulting in investors and businesses being less happy.
            'Businesses' : {None : None}
        }
            

        return graph
        


    def WelfareBenefitsGraph(self, changedamount, listofreturns):

        #Supply Side Policy



        graph = {
            #Public Sector Investment
            'Welfare Benefits Start' : {'WelfareBenefits' : changedamount},
            'WelfareBenefits' : {'GovernmentSpending Start' : None, 'HighIncome Start' : None, 'MiddleIncome Start' : None, 'UnemploymentRate Start Multiple' : None},

            

            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*0.15)/2.75)/100))}, 
            'NationalDebt' : {None : None},

            'HighIncome Start' : {'HighIncome' : (math.sqrt(((1-((listofreturns['Start'] * 0.6)/100))**2)))},    #High and middle income are unhappy if welfare befits increase as their tax money will
                                                                                                #   be spent on this as opposed to things that can benefit them.
                                                                                                
            'HighIncome' : {None : None},

            'MiddleIncome Start' : {'MiddleIncome' : (math.sqrt(((1-((listofreturns['Start'] * 0.45)/100))**2)))},
            'MiddleIncome' : {'MiddleIncome' : None},
 
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.25))},
            'UnemploymentRate' : {'Unemployed' : 1 + ((listofreturns['%change']/1.5)/1000), 'Businesses Start' : None},
            'Unemployed' : {None : None},
            
            
            'Businesses Start' : {'Businesses' : 1+(listofreturns['UnemploymentRate Start Multiple']/10)},    #This is acutally inversed, if more money is spent on defence, economic growth tends to
                                                                                                #   decrease, resulting in investors and businesses being less happy.
            'Businesses' : {None : None}
        }
            

        return graph



    def VocationalTrainingGraph(self, changedamount, listofreturns):

        #Supply Side Policy



        graph = {
            #Vocational Training
            'Vocational Training Start' : {'VocationalTraining' : changedamount},
            'VocationalTraining' : {'GovernmentSpending Start' : None, 'UnemploymentRate Start Multiple' : None, 'Disposable Income Start Multiple' : None},

            

            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*0.15)/2.75)/100))}, 
            'NationalDebt' : {None : None},
 
            'UnemploymentRate Start Multiple' : {'UnemploymentRate' : 1-(listofreturns['ValueForUnemployment']*(0.25))},
            'UnemploymentRate' : {'Unemployed' : 1 + ((listofreturns['%change']/2)/1000), 'Businesses Start' : None, },
            'Unemployed' : {None : None},
            
            
            'Businesses Start' : {'Businesses' : 1-(listofreturns['UnemploymentRate Start Multiple']/30)},  
            'Businesses' : {None : None},


            'Disposable Income Start Multiple' : {'DisposableIncome': (1+(listofreturns["%change"]*1.5/10000))},    #As this is %change, which is dramatically bigger in spending than 
                                                                                                                    #   taxation, the value that it is divided by must be much bigger 
                                                                                                                    #   so that it is more realistic and brought into similar levels
                                                                                                                    #   as the tax effects.

            
            'DisposableIncome' : {'Consumption Start Multiple' : None},
            'Consumption Start Multiple' : {'Consumption' : 1-(1-(listofreturns['Disposable Income Start Multiple'] * self.MPC_value))}, #Of the increase in disposable income, MPC_value
                                                                                                                                         #  is consumption.

            'Consumption' : {'Exports Start Multiple': None},   #This consumption doesn't effect import, but exports are effected (as productivity and quality in the economy would have
                                                                #   increased).
            'Exports Start Multiple' : {'Exports' : 1-((1-listofreturns['Disposable Income Start Multiple'])*self.exportsweightvalue)},
            'Exports' : {'CurrentAccount' : (self.Exports-(self.Exports*changedamount)), 'GDP Start' : None},   #self.exports - newvalue here as altough this is the negative of the
                                                                                                                #   changed amount, the current account value calculated later
                                                                                                                #   in policies_everyting subtracts this value generated here,
                                                                                                                #   so this must be the negative of the changed amount so that exports
                                                                                                                #   improve the current account, not worsen it.
            'CurrentAccount' : {None : None},
            'GDP Start' : {'GDP' : listofreturns['Exports Start Multiple']},
            'GDP' : {None : None}
        }
            

        return graph



    def CouncilHousingGraph(self, changedamount, listofreturns):

        #Supply Side Policy



        graph = {
            #Council Housing
            'Council Housing Start' : {'CouncilHousing' : changedamount},
            'CouncilHousing' : {'GovernmentSpending Start' : None, 'Unemployed Start' : None, 'LowIncome Start' : None},

            

            'GovernmentSpending Start' : {'GovernmentSpending' : listofreturns['Start']},   #As the changed amount is the exact amount government spending will increase or decrease that
                                                                                            #   exact amount.
            'GovernmentSpending' : {'NationalDebt' : 1+((((listofreturns['%change']*0.15)/2.75)/100))}, 
            'NationalDebt' : {None : None},
 
            'Unemployed Start' : {'Unemployed' : 1+((listofreturns['%change'] * 0.05)/100)},
            'Unemployed' : {None : None},

            'LowIncome Start' : {'LowIncome' : 1+((listofreturns['%change'] * 0.04)/100)},
            'LowIncome' : {None : None}
            

        }
            

        return graph



    def InterestRatesGraph(self, changedamount, listofreturns):

        #Monetary Policy

        #In this graph, CurrentAccount 1 and CurrentAccount 2 are used as the CurrentAccount is effected by 2 different things, but won't be updated on the second time as it is already
        #   in the visitedlist (MakeChanges class). Therefore 2 other nodes are used and the total of these is the change to the current account (which is ammended in the
        #   policies_everything class).

        #This graph is also unique as it calls functions in its weights.


        graph = {
            #Interest Rates
            'Interest Rates Start' : {'InterestRates' : changedamount},
            'InterestRates' : {'CurrencyValue Start Multiple' : None, 'Consumption Start Multiple' : None, 'Businesses Start' : None},

            
            'CurrencyValue Start Multiple' : {'CurrencyValue' : listofreturns['CurrencyValue Start Multiple']},  #This calls the function CurrencyValueDeterminant which determines
                                                                                                                #   how big interest rates are compared to the USA and then gives it
                                                                                                                #   a realistic value. Without this method, the effects on the
                                                                                                                #   currency value would be unrealisitc and volatiledepending on
                                                                                                                #   the change, therefore this method is the best option.
            'CurrencyValue' : {'Imports Start' : None, 'Exports Start' : None},
            'Imports Start' : {'Imports' : self.TradeDeterminant(listofreturns['CurrencyValue Start Multiple'] - self.CurrencyValue, "Imports")},
            'Imports' : {'CurrentAccount 1' : ((self.Imports*changedamount)-self.Imports)},
            'CurrentAccount 1' : {None : None},
 
            
            'Exports Start' : {'Exports' : self.TradeDeterminant(listofreturns['CurrencyValue Start Multiple'] - self.CurrencyValue, "Exports")},
            'Exports' : {'CurrentAccount 2' : (self.Exports-(self.Exports*changedamount))}, #Should technically be new - original, but in policies_everything it is the current account 
                                                                                            #   - the newweighted value, so this must be inversed.
            'CurrentAccount 2' : {None : None},

            #No disposable income so again another function is required for consumption.
            'Consumption Start Multiple' : {'Consumption' : self.ConsumptionDeterminant(listofreturns['CurrencyValue Start Multiple'] - self.CurrencyValue)},
            'Consumption' : {'Inflation' : changedamount - 0.05, 'UnemploymentRate Start' : None},    #Inflation is affected almost equally as much as consumption.
            'Inflation' : {None : None},
            'UnemploymentRate Start' : {'UnemploymentRate' : (1-listofreturns['Consumption Start Multiple'])*-8},
            'UnemploymentRate' : {None : None},

            'Businesses Start' : {'Businesses' : 1-((listofreturns["Start"]/100)*0.95)},   #With higher interest rates, businesses can borrow less, invest less etc so are less happy.
            'Businesses' : {None : None}
        }
        

        return graph

    

    def ConsumptionDeterminant(self, changedcurrencyvalue):

        if changedcurrencyvalue < 0:
            #When it has decreased, the value has increased, which reduces inflation as saving increases and borrowing decreases reducing consumption in the economy.
            ConsumptionMultiplier = 1 + changedcurrencyvalue/3
        else:
            ConsumptionMultiplier = 1 + changedcurrencyvalue/4

        return ConsumptionMultiplier

    def CurrencyValueDeterminant(self, changedamount):

        InterestRate = changedamount + self.InterestRate    #Get the actual Interest Rate which is needed to determine the effects compared to the USD.


        #If Interest Rates are 4% and are increased to 12%, the currency value would be almost the same as if Interest Rates started at 11% and are increased to 12%.
        #   This is because the currency value is not affected by the change in interest rates, but by the actual level of interest rates, which is why this method is needed, as opposed
        #   to a geometric or arithmetic calculation (as seen with previous graphs).
        
        if InterestRate > 90:   #Which is extremely unrealisitc, but the user can do this.
            CurrencyValue = round(random.uniform(0.1, 0.15),2)
        elif InterestRate > 75:
            CurrencyValue = round(random.uniform(0.15, 0.2),2)
        elif InterestRate > 60:
            CurrencyValue = round(random.uniform(0.2, 0.25),2)
        elif InterestRate > 50:
            CurrencyValue = round(random.uniform(0.25, 0.3),2)
        elif InterestRate > 40:
            CurrencyValue = round(random.uniform(0.3, 0.35),2)
        elif InterestRate > 30:
            CurrencyValue = round(random.uniform(0.35, 0.4),2)
        elif InterestRate > 15:
            CurrencyValue = round(random.uniform(0.4, 0.45),2)
        elif InterestRate > 13:
            CurrencyValue = round(random.uniform(0.45, 0.5),2)
        elif InterestRate > 11:
            CurrencyValue = round(random.uniform(0.5, 0.6),2)
        elif InterestRate > 9:
            CurrencyValue = round(random.uniform(0.6, 0.7),2)
        elif InterestRate > 7:
            CurrencyValue = round(random.uniform(0.7, 0.8),2)
        elif InterestRate > 5:
            CurrencyValue = round(random.uniform(0.8, 0.9),2)
        elif InterestRate > 2.5:
            CurrencyValue = round(random.uniform(0.9, 0.95),2)
        elif InterestRate == 2.5:
            CurrencyValue = round(random.uniform(0.95, 1.05),2)
        elif InterestRate == 0:
            CurrencyValue = round(random.uniform(2, 2.8),2)
        elif InterestRate < 0.2:
            CurrencyValue = round(random.uniform(1.9, 2),2)
        elif InterestRate < 0.3:
            CurrencyValue = round(random.uniform(1.8, 1.9),2)
        elif InterestRate < 0.4:
            CurrencyValue = round(random.uniform(1.7, 1.8),2)
        elif InterestRate < 0.45:
            CurrencyValue = round(random.uniform(1.6, 1.7),2)
        elif InterestRate < 0.5:
            CurrencyValue = round(random.uniform(1.5, 1.6),2)
        elif InterestRate < 0.75:
            CurrencyValue = round(random.uniform(1.45, 1.5),2)
        elif InterestRate < 1:
            CurrencyValue = round(random.uniform(1.4, 1.45),2)
        elif InterestRate < 1.25:
            CurrencyValue = round(random.uniform(1.35, 1.4),2)
        elif InterestRate < 1.5:
            CurrencyValue = round(random.uniform(1.3, 1.35),2)
        elif InterestRate < 1.75:
            CurrencyValue = round(random.uniform(1.25, 1.3),2)
        elif InterestRate < 2:
            CurrencyValue = round(random.uniform(1.2, 1.25),2)
        elif InterestRate < 2.25:
            CurrencyValue = round(random.uniform(1.15, 1.2),2)
        elif InterestRate < 2.5:
            CurrencyValue = round(random.uniform(1.05, 1.15),2)
        



        return CurrencyValue

    def TradeDeterminant(self, changedcurrencyvalue, whichtrade):
        print("changedcurrencyvalue is: ", changedcurrencyvalue)
        #changedamount-self.CurrencyValue
        if whichtrade == "Imports":
            
            if changedcurrencyvalue < 0:
                #print("less than 0")
                #Then the value of the currency has increased as you can buy more USD for less.
                #Stronger currency means imports are cheaper so more people buy imports.
                ImportsMultiplier = 1 + (-changedcurrencyvalue/2)    #Will be positive as its a negative timesed by -1 added to 1.
            else:
                ImportsMultiplier = 1 + (-changedcurrencyvalue/2.5)    #In this case, the value will be less than 1 as its a positive timesed by -1 added to 1.

                
            return ImportsMultiplier

        
        elif whichtrade == "Exports":

            if changedcurrencyvalue > 0:
                #print("less than 0")
                #Then the value of the currency has decreased as you can buy less USD for more.
                #Weaker currency means exports are cheaper so other countries buy these exports.
                ExportsMultiplier = 1 + (changedcurrencyvalue/2)    #Will be positive as its a positive added to 1.
            else:
                ExportsMultiplier = 1 + (changedcurrencyvalue/2.5)    #Will be negative as its a negative added to 1.


            return ExportsMultiplier
            
#End of file: Graphs
        
        

        
if __name__ == "__main__":
    workthis = GraphCreations(1)
    graph = workthis.TaxGraph(4, 0)
   
    workthis.TestThis(graph)







