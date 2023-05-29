import sqlite3
import bcrypt

class Login:

    def __init__(self) -> None:
        pass

    def authenticate_user(self, username, password):
        #TODO encrypt username for searching in database
        
        #check if username exists in database  
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            c.execute("SELECT password, salt FROM users WHERE username=?", (username,))
            user_data = c.fetchone() #this is a tuple
            c.close()
        except sqlite3.Error as error:
            print("Failed to get user data from sqlite table", error)
        finally:
            if connection:
                connection.close()
        
        #if user exists, check if the password matches
        if (user_data):
            # Hash the entered password with the stored salt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), user_data[1])

            if (user_data[0] == hashed_password):
                return True
            else:
                print("\033[91m\nUsername/Password is incorrect.\033[0m")
                return False
        else:
            print("\033[91m\nUsername/Password is incorrect.\033[0m")
            return False


    

# #Test
#x = Login()
#salt = "$2b$12$2r52R8W8E1r86A5IB6KxA.n2RSpqnc9Afhr/LHrbdb.br0Wk7xwWu".encode('utf-8')
#hashedpassw = bcrypt.hashpw("winner1998".encode('utf-8'), salt)
#x.authenticate_user(hashedpassw, salt)
#x.authenticate_user('john_1998', 'winner1998')

