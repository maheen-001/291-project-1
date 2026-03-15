# More detail of any AI tool used, including the name, URL, all the input given and all the output received.  

-----

1. Used Chatgpt to generate fake course data for testing. The input was:

Could you make me fake data using this schema:

users(uid, name, email, role, pwd), where role ∈ {Student, Instructor, Admin} (i.e., role can be Student, Instructor, or Admin).
courses(cid, title, description, category, price, pass_grade, max_students)
enrollments(cid, uid, start_ts, end_ts, role), where role ∈ {Student, Instructor} (i.e., role can be Student or Instructor).
modules(cid, mid, name, summary, weight)
lessons(cid, mid, lid, title, duration, content)
completion(uid, cid, mid, lid, ts)
grades(uid, cid, mid, received_ts, grade)
certificates(cid, uid, received_ts, final_grade)
payments(uid, cid, ts, credit_card_no, expiry_date)

-----

This is the output:

-- =========================
-- SEED USERS (Instructor)
-- =========================

INSERT INTO users (name, email, role, pwd)
VALUES ('Dr. Smith', 'smith@uni.ca', 'Instructor', 'pass123');

-- =========================
-- SEED COURSES
-- =========================

INSERT INTO courses (title, description, category, price, pass_grade, max_students)
VALUES
('Intro to Databases', 'Learn SQL and relational design', 'CS', 100.0, 50, 30),
('Advanced SQL', 'Deep dive into queries and optimization', 'CS', 120.0, 60, 25),
('Python Programming', 'Python from basics to advanced', 'Programming', 90.0, 55, 40),
('Data Structures', 'Learn lists, trees, graphs', 'CS', 110.0, 50, 35),
('Web Development', 'Frontend and backend basics', 'Programming', 95.0, 50, 30),
('Machine Learning Basics', 'Intro to ML concepts', 'AI', 150.0, 65, 20);

-- =========================
-- ASSIGN INSTRUCTOR TO COURSES
-- =========================

INSERT INTO enrollments (cid, uid, end_ts, role)
SELECT cid, 1, DATETIME('now', '+2 years'), 'Instructor'
FROM courses;

-- =========================
-- SEED MODULES
-- =========================

INSERT INTO modules (cid, mid, name, summary, weight)
VALUES
(1, 1, 'Database Basics', 'Intro concepts', 20),
(1, 2, 'SQL Queries', 'Select, Join, Group By', 30),
(1, 3, 'Normalization', 'Database design theory', 50),

(2, 1, 'Indexes', 'Index optimization', 50),
(2, 2, 'Query Plans', 'Understanding execution plans', 50),

(3, 1, 'Python Basics', 'Syntax and variables', 50),
(3, 2, 'OOP in Python', 'Classes and objects', 50),

(4, 1, 'Arrays & Lists', 'Linear structures', 40),
(4, 2, 'Trees', 'Binary trees & BST', 60),

(5, 1, 'HTML & CSS', 'Frontend basics', 50),
(5, 2, 'Backend APIs', 'Server-side basics', 50),

(6, 1, 'Linear Regression', 'Basic ML model', 50),
(6, 2, 'Classification', 'Logistic regression', 50);

-- =========================
-- SEED LESSONS
-- =========================

INSERT INTO lessons (cid, mid, lid, title, duration, content)
VALUES
(1,1,1,'What is a Database?',20,'Database intro content'),
(1,1,2,'Relational Model',25,'Relational theory content'),
(1,2,1,'SELECT Basics',30,'SELECT examples'),
(1,2,2,'JOIN Operations',35,'JOIN examples'),
(1,3,1,'1NF and 2NF',30,'Normalization rules'),
(1,3,2,'3NF',30,'Advanced normalization'),

(3,1,1,'Variables',20,'Python variables'),
(3,1,2,'Loops',25,'For and while loops'),
(3,2,1,'Classes',30,'OOP basics'),
(3,2,2,'Inheritance',35,'Inheritance examples'),

(6,1,1,'What is ML?',20,'Intro to ML'),
(6,1,2,'Regression Example',25,'Linear regression demo');

This was placed in the database_schema.sql file!

-----
2. Samer thing except for fake course/module/lesson data. This was the output:

INSERT INTO completion (uid, cid, mid, lid)
VALUES
-- Course 1
(1,1,1,1),
(1,1,1,2),
(1,1,2,1),
(1,1,2,2),
(1,1,3,1),
(1,1,3,2),

-- Course 3
(1,3,1,1),
(1,3,1,2),
(1,3,2,1),
(1,3,2,2);

-- =========================
-- SEED GRADES
-- =========================

INSERT INTO grades (uid, cid, mid, grade)
VALUES
-- Course 1
(1,1,1,80),
(1,1,2,70),
(1,1,3,90),

-- Course 3
(1,3,1,75),
(1,3,2,85),

-- Course 6 (partial attempt)
(1,6,1,60);

-- =========================
-- SEED CERTIFICATE
-- =========================

INSERT INTO certificates (cid, uid, final_grade)
VALUES
(1,1,82);

INSERT INTO grades (uid, cid, mid, grade)
VALUES
(1,2,1,40),
(1,2,2,45);