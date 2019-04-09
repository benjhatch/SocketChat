import pygame as pg
class Window:
    def __init__(self, contact, screen):

        self.myMessages = {}
        self.sentMessages = {}
        self.order = 0

        self.screen = screen
        self.myFont = pg.font.SysFont('Comic Sans MS', 25)
        self.contact = self.myFont.render(contact, True, (255, 0, 0))

        self.updateWindow()

    def updateWindow(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.contact, (250, 25))
        for i in range(self.order):
            if i in self.sentMessages:
                self.displayMessage(self.sentMessages[i], i, (0, 0, 0))
            else:
                self.displayMessage(self.myMessages[i], i, (0, 0, 255))
        pg.display.update()

    def displayMessage(self, msg, index, color):
        msg = self.myFont.render(msg.msg, True, color)
        self.screen.blit(msg, (10, 50 + (25 * index)))
        pg.display.update()

    def handleNewMsg(self, msg, sent=False):
        if sent:
            self.sentMessages[self.order] = msg
        else:
            self.myMessages[self.order] = msg
        self.order += 1