from datetime import datetime
from random import randint
from database import Database
from inputvalidation import *
from log import Log

class Member:
    def __init__(self, member_id, fn, ln, age, gender, weight, strname, housenr, zip, city, email, mobile, date):
        self.memberId = member_id
        self.firstname = fn
        self.lastname = ln
        self.age = age
        self.gender = gender
        self.weight = weight
        self.streetname = strname
        self.housenumber = housenr
        self.zipcode = zip
        self.city = city
        self.email = email
        self.mobile = mobile
        self.registrationDate = date
    


def get_current_date():
    date = datetime.now()
    return date.strftime("%d-%m-%Y")


def member_id_generator():

    #get two last digit of current year
    year = datetime.now().year % 100

    #get a random 7 digit number
    random_number = ''.join(["{}".format(randint(0, 9)) for num in range(0, 7)])
    
    #calculate checksum
    sum = 0
    for i in random_number:
        sum += int(i)
    for i in str(year):
        sum += int(i)
    checksum = sum % 10

    return str(year) + random_number + str(checksum)

def add_new_member(user):
    print("\nAdd new member ")
    db = Database()
    while True:
        print("\nDo you want to add a new member? \n\n1. Yes \n2. No")
        inp = input("\nEnter a number: ")
        if validate_numberInput(inp, 1, 2) == False:
            InvalidInput()
        else:
            inp = int(inp)
            if inp == 2:
                return
            else:
                break
    
    #ask firstname
    while True:
        firstname = input("\nEnter First Name: ")
        if validate_name(firstname) == False:
            print("Name invalid. Try again")
        else:
            break

    #ask lastname
    while True:
        lastname = input("Enter Last Name: ")
        if validate_name(lastname) == False:
            print("Name invalid. Try again")
        else:
            break

    #ask age
    while True:
        age = input("Enter Your Age: ")
        if validate_age(age) == False:
            print("Age invalid. Try again")
        else:
            break

    #ask gender
    while True:
        gender = input("Enter Your Gender (M/F/O): ")
        if validate_gender(gender) == False:
            print("Input must contain letter M (male), F (female) or O (others)")
        else:
            break

    #ask weight
    while True:
        weight = input("Enter Your Weight: ")
        if validate_weight(weight) == False:
            InvalidInput()
        else:
            break

    #ask streetname
    while True:
        streetname = input("Enter Your Street Name: ")
        if validate_name(streetname) == False:
            print("Street name invalid. Try again")
        else:
            break

    #ask house number
    while True:
        house_nr = input("Enter Your House Number (ex: 104B or 55): ")
        if validate_houseNr(house_nr) == False:
            InvalidInput()
        else:
            break

    #ask zip code
    while True:
        zip = input("Enter Your Zip Code (DDDDXX): ")
        if validate_zipCode(zip) == False:
            InvalidInput()
        else:
            break

    #ask city
    print("\nWhich city do you live in?")
    list_city = ["Amsterdam", "Rotterdam", "Den Haag", "Utrecht", "Tilburg", "Eindhoven", "Breda", "Delft", "Leiden", "Nijmegen"]
    i = 1
    for j in list_city:
        print(str(i) + ". " + j)
        i += 1

    while True:
        number = input("\nEnter a number: ")
        if validate_numberInput(number,1,10) == False:
            InvalidInput()
        else:
            break
    city = list_city[int(number) - 1]

    #ask email
    while True:
        email = input("Enter Email Address: ")
        if validate_email(email) == False:
            print("Invalid email address. Try again")
        else:
            break

    #ask phone nr
    phone = "+31-6-"
    while True:
        input_nr = input(f"Fill in mobile number:  {phone}")
        if validate_phoneNr(input_nr) == False:
            print("Invalid mobile phone. Try again")
        else:
            break
    phone += input_nr

    #generate member id
    memberId = member_id_generator()
    #check if member id exists
    while db.searchMemberID(memberId) == True:
        memberId = member_id_generator()

    #get date
    registration_date = get_current_date()

    #add info to database
    member = Member(memberId, firstname, lastname, age, gender, weight, streetname, house_nr, zip, city,email, phone, registration_date)
    db.insertMemberData(member)

    print("\nNew member added!")
    Log(user.Username, "Created new member", f"memberId: {memberId}", "No").log() #log incident
    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return
    
