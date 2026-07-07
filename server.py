#!/usr/bin/env python3
"""
Tiny offline server for the BPI Grocery Challenge tool.

Usage:
    python server.py

Then:
  - CONTROL (this laptop): opens automatically at http://localhost:8000/
    This is where the operator adds items, sets the budget, and hits Calculate.
  - VIEW (the big screen / projector / 2nd monitor): click "Open View Screen"
    in the control page, then drag that window onto the external display and
    press F11 for full screen.

Why a server instead of double-clicking the HTML files?
Browsers share localStorage only between pages on the same "origin"
(scheme + host + port). Serving both pages from http://localhost:8000 lets the
Control page write a value and the View page read it instantly — no internet,
no database, no polling. Opening the files directly via file:// does NOT
reliably share storage, which is why we serve them.

Requires Python 3.7+ (uses the `directory` argument). No external packages.
"""
import http.server
import socketserver
import os
import threading
import webbrowser

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Never cache: staff edit itemlist.txt between rounds and expect a plain
        # refresh to pick up the change.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass  # keep the console output quiet


def main():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        control_url = f"http://localhost:{PORT}/"
        print("\n  BPI Grocery Challenge — server running. Press Ctrl+C to stop.\n")
        print(f"  Control (operator) : {control_url}")
        print(f"  View (big screen)  : http://localhost:{PORT}/view.html")
        print("\n  Opening the control panel in your browser…\n")

        # Pop the control panel open for the operator once the server is up.
        threading.Timer(0.6, lambda: webbrowser.open(control_url)).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Stopped.\n")


if __name__ == "__main__":
    main()
