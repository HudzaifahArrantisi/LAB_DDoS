from flask import Flask, jsonify
import threading
import time
from collections import deque

app = Flask(__name__)
request_counts = deque(maxlen=10)  # Menyimpan 10 data terakhir
lock = threading.Lock()  # Thread-safe

def monitor_traffic():
    while True:
        with lock:
            current_count = sum(request_counts)
        print(f"Requests/s: {current_count}")
        time.sleep(1)

@app.route('/')
def home():
    with lock:
        request_counts.append(1)  # Catat request
    return "Server OK"

@app.route('/request_counts')
def get_counts():
    with lock:
        return jsonify({"count": sum(request_counts)})

if __name__ == '__main__':
    threading.Thread(target=monitor_traffic, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, threaded=True)
