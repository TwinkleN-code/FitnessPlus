
import random
import bcrypt
from database import Database
from inputvalidation import *
from log import Log
from login import MaskPassword, authenticate_user, waiting_time
from member import get_current_date
from user import User

# CREATE READ UPDATE USER

def add_new_user(user:User, role):
    print(f"\nAdd new {role} ")
    db = Database()
    while True:
        print(f"\nDo you want to add a new {role}? \n\n1. Yes \n2. No")
        inp = input("\nEnter a number: ")
        if validate_numberInput(inp, 1, 2) == False:
            InvalidInput()
        else:
            inp = int(inp)
            if inp == 2:
                return
            else:
                break

    #ask first name
    while True:
        firstname = input("\nEnter First Name: ")
        if validate_name(firstname) == False:
            print("Name invalid. Try again")
        else:
            break

    #ask last name
    while True:
        lastname = input("Enter Last Name: ")
        if validate_name(lastname) == False:
            print("Name invalid. Try again")
        else:
            break

    #ask username
    print("\nUsername requirements:  \n- must have at least 8 characters \n- must be no longer than 12 characters \n- must be started with a letter or underscores (_) \n- can contain letters (a-z), numbers (0-9), underscores (_), apostrophes (') and periods (.) \n- no distinguish between lowercase or uppercase letters")
    while True:
        username = input("\nEnter Username: ")
        val = validate_username(username)
        if val.validation == False:
            print(val.error_text)
        else:
            #check if username already exists
            exist = db.searchUser(username)
            if exist:
                print("Username already exists. try again")
            else:
                break

    #ask password
    print("\nPassword requirements: \n- must have at least 12 characters \n- must be no longer than 30 characters \n- can contain letters (a-z), numbers (0-9) and special characters \n- allowed special characters: ~!@#$%&_-+=`|\()}{[]:;'<>,.?/ \n- must have a combination of at least one lowercase letter, one uppercase letter, one digit and one special character")
    while True:
        password = MaskPassword("\nEnter Password: ")
        password2 = MaskPassword("Re-enter Password: ")
        val_passw = validate_password(password)
        if password != password2:
            print("Passwords do not match")
        #if validation vailed
        elif val_passw.validation == False:
            print(val_passw.error_text)
        elif (val.validation == True):
            break

    #registration date
    registration_date = get_current_date()

    #generate salt
    salt = bcrypt.gensalt()
    hashedpassw = bcrypt.hashpw(password.encode('utf-8'), salt)

    #add user to database
    new_user = User(role,firstname,lastname,registration_date,username,hashedpassw,salt,"No")
    db.insertUserData(new_user)
    Log(user.Username, f"New {role} user is created", f"username: {username}", "No").log()
    print("\nUser added succesfully")
    
    #go back
    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return


def InvalidInput():
    print("Invalid input. Try again \n")

