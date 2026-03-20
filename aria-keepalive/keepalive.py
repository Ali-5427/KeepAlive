import requests
import time
import os
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

KAGGLE_URL = os.environ.get("KAGGLE_URL", "https://caused-manhattan-notifications-souls.trycloudflare.com")
MODEL_NAME = os.environ.get("MODEL_NAME", "qwen2.5:7b")

headers = {
    "Content-Type": "application/json",
    "User-Agent": "curl/7.68.0"
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "alive"}).encode())

    def log_message(self, format, *args):
        pass

def start_pinger():
    print(f"Pinging {KAGGLE_URL} every 30 seconds...")
    while True:
        try:
            r = requests.post(
                f"{KAGGLE_URL}/api/chat",
                json={
                    "model": MODEL_NAME,
                    "messages": [{"role": "user", "content": "hi"}],
                    "stream": False
                },
                headers=headers,
                timeout=25
            )
            print(f"✅ {time.strftime('%H:%M:%S')} — Status: {r.status_code}")
        except Exception as e:
            print(f"❌ {time.strftime('%H:%M:%S')} — Error: {str(e)[:100]}")
        time.sleep(30)

threading.Thread(target=start_pinger, daemon=True).start()

port = int(os.environ.get("PORT", 8080))
server = HTTPServer(("0.0.0.0", port), handler)
print(f"Web server running on port {port}")
server.serve_forever()
