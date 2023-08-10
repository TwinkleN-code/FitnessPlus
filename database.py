import sqlite3
from encryption import *
from user import User


class Database:
    def __init__(self):
        self.public_key = read_public_key()


    #create a database if it does not exists
    def createDatabase(self):
        try:
            connection = sqlite3.connect("FitnessPlus")
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS Members (MemberID BLOB, FirstName BLOB, LastName BLOB, Age BLOB, Gender BLOB, Weight BLOB, StreetName BLOB, HouseNr BLOB, Zip BLOB, City BLOB, Email BLOB, Mobile BLOB, RegistrationDate BLOB)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Users (UserID BLOB, Role BLOB, FirstName BLOB, LastName BLOB, RegistrationDate BLOB, Username BLOB, Password BLOB, Salt BLOB, TemporaryPassword BLOB)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Logs (No BLOB, Username BLOB, Date BLOB, Time BLOB, Description BLOB, AdditionalInfo BLOB, Suspicious BLOB)''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Alert (No INT, SystemAdmin INT, SuperAdmin INT)''')
            connection.commit()
            cursor.close()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite: " + error)
        finally:
            if connection:
                connection.close()

   
    #insert encrypted data of members in database
    def insertMemberData(self, member):
        #encrypt
        fname = encrypt(member.firstname, self.public_key)
        lname = encrypt(member.lastname, self.public_key)
        age = encrypt(member.age, self.public_key)
        gender = encrypt(member.gender, self.public_key)
        weight = encrypt(member.weight, self.public_key)
        streetname = encrypt(member.streetname, self.public_key)
        housenr = encrypt(member.housenumber, self.public_key)
        zip_code = encrypt(member.zipcode, self.public_key)
        city = encrypt(member.city, self.public_key)
        mobile = encrypt(member.mobile, self.public_key)
        email = encrypt(member.email, self.public_key)
        date = encrypt(member.registrationDate, self.public_key)

        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            c.execute("INSERT INTO Members VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (member.memberId, fname, lname, age, gender, weight,streetname, housenr, zip_code, city, email, mobile, date))
            connection.commit()
            c.close()      
        except sqlite3.Error as error:
            print("Failed to insert member data into sqlite table", error)
        finally:
            if connection:
                connection.close()

    
    
    #get all data of members
    def getMembersData(self):
        members = []
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            for i in c.execute('SELECT * FROM Members'):  #i takes a whole row
                members.append(i)
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of users from sqlite table", error)
        finally:
            if connection:
                connection.close()

        #get private key:
        private_key = read_private_key()

        decrypted_results = []
        i = 0
        while i < len(members):
            decrypted_row = []
            j = 0
            while j < len(members[i]):
                if (j > 0):
                    decrypted_value = decrypt(members[i][j], private_key)
                    decrypted_row.append(decrypted_value)
                else:
                    decrypted_row.append(members[i][j])
                j += 1
            decrypted_results.append(decrypted_row)
            i += 1

        return decrypted_results
   
    
    def searchMember(self,searchkey):
        #get all members data
        members = self.getMembersData()

        #filter with search key 
        filtered_data = []
        for member in members:
            for item in member:
                if searchkey.lower() in str(item).lower():
                    filtered_data.append(member)
                    break

        return filtered_data 
    
    def searchMemberID(self, memberId):
        members = self.getMembersData()
        if len(members) > 0:
            for member in members:
                if member[0] == memberId:
                    return True
        return False

    
    def updateMemberProfile(self,member_id, category, new_info):
        #encrypt updated information
        new_info = encrypt(new_info, self.public_key)

        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()           
            c.execute(f"UPDATE members SET {category}=? WHERE MemberID=?", (new_info, member_id))
            connection.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of member from sqlite table", error)
        finally:
            if connection:
                connection.close()

    def deleteMember(self, member_id):
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()           
            c.execute("DELETE FROM members WHERE MemberID=?", (member_id,))
            connection.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of member from sqlite table", error)
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

        #get private key:
        private_key = read_private_key()

        decrypted_results = []
        i = 0
        while i < len(users):
            decrypted_row = []
            j = 0
            while j < len(users[i]):
                #don't decrypt password and salt and userID
                if j != 0 and j != 6 and j != 7:
                    decrypted_value = decrypt(users[i][j], private_key)
                    decrypted_row.append(decrypted_value)
                else:
                    decrypted_row.append(users[i][j])
                    
                j += 1
            decrypted_results.append(decrypted_row)
            i += 1

        return decrypted_results
    
    def getUser(self, username):
        users = self.getUsersData()
        for user in users:
            if user[5] == username:
                return user
        return []
    
    #add encrypted data of users in database
    def insertUserData(self, user:User):


        #encrypt
        role = encrypt(user.Role, self.public_key)
        fname = encrypt(user.FirstName, self.public_key)
        lname = encrypt(user.LastName, self.public_key)
        date = encrypt(user.Date, self.public_key)
        username = encrypt(user.Username, self.public_key)    
        temp = encrypt(user.Temp, self.public_key)

        #get id
        users = self.getUsersData()  
        user_id = str(len(users)+1)

        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            c.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, role, fname, lname, date, username, user.Password, user.Salt, temp))
            connection.commit()
            c.close()      
        except sqlite3.Error as error:
            print("Failed to insert user data into sqlite table", error)
        finally:
            if connection:
                connection.close()

    #checks if a user exists with given username
    def searchUser(self, username):
        users = self.getUsersData()

        if len(users)> 0:
            for user in users:
                if user[5] == username:
                    return True
        
        return False
        

    #checks if a specific username with a specific role exists
    def searchUsername(self, role, username):
        users = self.getUsersData()

        if len(users)> 0:
            for user in users:
                if user[5] == username and user[1] == role:
                    return True
        
        return False
        
    def updateUserProfile(self,username, category, new_info):
        #encrypt updated information. Do not encrypt password
        if category != "Password" and category != "Salt":
            new_info = encrypt(new_info, self.public_key)

        #get all users
        users = self.getUsersData()

        #retrieve userID 
        userID = ""
        if len(users)> 0:
            for user in users:
                if user[5] == username:
                    userID = user[0]
            
        #update in database
        if len(userID) > 0:
            try:
                connection = sqlite3.connect("FitnessPlus")
                c = connection.cursor()           
                c.execute(f"UPDATE Users SET {category}=? WHERE UserID=?", (new_info, userID))
                connection.commit()
                c.close()
            except sqlite3.Error as error:
                print("Failed to get data of user from sqlite table", error)
            finally:
                if connection:
                    connection.close()

    def deleteUser(self, username, role):
        #get all users
        users = self.getUsersData()

        #retrieve userID 
        userID = ""
        if len(users)> 0:
            for user in users:
                if user[5] == username and user[1] == role:
                    userID = user[0]
        #delete record from database
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()           
            c.execute("DELETE FROM Users WHERE UserID=?", (userID,))
            connection.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of user from sqlite table", error)
        finally:
            if connection:
                connection.close()

    def get_alert(self):
        alerts = []   
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            for i in c.execute('SELECT * FROM Alert'):  #i takes a whole row
                alerts.append(i)
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of alert from sqlite table", error)
        finally:
            if connection:
                connection.close()

        return alerts

    def create_alert(self):

        alerts = self.get_alert()
        if alerts == []:
            try:
                connection = sqlite3.connect("FitnessPlus")
                c = connection.cursor()
                c.execute("INSERT INTO Alert VALUES (?, ?, ?)", ("1", 1, 1))
                connection.commit()
                c.close()      
            except sqlite3.Error as error:
                print("Failed to insert alert data into sqlite table", error)
            finally:
                if connection:
                    connection.close()
        else:
            sys_admin_alert = int(alerts[0][1]) + 1
            super_admin_alert = int(alerts[0][2]) + 1 
            try:
                connection = sqlite3.connect("FitnessPlus")
                c = connection.cursor()           
                c.execute(f"UPDATE Alert SET SystemAdmin=?, SuperAdmin=? WHERE No=?", (sys_admin_alert, super_admin_alert, 1,))
                connection.commit()
                c.close()
            except sqlite3.Error as error:
                print("Failed to get data of alert from sqlite table", error)
            finally:
                if connection:
                    connection.close()
        

    def reset_alert(self, role):
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()           
            c.execute(f"UPDATE Alert SET {role}=? WHERE No=?", (0,1,))
            connection.commit()
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of alert from sqlite table", error)
        finally:
            if connection:
                connection.close()

