# Made by Manaal Naeem for the 291 mini-project 1 on March 2 2026
# Updated Sarah Mohammed for the 291 mini-project 1 on March 4 2026


from datetime import datetime

"""
Functionalities of Instructor - can only preform actions on courses they teach
"""
def update_certificates(conn, user, cid, new_pass_grade):
    """
    
    """
    cursor = conn.cursor()

    certificates_added = 0
    certificates_removed = 0

    cursor.execute("""
        SELECT uid
        FROM enrollments
        WHERE cid = ?
          AND role = 'Student'
          AND CURRENT_TIMESTAMP BETWEEN start_ts AND end_ts
    """, (cid,))
    students = cursor.fetchall() #get all active students

    cursor.execute("""
        SELECT COUNT(*) 
        FROM lessons
        WHERE cid = ?
    """, (cid,))
    total_lessons = cursor.fetchone()[0] #total number of lessons in course

    for s in students:
        uid = s["uid"]
        cursor.execute("""
            SELECT COUNT(*)
            FROM completion
            WHERE uid = ?
              AND cid = ?
        """, (uid, cid))
        completed_lessons = cursor.fetchone()[0] #check completed lessons count

        completed_all = (completed_lessons == total_lessons)

        cursor.execute("""
            SELECT g.mid, g.grade, m.weight
            FROM grades g
            JOIN modules m
              ON g.cid = m.cid AND g.mid = m.mid
            WHERE g.uid = ?
              AND g.cid = ?
        """, (uid, cid))
        grades = cursor.fetchall() #weighted final grade

        total_weighted = 0
        total_weight = 0

        for row in grades:
            total_weighted += row["grade"] * row["weight"]
            total_weight += row["weight"]

        final_grade = (total_weighted / total_weight) if total_weight > 0 else 0

        qualifies = completed_all and final_grade >= new_pass_grade

        cursor.execute("""
            SELECT 1 FROM certificates
            WHERE cid = ? AND uid = ?
        """, (cid, uid))
        cert_exists = cursor.fetchone() is not None  #check if certificate exists

        #insert certificate if qualifies and none exists
        if qualifies and not cert_exists:
            cursor.execute("""
                INSERT INTO certificates (cid, uid, received_ts, final_grade)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?)
            """, (cid, uid, final_grade))
            certificates_added += 1

        #delete certificate if doest qyalify
        if not qualifies and cert_exists:
            cursor.execute("""
                DELETE FROM certificates
                WHERE cid = ? AND uid = ?
            """, (cid, uid))
            certificates_removed += 1

    conn.commit()

    cursor.execute("""
        SELECT cid, price, pass_grade, max_students
        FROM courses
        WHERE cid = ?
    """, (cid,))
    course = cursor.fetchone()

    print("\nCourse Update Summary:\n")
    print("cid:", course["cid"])
    print("price:", course["price"])
    print("pass_grade:", course["pass_grade"])
    print("max_students:", course["max_students"])
    print("certificates_added:", certificates_added)
    print("certificates_removed:", certificates_removed)
    print()
    

