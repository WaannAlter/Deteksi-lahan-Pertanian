from http.server import SimpleHTTPRequestHandler
import socketserver
import webbrowser
import os
import sys
import threading

PORT = 9080
HTML_FILE = "index.html"

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS - optional but helpful for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, must-revalidate')
        self.send_header('Expires', '0')
        super().end_headers()

class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True  # Ensures threads exit on server shutdown

def start_web_server():
    """Starts a simple HTTP server to serve the visualization."""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(HTML_FILE):
        print(f"Error: Could not find {HTML_FILE} in {os.getcwd()}")
        print("Please make sure the HTML file exists in the same directory as this script.")
        sys.exit(1)

    handler = MyHTTPRequestHandler
    with ThreadingTCPServer(("", PORT), handler) as httpd:
        print(f"\nServing visualization at:")
        print(f"https://localhost:{PORT}/{HTML_FILE}")
        print(f"Press Ctrl+C to stop the server\n")
        try:
            webbrowser.open_new_tab(f"http://localhost:{PORT}/{HTML_FILE}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
            httpd.shutdown()
            httpd.server_close()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    start_web_server()