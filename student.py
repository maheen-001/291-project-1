# Made by Maheen Abbasi for the 291 mini-project 1 on March 1, 2026

"""
Handles student actions (search, enroll, view enrolled and relevant info)
"""

# Imports
from utils import paginate, MAX_ON_PAGE, center_print, center_divider
from datetime import datetime, timedelta
import shutil

"""
This function will dynamically build a SQL query based on the user's input(s)

Input: conn, user
Output: list of courses meeting the user's requirements
"""
def search(conn, user):
    cursor = conn.cursor()

    # Get the user input(s)
    print("")
    keyword = input("❁›--› Enter keyword (press Enter to skip): ").strip()
    category = input("❁›--› Filter by category (press Enter to skip): ").strip()
    min_price = input("❁›--› Min price (press Enter to skip): ").strip()
    max_price = input("❁›--› Max price (press Enter to skip): ").strip()
    print("")

    # Base query ends in WHERE 1=1, which is always true, so we can just append additional AND ... statements
    base_query = """
    SELECT c.cid, c.title, c.description, c.category, c.price, c.pass_grade, c.max_students,
    (SELECT COUNT(*) FROM enrollments e WHERE e.cid = c.cid AND e.role = 'Student'
    AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts) AS current_enrollment
    FROM courses c WHERE 1=1
    """

    # Empty params lisrt will; be updated with the base query after
    params = []

    # Assemble/build query by appending conditions specified by the input
    if keyword:
        base_query += " AND (LOWER(c.title) LIKE LOWER(?) OR LOWER(c.description) LIKE LOWER(?))"
        key_word = f"%{keyword}%"
        params.extend([key_word, key_word])
    
    if category:
        base_query += " AND c.category = ?"
        params.append(category)
    
    if min_price:
        base_query += " AND c.price >= ?"
        params.append(float(min_price))
    
    if max_price:
        base_query += " AND c.price <= ?"
        params.append(float(max_price))
    
    base_query += " ORDER BY c.cid"

    # trigger paginate
    while True:
        selected_cid = paginate(cursor, base_query, tuple(params))

        if selected_cid:
            show_course_details(conn, user, selected_cid)
        else:
            return

"""
This function will:
    --> Fetch and display the course
    --> Check if the user is already enrolled

Input: conn, user, cid
Output: course details
"""
def show_course_details(conn, user, cid):
    cursor = conn.cursor()

    # SQL query o get course details using the given cid
    cursor.execute("""
        SELECT c.cid, c.title, c.description, c.category, c.price, c.pass_grade, c.max_students,
        (SELECT COUNT(*) FROM enrollments e WHERE e.cid = c.cid AND e.role = 'Student' AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts)
        AS current_enrollment FROM courses c WHERE c.cid = ?
    """, (cid,))

    course = cursor.fetchone()

    # No course found, exit early
    if not course:
        print("\n🚫 Course not found! 🚫")
        input("\n❁›--› Press Enter to return.")
        return
    
    # Display each field of the course as key: value pairs
    print("\nCourse Details: ")
    for key in course.keys():
        print(f"{key}: {course[key]}")

    # Chekc if already enrolled
    cursor.execute("""
        SELECT * FROM enrollments WHERE cid = ? AND uid = ? AND role = 'Student' AND CURRENT_TIMESTAMP BETWEEN start_ts AND end_ts
    """, (cid, user["uid"]))

    enrollment = cursor.fetchone()

    # If the user is already enrolled, don't show the option
    if enrollment:
        print("\n╰┈➤ You are already enrolled in this course.")
        input("\n❁›--› Press Enter to return.")
        return
    # Show option to enroll if the user is NOT already enrolled
    else:
        while True:
            print("\nOptions:\n")
            print("1. Enroll")
            print("2. Back\n")

            choice = input("❁›--› Please choose an option (1-2): ")

            if choice == "1":
                enroll(conn, user, course)
                return
            elif choice == "2":
                return
            else:
                print("\n🚫 Invalid choice. 🚫")