def update_course(conn, user):
    cursor = conn.cursor()

    view_courses_q = """
        SELECT
            c.cid,
            c.title,
            c.category,
            c.price,
            c.pass_grade,
            c.max_students,
            (   SELECT COUNT(*)
                FROM enrollments e2
                WHERE e2.cid = c.cid
                  AND e2.role = 'Student'
                  AND CURRENT_TIMESTAMP BETWEEN e2.start_ts AND e2.end_ts) AS current_enrollment
        FROM courses c
        JOIN enrollments e
          ON e.cid = c.cid
        WHERE e.role = 'Instructor'
          AND e.uid = ?
        ORDER BY c.cid
    """
    cursor.execute(view_courses_q, (user["uid"],))
    courses = cursor.fetchall()

    if not courses:
        print("\n╰┈➤ No courses found")
        return

    print("\ncid | title | category | price | pass_grade | max_students | current_enrollment")
    print("-" * 80)
    for c in courses:
        print(f"{c['cid']} | {c['title']} | {c['category']} | {c['price']} | "
              f"{c['pass_grade']} | {c['max_students']} | {c['current_enrollment']}")

    in_cid = input("\n❁›--› Please enter the course id to update (Enter to cancel): ").strip()
    if in_cid == "":
        return
        
    cid = int(in_cid)

    # Check instructor teaches THIS course + fetch current values
    cursor.execute("""
        SELECT c.cid, c.price, c.pass_grade, c.max_students
        FROM courses c
        JOIN enrollments e ON 
        e.cid = c.cid
        WHERE e.role = 'Instructor'
          AND e.uid = ?
          AND c.cid = ?
    """, (user["uid"], cid))
    course = cursor.fetchone()

    if not course:
        print("\n🚫 You may only update a course you teach. 🚫")
        return

    new_price = input(f"New price (current {course['price']}) [Enter to keep]: ").strip()
    new_pass  = input(f"New pass_grade (current {course['pass_grade']}) [Enter to keep]: ").strip()
    new_max   = input(f"New max_students (current {course['max_students']}) [Enter to keep]: ").strip()

    price_val = course["price"] if new_price == "" else float(new_price)
    pass_val  = course["pass_grade"] if new_pass == "" else float(new_pass)
    max_val   = course["max_students"] if new_max == "" else int(new_max)

    cursor.execute("""
        UPDATE courses
        SET price = ?, pass_grade = ?, max_students = ?
        WHERE cid = ?
    """, (price_val, pass_val, max_val, cid))
    conn.commit()

    if price_val:
        update_certificates(conn, user, cid, pass_val)

    print("\n✅ Course successfully updated. ✅\n")

def add_student(conn, user):
    """
    Instructor override enrollment and can 
    add students even if the course is full
    """
    cursor = conn.cursor()

    cursor.execute("""
        SELECT c.cid, c.title
        FROM courses c
        JOIN enrollments e
          ON e.cid = c.cid
        WHERE e.uid = ?
          AND e.role = 'Instructor'
        ORDER BY c.cid
    """, (user["uid"],))
    courses = cursor.fetchall()     #show courses

    if not courses:
        print("\nNo courses found.")
        return

    print("\nCourses you teach:")
    for c in courses:
        print(f"{c['cid']} | {c['title']}")

    in_cid = input("\n❁›--› Enter course id (Enter to cancel): ").strip()
    if in_cid == "":
        return

    cid = int(in_cid)


    cursor.execute("""
        SELECT c.cid, c.title
        FROM courses c
        JOIN enrollments e
          ON e.cid = c.cid
        WHERE e.uid = ?
          AND e.role = 'Instructor'
          AND c.cid = ?
    """, (user["uid"], cid))
    course = cursor.fetchone()  #verify instructor teaches course

    if not course:
        print("\n🚫 You may only add students to courses you teach. 🚫")
        return

    uid = input("Enter student uid: ").strip()


    cursor.execute("""
        SELECT uid, name
        FROM users
        WHERE uid = ?
          AND role = 'Student'
    """, (uid,))
    student = cursor.fetchone()     #verify user exists and is student
    if not student:
        print("\n🚫 User does not exist or is not a Student. 🚫")
        return


    cursor.execute("""
        SELECT 1
        FROM enrollments
        WHERE cid = ?
          AND uid = ?
          AND role = 'Student'
          AND CURRENT_TIMESTAMP BETWEEN start_ts AND end_ts
    """, (cid, uid))
    exists = cursor.fetchone()    #check if already actively enrolled

    if exists:
        print("\n🚫 Student already actively enrolled in this course. 🚫")
        return

    #insert enrollment
    cursor.execute("""
        INSERT INTO enrollments (cid, uid, role, start_ts, end_ts)
        VALUES (?, ?, 'Student', CURRENT_TIMESTAMP, '9999-12-31')
    """, (cid, uid))
    start_ts = datetime.now()


    cursor.execute("""
        INSERT INTO payments (cid, uid, credit_card_no, expiry_date, ts)
        VALUES (?, ?, '0000000000000000', '12/2026', CURRENT_TIMESTAMP)
    """, (cid, uid))
    conn.commit()  #insert payment
    

    print("\n✅ Override Enrollment Successful ✅\n")
    print("cid:", cid)
    print("course_title:", course["title"])
    print("uid:", student["uid"])
    print("student_name:", student["name"])
    print("start_ts:", start_ts)
    print()

