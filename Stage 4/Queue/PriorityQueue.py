#New file: PriorityQueue


class PriorityQueueFunctions():
    #An empty queue is always passed in
    def __init__(self, UserID, Queue, policiesconfirmed):
        print("PRIORITY QUEUE")
        self.UserID = UserID
        self.Queue = Queue
        self.policiesconfirmed = policiesconfirmed
        #print(self.policies)
        print("original queue: ", self.Queue)
        
    def Size(self):
        
        return len(self.Queue)

    def is_Empty(self):
        #Could just be return self.Queue == [], which would do the same thing, however the below method was chosen as it is easier for me to look at later.
        if self.Queue == []:
            return True
        else:
            return False

    
    def enQueue(self, toadd):
        if self.is_Empty(): #If its empty, just add it into the queue.
            self.policiesconfirmed[toadd].insert(0, toadd) #What is being added is the value of the dictionary with key toadd. But the priority needs to go with the value so that
                                                    #   other policies being added can refer to this policies priority. As the value is a list, we can insert the priority (the key/toadd)
                                                    #   to the front of the value (which is a list).
                                                    
            self.Queue.append(self.policiesconfirmed[toadd])   #Can just be append as there are no other elements in the queue.
            
        else:
            #If theres already a policy in the queue, find where the policy being added will be inserted based on its priority, which is the first value of the list which details
            #   about the policy are contained in.
            position = self.findPosition(toadd) #Retrieve the position based on its priority
            self.policiesconfirmed[toadd].insert(0, toadd) #Add the priority to the front of the list.
            
            self.Queue.insert(position,self.policiesconfirmed[toadd])  #Add the new policy with all its details to the queue.

        print(self.Queue)
        #print(self.Queue[0][0])    prints Income Tax



    def findPosition(self, toadd):

        for element in self.Queue:
            position = self.Queue.index(element)
            
            
            if toadd < element[0]: #if it has a greater priority then the element being observed, place it in that position
                return position
                
            elif position == self.Size()-1: #if it has the lowest priority then, add it to the end
                return position + 1

    def findOtherQueuePosition(self, toadd, Queue):

        for element in Queue:
            position = Queue.index(element)


            if toadd < element:
                return position

            elif position == len(Queue) - 1:
                return position + 1
        

    def shift_priorities(self, shiftfrom):  #Only one priority can belong to one policy, not multiple, so this will shift up or down the other priorities.

        print("PRIORITY QUEUE 2")
        listofmaxes = {} #A list of all keys in policiesconfirmed.
        listofmins = {}  #A list of all keys in policiesconfirmed.
        temp_queue = []  #A temporary queue used to order listofmins and listofmaxes properly so that they can be used properly.
        for key in self.policiesconfirmed.keys():
            
            if temp_queue == []:
                temp_queue.append(key)
            else:
                position = self.findOtherQueuePosition(key, temp_queue) #Uses this method to put the priorities in order
                print("position is: ", position)
                temp_queue.insert(position, key)
            print(temp_queue)

        for element in temp_queue:
            
            listofmaxes[int(element)] = 1
            listofmins[int(element)] = 1

        
            #Add eachkey to the dictionary listofmaxes with value 1, meaning that it has not been looked at yet.



        for key, value in reversed(listofmaxes.items()):
            keyafter = (int(key) + 1)   #Take the key if the key being looked at will shift
            print("keyafter is now: ", keyafter)
            
            if (keyafter in listofmaxes) and (listofmaxes[keyafter] == 0):    #If there is already an element in the next slot and its not shifting, then this also cannot be shifted
                                                                            #   so set it to 0.
                listofmaxes[key] = 0
            elif keyafter == 0: #if the key will be shifted to 0 and no policies from previous quarters are having effect, then this must be set to 0 as this cannot happen.
                listofmaxes[key] = 0

            if key < shiftfrom: #Even if it is still 1 (so can be shifted), set it to 0 so that it isn't shifted. In some cases this doesn't matter, but in other it will.
                listofmaxes[key] = 0
                
            if keyafter == 5:   #Cannot excced 4.
                listofmaxes[key] = 0

                
        for key, value in listofmins.items():   
            keyafter = (int(key) - 1)   #Take the key if the key being looked at will shift
            if (keyafter in listofmins) and (listofmins[keyafter] == 0):    #If there is already an element in the next slot and its not shifting, then this also cannot be shifted
                                                                            #   so set it to 0.
                listofmins[key] = 0
            elif keyafter == 0: #if the key will be shifted to 0 and no policies from previous quarters are having effect, then this must be set to 0 as this cannot happen.
                listofmins[key] = 0

            if key > shiftfrom: #Even if it is still 1 (so can be shifted), set it to 0 so that it isn't shifted. In some cases this doesn't matter, but in other it will.
                listofmins[key] = 0

            if keyafter == 0:   #Cannot be lower than 1.
                listofmins[key] = 0
                
                #for key2, value2 in listofmaxes.items():
                 #   if key2 != key:
                  #      if key2 > key:
                   #         
                    #        listofmaxes[key2] = 0
                
        #for key, value in self.policiesconfirmed.items():
         #   if (int(key)-1) not in self.policiesconfirmed.items():
          #      for key2, value2 in listofmaxes.items():
           #         if key2 != key:
            #            if key2 > key:
             #               listofmins[key2] = 0

        
            
      
        print("list of maxes is: ", listofmaxes)
        print("list of mins is: ", listofmins)
        #Shift priorities down if they can be and need to be.
        hasshifted = False  #used to determine if it has shifted any priorities down, if not they must be shifted up.
        for key in listofmaxes.keys():
            #Get the maximum key value where the value isn't 0
            try:
                maximum = int(max(k for k, v in listofmaxes.items() if v != 0)) #Must be converted from string to integer.
            except:
                break
            if maximum >= shiftfrom:    #if the max is greater than or = to where the new one will replace another policy due to the same priorities, shift it down a priority.
                print("maximum is ", maximum)
                if maximum < 4: #cannot be increased to anything greater than 4
                    if (maximum+1) not in self.policiesconfirmed: #Means that this can't be shifted anymore eg: 4 did not shift so 3+1 = 4, but 3 cannot become 4 as 4 is already 
                                                                     #  existent.
                                                                     #  Eg: with keys 1, 3, 4 and inserting something into position 1, it should become 1, 2, 3, 4... so
                                                                     #  the 3 should not increase.
                        print("SHIFTING NOW the priority: ", maximum)
                        newmaximum = maximum + 1
                        hasshifted = True   #This means that priorities have actually moved down.
                        self.policiesconfirmed[str(newmaximum)] = self.policiesconfirmed[str(maximum)]  #Must be string otherwise we are adding an additional item, increasing the size
                                                                                                        #   of the dictionary in the loop which cannot happen.
                    
            
                listofmaxes[maximum] = 0    #Set its value to 0 so that the next greatest key (next lowest priority) can be changed


        listtoremove = []   #Any duplications that happened after the validation need to be removed, but it depends on which way the shift occured that effects which of the duplicates are
                            #   removed.
        print("has shifted is: ", hasshifted)
        if hasshifted:  #Some priorities will still duplicate even after policies_everything's validation as they duplicate after the loop.
                        #If hasshifted is true then priorities have been shifted down.
            for key, value in self.policiesconfirmed.items():
                for key2, value2 in self.policiesconfirmed.items(): #This nested loop checks whether or not there are two values that are the same, which cannot be fo my program.
                    if value[0] == value2[0]: #If there are two values with the same policy name, not including the changedamount.
                        if int(key) < int(key2):
                            listtoremove.append(key)    #We want to remove the one with higher priority (so the smaller value)
                        

            for element in listtoremove:
                print(element)
                del self.policiesconfirmed[str(element)]
                        
        if not hasshifted:  #Then we know that priorities above the new one to be added must be moved up, as they can't be moves down.
                            #   Eg: having priorities 1, 3 and 4 and adding another policy with priority 3 cannot move 3 or 4 down so will just replace it, so the current 3 should
                            #   move to 2, making it 1, 2, 3, 4.
            #listofmins = {}
            #for key in self.policiesconfirmed.keys():
                #listofmins[key] = 1
            for key in listofmins.keys():
                try:
                    minimum = int(min(k for k, v in listofmins.items() if v != 0))
                except:
                    break
                if minimum <= shiftfrom:
                    print("The minimum is: ", minimum)
                    if minimum > 1: #Don't include those that have priorities 0 or less as these are previous policies with time-lag so they should go first after their time to
                                    #   wait to have effect is over. These are normally supply side policies or interest rates (normally takes 18 months for interest rates to have effect).
                        if (minimum-1) not in self.policiesconfirmed:


                            newminimum = minimum - 1
                            self.policiesconfirmed[str(newminimum)] = self.policiesconfirmed[str(minimum)]
                    listofmins[minimum] = 0

            for key, value in self.policiesconfirmed.items():
                for key2, value2 in self.policiesconfirmed.items(): #This nested loop checks whether or not there are two values that are the same, which cannot be fo my program.
                    if value[0] == value2[0]: #If there are two values with the same policy name, not including the changedamount.
                        if int(key) > int(key2):
                            listtoremove.append(key)    #We want to remove the one with lower priority (so the larger value) as the shift went the other way.
                            


            for element in listtoremove:
                print(element)
                del self.policiesconfirmed[str(element)]
                
        

        print("list of maxes are: ", listofmaxes)
        #print("list of mins are: ", listofmins)
        print(self.policiesconfirmed)
        return self.policiesconfirmed
            
