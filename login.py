import msvcrt
import random
import time
import bcrypt
from database import Database
from inputvalidation import validate_password, validate_superAdmin, validate_username
from log import Log
from user import User


def Login(starting_minutes):
    print("\nPlease Log In")

    # 5 atttempts to log in
    attempts = 5
    for i in range(attempts):
        input_username = input("Enter username: ")
        input_password = MaskPassword("Enter password: ") 

        #check if super admin has logged in
        checkSuperAdmin = validate_superAdmin(input_username, input_password)
        if checkSuperAdmin == True:   
            #log succesfull login
            Log("super_admin", "Logged in", "", "No").log()
            return User("super admin", "", "", "", "super_admin", "", "", "")
        
        #validate
        val_username = validate_username(input_username)
        val_password = validate_password(input_password)
        if val_username.validation == True and val_password.validation == True:
            #authenticate
            auth = authenticate_user(input_username,input_password)
            
            #if authentication is succesfull return user data
            if auth[0] == True:
                return auth[1]
            elif auth[0] == False:
                #log failed login                              
                Log("", "Unsuccessful login", f"username {input_username} is used for a login attempt with wrong password", "No").log() 
        else:
            #validation failed. log it
            if val_password.validation == False:
                Log("", "Unsuccessful login", f"username {input_username} is used for a login attempt with an invalid password. Error that was found: {val_password.error_text}", "No").log()
            elif val_username == False:
                Log("", "Unsuccessful login", f"Invalid username {input_username} is used for a login attempt", "No").log()
            print("\nUsername/Password is invalid.\n")
        
        attempts -= 1
        #if 5 attempts and still failed, give a timeout
        if attempts == 0:
            print(f"Please try again after {starting_minutes} minutes")
            Log("", "Unsuccessful login", "Multiple usernames and passwords are tried in a row", "Yes").log()
            db = Database()
            db.create_alert()
            waiting_time(starting_minutes)

            #increase timeout every time user failed to log in
            return None


def MaskPassword(input_password):
    print(input_password, end='', flush=True)
    masked_password = ""
    while True:
        char = msvcrt.getwch()
        if char == "\r" or char == "\n":
            print()
            break
        elif char == "\b":
            if len(masked_password) > 0:
                masked_password = masked_password[:-1]
                print("\b \b", end="", flush=True)
        else:
            masked_password += char
            print("●", end="", flush=True)
    return masked_password

def generate_captcha_text(length=6):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$&*+-?!='
    captcha_text = ''.join(random.choice(characters) for _ in range(length))
    return captcha_text

def waiting_time(minutes):
    try:
        time.sleep(minutes*60) 
        # time.sleep(1)
        print("Waiting time ended")
    except KeyboardInterrupt:
        print("\nWaiting time interrupted by user.")


def authenticate_user(username, password):
    db = Database()

    #get data of user
    user_data = db.getUser(username)
    
    #if user exists, check if the password matches
    if len(user_data) > 0:

        # Hash the entered password with the stored salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), user_data[7])

        if (user_data[6] == hashed_password):
            return [True, User(user_data[1],user_data[2], user_data[3], user_data[4], user_data[5], "","", user_data[8])]
        else:
            print("\nUsername/Password is incorrect.")
            return [False, ""]
    else:
        print("\nUsername/Password is incorrect.")
        return [False, ""]
