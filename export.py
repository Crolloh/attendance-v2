import sqlite3
import pandas as pd
import os
import sys
import datetime
from attendance import get_gradelevel, get_db_path
from openpyxl.utils import get_column_letter

def export_excel(grade_level, subject):
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
    home = os.path.expanduser("~")
    where_doc = os.path.join(home, "Documents")
    app_folder = os.path.join(where_doc, "Attendance Exports")
    os.makedirs(app_folder, exist_ok=True)
    subfolders_bydate = os.path.join(app_folder, f"{datetime.date.today()}")
    os.makedirs(subfolders_bydate, exist_ok=True)
    filename = f"Attendance_{datetime.date.today()} {subject} grade{grade_level}.xlsx"
    full_path = os.path.join(subfolders_bydate, filename)

    with pd.ExcelWriter(full_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']

        for i, col in enumerate(df.columns, 1):
            max_length = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.column_dimensions[get_column_letter(i)].width = max_length

    os.startfile(subfolders_bydate)

    return full_path
