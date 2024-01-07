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
        self.scene = Scene.MainMenuScene(window)#初始界面
        self.tot = 0

        self.obstacles = Map.gen_obstacles()
        self.window = window

    def get_width(self):
        return WindowSettings.width 

    def get_height(self):
        return WindowSettings.height
                
    
    def flush_scene(self,dest):
        if dest == GameState.GAME_PLAY_WILD:
            self.scene = Scene.WildScene(self.window)
        elif dest == GameState.GAME_PLAY_CITY:
            self.scene = Scene.CityScene(self.window)
        self.scene.render()

    def render_mainmenu(self):
        self.scene.render()

    def render_wild_scene(self,player,wave):
        self.scene.render()
        textHP = "player HP: " + str(player.HP)
        textwave = "Wave:" + str(wave)
        textAttack = "player Attack" + str(player.Attack)
        textMoney = "player Money: " + str(player.Money)
        self.write(textHP,1120,10)
        self.write(textwave,500,100)
        self.write(textAttack,1120,35)
        self.write(textMoney,1100,70)

    def render_city_scene(self,player):
        self.scene.render()
        textHP = "player HP: " + str(player.HP)
        textAttack = "player Attack" + str(player.Attack)
        textMoney = "player Money: " + str(player.Money)
        self.write(textHP,1120,10)
        self.write(textAttack,1120,35)
        self.write(textMoney,1100,70)
        
    def write(self,text,x,y):
        self.window.blit(self.font.render(text, True,self.fontColor),
                        (x, y))        

        # TODO

    
