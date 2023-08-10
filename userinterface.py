import os
import bcrypt
from backup import CreateBackup, RestoreBackUp
from database import Database
from inputvalidation import *
from log import view_logs
from login import *
from member import *
from user import User
from user_profile import *


def LoginPage():
    title = "Fitness Plus"
    formatted_title = f"{title}"
    borderline = "¨" * (len(title) + 4)
    print(f"\n* {formatted_title} *")
    print(borderline)

    minutes = 5
    while True:
        user = Login(minutes)
        if user is not None:
            Log(user.Username, "Logged In", "", "No").log() #log succesfull login
            break
        minutes *= 2
    
    #go to account
    if user.Role.lower() == "super admin":
        clear_console()    
        SuperAdminPage(user)            
    elif user.Role.lower() == "trainer":
        clear_console()    
        TrainerPage(user)     
    elif user.Role.lower() == "system admin":
        clear_console()    
        SystemAdminPage(user)
            
    
def InvalidInput():
    print("Invalid input. try again \n")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def MemberOptions(user):

    while True:
        clear_console()
        print("\nMember Options ")

        #trainers can add, search and update
        if user.Role == "trainer":
            print("\n1. Add new member \n2. Search member \n3. Update member profile \n4. ← Go back")
        #system admins and super admins can add, update, search and delete
        elif user.Role == "system admin" or user.Role == "super admin":
            print("\n1. Add new member \n2. Search member \n3. Update or modify member profile \n4. Delete member \n5. ← Go back")
        
        user_input = input("\nEnter a number: ")
        if validate_numberInput(user_input, 1, 5) == False:
            InvalidInput()
        else:
            #if validation succeed convert input string to int
            user_input = int(user_input)
            if user_input == 1: 
                clear_console()
                add_new_member(user)          
            elif user_input == 2:
                clear_console()
                search_member()
            elif user_input == 3:
                clear_console()
                update_member_profile(user)
            elif user_input == 4 and user.Role == "trainer":
                clear_console()
                return
            elif user_input == 4 and (user.Role == "system admin" or user.Role == "super admin"):
                clear_console()
                delete_member(user)
            elif user_input == 5 and (user.Role == "system admin" or user.Role == "super admin"):
                clear_console()
                return
            else:
                InvalidInput()

def TrainerPage(user: User):
    clear_console()
    #check if account has a temporary password
    if (user.Temp == "Yes"):
        #update password
        print("You have a temporary password. You need to update your password")
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
        db = Database()
        db.updateUserProfile(user.Username, "Password", new_hashedpassw)
        db.updateUserProfile(user.Username, "Salt", new_salt)
        db.updateUserProfile(user.Username, "TemporaryPassword", "No")
        Log(user.Username, "Updated password", "", "No").log()
        print("\nUser password updated!")
        
        while True:
            cont = input("\nEnter 1 to continue: ")
            if validate_numberInput(cont, 1, 1) == False:
                InvalidInput()
            else:
                break 

    while True:
        clear_console()
        print(f"\n{user.FirstName} {user.LastName} \n{user.Date}\n")
        print("1. Update password \n2. Member options \n3. Log out \n")
        
        #input validation
        while True:
            user_input = (input("Enter a number: "))
            if validate_numberInput(user_input, 1, 3) == False:
                InvalidInput()
            else:
                #if validation succeed convert input string to int
                user_input = int(user_input)
                break

        if user_input == 1:
            clear_console()
            update_own_password(user)
        elif user_input == 2:
            clear_console()
            MemberOptions(user)
        elif user_input == 3:
            clear_console()
            LoginPage()
            break

   
def SystemAdminPage(user: User):
    clear_console()

    #check if account has a temporary password
    if (user.Temp == "Yes"):
        #update password
        print("You have a temporary password. You need to update your password")
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
        db = Database()
        db.updateUserProfile(user.Username, "Password", new_hashedpassw)
        db.updateUserProfile(user.Username, "Salt", new_salt)
        db.updateUserProfile(user.Username, "TemporaryPassword", "No")
        print("\nUser password updated!")
        Log(user.Username, "Updated password", "", "No").log()
        
        while True:
            cont = input("\nEnter 1 to continue: ")
            if validate_numberInput(cont, 1, 1) == False:
                InvalidInput()
            else:
                break

    #check if there are suspicious activities
    db = Database()
    alerts = db.get_alert()
    if alerts != [] and alerts[0][1] > 0:
        print(f"\nALERT: You have {alerts[0][1]} unread suspicious activities.")
        db.reset_alert("SystemAdmin")
        while True:
            back = input("\nEnter 1 to continue: ")
            if validate_numberInput(back, 1, 1) == False:
                InvalidInput()
            else:
                break

    while True:
        clear_console()
        print(f"\n{user.FirstName} {user.LastName} \n{user.Date}\n")
        print("1. Update password \n2. Member options \n3. Trainer options \n4. View users \n5. View logs \n6. Backup and restore system \n7. Log out \n")
        
        #input validation
        user_input = input("Enter a number: ")
        if validate_numberInput(user_input, 1, 7) == False:
            InvalidInput()
        else:
            #if validation succeed convert input string to int and read input
            user_input = int(user_input)

            if user_input == 1:
                clear_console()
                update_own_password(user)
            elif user_input == 2:
                clear_console()
                MemberOptions(user)
            elif user_input == 3:
                clear_console()
                TrainerOptions(user)
            elif (user_input == 4):
                clear_console()
                view_users_UI()
            elif (user_input == 5):
                clear_console() 
                view_log_UI()
            elif (user_input == 6):
                clear_console()
                backup_and_restore_UI(user) 
            elif (user_input == 7):
                clear_console()
                LoginPage()
                break
            else:
                InvalidInput()

