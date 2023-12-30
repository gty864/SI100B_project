# -*- coding:utf-8 -*-

from Settings import *
import time
import random

import Bullet
import pygame
import Map
import NPC
import Monster

import Player
import DialogBox
import BattleBox

class SceneManager:
    def __init__(self, window):
        self.state = GameState.GAME_PLAY_WILD
        self.map = Map.gen_map()

        self.npcs = pygame.sprite.Group()
        self.npcs.add(NPC.NPC(WindowSettings.width // 4, WindowSettings.height // 4 + 80))

        
        self.obstacles = Map.build_obstacles()
        
        self.window = window

        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        for _ in range(5):
            self.monsters.add(Monster.Monster(random.randrange(1,WindowSettings.width), random.randrange(1,WindowSettings.height)))
        self.battleBox = None

    def get_width(self):
        return WindowSettings.width 

    def get_height(self):
        return WindowSettings.height
    
    def check_event_talking(self, player, keys):
        # check for all npcs
        for npc in self.npcs.sprites():
            # 结束对话
            if npc.talking and keys[pygame.K_RETURN]:
                npc.talking = False
                player.talking = False
                npc.reset_talk_CD()
            # 保持对话
            elif pygame.sprite.collide_rect(player, npc) and npc.can_talk():
                npc.talking = True
                player.talking = True
                # TODO

    def check_event_battle(self, player, keys):
        pass

    def fire(self,x,y):
        new_bullet = Bullet.Bullet(x,y)
        self.bullets.add(new_bullet)


    def update(self,monster):
        # update npc,monster,bullet
        
        for each in self.npcs.sprites():
            each.update()
        for each in self.bullets.sprites():
            each.update(monster.get_posx(),monster.get_posy())

        for each in self.monsters.sprites():
            each.update()

    def render(self,monster):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j],
                                 (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

        
        for bullet in self.bullets.copy():
            #消除屏幕外的子弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= WindowSettings.height or bullet.rect.right >= WindowSettings.width or bullet.rect.left <= 0:
                self.bullets.remove(bullet)
            #消除碰到障碍物的子弹
            if pygame.sprite.spritecollide(bullet, self.obstacles, False):
                self.bullets.remove(bullet)
            '''
            if pygame.sprite.spritecollide(bullet, self.monsters, False):
                self.bullets.remove(bullet)
                self.monsters.remove(monster)

            collisions = pygame.sprite.groupcollide(
                self.bullets, self.monsters, True, True)    
            '''    

            #print(len(self.bullets))
        self.obstacles.draw(self.window)
        self.npcs.draw(self.window)
        self.bullets.draw(self.window)
        self.monsters.draw(self.window)

    #判断是否杀死怪物
    def iskilled(self,monster):
        for bullet in self.bullets.copy():
            if pygame.sprite.spritecollide(bullet, self.monsters, False):
                self.bullets.remove(bullet)
                self.monsters.remove(monster)
                collisions = pygame.sprite.groupcollide(
                self.bullets, self.monsters, True, True) 
                return True

    #获得一个随机怪物
    def getmonster(self):
        return random.choice(self.monsters.sprites())


        # TODO

    
