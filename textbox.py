import pygame as pg

class Textbox:
    def __init__(self, screen, height=25):
        self.text = ""
        self.active = False
        self.screen = screen
        self.height = height
        self.screenWidth = pg.display.get_surface().get_width()
        self.screenHeight = pg.display.get_surface().get_height()
        self.font = pg.font.SysFont('Arial', 30)
        pg.draw.rect(self.screen, (0, 0, 0), (0, 500-self.height, self.screenWidth, self.height))

    def updateBox(self):
        self.handleMessageSize()
        msg = self.font.render(self.text, True, (0, 0, 0))
        pg.draw.rect(self.screen, (242, 242, 242), (0, 500-self.height, self.screenWidth, self.height))
        self.screen.blit(msg, (0, self.screenHeight - self.height))


    def handleMessageSize(self):
        pass
        """
        for i in range(1, len(self.text)):
            if i % 30 == 0:
                self.text = self.text[:i] + "\n" + self.text[i:]
                self.height += 25
        self.text.replace("\n", "")
        """

    def handleKeydown(self, event):
        if self.active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.updateBox()
            pg.display.update()

    def handleClick(self):
        xcor, ycor = pg.mouse.get_pos()
        if ycor > self.screenHeight - self.height:
            self.active = True
        else:
            self.active = False

    def reset(self):
        self.text = ""
        self.height = 30
        self.active = False
        self.updateBox()