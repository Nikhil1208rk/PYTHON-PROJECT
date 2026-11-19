
import sqlite3

DB_NAME = "student_records.db"


# Create database table
def create_table():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            enrollment TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            python REAL,
            web REAL,
            dsa REAL,
            calculus REAL,
            attendance REAL,
            study_hours REAL,
            sleep_hours REAL
        )
    """)

    conn.commit()
    conn.close()


# Save or update student
def save_student(data):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(enrollment) DO UPDATE SET
            name = excluded.name,
            python = excluded.python,
            web = excluded.web,
            dsa = excluded.dsa,
            calculus = excluded.calculus,
            attendance = excluded.attendance,
            study_hours = excluded.study_hours,
            sleep_hours = excluded.sleep_hours
    """, (
        data["enrollment"],
        data["name"],
        data["Python"],
        data["Web Development"],
        data["DSA"],
        data["Calculus"],
        data["attendance"],
        data["study_hours"],
        data["sleep_hours"]
    ))

    conn.commit()
    conn.close()


# Search student
def search_student(enrollment):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE enrollment = ?",
        (enrollment,)
    )

    student = cursor.fetchone()

    conn.close()

    return student


# Delete student
def delete_student(enrollment):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE enrollment = ?",
        (enrollment,)
    )

    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return deleted


# Get all students
def get_all_students():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    conn.close()

    return students


# Create table automatically
create_table()
