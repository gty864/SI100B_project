# -*- coding:utf-8 -*-

from typing import *
from Settings import *
import math
import random
import time
import sys

import Bullet
import pygame
import Map
import NPC
import DialogBox
import Monster
import Scene

class SceneManager:
    def __init__(self, window, fontSize: int = BattleSettings.textSize):
        
        self.fontSize = fontSize
        self.fontColor = (255, 0, 0)
        self.font = pygame.font.Font("C:/Windows/Fonts/STKAITI.TTF", self.fontSize)
        self.map = Map.gen_city_map()
        self.scene = Scene.MainMenuScene(window)#初始界面

        self.tot = 0
        self.refreshtot = 0
        self.refreshtext = ""
        self.text = ""
        self.refreshCoins = PropSettings.refreshcoins
        self.wave = 0

        self.obstacles = Map.gen_obstacles()
        self.npcs = pygame.sprite.Group()
        self.npcs.add(NPC.NPC(WindowSettings.width // 4, WindowSettings.height // 4 + 80),
                      NPC.copperbox(WindowSettings.width // 3 *2-100, WindowSettings.height // 4 + 180),
                      NPC.merchant(WindowSettings.width // 3 *2, WindowSettings.height // 4 + 80),
                      NPC.silverbox(WindowSettings.width // 3 *2, WindowSettings.height // 4 + 180),
                      NPC.goldenbox(WindowSettings.width // 3 *2 +100, WindowSettings.height // 4 + 230),
                      ) 
        self.window = window

    def get_width(self):
        return WindowSettings.width 

    def get_height(self):
        return WindowSettings.height
    
    def reset_shop(self):
        self.tot = 0
        self.refreshtot = 0
        self.refreshtext = ""
        self.text = ""
        self.refreshCoins = PropSettings.refreshcoins
        for npc in self.npcs.sprites():
            if npc.type == NPCType.COPPERBOX or npc.type == NPCType.SILVERBOX or npc.type == NPCType.GOLDENBOX:
                npc.reset()

    def check_event_talking(self, player, keys):
        # check for all npcs
        for npc in self.npcs.sprites():
            # 结束对话
            if npc.talking and keys[pygame.K_q]:
                npc.talking = False
                player.talking = False
                npc.reset_talk_CD()
            # 保持对话
            elif pygame.sprite.collide_rect(player, npc) and npc.can_talk():
                npc.talking = True
                player.talking = True
                if npc.type == NPCType.NPC:
                    dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.npc,
                        ["Gary, Karina被怪物抓走了,进入传送门前往成都打败怪物把她救出来","","按q退出谈话"])
                    
                elif npc.type == NPCType.MERCHANT:
                    self.refreshtot += 1
                    dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant,
                        [f"按ENTER键花费 {str(-self.refreshCoins)} 元刷新宝箱","","刷新完按q退出","",self.refreshtext])
                    
                    if keys[pygame.K_RETURN] and self.refreshtot > 20:
                        for npc in self.npcs.sprites():
                            if npc.type == NPCType.COPPERBOX or npc.type == NPCType.SILVERBOX or npc.type == NPCType.GOLDENBOX:

                                self.refreshtext,self.refreshCoins = npc.refresh(player)
                                self.refreshtot = 0
                        npc.talking = False
                        player.talking = False
                        npc.reset_talk_CD()

                elif npc.type == NPCType.GOLDENBOX:
                    npc.wave = self.wave
                    dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant,
                        ["充值10元解锁该宝箱",""])
                    
                elif npc.type == NPCType.COPPERBOX or npc.type == NPCType.SILVERBOX:
                    npc.wave = self.wave
                    self.tot += 1
                    
                    dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant,
                        [npc.text,"",self.text])
                    if keys[pygame.K_RETURN] and self.tot > 20:
                        self.text = npc.buy(player)
                        self.tot = 0
                dialogBoxTemp.render()
                
    
    def flush_scene(self,dest):
        if dest == GameState.GAME_PLAY_WILD:
            self.scene = Scene.WildScene(self.window)
        elif dest == GameState.GAME_PLAY_CITY:
            self.scene = Scene.CityScene(self.window)
        elif dest == GameState.GAME_OVER:
            self.scene = Scene.GameoverScene(self.window)
        self.scene.render()

    def render_mainmenu(self):
        self.scene.render()

    def render_wild_scene(self,player,wave):
        self.scene.render()
        textHP = "血量: " + str(player.HP)
        textwave = "第" + str(wave) +"波"
        textAttack = "攻击力" + str(player.Attack)
        textMoney = "金币: " + str(player.Money)
        self.write(textHP,1120,10)
        self.write(textwave,500,10)
        self.write(textAttack,1120,42)
        self.write(textMoney,1120,70)

    def render_city_scene(self,player):
        self.scene.render()
        textHP = "血量: " + str(player.HP)
        textAttack = "攻击力" + str(player.Attack)
        textMoney = "金币: " + str(player.Money)
        self.write(textHP,1120,10)
        self.write(textAttack,1120,42)
        self.write(textMoney,1120,70)
        
    def write(self,text,x,y):
        self.window.blit(self.font.render(text, True,self.fontColor),
                        (x, y))  

    def update_npc(self):
        # update npc
        for each in self.npcs.sprites():
            each.update()      

        # TODO

    
