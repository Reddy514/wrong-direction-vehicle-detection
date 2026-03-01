import sqlite3
from core.config import DB_PATH

def view_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM violations")
        rows = cursor.fetchall()
        
        if not rows:
            print("No violations recorded in the database yet.")
            return

        # Print Header
        print("-" * 120)
        print(f"{'ID':<4} | {'Timestamp':<25} | {'Class':<10} | {'Plate':<15} | {'Conf':<6} | {'Image Path'}")
        print("-" * 120)

        # Print Rows
        for row in rows:
            v_id, ts, v_class, plate, conf, img = row
            # Format timestamp for better readability if it's ISO
            ts_short = ts.split(".")[0].replace("T", " ")
            print(f"{v_id:<4} | {ts_short:<25} | {v_class:<10} | {plate:<15} | {conf:<6.2f} | {img}")
            
    except sqlite3.OperationalError as e:
        print(f"Error: {e}. (Does the database exist yet? Run main.py first to create it.)")
    finally:
        conn.close()

if __name__ == "__main__":
    view_data()
