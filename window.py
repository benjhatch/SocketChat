import pygame as pg
class Window:
    def __init__(self, contact, screen):

        self.myMessages = {}
        self.sentMessages = {}
        self.order = 0

        self.headerFont = pg.font.SysFont('Arial', 25)
        self.textFont = pg.font.SysFont('Arial', 18)
        self.screen = screen
        self.contact = self.headerFont.render(contact, True, (0, 0, 0))

        self.length, self.height = self.headerFont.size(contact)
        self.updateWindow()

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
        pg.display.update()

    def displayMessage(self, msg, index, sent, color):
        length, height = self.textFont.size(msg.msg)
        x = 10
        y = height * index
        msg = self.textFont.render(msg.msg, True, (0, 0, 0))
        if sent:
            x = 490-length
        pg.draw.rect(self.screen, color, (x-2.5, y+self.height*3, length+5, height))
        self.screen.blit(msg, (x, y+self.height*3))
        pg.display.update()

    def handleNewMsg(self, msg, sent=False):
        if sent:
            self.sentMessages[self.order] = msg
        else:
            self.myMessages[self.order] = msg
        self.order += 1