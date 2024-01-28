import pygame
from Settings import *

class BgmPlayer():
    def __init__(self):
        pass


    def play(self, name, loop=-1):
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(loop)

    def stop(self):
        pygame.mixer.music.stop()



    
