import pygame as pg

class Textbox:
    def __init__(self, screen, height=25):
        self.text = ""
        self.lines = []
        self.currentIndex = 0

        self.active = False
        self.screen = screen
        self.height = height
        self.screenWidth = pg.display.get_surface().get_width()
        self.screenHeight = pg.display.get_surface().get_height()
        self.font = pg.font.SysFont('Arial', 30)
        pg.draw.rect(self.screen, (0, 0, 0), (0, 500-self.height, self.screenWidth, self.height))

    def updateBox(self):
        pg.draw.rect(self.screen, (242, 242, 242), (0, 500-self.height, self.screenWidth, self.height))
        self.showText()


    def showText(self):
        self.handleText()
        for i in range(len(self.lines)):
            lineText = self.font.render(self.lines[i].text, True, (0, 0, 0))
            self.screen.blit(lineText, (0, self.lines[i].pos))
            if not self.lines[i].complete:
                self.lines.pop(i)

    def handleText(self):
        for i in range(self.currentIndex, len(self.text)):
            textLength, textHeight = self.font.size(self.text[self.currentIndex:i])
            if textLength >= self.screenWidth:
                self.height += textHeight
                self.lines.append(Line(self.text[self.currentIndex:i], self.screenHeight - textHeight))
                self.currentIndex = i
                for line in self.lines:
                    line.updatePos(textHeight)
        self.lines.append(Line(self.text[self.currentIndex:len(self.text)], self.screenHeight - 25, False))


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
        self.currentIndex = 0
        self.active = False
        self.updateBox()

class Line:
    def __init__(self, text, pos, complete = True):
        self.text = text
        self.pos = pos
        self.complete = complete

    def addChar(self, char):
        self.text += char

    def updatePos(self, unit):
        self.pos -= unit