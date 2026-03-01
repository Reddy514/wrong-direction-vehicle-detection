import sqlite3
import datetime
from core.config import DB_PATH

def init_db():
    """Initializes the SQLite database schema if not present."""
    conn = sqlite3.connect(DB_PATH)
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
    """Inserts a violation record into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    c.execute('''
        INSERT INTO violations (timestamp, vehicle_class, plate_text, plate_confidence, image_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (timestamp, vehicle_class, plate_text, plate_confidence, image_path))
    conn.commit()
    conn.close()
    return timestamp
