import msvcrt
import os

from inputvalidation import validate_password, validate_superAdmin, validate_username
from login import Login

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

def InvalidInput():
    print("\033[91mInvalid input. Try again\033[0m \n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def printError(text):
    print(f"\033[91m\n{text}\033[0m \n")

def LoginPage():
    title = "Fitness Plus (Fit+)"
    formatted_title = f"\033[0;35m{title}\033[0m"
    borderline = "¨" * (len(title) + 4)
    print(f"\n\033[91;2m* {formatted_title} \033[91;2m*\033[0m")
    print(borderline)

    print("\nPlease Log In")
    input_username = input("\033[94mEnter username:\033[0m ")
    input_password = MaskPassword("\033[94mEnter password:\033[0m ")

    #check if super admin has logged in
    checkSuperAdmin = validate_superAdmin(input_username, input_password)
    if (checkSuperAdmin == True):
        clear_console()    
        print("\033[32m\nLogged in successfully!\033[0m")
        SuperAdminPage()
        return  
    
    #input validation for username and password
    while (validate_username(input_username) == False or validate_password(input_password) == False):
        input_username = input("\033[94mEnter username:\033[0m ")
        input_password = MaskPassword("\033[94mEnter password:\033[0m ")

    #authorization and authenthication
    login = Login()


    #go to account
    clear_console()    
    print("\033[32m\nLogged in successfully!\033[0m")
    

def MemberOptions():
    while(True):
        print("\n\033[95mMember Options\033[0m ")
        print("\n1. Add new member \n2. Update member profile \n3. Search member \n4. ← Go back")
        user_input = int(input("\n\033[94mEnter a number: \033[0m"))
        if (user_input == 4):
            clear_console()
            return
        else:
            InvalidInput()
        #TODO 1,2,3




def TrainerPage(firstname, lastname, registration_date):
    
    while(True):
        clear_console()
        print(f"\n\033[95m{firstname} {lastname} \n{registration_date}\n\033[0m")
        print("1. Update password \n2. Member options \n3. Log out \n")
        user_input = int(input("\033[94mEnter a number: \033[0m"))

        #TODO check input validation for user_input

        if (user_input == 1):
            clear_console()
            #TODO
            return
        elif (user_input == 2):
            clear_console()
            MemberOptions()
        elif (user_input == 3):
            clear_console()
            LoginPage()
            break
        else:
            InvalidInput()

def TrainerOptions():
    while(True):
        print("\n\033[95mTrainer Options\033[0m ")
        print("\n1. Add new trainer \n2. Update trainer profile \n3. Delete trainer account \n4. Reset password of trainer account \n5. ← Go back")
        user_input = int(input("\n\033[94mEnter a number: \033[0m"))
        if (user_input == 5):
            clear_console()
            return
        else:
            InvalidInput()
        #TODO 1,2,3,4


def SystemAdminPage(firstname, lastname, registration_date):

    while(True):
        clear_console()
        print(f"\n\033[95m{firstname} {lastname} \n{registration_date}\n\033[0m")
        print("1. Update password \n2. Member options \n3. Trainer options \n4. View users \n5. View logs \n6. Backup and restore system \n7. Log out \n")
        user_input = int(input("\033[94mEnter a number: \033[0m"))

        if (user_input == 1):
            #TODO
            return
        elif (user_input == 2):
            clear_console()
            MemberOptions()
        elif (user_input == 3):
            clear_console()
            TrainerOptions()
        elif (user_input == 4):
            clear_console()
            #TODO
            return
        elif (user_input == 5):
            clear_console() 
            #TODO
            return
        elif (user_input == 6):
            clear_console()
            #TODO
            return
        elif (user_input == 7):
            clear_console()
            LoginPage()
            break
        else:
            InvalidInput()

def SystemAdminOptions():
    while(True):
        print("\n\033[95mSystem Administrator Options\033[0m ")
        print("\n1. Add new admin \n2. Update admin profile \n3. Delete admin account \n4. Reset password of admin account \n5. ← Go back")
        user_input = int(input("\n\033[94mEnter a number: \033[0m"))
        if (user_input == 5):
            clear_console()
            return
        else:
            InvalidInput()
        #TODO 1,2,3,4

def SuperAdminPage():
    #clear_console()
    print("\n\033[95msuper_admin \033[0m \n")
    print("1. View users \n2. Member options \n3. Trainer options \n4. Admin options \n5. View logs \n6. Backup and restore system \n7. Log out \n")

    while(True):
        user_input = int(input("\033[94mEnter a number: \033[0m"))

        if (user_input == 1):
            clear_console()
            #TODO
            return
        elif (user_input == 2):
            clear_console()
            MemberOptions()
        elif (user_input == 3):
            clear_console()
            TrainerOptions()
        elif (user_input == 4):
            clear_console()
            SystemAdminOptions()
        elif (user_input == 5):
            clear_console() 
            #TODO
            return
        elif (user_input == 6):
            clear_console()
            #TODO
            return
        elif (user_input == 7):
            clear_console()
            LoginPage()
            break
        else:
            InvalidInput()        

# LoginPage()
# TrainerPage('Twinkle', 'Niddha', "18-05-2023")
# MemberOptions()
# SystemAdminPage('Twinkle', 'Niddha', "18-05-2023")
# SuperAdminPage()


