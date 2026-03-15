# Made by Maheen Abbasi for the 291 mini-project 1 on Feb. 23 2026

"""
This file handles the register and login fucntions of the program

Rules: password stored as plain text; parameterized queries; mask password input
"""

# imports
import getpass

"""
Function for an existing user to login.

Input: conn
Output: Returns a dict of the user made from converting the Row object, or None if uid and/or password was incorrect
"""
def login(conn):
    cursor = conn.cursor()

    # Get user input (with enforcement of numerical uid)
    uid_in = input("\n❁›--› Enter User ID: ").strip()
    if not uid_in.isdigit():
        print("\n🚫 User ID must be numeric. 🚫")
        return None
    uid = int(uid_in)

    password = getpass.getpass("❁›--› Enter Password: ").strip()

    # Verify
    cursor.execute("SELECT * FROM users WHERE uid = ? AND pwd = ?", (uid, password))
    user = cursor.fetchone()

    # Feedback
    if user:
        word = "an"
        if user['role'] == "Student":
            word = "a"
        print(f"\n✅ Login successful ✅\n\n╰┈➤ Hello, {user['name']}! You are currently logged in as {word} {user['role']}.")
        return dict(user)
    else:
        print("\n🚫 Invalid uid or password 🚫\n")
        return None
    
"""
Function for a new user ot register

Input: conn
Output: Retruns dict with the new user's info, or None if regitration fails
"""
def register(conn):
    cursor = conn.cursor()

    # User input
    name = input("\n❁›--› Enter your name: ").strip()
    email = input("❁›--› Enter your email: ").strip()
    password = getpass.getpass("❁›--› Enter a password: ").strip()

    # Verify that the email is unique (case insensitive vers)
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,))
    if cursor.fetchone():
        print("\n🚫 The email is already in use. 🚫")
        return None

    # Insert the new user
    cursor.execute("INSERT INTO users (name, email, role, pwd) VALUES (?, ?, ?, ?)", 
                   (name, email, "Student", password))
    conn.commit()

    # Feedback and uid
    new_uid = cursor.lastrowid
    print(f"\n✅ Registration was successful, your user ID is: {new_uid} ✅\n")
    
    return {
        "uid": new_uid,
        "name": name,
        "role": "Student"
    }