
class Authentication:
    # methods or functions

    def signup(self):
        # signup
        email = "contact@ss.co"
        password = "123456"
        name = "Anji Reddy"

        print("signup success")


    def login(self):
        # login
        email = "contact@ss.co"
        password = "1234567"

        if email == "contact@ss.co" and password == "123456":
            print("login success")
        else:
            print("invalid login credentials")

    def reset_password(self):
        # reset password
        email = "contact@ss.co"

        if email == "contact@ss.co":
            print("password reset link sent to your email id. please check junk/trash folder")
        else:
            print("no account with your email id")



auth = Authentication()
auth.login()

def session_data():
    print("collecting all session info")

session_data()

def concat_data(first_name, last_name):
    full_namne = first_name + " " + last_name
    return full_namne

data = concat_data("anji", "reddy")

print( data )

def add(a, b):
    return a + b

print( add(10, 20) )


