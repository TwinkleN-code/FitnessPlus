import sqlite3
import bcrypt

class Login:

    def __init__(self) -> None:
        pass

    def authenticate_user(self, username, password):
        #TODO encrypt username for searching in database
        
        #check if username exists   
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
        
        #if exists
        if (user_data):
            # Hash the entered password with the stored salt
            get_password = user_data[0].encode('utf-8')
            salt = user_data[1].encode('utf-8')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)


    

# #Test
# x = Login()
# hashedpassw = bcrypt.hashpw("winner1998".encode('utf-8'), "salty")
# x.authenticate_user(hashedpassw, "salty")
