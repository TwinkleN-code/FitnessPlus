from userinterface import LoginPage
from database import Database


def main():
    db = Database()
    db.createDatabase()
    
    LoginPage()


main()