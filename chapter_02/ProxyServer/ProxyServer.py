from socket import *
import sys

def format_http(status_line: str, headers: dict = None, body: bytes = b"") -> bytes:
    # Default headers dictionary if none provided
    if headers is None:
        headers = {
            "Content-Type": "text/plain; charset=UTF-8",  # Default Content-Type
            "Connection": "close"                         # Default Connection header
        }

    if body:
        headers["Content-Length"] = len(body)

    headers_formatted = "\r\n".join(f"{key}: {value}" for key, value in headers.items())

    response = (
        f"{status_line}\r\n" 
        f"{headers_formatted}\r\n\r\n"
    ).encode() + body 

    return response

if len(sys.argv) <= 1:
    print('Usage: "python ProxyServer.py server_ip"\n[server_ip: It is the IP Address of Proxy Server]')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
PORT = 12000

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], PORT))
tcpSerSock.listen(1)
print('Ready to serve...')

while True:
    # Start receiving data from the client
    connSock, addr = tcpSerSock.accept()
    print('Received a connection from:', addr)
    
    try:
        message = connSock.recv(1024)
        print("Received message:", message.split())
        
        # Extract the filename from the HTTP GET request (e.g. GET /index.html HTTP/1.1)
        if len(message.split()) < 2:
            connSock.close()
            continue
        
        filename = message.split()[1].decode().partition("/")[2]
        fileExist = "false"
        filetouse = "/" + filename
        
        try:
            # Check whether the file exists in the cache.
            # The cached file only contains the body (no HTTP headers)
            with open(filetouse[1:], "r") as f:
                outputdata = f.readlines()
            fileExist = "true"
            
            # ProxyServer finds a cache hit and generates a response message.
            # It sends its own HTTP header.
            connSock.send("HTTP/1.0 200 OK\r\n".encode())
            connSock.send("Content-Type: text/html\r\n\r\n".encode())
            
            for line in outputdata:
                connSock.send(line.encode())
            connSock.send(b"\r\n")
            
            print('Read from cache')
        
        except IOError as e:
            if fileExist == "false":
                # Create a socket on the proxy server to connect to the remote web server
                tempSocket = socket(AF_INET, SOCK_STREAM)
                hostn = filename.replace("www.", "", 1)
                print("Connecting to host:", hostn)
                
                try:
                    # Connect to the remote web server (default HTTP port 80)
                    tempSocket.connect((hostn, 80))
                    
                    # Ask the origin server for the requested file.
                    fileobj = tempSocket.makefile('rwb', 0)
                    fileobj.write(format_http("GET / HTTP/1.0"))
                    
                    # Read the full response from the origin server.
                    response = fileobj.read()
                    
                    # Find the end of the header section marked by "\r\n\r\n"
                    header_end = response.find(b"\r\n\r\n")
                    if header_end != -1:
                        # Extract only the body (everything after the header)
                        body = response[header_end + 4:]
                    else:
                        body = response
                    
                    # Cache the body only (removing the status line and headers)
                    cache_file_path = "./" + filename
                    with open(cache_file_path, "wb") as cache_file:
                        cache_file.write(body)
                    
                    # Send our own HTTP header and then the body to the client.
                    connSock.send("HTTP/1.0 200 OK\r\n".encode())
                    connSock.send("Content-Type: text/html\r\n\r\n".encode())
                    connSock.send(body)
                
                except Exception as ex:
                    connSock.send("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
                    print("Illegal request:", ex)
                    connSock.close()
            
            else:
                # HTTP response message for file not found
                connSock.send("HTTP/1.0 404 Not Found\r\n".encode())
                connSock.send("Content-Type: text/html\r\n".encode())
                connSock.send("<html><body><h1>404 Not Found</h1></body></html>".encode())
        finally:
            connSock.close()
    
    except Exception as e:
        print("Error:", e)
        connSock.close()

    # Optionally, you may close tcpSerSock if you want to terminate the proxy server.
    # For a continuously running server, leave tcpSerSock open.