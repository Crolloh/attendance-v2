#This is to setup both the DBs of the attendance (add/remove of students from og DB)
import sqlite3
from datetime import datetime
import os
import sys
import shutil

def get_db_path():
    appdata = os.getenv("APPDATA")
    app_folder = os.path.join(appdata, "AttendanceApp")
    
    if not os.path.exists(app_folder):
        os.makedirs(app_folder)
    
    db_path = os.path.join(app_folder, "attendance.db")

    if not os.path.exists(db_path):
        if hasattr(sys, "_MEIPASS"):
           shutil.copy(
               os.path.join(sys._MEIPASS, "attendance.db"),
            db_path
           )
        else:
            shutil.copy("attendance.db", db_path)

    return db_path

def get_connection():
    return sqlite3.connect(get_db_path())

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            student_names TEXT NOT NULL,
            grade_level INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_11 (
            student_id INTEGER PRIMARY KEY,
            student_names TEXT,
            time_in TEXT DEFAULT NULL,
            time_out TEXT DEFAULT NULL,
            status TEXT DEFAULT 'N/A',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_12 (
            student_id INTEGER PRIMARY KEY,
            student_names TEXT,
            time_in TEXT DEFAULT NULL,
            time_out TEXT DEFAULT NULL,
            status TEXT DEFAULT 'N/A',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()

def get_gradelevel(grade_level):
    if grade_level == 11:
        return "attendance_11"
    elif grade_level == 12:
        return "attendance_12"
    else: 
        raise ValueError("Invalid grade level")
    
def add_student(student_id, student_name, grade_level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO students (student_id, student_names, grade_level)
        VALUES (?, ?, ?)
    """, (student_id, student_name, grade_level))

    gradeLevel = get_gradelevel(grade_level)

    cursor.execute(f"""
        INSERT OR IGNORE INTO {gradeLevel} (student_id, student_names)
        VALUES (?, ?)
    """, (student_id, student_name))

    conn.commit()
    conn.close()

def time_in_or_out(student_id, grade_level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_names, grade_level FROM students WHERE student_id = ?",
        (student_id,)
    )
    student = cursor.fetchone()

    if not student:
        conn.close()
        return "Unregistered ID"
    
    name = student[0]
    gradeLevel = student[1]

    if gradeLevel != grade_level:
        conn.close()
        return f"{name} is not in {gradeLevel}"
    
    table = get_gradelevel(grade_level)

    cursor.execute(f"SELECT time_in, time_out FROM {table} where student_id = ?",
        (student_id,)
    )
    recorded = cursor.fetchone()

    if not recorded:
        conn.close()
        return "Student not found in database"
    
    time_in1, time_out1 = recorded

    if not time_in1:
        conn.close()
        return record_attendance(student_id, grade_level)
    elif not time_out1:
        conn.close()
        return time_out(student_id, grade_level)
    else:
        conn.close()
        return "Student already timed in and out"

    conn.commit()
    conn.close()

def time_out(student_id, grade_level):
    conn = get_connection()
    cursor = conn.cursor()

    table = get_gradelevel(grade_level)

    cursor.execute(
    f"SELECT time_out FROM {table} WHERE student_id = ?",
    (student_id,)
    )
    if cursor.fetchone()[0]:
        conn.close()
        return "Already timed out"

    cursor.execute(
        "SELECT student_names, grade_level FROM students WHERE student_id = ?",
        (student_id,)
    )
    student = cursor.fetchone()

    time_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(f"""
        UPDATE {table}
        SET time_out = ?
        WHERE student_id = ?
    """, (time_out, student_id))

    conn.commit()
    conn.close()

    return f"{student[0]} timed out"


def record_attendance(student_id, grade_level):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT student_names, grade_level FROM students WHERE student_id = ?",
        (student_id,)
    )
    student = cursor.fetchone()
    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table = get_gradelevel(grade_level)

    cursor.execute(f"""
        UPDATE {table}
        SET time_in = ?, status = ?
        WHERE student_id = ?
    """, (time_in, "Present", student_id))

    conn.commit()
    conn.close()

    return f"{student[0]} marked present"

def remove_student(student_id, grade_level):
    conn = get_connection()
    cursor = conn.cursor()
    #DELETE FROM ATTENDANCE
    table = get_gradelevel(grade_level)
    cursor.execute(f"DELETE FROM {table} WHERE student_id = ?", 
    (student_id,)
    )
    #DELETE FROM STUDENTS
    cursor.execute("DELETE FROM students WHERE student_id = ?", 
    (student_id,)
    )

    conn.commit()
    conn.close()
    
def clear_attendance(grade_level):
    conn = get_connection()
    cursor = conn.cursor()
    
    table = get_gradelevel(grade_level)
    cursor.execute(f"""
        UPDATE {table}
        SET time_in = NULL, time_out = NULL , status = NULL
    """)

    conn.commit()
    conn.close()
