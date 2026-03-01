import sqlite3
import datetime

def init_db():
    conn = sqlite3.connect('violations.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            vehicle_class TEXT,
            plate_text TEXT,
            plate_confidence REAL,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_violation(vehicle_class, plate_text, plate_confidence, image_path):
    conn = sqlite3.connect('violations.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO violations (timestamp, vehicle_class, plate_text, plate_confidence, image_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, vehicle_class, plate_text, plate_confidence, image_path))
    conn.commit()
    conn.close()
    return timestamp