def InvalidInput():
    print("Invalid input. Try again \n")

def search_member():
    print("\nSearch member \n")
    while True:
        search_key = input("Enter search key: ") 
        if validate_searchkey(search_key) == False:
            InvalidInput()
        else:
            break
    
    #search in database
    db = Database()
    result = db.searchMember(search_key)

    #if result found print
    if len(result) == 0:
        print("No result found")
    else:
        print(f"\n{str(len(result))} Result Found: \n")
        count = 1
        for i in result:
            print(f"{count}| Member Id = {i[0]}")
            print(f"   First Name = {i[1]}")
            print(f"   Last Name = {i[2]}")
            print(f"   Age = {i[3]}")
            print(f"   Gender = {i[4]}")
            print(f"   Weight = {i[5]}")
            print(f"   Address = {i[6]} {i[7]}")
            print(f"   Zip Code = {i[8]}")
            print(f"   City = {i[9]}")
            print(f"   Email Address = {i[10]}")
            print(f"   Mobile = {i[11]}")
            print(f"   Registration Date = {i[12]}\n")

            count += 1

    while True:
        back = input("Enter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return
        
def update_member_profile(user):
    db = Database()
    print("\nUpdate/Modify Member Profile \n")

    while True:
        print("\nPlease note that you will need the member ID to update or modify the member's profile. \nDo you want to continue? \n\n1. Yes \n2. No")
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
        input_memID = input("Enter member Id: ")
        if validate_memberId(input_memID) == True:

            #check if member id exists
            result = db.searchMemberID(input_memID)

            #if member exists ask what to update
            if result == True:
                print("\nChoose option to update: \n1. First Name \n2. Last Name \n3. Age \n4. Gender \n5. Weight \n6. Street Name \n7. House Number \n8. Zip Code \n9. City \n10. Email Address \n11. Mobile Number")
                
                while True:
                    user_input = input("\nEnter a number: ")
                    if validate_numberInput(user_input, 1,11) == False:
                        InvalidInput()
                    else:
                        user_input = int(user_input)
                        break

                #update first name
                if user_input == 1:
                    while True:
                        new_fname = input("\nEnter new First Name: ")
                        if (validate_name(new_fname) == False):
                            print("Name invalid. Try again")
                        else:
                            break
                    db.updateMemberProfile(input_memID, "FirstName", new_fname)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"First name of member with id: {input_memID} updated", "No").log()
                    break                    

                #update last name
                elif user_input == 2:
                    while True:
                        new_lname = input("\nEnter new Last Name: ")
                        if (validate_name(new_lname) == False):
                            print("Name invalid. Try again")
                        else:
                            break
                    db.updateMemberProfile(input_memID, "LastName", new_lname)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Last name of member with id: {input_memID} updated", "No").log()
                    break

                #update age
                elif user_input == 3:
                    while True:
                        new_age = input("\nEnter new Age: ")
                        if validate_age(new_age) == False:
                            print("Age invalid. Try again")
                        else:
                            break
                    db.updateMemberProfile(input_memID, "Age", new_age)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Age of member with id: {input_memID} updated", "No").log()
                    break

                #update gender    
                elif user_input == 4:
                    while True:
                        new_gender = input("\nEnter new Gender (M/F/O): ")
                        if validate_gender(new_gender) == False:
                            print("Input must contain letter M (male), F (female) or O (others)")
                        else:
                            break
                    db.updateMemberProfile(input_memID, "Gender", new_gender)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Gender of member with id: {input_memID} updated", "No").log()
                    break
                
                #update weight    
                elif user_input == 5:
                    while True:
                        new_weight = input("\nEnter new Weight: ")
                        if validate_weight(new_weight) == False:
                            InvalidInput()
                        else:
                            break
                    db.updateMemberProfile(input_memID, "Weight", new_weight)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Weight of member with id: {input_memID} updated", "No").log()
                    break

                #update streetname
                elif user_input == 6:
                    while True:
                        new_streetname = input("\nEnter new Street Name: ")
                        if validate_name(new_streetname) == False:
                            print("Street name invalid. Try again")
                        else:
                            break
                    db.updateMemberProfile(input_memID, "StreetName", new_streetname)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"streetname of address of member with id: {input_memID} updated", "No").log()
                    break

                #update house nr   
                elif user_input == 7:
                    while True:
                        new_house_nr = input("\nEnter new House Number: ")
                        if validate_houseNr(new_house_nr) == False:
                            InvalidInput()
                        else:
                            break
                    db.updateMemberProfile(input_memID, "HouseNr", new_house_nr)   
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"House number of address of member with id: {input_memID} updated", "No").log()
                    break
                
                #update zip code    
                elif user_input == 8:
                    while True:
                        new_zip = input("\nEnter new Zip Code (DDDDXX): ")
                        if validate_zipCode(new_zip) == False:
                            InvalidInput()
                        else:
                            break
                    db.updateMemberProfile(input_memID, "Zip", new_zip)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Zipcode of member with id: {input_memID} updated", "No").log()
                    break
                
                #update city
                elif user_input == 9:
                    list_city = ["Amsterdam", "Rotterdam", "Den Haag", "Utrecht", "Tilburg", "Eindhoven", "Breda", "Delft", "Leiden", "Nijmegen"]
                    i = 1
                    for j in list_city:
                        print(str(i) + ". " + j)
                        i += 1
                    while True:
                        res = input("\nEnter number to update city: ")
                        if validate_numberInput(res,1,10) == False:
                            InvalidInput()
                        else:
                            break    
                    
                    new_city = list_city[int(res) - 1]
                    db.updateMemberProfile(input_memID, "City", new_city)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"City of member with id: {input_memID} updated", "No").log()
                    break
                
                #update email
                elif user_input == 10:
                    while True:
                        new_email = input("\nEnter new email address: ")
                        if validate_email(new_email) == False:
                            print("Invalid email address. Try again")
                        else:
                            break
                    db.updateMemberProfile(input_memID, "Email", new_email)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Email of member with id: {input_memID} updated", "No").log()
                    break
                
                #update mobile    
                elif user_input == 11:
                    new_phone = "+31-6-"
                    while True:
                        input_nr = input(f"Fill new mobile number:  {new_phone}")
                        if (validate_phoneNr(input_nr) == False):
                            print("Invalid mobile phone. Try again")
                        else:
                            break
                    new_phone += input_nr
                    db.updateMemberProfile(input_memID, "Mobile", new_phone)
                    print("\nMember profile updated!")
                    Log(user.Username, "Updated member profile", f"Mobile of member with id: {input_memID} updated", "No").log()
                    break

            else:
                print("Member not found. try again")

        else:
            InvalidInput()

    while True:
        back = input("\nEnter 1 to go back: ")
        if validate_numberInput(back, 1, 1) == False:
            InvalidInput()
        else:
            return            

def delete_member(user):
    db = Database()
    print("\nDelete Member ")

    while True:
        print("\nPlease note that you will need the member ID to delete a member's profile. \nDo you want to continue? \n\n1. Yes \n2. No")
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
        input_memID = input("\nEnter member Id: ")
        if validate_memberId(input_memID) == True:

            #check if member id exists
            result = db.searchMemberID(input_memID)

            #if exists delete member
            if result == True:
                while True:
                    print("\nAre you sure you want to delete this member? \n\n1. Yes \n2. No")
                    num = input("\nEnter a number: ")
                    if validate_numberInput(num,1,2) == False:
                        InvalidInput()
                    else:
                        num = int(num)
                        if num == 1:
                            db.deleteMember(input_memID)
                            print("\nMember deleted succesfully!")
                            Log(user.Username, "Member is deleted", f"Member with id {input_memID} is deleted", "No").log()                            
                            #Go back
                            while True:
                                back = input("\nEnter 1 to go back: ")
                                if validate_numberInput(back, 1, 1) == False:
                                    InvalidInput()
                                else:
                                    return   
                        elif (num == 2):
                            return
                        else:
                            InvalidInput()
            else:
                print("Member not found. please try again")
        else:
            InvalidInput()

    

        
            


