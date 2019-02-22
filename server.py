import socket

s = socket.socket()
host = socket.gethostbyname(socket.gethostname())
print("server will start on host", host)
port = 8080
s.bind((host,port))
print("Server done binding to host and port successfully")
print()
print("Server is waiting for incoming connections")
s.listen(1)
conn, addr = s.accept()
print(addr, "Has connected to the server and is now online...")
print()
while 1:
    message = input("Enter a message: ")
    message = message.encode()
    conn.send(message)
    print("message has been sent")
    print()
    incoming_message = conn.recv(1024)
    incoming_message = incoming_message.decode()
    print("Client: ", incoming_message)
    print()
