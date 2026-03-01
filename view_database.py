import sqlite3
import pandas as pd

conn = sqlite3.connect("violations.db")
df = pd.read_sql_query("SELECT * FROM violations", conn)
print(df)
conn.close()