"""
This funciton allows a student to enroll in a course (with payment). It will:
    --> Validate the card num, cvv, and expiry date
    --> Check requirements before enrolling (course not full, student not already enrolled)
    --> Insert into enrollments and payments if everything is successful.

Note: start_ts has the default CURRENT_TIMESTAMP, and end_ts is 1 year from now

Input: conn, user, course
Output: confirmation message on successful enroll, failure message otherwise
"""
def enroll(conn, user, course):
    cursor = conn.cursor()
    cid = course["cid"]

    # Prevent double enrollment
    cursor.execute("""
        SELECT 1 FROM enrollments WHERE cid = ? AND uid = ? AND role = 'Student' AND CURRENT_TIMESTAMP BETWEEN start_ts AND end_ts
    """, (cid, user["uid"]))

    if cursor.fetchone():
        print("\n🚫 You already have an active enrollment in this course. 🚫")
        return
    
    # Check if the course is full
    cursor.execute("""
        SELECT COUNT(*) FROM enrollments WHERE cid = ? AND role = 'Student' AND CURRENT_TIMESTAMP BETWEEN start_ts AND end_ts
    """, (cid,))
    current_enrollment = cursor.fetchone()[0]

    if current_enrollment >= course["max_students"]:
        print("\n🚫 Course is full. Cannot enroll. 🚫")
        input("\n❁›--› Press Enter to return.")
        return
    
    # Course isn't full, get credit card input (and remove spaces!)
    card_number = input("❁›--› Enter credit card number: ").replace(" ", "")
    cvv = input("❁›--› Enter CVV: ").strip()
    expiry = input("❁›--› Enter expiry date (MM/YYYY): ").strip()

    # Validate card num
    if not (card_number.isdigit() and len(card_number) == 16):
        print("\n🚫 Invalid card number. 🚫")
        return
    
    # Validate CVV
    if not (cvv.isdigit() and len(cvv) == 3):
        print("\n🚫 Invalid CVV. 🚫")
        return
    
    # Validate expiry date
    try:
        exp_month, exp_year = expiry.split("/")
        exp_month = int(exp_month)
        exp_year = int(exp_year)

        expiry_date = datetime(exp_year, exp_month, 1)
        if expiry_date <= datetime.now():
            print("\n🚫 Card has expired. 🚫")
            return
    except:
        print("\n🚫 Invalid expiry format. 🚫")
        return

    # Everything is valid, insert the enrollment
    start_ts = datetime.now()
    end_ts = start_ts + timedelta(days=365)

    # Insert enrollment
    cursor.execute("""
        INSERT INTO enrollments (cid, uid, start_ts, end_ts, role) VALUES (?, ?, ?, ?, 'Student')
    """, (cid, user["uid"], start_ts, end_ts))
    
    # Insert payment record
    cursor.execute("""
        INSERT INTO payments (uid, cid, ts, credit_card_no, expiry_date) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
    """, (user["uid"], cid, card_number, expiry))
    
    conn.commit()

    # 12 asterisks and the last 4 digits of the card + timestamp
    cursor.execute("""
        SELECT ts FROM payments WHERE uid = ? AND cid = ? ORDER BY ts DESC LIMIT 1
    """, (user["uid"], cid))
    payment_ts = cursor.fetchone()["ts"]

    masked = "************" + card_number[-4:]

    # Confirmation message
    print("\n✅ Enrollment Successful! ✅\n")
    print("cid:", cid)
    print("title:", course["title"])
    print("price:", course["price"])
    print("payments.ts:", payment_ts)
    print("card:", masked)
    print()
    input("❁›--› Press Enter to return.")

