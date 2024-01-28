# -*- coding:utf-8 -*-
from Attributes import *
from Settings import *
import pygame
import os

# 设置角色动画
class Player(pygame.sprite.Sprite,Collidable):
    def __init__(self, x, y):
        super().__init__()
        Collidable.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(img),
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for img in GamePath.player]
        self.turn = False #判断玩家当前为左还是为右，F左，T右
        self.turned = False
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = PlayerSettings.playerSpeed
        self.talking = False
        self.dx = 0
        self.dy = 0

        self.HP = PlayerSettings.playerHP
        self.Attack = PlayerSettings.playerAttack
        self.Defence = PlayerSettings.playerDefence
        self.Money = PlayerSettings.playerMoney
        self.Attackspeed = PlayerSettings.playerAttackspeed

    def move(self, dx, dy):
        self.rect = self.rect.move(dx,dy)

    def facai(self):
        self.Money +=  100

    def get_playerAttackspeed(self):
        return self.Attackspeed

    def get_posx(self):
        return self.rect.x
    def get_posy(self):
        return self.rect.y
    
    ####try_move更新可能移动，update更新实际移动
    def update(self, keys, obstacle = False):
        if self.talking:
            # 如果不移动，显示静态图像
            self.index = 0
            self.image = self.images[self.index]
        else:
            # Update Player Position
            if obstacle:
                self.rect = self.rect.move(-self.dx, -self.dy)
            # 更新角色动画
            if any(keys):
                self.index = (self.index + 1) % 4
                if self.turn == False:
                    self.index += 4 #挖了个小坑，之后若player的img多了要改一改
                self.image = self.images[self.index]

    def try_move(self, keys):
        if self.talking:
            # 如果不移动，显示静态图像
            self.index = 0
            self.image = self.images[self.index]
        else:
            dx = 0
            dy = 0

            if keys[pygame.K_w] and self.rect.top > 0 :
                dy -= self.speed
            if keys[pygame.K_s] and self.rect.bottom < WindowSettings.height:
                dy += self.speed
            if keys[pygame.K_a] and self.rect.left > 0:
                dx -= self.speed
                self.turn = False

            if keys[pygame.K_d] and self.rect.right < WindowSettings.width:
                dx += self.speed
                self.turn = True
                
            self.rect = self.rect.move(dx, dy)
            self.dx = dx
            self.dy = dy

    def attr_update(self, addCoins = 0, addHP = 0, addAttack = 0, addSpeed =0, addAttackspeed =0,addDefence = 0):
        if self.Money + addCoins < 0:
            return False
        if self.HP + addHP < 0:
            return False
        self.Money += addCoins
        self.HP += addHP
        self.Attack += addAttack
        self.Defence += addDefence
        self.speed += addSpeed
        self.Attackspeed += addAttackspeed
        return True

    def wasattacked(self,attack):
        self.HP -= attack
 
    def get_attack(self):
        return self.Attack
    
    def get_HP(self):
        return self.HP

    def draw(self, window):
        window.blit(self.image, self.rect)