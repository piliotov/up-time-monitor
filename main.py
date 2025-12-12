from datetime import datetime
import sqlite3, json

with open("config.json") as config_file:
    config = json.load(config_file)

url = config["url"]
check_interval = config["interval_sec"]
check_timeout = config["timeout_sec"]
latency = config["max_latency_ms"]

db = sqlite3.connect("uptime_monitor.db")
c = db.cursor()
c.execute("""
          CREATE TABLE IF NOT EXISTS checks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          ts_utc TEXT,
          status_code INTEGER,
          ok_state INTEGER,
          latency_ms INTEGER, 
          error_msg TEXT
          )
          """)
db.commit()