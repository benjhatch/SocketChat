import pygame as pg

class Message:
    def __init__(self, to, msg, sender):
        self.to = to
        self.msg = msg
        self.sender = sender