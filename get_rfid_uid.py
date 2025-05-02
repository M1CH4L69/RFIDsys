import time
import pyodbc
from datetime import datetime

def get_connection():
    return pyodbc.connect(
        'DRIVER={FreeTDS};'
        'SERVER=X;'
        'PORT=X;'
        'UID=X;'
        'PWD=X;'
        'DATABASE=X;'
        'TDS_Version=7.4;'
    )

print("Reader ready. Please scan your card...")

while True:
    try:
        uid = input("Reading UID (scan your card): ")
        print(f"UID read: {uid}")

        try:
            uid_int = int(uid)
        except ValueError:
            print(f"UID '{uid}' is not a valid number.")
            continue

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, surname, blocked FROM users WHERE id = ?", (uid_int,))
        user = cursor.fetchone()

        if user:
            user_id, name, surname, blocked = user
            if blocked:
                print(f"User {name} {surname} is blocked.")
            else:
                cursor.execute(
                    "SELECT TOP 1 action FROM logs WHERE user_id = ? ORDER BY timestamp DESC",
                    (user_id,)
                )
                last = cursor.fetchone()
                status = "exit" if last and last[0] == "entry" else "entry"
                now = datetime.now()

                cursor.execute(
                    "INSERT INTO attendance (user_id, status, timestamp) VALUES (?, ?, ?)",
                    (user_id, status, now)
                )

                cursor.execute(
                    "INSERT INTO logs (user_id, action, info, timestamp) VALUES (?, ?, ?, ?)",
                    (user_id, status, f"RFID scan {status}", now)
                )

                conn.commit()
                print(f"{status.upper()} recorded for user {name} {surname}.")

        else:
            print("Unknown UID.")

        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(2)
