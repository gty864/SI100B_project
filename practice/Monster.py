# -*- coding:utf-8 -*-

from Settings import *
import pygame
import random
import math

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.type = MonsterType.Monster
        self.image = pygame.image.load(GamePath.monster)
        self.image = pygame.transform.scale(self.image, (MonsterSettings.monsterWidth, MonsterSettings.monsterHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = MonsterSettings.monsterSpeed
        self.HP = MonsterSettings.monsterHP
        self.Attack = MonsterSettings.monsterAttack
        self.money = MonsterSettings.monsterMoney
        self.direction = 1

    def update(self,x,y): #玩家的x,y坐标,t为所构成rt三角形的斜边长
        t = math.sqrt((y-self.rect.y)**2 + (x-self.rect.x)**2)
        if t != 0:
            self.rect.y += self.speed / t * (y-self.rect.y)
            self.rect.x += self.speed / t * (x-self.rect.x) 
        if  self.rect.left < 0 or self.rect.right > WindowSettings.width :
            self.direction *= -1  # 反转方向
            self.image = pygame.transform.flip(self.image, True, False)

    def wasattacked(self,attack):
        self.HP -= attack

    def faster(self):
        self.speed += 2
        
    def get_attack(self):
        return self.Attack
    
    def get_HP(self):
        return self.HP

    def get_posx(self):
        return self.rect.x
    def get_posy(self):
        return self.rect.y
    
class Thug(Monster): #暴徒，速度快，血量低，伤害高
    def __init__(self, x, y):
        super().__init__(x,y)

        self.type = MonsterType.Thug
        self.image = pygame.image.load(GamePath.thug)
        self.image = pygame.transform.scale(self.image, (MonsterSettings.monsterWidth, MonsterSettings.monsterHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = ThugSettings.thugSpeed
        self.HP = ThugSettings.thugHP
        self.Attack = ThugSettings.thugAttack
        self.money = ThugSettings.thugMoney
        self.direction = 1

class Hulk(Monster): #胡尔克，血量高，伤害高
    def __init__(self, x, y):
        super().__init__(x,y)

        self.type = MonsterType.Hulk
        self.image = pygame.image.load(GamePath.hulk)
        self.image = pygame.transform.scale(self.image, (MonsterSettings.monsterWidth*2, MonsterSettings.monsterHeight*2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = HulkSettings.hulkSpeed
        self.HP = HulkSettings.hulkHP
        self.Attack = HulkSettings.hulkAttack
        self.money = HulkSettings.hulkMoney
        self.direction = 1

class Soldier(Monster): #士兵，会开枪
    def __init__(self, x, y):
        super().__init__(x,y)

        self.type = MonsterType.Soldier
        self.image = pygame.image.load(GamePath.soldier)
        self.image = pygame.transform.scale(self.image, (MonsterSettings.monsterWidth*1.2, MonsterSettings.monsterHeight*1.2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = SoldierSettings.soldierSpeed
        self.HP = SoldierSettings.soldierHP
        self.Attack = SoldierSettings.soldierAttack
        self.money = SoldierSettings.soldierMoney
        self.direction = 1

