import sqlite3
from datetime import datetime

conn = sqlite3.connect("medicine.db", check_same_thread=False)
c = conn.cursor()

# ── TABLES ──────────────────────────────────────────
c.execute("""
CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    medicine TEXT,
    reminder_time TEXT,
    stock INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    medicine TEXT,
    status TEXT,
    timestamp TEXT
)
""")

conn.commit()

# ── ADD SCHEDULE ────────────────────────────────────
def add_schedule(patient, medicine, reminder_time, stock):

    c.execute("""
    INSERT INTO schedules
    (patient, medicine, reminder_time, stock)
    VALUES (?, ?, ?, ?)
    """, (patient, medicine, reminder_time, stock))

    conn.commit()

# ── GET SCHEDULE ────────────────────────────────────
def get_schedule(patient):

    c.execute("""
    SELECT id, medicine, reminder_time, stock
    FROM schedules
    WHERE patient=?
    """, (patient,))

    return c.fetchall()

# ── ADD LOG ─────────────────────────────────────────
def add_log(patient, medicine, status):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
    INSERT INTO logs
    (patient, medicine, status, timestamp)
    VALUES (?, ?, ?, ?)
    """, (patient, medicine, status, timestamp))

    conn.commit()

# ── GET ALL LOGS ────────────────────────────────────
def get_all_logs(patient):

    c.execute("""
    SELECT id, medicine, status, timestamp
    FROM logs
    WHERE patient=?
    ORDER BY id DESC
    """, (patient,))

    return c.fetchall()

# ── UPDATE STOCK ────────────────────────────────────
def update_stock(patient, medicine):

    c.execute("""
    SELECT id, stock
    FROM schedules
    WHERE patient=? AND medicine=?
    ORDER BY id DESC
    LIMIT 1
    """, (patient, medicine))

    result = c.fetchone()

    if result:

        row_id, stock = result

        if stock > 0:

            new_stock = stock - 1

            c.execute("""
            UPDATE schedules
            SET stock=?
            WHERE id=?
            """, (new_stock, row_id))

            conn.commit()