import sqlite3
import pandas as pd

def export_excel():
    conn = sqlite3.connect("attendance.db")
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    df.to_excel("attendance.xlsx", index=False)
    conn.close()
    print("Exported to attendance.xlsx")