"""
This function will allow a student to view the courses they are
enrolled in, and then present a few actions for them to choose from.

Input: conn, user
Output: list of courses user is enrolled in
"""
def view_enrolled(conn, user):
    cursor = conn.cursor()
    page = 0

    while True:
        # rows to skip based on current page
        offset = page * MAX_ON_PAGE

        # Gett the courses for user
        cursor.execute("""
            SELECT c.cid, c.title, c.category, e.start_ts, c.pass_grade FROM enrollments e
            JOIN courses c ON e.cid = c.cid WHERE e.uid = ? AND e.role = 'Student' AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts
            ORDER BY c.cid LIMIT ? OFFSET ?
        """, (user["uid"], MAX_ON_PAGE, offset))
        rows = cursor.fetchall()

        # No enrollments (for both page 0 and further)
        if not rows:
            if page == 0:
                print("\n╰┈➤ No active enrollments.\n")
                return
            else:
                page -= 1
                continue

        # Print courses
        print()
        center_print(f"----- Active Courses For {user['name']} -----")
        print()
        center_divider()
        for row in rows:
            print()
            center_print(f"cid: {row['cid']}")
            center_print(f"title: {row['title']}")
            center_print(f"category: {row['category']}")
            center_print(f"start_ts: {row['start_ts']}")
            center_print(f"pass_grade: {row['pass_grade']}")
            print()
            center_divider()

        print("\nOptions:\n")
        if page > 0:
            print("P. Prev")
        if len(rows) == MAX_ON_PAGE:
            print("N. Next")
        print("S. Select by cid")
        print("B. Back")

        # User input
        choice = input("\n❁›--› Please choose an option (P/N/S/B): ").lower()

        # Route user input
        if choice == "n" and len(rows) == MAX_ON_PAGE:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "s":
            cid = input("\n❁›--› Enter cid: ")
            valid = 0
            # Only view course submenu for courses that the user is enrolled in.
            for row in rows:
                if int(cid) == int(row['cid']):
                    valid = 1
            if valid:
                course_submenu(conn, user, cid)
            else:
                print("\n🚫 You are not enrolled in that course. 🚫")
        elif choice == "b":
            return
        else:
            print("\n🚫 Invalid choice. 🚫")

"""
This function will show a "submenu" for a single course where the user can choose to:
    1. see modules
    2. see grades
    3. see certs
    4. go back

Input: conn, user, cid
Output: none, routes to other functions to handle specific actions
"""
def course_submenu(conn, user, cid):
    while True:
        print("\nOptions:\n")
        print("1. See all modules")
        print("2. See grades")
        print("3. See certificate")
        print("4. Back")

        choice = input("\n❁›--› Please choose an option (1-4): ")

        if choice == "1":
            view_modules(conn, user, cid)
        elif choice == "2":
            see_grades(conn, user, cid)
        elif choice == "3":
            see_certificate(conn, user, cid)
        elif choice == "4":
            return
        else:
            print("\n🚫 Invalid choice. 🚫")

"""
Helper function to view the modules of a course.

Input: conn, user, cid
Output: mid, name, weight, summary
"""
def view_modules(conn, user, cid):
    cursor = conn.cursor()
    page = 0

    while True:
        # Same as before, rows to skip
        offset = page * MAX_ON_PAGE

        # SQL to get the relevant info
        cursor.execute("""
            SELECT mid, name, weight, summary FROM modules WHERE cid = ? ORDER BY mid LIMIT ? OFFSET ?
        """, (cid, MAX_ON_PAGE, offset))
        rows = cursor.fetchall()

        # No modules
        if not rows:
            print("\n╰┈➤ No modules found.\n")
            return

        # Otherwise, print the info
        center_print()
        center_print(f"----- Modules for course {cid} -----")
        print()
        center_divider()
        for row in rows:
            print()
            center_print(f"mid: {row['mid']}")
            center_print(f"name: {row['name']}")
            center_print(f"weight: {row['weight']}")
            center_print(f"summary: {row['summary']}")
            print()
            center_divider()
        
        # User options once again
        print("\nOptions:\n")
        if page > 0:
            print("P. Prev")
        if len(rows) == MAX_ON_PAGE:
            print("N. Next")
        print("S. Select mid")
        print("B. Back")

        choice = input("\n❁›--› Please choose an option (P/N/S/B): ").lower()

        # Route choice
        if choice == "n" and len(rows) == MAX_ON_PAGE:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "s":
            mid = input("❁›--› Enter mid: ")
            view_lessons(conn, user, cid, mid)
        elif choice == "b":
            return
        else:
            print("\n🚫 Invalid choice. 🚫")

