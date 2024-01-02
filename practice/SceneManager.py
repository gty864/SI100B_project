# -*- coding:utf-8 -*-

from Settings import *
import math
import random

import Bullet
import pygame
import Map
import NPC
import Monster
import Button

import Player
import DialogBox
import BattleBox

def distance(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)

class SceneManager:
    def __init__(self, window):
        self.state = GameState.GAME_PLAY_WILD
        self.map = Map.gen_map()
        self.active = False

        self.npcs = pygame.sprite.Group()
        self.npcs.add(NPC.NPC(WindowSettings.width // 4, WindowSettings.height // 4 + 80))

        
        self.obstacles = Map.build_obstacles()
        
        self.window = window

        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        for _ in range(5):
            self.monsters.add(Monster.Monster(random.randrange(5,WindowSettings.width-5), random.randrange(5,WindowSettings.height-5)))
        self.battleBox = None

    def get_width(self):
        return WindowSettings.width 

    def get_height(self):
        return WindowSettings.height
    
    def begin_game(self):
        #self.state.reset_state()
        #加一段重置游戏设定
        self.active = True
    
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
        min = 998244353
        for each in self.monsters.sprites():
            if distance(x,y,each.get_posx(),each.get_posy()) < min:
                min = distance(x,y,each.get_posx(),each.get_posy())
                monsterx = each.get_posx()
                monstery = each.get_posy()

        t = math.sqrt((monstery-y)**2 + (monsterx-x)**2) #t为斜边长
        new_bullet = Bullet.Bullet(x,y,(monstery-y)/t,(monsterx-x)/t)
        self.bullets.add(new_bullet)


    def update(self,player):
        # update npc,monster,bullet
        
        for each in self.npcs.sprites():
            each.update()
        for each in self.bullets.sprites():
            each.update()

        for each in self.monsters.sprites():
            each.update(player.get_posx(),player.get_posy())
        
        #怪少了，生成新的怪
        if len(self.monsters.sprites()) < 1:
            for _ in range(5):
                self.monsters.add(Monster.Monster(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))

    def render(self,player):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j],
                                 (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
                
         #消除碰到怪物的子弹和怪物        
        for monster in self.monsters.copy():
                if pygame.sprite.spritecollide(monster,self.bullets, False):
                    for bullet in self.bullets.copy():
                        if pygame.sprite.spritecollide(bullet,self.monsters, False):
                            self.monsters.remove(monster)
                            self.bullets.remove(bullet)

        for monster in self.monsters.copy():
            if pygame.sprite.spritecollide(player, self.monsters, False):
                self.monsters.remove(monster)
                self.active = False                                         
        
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
                return True

    #获得group中的一个随机怪物
    def getmonster(self):
        return random.choice(self.monsters.sprites())

    def game_active(self):
        return self.active

        # TODO

    
