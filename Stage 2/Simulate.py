#New file: Simulate
import sys
import json
import random

import mysql.connector


sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 4\Queue")
import PriorityQueue as PQ

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")
import OtherStatements as OS

import PolicyRatingDisplay as PRD

import Main_Menu as MainMenu






class Simulate(PRD.policies_everything):

    def __init__(self, UserID):

        self.UserID = UserID
        self.policiesconfirmed = self.LoadPoliciesConfirmed()   #As policies_everything is the child class of LoadEverything and this is the child class of policies_everything, this class
                                                                #   can access all methods in those two classes.
        self.Q2Changes = self.LoadQ2PoliciesConfirmed()
        self.Q3Changes = self.LoadQ3PoliciesConfirmed()
        self.TimeLagged = self.LoadTimeLagged()
        self.listtotimelag = ['Public Investment', 'Welfare Benefits', 'Vocational Training', 'Council Housing', 'Education', 'Interest Rates']  #A list of policies with a time lag.

        self.PoliciesFailed = []

        
        print(self.policiesconfirmed)

        self.PQ = PQ.PriorityQueueFunctions(self.UserID, [], self.policiesconfirmed)

        super().__init__(None, None, self.UserID)
        self.policy_screen.destroy()


    def lengthofchanges(self, allchanges):
        #print("length is: ", len(self.allchanges))
        return len(allchanges)



    def SimulateClicked(self):

        
        #if (not self.policiesconfirmed) and (not self.TimeLagged):
        #pass
                
        if self.policiesconfirmed:    #If there is something in policiesconfirmed, ignoring whether TimeLagged has anything in it, AddToTimeLagged.
            self.AddToTimeLagged()

        elif not self.policiesconfirmed:    #If policiesconfirmed is empty but there are still policies yet to have effect (because of their time lag), run the economy.

            self.ShiftQuarters({})
            
            
            
        return self.policiesconfirmed, self.Q2Changes, self.Q3Changes, self.TimeLagged 

            

        

            #self.AddToPriorityQueue()


    def AddToTimeLagged(self):
        print("NOT EMPTY")

        tempQ3Changes = {}
        tempToRemove = []
        n = -3  #Start the value at -3 (maximum of 4 can be added, filling priorities of 0, -1, -2, -3).
        removefromPoliciesConfirmed = []
            
        for policy in reversed(self.policiesconfirmed.keys()):  #So that ones with lower priorities go first.
            if (self.policiesconfirmed[policy])[0] in self.listtotimelag:
                name = self.policiesconfirmed[policy][0]
                
                        
                if name not in self.TimeLagged: #If it hasnt already had its time lag take effect
                    print(name , " is to be time lagged") 
                    tempQ3Changes[str(n)] = self.policiesconfirmed[policy]  #Place it into a temprary dictionary.
                    tempToRemove.append(policy)
                    print("Removing ", policy)
                    self.TimeLagged.append(name)
                    n += 1 #Add 1 to n so that the next policy added (if there are any) will be further away from the start of the confirmedpolicies, meaning it is more likely to fail
                            #   (which is determined further down).
                else:   #If it has already had its time lag take effect, remove it from the time lag list
                    alreadyintimelag = False    #Create a boolean that will determine if this policy is still in time lag
                    for key, value in self.Q2Changes.items():

                        if name == value[0]:

                            removefromPoliciesConfirmed.append(policy)
                            OtherStatements = OS.ExtraStatements(self.UserID)
                            message = ("A previous change in " + str(name) + """ is still
taking effect therefore
        your new changes will have no effect!""")
                            OtherStatements.Notices(message, False, None)
                            alreadyintimelag = True #Set the boolean to true, so now the policy will not be removed from the Time Lagged and the previous one will still have effect,
                                                    #   otherwise the policy would be removed from TimeLagged but the policy will still be in Q2 or Q3 changes, causing the
                                                    #   program to crash.
                            break   #Then exit the loop and move onto the next policy
                            
                    for key, value in self.Q3Changes.items():

                        if name == value[0]:
                            print("its already been time lagged")
                            #If the user makes a change that has a time lag, but a previous change of that policy is already in its time lag stages, then
                            #   the change jsut made should be removed and the user should be informed

                            removefromPoliciesConfirmed.append(policy)
                            OtherStatements = OS.ExtraStatements(self.UserID)
                            message = ("A previous change in " + str(name) + """ is still
taking effect therefore
        your new changes will have no effect!""")
                            OtherStatements.Notices(message, False, None)
                            alreadyintimelag = True #Set the boolean to true, so now the policy will not be removed from the Time Lagged and the previous one will still have effect,
                                                    #   otherwise the policy would be removed from TimeLagged but the policy will still be in Q2 or Q3 changes, causing the
                                                    #   program to crash.
                            break   #Then exit the loop and move onto the next policy
                    if not alreadyintimelag:    #Now check if the policy is still waiting to have effects from previously, if so then don't do anything, but if it isn't,
                                                #   the policy has already had its time lag effect so is ready to effect the economy, so remove it from the TimeLagged
                        self.TimeLagged.remove(name)

        print(tempQ3Changes, " and ", tempToRemove, " and ", n)

        print("removing from policies confirmed because of a previous policy still in effect: ", removefromPoliciesConfirmed)
        #Now remove policies that are still in the time lag stage that have been confirmed again!
        for removal in removefromPoliciesConfirmed:
            del self.policiesconfirmed[removal]

        print("new policiesconfirmed after removing ones that are still time lagged is: ", self.policiesconfirmed)
        
        for toRemove in tempToRemove:
            print("Removed: ", self.policiesconfirmed[toRemove])
            del self.policiesconfirmed[toRemove]    #Remove those from the policiesconfirmed to run in the next quarter.


        self.ShiftQuarters(tempQ3Changes)



        #Now add any from Q2 into the policiesconfirmed to change in the next quarter.
    def ShiftQuarters(self, tempQ3Changes):

         #Now add any from Q2 into the policiesconfirmed to change in the next quarter.

        for policy in self.Q2Changes:
            self.policiesconfirmed[policy] = self.Q2Changes[policy]
            print(self.Q2Changes[policy])   #Again remove any policies in here from the time lagged so that they don't continuously have a time lag and never actually have an effect.
            self.TimeLagged.remove(self.Q2Changes[policy][0])

        self.Q2Changes = self.Q3Changes #Copy everything from Q3 into Q2 now
        self.Q3Changes = {} #Now reset Q3 so that new policies can be added.


        #If this method is being called directly from SimulateClicked then it is because there are effects yet to take place due to their time lag, but no policy changes set by the user
        #   in the current quarter. Therefore, tempQ3Changes won't need to as nothing is being added into Q3Changes (as nothing is in policiesconfirmed).
        #   However, if this method is being called from AddToTimeLagged then there are items in policiesconfirmed and tempQ3Changes is needed.
        
        for toAdd in tempQ3Changes.keys():
                self.Q3Changes[toAdd] = tempQ3Changes[toAdd]
                    
        print("final policiesconfirmed: ", self.policiesconfirmed)
        print("final Q2 Changes: ", self.Q2Changes)
        print("final Q3 Changes: ", self.Q3Changes)
        print("Time Lagged is: ", self.TimeLagged)

            

        
    def AddToPriorityQueue(self):

        
        
        if (not self.policiesconfirmed) and (not self.TimeLagged):
            ##There are no changes at all, but in this simulation the user MUST have at least one change.
            message = """There must be at least one
change occuring to
simulate the economy"""
            self.Error(message)
        else:
            print("before adding to priority queue policies confirmed is: ", self.policiesconfirmed)
            for key in self.policiesconfirmed.keys():
                self.PQ.enQueue(key)

            Queue = self.PQ.Queue   #Queue contains full details about the policies to be changed, with their priorities, the policyname and the changedamount.
            print("QUEUE IS: ", Queue)

            self.getOverallEffects(Queue)



        print(self.PoliciesFailed)
        return self.PoliciesFailed

 
    def getOverallEffects(self, Queue):

        self.allchanges = []

        if not self.policiesconfirmed:
            print("Nothing to simulate at this point due to all policies being time lagged")

            #Update the year only.
            getYear = OS.ExtraStatements(self.UserID)
            Year = getYear.getYear()
            print(Year)

            Year = getYear.addQuarterToYear(Year)
            print(Year)





            economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="notThePassword_321",database="economygame")
            mycursor = economygamedb.cursor()
            updatestats = ("""UPDATE Statistics SET Year = %s WHERE StatsID = %s""")
            statstoupdate = (Year[0], self.UserID)
            mycursor.execute(updatestats, statstoupdate)
            economygamedb.commit()
            
                
        else:    
            for change in Queue:
                indexofchange = Queue.index(change)
                priority = int((self.PQ.Queue[indexofchange])[0])
                policyname = self.PQ.Queue[indexofchange][1]
                changedamountforpolicy = self.PQ.Queue[indexofchange][2]
                #print(indexofchange)
                print("self.PQ.Queue[indexofchange][2] is: ", changedamountforpolicy)

                
                self.weighteddictionary = self.getOverallchanges(policyname, changedamountforpolicy)



                #Now randomise the chance that the policy does not go exactly how it was displayed and calculated when show expected changes was pressed.
                #This is calculated only for policies without a time lag, however policies with a time lag have a chance of failing. This is only if the changed amount was greater than 0
                #   (it increased). This also will apply for interest rates.
                
                
                if (priority > 0) and (policyname not in self.listtotimelag):   #Must be a change made in the current quarter and not one that is still yet to be time lagged.
                    #Based on the priority, change the expected effects. If the priority is higher, it will be more like the expected effects, but if it is lower it will be less likely.
                    probability = 0.1   #Default probability = 0.1, meaning the max for a policy of highest priority is 0.1
                    probabilitymultiplier = priority - random.uniform(0, 1) #This means the the policy with the highest priority could have a 0 chance of having any changes.
                    
                    probability = probability * probabilitymultiplier

                    if probability != 0:    #If it is, skip this as the values won't change and the dictionary will be iterated through for no reason.
                        
                        if random.uniform(0, 1) < 0.5:
                            change = -1  #Will dicrease the value
                        else:
                            change = +1  #Will increase the value
                                
                        for policyname, changedamount in self.weighteddictionary.items():
                            if policyname == 'GovernmentSpending':
                                    pass
                            else:
                                randomvalue = random.uniform(0, 1)
                                if randomvalue < probability:    #If the generated random value is less than the generated probability (based on its priority), change the value

                                    
                                    if policyname == 'UnemploymentRate':
                                        amounttochangeby = random.uniform(0.5, 1.5)
                                    elif policyname == 'Imports' or policyname == 'Exports':    #Never randomly affect current account directly as this won't change the import and export
                                                                                                #   values therefore the value of exports-imports will not = currentaccount.
                                        amounttochangeby = random.uniform(10, 20)
                                    else:
                                        amounttochangeby = random.uniform(0.05, 0.15)   #Cannot be too big

                                    newchangedamount = changedamount + (change*amounttochangeby)
                                    print(policyname, " was randomly affected by: ", (change*amounttochangeby))
                                    self.weighteddictionary[policyname] = newchangedamount


                else:   #If the priority <= 0
                    if changedamountforpolicy > 0:   #If the amount spent on the policy has increased, it has a chance of failing and the money will have been wasted.
                        probability = 0.2
                        #Use the index of change to determine its probability of failure.

                        probabilitymultiplier = (indexofchange+1) - random.uniform(0, 1)
                        probabilityoffailure = probability * probabilitymultiplier
                        print("PROBABILITY OF FAILURE IS: ", probabilityoffailure)
                        
                        if probabilityoffailure != 0:   #Again, if it is then skip it to prevent iterating an extra time through a policy for no reason.
                
                            failedchance = random.uniform(0,0.5)
                            print("probabilty of failure is: ", probabilityoffailure, " and failed chance is: ", failedchance)
                            failed = False
                            if failedchance < probabilityoffailure:
                                failed = True

                            print("FAILED CHANCE IS: ", failedchance)


        
                            if failed:  #The effects will all fail, except for the spending
                                self.PoliciesFailed.append(policyname)    #The name of the policy that failed is added to a list of failed policies for the quarter.

                                haveFailed = [] #The list of individual economic factors that failed to change.

                                for policyname in self.weighteddictionary.keys():    #The value is not needed here.

                                    if (policyname == "GovernmentSpending") or (policyname == "NationalDebt"):
                                        pass
                                    else:
                                        haveFailed.append(policyname) #Cannot just remove from the dictionary self.weighteddcitonary here as it is being iterated through so its size
                                                                    #   can not change.

                                for policyname in haveFailed:
                                    print(policyname, " failed")
                                    del self.weighteddictionary[policyname]
                                    

                                    
                                    

                            
                        

                    
                    
                print("AFTER RANDOM CHANGES: ", self.weighteddictionary)
                            
                        
                            
                        
                
                self.allchanges.append(self.weighteddictionary)


            #print("all the changes are: ", self.allchanges)

            for self.weighteddictionary in self.allchanges:   #For every policy change, get the weighted dictionary returned from it.
                #print(self.weighteddictionary)
                indexofweighteddictionary = self.allchanges.index(self.weighteddictionary)
                nextchange = indexofweighteddictionary + 1  #Get the element's (changes) index that is after the change being looked at.
                lookedat = []
                print("NEXT CHANGE IS: ", nextchange)
                if nextchange < self.lengthofchanges(self.allchanges):  #If the nextchange is not equal to or greater than the total size, then we know we are not looking at the last change
                                                                   #    in the list self.allchanges. This means that final changes have not all been calculated yet.
                    self.UpdateValues(nextchange, indexofweighteddictionary, lookedat)

                else:
                    lastelement = self.allchanges[self.lengthofchanges(self.allchanges)-1]    #Gets the last element in all changes.
                    #Everything effected needs to be in this dictionary, however some economic factors aren't in this last element. If they aren't, add them in.
                    for element in reversed(self.allchanges):    #Must be reversed otherwise the values before being updated with other elements would be used.
                        if element != lastelement:  #Don't include the last element as this is the dictionary being used to calculate the final effects and would waste a loop
                                                    #   as it is comparing with itself.
                            for name in element.keys():
                                if name not in lastelement: #If its not there then add it in.
                                    print(name, " is not in the last element")
                                    lastelement[name] = element[name]
                                else:
                                    print(name, " is already in the last element")
                        
                    print("final and successful is: ", lastelement)
            finalfigures = self.change_figures(lastelement)
            print("Final Figures are: ", finalfigures)


            #There still may be factors that weren't affected by any of the policy changes, however these will not yet be in the finalfigures.
            #These need to be added. When updated into the database, these values will just be kept the same.
            for effect in self.namesoffigures:
                if effect not in finalfigures:
                    print("effect not in final figures is: ", effect)
                    #if (effect = "CurrentAccount") or effect == "UnemploymentRate" or effect == "GovernmentSpending" or effect == "CurrentAccount"):
                    finalfigures[effect] = eval(("self." + effect)) #Thes
                    #finalfigures[effect] = 1
            self.ShowEffects(finalfigures)



                
        
       
    def UpdateValues(self, nextchange, indexofweighteddictionary, lookedat):

        for key in self.weighteddictionary.keys():  #For every key in the self.weighteddictionary/ change being looked at, find the closest element to it (in the list self.allchanges) 
                                                    #   that has the same key (therefore the same economic factor is being affected).
                                                                               
            if key in self.allchanges[nextchange]:   #If the key in the current changed dictionary is in the next changed dictionary, then update that keys value in the nextchange
                                                            #   dictionary. This is timesing the values or addidtion or subtraction depending on the factor being affected.



                if key not in lookedat:
                    
                    #print("key in both is: ", key, " between index: ", indexofweighteddictionary, " and ", nextchange)
                    nextweighteddictionary = self.allchanges[nextchange]
                    nameoffactor = key  #The key represent the actual economic factor being changed.
                                

                    newvalue = self.calculateNewValue(self.weighteddictionary[key], nextweighteddictionary[key], nameoffactor)
                    #print(key, " HAS A NEW VALUE OF: ", newvalue, " at the index: ", nextchange)

                                
                                
                    print("new change for: ", key, " is: ", newvalue)
                    nextweighteddictionary[key] = newvalue
                    lookedat.append(key)    #So that the value is changed only once throughout the whole listofchanges, otherwise the final value would be two times bigger.

            else:
                print("key not in either is: ", key, " between index: ", indexofweighteddictionary, " and ", nextchange)
                if nextchange + 1 < self.lengthofchanges(self.allchanges):
                    nextchange = nextchange + 1
                    self.UpdateValues(nextchange, indexofweighteddictionary, lookedat)
                else:   #This factor is not being affected by any of the changes ahead of it in the list so move onto the next one.
                    break

    def getOverallchanges(self, policyname, changedamount):

        

        self.weighteddictionary = self.getChangedFigures(changedamount, policyname) 

        return self.weighteddictionary







    
        
    def calculateNewValue(self, firstvalue, secondvalue, nameoffactor):

        if (nameoffactor == "CurrentAccount") or (nameoffactor == "UnemploymentRate") or (nameoffactor == "GovernmentSpending"):
            newvalue = firstvalue + secondvalue                                 #Add these as, in changed figures the final value is calculated by minusing the new generated value
                                                                                #   from the original. Therefore here they must be added.
                                                                                #   Eg: For the current account, 20 + 30 means the current account will worsen by £50 million
                                                                                #   so they must be added.
        else:
            newvalue = firstvalue * secondvalue

        return newvalue
        
    
        


    def ShowEffects(self, finalfigures):


        #Update all database values, even if they remained the same
        self.UpdateDatabase(finalfigures)

        

        #Display the changed effects using menu_main.policy_showratings()
        
        #mainmenu = MainMenu.menu_main(self.UserID)
        #mainmenu.mainmenu_screen.destroy()
        #mainmenu.mainmenu_screen.update()
        
        
        #mainmenu.policy_showratings()

    def UpdateDatabase(self, finalfigures):
        
        getYear = OS.ExtraStatements(self.UserID)
        Year = getYear.getYear()
        print(Year)

        Year = getYear.addQuarterToYear(Year)
        print(Year)
        
        
        self.namesoffigures = [
            'HighIncome', 'Pensioners', 'MiddleIncome', 'Unemployed', 'LowIncome', 'Businesses', 'Overall',
            'NationalDebt', 'CurrentAccount', 'UnemploymentRate', 'Inflation', 'GDP', 'Year',
            'CurrencyValue', 'TaxRevenue', 'GovernmentSpending', 'DisposableIncome', 'MPC', 'Imports', 'Exports',
                            ]
        

        HighIncome = (finalfigures['HighIncome']/100)
        Pensioners = (finalfigures['Pensioners']/100)
        MiddleIncome = (finalfigures['MiddleIncome']/100)
        Unemployed = (finalfigures['Unemployed']/100)
        LowIncome = (finalfigures['LowIncome']/100)
        Businesses = (finalfigures['Businesses']/100)
        Overall = ((HighIncome + Pensioners + MiddleIncome + Unemployed + LowIncome + Businesses)/6)
        NationalDebt = round(finalfigures['NationalDebt'], 2)
        UnemploymentRate = round(finalfigures['UnemploymentRate'], 2)
        InflationRate = round(finalfigures['Inflation'], 2)
        GDP = round(finalfigures['GDP'], 2)
        Year = Year[0]
        CurrencyValue = round(finalfigures['CurrencyValue'], 2)
        TaxRevenue = round(finalfigures['TaxRevenue'], 2)
        GovernmentSpending = round(finalfigures['GovernmentSpending'], 2)
        BudgetBalance = TaxRevenue - GovernmentSpending
        DisposableIncome = round(finalfigures['DisposableIncome'], 2)
        MPC = round(finalfigures['MPC'], 2)
        Imports = round(finalfigures['Imports'], 2)
        Exports = round(finalfigures['Exports'], 2)
        CurrentAccount = Exports - Imports

        print("CURRENCY VALUE IS: ", CurrencyValue)



        

        for policykey in self.policiesconfirmed.keys():
            policyname = self.policiesconfirmed[policykey][1]   #The name of the policy is the second element as it is now stored in the order : priority, policyname, changedamount.
            policyname = policyname.replace(" ", "")
            changedamount = self.policiesconfirmed[policykey][2]    #The changed amount is the third element in the list.
            newvalue = eval("self." + policyname) + changedamount
            
            if policyname == "IncomeTax":
                self.IncomeTax = newvalue
            elif policyname == "ExciseDuty":
                self.ExciseDuty = newvalue
            elif policyname == "NationalInsurance":
                self.NationalInsurance = newvalue
            elif policyname == "CorporationTax":
                self.CorporationTax = newvalue
            elif policyname == "ValueAddedTax":
                self.ValueAddedTax = newvalue
            elif policyname == "CarbonTax":
                self.CarbonTax = newvalue

            elif policyname == "SocialProtection":
                self.SocialProtection = newvalue
            elif policyname == "Education":
                self.Education = newvalue
            elif policyname == "Health":
                self.Health = newvalue
            elif policyname == "Defence":
                self.Defence = newvalue

            elif policyname == "InterestRates":
                self.InterestRates = newvalue

            elif policyname == "PublicInvestment":
                self.PublicInvestment = newvalue
            elif policyname == "WelfareBenefits":
                self.WelfareBenefits = newvalue
            elif policyname == "VocationalTraining":
                self.VocationalTraining = newvalue
            elif policyname == "CouncilHousing":
                self.CouncilHousing = newvalue


        economygamedb = mysql.connector.connect(host="localhost",user="root",passwd="notThePassword_321",database="economygame")
        mycursor = economygamedb.cursor()

        updateratings = ("""UPDATE Ratings SET HighIncome = %s,
                                            MiddleIncome = %s,
                                            LowIncome = %s,
                                            Pensioners = %s,
                                            Unemployed = %s,
                                            Businesses = %s,
                                            Overall = %s WHERE RatingsID = %s""")
        ratingstoupdate = (HighIncome, MiddleIncome, LowIncome, Pensioners, Unemployed, Businesses, Overall, self.UserID)

        
        updatestats = ("""UPDATE Statistics SET NationalDebt = %s,
                                            CurrentAccount = %s,
                                            UnemploymentRate = %s,
                                            InflationRate = %s,
                                            GDP = %s,
                                            Year = %s WHERE StatsID = %s""")
        statstoupdate = (NationalDebt, CurrentAccount, UnemploymentRate, InflationRate, GDP, Year, self.UserID)


        updateextrastats = ("""UPDATE ExtraStatistics SET BudgetBalance = %s,
                                            CurrencyValue = %s,
                                            TaxRevenue = %s,
                                            GovernmentSpending = %s,
                                            DisposableIncome = %s,
                                            MPC = %s,
                                            Imports = %s,
                                            Exports = %s WHERE ExtraStatsID = %s""")
        extrastatstoupdate = (BudgetBalance, CurrencyValue, TaxRevenue, GovernmentSpending, DisposableIncome, MPC, Imports, Exports, self.UserID)


        updatetaxes = ("""UPDATE FiscalTaxes SET IncomeTax = %s,
                                            ExciseDuty = %s,
                                            NationalInsurance = %s,
                                            CorporationTax = %s,
                                            CarbonTax = %s,
                                            VAT = %s WHERE TaxesID = %s""")
        taxestoupdate = (self.IncomeTax, self.ExciseDuty, self.NationalInsurance, self.CorporationTax, self.CarbonTax, self.ValueAddedTax, self.UserID)


        updatespending = ("""UPDATE FiscalSpending SET SocialProtection = %s,
                                            Education = %s,
                                            Health = %s,
                                            Defence = %s WHERE SpendingID = %s""")
        spendingtoupdate = (self.SocialProtection, self.Education, self.Health, self.Defence, self.UserID)


        updateinterestrates = ("""UPDATE MonetaryPolicies SET InterestRate = %s WHERE MonetaryID = (%s)""")
        interestratestoupdate = (self.InterestRates, self.UserID)


        updateSSP = ("""UPDATE SupplySidePolicies SET PublicSectorInvestment = %s,
                                            WelfareBenefits = %s,
                                            VocationalTraining = %s,
                                            CouncilHousing = %s WHERE SupplySideID = %s""")
        SSPtoupdate = (self.PublicInvestment, self.WelfareBenefits, self.VocationalTraining, self.CouncilHousing, self.UserID)



        updatepoliciesconfirmed = ("""UPDATE PoliciesConfirmed SET Q2Changes = %s,
                                                                Q3Changes = %s,
                                                                TimeLagged = %s WHERE ConfirmedID = %s""")
        policiesconfirmedupdates = (json.dumps(self.Q2Changes), json.dumps(self.Q3Changes), json.dumps(self.TimeLagged), self.UserID)
                                                                
        

        #Could be done using a for loop however the difference in efficiency is only marginal. (with a dictionary)
        mycursor.execute(updateratings, ratingstoupdate)
        mycursor.execute(updatestats, statstoupdate)
        mycursor.execute(updateextrastats, extrastatstoupdate)
        mycursor.execute(updatetaxes, taxestoupdate)
        mycursor.execute(updatespending, spendingtoupdate)
        mycursor.execute(updateinterestrates, interestratestoupdate)
        mycursor.execute(updateSSP, SSPtoupdate)

        mycursor.execute(updatepoliciesconfirmed, policiesconfirmedupdates)
    
        economygamedb.commit()


        print("POLICIES CONFIRMED AT THE END ARE STILL: ", self.policiesconfirmed)

#End of file: Simulate




        
        







if __name__ == "__main__":

    simulate = Simulate(1)
    #simulate.getOverself.allchanges()
    #simulate.AddToPriorityQueue()
    #simulate.AddToPriorityQueue()
    simulate.AddTimeLaggedPolicies()







    






















    

    
