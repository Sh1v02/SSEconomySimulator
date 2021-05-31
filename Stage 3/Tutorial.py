from tkinter import *

import sys

sys.path.append(r"C:\Users\shiva\OneDrive\Desktop\A-Levels\Computer Science\NEA\Code\Stage 3\Images")
#import FirstPage.png

import PIL.Image #For loading the image and rendering it.
from PIL import ImageTk




class Tutorial():

    def __init__(self):

        #The tutorial class will have one screen which will be positioned in different places depending on the part of the tutorial the user is on.
        #   The size is also different at some times.

        

        self.tutorial_screen = Tk()
        self.tutorial_screen.configure(bg = "black")

        
        self.FirstImage = PIL.Image.open("FirstPage.png") #Load the images.
        self.SecondImage = PIL.Image.open('Ratings.png')
        self.ThirdImage = PIL.Image.open('Statistics.png')
        self.FourthImage = PIL.Image.open('Policies.png')
        self.FifthImage = PIL.Image.open('FiscalPolicySelected.png')
        self.SixthImage = PIL.Image.open('FiscalPolicyTaxation.png')
        self.SeventhImage = PIL.Image.open('IncomeTax.png')
        self.EighthImage = PIL.Image.open('ExtraStatistics.png')
        self.NinthImage = PIL.Image.open('ConfirmedPolicies.png')
        self.TenthImage = PIL.Image.open('ElectionResults.png')
        


        #self.QuickIntro()
        #self.T_Ratings()

    def reload(self):

        self.tutorial_screen.destroy()
        self.__init__()

    def infoLabel(self, info, width):

        infolabel = Label(self.tutorial_screen, text = info, font = ("Comic Sans", 16), bg = "black", foreground = "white").place(x = 0, y = 0, width = width, height = 100)

        
        
    def QuickIntro(self):

        self.tutorial_screen.geometry("1920x1080")
        
        info = """Below shows you the order in which the main menu will be explored.
These will be explained in more detail after you press continue to continue the tutorial."""
        self.infoLabel(info, 1700)
        
        render = ImageTk.PhotoImage(self.FirstImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        FirstImage = Label(self.tutorial_screen, image = render)
        FirstImage.image = render
        FirstImage.place(x = 252, y = 100)    #Must be placed after.

        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_Ratings()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 200, height = 90)



    def T_Ratings(self):

        self.tutorial_screen.geometry("1920x1080")

        info = """How happy people are with your economy will naturally play a big role in your election. However try not to
prioritise ratings and forget about your other government objectives:
Full Employment, Price Stability, Good Balance Of Payments and steady Economic Growth"""
        self.infoLabel(info, 1700)

        render = ImageTk.PhotoImage(self.SecondImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        Ratings = Label(self.tutorial_screen, image = render)
        Ratings.image = render
        Ratings.place(x = 311, y = 210)   #Must be placed after.

        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_Statistics()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 200, height = 90)

        

    def T_Statistics(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """How well you are doing with your government objectives can be evaluated from this data. Each one plays a big role in your
re-election and shows how well your economy is doing."""
        self.infoLabel(info, 1700)




        
        render = ImageTk.PhotoImage(self.ThirdImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        Statistics = Label(self.tutorial_screen, image=render)
        Statistics.image = render
        Statistics.place(x = 0, y = 480)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_Policies()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)



    def T_Policies(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """The three policies you will have access to are the Fiscal Policy, the Monetary Policy and the Supply Side Policy.
Each of these are explained in more depth when you click on them.
Let's take a look at the Fiscal Policy."""
        self.infoLabel(info, 1700)

        


        
        render = ImageTk.PhotoImage(self.FourthImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        Policies = Label(self.tutorial_screen, image=render)
        Policies.image = render
        Policies.place(x = 0, y = 443)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_FiscalPolicySelected()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)



    def T_FiscalPolicySelected(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """You may be asked to select a type
 depending on the policy you want to change. In the Fiscal Policy, there are six different
 taxes that you can control and four different types of spending."""
        self.infoLabel(info, 1700)

        


        
        render = ImageTk.PhotoImage(self.FifthImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        Select = Label(self.tutorial_screen, image=render)
        Select.image = render
        Select.place(x = 740, y = 350)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_FiscalPolicyTaxation()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)


    def T_FiscalPolicyTaxation(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """Once you select an option you will be sent to a tab where you have more detailed information about this type of policy
and what you can control. In taxation in the Fiscal Policy, you have access to six different types of taxes, some regressive
and some progressive. Regressive effect lower income earners more, while progressive effects higher income earners more."""
        self.infoLabel(info, 1700)

        


        
        render = ImageTk.PhotoImage(self.SixthImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        Tax = Label(self.tutorial_screen, image=render)
        Tax.image = render
        Tax.place(x = 462, y = 200)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_IncomeTax()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)


    def T_IncomeTax(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """Once you select a policy you are able to change the value with the slider. After you change the value and have viewed the expected changes
to your economy, you can confirm the policy. Once you confirm the policy, you will be asked for a priority. The higher the priority you choose
the more likely the effects are equal to the expected changes. If you already have 4 policies confirmed, you will be asked to replace one."""
        self.infoLabel(info, 1700)

        


        
        render = ImageTk.PhotoImage(self.SeventhImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        Tax = Label(self.tutorial_screen, image=render)
        Tax.image = render
        Tax.place(x = 462, y = 124)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_ExtraStatistics()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)




    def T_ExtraStatistics(self):



        self.tutorial_screen.geometry("1920x1080")


        info = """By selecting one of the Additional Statistics buttons, you have access to several other statistics that
are working behind the scenes. These are also important and are key indicators of economic growth. You can also view a
graphical representation of some of your data here, which will help you to understand where you need to make changes."""
        self.infoLabel(info, 1700)




        
        render = ImageTk.PhotoImage(self.EighthImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        ExtraStatistics = Label(self.tutorial_screen, image=render)
        ExtraStatistics.image = render
        ExtraStatistics.place(x = 462, y = 140)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_Confirmed()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)



    def T_Confirmed(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """You can view your confirmed policies, which can be a maximum of 4 per quarter.
You can also reset these policies by pressing Reset Policies Confirmed.
Once you are happy with your confirmed policies, you can simulate your economy."""
        self.infoLabel(info, 1700)




        
        render = ImageTk.PhotoImage(self.NinthImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        ExtraStatistics = Label(self.tutorial_screen, image=render)
        ExtraStatistics.image = render
        ExtraStatistics.place(x = 619, y = 256)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_ElectionResults()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)



    def T_ElectionResults(self):

        self.tutorial_screen.geometry("1920x1080")


        info = """Depending on the difficulty you selected, an election will run after either 12 or 24 months.
Based on your economy and its progress, you may win or lose the election. Losing will result in your game ending."""
        self.infoLabel(info, 1700)




        
        render = ImageTk.PhotoImage(self.TenthImage, master = self.tutorial_screen)     #Render the image. #Master is needed so that when opened in the main menu, it is placed on the
                                                                                        #   correct window and the image can be found.
        ExtraStatistics = Label(self.tutorial_screen, image=render)
        ExtraStatistics.image = render
        ExtraStatistics.place(x = 564, y = 290)



        nextpart = Button(self.tutorial_screen, text = "Continue", command = lambda: [self.reload(), self.T_End()],
                          bg = "black", foreground = "white").place(x = 1710, y = 5, width = 180, height = 90)



    def T_End(self):



        self.tutorial_screen.geometry("1920x1080")


        info = """This is the end of the tutorial. If at any point you want to go
through the tutorial again, simply click Tutorial.
There are several helpful buttons that you will find as you look
around your economy.

Try to think about how the economy will be effected
by your actions and click the 'What To Do' buttons if you still
don't completely understand the function of the tab you are on or you
want more information about the policy you are controlling.

Remember to explore different changes as much as you can so
that you can understand these key aspects of macro-economics
extremely well!

Thank you for playing!

Good Luck!"""
        FinalInfo = Label(self.tutorial_screen, text = info, bg = "black", foreground = "white", font = ("Comic Sans", 18, "bold")).place(x = 10, y = 10, width = 1900, height = 800)

        EndButton = Button(self.tutorial_screen, text = "Play Simulator", foreground = "red", font = ("Comic Sans", 18, "bold"),
                           command = lambda: self.tutorial_screen.destroy()).place(x = 710, y = 650, width = 500, height = 400)

                          

        

        



    

        

        

        

        





if __name__ == "__main__":

    tutorial = Tutorial()
    tutorial.QuickIntro()

    #tutorial.T_Statistics()
        
