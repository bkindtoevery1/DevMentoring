import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 5000))
serversocket.listen(5)

while True:
    (clientsocket, address) = serversocket.accept()
    print('connected by', address)