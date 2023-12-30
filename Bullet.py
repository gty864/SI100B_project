# -*- coding:utf-8 -*-
from Settings import *
import pygame
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load(GamePath.bullet)
        self.image = pygame.transform.scale(self.image, (BulletSettings.bulletWidth, BulletSettings.bulletHeight))
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)

        self.speed = BulletSettings.bulletSpeed

    def update(self,x,y):
        self.rect.y += (y-self.rect.y) / self.speed
        self.rect.x += (x-self.rect.x) / self.speed


        

