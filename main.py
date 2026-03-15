# Made by Maheen Abbasi for the 291 mini-project 1 on Feb. 23 2026

"""
The main python program
"""

# Imports
from db import connect
from auth import login, register
from menus import student_menu, instructor_menu, admin_menu
from utils import center_print

def main():
    conn = connect()

    # Main menu
    while True:
        print()
        center_print("ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ")
        center_print("➳♥ ----- Welcome ----- ➳♥")
        center_print("ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ")
        print()
        center_print("1. Login")
        center_print("2. Register")
        center_print("3. Exit")

        # User input
        choice = input("\n❁›--› Please choose an option (1-3): ")

        # Handle input

        # Login
        if choice == "1":
            user = login(conn)

            if user:
                role = user["role"]

                if role == "Student":
                    student_menu(conn, user)
                elif role == "Instructor":
                    instructor_menu(conn, user)
                elif role == "Admin":
                    admin_menu(user, conn)
        
        # Register
        elif choice == "2":
            user = register(conn)
        
        # Exit
        elif choice == "3":
            print("\nExiting...\n")
            break

        # Invalid
        else:
            print("\n🚫 Invalid choice, please try again. 🚫")

if __name__ == "__main__":
    main()