import socket
import threading
from queue import Queue
import pickle
from message import Message

class ChatServer:
    def __init__(self):
        #basic variables
        self.run = True
        self.s = socket.socket()
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 8080
        self.connections = {}
        self.q = Queue()
        #bind host and port
        try:
            self.s.bind((self.host,self.port))
            print("Server done binding host and port")
            # general instructions
            print("Server is waiting for incoming connections...")
            print("Server will start on host", self.host)
            print("Copy and paste ip into client input")
            # makes sure one thing printed at a time
            self.print_lock = threading.Lock()
            # connect to clients
            self.acceptClients()
        except:
            print("unable to bind host and port...check if port is open")
            self.run = False

    #START
    def acceptClients(self):
        self.resetConnections()
        while self.run:
            self.s.listen(0)
            conn, addr = self.s.accept()
            print(addr, "has connected to the server")
            self.s.setblocking(True)

            name = pickle.loads(conn.recv(1024))
            self.connections[name] = conn

            self.q.put(conn)
            self.newThread()

    def newThread(self):
        t = threading.Thread(target=self.threader)
        t.start()

    def threader(self):
        while self.run:
            conn = self.q.get()
            self.recvMessage(conn)

    #SERVER IN ACTION
    def recvMessage(self,conn):
        while self.run:
            msg = conn.recv(1024)
            msg = pickle.loads(msg)
            self.redirectMsg(msg)

    def redirectMsg(self,msg):
        if msg.to in self.connections:
            conn = self.connections[msg.to]
            conn.send(pickle.dumps(msg))
        else:
            conn = self.connections[msg.sender]
            newMsg = Message(msg.sender, "WARNING: not in the server directory", "SERVER")
            conn.send(pickle.dumps(newMsg))

    def resetConnections(self):
        for conn in self.connections.values():
            conn.close()
        self.connections = {}

server = ChatServer()