# -*- coding:utf-8 -*-
from Settings import *
import prop
import pygame

# 设置 NPC
class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(GamePath.npc)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = NPCType.NPC
        self.initialPosition = x  # 记录初始位置
        self.speed = NPCSettings.npcSpeed
        self.direction = 1
        self.patrollingRange = 70  # 巡逻范围

        self.talking = False
        self.talkCD = 0 # cooldown of talk

    def update(self):
        if not self.talking:
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.initialPosition) > self.patrollingRange:
                self.direction *= -1  # 反转方向
                self.image = pygame.transform.flip(self.image, True, False)
            if self.talkCD > 0:
                self.talkCD -= 1
    
    def reset_talk_CD(self):
        self.talkCD = NPCSettings.talkCD 

    def can_talk(self):
        return self.talkCD == 0
    
    def draw(self, window):
        window.blit(self.image, self.rect)
    
class NPC2(NPC):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.npc2)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))

        self.type = NPCType.NPC2
    def update(self):
        if not self.talking:
            if self.talkCD > 0:
                self.talkCD -= 1

class Karina(NPC):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.karina)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))

        self.type = NPCType.Karina
    def update(self):
        if not self.talking:
            if self.talkCD > 0:
                self.talkCD -= 1


class merchant(NPC):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.merchant)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = NPCType.MERCHANT
    def update(self):
        if not self.talking:
            if self.talkCD > 0:
                self.talkCD -= 1

class merchant2(merchant):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.merchant2)
        self.image = pygame.transform.scale(self.image, (NPCSettings.npcWidth-10, NPCSettings.npcHeight+10))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = NPCType.MERCHANT2

class dog(NPC):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.images = [pygame.transform.scale(pygame.image.load(img), 
                            (NPCSettings.npcWidth-20, NPCSettings.npcHeight-20)) for img in GamePath.dog]
        
        self.speed = NPCSettings.dogSpeed
        self.patrollingRange = 300
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.index = 0

        self.type = NPCType.DOG

    def update(self):
        if not self.talking:
            self.index = (self.index + 1) % len(self.images)
            self.rect.x += self.speed * self.direction
            self.image = self.images[self.index]
            if abs(self.rect.x - self.initialPosition) > self.patrollingRange:
                self.direction *= -1  # 反转方向
            
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            if self.talkCD > 0:
                self.talkCD -= 1


class copperbox(merchant):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.copperbox)
        self.image = pygame.transform.scale(self.image, (NPCSettings.boxWidth, NPCSettings.boxHeight))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.type = NPCType.COPPERBOX
        self.talking = False
        self.canbuy = True
        self.talkCD = 0 # cooldown of talk
        self.wave = 0

        self.prop = prop.prop()
        self.addCoins,self.addHP,self.addAttack,self.addSpeed,self.addAttackspeed,self.text = self.prop.get_prop(self.wave)
        self.refreshCoins = PropSettings.refreshcoins

    def reset(self):
        self.canbuy = True
        self.refreshCoins = PropSettings.refreshcoins
        self.addCoins,self.addHP,self.addAttack,self.addSpeed,self.addAttackspeed,self.text = self.prop.get_prop(self.wave)

    def buy(self,player):
        if self.canbuy:
            if player.attr_update(self.addCoins , self.addHP,self.addAttack,self.addSpeed,self.addAttackspeed):
                self.canbuy = False
                return "购买成功！"
            else:
                return "金币不足 "
        else:
            if not player.attr_update(self.addCoins , self.addHP,self.addAttack,self.addSpeed,self.addAttackspeed):
                return "金币不足 "
            else:
                player.attr_update(-self.addCoins , -self.addHP,-self.addAttack,-self.addSpeed,-self.addAttackspeed)
                return "已经购买过了，尝试刷新一下"

    def refresh(self,player):
        if player.attr_update(self.refreshCoins):
            self.canbuy = True
            self.addCoins,self.addHP,self.addAttack,self.addSpeed,self.addAttackspeed,self.text = self.prop.get_prop(self.wave)
            self.refreshCoins *= 2
            return ("刷新成功！",self.refreshCoins)
            
        else:
            return ("金币不足 ",self.refreshCoins)
    

class silverbox(copperbox):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.silverbox)
        self.image = pygame.transform.scale(self.image, (NPCSettings.boxWidth, NPCSettings.boxHeight))

        self.type = NPCType.SILVERBOX

class paperbox(copperbox):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.copperbox)
        self.image = pygame.transform.scale(self.image, (NPCSettings.boxWidth, NPCSettings.boxHeight))

        self.type = NPCType.PAPERBOX


class goldenbox(copperbox):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.image = pygame.image.load(GamePath.goldenbox)
        self.image = pygame.transform.scale(self.image, (NPCSettings.boxWidth, NPCSettings.boxHeight))

        self.type = NPCType.GOLDENBOX