def update_user_profile(user, role):
    db = Database()
    print(f"\nUpdate/Modify {role} profile")

    while True:
        print("\nPlease note that you will need username to update or modify the user's profile. \nDo you want to continue? \n\n1. Yes \n2. No")
        inp = input("\nEnter a number: ")
        if validate_numberInput(inp, 1, 2) == False:
            InvalidInput()
        else:
            inp = int(inp)
            if inp == 2:
                return
            else:
                break

    while True:
        input_username = input(f"\nEnter {role} username: ")
        #validate username
        val_username = validate_username(input_username)
        if val_username.validation == True:

            #check if user exists and is a trainer/admin
            result = db.searchUsername(role, input_username)

            #if user found ask what to update
            if result:
                print("\nChoose option to update: \n1. First Name \n2. Last Name \n3. Username \n4. Password")

                while True:
                    user_input = input("\nEnter a number: ")
                    if validate_numberInput(user_input, 1, 4) == False:
                        InvalidInput()
                    else:
                        user_input = int(user_input)
                        break
                
                #update firstname
                if user_input == 1:
                    while True:
                        new_fname = input("\nEnter new First Name: ")
                        if (validate_name(new_fname) == False):
                            print("Name invalid. Try again")
                        else:
                            break
                    db.updateUserProfile(input_username, "FirstName", new_fname)
                    print("\nUser profile updated!")
                    Log(user.Username, "User profile updated", f"First name of user with username: {input_username} updated", "No").log()
                    break
                
                #update last name
                elif user_input == 2:
                    while (True):
                        new_lname = input("\nEnter new Last Name: ")
                        if (validate_name(new_lname) == False):
                            print("Name invalid. Try again")
                        else:
                            break
                    db.updateUserProfile(input_username, "LastName", new_lname)
                    print("\nUser profile updated!")
                    Log(user.Username, "User profile updated", f"Last name of user with username: {input_username} updated", "No").log()
                    break
                
                #update username
                elif user_input == 3:
                    print("\nUsername requirements:  \n- must have at least 8 characters \n- must be no longer than 12 characters \n- must be started with a letter or underscores (_) \n- can contain letters (a-z), numbers (0-9), underscores (_), apostrophes (') and periods (.) \n- no distinguish between lowercase or uppercase letters")
                    while True:
                        new_username = input("\nEnter new Username: ")
                        val = validate_username(new_username)
                        if (val.validation == False):
                            print(val.error_text)
                        else:
                            #check if username already exists
                            exist = db.searchUser(new_username)
                            if exist:
                                print("Username already exists. try again")
                            else:
                                break
                    #update in database
                    db.updateUserProfile(input_username, "UserName", new_username)
                    print("\nUsername updated!")
                    Log(user.Username, "User profile updated", f"Username of user with old username: {input_username} updated", "No").log()
                    break
                
                #update password
                elif (user_input == 4):
         
                    print("\nPassword requirements:  \n- must have at least 12 characters \n- must be no longer than 30 characters \n- can contain letters (a-z), numbers (0-9) and special characters \n- allowed special characters: ~!@#$%&_-+=`|\()}{[]:;'<>,.?/ \n- must have a combination of at least one lowercase letter, one uppercase letter, one digit and one special character")                 
                    while True:
                        new_password = MaskPassword("\nEnter new Password: ")
                        new_password2 = MaskPassword("Re-enter new Password: ")
                        val_passw = validate_password(new_password)
                        #validate password
                        if new_password != new_password2:
                            print("Passwords do not match")
                        elif val_passw.validation == False:
                            print(val_passw.error_text)
                        elif val_passw.validation == True:
                            break

                    #generate salt
                    new_salt = bcrypt.gensalt()
                    new_hashedpassw = bcrypt.hashpw(new_password.encode('utf-8'), new_salt)

                    #update in database
                    db.updateUserProfile(input_username, "Password", new_hashedpassw)
                    db.updateUserProfile(input_username, "Salt", new_salt)
                    print("\nUser password updated!")
                    Log(user.Username, "User profile updated", f"Password of user with username: {input_username} updated", "No").log()
                    break
            else:
                print("User not found. try again")

        else:
            InvalidInput()

    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return   
                    
def delete_user(user, role):
    db = Database()
    print("\nDelete User ")
    while True:
        print("\nPlease note that you will need username to delete user's profile. \nDo you want to continue? \n\n1. Yes \n2. No")
        inp = input("\nEnter a number: ")
        if validate_numberInput(inp, 1, 2) == False:
            InvalidInput()
        else:
            inp = int(inp)
            if inp == 2:
                return
            else:
                break

    while True:
        input_username = input("\nEnter username: ")
        val_username = validate_username(input_username)
        if val_username.validation == True:

            #check if username exists and if it is a trainer/admin
            result = db.searchUsername(role, input_username)

            #if exists delete user
            if result:
                print(f"\nAre you sure you want to delete {input_username} permanently? \n1. Yes \n2. No")
                while True:
                    user_input = input("\nEnter a number: ")
                    if validate_numberInput(user_input,1,2) == False:
                        InvalidInput()  
                    else:
                        user_input = int(user_input)
                        if user_input == 1:
                            db.deleteUser(input_username, role)
                            print("\nUser deleted succesfully!")
                            Log(user.Username, "User is deleted", f"User {input_username} is deleted", "No").log()

                            while True:
                                back = input("\nEnter 1 to go back: ")
                                if validate_numberInput(back, 1, 1) == False:
                                    InvalidInput()
                                else:
                                    return   
                        elif user_input == 2:
                            return
            else:
                print("Username does not exists. try again")
        else:
            InvalidInput()


