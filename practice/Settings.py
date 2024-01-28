
# -*- coding:utf-8 -*-

from enum import Enum
import pygame

class WindowSettings:
    name = "Dungeon Breakers"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class ClockSettings:
    clock = 26

class WeaponSettings:
    weaponWidth = 55
    weaponHeight = 40
    offsetx = 25
    offsetx2 = 15
    offsety = 20

class TimeSettings:
    firstcount = 20
    secondcount = 25
    thirdcount = 30
    fourthcount = 45
    bosscount = 120

class BulletSettings:
    bulletSpeed = 30
    bulletWidth = 40
    bulletHeight = 70
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
    playerWidth = 70
    playerHeight = 65
    playerHP = 20
    playerAttack = 2
    playerDefence = 1
    playerMoney = 40
    playerAttackspeed = 6

class NPCSettings:
    npcSpeed = 1
    dogSpeed = 2
    npcWidth = 80
    npcHeight = 80
    boxWidth = 30
    boxHeight = 30
    talkCD = 75           # 1s

class MonsterSettings:
    initialmonsternum = 6
    monsterWidth = 65
    monsterHeight = 65
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
    hulkHP = 40
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
    bossSpeed = 3.5
    bossAttack = 10
    bossbulletattack = 3
    bossbulletattackspeed = 80
    bossshockwaveattack = 6
    bossswattackspeed = 60
    initialbossnum = 1


class SceneSettings:
    tileXnum = 48
    tileYnum = 27
    tileWidth = tileHeight = 40
    obstacleDensity = 0.01

class MenuSettings:
    textSize = 36
    blinkInterval = 15

class SceneType(Enum):
    CITY = 1
    WILD = 2
    WIN = 3
    MAIN = 4
    OVER = 5
    BADENDING = 6
    GOODENDING = 7

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
    PAPERBOX = 6
    MERCHANT2 = 7
    DOG = 8
    NPC2 = 9
    Karina = 10

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
    growthrate = 1.2
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
    npc2 = r".\assets\npc\npc2.png"
    merchant = r".\assets\npc\merchant.png"
    merchant2 = r".\assets\npc\merchant2.png"
    karina = r".\assets\npc\karina.png"
    
    thug = r".\assets\npc\thug.png"
    hulk = r".\assets\npc\hulk.png"
    soldier = r".\assets\npc\soldier.png"
    monster = r".\assets\npc\monster\1.png"
    boss = r".\assets\npc\boss.png"
    bullet = r".\assets\bullets\bullet1.png"
    monsterbullet = r".\assets\bullets\bullet2.png"
    bossbullet = r".\assets\bullets\bossbullet.png"
    bossshockwave = r".\assets\bullets\bossbullet2.png"

    dog = [
        r".\assets\dog\dog1.png",
        r".\assets\dog\dog2.png",
        r".\assets\dog\dog3.png",
        r".\assets\dog\dog4.png",
        r".\assets\dog\dog5.png",
    ]

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
        r".\assets\tiles\city7.png", 
        r".\assets\tiles\city8.png", 
        r".\assets\tiles\city9.png", 
        r".\assets\tiles\city10.png", 

    ]

    cityTiles = [
        r".\assets\tiles\city1.png", 
        r".\assets\tiles\city2.png", 
        r".\assets\tiles\city3.png", 
        r".\assets\tiles\city4.png", 
        r".\assets\tiles\city5.png", 
        r".\assets\tiles\city6.png", 
        r".\assets\tiles\city7.png", 
        r".\assets\tiles\city8.png", 
        r".\assets\tiles\city9.png", 
        r".\assets\tiles\city10.png", 
    ]

    winmapTiles = [
        r".\assets\tiles\winmap1.png", 
        r".\assets\tiles\winmap2.png", 
        r".\assets\tiles\winmap3.png", 
        r".\assets\tiles\winmap4.png", 
        r".\assets\tiles\winmap5.png", 
        r".\assets\tiles\winmap6.png", 
        r".\assets\tiles\city7.png", 
        r".\assets\tiles\city8.png", 
        r".\assets\tiles\city9.png", 
        r".\assets\tiles\city10.png", 

    ]

    obstacles = [
        r".\assets\tiles\tree.png",
        r".\assets\tiles\desk.png",
        r".\assets\tiles\column.png",
    ]
    copperbox = r".\assets\others\copperbox.png"
    silverbox = r".\assets\others\silverbox.png"
    goldenbox = r".\assets\others\goldenbox.png"

    menu = r".\assets\others\menu.gif"
    gameover = r".\assets\others\gameover.png"
    badending = r".\assets\others\badending.png"
    goodending = r".\assets\others\goodending.png"
    
    portal = r".\assets\others\portal.png"

    city = r".\assets\bgm\city.mp3"
    fighting = r".\assets\bgm\fighting.mp3"
    defeat = r".\assets\bgm\defeat.mp3"
    fire = r".\assets\bgm\fire.wav"

class GameState(Enum):
    MAIN_MENU = 1
    GAME_LOADING = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_QUIT = 7
    GAME_PLAY_CITY = 8
    GAME_BADENDING = 9
    GAME_GOODENDING = 10

###新加beattacked,citydialog,windialog
class GameEvent:
    EVENT_LOSE = pygame.USEREVENT + 1
    EVENT_DIALOG1 = pygame.USEREVENT + 2
    EVENT_FIGHT = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5
    EVENT_ENDFIGHT = pygame.USEREVENT +6
    EVENT_QT = pygame.USEREVENT +7
    EVENT_WIN = pygame.USEREVENT +8
    EVENT_GOODENDING = pygame.USEREVENT + 9
    EVENT_BADENDING = pygame.USEREVENT + 10
    EVENT_BEATTACKED = pygame.USEREVENT + 11
    EVENT_CITYDIALOG = pygame.USEREVENT + 13
    EVENT_WINDIALOG = pygame.USEREVENT + 14

