# -*- coding:utf-8 -*-

from typing import *
from Settings import *
from SceneManager import SceneManager
from Scene import Scene
from Player import Player

import pygame
import math
import random
import sys

import Bullet
import Map
import NPC
import Monster


import DialogBox
import BattleBox

def distance(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)

class GameManager:
    def __init__(self,window):

        self.state = GameState.GAME_PLAY_WILD
        self.scene = SceneManager(window)
        self.tot = 0
        self.attackspeed = 0 #控制攻速的变量，并非攻速

        self.player = Player(WindowSettings.width // 2, WindowSettings.height // 2)

        self.npcs = pygame.sprite.Group()
        self.npcs.add(NPC.NPC(WindowSettings.width // 4, WindowSettings.height // 4 + 80))

        self.obstacles = Map.gen_obstacles()
        self.count = 60
        self.window = window
        self.screen = Scene(window)

        self.monsternum = MonsterSettings.initialmonsternum
        self.monsterfrequency = 0
        self.wave = 1

        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        for _ in range(MonsterSettings.initialmonsternum):
            self.monsters.add(Monster.Monster(random.randrange(5,WindowSettings.width-5), random.randrange(5,WindowSettings.height-5)))
        self.battleBox = None
    
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

    def fire(self,x,y):
        min = 998244353
        flg = 0  
        for each in self.monsters.sprites():
            flg = 1
            if distance(x,y,each.get_posx(),each.get_posy()) < min:
                min = distance(x,y,each.get_posx(),each.get_posy())
                monsterx = each.get_posx()
                monstery = each.get_posy()
        if flg == 1:  #如果有怪才射
            t = math.sqrt((monstery-y)**2 + (monsterx-x)**2) #t为斜边长
            if t != 0:
                new_bullet = Bullet.Bullet(x,y,(monstery-y)/t,(monsterx-x)/t)
                self.bullets.add(new_bullet)
            else:
                new_bullet = Bullet.Bullet(x,y,0,1)
                self.bullets.add(new_bullet)

    def update(self):
        if self.state == GameState.GAME_QUIT:
            pygame.quit()
            sys.exit()
        # 战斗结束，进入商店
        if self.state == GameState.GAME_PLAY_CITY:    
            self.update_city()
            self.stop_monster()
            #商店结束，进入战斗
        if self.state == GameState.GAME_PLAY_WILD:
            self.timing()
            self.update_wild()

    def update_city(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.scene.scene)

        for each in self.npcs.sprites():
            each.update()


    def update_wild(self):
        # update npc,monster,bullet
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.scene.scene)
        self.attackspeed += 1
        if keys[pygame.K_SPACE]:     #按空格键开火                               
            if self.attackspeed > self.player.Attackspeed: 
                self.fire(self.player.get_posx(),self.player.get_posy())
                self.attackspeed = 0   

        for each in self.npcs.sprites():
            each.update()
        for each in self.bullets.sprites():
            each.update()

        for each in self.monsters.sprites():
            each.update(self.player.get_posx(),self.player.get_posy())

        self.gen_monster()
        self.update_bullet(self.player)
        self.update_monster(self.player)	
        
    def gen_monster(self):
        if len(self.monsters.sprites()) < 1:
            if  self.wave >= 2:
                for _ in range(4):
                    self.monsters.add(Monster.Thug(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))
            self.monsternum+=1
            for _ in range(self.monsternum):
                self.monsters.add(Monster.Monster(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))
            for each in self.monsters.sprites():
                each.faster()



       
    def update_bullet(self,player):
         #消除碰到怪物的子弹        
        for monster in self.monsters.copy():
                if pygame.sprite.spritecollide(monster,self.bullets, False):
                    for bullet in self.bullets.copy():
                        if pygame.sprite.spritecollide(bullet,self.monsters, False): #怪被子弹击中了，减血
                            monster.wasattacked(player.get_attack())
                            if monster.get_HP() <= 0 :
                                self.monsters.remove(monster)
                            self.bullets.remove(bullet)

        for bullet in self.bullets.copy():
            #消除屏幕外的子弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= WindowSettings.height or bullet.rect.right >= WindowSettings.width or bullet.rect.left <= 0:
                self.bullets.remove(bullet)
            #消除碰到障碍物的子弹
            if pygame.sprite.spritecollide(bullet, self.obstacles, False):
                self.bullets.remove(bullet)
        
    def update_monster(self,player):
        self.monsterfrequency += 1
        for monster in self.monsters.copy():
            if pygame.sprite.spritecollide(player, self.monsters, False):
                if self.monsterfrequency > 10:
                    player.wasattacked(monster.get_attack())
                    self.monsterfrequency = 0
                if player.get_HP() <= 0:
                    self.active = False

    def switch_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.GAME_QUIT
            if event.type == GameEvent.EVENT_ENDFIGHT:
                self.scene.flush_scene()
                self.wave += 1
                self.state = GameState.GAME_PLAY_CITY
            if event.type == GameEvent.EVENT_FIGHT:
                 self.scene.flush_scene()
                 self.state = GameState.GAME_PLAY_WILD
    
    def render(self):
        if self.state == GameState.GAME_QUIT:
                pygame.quit()
                sys.exit()
            # 战斗结束，进入商店
        if self.state == GameState.GAME_PLAY_CITY:
                self.stop_monster()
                self.player.draw(self.window)
                self.render_city()
            #商店结束，进入战斗
        if self.state == GameState.GAME_PLAY_WILD:
            self.render_wild()
            
            self.scene.write("Countdown: "+str(self.count),500,50)


    def render_wild(self):
        self.scene.render_wild_scene(self.player,self.wave)
        self.monsters.draw(self.window)
        self.bullets.draw(self.window)
        self.player.draw(self.window)

    def render_city(self):
        self.scene.render_city_scene(self.player)
        self.player.draw(self.window)

    def timing(self):
        self.tot += 1
        if self.tot >= ClockSettings.clock:
            self.count -=1
            self.tot = 0
        if self.count <= 57:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_ENDFIGHT))
            self.count = 60

    def stop_monster(self):
        for monster in self.monsters.copy():
            self.monsters.remove(monster)        

    #获得group中的一个随机怪物
    def getmonster(self):
        return random.choice(self.monsters.sprites())

        # TODO

    
