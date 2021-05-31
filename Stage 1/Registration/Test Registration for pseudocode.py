import mysql.connector



password = input("Enter a password: ")

class hashpassword():
    def __init__(self,password):
        self.password = password
        self.temp_value = 0
        self.value = 0
        self.ascii_char = 0
        self.final_value = 0

        self.ascii_char2 = 0
        
    def hash(self):

        extraval1 = len(self.password)-2
        extraval2 = len(self.password)-3
        extraval3 = len(self.password)-4
        
        
        
        
        for character in self.password:
            self.ascii_char = ord(character)
            self.temp_value = ((((self.ascii_char+12)*4)-2) * 4) - 2
            self.value += self.temp_value

            if self.password.find(character) == extraval1:
                self.value += (self.ascii_char*3)-2
            elif self.password.find(character) == extraval2:
                self.value += (self.ascii_char*3)-4
            elif self.password.find(character) == extraval3:
                self.value += (self.ascii_char*3)-3

        self.final_value = self.value % 40
            

        print(self.final_value)            
            
            
            


hashit = hashpassword(password)

hashit.hash()


