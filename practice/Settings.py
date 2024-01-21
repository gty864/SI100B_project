
# -*- coding:utf-8 -*-

from enum import Enum
import pygame

class WindowSettings:
    name = "Thgink Luos"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class ClockSettings:
    clock = 26

class WeaponSettings:
    weaponWidth = 35
    weaponHeight = 20
    offsetx = 25
    offsetx2 = 15
    offsety = 20

class TimeSettings:
    firstcount = 25
    secondcount = 30
    thirdcount = 40
    fourthcount = 50
    bosscount = 120

class BulletSettings:
    bulletSpeed = 30
    bulletWidth = 30
    bulletHeight = 60
    monsterbulletWidth = 30
    monsterbulletHeight = 30

class MonsterBulletSettings:
    monsterbulletSpeed = 15

class BossBulletSettings:
    bossbulletSpeed = 18

class BossshockwaveSettings:
    bossshockwaveSpeed = 15
    bossshockwaveHeight = 200
    bossshockwaveWidth = 30

class PlayerSettings:
    playerSpeed = 8
    playerWidth = 50
    playerHeight = 45
    playerHP = 20
    playerAttack = 2
    playerDefence = 1
    playerMoney = 40
    playerAttackspeed = 6

class NPCSettings:
    npcSpeed = 1
    npcWidth = 60
    npcHeight = 60
    boxWidth = 30
    boxHeight = 30
    talkCD = 30           # 1s

class MonsterSettings:
    initialmonsternum = 5
    monsterWidth = 45
    monsterHeight = 45
    monsterSpeed = 1.5
    monsterHP = 12
    monsterAttack = 1
    monsterMoney = 2

class ThugSettings:
    thugHP = 8
    thugSpeed = 5
    thugAttack = 2
    initialthugnum = 3
    thugMoney = 5

class HulkSettings:
    hulkHP = 50
    hulkSpeed = 3
    hulkAttack = 4
    initialhulknum = 1
    hulkchargedist = 50
    hulkchargespeed = 8
    hulkchargecd = 80
    hulkMoney = 15

class SoldierSettings:
    soldierHP = 8
    soldierSpeed = 1.2
    soldierAttack = 3
    soldierattackspeed = 20
    initialsoldiernum = 1
    soldierMoney = 7

class BossSettings:
    bossHP = 500
    bossSpeed = 1.2
    bossAttack = 10
    bossbulletattack = 3
    bossbulletattackspeed = 120
    bossshockwaveattack = 6
    bossswattackspeed = 60
    initialbossnum = 1


class SceneSettings:
    tileXnum = 36
    tileYnum = 18
    tileWidth = tileHeight = 40
    obstacleDensity = 0.01

class MenuSettings:
    textSize = 36
    blinkInterval = 15

class SceneType(Enum):
    CITY = 1
    WILD = 2
    MAIN = 3
    OVER = 4

class MonsterType(Enum):
    Monster = 1
    Thug = 2
    Soldier = 3
    Hulk = 4
    Boss = 5

class BulletType(Enum):
    Soldier = 1
    Boss = 2
    Shockwave = 3

class NPCType(Enum):
    NPC = 1
    MERCHANT = 2
    COPPERBOX = 3
    SILVERBOX = 4
    GOLDENBOX = 5

class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxAlpha = 150
    boxStartX = WindowSettings.width // 4           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20 # Coordinate Y of the box

    textSize = 30 # Default font size
    textStartX = WindowSettings.width // 4 + 10         # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3                # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20

class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 3 // 4 
    boxAlpha = 200
    boxStartX = WindowSettings.width // 8           # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 30 # Default font size
    textStartX = WindowSettings.width // 4 
    textPlayerStartX = WindowSettings.width // 4          # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 2 +100   
    textStartY = WindowSettings.height // 3         # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3            # Vertical distance of two lines

    playerWidth = WindowSettings.width // 6
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8
    playerCoordY = WindowSettings.height // 2 

    monsterWidth = WindowSettings.width // 6
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2 

    stepSize = 20

class PortalSettings:
    portalWidth = 320
    portalHeight = 320

class PropSettings:
    growthrate = 1.1
    refreshcoins = -1
    copper = 25
    silver = 15
    gold = 5


class GamePath:
    # player/npc related path
    player = [
        r".\assets\player\1.png", 
        r".\assets\player\2.png", 
        r".\assets\player\3.png", 
        r".\assets\player\4.png", 
        r".\assets\player\5.png", 
        r".\assets\player\6.png", 
        r".\assets\player\7.png", 
        r".\assets\player\8.png", 
    ]
    npc = r".\assets\npc\npc.png"
    merchant = r".\assets\npc\merchant.png"
    thug = r".\assets\npc\thug.png"
    hulk = r".\assets\npc\hulk.png"
    soldier = r".\assets\npc\soldier.png"
    monster = r".\assets\npc\monster\1.png"
    boss = r".\assets\npc\boss.png"
    bullet = r".\assets\bullets\bullet1.png"
    monsterbullet = r".\assets\bullets\bullet2.png"
    bossbullet = r".\assets\bullets\bossbullet.png"
    bossshockwave = r".\assets\bullets\bossbullet2.png"

    weapon = [
        r".\assets\weapons\gun.png",
        r".\assets\weapons\snowfox.png"
    ]

    groundTiles = [
        r".\assets\tiles\ground1.png", 
        r".\assets\tiles\ground2.png", 
        r".\assets\tiles\ground3.png", 
        r".\assets\tiles\ground4.png", 
        r".\assets\tiles\ground5.png", 
        r".\assets\tiles\ground6.png", 
    ]

    cityTiles = [
        r".\assets\tiles\city1.png", 
        r".\assets\tiles\city2.png", 
        r".\assets\tiles\city3.png", 
        r".\assets\tiles\city4.png", 
        r".\assets\tiles\city5.png", 
        r".\assets\tiles\city6.png", 
    ]

    copperbox = r".\assets\others\copperbox.png"
    silverbox = r".\assets\others\silverbox.png"
    goldenbox = r".\assets\others\goldenbox.png"

    menu = r".\assets\others\menu.png"
    gameover = r".\assets\others\gameover.png"
    tree = r".\assets\tiles\tree.png"
    portal = r".\assets\others\portal.png"

class GameState(Enum):
    MAIN_MENU = 1
    GAME_LOADING = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_QUIT = 7
    GAME_PLAY_CITY = 8

class GameEvent:
    EVENT_LOSE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_FIGHT = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    EVENT_ENDFIGHT = pygame.USEREVENT +6
    EVENT_QT = pygame.USEREVENT +7