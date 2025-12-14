from datetime import datetime, timezone
import time
import sqlite3
import json
import httpx
import schedule

with open("config.json") as config_file:
    config = json.load(config_file)

url = config["url"]
check_interval = config["interval_sec"]
check_timeout = config["timeout_sec"]
latency_max = config["max_latency_ms"]

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


def check_website():
    current_time = datetime.now(timezone.utc).isoformat()
    try:
        time_start = time.time()
        response = httpx.get(url, timeout=check_timeout)
        latency_ms = int((time.time() - time_start) * 1000)
        status_code = response.status_code
        ok = int(200 <= status_code < 400 and latency_ms <= latency_max)
        error_msg = None
    except Exception as e:
        status_code = None
        ok = 0
        latency_ms = None
        error_msg = str(e)
    db.execute("""
        INSERT INTO checks (ts_utc, status_code, ok_state, latency_ms, error_msg)
        VALUES (?, ?, ?, ?, ?)""", (current_time, status_code, ok, latency_ms, error_msg))
    db.commit()
    print("A check has been executed.")



def main():
    schedule.every(check_interval).seconds.do(check_website)
    print(f"Scheduler started. Checking every {check_interval} seconds.")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