#End of file: PriorityQueue        
            
            



def main():
    Queue = []    
    policiesconfirmed = {
                  "1" : ["Income Tax", 10],       #10 represent the changedamount --> {Priority, ("PolicyName", changedamount)}
                  "3" : ["Value Added Tax", -2],
                  "4" : ["Corporation Tax", 5],
                  "0" : ["Education", 4]
                  } 
    #print((dictionary[1])[1])                   #Returns the second element from a value (which is a list) with key 1.
    
    print(policiesconfirmed)
    runQueue = PriorityQueueFunctions(1, Queue, policiesconfirmed)
    priority = int(input("Enter priority for the change: "))
    alreadythere = False
    for key in policiesconfirmed.keys():
        if key == priority:
            alreadythere = True

    if alreadythere:
        policiesconfirmed = runQueue.shift_priorities(priority)


    #If you are changing the priority of a policy change.
    policyname = "Income Tax"
    policyexists = False
    for key, value in policiesconfirmed.items():
        print(value[0])
        if value[0] == policyname:
            print("policy exists now true")
            policyexists = True
            existingpolicykey = key

            
    if policyexists:
        del policiesconfirmed[existingpolicykey ]
        
        
    policiesconfirmed[priority] = [policyname, 10]
    

    print("new policies confirmed is: ", policiesconfirmed)
    

    
    
    Queue = []
    runQueue = PriorityQueueFunctions(1, Queue, policiesconfirmed)
    for key, value in policiesconfirmed.items():
        #print(value[0])
        print("")
        runQueue.enQueue(key)





    
if __name__ == "__main__":

    main()
    policiesconfirmed = {
                  1 : ["Income Tax", 10],       #10 represent the changedamount --> {Priority, ("PolicyName", changedamount)}
                  3 : ["Corporation Tax", -5],
                  2 : ["Education" , 5],
                  4 : ["Value Added Tax", 3],
                  0 : ["Interest Rates", 2]
                  } 
    #check2(policiesconfirmed, 2)

   







    
