# -*- coding:utf-8 -*-

from typing import *
from Attributes import *
from Settings import *
from SceneManager import SceneManager
from Scene import Scene
from Scene import CityScene
from Scene import WildScene
from Player import Player
from Weapon import Weapon
from BgmPlayer import BgmPlayer

import pygame
import math
import random
import sys

import Bullet
import Map
import Monster
import prop

def distance(a,b,c,d):
    return math.sqrt((a-c)**2+(b-d)**2)

class GameManager:
    def __init__(self,window):

        self.state = GameState.MAIN_MENU
        self.scene = SceneManager(window)
        self.tot = 0
        self.attackspeed = 0 #控制攻速的变量，并非攻速
        self.bgm = BgmPlayer()

        self.player = Player(WindowSettings.width // 2, WindowSettings.height // 2)
        self.weapon = Weapon(WindowSettings.width // 2 , WindowSettings.height // 2 )

        self.npcs = pygame.sprite.Group()
        self.npcs = self.scene.npcs.copy()

        self.obstacles = Map.gen_obstacles()
        self.window = window
        self.screen = Scene(window)
        self.cityscene = CityScene(window)
        self.wildscene = WildScene(window)

        self.monsternum = MonsterSettings.initialmonsternum
        self.thugnum = ThugSettings.initialthugnum
        self.hulknum = HulkSettings.initialhulknum
        self.soldiernum = SoldierSettings.initialsoldiernum
        self.bossnum = BossSettings.initialbossnum
        self.ifthug = 0
        self.ifhulk = 0
        self.ifsoldier = 0
        self.ifboss = 0
        self.ifmonsterstronger = 0

        self.soldierfrequency = 0
        self.monsterfrequency = 0
        self.bossswfrequency = 0
        self.bossbulletfrequency = 0

        self.count = TimeSettings.firstcount
        self.monsterwavecount = 0 #如果没打完，每7秒出一波怪
        self.monsterwave = 0
        self.wave = 1
        self.prop = prop.prop()

        self.monsters = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsterbullets = pygame.sprite.Group()
        self.bossbullets = pygame.sprite.Group()
        self.bossshockwaves = pygame.sprite.Group()
        self.battleBox = None

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

    def monsterfire(self,x,y,type):
        playerx = self.player.get_posx()
        playery = self.player.get_posy()
        t = math.sqrt((playery-y)**2 + (playerx-x)**2)
        if t != 0:
            if type == BulletType.Soldier:
                new_bullet = Bullet.MonsterBullet(x,y,(playery-y)/t,(playerx-x)/t)
                self.monsterbullets.add(new_bullet)
            elif type == BulletType.Boss:
                new_bullet = Bullet.BossBullet(x,y,(playery-y)/t,(playerx-x)/t)
                self.bossbullets.add(new_bullet)
            elif type == BulletType.Shockwave:
                new_bullet = Bullet.BossShockwave(x,y,(playery-y)/t,(playerx-x)/t)
                self.bossshockwaves.add(new_bullet)
        else:
            if type == BulletType.Soldier:
                new_bullet = Bullet.MonsterBullet(x,y,0,1)
                self.monsterbullets.add(new_bullet)     
            elif type == BulletType.Boss:
                new_bullet = Bullet.BossBullet(x,y,0,1)
                self.bossbullets.add(new_bullet)
            elif type == BulletType.Shockwave:
                new_bullet = Bullet.BossShockwave(x,y,0,1)
                self.bossshockwaves.add(new_bullet)

    def update(self):
        if self.state == GameState.GAME_QUIT:
            pygame.quit()
            sys.exit()
        # 战斗结束，进入商店
        elif self.state == GameState.GAME_PLAY_CITY:    
            self.update_city()
            self.stop_monster()
            self.stop_bullet()
            #商店结束，进入战斗
        ####这里调换了顺序
        elif self.state == GameState.GAME_PLAY_WILD:
            self.update_wild()
            self.timing()
        elif self.state == GameState.GAME_WIN:
            self.update_win()
            self.stop_monster()
            self.stop_bullet()

    def update_city(self):
        keys = pygame.key.get_pressed()
        self.player.try_move(keys)
        self.update_collide()
        self.player.update(keys,self.player.collidingWith["obstacle"] )
        self.weapon.update(self.player)
        if keys[pygame.K_k]:
            self.player.facai()
        for each in self.npcs.sprites():
            if each.type != NPCType.Karina:
                each.update()
        self.check_collideevent()

    ####更新碰撞，更新碰撞对应事件
    def update_win(self):
        keys = pygame.key.get_pressed()
        self.player.try_move(keys)
        self.update_collide()
        self.check_collideevent()
        self.player.update(keys)
        for each in self.npcs.sprites():
            if each.type == NPCType.Karina or each.type == NPCType.DOG :
                each.update()

    ####更新碰撞，更新碰撞对应事件
    def update_wild(self):
        # update npc,monster,bullet
        keys = pygame.key.get_pressed()
        self.player.try_move(keys)
        self.update_collide()
        self.player.update(keys,self.player.collidingWith["obstacle"] )
        self.weapon.update(self.player)
        self.check_collideevent()
        self.attackspeed += 1
        if keys[pygame.K_SPACE]:     #按空格键开火                               
            if self.attackspeed > self.player.Attackspeed: 
                self.bgm.play(GamePath.fire,1)
                self.fire(self.player.get_posx(),self.player.get_posy())
                self.attackspeed = 0   

        for each in self.bullets.sprites():
            each.update()
        for each in self.monsterbullets.sprites():
            each.update()
        for each in self.bossbullets.sprites():
            each.update()
        for each in self.bossshockwaves.sprites():
            each.update()
        
        for each in self.monsters.sprites():
            each.update(self.player.get_posx(),self.player.get_posy())

        self.gen_monster()
        self.update_bullet()
        self.update_monsterbullet()
        self.update_monster()
        self.update_soldier()
        self.update_boss()
        self.ifplayerdie()
        

    def ifplayerdie(self):
        if self.player.HP <= 0:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_LOSE))
     
    def gen_monster(self):
        if self.monsterwavecount >= 7 :
            if self.monsterwave * 7 + self.count <= 30:
                self.add_monster()
            self.monsterwavecount = 0
        if len(self.monsters.sprites()) < 1 :
            self.add_monster()
            self.monsterwave += 1

    def add_monster(self):
        for _ in range(self.thugnum * self.ifthug ):
            self.monsters.add(Monster.Thug(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))

        for _ in range(self.hulknum * self.ifhulk ):
            self.monsters.add(Monster.Hulk(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))

        for _ in range(self.soldiernum * self.ifsoldier ):
            self.monsters.add(Monster.Soldier(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))     
        for _ in range(self.monsternum):
            self.monsters.add(Monster.Monster(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))
        for _ in range(self.bossnum * self.ifboss):
            self.ifboss = 0
            self.monsters.add(Monster.Boss(random.randrange(5,WindowSettings.width-5), random.randrange(1,WindowSettings.height-1)))        
    
        if self.ifmonsterstronger:
            self.monster_stronger()

    def update_bullet(self):
         #消除碰到怪物的子弹        
        for monster in self.monsters.copy():
            if pygame.sprite.spritecollide(monster,self.bullets, False):
                for bullet in self.bullets.copy():
                    if pygame.sprite.spritecollide(bullet,self.monsters, False): #怪被子弹击中了，减血
                        monster.wasattacked(self.player.get_attack())
                        if monster.HP <= 0 :
                            if monster.type == MonsterType.Boss:
                                pygame.event.post(pygame.event.Event(GameEvent.EVENT_WIN))
                            self.player.Money += monster.money
                            self.monsters.remove(monster)
                        self.bullets.remove(bullet)

        for bullet in self.bullets.copy():
            #消除屏幕外的子弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= WindowSettings.height or bullet.rect.right >= WindowSettings.width or bullet.rect.left <= 0:
                self.bullets.remove(bullet)
            #消除碰到障碍物的子弹
            pygame.sprite.spritecollide(bullet, self.obstacles, True)

    def update_monsterbullet(self):

        for bullet in self.monsterbullets.copy():
            #消除屏幕外的子弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= WindowSettings.height or bullet.rect.right >= WindowSettings.width or bullet.rect.left <= 0:
                self.monsterbullets.remove(bullet)
            #消除碰到障碍物的子弹
            pygame.sprite.spritecollide(bullet, self.obstacles, True)

        for bullet in self.bossshockwaves.copy():
            #消除屏幕外的冲击波
            if bullet.rect.bottom <= 0 or bullet.rect.top >= WindowSettings.height or bullet.rect.right >= WindowSettings.width or bullet.rect.left <= 0:
                self.bossshockwaves.remove(bullet)

        for bullet in self.bossbullets.copy():
            #子弹碰库反弹
            if bullet.rect.bottom <= 0 or bullet.rect.top >= WindowSettings.height or bullet.rect.right >= WindowSettings.width or bullet.rect.left <= 0:
                bullet.turn()

            pygame.sprite.spritecollide(bullet, self.obstacles, True)
        
    def update_monster(self):
        self.monsterfrequency += 1

    def update_soldier(self):
        self.soldierfrequency += 1
        if self.soldierfrequency > SoldierSettings.soldierattackspeed:
            self.soldierfrequency = 0
            for monster in self.monsters.copy():
                if monster.type == MonsterType.Soldier:
                    self.monsterfire(monster.get_posx(),monster.get_posy(),BulletType.Soldier)

    def update_boss(self):
        self.bossswfrequency += 1
        if self.bossswfrequency > BossSettings.bossswattackspeed:
            self.bossswfrequency = 0
            for monster in self.monsters.copy():
                if monster.type == MonsterType.Boss:
                    self.monsterfire(monster.get_posx(),monster.get_posy(),BulletType.Shockwave)   

        self.bossbulletfrequency += 1
        if self.bossbulletfrequency > BossSettings.bossbulletattackspeed:
            self.bossbulletfrequency = 0
            for monster in self.monsters.copy():
                if monster.type == MonsterType.Boss:
                    self.monsterfire(monster.get_posx(),monster.get_posy(),BulletType.Boss)  

    def initplayer(self):
        self.player.rect.x,self.player.rect.y = WindowSettings.width // 2, WindowSettings.height // 2
        self.weapon.rect.x,self.player.rect.y = WindowSettings.width // 2, WindowSettings.height // 2

    def reset(self):
        self.monsternum = MonsterSettings.initialmonsternum
        self.thugnum = ThugSettings.initialthugnum
        self.hulknum = HulkSettings.initialhulknum
        self.soldiernum = SoldierSettings.initialsoldiernum
        self.ifthug = 0
        self.ifhulk = 0
        self.ifsoldier = 0

        self.soldierfrequency = 0
        self.monsterfrequency = 0
        self.count = TimeSettings.firstcount
        self.monsterwavecount = 0 #如果没打完，每7秒出一波怪
        self.monsterwave = 0
        self.wave = 1

        self.player.speed = PlayerSettings.playerSpeed
        self.player.talking = False

        self.player.HP = PlayerSettings.playerHP
        self.player.Attack = PlayerSettings.playerAttack
        self.player.Defence = PlayerSettings.playerDefence
        self.player.Money = PlayerSettings.playerMoney
        self.player.Attackspeed = PlayerSettings.playerAttackspeed

        self.scene.wave = 0


    def switch_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = GameState.GAME_QUIT

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN\
                and (self.state == GameState.MAIN_MENU or self.state == GameState.GAME_OVER or self.state == GameState.GAME_BADENDING or self.state == GameState.GAME_GOODENDING ):
                    self.bgm.stop()
                    self.bgm.play(GamePath.city)
                    self.scene.flush_scene(GameState.GAME_PLAY_CITY)
                    self.state = GameState.GAME_PLAY_CITY
                if event.key == pygame.K_ESCAPE\
                and (self.state == GameState.MAIN_MENU or self.state == GameState.GAME_OVER ):
                    self.state = GameState.GAME_QUIT

            elif event.type == GameEvent.EVENT_LOSE:
                self.initplayer()
                self.reset()
                self.bgm.stop()
                self.bgm.play(GamePath.defeat)
                self.state = GameState.GAME_OVER

            elif event.type == GameEvent.EVENT_WIN:
                self.scene.flush_scene(GameState.GAME_WIN)
                self.state = GameState.GAME_WIN

            elif event.type == GameEvent.EVENT_ENDFIGHT:
                self.scene.flush_scene(GameState.GAME_PLAY_CITY)
                self.bgm.stop()
                self.bgm.play(GamePath.city)
                self.state = GameState.GAME_PLAY_CITY

                self.endfight_things()
                self.scene.reset_shop()
                self.initplayer()
                self.gen_monster_logic()
                self.time_logic()

            elif event.type == GameEvent.EVENT_FIGHT:
                 self.bgm.stop()
                 self.bgm.play(GamePath.fighting)
                 self.initplayer()
                 self.scene.flush_scene(GameState.GAME_PLAY_WILD)
                 self.state = GameState.GAME_PLAY_WILD

            elif event.type == GameEvent.EVENT_BADENDING:
                self.initplayer()
                self.reset()
                self.scene.reset()
                self.scene.flush_scene(GameState.GAME_BADENDING)
                self.state = GameState.GAME_BADENDING

            elif event.type == GameEvent.EVENT_GOODENDING:
                self.initplayer()
                self.reset()
                self.scene.reset()
                self.scene.flush_scene(GameState.GAME_GOODENDING)
                self.state = GameState.GAME_GOODENDING
    
    ####检测不同碰撞事件
    def check_collideevent(self):
        for event in pygame.event.get():
            if event.type == GameEvent.EVENT_CITYDIALOG and self.state != GameState.GAME_WIN:
                keys = pygame.key.get_pressed()
                self.scene.check_event_talking1(self.player, self.player.collidingObject["npc"], keys)

            elif event.type == GameEvent.EVENT_BEATTACKED:
                monsterattack = SoldierSettings.soldierAttack
                bossbulletattack = BossSettings.bossbulletattack
                bossshockwaveattack = BossSettings.bossshockwaveattack

                if self.player.collidingWith["monsterbullet"]:
                    self.player.wasattacked(monsterattack)
                if self.player.collidingWith["bossbullet"]:
                    self.player.wasattacked(bossbulletattack)
                if self.player.collidingWith["bossshockwave"]:
                    self.player.wasattacked(bossshockwaveattack)
                if self.player.collidingWith["monster"]:
                    self.player.wasattacked(self.player.collidingObject["monster"].Attack)
                    self.monsterfrequency = 0
            
            elif event.type == GameEvent.EVENT_WINDIALOG and self.state == GameState.GAME_WIN:
                keys = pygame.key.get_pressed()
                self.scene.check_event_talking2(self.player, self.player.collidingObject["npc"], keys)


    def endfight_things(self):
        self.wave += 1
        self.scene.wave += 1     
        self.monsterwave = 0
        self.monsterwavecount = 0

    def time_logic(self):
        if self.wave < 3:
            self.count = TimeSettings.firstcount
        elif self.wave >= 3 and self.wave < 5:
            self.count = TimeSettings.secondcount
        elif self.wave >= 5 and self.wave < 7:
            self.count = TimeSettings.thirdcount
        elif self.wave >= 7 :
            self.count = TimeSettings.fourthcount

    def monster_stronger(self):
        for monster in self.monsters.copy():
            monster.stronger()
            monster.faster()
            
    def gen_monster_logic(self): #出怪逻辑
        if self.wave == 2:
            self.ifthug = 1
            self.monsternum += 1
        elif self.wave == 3:
            self.ifsoldier = 1        
            self.thugnum += 1
        elif self.wave == 4:
            self.ifmonsterstronger = 1
            self.ifhulk = 1
            self.thugnum += 2
        elif self.wave == 5:
            self.monsternum += 1
            self.soldiernum += 1
        elif self.wave == 6:
            self.hulknum += 1
            self.thugnum += 1
            self.soldiernum += 1
        elif self.wave == 7:
            self.thugnum = 2
            self.hulknum = 2
            self.soldiernum = 2
            self.monsternum = 3
            self.ifboss = 1

    
    def render(self):
        if self.state == GameState.GAME_QUIT:
                pygame.quit()
                sys.exit()
            # 战斗结束，进入商店
        elif self.state == GameState.GAME_PLAY_CITY:
                self.stop_monster()
                self.player.draw(self.window)
                self.render_city()
            #商店结束，进入战斗
        elif self.state == GameState.GAME_PLAY_WILD:
            self.render_wild()
            self.scene.write("倒计时: "+str(self.count),500,50)

        elif self.state == GameState.GAME_WIN:
            self.stop_monster()
            self.player.draw(self.window)
            self.render_win()

        elif self.state == GameState.MAIN_MENU:
            self.scene.render_mainmenu()

        elif self.state == GameState.GAME_OVER:
            self.scene.flush_scene(GameState.GAME_OVER)

    def render_wild(self):
        self.scene.render_wild_scene(self.player,self.wave,self.bullets, self.bossbullets, self.monsterbullets,self.monsters)
        self.monsters.draw(self.window)
        self.bullets.draw(self.window)
        self.bossbullets.draw(self.window)
        self.monsterbullets.draw(self.window)
        self.bossshockwaves.draw(self.window)

        self.player.draw(self.window)
        self.weapon.draw(self.window)
        
    ####渲染对话框
    def render_city(self):
        self.scene.render_city_scene(self.player)
        self.player.draw(self.window)
        self.weapon.draw(self.window)

        for npc in self.npcs.copy():
            if npc.type != NPCType.Karina:
                npc.draw(self.window)

        self.scene.update_npc()
        if self.player.talking:
            self.render_dialogBox()

    def render_win(self):
        self.scene.render_win_scene(self.player)
        self.player.draw(self.window)
        for npc in self.npcs.copy():
            if npc.type == NPCType.Karina or npc.type == NPCType.DOG:
                npc.draw(self.window)

        self.scene.update_npc()
        if self.player.talking:
            self.render_dialogBox()

    def timing(self):
        self.tot += 1
        if self.tot >= ClockSettings.clock:
            self.count -=1
            self.monsterwavecount += 1
            self.tot = 0
        if self.count <= 0:
            pygame.event.post(pygame.event.Event(GameEvent.EVENT_ENDFIGHT))

    def stop_monster(self):
        for monster in self.monsters.copy():
            self.monsters.remove(monster)

    def stop_bullet(self):
        for bullet in self.bullets.copy():
            self.bullets.remove(bullet)
        for bullet in self.monsterbullets.copy():
            self.monsterbullets.remove(bullet)            

    #获得group中的一个随机怪物
    def getmonster(self):
        return random.choice(self.monsters.sprites())

        # TODO
    
    ####更新玩家碰撞状态
    def update_collide(self):
        Collidable.__init__(self.player)
 
        # Player -> Obstacles
        ##### Your Code Here ↓ #####
        if pygame.sprite.spritecollide(self.player, self.scene.scene.obstacles, False):
                # 遇到障碍物，取消移动
            self.player.collidingWith["obstacle"] = True 
        ##### Your Code Here ↑ #####

        # Player -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        ##### Your Code Here ↓ #####
        for npc in self.scene.npcs:
            if pygame.sprite.collide_rect(self.player, npc) :
                if self.state == GameState.GAME_PLAY_CITY:
                    self.player.collidingWith["npc"] = True 
                    self.player.collidingObject["npc"] = npc
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_CITYDIALOG))

        for npc in self.scene.npcs:
            if pygame.sprite.collide_rect(self.player, npc) :
                if self.state == GameState.GAME_WIN:
                    self.player.collidingWith["npc"] = True 
                    self.player.collidingObject["npc"] = npc
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_WINDIALOG))
        ##### Your Code Here ↑ #####

        # Player -> Monsters
        ##### Your Code Here ↓ #####
        for monster in self.monsters.copy():
            if pygame.sprite.collide_rect(self.player, monster):
                if self.state == GameState.GAME_PLAY_WILD:
                    if self.monsterfrequency > 10:
                        pygame.event.post(pygame.event.Event(GameEvent.EVENT_BEATTACKED))
                        self.player.collidingWith["monster"] = True
                        self.player.collidingObject["monster"] = monster
        ##### Your Code Here ↑ #####
        
        # Player -> Portals
        ##### Your Code Here ↓ #####
        if pygame.sprite.spritecollide(self.player, self.cityscene.portals, 
                                    False, pygame.sprite.collide_mask):
            if self.state == GameState.GAME_PLAY_CITY:
                self.player.collidingWith["portal"] = True 
                self.player.collidingObject["portal"] = self.cityscene.portals
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_FIGHT))
                self.switch_state()
        ##### Your Code Here ↑ #####
        
        # Player -> Bullet
        ##### Your Code Here ↓ #####
        if pygame.sprite.spritecollide(self.player,self.monsterbullets, True): 
            if self.state == GameState.GAME_PLAY_WILD:#人物被子弹击中了，减血
                self.player.collidingWith["monsterbullet"] = True 
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_BEATTACKED))

        if pygame.sprite.spritecollide(self.player,self.bossbullets, True):
            if self.state == GameState.GAME_PLAY_WILD:
                self.player.collidingWith["bossbullet"] = True 
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_BEATTACKED))

        if pygame.sprite.spritecollide(self.player,self.bossshockwaves, True):
            if self.state == GameState.GAME_PLAY_WILD:
                self.player.collidingWith["bossshockwave"] = True 
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_BEATTACKED))

        ##### Your Code Here ↑ #####


    ####渲染对话框
    def render_dialogBox(self):
        self.scene.dialogBoxTemp.render()

    
