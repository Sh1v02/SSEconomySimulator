import Graphs

import sys
sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Databases")    #Load_Everything
import Load_Everything as LE

class MakeChanges():

    def __init__(self, UserID):

        self.UserID = UserID
        #self.visitedlist = visitedlist
        #self.weightslist = weightslist

        
        

    def TaxOne(self):

        x = 0
        n = 1
        value = 4

        #print(self.visitedlist, self.weightslist)
        for i in self.weightslist:
            print(self.visitedlist[n], self.weightslist[x])
            x += 1
            n += 1


    def dfs(self, graph, CurrentVertex, visited, weights, listofreturns):

    

        if ("Start" not in CurrentVertex):
            visited.append(CurrentVertex)
        #print("Current Vertex is : ", CurrentVertex)
        #print(" ")
        
        for vertex in graph[CurrentVertex]:     #TAKE EACH NODE CONNECTED TO THE CURRENT VERTEX
            
            
            for key, value in graph.items():    #To be able to access any node's weight, not just the last weight added, we must add any node which has many children to a dictionary.
                                                #Every node that has more than one child will have another node with the same name but 'Start' added to it.
                                                #This nested for loop nested inside the main for loop will add every node that has more than one child and its weight so it can be accessed
                                                #   at any time.
                if "StartM" in key:            #key == "Disposable Income Start" or key == "Demand Start" or key == :
                    for key1 in value:
                        
                        
                        listofreturns[key] = value[key1]

                
                #print(" ")
                
                
                if key == vertex:           #IF THE KEY BEING LOOKED AT IS THE VERTEX THEN TRAVERSE FROM THERE

                    #print("the key is : ", key)
                    #print("the value is : ", value)

                    nextvertex = key        #SET THE NEXT VERTEX TO BE VISITED = TO THE KEY
                    
                    if vertex not in visited:
                        
                        for key1 in value:      #NOW LOOK AT THE NESTED DICTIONARY
                            #print("VALUE1 IS ",key1)
                            
                            weighttoappend = value[key1]    #TAKE THE VALUE
                            #print(key1, ": ", weighttoappend)



                            
                            #if "Start" in vertex:
                             #   pass

                              #  returnto.append(weighttoappend)
                               # print("appending ", weighttoappend, key1)
                                #print(returnto)

                                
                                
                            if weighttoappend != None:      #NEEDED AS WITHOUT THIS, IT WOULD NOT APPEND THE KEY TO THE LIST
                                weights.append(weighttoappend)     #ADD THE WEIGHT TO THE WEIGHT LIST


                                
                                newamount = weighttoappend
                                GetGraph = Graphs.GraphCreations(self.UserID)   #MUST CREATE A NEW CHANGED AMOUNT VALUE AND PASS IT THROUGH AS EACH NODE WILL AFFECT ANOTHER NODE
                                                                                #   DIFFERENTLY TO ANOTHER! OTHERWISE IT WOULD BE POINTLESS
                                                                                #THE NEW CHANGED AMOUNT VALUE WILL BE THE WEIGHT OF THE LAST NODE ADDED
                                graph = GetGraph.TaxGraph(newamount, listofreturns)
                            #else:
                             #   pass
                              #  if len(returnto) > 1:
                               #     
                                #    newamount = returnto.pop(0)
                                 #   print(returnto)
#
 #                                   GetGraph = Graphs.GraphCreations(self.UserID)   #MUST CREATE A NEW CHANGED AMOUNT VALUE AND PASS IT THROUGH AS EACH NODE WILL AFFECT ANOTHER NODE
  #                                                                                  #   DIFFERENTLY TO ANOTHER! OTHERWISE IT WOULD BE POINTLESS
   #                                                                                 #THE NEW CHANGED AMOUNT VALUE WILL BE THE WEIGHT OF THE LAST NODE ADDED
    #                                graph = GetGraph.TaxGraph(newamount, startval)

                                    
                                
                      
                                                
                                
                                     
                            
                            
                            
                            if nextvertex not in visited:   #THIS IS NEEDED AGAIN AS ONCE THE TRAVERSAL TRACKS ALL THE WAY BACK TO A VERTEX WITH MULTIPLE LINKS IT WILL RE ADD IT AS IT IS
                                                            #   ALREADY INSIDE THE LOOP THERFORE NEEDS RE VALIDATING
                                
                                #print("MOVING ON")
                                runthis = MakeChanges(1)
                                runthis.dfs(graph,nextvertex,visited, weights, listofreturns)  #RECURSION TO THEN MOVE ONTO THE NEXT NODE FOLLOWING THE DEPTH FIRST TRAVERSAL 
                                
        
        
        return visited, weights






    def RunTaxGraph(self, startpoint, changedamount):
        
        #startpoint = input("Enter startpoint ")
        #startpoint = startpoint + " Start"
        
        GetGraph = Graphs.GraphCreations(self.UserID)
        
        listofreturns = {'Income Tax Start' : 0, 'Disposable Income Start' : 0, 'Demand Start' : 0, 'Low Income Earners Start' : 0}   #Must have the name of all return nodes in the dictionary first
        graph = GetGraph.TaxGraph(changedamount,listofreturns)     #MUST BE 0 AND NOT NONE AS CANNOT CARRY OUT INTEGER OPERATIONS UNLESS ITS AN INTEGER
        


        for key, value in graph.items():
            if key == "Income Tax Start":
                for key1 in value:
                    
                    IncomeTaxStart = value[key1]
                    listofreturns[key] = IncomeTaxStart
            


        
        
       



        print("CHANGED AMOUNT : ", changedamount)
        
        visitedlist, weightslist = self.dfs(graph,startpoint, [], [], listofreturns)   #LAST ONE IS RETURN TO STACK/LIST

        x = 0
        n = 1

        

        
        IncomeT, ExciseD, NationalI, CorpT, VAT, CarbonT = None, None, None, None, None, None
        getTaxes = LE.Load(self.UserID)
        IncomeT, ExciseD, NationalI, CorpT, VAT, CarbonT = getTaxes.LoadFiscalTaxes(IncomeT, ExciseD, NationalI, CorpT, VAT, CarbonT)

        usethisval = visitedlist.index('TaxRevenue')
        print(weightslist[usethisval])
        print("visited in this order : ", visitedlist)

        print("")
        for i in weightslist:
            print(visitedlist[n], weightslist[x])
            
            x += 1
            n += 1
        print(eval(visitedlist[0])) #USED SO THAT THE ACTUAL INCOMET VALUE IS DISPLAYED 


if __name__ == "__main__":
    
    runthisthing = MakeChanges(1)
    runthisthing.RunTaxGraph('Income Tax Start', 200)
    


        
