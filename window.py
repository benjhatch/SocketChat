import pygame as pg
from textbox import Textbox

class Window:
    def __init__(self, contact, screen):

        self.myMessages = {}
        self.sentMessages = {}
        self.order = 0

        self.headerFont = pg.font.SysFont('Arial', 40)
        self.textFont = pg.font.SysFont('Arial', 30)
        self.screen = screen
        self.contact = self.headerFont.render(contact, True, (0, 0, 0))
        self.textbox = Textbox(screen)

        self.length, self.height = self.headerFont.size(contact)
        self.updateWindow()

    def handleEvent(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.textbox.handleClick()
        if event.type == pg.KEYDOWN:
            self.textbox.handleKeydown(event)

    def displayHeader(self):
        pg.draw.rect(self.screen, (236, 240, 244), (0, 0, 500, self.height*3))
        self.screen.blit(self.contact, ((500-self.length) / 2, self.height))

    def updateWindow(self):
        self.screen.fill((255, 255, 255))
        self.displayHeader()
        for i in range(self.order):
            if i in self.sentMessages:
                self.displayMessage(self.sentMessages[i], i, True, (51, 153, 255))
            else:
                self.displayMessage(self.myMessages[i], i, False, (236, 240, 244))
        self.textbox.updateBox()
        pg.display.update()

    def displayMessage(self, msg, index, sent, color):
        length, height = self.textFont.size(msg.msg)
        x = 10
        y = height * index
        msg = self.textFont.render(msg.msg, True, (0, 0, 0))
        if sent:
            x = 490-length
        pg.draw.rect(self.screen, color, (x-2.5, y+self.height*3+2, length+5, height))
        self.screen.blit(msg, (x, y+self.height*3+2))

    def handleNewMsg(self, msg, sent=False):
        if sent:
            self.sentMessages[self.order] = msg
        else:
            self.myMessages[self.order] = msg
        self.order += 1

    def refreshBox(self):
        self.textbox.reset()