"""
Helper function to see the frades of a course.

Input: conn, user, cid
Output: mid, module_name, weight, grade, received_ts, followed by one grade summary line
"""
def see_grades(conn, user, cid):
    cursor = conn.cursor()

    # Get the grades with other relevant info
    cursor.execute("""
        SELECT g.mid, m.name AS module_name, m.weight, g.grade, g.received_ts FROM grades g
        JOIN modules m ON g.cid = m.cid AND g.mid = m.mid WHERE g.uid = ? AND g.cid = ? ORDER BY g.mid
    """, (user["uid"], cid))
    rows = cursor.fetchall()

    # No grades
    if not rows:
        print("\n🚫 No grades found. 🚫")
        print("\nfinal_grade = N/A")
        return
    
    total_weighted = 0
    total_weight = 0

    # Print hte info while summing weighted grades and weight
    print()
    center_print("Grades:")
    print()
    center_divider()
    for row in rows:
        print()
        center_print(f"mid: {row['mid']}")
        center_print(f"module_name: {row['module_name']}")
        center_print(f"weight: {row['weight']}")
        center_print(f"grade: {row['grade']}")
        center_print(f"received_ts: {row['received_ts']}")
        print()
        center_divider()
        total_weighted += row["grade"] * row["weight"]
        total_weight += row["weight"]
    
    if total_weight > 0:
        final_grade = total_weighted / total_weight
    else:
        final_grade = 0
    
    print()
    center_print(f"final_grade = {round(final_grade, 2)}")
    print()

"""
Helper function to see te certificate of a course.

Input: conn, user, cid
Output: cid, course_title, reveived_ts, final_grade; "No certificate found" if it applies
"""
def see_certificate(conn, user, cid):
    cursor = conn.cursor()

    # Get the cert if it exists (the latest one in the case mutliple exist)
    cursor.execute("""
        SELECT c.cid, co.title AS course_title, c.received_ts, c.final_grade FROM certificates c
        JOIN courses co ON c.cid = co.cid WHERE c.uid = ? AND c.cid = ? ORDER BY c.received_ts DESC LIMIT 1
    """, (user["uid"], cid))
    cert = cursor.fetchone()

    # No cert exists
    if not cert:
        print("\n🚫 No certificate found. 🚫")
        return
    
    # Print info otherwise
    print()
    center_print(f"cid: {cert['cid']}")
    center_print(f"course_title: {cert['course_title']}")
    center_print(f"received_ts: {cert['received_ts']}")
    center_print(f"final_grade: {cert['final_grade']}")
    print()

"""
Helper function to see the lessons of a module.

Input: conn, user, cid, mid
Output: lid, title, duration, comp_status (completed/not completed)
"""
def view_lessons(conn, user, cid, mid):
    cursor = conn.cursor()
    page = 0

    while True:
        # Rows to skip
        offset = page * MAX_ON_PAGE

        # Get the status of the lesson (completed/not completed), saved as comp_status
        cursor.execute("""
            SELECT l.lid, l.title, l.duration, CASE WHEN EXISTS (
                SELECT 1 FROM completion c WHERE c.uid = ? AND c.cid = l.cid AND c.mid = l.mid AND c.lid = l.lid)
            THEN 'Completed' ELSE 'Not Completed' END AS comp_status
            FROM lessons l WHERE l.cid = ? AND l.mid = ? ORDER BY l.lid LIMIT ? OFFSET ?
        """, (user["uid"], cid, mid, MAX_ON_PAGE, offset))
        rows = cursor.fetchall()

        # Case where there are no lessons
        if not rows:
            print("\n╰┈➤ No lessons found.\n")
            return
        
        # Print info otherwise
        print()
        center_print(f"----- Lessons for module {mid} -----")
        print()
        center_divider()
        for row in rows:
            print()
            center_print(f"lid: {row['lid']}")
            center_print(f"title: {row['title']}")
            center_print(f"duration: {row['duration']}")
            center_print(f"status: {row['comp_status']}")
            print()
            center_divider()
        
        # User options once again
        print("\nOptions:\n")
        if page > 0:
            print("P. Prev")
        if len(rows) == MAX_ON_PAGE:
            print("N. Next")
        print("S. Select lid")
        print("B. Back")

        choice = input("\n❁›--› Please choose an option (P/N/S/B): ").lower()

        # Route choice
        if choice == "n" and len(rows) == MAX_ON_PAGE:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "s":
            lid = input("❁›--› Enter lid: ")
            lesson_detail(conn, user, cid, mid, lid)
        elif choice == "b":
            return
        else:
            print("\n🚫 Invalid choice. 🚫")

