import sys



class PriorityQueueFunctions():

    def __init__(self, UserID, Queue, policiesconfirmed):
        self.UserID = UserID
        self.Queue = Queue
        self.policies = policiesconfirmed
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
            self.policies[toadd].insert(0, toadd) #What is being added is the value of the dictionary with key toadd. But the priority needs to go with the value so that
                                                    #   other policies being added can refer to this policies priority. As the value is a list, we can insert the priority (the key/toadd)
                                                    #   to the front of the value (which is a list).
                                                    
            self.Queue.append(self.policies[toadd])   #Can just be append as there are no other elements in the queue.
            
        else:
            #If theres already a policy in the queue, find where the policy being added will be inserted based on its priority, which is the first value of the list which details
            #   about the policy are contained in.
            position = self.findPosition(toadd) #Retrieve the position based on its priority
            self.policies[toadd].insert(0, toadd) #Add the priority to the front of the list.
            
            self.Queue.insert(position,self.policies[toadd])  #Add the new policy with all its details to the queue.

        print(self.Queue)
        #print(self.Queue[0][0])    prints Income Tax



    def findPosition(self, toadd):

        for element in self.Queue:
            position = self.Queue.index(element)
            
            
            if toadd < element[0]: #if it has a greater priority then the element being observed, place it in that position
                return position
                
            elif position == self.Size()-1: #if it has the lowest priority then, add it to the end
                return position + 1
        
        
    
        
        



def main():


    
    policiesconfirmed = {
                  1 : ["Income Tax", 10],       #10 represent the changedamount --> {Priority, ("PolicyName", changedamount)}
                  3 : ["Corporation Tax", -5],
                  2 : ["Education" , 5],
                  4 : ["Value Added Tax", 3],
                  0 : ["Interest Rates", 2]
                  } 
    #print((dictionary[1])[1])                   #Returns the second element from a value (which is a list) with key 1.
    

    priority = int(input("Enter priority for the change: "))
    
    policiesconfirmed = check2(policiesconfirmed, priority)
   
    policiesconfirmed[priority] = ["National Insurance", -2]
    

    print("new policies confirmed is: ", policiesconfirmed)
    

    
    
    Queue = []
    runQueue = PriorityQueueFunctions(1, Queue, policiesconfirmed)
    for key, value in policiesconfirmed.items():
        #print(value[0])
        print("")
        runQueue.enQueue(key)



def check2(policiesconfirmed, limit):
    
    listofmaxes = {}
    for key in policiesconfirmed.keys():
        listofmaxes[key] = 1
        #add eachkey to the dictionary listofmaxes

    

    
    for key in listofmaxes.keys():
        #Get the maximum key value where the value isn't 0
        maximum = max(k for k, v in listofmaxes.items() if v != 0)
        if maximum >= limit:    #if the max is greater than or = to where the new one will be placed, shift it down a priority
            print("maximum is ", maximum)
            policiesconfirmed[maximum + 1] = policiesconfirmed[maximum]
            listofmaxes[maximum] = 0    #set its value to 0 so that the next greatest key (next lowest priority) can be changed
            
        
    
 
    
    

    print(listofmaxes)
    print(policiesconfirmed)
    return policiesconfirmed
    
    


    
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

   







    
