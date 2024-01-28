# -*- coding:utf-8 -*-

from Settings import *
import pygame
import random
import math

def distance(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)

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
        '''
        if  self.rect.left < 0 or self.rect.right > WindowSettings.width :
            self.direction *= -1  # 反转方向
            self.image = pygame.transform.flip(self.image, True, False)   
        '''


    def wasattacked(self,attack):
        self.HP -= attack

    def faster(self):
        self.speed += 1

    def stronger(self):
        self.HP += 4
        self.Attack += 1

    def get_posx(self):
        return self.rect.x
    def get_posy(self):
        return self.rect.y
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
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
        self.sum = 0
        self.rect.topleft = (x, y)

        self.ifcharge = False

        self.chargex = 0
        self.chargey = 0
        self.chargecd = HulkSettings.hulkchargecd
        self.speed = HulkSettings.hulkSpeed
        self.chargedist = HulkSettings.hulkchargedist
        self.chargespeed = HulkSettings.hulkchargespeed
        self.HP = HulkSettings.hulkHP
        self.Attack = HulkSettings.hulkAttack
        self.money = HulkSettings.hulkMoney
        self.direction = 1
        self.chargetime = 0

    def update(self,x,y):
        self.chargetime += 1
        t = math.sqrt((y-self.rect.y)**2 + (x-self.rect.x)**2)
        if self.chargetime > self.chargecd :

            self.charge(self.chargex,self.chargey,t)
        else:
            self.chargex = x
            self.chargey = y
            if t != 0:
                self.rect.y += self.speed / t * (y-self.rect.y)
                self.rect.x += self.speed / t * (x-self.rect.x)
                pass

    def charge(self,x,y,t):
        if self.sum > self.chargedist:
                self.chargetime = 0
                self.sum = 0
        else:
            self.sum += self.speed
            if t != 0:
                self.rect.y += self.chargespeed * self.speed / t * (y-self.rect.y)
                self.rect.x += self.chargespeed * self.speed / t * (x-self.rect.x)


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

class Boss(Monster): # Boss
    def __init__(self, x, y):
        super().__init__(x,y)

        self.type = MonsterType.Boss
        self.image = pygame.image.load(GamePath.boss)
        self.image = pygame.transform.scale(self.image, (MonsterSettings.monsterWidth*4.5, MonsterSettings.monsterHeight*4.5))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.speed = BossSettings.bossSpeed
        self.HP = BossSettings.bossHP
        self.Attack = BossSettings.bossAttack
        self.direction = 1

    #def 

