# -*- coding:utf-8 -*-
from Settings import *
import pygame
import math
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y,sin,cos):
        super().__init__()
        self.image = pygame.image.load(GamePath.bullet)
        self.image = pygame.transform.scale(self.image, (BulletSettings.bulletWidth, BulletSettings.bulletHeight))
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)
        self.sin = sin
        self.cos = cos

        self.speed = BulletSettings.bulletSpeed

    def update(self):
        '''
        if math.sqrt((self.rect.x - x)**2+(self.rect.y - y)**2) <= 100:
            self.rect.y = y
            self.rect.x = x
        else: 
            self.rect.y += (y-self.rect.y) / self.speed
            self.rect.x += (x-self.rect.x) / self.speed        
        '''
        self.rect.y += self.sin*self.speed
        self.rect.x += self.cos*self.speed



        

