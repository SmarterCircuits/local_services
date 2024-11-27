from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "/srv/checkin.db"  # Update path as needed

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS key_value_store (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """)
        conn.commit()

if not os.path.exists(DB_PATH):
    init_db()

@app.route('/checkin', methods=['POST'])
def checkin():
    data = request.json
    device = data.get('device')
    if not device:
        return jsonify({"error": "Device identifier is required"}), 400

    timestamp = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO checkins (device, timestamp) VALUES (?, ?)", (device, timestamp))
        conn.commit()
    
    return jsonify({"message": "Check-in recorded", "device": device, "timestamp": timestamp})

@app.route('/keyvalue', methods=['POST'])
def set_key_value():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if not key or not value:
        return jsonify({"error": "Both key and value are required"}), 400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO key_value_store (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value=excluded.value
        """, (key, value))
        conn.commit()
    
    return jsonify({"message": "Key-value pair saved", "key": key, "value": value})

@app.route('/keyvalue/<key>', methods=['GET'])
def get_key_value(key):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM key_value_store WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            return jsonify({"key": key, "value": row[0]})
        else:
            return jsonify({"error": "Key not found"}), 404

@app.route('/checkins', methods=['GET'])
def get_checkins():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, device, timestamp FROM checkins ORDER BY timestamp DESC")
        checkins = [{"id": row[0], "device": row[1], "timestamp": row[2]} for row in cursor.fetchall()]
    
    return jsonify(checkins)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
