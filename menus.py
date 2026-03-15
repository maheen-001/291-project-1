# Made by Maheen Abbasi for the 291 mini-project 1 on Feb. 23 2026

"""
This filw contains the role=based menu routing
"""

# Imports
from student import search, view_enrolled, past_pay
from admin import top_5_active, payment_counts
from instructor import update_course, add_student, view_course_stats
from utils import center_print


"""
Student menu
"""
def student_menu(conn, user):
    while True:
        print()
        center_print("☆彡 ----- Student Menu ----- ☆彡")
        center_print("1. Search Courses")
        center_print("2. View Enrolled Courses")
        center_print("3. View Past Payments")
        center_print("4. Logout")
        center_print("5. Exit")

        # User input
        choice = input("\n❁›--› Please choose an option (1-5): ")

        # Route
        if choice == "1":
            search(conn, user)
        elif choice == "2":
            view_enrolled(conn, user)
        elif choice == "3":
            past_pay(conn, user)
        elif choice == "4":
            break
        elif choice == "5":
            print("\nExiting...\n")
            exit()
        else:
            print("\n🚫 Invalid choice. 🚫")

"""
Instructor menu
"""
def instructor_menu(conn, user):
    while True:
        print()
        center_print("☆彡 ----- Instructor Menu ----- ☆彡")
        center_print("1. Update Course")
        center_print("2. Add Student")
        center_print("3. View Course Stats")
        center_print("4. Logout")
        center_print("5. Exit")

        # User input
        choice = input("❁›--› Please choose an option (1-5): ")

        # Route
        if choice == "1":
            print("Update Course")
            update_course(conn, user)
        elif choice == "2":
            add_student(conn, user)
        elif choice == "3":
            view_course_stats(conn, user)
        elif choice == "4":
            break
        elif choice =="5":
            print("\nExiting...\n")
            exit()
        else:
            print("\n🚫 Invalid choice. 🚫")

"""
Admin menu
"""
def admin_menu(user, conn):
    while True:
        print()
        center_print("☆彡 ----- Admin Menu ----- ☆彡")
        center_print("1. Top 5 courses by active enrollment")
        center_print("2. Payment counts per course")
        center_print("3. Logout")
        center_print("4. Exit")

        # User input
        choice = input("\n❁›--› Please choose an option (1-4): ")

        # Route
        if choice == "1":
            top_5_active(conn)
        elif choice == "2":
            payment_counts(conn)
        elif choice == "3":
            break
        elif choice == "4":
            print("\nExiting...\n")
            exit()
        else:
            print("\n🚫 Invalid choice. 🚫")