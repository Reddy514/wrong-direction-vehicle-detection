import sqlite3
from datetime import datetime
import os

DB_NAME = "violations.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_id INTEGER UNIQUE,
            vehicle_class TEXT,
            plate_number TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def insert_violation(track_id, vehicle_class, plate_number, confidence):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO violations (track_id, vehicle_class, plate_number, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            track_id,
            vehicle_class,
            plate_number,
            confidence,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        # Ignore duplicate track ids due to the UNIQUE constraint
        pass
