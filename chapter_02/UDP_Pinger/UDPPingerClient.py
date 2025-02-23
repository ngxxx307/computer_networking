from socket import socket, AF_INET, SOCK_DGRAM
from time import time

serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # AF_INET means IPv4, SOCK_DGRAM means UDP
clientSocket.settimeout(1)

for i in range(10):
    clientSocket.sendto(str(i).encode(),(serverName, serverPort))
    start_time = time()

    try: 
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        elapsed_time = time() - start_time
        print("RTT:", i, f"{elapsed_time:.6f}")
    except TimeoutError:
        print("timeout: " , i)

clientSocket.close()