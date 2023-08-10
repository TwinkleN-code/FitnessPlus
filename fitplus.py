import os
from encryption import *
from userinterface import LoginPage
from database import Database


def main():
    
    #create private and public key if not exists
    if not os.path.isfile('private_key.pem') and not os.path.isfile('public_key.pem'):
        private_key = generate_private_key()
        public_key = generate_public_key(private_key)
        save_private_key(private_key)
        save_public_key(public_key)

    #create database
    db = Database()
    db.createDatabase()

    #login  
    LoginPage()

main()