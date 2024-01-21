# -*- coding:utf-8 -*-

import pygame
from GameManager import GameManager
from Settings import *

def run_game():
    pygame.init()
    pygame.display.set_caption(WindowSettings.name)
    window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
    manager = GameManager(window)

    clock = pygame.time.Clock()     
    while True:
        clock.tick(30)
        manager.switch_state()      
        manager.update()
        manager.render()
        pygame.display.flip()

if __name__ == "__main__":
    run_game()
