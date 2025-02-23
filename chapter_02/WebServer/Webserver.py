from socket import socket, AF_INET, SOCK_STREAM
import json
from enum import Enum


serverPort = 12000

httpMethods = {"GET"}

line_separator = "\r\n"

def format_http_response(status_line: str, headers: dict = None, body: bytes = b"") -> bytes:
    # Default headers dictionary if none provided
    headers = headers or {}

    if body:
        headers["Content-Length"] = len(body)

    headers_formatted = "\r\n".join(f"{key}: {value}" for key, value in headers.items())

    response = (
        f"{status_line}\r\n" 
        f"{headers_formatted}\r\n\r\n"
    ).encode() + body 

    return response

def parseHTTP(msg: str):
    msgList = msg.split(line_separator)
    
    try:
        method, path, httpVersion = msgList[0].split(" ")
        body = msgList[-1]
        headers = msgList[1:-1]

        if httpVersion != "HTTP/1.1":
            return format_http_response("HTTP/1.1 400 Bad Request")
        if method not in httpMethods:
            return format_http_response("HTTP/1.1 405 Method Not Allowed")
        
        filepath = ""
        stripped_path = path.lstrip("/")
        if stripped_path == "":
            filepath = "index.html"
        else:
            filepath = stripped_path
        
        with open(filepath, mode='rb') as f:
            content = f.read()
        content_type = getContentType(filepath.split(".")[1])

        return format_http_response("HTTP/1.1 400 Bad Request", {"Content-Type": content_type, "Connection": "close"}, content)
    except FileNotFoundError:
        return format_http_response("HTTP/1.1 404 Not Found")

def getContentType(fileExtension: str) -> str:
    # Map file extensions to Content-Type
    contentTypes = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "json": "application/json",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "txt": "text/plain",
    }
    return contentTypes.get(fileExtension, "application/octet-stream")  # Default

# Create and use the server socket within a context manager
with socket(AF_INET, SOCK_STREAM) as serverSocket:
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)  # Max number of pending connections in the queue
    print(f'The server is listen on port {serverPort}')

    while True:
        # Accept a new connection within the context of the server socket
        with serverSocket.accept()[0] as connSocket:
            msg = connSocket.recv(1024).decode()
            resp = parseHTTP(msg)
            connSocket.send(resp)