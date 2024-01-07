# -*- coding:utf-8 -*-

from Settings import *
from Player import Player
import pygame
import os

# 设置角色动画
class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (WeaponSettings.weaponWidth, WeaponSettings.weaponHeight)) for img in GamePath.weapon]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PlayerSettings.playerSpeed
        self.talking = False

    def get_posx(self):
        return self.rect.x
    def get_posy(self):
        return self.rect.y

    def update(self, player):
        if player.turn == True:
            self.rect.x = player.rect.x + WeaponSettings.offsetx
        else:
            self.rect.x = player.rect.x - WeaponSettings.offsetx2
        self.rect.y = player.rect.y + WeaponSettings.offsety

    def draw(self, window):
        window.blit(self.image, self.rect)