#!/usr/bin/env python3
import zmq
import json
import sqlite3
import os
import time
from datetime import datetime

ROOT = "/app"
DB_FILE = os.path.join(ROOT, "db.sqlite3")
os.makedirs(ROOT, exist_ok=True)

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        timestamp TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        timestamp TEXT
    )
    """)
    conn.commit()
    return conn

conn = init_db()
cur = conn.cursor()

# ZeroMQ REP
ctx = zmq.Context()
sock = ctx.socket(zmq.REP)
sock.bind("tcp://0.0.0.0:5555")
print("🟢 Server listening on tcp://0.0.0.0:5555")

def send_reply(socket, reply_obj):
    socket.send_string(json.dumps(reply_obj))

while True:
    try:
        raw = sock.recv()
        try:
            msg = json.loads(raw.decode())
        except Exception:
            send_reply(sock, {"service":"error","data":{"status":"erro","timestamp":now_iso(),"description":"invalid json"}})
            continue

        service = msg.get("service")
        data = msg.get("data", {})
        ts = now_iso()

        if service == "login":
            username = data.get("user")
            if not username:
                send_reply(sock, {"service":"login","data":{"status":"erro","timestamp":ts,"description":"missing user"}})
                continue
            try:
                cur.execute("INSERT INTO users (username, timestamp) VALUES (?, ?)", (username, ts))
                conn.commit()
                send_reply(sock, {"service":"login","data":{"status":"sucesso","timestamp":ts}})
            except sqlite3.IntegrityError:
                send_reply(sock, {"service":"login","data":{"status":"erro","timestamp":ts,"description":"Usuário já existe"}})

        elif service == "users":
            cur.execute("SELECT username FROM users")
            users = [r[0] for r in cur.fetchall()]
            send_reply(sock, {"service":"users","data":{"timestamp":ts,"users":users}})

        elif service == "channel":
            channel = data.get("channel")
            if not channel:
                send_reply(sock, {"service":"channel","data":{"status":"erro","timestamp":ts,"description":"missing channel"}})
                continue
            try:
                cur.execute("INSERT INTO channels (name, timestamp) VALUES (?, ?)", (channel, ts))
                conn.commit()
                send_reply(sock, {"service":"channel","data":{"status":"sucesso","timestamp":ts}})
            except sqlite3.IntegrityError:
                send_reply(sock, {"service":"channel","data":{"status":"erro","timestamp":ts,"description":"Canal já existe"}})

        elif service == "channels":
            cur.execute("SELECT name FROM channels")
            channels = [r[0] for r in cur.fetchall()]
            send_reply(sock, {"service":"channels","data":{"timestamp":ts,"channels":channels}})

        else:
            send_reply(sock, {"service":service,"data":{"status":"erro","timestamp":ts,"description":"unknown service"}})

    except KeyboardInterrupt:
        print("Shutting down server")
        break
    except Exception as e:
        print("Server error:", e)
        # keep running

# close DB on exit
conn.close()
