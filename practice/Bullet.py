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

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


class MonsterBullet(Bullet):
    def __init__(self, x,y,sin,cos):
        super().__init__(x,y,sin,cos)
        self.image = pygame.image.load(GamePath.monsterbullet)
        self.image = pygame.transform.scale(self.image, (BulletSettings.monsterbulletWidth, BulletSettings.monsterbulletHeight))

        self.speed = MonsterBulletSettings.monsterbulletSpeed


class BossBullet(Bullet):
    def __init__(self, x,y,sin,cos):
        super().__init__(x,y,sin,cos)
        self.image = pygame.image.load(GamePath.bossbullet)
        self.image = pygame.transform.scale(self.image, (BulletSettings.monsterbulletWidth, BulletSettings.monsterbulletHeight))
        self.speed = BossBulletSettings.bossbulletSpeed

    def turn(self):
        self.sin = -self.sin
        self.cos = -self.cos

class BossShockwave(Bullet):
    def __init__(self, x,y,sin,cos):
        super().__init__(x,y,sin,cos)
        self.image = pygame.image.load(GamePath.bossshockwave)
        self.image = pygame.transform.scale(self.image, (BossshockwaveSettings.bossshockwaveWidth, BossshockwaveSettings.bossshockwaveHeight))
        self.speed = BossshockwaveSettings.bossshockwaveSpeed
        

