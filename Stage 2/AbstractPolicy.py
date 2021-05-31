from tkinter import *





class FiscalPolicy():
    
    def __init__(self, policyname):
        self.policy_screen = Tk()
        self.policy_screen.configure(bg = "aqua")
        self.policy_screen.geometry("800x900+560+90") 
        self.policy_screen.title(policyname)
        self.policy_screen.resizable(False,False)





#class MonetaryPolicy(FiscalPolicy):
#    def __init__(self, policyname):
#        FiscalPolicy.__init__(self, policyname)


def main():
    
    print("yay")

if __name__ == "__main__":
    main()
    