"""
This helper function allows the user to view the details of a lesson.

Input: conn, user, cid, mid, lid
Output: cid, mid, lid, title, duration, content, status
"""
def lesson_detail(conn, user, cid, mid, lid):
    cursor = conn.cursor()

    # Get lesson
    cursor.execute("""
        SELECT * FROM lessons WHERE cid = ? AND mid = ? AND lid = ?
    """, (cid, mid, lid))
    lesson = cursor.fetchone()

    # Lesson dne
    if not lesson:
        print("\n🚫 Lesson not found. 🚫\n")
        return
    
    # Get completion
    cursor.execute("""
        SELECT 1 FROM completion WHERE uid = ? AND cid = ? AND mid = ? AND lid = ?
    """, (user["uid"], cid, mid, lid))
    completed = cursor.fetchone() is not None
    status = "Completed" if completed else "Not Completed"

    # Print infp:
    print("\nLesson Details:")
    print("cid:", cid)
    print("mid:", mid)
    print("lid:", lid)
    print("title:", lesson["title"])
    print("duration:", lesson["duration"])
    print("content:", lesson["content"])
    print("status:", status)

    if completed:
        print("\n✅ Already completed. ✅")
        return
    
    # Display options
    print("\nOptions:\n")
    print("1. Mark as complete")
    print("2. Back")

    choice = input("\n❁›--› Please choose an option (1/2): ").lower()

    # Route
    if choice == "1":
        # Mark as compelte by inserting a corresponding entry into completion
        cursor.execute("""
            INSERT INTO completion (uid, cid, mid, lid, ts) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (user["uid"], cid, mid, lid))
        conn.commit()
        print("\n✅ Lesson marked as complete! ✅\n")
    elif choice == "2":
        return
    else:
        print("\n🚫 Invalid choice. 🚫")


"""
Helper function to view past payments made.

Input: conn, user
Output: ts, cid, course_title, masked card (with last 4 digits), expiry_date
"""
def past_pay(conn, user):
    cursor = conn.cursor()
    page = 0

    while True:
        # Rows to skip
        offset = page * MAX_ON_PAGE

        # Get the payments
        cursor.execute("""
            SELECT p.ts, p.cid, c.title AS course_title, p.credit_card_no, p.expiry_date
            FROM payments p JOIN courses c ON p.cid = c.cid WHERE p.uid = ? ORDER BY p.ts DESC LIMIT ? OFFSET ?
        """, (user["uid"], MAX_ON_PAGE, offset))
        rows = cursor.fetchall()

        # No prev payments made or we're on the last page
        if not rows:
            if page == 0:
                print("\n╰┈➤ No previous payments have been made.")
                return
            else:
                page -= 1
                continue
        
        # Otherwise, print info for each past payment
        print()
        center_print(f"----- Past Payments For {user['name']} -----")
        print()
        center_divider()
        for row in rows:
            print()
            masked = "************" + row["credit_card_no"][-4:]
            center_print(f"ts: {row['ts']}")
            center_print(f"cid: {row['cid']}")
            center_print(f"course_title: {row['course_title']}")
            center_print(f"card: {masked}")
            center_print(f"expiry_date: {row['expiry_date']}")
            print()
            center_divider()
        
        # Display options
        print("\nOptions:\n")
        if page > 0:
            print("P. Prev")
        if len(rows) == MAX_ON_PAGE:
            print("N. Next")
        print("B. Back")

        choice = input("\n❁›--› Please choose an option (P/N/B): ").lower()

        # Route
        if choice == "n" and len(rows) == MAX_ON_PAGE:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "b":
            return
        else:
            print("\n🚫 Invalid choice. 🚫")