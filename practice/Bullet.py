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
        self.rect.y += self.sin*self.speed
        self.rect.x += self.cos*self.speed


class MonsterBullet(Bullet):
    def __init__(self, x,y,sin,cos):
        super().__init__(x,y,sin,cos)
        self.image = pygame.image.load(GamePath.monsterbullet)
        self.image = pygame.transform.scale(self.image, (BulletSettings.monsterbulletWidth, BulletSettings.monsterbulletHeight))
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)
        self.sin = sin
        self.cos = cos

        self.speed = MonsterBulletSettings.monsterbulletSpeed

    def update(self):
        self.rect.y += self.sin*self.speed
        self.rect.x += self.cos*self.speed

        

