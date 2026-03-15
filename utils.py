# Made by Maheen Abbasi for the 291 mini-project 1 on March 1, 2026

"""
This file contains reuseable helper functions used by the rest of the program
"""

# imports
import shutil

# Max num of results to display on a page
MAX_ON_PAGE = 5

"""
Paginate function that will:
    --> Show 5 results per page
    --> Handle next/previous actions
    --> Let the user select a course

Input: cursor, base_query, and params (as tuple)
Output: a selected cid (if that option is chosen)
"""
def paginate(cursor, base_query, params):
    # Track which page the user is on using 0-indexing
    page = 0

    while True:
        # Calculate how many rows to skip based on the curret page
        offset = page * MAX_ON_PAGE

        # Append the limit (rows to display) and offset (skip first n rows) to the base query for pagniation
        paginated = base_query + " LIMIT ? OFFSET ?"

        # Execute the query with limit = 5, offset (calculated earlier), and params given by the caller
        cursor.execute(paginated, params + (MAX_ON_PAGE, offset))
        rows = cursor.fetchall()

        # Handle empty results
        if not rows:
            # Case 1: no results at all
            if page == 0:
                print("No records.\n")
                return
            # Case 2: past the last page
            else:
                print("No more records.")
                page -= 1
                continue
        
        # Display each row
        print()
        center_print("ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ COURSES ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ")
        for row in rows:
            lines = [
                "",
                f"Course ID: {row['cid']}",
                f"Title: {row['title']}",
                f"Description: {row['description']}",
                f"Category: {row['category']}",
                f"Price: {row['price']}",
                f"Pass Grade: {row['pass_grade']}",
                f"Max Students: {row['max_students']}",
                f"Current Enrollment: {row['current_enrollment']}",
                ""
            ]
            for line in lines:
                center_print(line)
                
        center_print("ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ END PAGE ƸӜƷ.•°*”˜˜”*°•.ƸӜƷ•°*”˜˜”*°•.ƸӜƷ")
        
        # Nav options based on the current state
        print("\nOptions:")
        if page > 0:
            print("P. Prev")
        if len(rows) == MAX_ON_PAGE:
            print("N. Next")
        print("S. Select by cid")
        print("B. Back")
        
        # Get user input
        choice = input("\nPlease choose an option: ").strip().lower()
        print("")

        # Validate and process user input
        if choice == "n" and len(rows) == MAX_ON_PAGE:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "s":
            cid = input("Enter cid: ")
            return cid
        elif choice == "b":
            return None
        else:
            print("🚫 Invalid option, please try again. 🚫")

"""
Helper function to help center the terminal output so the tables look nicer, using shutil
"""
def center_print(text = ""):
    width = shutil.get_terminal_size().columns
    print(text.center(width))

"""
Header Pattern
"""
def center_divider(pattern = "--❁", repeat = 15):
    width = shutil.get_terminal_size().columns
    line = pattern * repeat
    print(line.center(width))