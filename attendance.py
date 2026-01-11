#This is to setup both the DBs of the attendance (add/remove of students from og DB)
import sqlite3
from datetime import datetime


def get_connection():
    return sqlite3.connect('attendance.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            student_names TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            student_id INTEGER PRIMARY KEY,
            student_names TEXT,
            time_in TEXT DEFAULT NULL,
            status TEXT DEFAULT 'N/A',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()

def add_student(student_id, student_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO students (student_id, student_names)
        VALUES (?, ?)
    """, (student_id, student_name))

    cursor.execute("""
        INSERT OR IGNORE INTO attendance (student_id, student_names)
        VALUES (?, ?)
    """, (student_id, student_name))

    conn.commit()
    conn.close()

def record_attendance(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_names FROM students WHERE student_id = ?",
        (student_id,)
    )
    student = cursor.fetchone()

    if not student:
        conn.close()
        return "Unregistered ID"

    cursor.execute(
        "SELECT time_in FROM attendance WHERE student_id = ?",
        (student_id,)
    )
    already_present = cursor.fetchone()

    if already_present and already_present[0]:
        conn.close()
        return f"{student[0]} already timed in"

    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        UPDATE attendance
        SET time_in = ?, status = ?
        WHERE student_id = ?
    """, (time_in, "Present", student_id))

    conn.commit()
    conn.close()

    return f"{student[0]} marked present"

def remove_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    #DELETE FROM ATTENDANCE
    cursor.execute("DELETE FROM attendance WHERE student_id = ?", 
    (student_id,)
    )
    #DELETE FROM STUDENTS
    cursor.execute("DELETE FROM students WHERE student_id = ?", 
    (student_id,)
    )

    conn.commit()
    conn.close()
    
def clear_attendance():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE attendance
        SET time_in = NULL , status = NULL
    """)

    conn.commit()
    conn.close()
