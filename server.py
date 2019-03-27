import socket
import threading
from queue import Queue
import pickle

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
            self.s.setblocking(1)

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

    def redirectMsg(self,data):
        to = data[0]
        msg = data[1]
        sender = data[2]
        if to in self.connections:
            conn = self.connections[to]
            newMsg = (sender,msg)
            conn.send(pickle.dumps(newMsg))
        else:
            conn = self.connections[sender]
            conn.send(pickle.dumps((to,"WARNING: not in the server directory")))

    def resetConnections(self):
        for conn in self.connections.values():
            conn.close()
        self.connections = {}

server = ChatServer()