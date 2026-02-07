"""HTTP server manager for Easy Versioning."""

import os
import time
import threading
import http.server
import socketserver
from ..utils import info, success

class ServerManager:
    """Manages a local HTTP server for documentation preview."""
    
    def __init__(self, build_path):
        self.build_path = build_path
    
    def start_quick_server(self, latest_version, default_language):
        """
        Start a static HTTP server on localhost:8001 and open the documentation homepage.
        """
        port = 8001 # Not 8000 to not use the same port as the bat file's server
        root_path = os.path.join(self.build_path, "build")
        os.chdir(root_path)

        url = f"http://localhost:{port}/{latest_version}/{default_language}/index.html"
        
        # Server variables
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", port), handler)

        def serve():
            info(f"Serving documentation at: {url}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
            httpd.server_close()
            info("Server shut down.")

        # Start the server in a different thread
        thread = threading.Thread(target=serve)
        thread.daemon = True
        thread.start()

        # Waiting for the server to open correctly
        time.sleep(1)

        # Giving quick access using the console to the user
        success(f"\n\nServer is running,  Visit your documentation at:\n{url.replace(' ', '%20')}")

        try:
            input("Press Enter to stop the server...\n")
        except KeyboardInterrupt:
            print("\nServer interrupted by user.")