def TrainerOptions(user):
    while(True):
        clear_console()
        print("\nTrainer Options ")
        print("\n1. Add new trainer \n2. Update trainer profile \n3. Delete trainer account \n4. Reset password of trainer account \n5. ← Go back")
        
        #input validation
        while True:
            user_input = input("\nEnter a number: ")
            if validate_numberInput(user_input, 1, 5) == False:
                InvalidInput()
            else:
                #if valiation succeed
                user_input = int(user_input)
                break
        
        if user_input == 1: 
            clear_console()
            add_new_user(user, "trainer")   
        elif user_input == 2:
            clear_console()
            update_user_profile(user, "trainer")
        elif user_input == 3:
            clear_console()
            delete_user(user, "trainer")
        elif user_input == 4:
            clear_console()
            reset_password(user, "trainer")            
        elif user_input == 5:
            clear_console()
            return
        else:
            InvalidInput()

def SystemAdminOptions(user):
    while True:
        clear_console()
        print("\nSystem Administrator Options ")
        print("\n1. Add new admin \n2. Update admin profile \n3. Delete admin account \n4. Reset password of admin account \n5. ← Go back")
        
        #input validation
        while True:
            user_input = input("\nEnter a number: ")
            if validate_numberInput(user_input, 1, 5) == False:
                InvalidInput()
            else:
                #if valiation succeed
                user_input = int(user_input)
                break

        if user_input == 1: 
            clear_console()
            add_new_user(user, "system admin")   
        elif user_input == 2:
            clear_console()
            update_user_profile(user, "system admin")
        elif user_input == 3:
            clear_console()
            delete_user(user, "system admin")
        elif user_input == 4:
            clear_console()
            reset_password(user, "system admin")            
        elif user_input == 5:
            clear_console()
            return
        else:
            InvalidInput()

def view_users_UI():
    db = Database()
    users = db.getUsersData()
    
    if (len(users) > 0):
        count = 1
        for user in users:
            print(f"\n{count}| User ID: {user[0]}")
            print(f"   Role: {user[1]}")
            print(f"   First Name = {user[2]}")
            print(f"   Last Name = {user[3]}")
            print(f"   Username = {user[5]}")
            print(f"   Registration Date = {user[4]}")
            count += 1
    else:
        print("\nThere are no users")

    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return
 
def view_log_UI():
    logs = view_logs()

    if (len(logs) > 0):
        for log in logs:
            if (log[6] == "No"):
                print(f"\nNo: {log[0]} \nUsername: '{log[1]}' \nDate: {log[2]} \nTime: {log[3]} \nDescription: {log[4]} \nAdditional Information: {log[5]} \nSuspicious: {log[6]}")
            else:
                print(f"\nNo: {log[0]} \nUsername: '{log[1]}' \nDate: {log[2]} \nTime: {log[3]} \nDescription: {log[4]} \nAdditional Information: {log[5]} \nSuspicious: {log[6]}")

    else:
        print("\nLogs are empty")

    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return
        
def backup_and_restore_UI(user):
    print("Choose an option: \n\n1. Make a backup of the system \n2. Restore backup \n3. ← Go back")
    while True:
        user_input = input("\nEnter a number: ")
        if validate_numberInput(user_input,1,3) == False:
            print("\nInput invalid. try again")
            break
        else:
            user_input = int(user_input)
            if user_input == 1:
                CreateBackup()
                print("\nA backup of the system is made!")
                Log(user.Username, "Made backup of the system", "", "No").log()
                break
            elif user_input == 2:
                RestoreBackUp()
                print("\nBackup restored!")
                Log(user.Username, "Restored backup", "", "No").log()
                break
            elif user_input == 3:
                return

    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return

def SuperAdminPage(user):

    #check if there are suspicious activities
    clear_console()
    db = Database()
    alerts = db.get_alert()
    if alerts != [] and alerts[0][2] > 0:
        print(f"\nALERT: You have {alerts[0][2]} unread suspicious activities.")
        db.reset_alert("SuperAdmin")
        while True:
            back = input("\nEnter 1 to continue: ")
            if validate_numberInput(back, 1, 1) == False:
                InvalidInput()
            else:
                break

    #menu
    while True:
        clear_console()
        print("\nsuper_admin ")
        print("\n1. View users \n2. Member options (add | update | delete | search profile) \n3. Trainer options (add | update | delete | reset password) \n4. Admin options (add | update | delete | reset password) \n5. View logs \n6. Backup and restore system \n7. Log out \n")
        
        #input validation
        user_input = input("Enter a number: ")
        if validate_numberInput(user_input, 1, 7) == False:
            InvalidInput()
        else:
            #if validation succeed convert input string to int and read input
            user_input = int(user_input)

            if user_input == 1:
                clear_console()
                view_users_UI()
            elif user_input == 2:
                clear_console()
                MemberOptions(user)
            elif user_input == 3:
                clear_console()
                TrainerOptions(user)
            elif user_input == 4:
                clear_console()
                SystemAdminOptions(user)
            elif user_input == 5:
                clear_console() 
                view_log_UI()
            elif user_input == 6:
                clear_console()
                backup_and_restore_UI(user)    
            elif user_input == 7:
                clear_console()
                LoginPage()
                break
            else:
                InvalidInput()        
