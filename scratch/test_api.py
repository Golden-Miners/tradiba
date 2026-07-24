import urllib.request
import json
import time
from threading import Thread
import uvicorn
from tradiba.api.app import app

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

def test_api():
    t = Thread(target=run_server, daemon=True)
    t.start()
    
    time.sleep(2)  # Wait for server to boot
    
    req = urllib.request.Request("http://127.0.0.1:8000/health")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        print(f"Health Response: {json.loads(response.read().decode())}")
        
    req = urllib.request.Request("http://127.0.0.1:8000/trades")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        print(f"Trades Response: {json.loads(response.read().decode())}")
        
    print("API is working correctly!")

if __name__ == "__main__":
    test_api()
