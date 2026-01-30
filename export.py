import sqlite3
import pandas as pd
import os
import sys
import datetime
from attendance import get_gradelevel

def get_db_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "attendance.db")
    return "attendance.db"

def export_excel(grade_level):
    conn = sqlite3.connect(get_db_path())
    table = get_gradelevel(int(grade_level))
    query = f"""
        SELECT student_id,
               student_names,
               time_in,
               time_out,
               status
        FROM {table}
        ORDER BY student_names
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    filename = f"Attendance_{datetime.date.today()}.xlsx"
    df.to_excel(filename, index=False)

    return filename
