# -*- coding:utf-8 -*-

from typing import *
from Settings import *

import pygame
import Map
import NPC
import DialogBox
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
        self.lastnpc = 0

        self.ifdog = False
        self.dogtot = 0
        self.badtot = 0
        self.goodtot = 0
        self.dogtextnumber = 0
        self.badtextnumber = 0
        self.goodtextnumber = 0

        self.obstacles = Map.gen_obstacles()
        self.npcs = pygame.sprite.Group()
        self.npcs.add(NPC.NPC(WindowSettings.width // 4, WindowSettings.height // 4 + 150),
                      NPC.NPC2(WindowSettings.width // 3 *2, WindowSettings.height // 3 * 2 ),
                      NPC.dog(WindowSettings.width // 4 , WindowSettings.height // 4 *3),
                      NPC.Karina(WindowSettings.width // 4 *3 , WindowSettings.height // 2),
                      NPC.copperbox(WindowSettings.width // 3 *2-150, WindowSettings.height // 4 + 80),
                      NPC.merchant(WindowSettings.width // 3 *2, WindowSettings.height // 4 - 100 ),
                      NPC.merchant2(WindowSettings.width // 3 *2-300, WindowSettings.height // 4 - 100),
                      NPC.silverbox(WindowSettings.width // 3 *2, WindowSettings.height // 4 + 80),
                      NPC.paperbox(WindowSettings.width // 3 *2-300, WindowSettings.height // 4 + 80),
                      NPC.goldenbox(WindowSettings.width // 3 *2 +150, WindowSettings.height // 4 + 80),
                      ) 
        self.window = window

        ###加了self.dialogBoxTemp
        self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.npc,
                        ["Gary, Karina被怪物抓走了","","现在唯一的办法是进入传送门前往怪物地牢打败最终boss","","按q退出谈话"])
        self.dogtextlist = ["终于解脱了","其实我是舔狗精","在天庭犯了错，被贬下凡","那个就是Karina吧","我知道你喜欢她很久了","让我来助你一臂之力吧"]
        self.badtextlist = ["Gary, 真没想到你会来救我","可我们只是朋友对吧"]

        self.goodtextlist =["Gary,谢谢你来救我","Can i be your girlfriend?"]

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
            if npc.type == NPCType.COPPERBOX or npc.type == NPCType.SILVERBOX or npc.type == NPCType.GOLDENBOX or npc.type == NPCType.PAPERBOX:
                npc.reset()

    ###加了检测碰撞npc，self.dialogBoxTemp
    def check_event_talking1(self, player, npc, keys):
            # 结束对话
            if npc.talking and keys[pygame.K_q]:
                npc.talking = False
                player.talking = False
                npc.reset_talk_CD()
            # 保持对话
            elif npc.can_talk() and npc.type != NPCType.Karina:
                npc.talking = True
                player.talking = True
                if npc.type == NPCType.NPC:
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.npc,
                        ["Gary, Karina被怪物抓走了","","现在唯一的办法是进入传送门前往怪物地牢打败最终boss","","按q退出谈话"])
                    
                elif npc.type == NPCType.NPC2:
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.npc2,
                        ["怪物地牢一共有7层","",f"加油，你已经达到了第{self.wave}层了","","最终Boss在第7层","","按q退出谈话"])              
                    
                elif npc.type == NPCType.MERCHANT2:
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant2,
                        ["欢迎来到神秘商店","","靠近宝箱按ENTER键购买商品","","旁边的是我哥，你可以找他刷新宝箱","","按q退出谈话"])
                    
                elif npc.type == NPCType.DOG:
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.dog[0],
                        ["汪 ~    汪 ~"])
                            
                elif npc.type == NPCType.MERCHANT:
                    self.refreshtot += 1
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant,
                        [f"按ENTER键花费 {str(-self.refreshCoins)} 元刷新宝箱","","旁边的是我弟，他会告诉你如何购买商品","","刷新完按q退出","",self.refreshtext])
                    
                    if keys[pygame.K_RETURN] and self.refreshtot > 20:
                        for npc in self.npcs.sprites():
                            if npc.type == NPCType.COPPERBOX or npc.type == NPCType.SILVERBOX or npc.type == NPCType.GOLDENBOX or npc.type == NPCType.PAPERBOX:

                                self.refreshtext,self.refreshCoins = npc.refresh(player)
                                self.refreshtot = 0
                        npc.talking = False
                        player.talking = False
                        npc.reset_talk_CD()

                elif npc.type == NPCType.GOLDENBOX:
                    npc.wave = self.wave
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant,
                        ["充值10元解锁该宝箱",""])
                    
                elif npc.type == NPCType.COPPERBOX or npc.type == NPCType.SILVERBOX or npc.type == NPCType.PAPERBOX:
                    if npc.type != self.lastnpc:
                        self.text = ""
                    npc.wave = self.wave
                    self.tot += 1
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.merchant,
                            [npc.text,"",self.text]) 
                    self.lastnpc = npc.type               
                    if keys[pygame.K_RETURN] and self.tot > 10:
                        self.text = npc.buy(player)
                        self.tot = 0
                #dialogBoxTemp.render()
    ####加了检测碰撞npc
    def check_event_talking2(self, player, npc, keys):
            # 结束对话
            if npc.talking and keys[pygame.K_q]:
                npc.talking = False
                player.talking = False
                npc.reset_talk_CD()
            for npcs in self.npcs.sprites():
                self.dogtot += 1
                self.badtot += 1
                self.goodtot += 1
            if npc.talking and keys[pygame.K_RETURN]:
                #npc.reset_talk_CD()
                if npc.type == NPCType.DOG:
                    if self.dogtot > 80:
                        self.dogtot = 0 
                        self.dogtextnumber += 1
                elif npc.type == NPCType.Karina:
                    if self.ifdog:
                        if self.goodtot > 80:
                            self.goodtot = 0 
                            self.goodtextnumber += 1
                    else:
                        if self.badtot > 80:
                            self.badtot = 0 
                            self.badtextnumber += 1
            # 保持对话
                
            elif npc.can_talk() and (npc.type == NPCType.Karina or npc.type == NPCType.DOG ):
                npc.talking = True
                player.talking = True

                if npc.type == NPCType.DOG:
                    self.ifdog = True
                    if self.dogtextnumber >= len(self.dogtextlist):
                        self.dogtextnumber = len(self.dogtextlist) - 1
                    self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.dog[0],
                        [self.dogtextlist[self.dogtextnumber],"","按ENTER键继续谈话"])
                    
                elif npc.type == NPCType.Karina:
                    if self.ifdog:
                        if self.goodtextnumber >= len(self.goodtextlist):
                            self.goodtextnumber = len(self.goodtextlist) - 1
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_GOODENDING))
                        self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.karina,
                                [self.goodtextlist[self.goodtextnumber],"","按ENTER键继续谈话"])
                    else:
                        if self.badtextnumber >= len(self.badtextlist):
                            self.badtextnumber = len(self.badtextlist) - 1
                            pygame.event.post(pygame.event.Event(GameEvent.EVENT_BADENDING))
                        self.dialogBoxTemp = DialogBox.DialogBox(self.window, GamePath.karina,
                            [self.badtextlist[self.badtextnumber],"","按ENTER键继续谈话"])
                    
                
    def flush_scene(self,dest):
        if dest == GameState.GAME_PLAY_WILD:
            self.scene = Scene.WildScene(self.window)
        elif dest == GameState.GAME_PLAY_CITY:
            self.scene = Scene.CityScene(self.window)
        elif dest == GameState.GAME_OVER:
            self.scene = Scene.GameoverScene(self.window)
        elif dest == GameState.GAME_WIN:
            self.scene = Scene.WinScene(self.window)
        elif dest == GameState.GAME_BADENDING:
            self.scene = Scene.BadendingScene(self.window)
        elif dest == GameState.GAME_GOODENDING:
            self.scene = Scene.GoodendingScene(self.window)
        self.scene.render()

    def render_mainmenu(self):
        self.scene.render()

    def render_wild_scene(self,player,wave, bullets, bossbullets, monsterbullets,monsters ):
        self.scene.update_camera(player,bullets, bossbullets, monsterbullets,monsters)
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

    def render_win_scene(self,player):
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

    def reset(self):
        self.ifdog = False
        self.dogtot = 0
        self.badtot = 0
        self.goodtot = 0
        self.dogtextnumber = 0
        self.badtextnumber = 0
        self.goodtextnumber = 0


        # TODO

    