def view_course_stats(conn, user):
    """
    View all courses taught by the logged-in instructor, including:
    cid, title, active_enrollment, completion_rate, average_final_grade
    """
    cursor = conn.cursor()

    view_course_query = """
    WITH instructor_courses AS (
        SELECT c.cid, c.title
        FROM courses c
        JOIN enrollments e ON e.cid = c.cid
        WHERE e.uid = ?
          AND e.role = 'Instructor'
    ),

    active_students AS (
        SELECT e.cid, e.uid
        FROM enrollments e
        WHERE e.role = 'Student'
          AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts
    ),

    active_counts AS (
        SELECT cid, COUNT(*) AS active_enrollment
        FROM active_students
        GROUP BY cid
    ),

    lesson_counts AS (
        SELECT cid, COUNT(*) AS total_lessons
        FROM lessons
        GROUP BY cid
    ),

    student_completion AS (
        SELECT
            a.cid,
            a.uid,
            COUNT(DISTINCT comp.mid || '-' || comp.lid) AS completed_lessons
        FROM active_students a
        LEFT JOIN completion comp
          ON comp.cid = a.cid
         AND comp.uid = a.uid
        GROUP BY a.cid, a.uid
    ),

    completed_counts AS (
        SELECT
            sc.cid,
            COUNT(*) AS completed_students
        FROM student_completion sc
        JOIN lesson_counts lc
          ON lc.cid = sc.cid
        WHERE sc.completed_lessons = lc.total_lessons
        GROUP BY sc.cid
    ),

    student_final_grades AS (
        SELECT
            e.cid,
            e.uid,
            SUM(g.grade * m.weight) * 1.0 / SUM(m.weight) AS final_grade
        FROM enrollments e
        JOIN grades g
          ON g.uid = e.uid
         AND g.cid = e.cid
        JOIN modules m
          ON m.cid = g.cid
         AND m.mid = g.mid
        WHERE e.role = 'Student'
          AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts
        GROUP BY e.cid, e.uid
    ),

    grade_averages AS (
        SELECT
            cid,
            ROUND(AVG(final_grade), 2) AS average_final_grade
        FROM student_final_grades
        GROUP BY cid
    )
    -- select final columns for output
    -- cid title, active enrolled students, compeletion rate, average final grade
    SELECT
        ic.cid,
        ic.title,
        COALESCE(ac.active_enrollment, 0) AS active_enrollment,
        COALESCE(cc.completed_students, 0) AS completed_students,
        CASE
            WHEN COALESCE(ac.active_enrollment, 0) = 0 THEN 0
            ELSE ROUND(100.0 * COALESCE(cc.completed_students, 0) / ac.active_enrollment, 2)
        END AS completion_rate,
        ga.average_final_grade
    FROM instructor_courses ic
    LEFT JOIN active_counts ac
      ON ac.cid = ic.cid
    LEFT JOIN completed_counts cc
      ON cc.cid = ic.cid
    LEFT JOIN grade_averages ga
      ON ga.cid = ic.cid
    ORDER BY ic.cid
    """

    cursor.execute(view_course_query, (user["uid"],))
    rows = cursor.fetchall()

    if not rows:
        print("\nNo courses found")
        return

    print("\ncid | title | active_enrollment | completion_rate | average_final_grade")
    print("-" * 80)
    for row in rows:
        avg_grade = row["average_final_grade"] if row["average_final_grade"] is not None else "N/A"
        print(f"{row['cid']} | {row['title']} | {row['active_enrollment']} | "
              f"{row['completion_rate']}% | {avg_grade}")
    print()