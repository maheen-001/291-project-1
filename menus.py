# Made by Maheen Abbasi for the 291 mini-project 1 on Feb. 23 2026

"""
This filw contains the role=based menu routing

TODO: Nothing is actually implemented yet so everything
"""

"""
Student menu
"""
def student_menu(user):
    while True:
        print("\n# ----- Student Menu ----- #")
        print("1. TODO: add feature")
        print("2. Logout")
        print("3. Exit")

        # User input
        choice = input("Please choose an options (1-3): ")

        # Route
        if choice == "2":
            break
        elif choice == "3":
            exit()
        else:
            print("TODO: Not implemented.")

"""
Instructor menu
"""
def instructor_menu(user):
    while True:
        print("\n# ----- Instructor Menu ----- #")
        print("1. TODO: add feature")
        print("2. Logout")
        print("3. Exit")

        # User input
        choice = input("Please choose an options (1-3): ")

        # Route
        if choice == "2":
            break
        elif choice == "3":
            exit()
        else:
            print("TODO: Not implemented.")

"""
Admin menu
"""
def admin_menu(user):
    while True:
        print("\n# ----- Admin Menu ----- #")
        print("1. TODO: add feature")
        print("2. Logout")
        print("3. Exit")

        # User input
        choice = input("Please choose an options (1-3): ")

        # Route
        if choice == "2":
            break
        elif choice == "3":
            exit()
        else:
            print("TODO: Not implemented.")