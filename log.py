import datetime
import sqlite3

from encryption import decrypt, encrypt, read_private_key, read_public_key


class Log:
    def __init__(self, username, descriptionOfActivity, additionalInformation, susp):
        self.Username = username
        self.Date = datetime.datetime.now().strftime("%d-%m-%Y")
        self.Time = datetime.datetime.now().strftime('%H:%M:%S')
        self.DescriptionOfActivity = descriptionOfActivity
        self.AdditionalInformation = additionalInformation
        self.Suspicious = susp

    def log(self):
        #encrypt data
        public_key = read_public_key()
        self.Username = encrypt(self.Username, public_key)
        self.Date = encrypt(self.Date, public_key)
        self.Time = encrypt(self.Time, public_key)
        self.DescriptionOfActivity = encrypt(self.DescriptionOfActivity, public_key)
        self.AdditionalInformation = encrypt(self.AdditionalInformation, public_key)
        self.Suspicious = encrypt(self.Suspicious, public_key)

        #get number
        logs = []
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            for i in c.execute('SELECT * FROM Logs'):  #i takes a whole row
                logs.append(i)
            c.close()
        except sqlite3.Error as error:
            print("Failed to get data of logs from sqlite table", error)
        finally:
            if connection:
                connection.close()
        self.No = encrypt(str(len(logs)+1), public_key)

        #save to database
        try:
            connection = sqlite3.connect("FitnessPlus")
            c = connection.cursor()
            c.execute("INSERT INTO Logs VALUES (?, ?, ?, ?, ?, ?, ?)", (self.No ,self.Username, self.Date, self.Time, self.DescriptionOfActivity, self.AdditionalInformation, self.Suspicious))
            connection.commit()
            c.close()      
        except sqlite3.Error as error:
            print("Failed to insert log into sqlite table", error)
        finally:
            if connection:
                connection.close()
    

def view_logs():
    pk = read_private_key()
    logs = []
   
    try:
        connection = sqlite3.connect("FitnessPlus")
        c = connection.cursor()
        for i in c.execute('SELECT * FROM Logs'):  #i takes a whole row
            logs.append(i)
        c.close()
    except sqlite3.Error as error:
        print("Failed to get data of logs from sqlite table", error)
    finally:
        if connection:
            connection.close()

    decrypted_results = []
    for row in logs:
        decrypted_row = []
        for value in row:
            decrypted_value = decrypt(value, pk)
            decrypted_row.append(decrypted_value)
        decrypted_results.append(decrypted_row)

    return decrypted_results
