import socket
import threading
import pickle
import time
import pygame as pg

class Client:
    def __init__(self, host, user, to):
        self.host = host
        self.user = user
        self.to = to
        self.count = 0
        self.run = True
        pg.init()
        self.myFont = pg.font.SysFont('Comic Sans MS', 25)
        pg.font.init()
        self.screen = pg.display.set_mode((500, 500))
        self.allMessages = {}
        self.allSentMessages = {}
        self.s = socket.socket()
        self.port = 8080

        self.s.connect((self.host, self.port))
        self.s.send(pickle.dumps(self.user))
        print("Connected to server")

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
            if msg[0] in self.allMessages:
                self.allMessages[msg[0]].append(msg)
            else:
                self.allMessages[msg[0]] = [msg]
            self.displayMsg(msg[1])

    def sendMsg(self):
        msg = input("Message: ")
        data = (self.to, msg, self.user)
        self.s.send(pickle.dumps(data))
        self.displayMsg(msg)
        pg.display.update()

    def displayMsg(self,msg):
        message = self.myFont.render(msg, True, (255, 255, 255))
        self.screen.blit(message, (10, 50 + (20 * self.count)))
        self.count += 1
        pg.display.update()

    def runClient(self):
        self.screen.fill((0,0,0))
        name = self.myFont.render(self.to, True, (255, 255, 255))
        self.screen.blit(name, (250, 5))
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        self.to = input('Enter who you want to send a message to: ')
                    if event.key == pg.K_m:
                        self.sendMsg()
            time.sleep(0.5)

client = Client(input("Server ip: "), input("Enter username: "), input("Message to: "))