import socket
import threading
import pickle
import time
import pygame as pg
from message import Message

class Client:
    def __init__(self, host, user, to):
        self.run = True
        self.host = host
        self.user = user
        self.to = to
        self.allMessages = {}
        self.allSentMessages = []
        self.count = 0

        self.s = socket.socket()
        self.port = 8080
        self.s.connect((self.host, self.port))
        self.s.send(pickle.dumps(self.user))
        print("Connected to server")

        pg.init()
        pg.font.init()
        self.screen = pg.display.set_mode((500, 500))
        self.myFont = pg.font.SysFont('Comic Sans MS', 25)

        self.print_lock = threading.Lock()
        self.startThreads()
        self.runClient()

    def startThreads(self):
        self.t = threading.Thread(target=self.recvMsg)
        self.t.start()

    def recvMsg(self):
        while self.run:
            msg = self.s.recv(1025)
            msg = pickle.loads(msg)
            if msg.sender in self.allMessages:
                self.allMessages[msg.sender].append(msg)
            else:
                self.allMessages[msg.sender] = [msg]
            msg.display(self.screen, self.myFont, self.count)
            self.count += 1

    def sendMsg(self):
        message = input("Message: ")
        msg = Message(self.to, message, self.user)
        self.s.send(pickle.dumps(msg))
        self.allSentMessages.append(msg)
        msg.display(self.screen, self.myFont, self.count, (255, 0, 0))
        self.count += 1

    def runClient(self):
        self.screen.fill((0,0,0))
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        self.to = input('Enter who you want to send a message to: ')
                    if event.key == pg.K_m:
                        self.sendMsg()
                    if event.key == pg.K_p:
                        print(self.allMessages)
            time.sleep(0.5)

client = Client(input("Server ip: "), input("Enter username: "), input("Message to: "))