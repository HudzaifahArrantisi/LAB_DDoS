# monitor_realtime.py
import matplotlib.pyplot as plt
import requests
import time
from collections import deque
from threading import Thread
import numpy as np

# Konfigurasi
TARGET_URL = "http://localhost:5000/request_counts"
UPDATE_INTERVAL = 0.5  # Pembaruan data setiap 0.5 detik
MAX_DATA_POINTS = 60  # Jumlah maksimal titik data di grafik

# Persiapan data
timestamps = deque(maxlen=MAX_DATA_POINTS)
request_rates = deque(maxlen=MAX_DATA_POINTS)
is_running = True

# Inisialisasi plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')
ax.set_xlabel('Waktu (detik)')
ax.set_ylabel('Requests/s')
ax.set_title('REALTIME DDoS Traffic Monitor')
ax.grid(True)

def fetch_data():
    while is_running:
        try:
            response = requests.get(TARGET_URL, timeout=1)
            count = response.json().get('count', 0)
            
            # Update data
            timestamps.append(time.time())
            request_rates.append(count)
            
            # Normalisasi timestamp
            normalized_ts = np.array(timestamps) - timestamps[0]
            
            # Update plot
            line.set_xdata(normalized_ts)
            line.set_ydata(request_rates)
            ax.relim()
            ax.autoscale_view()
            fig.canvas.draw()
            fig.canvas.flush_events()
            
            print(f"Requests/s: {count}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(UPDATE_INTERVAL)

if __name__ == '__main__':
    try:
        print("[+] Memulai real-time monitoring...")
        Thread(target=fetch_data, daemon=True).start()
        
        # Pertahankan window plot tetap terbuka
        while plt.fignum_exists(fig.number):
            plt.pause(1)
            
    except KeyboardInterrupt:
        is_running = False
        print("\n[+] Monitoring dihentikan")