def reset_password(user, role):
    print(f"\nReset password ")
    db = Database()
    while True:
        print(f"\nPlease note that you will need username for this action. \nDo you want to reset password of a {role} account? \n\n1. Yes \n2. No")
        inp = input("\nEnter a number: ")
        if validate_numberInput(inp, 1, 2) == False:
            InvalidInput()
        else:
            inp = int(inp)
            if inp == 2:
                return
            else:
                break

    while True:
        input_username = input("\nEnter username: ")
        val_username = validate_username(input_username)
        if val_username.validation == True:

            #check if username exists and if it is a trainer
            result = db.searchUsername(role, input_username)

            #if exist put a temporary password and send a notification to intended account
            if result:
                while True:
                    print(f"\nAre you sure you want to reset user's password? A temporary password will be generated \n\n1. Yes \n2. No")
                    inp = input("\nEnter a number: ")
                    if validate_numberInput(inp, 1, 2) == False:
                        InvalidInput()
                    else:
                        inp = int(inp)
                        if inp == 2:
                            return
                        else:
                            break

                temp_passw = generate_random_password()
                print(f"\nThe temporary password is:  {temp_passw}  \nPlease notify intended user")

                #Hash and salt the temp password 
                new_salt = bcrypt.gensalt()
                new_hashedpassw = bcrypt.hashpw(temp_passw.encode('utf-8'), new_salt)

                #update in database
                db.updateUserProfile(input_username, "Password", new_hashedpassw)
                db.updateUserProfile(input_username, "Salt", new_salt)
                db.updateUserProfile(input_username, "TemporaryPassword", "Yes")
                print("\nPassword reset!")
                Log(user.Username, "Password reset", f"User '{input_username}' password is reset", "No").log()

                while True:
                    back = input("\nEnter 1 to go back: ")
                    if validate_numberInput(back, 1, 1) == False:
                        InvalidInput()
                    else:
                        return  

            else:
                print("Username does not exists. try again")
        else:
            InvalidInput()

def generate_random_password():

    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digits = "0123456789"
    special_characters = r"~!@#$%&_-+=`|\(){}[]:;'<>,.?/"

    password = []

    # Add one character from each 
    password.append(random.choice(lowercase_letters))
    password.append(random.choice(uppercase_letters))
    password.append(random.choice(digits))
    password.append(random.choice(special_characters))

    # Choose random length between 8 and 15
    remaining_length = random.randint(8, 15) 

    # fill in the remaining length with random characters
    for i in range(remaining_length):
        password.append(random.choice(random.choice([lowercase_letters, uppercase_letters, digits, special_characters])))

    # Convert the list of characters to a string
    password = ''.join(password)

    return password



#updating user's own password
def update_own_password(user: User):
    print("\nUpdate password \n")

    db = Database()
    attempts = 5
    i = 0
    while i < attempts:
        curr_passw = MaskPassword("Enter current password to continue: ")
        
        #password validation
        v = validate_password(curr_passw)
        if v.validation == True:
            #authentication
            auth = authenticate_user(user.Username, curr_passw)
            if auth[0] == True:
                while True:
                    #enter new password
                    new_passw = MaskPassword("Enter new password: ")
                    new_passw2 = MaskPassword("Confirm password: ")

                    if new_passw == new_passw2:

                        #input validation for new password 
                        while validate_password(new_passw).validation == False:
                            print(validate_password(new_passw).error_text)
                            new_passw = MaskPassword("Enter new password: ")
                            new_passw2 = MaskPassword("Confirm password: ")

                        # Generate a new salt and hash the password
                        salt = bcrypt.gensalt()
                        hashed_password = bcrypt.hashpw(new_passw.encode('utf-8'), salt)

                        # update to database
                        db.updateUserProfile(user.Username, "Password", hashed_password)
                        db.updateUserProfile(user.Username, "Salt", salt)

                        print("\nPassword updated successfuly!")
                        Log(user.Username, "Password updated successfuly", "", "No" ).log() #log incident
                        while True:
                            back = input("Enter 1 to go back: ")
                            if validate_numberInput(back, 1, 1) == False:
                                InvalidInput()
                            else:
                                return
                    
                    else:
                        print("Passwords don't match. try again\n")
        else:
            i += 1
            print("Incorrect password.")
            Log(user.Username, "Update password failed", "user entered wrong password before updating", "No").log()

        #give time out after several attempts
        if (i >= 4):
            print("Please try again after 5 minutes")
            Log(user.Username, "Update password failed", "user entered wrong password many times in a row", "Yes").log()
            db.create_alert()
            waiting_time(5) 
            i = 0
