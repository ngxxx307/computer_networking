from socket import socket, AF_INET, SOCK_STREAM

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort)) # Unlike UDP, connection must be established before sending data

sentence = input("Input lowercase sentence:")

clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)

print("From Server: ", modifiedSentence.decode())

clientSocket.close()