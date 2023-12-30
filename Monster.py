# -*- coding:utf-8 -*-

from Settings import *
import pygame

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

    def update(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.initialPosition) > self.patrollingRange:
            self.direction *= -1  # 反转方向
            self.image = pygame.transform.flip(self.image, True, False)

    def get_posx(self):
        return self.rect.x
    def get_posy(self):
        return self.rect.y