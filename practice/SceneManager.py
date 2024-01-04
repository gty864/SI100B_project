# -*- coding:utf-8 -*-

from typing import *
from Settings import *
import math
import random
import time
import sys

import Bullet
import pygame
import Map
import NPC
import Monster
import Scene

class SceneManager:
    def __init__(self, window, fontSize: int = BattleSettings.textSize):
        
        self.fontSize = fontSize
        self.fontColor = (255, 0, 0)
        self.font = pygame.font.Font(None, self.fontSize)
        self.map = Map.gen_city_map()
        self.scene = Scene.CityScene(window)
        self.tot = 0

        self.obstacles = Map.gen_obstacles()
        self.window = window

    def get_width(self):
        return WindowSettings.width 

    def get_height(self):
        return WindowSettings.height
                
    
    def flush_scene(self):
        if self.scene.type == SceneType.CITY:
            self.scene = Scene.WildScene(self.window)
        elif self.scene.type == SceneType.WILD:
            self.scene = Scene.CityScene(self.window)
        self.scene.render()

    def render_wild_scene(self,player,wave):
        self.scene.render()
        textHP = "player HP: " + str(player.HP)
        textwave = "Wave:" + str(wave)
        self.write(textHP,1000,50)
        self.write(textwave,500,100)

    def render_city_scene(self,player):
        self.scene.render()
        textHP = "player HP: " + str(player.HP)
        self.write(textHP,1000,50)
        
    def write(self,text,x,y):
        self.window.blit(self.font.render(text, True,self.fontColor),
                        (x, y))        

        # TODO

    
