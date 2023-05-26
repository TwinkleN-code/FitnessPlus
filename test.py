import bcrypt
import sqlite3

# Connect to the SQLite3 database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create the users table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              username TEXT UNIQUE,
              password TEXT,
              salt TEXT)''')
conn.commit()

def create_user(username, password):
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Insert the user into the database
    c.execute("INSERT INTO users (username, password, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
    conn.commit()

def authenticate_user(username, password):
    # Retrieve the user from the database
    c.execute("SELECT password, salt FROM users WHERE username=?", (username,))
    row = c.fetchone()

    if row:
        stored_password = row[0].encode('utf-8')
        salt = row[1].encode('utf-8')

        # Hash the entered password with the stored salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Verify the password
        if hashed_password == stored_password:
            print("Authentication successful")
        else:
            print("Authentication failed")
    else:
        print("User not found")

def main():
    while True:
        print("1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            create_user(username, password)
            print("User created successfully\n")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            authenticate_user(username, password)
            print()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.\n")

    # Close the database connection
    conn.close()

# if __name__ == '__main__':
#     main()