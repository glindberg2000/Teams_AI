import os
import sys
import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "test_runner.log")


def log_message(message):
    timestamp = datetime.datetime.now().isoformat()
    full_message = f"{timestamp} - {message}\n"
    print(full_message, flush=True)  # Keep printing to stdout as well, just in case
    with open(LOG_FILE, "a") as f:
        f.write(full_message)


log_message("--- test_runner.py starting ---")
log_message(f"CWD: {os.getcwd()}")
log_message(f"Python Executable: {sys.executable}")
log_message(f"Python Version: {sys.version}")
log_message(f"Script Args: {sys.argv}")
log_message(f"Attempting to write to log file: {LOG_FILE}")
log_message("--- test_runner.py finished ---")
