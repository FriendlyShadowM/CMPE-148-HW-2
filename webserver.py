# webserver.py
from socket import *
import os
import mimetypes
import sys

HOST = ""          # Listen on all interfaces
PORT = 6789        # Change if needed

def http_response(status_line: str, headers: dict, body: bytes) -> bytes:
    # Ensure required headers
    headers = {
        "Server": "MiniPy/1.0",
        "Connection": "close",
        **headers,
        "Content-Length": str(len(body)),
    }
    # Build header block with CRLF
    header_block = status_line + "\r\n" + "\r\n".join(f"{k}: {v}" for k, v in headers.items()) + "\r\n\r\n"
    return header_block.encode("iso-8859-1") + body

def guess_type(path: str) -> str:
    ctype, _ = mimetypes.guess_type(path)
    return ctype or "application/octet-stream"

def serve_file(path: str) -> bytes:
    try:
        with open(path, "rb") as f:
            data = f.read()
        status = "HTTP/1.1 200 OK"
        headers = {"Content-Type": guess_type(path)}
        return http_response(status, headers, data)
    except FileNotFoundError:
        body = b"""<html><body><h1>404 Not Found</h1><p>The requested file was not found.</p></body></html>"""
        return http_response("HTTP/1.1 404 Not Found", {"Content-Type": "text/html; charset=utf-8"}, body)

def bad_request() -> bytes:
    body = b"<html><body><h1>400 Bad Request</h1></body></html>"
    return http_response("HTTP/1.1 400 Bad Request", {"Content-Type": "text/html; charset=utf-8"}, body)

def method_not_allowed() -> bytes:
    body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
    return http_response("HTTP/1.1 405 Method Not Allowed", {"Content-Type": "text/html; charset=utf-8", "Allow": "GET"}, body)

def internal_error() -> bytes:
    body = b"<html><body><h1>500 Internal Server Error</h1></body></html>"
    return http_response("HTTP/1.1 500 Internal Server Error", {"Content-Type": "text/html; charset=utf-8"}, body)

def sanitize_path(url_path: str) -> str:
    # Default document
    if url_path == "/" or url_path == "":
        url_path = "/HelloWorld.html"

    # Prevent path traversal and strip leading slash
    safe = os.path.normpath(url_path.lstrip("/"))
    if safe.startswith("..") or os.path.isabs(safe):
        return None
    return safe

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Allow quick restart on Windows/Linux
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(1)

    print(f"Ready to serve on port {PORT}...")

    try:
        while True:
            connectionSocket, addr = serverSocket.accept()
            try:
                message = connectionSocket.recv(4096)
                if not message:
                    connectionSocket.close()
                    continue

                # Decode only the request line safely
                try:
                    request_text = message.decode("iso-8859-1", errors="replace")
                    request_line = request_text.split("\r\n", 1)[0]
                    parts = request_line.split()
                    if len(parts) < 3:
                        connectionSocket.sendall(bad_request())
                        continue
                    method, path, version = parts[0], parts[1], parts[2]
                except Exception:
                    connectionSocket.sendall(bad_request())
                    continue

                if method.upper() != "GET":
                    connectionSocket.sendall(method_not_allowed())
                    continue

                safe_path = sanitize_path(path)
                if not safe_path:
                    connectionSocket.sendall(bad_request())
                    continue

                response = serve_file(safe_path)
                connectionSocket.sendall(response)

            except Exception:
                # Fallback on any unexpected error per-connection
                try:
                    connectionSocket.sendall(internal_error())
                except Exception:
                    pass
            finally:
                connectionSocket.close()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        serverSocket.close()
        sys.exit(0)

if __name__ == "__main__":
    main()
