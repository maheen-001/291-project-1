# Made by Maheen Abbasi for the 291 mini-project 1 on Feb. 23 2026

"""
The main python program
"""

# Imports
from db import connect
from auth import login, register
from menus import student_menu, instructor_menu, admin_menu

def main():
    conn = connect()

    # Main menu
    while True:
        print("\n# ----- Welcome ----- #")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        # User input
        choice = input("Please choose an option (1-3): ")

        # Handle input

        # Login
        if choice == "1":
            user = login(conn)

            if user:
                role = user["role"]

                if role == "Student":
                    student_menu(user)
                elif role == "Instructor":
                    instructor_menu(user)
                elif role == "Admion":
                    admin_menu(user)
        
        # Register
        elif choice == "2":
            user = register(conn)
        
        # Exit
        elif choice == "3":
            print("Exiting...")
            break

        # Invalid
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()