import os
import sys
import time
import threading
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

SCRIPTS = ["data.py","indicators.py", "strategy.py","notifier.py"]


def run_script(script_name):
    """Jalankan skrip sebagai subprocess dan restart otomatis jika berhenti/crash."""
    while True:
        print(f"[Launcher] Menjalankan {script_name}...", flush=True)
        try:
            # sys.executable = pakai Python yang sama; -u = log langsung tampil di Render
            result = subprocess.run([sys.executable, "-u", script_name])
            print(f"[Launcher] {script_name} berhenti (kode {result.returncode}). "
                  f"Restart dalam 10 detik...", flush=True)
        except Exception as e:
            print(f"[Error] {script_name}: {e}. Restart dalam 10 detik...", flush=True)
        time.sleep(10)


class HealthHandler(BaseHTTPRequestHandler):
    """Server mini agar Render (Web Service gratis) mendeteksi port terbuka."""

    def _ok(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def do_GET(self):
        self._ok()
        self.wfile.write(b"Synapse-Trader-Bot is running")

    def do_HEAD(self):
        self._ok()

    def log_message(self, *args):
        pass  # jangan menuh-menuhin log


if __name__ == "__main__":
    print("=== Memulai Synapse-Trader-Bot Launcher ===", flush=True)

    for script in SCRIPTS:
        threading.Thread(target=run_script, args=(script,), daemon=True).start()

    port = int(os.environ.get("PORT", 10000))
    print(f"[Launcher] Health server di port {port}", flush=True)
    HTTPServer(("0.0.0.0", port), HealthHandler).serve_forever()