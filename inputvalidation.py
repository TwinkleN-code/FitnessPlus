import re
from database import Database

from log import Log

class validationType:
    def __init__(self, validate, errortext) -> None:
        self.error_text = errortext
        self.validation = validate


def validate_username(username):
    # Remove whitespaces
    username = username.strip()

    # check for null bytes
    if check_null_bytes(username) == True:
        Log("", "Null bytes used", f"null bytes were found when validating username: {username}", "Yes")
        db = Database()
        db.create_alert()
        return validationType(False, "username contains invalid characters")

    #must have length >= 8 and <= 12
    if not (len(username) >= 8 and len(username) <= 12):
        return validationType(False, "username must have minimal 8 and maximal 12 characters")
    
    #must be started with a letter or underscore
    if not re.match(r'^[a-zA-Z_]', username):
        return validationType(False, "username must start with a letter or an underscore")
    
    #can contain letters, numbers and _ '.
    if not re.match(r'^[a-zA-Z0-9_\'\.]+$', username):
        return validationType(False, "username contains invalid characters")
    
    return validationType(True, "")


def validate_password(password):
    # Remove whitespaces
    password = password.strip()

    # check for null bytes
    if check_null_bytes(password) == True:
        Log("", "Null bytes used", f"null bytes were found when validating password: {password}", "Yes")
        db = Database()
        db.create_alert()
        return validationType(False, "password contains invalid characters")

    #must have length <= 12 and >= 30
    if not (len(password) >= 12 and len(password) <= 30):
        return validationType(False, "password must have minimal 12 and maximal 30 characters")
    
    #can contain (a-z), (A-Z), (0-9), ~!@#$%&_-+='|\(){}[]:;'<>,.?/
    if not re.match(r"^[a-zA-Z0-9~!@#$%&+`|\(){}[\]:;'<>,.?/_-]+$", password):
        Log("", "Invalid characters", f"invalid characters were found when validating password: {password}", "No")
        return validationType(False, "password contains invalid characters")

    #must have at least one lowercase, one uppercase, one digit, one special character
    if not re.search(r"[a-z]", password) or \
       not re.search(r"[A-Z]", password) or \
       not re.search(r"\d", password) or \
       not re.search(r"[~!@#$%&+`|\(){}[\]:;'<>,.?/_-]", password):
        return validationType(False, "password must contain at least one lowercase, one uppercase, one digit and one special character")
    
    return validationType(True, "")

def validate_superAdmin(username, password):
    # Remove whitespaces
    username = username.strip()
    password = password.strip()

    # check for null bytes
    if check_null_bytes(username) == True or check_null_bytes(password) == True:
        return False

    if username == "super_admin" and password == "Admin_123!":
        return True
    return False


def validate_numberInput(user_input, min, max):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        return False

    try:
        number = int(user_input)
        #check if entered number contains min and max value
        if (min <= number <= max): 
            return True
        else:
            return False
    except ValueError:
        return False

def validate_name(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating name: {user_input}", "No")
        return False

    # Minimum and max length check
    if len(user_input) < 2 and len(user_input) > 30:
        return False

    # Check if all characters are valid
    if not re.match(r"^[a-zA-Z'-.\sÀ-ÿ]+$", user_input):
        return False

    return True

def validate_age(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating name: {user_input}", "No")
        return False

    try:
        user_input = int(user_input) 
        if (user_input > 0 and user_input <= 100):
            return True
        else:
            return False
    except ValueError:
        return False
    
def validate_gender(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating gender: {user_input}", "No")
        return False

    if user_input.upper() not in ['M', 'F', 'O']:
        return False
    else:
        return True
    
def validate_weight(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating weight: {user_input}", "No")
        return False

    try:
        user_input = float(user_input) 
        if (user_input > 0):
            return True
        else:
            return False
    except ValueError:
        return False
    
def validate_houseNr(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating house number: {user_input}", "No")
        return False
    
    if (re.match(r'^\d+$', user_input)):
        return True
    elif (re.match(r'^\d+[a-zA-Z]$', user_input)):
        return True
    return False


def validate_zipCode(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating zipcode: {user_input}", "No")
        return False
    
    if (re.match(r'^\d{4}[A-Z]{2}$', user_input.upper())):
        return True
    return False

def validate_email(user_input):
    # Remove whitespaces
    user_input = user_input.strip()
    
    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating email: {user_input}", "No")
        return False

    if (re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', user_input)):
        return True
    return False

def validate_phoneNr(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating phone number: {user_input}", "No")
        return False
    
    return user_input.isdigit() and len(user_input) == 8

def validate_memberId(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating member id: {user_input}", "Yes")
        db = Database()
        db.create_alert()
        return False
    
    return user_input.isdigit() and len(user_input) == 10 

def validate_searchkey(user_input):
    # Remove whitespaces
    user_input = user_input.strip()

    # check for null bytes
    if check_null_bytes(user_input) == True:
        Log("", "Null bytes used", f"null bytes were found when validating search key: {user_input}", "Yes")
        db = Database()
        db.create_alert()
        return False

    #max 30 characters
    if (len(user_input) > 30 or len(user_input) == 0):
        return False

    if re.match(r'^[a-zA-Z0-9\-@ \'"\.,+À-ÿ]+$', user_input):
        return True
    return False

def check_null_bytes(input_string):
    if re.search(r'\x00', input_string):
        return True
    return False


