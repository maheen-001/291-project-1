# CMPUT 291 Project 1 – Course Management System

A command-line course management system built using **Python** and **SQLite**.

## Team Members

* Maheen Abbasi
* Sarah Mohammed
* Manaal Naeem

## Features

### Student

* Register and log in
* Search and filter courses
* View course details
* Enroll in courses
* View enrolled courses
* View modules and lessons
* Mark lessons as completed
* View grades
* View certificates
* View past payments

### Instructor

* Update courses
* Change course price, passing grade, and enrollment limit
* Override enrollment limits
* View course statistics
* Manage certificate eligibility

### Administrator

* View the top 5 courses by active enrollment
* View payment counts by course

## Technologies Used

* Python
* SQLite
* SQL

## Project Structure

```text
main.py          # Program entry point
db.py            # Database connection
auth.py          # Login and registration
menus.py         # Role-based menus
student.py       # Student functionality
instructor.py    # Instructor functionality
admin.py         # Administrator functionality
utils.py         # Helper functions
```

## Running the Program

```bash
python main.py <database_file>
```

Example:

```bash
python main.py test.db
```

## 📚 Additional Resources

* [Stack Overflow – How do I print in the middle of the screen?](https://stackoverflow.com/questions/29780053/how-do-i-print-in-the-middle-of-the-screen)
  Used to help implement centered terminal output for improved table formatting.

  We did not collaborate with anyone outside of the project group.

---

**CMPUT 291 – Winter 2026**
**University of Alberta**
