import socket
import threading
import pickle
import time
import pygame as pg
from window import Window
from message import Message

class Client:
    def __init__(self, host, user, to):
        self.run = True
        pg.init()

        self.host = host
        self.user = user
        self.to = to

        self.s = socket.socket()
        self.port = 8080
        self.s.connect((self.host, self.port))
        self.s.send(pickle.dumps(self.user))
        print("Connected to server")
        self.print_lock = threading.Lock()

        self.screen = pg.display.set_mode((500, 500))
        self.myContacts = {self.to: Window(self.to, self.screen)}

        self.startThreads()
        self.runClient()

    def startThreads(self):
        self.t = threading.Thread(target=self.recvMsg)
        self.t.start()

    def recvMsg(self):
        while self.run:
            msg = self.s.recv(1025)
            msg = pickle.loads(msg)
            if msg.sender in self.myContacts:
                self.myContacts[msg.sender].handleNewMsg(msg)
            else:
                self.myContacts[msg.sender] = Window(msg.sender, self.screen)
                self.myContacts[msg.sender].handleNewMsg(msg)
            self.myContacts[msg.sender].updateWindow()

    def sendMsg(self, message):
        if self.to in self.myContacts:
            msg = Message(self.to, message, self.user)
            self.s.send(pickle.dumps(msg))
            self.myContacts[self.to].handleNewMsg(msg, True)
            self.myContacts[self.to].refreshBox()
            self.myContacts[self.to].updateWindow()
        else:
            self.myContacts[self.to] = Window(self.to, self.screen)
            self.sendMsg(message)

    def runClient(self):
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    pg.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.sendMsg(self.myContacts[self.to].textbox.text)
                    self.myContacts[self.to].textbox.text = ""
                else:
                    self.myContacts[self.to].handleEvent(event)

client = Client(input("Server ip: "), input("Enter username: "), input("Message to: "))