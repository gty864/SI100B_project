# -*- coding:utf-8 -*-

from Settings import *
import pygame
import random
import math

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(GamePath.monster)
        self.image = pygame.transform.scale(self.image, (MonsterSettings.monsterWidth, MonsterSettings.monsterHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = MonsterSettings.monsterSpeed
        self.direction = 1
        self.initialPosition = x
        self.patrollingRange = 400

    def update(self,x,y): #玩家的x,y坐标,t为所构成rt三角形的斜边长
        t = math.sqrt((y-self.rect.y)**2 + (x-self.rect.x)**2)
        self.rect.y += self.speed / t * (y-self.rect.y)
        self.rect.x += self.speed / t * (x-self.rect.x) 
        if  self.rect.left < 0 or self.rect.right > WindowSettings.width :
            self.direction *= -1  # 反转方向
            self.image = pygame.transform.flip(self.image, True, False)
        

    def get_posx(self):
        return self.rect.x
    def get_posy(self):
        return self.rect.y