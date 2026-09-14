import http.server
import socketserver
import mimetypes
import os
import socket

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Ensure correct MIME types for PS4 WebKit & AppCache
mimetypes.add_type('text/cache-manifest', '.appcache')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/octet-stream', '.bin')
mimetypes.add_type('text/html', '.html')

class PS4ExploitHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Disable caching during testing to ensure updated scripts load immediately
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} -> {args[0]}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    local_ip = get_local_ip()
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), PS4ExploitHTTPHandler) as httpd:
        print("=" * 65)
        print("  PS4 13.52 EXPLOIT WEB HOST SERVER")
        print("=" * 65)
        print(f"  Root Directory: {DIRECTORY}")
        print(f"  Local PC IP   : {local_ip}")
        print(f"  Port          : {PORT}")
        print("-" * 65)
        print("  ABRE ESTA URL EN EL NAVEGADOR DE TU PS4:")
        print(f"  --> http://{local_ip}:{PORT}/index.html")
        print("=" * 65)
        print("Esperando conexiones de la PS4...\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")
