import pygame as pg
class Window:
    def __init__(self, contact, screen):

        self.myMessages = {}
        self.sentMessages = {}
        self.order = 0

        self.screen = screen
        self.headerFont = pg.font.SysFont('Arial', 25)
        self.textFont = pg.font.SysFont('Arial', 18)
        self.contact = self.headerFont.render(contact, True, (255, 0, 0))
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.contact, (250, 8))

        self.updateWindow()

    def updateWindow(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.contact, (250, 8))
        for i in range(self.order):
            if i in self.sentMessages:
                self.displayMessage(self.sentMessages[i], i, True, (0, 0, 0))
            else:
                self.displayMessage(self.myMessages[i], i, False, (0, 0, 255))
        pg.display.update()

    def displayMessage(self, msg, index, sent, color):
        x,y = self.textFont.size(msg.msg)
        msg = self.textFont.render(msg.msg, True, color)
        if sent:
            self.screen.blit(msg, (490-x, 30+(y*index)))
        else:
            self.screen.blit(msg, (10, 30+(y*index)))
        pg.display.update()

    def handleNewMsg(self, msg, sent=False):
        if sent:
            self.sentMessages[self.order] = msg
        else:
            self.myMessages[self.order] = msg
        self.order += 1