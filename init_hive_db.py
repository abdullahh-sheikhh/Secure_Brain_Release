import sqlite3
import os

DB_PATH = "genesis_hive.db"

def init_db():
    print("[Database] Initializing Genesis Hive SQLite Database...")
    
    # Connect to SQLite (this automatically creates the file if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create Users Table (Bio-Profiles)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            baseline_heart_rate INTEGER,
            preferred_pemf_level INTEGER,
            general_health_goals TEXT
        )
    """)
    print("[Database] Verified 'users' table schema.")

    # 2. Create Conversations Table (Infinite Memory)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    """)
    print("[Database] Verified 'conversations' table schema.")

    # 3. Insert a Mock User for Testing
    mock_id = "9482"
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (mock_id,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (user_id, first_name, baseline_heart_rate, preferred_pemf_level, general_health_goals)
            VALUES (?, ?, ?, ?, ?)
        """, (mock_id, "John", 65, 3, "Recovering from knee surgery and dealing with high stress."))
        print(f"[Database] Mock User '{mock_id}' (John) successfully injected into local memory.")
    else:
        print(f"[Database] Mock User '{mock_id}' already exists.")

    # 4. Insert an alternative User to test the "Switch"
    sarah_id = "1122"
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (sarah_id,))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO users (user_id, first_name, baseline_heart_rate, preferred_pemf_level, general_health_goals)
            VALUES (?, ?, ?, ?, ?)
        """, (sarah_id, "Sarah", 58, 5, "Athletic optimization, marathon training, requires deep muscle relaxation."))
        print(f"[Database] Mock User '{sarah_id}' (Sarah) successfully injected into local memory.")

    conn.commit()
    conn.close()
    print("[Database] Initialization complete. Storage ready.")

if __name__ == "__main__":
    init_db()
