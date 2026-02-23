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
    uid_in = input("Enter User ID: ").strip()
    if not uid_in.isdigit():
        print("User ID must be numeric\n")
        return None
    uid = int(uid_in)

    password = getpass.getpass("Enter Password: ").strip()

    # Verify
    cursor.execute("SELECT * FROM users WHERE uid = ? AND pwd = ?", (uid, password))
    user = cursor.fetchone()

    # Feedback
    if user:
        print("Login successful\n")
        return dict(user)
    else:
        print("Invalid uid or password\n")
        return None
    
"""
Function for a new user ot register

Input: conn
Output: Retruns dict with the new user's info, or None if regitration fails
"""
def register(conn):
    cursor = conn.cursor()

    # User input
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    password = getpass.getpass("Enter a password: ").strip()

    # Verify that the email is unique (case insensitive vers)
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (email,))
    if cursor.fetchone():
        print("The email is already in use\n")
        return None
    
    # Generate a new uid (set as 1 if no uids exist, otherwise make it 1 higher than the max)
    cursor.execute("SELECT MAX(uid) FROM users")
    max_uid = cursor.fetchone()[0]
    new_uid = 1 if max_uid is None else max_uid + 1

    # Insert the new user
    cursor.execute("INSERT INTO users (uid, name, email, role, pwd) VALUES (?, ?, ?, ?, ?)", 
                   (new_uid, name, email, "Student", password))
    conn.commit()

    # Feedback
    print(f"Registration was successful, your user ID is: {new_uid}\n")
    
    return {
        "uid": new_uid,
        "name": name,
        "role": "Student"
    }