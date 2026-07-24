import threading
import time
import urllib.request
import json
import sys
import logging

logging.basicConfig(level=logging.INFO)

def run_app():
    from tradiba.bootstrap import bootstrap
    app = bootstrap()
    app.start()

t = threading.Thread(target=run_app, daemon=True)
t.start()

time.sleep(5)  # Wait for MT5 and FastAPI to initialize
try:
    with urllib.request.urlopen('http://127.0.0.1:8000/health') as response:
        data = json.loads(response.read().decode('utf-8'))
        print("Health check response:", data)
    sys.exit(0)
except Exception as e:
    print("Error querying health endpoint:", e)
    sys.exit(1)
