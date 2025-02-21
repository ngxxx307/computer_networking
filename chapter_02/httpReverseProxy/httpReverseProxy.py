from socket import socket, AF_INET, SOCK_STREAM
from enum import Enum


serverPort = 12000

httpMethods = {"GET"}

def parseHTTP(msg: str):
    
    msgList = msg.split("\r\n")
    
    try:
        method, path, httpVersion = msgList[0].split(" ")
        body = msgList[-1]
        headers = msgList[1:-1]

        if httpVersion != "HTTP/1.1":
            return "HTTP/1.1 400 Bad Request\r\n\r\n"
        if method not in httpMethods:
            return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        
        filepath = ""
        stripped_path = path.lstrip("/")
        if stripped_path == "":
            filepath = "index.html"
        else:
            filepath = stripped_path
        print("filepath:", filepath, path)
        
        with open(filepath, mode='rb') as f:
            content = f.read()
        print(content)
    except FileNotFoundError:
        return  "HTTP/1.1 404 Not Found\r\n\r\n"
    except Exception as e:
        print(e)
        print(type(e))
        return "HTTP/1.1 400 Bad Request\r\n\r\n"
    return f"HTTP/1.1 200 OK\r\n\r\n"

def getContentType(fileExtension: str) -> str:
    # Map file extensions to Content-Type
    contentTypes = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".txt": "text/plain",
    }
    return contentTypes.get(fileExtension, "application/octet-stream")  # Default

# Create and use the server socket within a context manager
with socket(AF_INET, SOCK_STREAM) as serverSocket:
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)  # Max number of pending connections in the queue
    print('The server is ready to receive')

    while True:
        # Accept a new connection within the context of the server socket
        with serverSocket.accept()[0] as connSocket:
            msg = connSocket.recv(1024).decode()
            resp = parseHTTP(msg)
            print("resp: ", resp)
            connSocket.send(resp.encode())