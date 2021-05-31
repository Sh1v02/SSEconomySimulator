class password:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def enter_username(self):
        username = input("Enter username: ")



usernameman = input("Enter") #must differ to the parameter name in the class
passwordman = input("Enter")
check_password = password(usernameman,passwordman)
print(check_password.username)


