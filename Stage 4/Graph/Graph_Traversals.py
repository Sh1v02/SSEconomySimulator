#New file: Graph_Traversals
import Graphs

import sys
sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")    #Load_Everything
import Load_Everything as LE


class MakeChanges(Graphs.GraphCreations):

    def __init__(self, UserID, policyname):

        self.UserID = UserID
        self.policyname = policyname

        super().__init__(self.UserID)
        
        #self.visitedlist = visitedlist
        #self.weightslist = weightslist


        #Load everything so that the actual values can be taken and the weights that were calculated through the traversal can be applied to the values to change the actual values.
        #This class is the child class of GraphCreations which is the child class of LoadEverything so has all methods that are protected from both classes.
        #self.IncomeT, self.ExciseD, self.NationalI, self.CorpT, self.VAT, self.CarbonT = self.LoadFiscalTaxes(None, None, None, None, None, None)
        #self.ratings, self.HighIncome, self.Pensioners, self.MiddleIncome, self.Unemployed, self.LowIncome, self.Business, self.Overall = self.LoadRatings(None, None, None, None, None, None, None)
        #self.NationalDebt, self.CurrentAccount, self.UnemploymentRate, self.Inflation, self.GDP, self.Year = self.LoadStatistics(None, None, None, None, None, None)
        #self.TaxRevenue, self.DisposableIncome, self.MPC, self.Imports, self.Exports = self.LoadExtraStatistics(None, None, None, None, None)


    

    def dfs(self, graph, CurrentVertex, visited, weights, listofreturns):

        #print(listofreturns)

        if ("Start" not in CurrentVertex):
            visited.append(CurrentVertex)
        #print("Current Vertex is : ", CurrentVertex)
        #print(" ")
        
        for vertex in graph[CurrentVertex]:     #TAKE EACH NODE CONNECTED TO THE CURRENT VERTEX
            
            for key, value in graph.items():    #To be able to access any node's weight, not just the last weight added, we must add any node which has many children to a dictionary.
                                                #Every node that has more than one child will have another node with the same name but 'Start' added to it.
                                                #This nested for loop nested inside the main for loop will add every node that has more than one child and its weight so it can be accessed
                                                #   at any time.

                                                
                if 'Start Multiple' in key:     #If Start Multiple is in the nodes name then it has multiple children therefore will have its weight referenced to by another node
                                                #   in the graph, so a dictionary is used so that it can be referenced.
                    for key1 in value:

                        listofreturns[key] = value[key1]    #Add to the dictionary with key of key the value of value[key1]

                
                
                if key == vertex:           #IF THE KEY BEING LOOKED AT IS THE VERTEX THEN TRAVERSE FROM THERE

                    #print("the key is : ", key)
                    #print("the value is : ", value)

                    nextvertex = key        #SET THE NEXT VERTEX TO BE VISITED = TO THE KEY
                    
                    if vertex not in visited:
                        
                        for key1 in value:      #NOW LOOK AT THE NESTED DICTIONARY
                            #print("VALUE1 IS ",key1)
                            #print("key is ", value, value[key1])
                            weighttoappend = value[key1]    #TAKE THE VALUE
                            
                                              
                            #print(key1, ": ", weighttoappend)
                                
                                
                            if weighttoappend != None:      #NEEDED AS WITHOUT THIS, IT WOULD NOT APPEND THE KEY TO THE LIST
                                
                                weights.append(weighttoappend)     #ADD THE WEIGHT TO THE WEIGHT LIST


                                newamount = weighttoappend      #MUST CREATE A NEW CHANGED AMOUNT VALUE AND PASS IT THROUGH AS EACH NODE WILL AFFECT ANOTHER NODE
                                                                #   DIFFERENTLY TO ANOTHER! OTHERWISE IT WOULD BE POINTLESS
                                                                #THE NEW CHANGED AMOUNT VALUE WILL BE THE WEIGHT OF THE LAST NODE ADDED

                                
                    

                                #Must reload the graph and by doing this the graph can be updated with any listofreturn values along with the new changedamount (newamount)
                                #   being passed through.
                                #Can use self as its inheriting GraphCreations
                                if self.policyname == "Income Tax":
                                    graph = self.IncomeTaxGraph(newamount,listofreturns)
                                elif self.policyname == "Corporation Tax" or self.policyname == "Carbon Tax":
                                    graph = self.CorporationCarbonTaxGraph(newamount,listofreturns)
                                elif self.policyname == "National Insurance":
                                    graph = self.NationalInsuranceGraph(newamount, listofreturns)
                                elif self.policyname == "Value Added Tax":
                                    graph = self.VATGraph(newamount, listofreturns)
                                elif self.policyname == "Excise Duty":
                                    graph = self.ExciseDutyGraph(newamount, listofreturns)
                                elif self.policyname == "Social Protection":
                                    graph = self.SocialProtectionGraph(newamount, listofreturns)
                                elif self.policyname == "Health" or self.policyname == "Education":
                                    graph = self.HealthEducationGraph(newamount, listofreturns, self.policyname)
                                elif self.policyname == "Defence":
                                    graph = self.DefenceGraph(newamount, listofreturns)
                                elif self.policyname == "Public Investment":
                                    graph = self.PublicInvestmentGraph(newamount, listofreturns)
                                elif self.policyname == "Welfare Benefits":
                                    graph = self.WelfareBenefitsGraph(newamount, listofreturns)
                                elif self.policyname == "Vocational Training":
                                    graph = self.VocationalTrainingGraph(newamount, listofreturns)
                                elif self.policyname == "Council Housing":
                                    graph = self.CouncilHousingGraph(newamount, listofreturns)
                                elif self.policyname == "Interest Rates":
                                    graph = self.InterestRatesGraph(newamount, listofreturns)
                                
                                    
                                                                          
                            
                            if nextvertex not in visited:   #THIS IS NEEDED AGAIN AS ONCE THE TRAVERSAL TRACKS ALL THE WAY BACK TO A VERTEX WITH MULTIPLE LINKS IT WILL RE ADD IT AS IT IS
                                                            #   ALREADY INSIDE THE LOOP THERFORE NEEDS RE VALIDATING
                                
                                
                                runthis = MakeChanges(self.UserID, self.policyname)
                                runthis.dfs(graph,nextvertex,visited, weights, listofreturns)  #RECURSION TO THEN MOVE ONTO THE NEXT NODE FOLLOWING THE DEPTH FIRST TRAVERSAL 
                                
        
        
        return visited, weights




    def RunTaxGraph(self, startpoint, changedamount):
        print("CHANGED AMOUNT : ", changedamount)

        #For some polciies, such as income tax, the graph is different so the listofreturns is different (such as ValueForUnemployment).
        #MUST BE 0 AND NOT NONE AS CANNOT CARRY OUT INTEGER OPERATIONS UNLESS ITS AN INTEGER
        listofreturns = {'Start' : changedamount, 'Disposable Income Start Multiple' : 2,
                         'Consumption Start Multiple' : 0, 'Low Income Earners Start' : 0,
                         'UnemploymentRate Start Multiple' : 0, 'Businesses Start Multiple' : 0,
                         '%change' : 0, 'CurrencyValue Start Multiple' : 0,
                         'CurrentAccount 1 Start Multiple' : 0, 'Exports' : 0}                       #Must have the name of all
                                                                                                           #   return nodes in the dictionary
                                                                                                           #   first.

        #Getting the GraphCreation class which contains all graphs
        #GetGraph = Graphs.GraphCreations(self.UserID)
        
        if self.policyname == "Income Tax":
            listofreturns['ValueForUnemployment'] = changedamount
            graph = self.IncomeTaxGraph(changedamount, listofreturns) 
        elif self.policyname == "Corporation Tax":
            listofreturns['ValueForUnemployment'] = changedamount/2
            graph = self.CorporationCarbonTaxGraph(changedamount, listofreturns)
        elif self.policyname == "National Insurance":
            listofreturns['ValueForUnemployment'] = changedamount/2
            graph = self.NationalInsuranceGraph(changedamount, listofreturns)
        elif self.policyname == "Value Added Tax":
            listofreturns['ValueForUnemployment'] = changedamount/2.5
            graph = self.VATGraph(changedamount, listofreturns)
        elif self.policyname == "Excise Duty":
            listofreturns['ValueForUnemployment'] = changedamount/3
            graph = self.ExciseDutyGraph(changedamount, listofreturns)
        elif self.policyname == "Carbon Tax":
            listofreturns['Start'] = listofreturns['Start']/1.1 #As disposable income is not affected in the simulation by the carbon tax, the only thing affected/ that uses the Start
                                                                #   value in listofreturns is businesses. Businesses are less affected by a carbon tax than by corporation tax and
                                                                #   although they are in the same graph, this will change the effects on businesses compared to corporaton tax.
            listofreturns['ValueForUnemployment'] = changedamount/4
            graph = self.CorporationCarbonTaxGraph(changedamount, listofreturns)
        elif self.policyname == "Interest Rates":
            #print("original currency value: ", self.CurrencyValue)
            #print(self.InterestRate)
            listofreturns['CurrencyValue Start Multiple'] = self.CurrencyValueDeterminant(changedamount)
            #Originally, the line above was set in the graph weight for CurrencyValue Start Multiple, however whenever referred to by its child nodes (Imports and Exports) it would
            #   run the CurrencyValueDeterminant function again, generating a different value for imports and exports to use. Therefore by setting it outside of the graph, the value will
            #   remain constant as it is not constantly being re-called when referred to.
            graph = self.InterestRatesGraph(changedamount, listofreturns)

            
        
        #print(listofreturns)

        #for key, value in graph.items():        #Needed so that a base weight is given to income tax so that all other weights can be processed. Without this loop the income tax weight
         #                                       #   will remain at 0 and all other nodes that depend on it as well.
          #  if key == startpoint:
           #     for key1 in value:
            #        
             #       
              #      listofreturns[key] = value[key1]
        #listofreturns["Start"] = changedamount


        print("CHANGED AMOUNT : ", changedamount)
        
        visitedlist, weightslist = self.dfs(graph,startpoint, [], [], listofreturns)   #LAST ONE IS RETURN TO STACK/LIST

        
        #print(visitedlist)
        #print(weightslist)

        
        
    
        print("")

        weightscounter = 0
        visitedcounter = 1     #Starts on 1 so that the first node isnt included as this won't be given an actual weight
        weighteddictionary = {}
        for i in weightslist:
            print(visitedlist[visitedcounter], weightslist[weightscounter])

            weighteddictionary[visitedlist[visitedcounter]] = weightslist[weightscounter]  #Add the combination to the dictionary with the key being the node name and value the change
            
            weightscounter += 1
            visitedcounter += 1
            

        #newval = eval(visitedlist[6])
        #print("original new val is ", newval, " and its being multiplied by ", weightslist[5])
        
        #newval = (newval * weightslist[5])/100

        #print(weighteddictionary)
        #print("actual value in database for ", visitedlist[6], " is ", weightslist[5]) #USED SO THAT THE ACTUAL INCOMET VALUE IS DISPLAYED
        #print("timesing ", self.Imports, " by ", weighteddictionary['Imports'])
        #print(self.Imports * weighteddictionary['Imports'])
        
        #print((weighteddictionary['Consumption']-1)/ (weighteddictionary['DisposableIncome']-1))

        #NOW MAKE ANOTHER DICITONARY WHERE IT APPENDS THE FINAL CHANGED VALUES OR MAYBE THE SAME DICTIOANRY BUT JUST UPDATES THEM
        #THEN U CAN REFER TO THE DICTIONARY USING A FOR LOOP WITH KEY AS OPPOSED TO AN ACTUAL NAME
        #ALREADY STARTED THIS WITH DICTIONARY NAME weighteddictionary
        
        return weighteddictionary   #So that all can be accessed












    def RunSpendingGraph(self, startpoint, changedamount):




        #Get the actual value of the policy we are changing, so remove the spaces and add self and evaluate it to get the
        #   actual value.
        original = eval("self." + self.policyname.replace(" ", "")) 
        #Rather than passing newvalue (which is the slider value) through several different methods through several different classes, the slider value can be obtained again just by
        #   rearranging the equation from the policy class (newvalue = changedamount - self.nameofpolicy).
        #The newvalue and original are needed together to calculate the changedamount as a percentage, not as a value itself as spending can increase by very large amounts, so changes 
        #   need to be represented as percentages.
        #The changed amount could not be converted to a percentage in the actual policy class as the raw figure (before % is calculated) is needed for some of the node (such as GSpending).
        
        newvalue = changedamount + original
        if original == 0:   #If original is 0, then dividing by the original (0) will produce an error. Just calulcate percentage change by subtracting the original (0) from the newvalue.
            changedamountpercentage = float(newvalue-original)
        else:
            changedamountpercentage = ((float(newvalue-original))/float(original))*100  #Float so that it is never dividing by 0.
        
        #Append this to the dictionary so it can be accessed in the graphs.

        
        #For some polciies, such as income tax, the graph is different so the listofreturns is different (such as ValueForUnemployment).
        
        listofreturns = {'Start' : changedamount, '%change' : changedamountpercentage, 'Disposable Income Start Multiple' : 0,
                         'Consumption Start Multiple' : 0, 'Low Income Earners Start' : 0,
                         'UnemploymentRate Start Multiple' : 0, 'Businesses Start Multiple' : 0, 'Exports Start Multiple' : 0}
                        #Must have the name of all return nodes in the dictionary first. The values must be 0 as operations cannot be performed on type None, even though these values will
                        #   be changed almost instantly.

        print(listofreturns['%change'])                                                                                                   
        

        
        #Getting the GraphCreation class which contains all graphs

        #The value that listofreturns['%change'] is divided by is based on which one normally impacts the economy the most based off of research.
        #Some polcicies, such as Education has a time lag (it takes a while for the effects to occur).
        if self.policyname == "Social Protection":
            graph = self.SocialProtectionGraph(changedamount, listofreturns)
        elif self.policyname == "Health":
            listofreturns['%change'] = listofreturns['%change']/2
            graph = self.HealthEducationGraph(changedamount, listofreturns, self.policyname)
        elif self.policyname == "Education":
            listofreturns['%change'] = listofreturns['%change']/1.85
            graph = self.HealthEducationGraph(changedamount, listofreturns, self.policyname)
        elif self.policyname == "Defence":
            graph = self.DefenceGraph(changedamount, listofreturns)
        elif self.policyname == "Public Investment":
            graph = self.PublicInvestmentGraph(changedamount, listofreturns)
        elif self.policyname == "Welfare Benefits":
            listofreturns['ValueForUnemployment'] = listofreturns['%change']/14    #This ssp effects the unemployment rate
            graph = self.WelfareBenefitsGraph(changedamount, listofreturns)
        elif self.policyname == "Vocational Training":
            listofreturns['ValueForUnemployment'] = listofreturns['%change']/14    #This ssp effects the unemployment rate
            graph = self.VocationalTrainingGraph(changedamount, listofreturns)
        elif self.policyname == "Council Housing":
            graph = self.CouncilHousingGraph(changedamount, listofreturns)
            
            
       

        print("CHANGED AMOUNT : ", changedamount)
        
        visitedlist, weightslist = self.dfs(graph,startpoint, [], [], listofreturns)   #LAST ONE IS RETURN TO STACK/LIST


        
    
        #print("")
        #print(visitedlist)
        #print(weightslist)
        weightscounter = 0
        visitedcounter = 1     #Starts on 1 so that the first node isn't included as this won't be given an actual weight
        weighteddictionary = {}
        for i in weightslist:
            print(visitedlist[visitedcounter], weightslist[weightscounter])

            weighteddictionary[visitedlist[visitedcounter]] = weightslist[weightscounter]  #Add the combination to the dictionary with the key being the node name and value the change
            
            weightscounter += 1
            visitedcounter += 1
            

        
        
        return weighteddictionary   #So that all can be accessed


#End of file: Graph_Traversals









        
if __name__ == "__main__":
    startpoint = ""
    choiceoftype = input("t for tax s for spending: ")

    if choiceoftype.lower() == "t":
        
        while startpoint != "x":
            
            startpoint = input("Enter a start location: ")
            changedval = float(input("Enter a changed value: "))

            
            runthisthing = MakeChanges(1, startpoint)
            runthisthing.RunTaxGraph(startpoint + " Start", changedval)
            print("")

    elif choiceoftype.lower() == "s":

        while startpoint != "x":
            
            startpoint = input("Enter a start location: ")
            changedval = float(input("Enter a changed value: "))

            
            runthisthing = MakeChanges(1, startpoint)
            runthisthing.RunSpendingGraph(startpoint + " Start", changedval)
            print("")

        
    


        
