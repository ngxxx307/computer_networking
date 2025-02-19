from socket import socket, AF_INET, SOCK_DGRAM

serverName = "127.0.0.1"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # AF_INET means IPv4, SOCK_DGRAM means UDP

message = input("Input lowercase sentence")

clientSocket.sendto(message.encode(),(serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())

clientSocket.close()