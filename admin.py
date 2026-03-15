# Made by Sarah Mohammed for the 291 mini-project 1 on March 2 2026

# Imports
from utils import center_divider, center_print

def top_5_active(conn):
    cursor = conn.cursor()

    query = """
    WITH active_counts AS (
        SELECT c.cid,
               c.title,
               COUNT(e.uid) AS active_enrollment
        FROM courses c
        LEFT JOIN enrollments e
            ON c.cid = e.cid
           AND e.role = 'Student'
           AND CURRENT_TIMESTAMP BETWEEN e.start_ts AND e.end_ts
        GROUP BY c.cid, c.title
    ),
    ranked AS (
        SELECT *,
               DENSE_RANK() OVER (ORDER BY active_enrollment DESC) AS rnk
        FROM active_counts
    )
    SELECT cid, title, active_enrollment
    FROM ranked
    WHERE rnk <= 5
    ORDER BY active_enrollment DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print()
    center_print("----- Top 5 Courses By Active Enrollment -----")
    print()

    center_divider()
    for row in rows:
        print()
        center_print(f"cid: {row['cid']}")
        center_print(f"title: {row['title']}")
        center_print(f"active_enrollment: {row['active_enrollment']}")
        print()
        center_divider()

    input("\n❁›--› Press Enter to return.")
    return

def payment_counts(conn):
    cursor = conn.cursor()

    query = """
    SELECT c.cid,
           c.title,
           COUNT(p.uid) AS payment_count
    FROM courses c
    LEFT JOIN payments p
        ON c.cid = p.cid
    GROUP BY c.cid, c.title
    ORDER BY payment_count DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    print()
    center_print("----- Payment Counts Per Course -----")
    print()
    center_divider()
    for row in rows:
        print()
        center_print(f"cid: {row['cid']}")
        center_print(f"title: {row['title']}")
        center_print(f"payment_count: {row['payment_count']}")
        print()
        center_divider()

    input("\n❁›--› Press Enter to return.")
    return