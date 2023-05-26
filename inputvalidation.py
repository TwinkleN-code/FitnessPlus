import re


def validate_username(username):
    #must have length >= 8 and <= 12
    if not (len(username) >= 8 and len(username) <= 12):
        print("\033[91m\nusername must have minimal 8 and maximal 12 characters\033[0m \n")
        return False
    
    #must be started with a letter or underscore
    if not re.match(r'^[a-zA-Z_]', username):
        print("\033[91m\nusername must start with a letter or an underscore\033[0m \n")
        return False
    
    #can contain letters, numbers and _ '.
    if not re.match(r'^[a-zA-Z0-9_\'\.]+$', username):
        print("\033[91m\nusername contains invalid characters\033[0m \n")
        return False

    return True


def validate_password(password):
    #must have length <= 12 and >= 30
    if not (len(password) >= 12 and len(password) <= 30):
        print("\033[91m\npassword must have minimal 12 and maximal 30 characters\033[0m \n")
        return False
    
    #can contain (a-z), (A-Z), (0-9), ~!@#$%&_-+='|\(){}[]:;'<>,.?/
    if not re.match(r"^[a-zA-Z0-9~!@#$%&+`|\(){}[\]:;'<>,.?/_-]+$", password):
        print("\033[91m\npassword contains invalid characters\033[0m \n")
        return False

    #must have at least one lowercase, one uppercase, one digit, one special character
    if not re.search(r"[a-z]", password) or \
       not re.search(r"[A-Z]", password) or \
       not re.search(r"\d", password) or \
       not re.search(r"[~!@#$%&+`|\(){}[\]:;'<>,.?/_-]", password):
        print("\033[91m\npassword must contain at least one lowercase, one uppercase, one digit and one special character\033[0m \n")
        return False
    
    return True

def validate_superAdmin(username, password):
    if (username == "super_admin" and password == "Admin_123!"):
        return True
    return False
