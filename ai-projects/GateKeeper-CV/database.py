import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'gatekeeper.db')

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table 1: vehicles (Whitelist/Blacklist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            plate_id TEXT PRIMARY KEY,
            owner_name TEXT,
            access_level TEXT -- 'RESIDENT', 'VISITOR', 'BANNED'
        )
    ''')

    # Table 2: entry_logs (The Audit Trail)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entry_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_id TEXT,
            timestamp DATETIME,
            confidence_score FLOAT,
            image_path TEXT,
            FOREIGN KEY (plate_id) REFERENCES vehicles(plate_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_vehicle(plate_id, owner_name, access_level):
    """Adds or updates a vehicle in the registry."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO vehicles (plate_id, owner_name, access_level)
        VALUES (?, ?, ?)
    ''', (plate_id.upper(), owner_name, access_level))
    conn.commit()
    conn.close()

def get_vehicle_status(plate_id):
    """Checks the status of a vehicle."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT owner_name, access_level FROM vehicles WHERE plate_id = ?', (plate_id.upper(),))
    result = cursor.fetchone()
    conn.close()
    return result if result else (None, 'UNKNOWN')

def log_entry(plate_id, confidence, image_path):
    """Logs a vehicle detection entry."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO entry_logs (plate_id, timestamp, confidence_score, image_path)
        VALUES (?, ?, ?, ?)
    ''', (plate_id.upper(), timestamp, confidence, image_path))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    # Add some dummy data for testing
    add_vehicle("GR-550-22", "John Doe", "RESIDENT")
    add_vehicle("GW-123-23", "Jane Smith", "VISITOR")
    add_vehicle("AS-999-21", "Malicious Actor", "BANNED")
    print("Database initialized and dummy data added.")
