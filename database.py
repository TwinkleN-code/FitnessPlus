import sqlite3

import bcrypt

from userinterface import printError


class Database:
    def __init__(self) -> None:
        pass

    #create a database if it does not exists
    def createDatabase(self):
        try:
            connection = sqlite3.connect("FitnessPlus")
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Members (MemberID TEXT, FirstName TEXT, LastName TEXT, Age TEXT, Gender TEXT, Weight TEXT, StreetName TEXT, HouseNr TEXT, Zip TEXT, City TEXT, Email TEXT, Mobile TEXT, RegistrationDate TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Users (Role TEXT, FirstName TEXT, LastName TEXT, RegistrationDate TEXT, Username TEXT, Password TEXT, Salt TEXT)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Logs (No TEXT, Username TEXT, Date TEXT, Time TEXT, Description TEXT, AdditionalInfo TEXT, Suspicious TEXT)''')
            connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            printError("Error while connecting to sqlite: " + error)
        finally:
            if connection:
                connection.close()

    #insert encrypted data of users in database
    def insertUserData(self, role, fname, lname, date, username, passw, salt):
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            c.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?)", (role, fname, lname, date, username, passw, salt))
            connection.commit()
            c.close()      
        except sqlite3.Error as error:
            print("Failed to insert user data into sqlite table", error)
        finally:
            if connection:
                connection.close()

    #get all data of users from database and save it into a list
    def getUsersData(self):
        users = []
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            for i in c.execute('SELECT * FROM Users'):  #i takes a whole row
                users.append(i)
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of users from sqlite table", error)
        finally:
            if connection:
                connection.close()

        return users
    
   
    



#Test
db = Database()
db.createDatabase()
salt = "salty".encode('utf-8')
hashedpassw = bcrypt.hashpw("winner1998".encode('utf-8'), salt)
db.insertUserData("trainer", "John", "Doe", "25-05-2023", "john_1998", hashedpassw, salt)
    