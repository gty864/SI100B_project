import pygame
from Settings import *

class BgmPlayer():
    def __init__(self):
        ##### Your Code Here ↓ #####
        
        pass
        ##### Your Code Here ↑ #####


    def play(self, name, loop=-1):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.load(name)
        pygame.mixer.music.play(loop)
        pass
        ##### Your Code Here ↑ #####

    def stop(self):
        ##### Your Code Here ↓ #####
        pygame.mixer.music.stop()
        pass
        ##### Your Code Here ↑ #####

    def update(self, GOTO):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


    
