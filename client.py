import socket
import threading
import pickle
import time

class Client:
    def __init__(self):
        self.run = True
        self.latestMsg = []
        self.s = socket.socket()
        self.id = input("Enter your username: ")
        self.host = input("Please enter the hostname of the server: ")
        self.port = 8080

        self.s.connect((self.host, self.port))
        self.s.send(pickle.dumps(self.id))
        print("Connected to server")

        self.print_lock = threading.Lock()
        self.startThreads()

        self.sendMsg()

    def startThreads(self):
        self.t = threading.Thread(target=self.recvMsg)
        self.t.start()

    def recvMsg(self):
        while self.run:
            msg = self.s.recv(1025)
            msg = pickle.loads(msg)
            self.latestMsg.append(msg)

    def sendMsg(self):
        while self.run:
            self.displayMessages()
            to = input("To: ")
            msg = input("Message: ")
            print()
            data = (to,msg,self.id)
            self.s.send(pickle.dumps(data))
            time.sleep(0.5)

    def displayMessages(self):
        for msg in self.latestMsg:
            print(msg,end="\n\n")
        del self.latestMsg[:]


client = Client()